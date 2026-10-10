# Threading Migration Plan: `sys`/`mt` → `std::thread` Primitives

**Scope:** `modules/c++/sys`, `modules/c++/mt`, `modules/c++/net` (dependents)
**C++ standard floor:** C++14 (unchanged — no `std::jthread`/`std::counting_semaphore`/`std::shared_mutex`)
**CPU affinity/pinning:** Out of scope — left completely unchanged
**API compatibility:** Breaking change accepted — this is a full migration, not a parallel/opt-in path

## 1. Motivation

The `sys` module currently implements its own thread/mutex/condition-variable/semaphore
abstractions, each with hand-written Windows (`*Win32`) and POSIX (`*Posix`) backends
selected at compile time via preprocessor dispatch:

```cpp
#if defined(_WIN32)
  using Thread = ThreadWin32;
#elif defined(CODA_OSS_POSIX_SOURCE)
  using Thread = ThreadPosix;
#else
  #error "Which thread package?"
#endif
```

This pattern predates C++11's standard threading library and was necessary when the
project's minimum standard was C++03/98. The project's floor has been C++14 for some
time, and three of the four primitives (`AtomicCounter`, `mt::Singleton`'s mutex, and
`mt::Algorithm`'s task-based parallelism) have already migrated to `std::` facilities
organically. A dormant, unused `sys::MutexCpp11` class (wrapping `std::mutex`) already
exists in the tree — someone began this exact migration previously and stopped because
`ConditionVar`'s POSIX/Win32 implementations reach into `Mutex`'s native handle, which
`std::mutex` doesn't portably expose.

This document finishes that migration for all four primitives, plus `Thread`, and
quantifies how much platform-specific code is eliminated as a result.

## 2. Design Decisions

| Question | Decision |
|---|---|
| Scope | Full migration: `Thread`, `Mutex`, `ConditionVar`, `Semaphore`, `ReadWriteMutex` |
| API breakage | Accepted. `sys::Thread` becomes `final` (non-inheritable); current subclassers move to composition. |
| C++ standard | C++14 preserved. `Semaphore` and `ReadWriteMutex` get hand-rolled `std::mutex`+`std::condition_variable` implementations since `std::counting_semaphore`/`std::shared_mutex` require C++20/17. |
| CPU affinity / pinning | Out of scope, unaffected. `sys::Thread` continues to expose `std::thread::native_handle()`, so `mt::ThreadGroup`'s `pinToCPU`, `CPUAffinityInitializerLinux`, and `ScopedCPUAffinityUnix` keep working unchanged (glibc/libstdc++ backs `std::thread` with a real `pthread_t`). |

## 3. Per-Primitive Migration

### 3.1 `sys::Mutex`

**Deleted:** `MutexInterface.h`, `MutexPosix.{h,cpp}`, `MutexWin32.{h,cpp}`, `MutexCpp11.{h,cpp}` (dormant, folded into the new implementation).

**Replacement:** A single, portable `sys::Mutex` wrapping `std::mutex` directly. No
virtual dispatch is needed since nothing outside `sys/` subclasses `MutexInterface`.

```cpp
namespace sys {
class Mutex final {
    std::mutex mNative;
public:
    Mutex() = default;
    Mutex(const Mutex&) = delete;
    Mutex& operator=(const Mutex&) = delete;
    void lock() { mNative.lock(); }
    void unlock() { mNative.unlock(); }
    std::mutex& getNative() { return mNative; } // consumed internally by ConditionVar
};
}
```

`mt::CriticalSection<sys::Mutex>` (used by `ThreadGroup`, `ExceptionLogger`, several
tests) requires **no changes** — it only calls `lock()`/`unlock()`.

### 3.2 `sys::ConditionVar`

Must migrate in the same change as `Mutex` — this is precisely the coupling that
blocked the dormant `MutexCpp11` migration. The POSIX/Win32 `ConditionVar`
implementations both call `Mutex::getNative()` to obtain the raw `pthread_mutex_t`/
`HANDLE` needed by `pthread_cond_wait`/the hand-rolled Win32 condvar emulation. Once
`Mutex::getNative()` returns `std::mutex&` instead, `ConditionVar` can wrap
`std::condition_variable` directly and the coupling resolves naturally — `std::condition_variable` only ever works with `std::mutex` anyway.

**Deleted:** `ConditionVarInterface.h`, `ConditionVarPosix.{h,cpp}`,
`ConditionVarWin32.{h,cpp}` (including ~230 lines of hand-rolled pre-Vista Windows
condition-variable emulation based on the "Strategies for Implementing POSIX Condition
Variables on Win32" pattern — entirely obsolete).

**Replacement:** `sys::ConditionVar` preserves its exact current public API
(`acquireLock()`, `dropLock()`, `wait()`, `wait(double)`, `signal()`, `broadcast()`,
plus both the "owns its mutex" and "shares an external mutex" constructor forms used by
`mt::RequestQueue`/`mt::OrderedRequestQueue`), internally built from
`std::condition_variable` + `std::unique_lock<std::mutex>`:

- `wait()` → `std::condition_variable::wait(lock)`
- `wait(double seconds)` → `std::condition_variable::wait_for(lock, duration)`
- `signal()` / `broadcast()` → `notify_one()` / `notify_all()`

No semantic change for any caller — the "caller must hold the lock before calling
`wait()`" contract documented in the current interface is preserved exactly.

### 3.3 `sys::Semaphore`

`std::counting_semaphore` is C++20-only, so with the C++14 floor preserved, this
primitive is hand-rolled from `std::mutex` + `std::condition_variable` + a counter — a
well-known ~15-line pattern:

```cpp
namespace sys {
class Semaphore final {
    std::mutex mMutex;
    std::condition_variable mCv;
    size_t mCount;
public:
    explicit Semaphore(size_t count = 0) : mCount(count) {}
    void wait() {
        std::unique_lock<std::mutex> lock(mMutex);
        mCv.wait(lock, [this]{ return mCount > 0; });
        --mCount;
    }
    void signal() {
        std::unique_lock<std::mutex> lock(mMutex);
        ++mCount;
        mCv.notify_one();
    }
};
}
```

**Deleted:** `SemaphoreInterface.h`, `SemaphorePosix.{h,cpp}`, `SemaphoreWin32.{h,cpp}`.
This also removes the macOS-specific exclusion (`!defined(__APPLE_CC__)`) in
`SemaphorePosix.h` that worked around unnamed POSIX semaphores being deprecated on
macOS — the hand-rolled version has no such platform restriction.

The `maxCount` constructor parameter on `SemaphoreWin32` is dropped; confirmed via
repo-wide grep that no caller uses anything but the default-count constructor.

### 3.4 `sys::ReadWriteMutex`

No interface or caller-visible change. It's built from `sys::Semaphore` +
`sys::Mutex`, both already migrated above; the `lockRead`/`unlockRead`/`lockWrite`/
`unlockWrite` logic in `ReadWriteMutex.cpp` is untouched. The existing
`#if !defined(__APPLE_CC__)` guard around the whole class can be **removed** since it
existed only because of the old `SemaphorePosix` macOS restriction being lifted in 3.3.

### 3.5 `sys::Thread` — the architectural change

This is the one primitive that cannot be a drop-in replacement, because `std::thread`
is a non-polymorphic, move-only RAII handle — it cannot be subclassed the way
`ThreadInterface`/`ThreadPosix`/`ThreadWin32` are designed to be today.

**Deleted:** `ThreadInterface.h`, `ThreadPosix.{h,cpp}`, `ThreadWin32.{h,cpp}`, the
`STANDARD_START_CALL` macro, and the thread `level`/`priority` concepts (`kill()`,
`setPriority()`, `getPriority()`, `getLevel()`, `MINIMUM/NORMAL/MAXIMUM_PRIORITY`,
`DEFAULT/KERNEL/USER_LEVEL`). A repo-wide grep confirmed **zero external callers** of
any of these outside `sys/`'s own implementation files, so none of this is a
compatibility risk — `kill()` already unconditionally threw "not implemented" on
Windows, and the priority/level concepts were effectively vestigial.

**Replacement:**

```cpp
namespace sys {
class Thread final {
    std::unique_ptr<Runnable> mTarget;
    std::thread mNative;
    std::string mName;
public:
    explicit Thread(Runnable* target, const std::string& name = "");
    ~Thread();
    Thread(const Thread&) = delete;
    Thread& operator=(const Thread&) = delete;

    void start();                 // mNative = std::thread([this]{ mTarget->run(); });
    void join()   { mNative.join(); }
    void detach() { mNative.detach(); }
    bool isRunning() const noexcept;
    std::string getName() const { return mName; }
    std::thread::native_handle_type getNative() { return mNative.native_handle(); } // for CPU-affinity code
    static void yield() { std::this_thread::yield(); }
};
}
```

`getThreadID()` (the free function used by `mt::WorkerThread::getThreadId()`) is kept
exactly as-is — it still calls `pthread_self()` on Linux directly, since there is no
portable `std::`-based replacement with the same `long`-comparable semantics, and this
code path is already Linux-only.

#### 3.5.1 Dependent rewrites (inheritance → composition)

Repo-wide analysis shows the blast radius here is narrower than it first appears:
**most of `mt`'s and `sys`'s own code already constructs `sys::Thread` from a
`Runnable*` rather than subclassing it** (e.g. `mt::ThreadGroup::createThread`,
`mt::BasicThreadPool::addThread`, and every usage in `sys/tests/ThreadTest4.cpp` and
`sys/unittests/test_atomic_counter.cpp`). Those call sites require **no changes at
all**.

Only three places subclass `sys::Thread` directly or indirectly and need rewriting:

| File | Current | New |
|---|---|---|
| `mt/include/mt/WorkerThread.h` | `template<typename T> class WorkerThread : public sys::Thread`, overrides `run()` | `WorkerThread` becomes a `sys::Runnable` (not a `Thread`); pools wrap instances in `std::make_shared<sys::Thread>(workerInstance)` — the same pattern already used elsewhere in this file's sibling code |
| `net/include/net/PerRequestThreadAllocStrategy.h` (+ `.cpp`) | `RequestHandlerThread : public sys::Thread` | `RequestHandlerThread : public sys::Runnable`; `handleConnection()` constructs `new sys::Thread(new RequestHandlerThread(...))` |
| `net/tests/AckMulticastSubscriber.cpp` | `RetransmitThread : public sys::Thread`; `pthread_detach(thr->getNative())` | `RetransmitThread : public sys::Runnable`; `sys::Thread thr(new RetransmitThread(...)); thr.start(); thr.detach();` — using the new `Thread::detach()` instead of a raw pthread call |

`mt::TiedWorkerThread` and `net::ConnectionThread` inherit from `WorkerThread`, not
`sys::Thread` directly, so they follow automatically once `WorkerThread` itself is
fixed — no additional source changes needed in those two files beyond recompilation.

`mt::AbstractThreadPool<Request_T>::newWorker()` changes its return type from
`WorkerThread<Request_T>*` to `sys::Runnable*` (the `WorkerThread` instance), with
`start()` wrapping the result in a `sys::Thread` the same way `BasicThreadPool`
already does today for its `GenericRequestHandler`-derived workers.

## 4. Code Volume Removed

Line counts below are measured directly from the files slated for deletion.

### 4.1 Files deleted entirely

| Primitive | Files removed | Lines removed |
|---|---|---|
| Mutex | `MutexInterface.h`, `MutexPosix.{h,cpp}`, `MutexWin32.{h,cpp}`, `MutexCpp11.{h,cpp}` (7 files) | 82+84+69+78+61+79+53 = **506** |
| ConditionVar | `ConditionVarInterface.h`, `ConditionVarPosix.{h,cpp}`, `ConditionVarWin32.{h,cpp}` (5 files) | 124+131+113+158+266 = **792** |
| Semaphore | `SemaphoreInterface.h`, `SemaphorePosix.{h,cpp}`, `SemaphoreWin32.{h,cpp}` (5 files) | 46+65+57+65+68 = **301** |
| Thread | `ThreadInterface.h`, `ThreadPosix.{h,cpp}`, `ThreadWin32.{h,cpp}` (5 files) | 284+153+104+148+64 = **753** |
| **Total** | **22 files** | **2,352 lines** |

This 2,352-line figure is pure platform-dispatch/implementation code being deleted
outright — it does not include the small amount of new portable replacement code
(roughly 150-250 lines total across the four new single-implementation headers/sources),
nor the dependent-class rewrites in §3.5.1.

### 4.2 What drives the size of the deletion

The POSIX/Win32 split was expensive specifically because:

- **ConditionVarWin32 alone is ~430 lines** (158 header + 266 cpp) implementing a
  hand-rolled condition variable from a semaphore, an event, a waiter count, and a
  critical section — a well-known pre-Vista compatibility workaround
  (`ConditionVarDataWin32`, citing the ACE-framework "Strategies for Implementing POSIX
  Condition Variables on Win32" article) that native `std::condition_variable` replaces
  in its entirety with zero custom logic.
- **Thread's two platform backends total ~470 lines** of priority/level handling,
  `pthread_create`/`CreateThread`-vs-`_beginthreadex` selection, and separate
  start/join/kill/yield implementations that collapse into a single ~60-line
  `std::thread`-based class.
- Every primitive duplicated the same `*Interface.h` + `*Posix.{h,cpp}` +
  `*Win32.{h,cpp}` three-way split (interface, POSIX impl, Win32 impl) purely to
  express what `std::mutex`/`std::condition_variable`/`std::thread` already provide
  as a single portable type.

### 4.3 Net effect on the Windows/Unix divide

Before this migration, `sys`'s threading layer has **4 primitives × up to 3 files
each** (interface + 2 platform backends) = up to 12 conceptual units, each requiring
separate maintenance, separate bug-fixing, and separate testing per platform. CMake
does not exclude non-matching platform files at the build-system level — **both**
Win32 and POSIX `.cpp` files are compiled on every platform today, with the
non-matching one resolving to an empty translation unit via `#ifdef`. After migration:

- **Mutex, ConditionVar, Semaphore**: zero platform-specific code remains. One
  implementation, compiled identically everywhere.
- **Thread**: zero platform-specific *application* code remains in `sys::Thread`
  itself. The only remaining platform-awareness anywhere in this subsystem is:
  - `getThreadID()`'s existing Linux-specific `pthread_self()` call (already isolated,
    unchanged by this migration, and orthogonal to it)
  - CPU-affinity code (`CPUAffinityInitializerLinux`/`CPUAffinityInitializerWin32`),
    which is explicitly **out of scope** and already structured as a separate,
    independently-isolated subsystem in `mt/`, not `sys/`
- **ReadWriteMutex**: the `!defined(__APPLE_CC__)` guard is removed entirely, since it
  only existed to work around the old `SemaphorePosix`'s macOS limitation.

In short: the Windows/Unix divide inside `sys`'s core threading primitives
(`Thread`/`Mutex`/`ConditionVar`/`Semaphore`) is **eliminated completely** — 2,352
lines of dual-platform implementation code are replaced by a few hundred lines of
single-implementation, platform-neutral code. The only platform-specific code left
anywhere in the threading-related portion of the tree is the CPU-affinity subsystem,
which this migration intentionally does not touch.

## 5. Risk Summary

| Risk | Assessment |
|---|---|
| `Mutex`/`ConditionVar` semantic change | None — straightforward 1:1 behavioral mapping, no recursive-mutex/try-lock/timed-mutex features used beyond what `std::` offers |
| `Semaphore` semantic change | None — hand-rolled implementation matches `wait()`/`signal()` semantics exactly; `maxCount` ctor param dropped (confirmed unused) |
| `Thread` priority/kill/level removal | None — confirmed zero external callers via repo-wide grep; `kill()` already threw on Windows |
| `Thread` inheritance → composition | Breaking, but mechanical. 3 subclassers total (`WorkerThread`, `RequestHandlerThread`, test-only `RetransmitThread`); most call sites already use the composition pattern |
| CPU affinity / pinning | Unaffected — `native_handle()` continues to expose the real `pthread_t` backing `std::thread` on glibc/libstdc++ |
| `getThreadID()` | Unchanged — remains a Linux-specific `pthread_self()` wrapper, orthogonal to this migration |

## 6. Suggested Sequencing

1. **Phase 1:** `Mutex` + `ConditionVar` together (hard dependency between them)
2. **Phase 2:** `Semaphore` + `ReadWriteMutex` together (`ReadWriteMutex` depends on `Semaphore`)
3. **Phase 3:** `Thread`, including the `WorkerThread`/`net` dependent rewrites
4. **Phase 4:** Test-file updates and `ReleaseNotes.md` entry

Each phase is independently compilable and testable; Phase 3 is the only one with
cross-module (`net`) impact and should be reviewed most carefully.
