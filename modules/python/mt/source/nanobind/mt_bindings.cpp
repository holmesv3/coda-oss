/*
 * =========================================================================
 * This file is part of mt-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * mt-python is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; If not,
 * see <http://www.gnu.org/licenses/>.
 */

#include <nanobind/nanobind.h>
#include <nanobind/trampoline.h>

#include <mt/ThreadPlanner.h>
#include <mt/ThreadGroup.h>
#include <sys/Runnable.h>
#include <import/except.h>

namespace nb = nanobind;
using namespace nb::literals;

// Trampoline class to allow Python classes to inherit from sys::Runnable
class PyRunnable : public sys::Runnable {
public:
    NB_TRAMPOLINE(sys::Runnable, 1);
    
    void run() override {
        NB_OVERRIDE_PURE(run);
    }
};

NB_MODULE(coda_mt, m) {
    m.doc() = "CODA-OSS multi-threading utilities";
    
    // sys::Runnable - base class for thread runnables
    // This allows Python classes to inherit from Runnable
    nb::class_<sys::Runnable, PyRunnable>(m, "Runnable")
        .def(nb::init<>())
        .def("run", &sys::Runnable::run);
    
    // ThreadPlanner - assists with dividing work among threads
    nb::class_<mt::ThreadPlanner>(m, "ThreadPlanner")
        .def(nb::init<size_t, size_t>(), 
             "numElements"_a, "numThreads"_a,
             "Constructor\n\n"
             "Args:\n"
             "    numElements: The total number of elements of work to be divided\n"
             "    numThreads: The number of threads that will be used for the work")
        .def("getNumElementsPerThread", &mt::ThreadPlanner::getNumElementsPerThread,
             "Get the number of elements each thread will work on.\n\n"
             "Returns:\n"
             "    The number of elements per thread (early threads may have more)")
        .def("getThreadInfo", 
             [](const mt::ThreadPlanner& self, size_t threadNum) {
                 size_t startElement, numElementsThisThread;
                 bool isValid = self.getThreadInfo(threadNum, startElement, numElementsThisThread);
                 return nb::make_tuple(isValid, startElement, numElementsThisThread);
             },
             "threadNum"_a,
             "Get thread work information.\n\n"
             "Args:\n"
             "    threadNum: The 0-based thread number\n\n"
             "Returns:\n"
             "    tuple: (isValid, startElement, numElementsThisThread)\n"
             "        isValid: True if this thread has work to do\n"
             "        startElement: The starting element index for this thread\n"
             "        numElementsThisThread: The number of elements this thread should process")
        .def("getNumThreadsThatWillBeUsed", &mt::ThreadPlanner::getNumThreadsThatWillBeUsed,
             "Get the number of threads that will actually be used.\n\n"
             "Returns:\n"
             "    The number of threads that will be used (may be less than requested)");
    
    // ThreadGroup - manages a group of threads
    nb::class_<mt::ThreadGroup>(m, "ThreadGroup")
        .def(nb::init<bool>(), 
             "pinToCPU"_a = false,
             "Constructor\n\n"
             "Args:\n"
             "    pinToCPU: Whether to enable CPU affinity-based thread pinning")
        .def("createThread",
             [](mt::ThreadGroup& self, sys::Runnable* runnable) {
                 // Note: ThreadGroup takes ownership of the runnable pointer
                 // We use nb::rv_policy::take_ownership semantics
                 if (runnable == nullptr) {
                     throw except::Exception(
                         except::Context(__FILE__, __LINE__, __FUNCTION__, "", 
                         "Invalid data type in createThread (expected sys::Runnable)"));
                 }
                 self.createThread(runnable);
             },
             "runnable"_a,
             // The ThreadGroup takes ownership of the runnable, so we need to prevent
             // Python from deleting it
             nb::call_guard<nb::gil_scoped_release>(),
             "Create and start a thread from a Runnable.\n\n"
             "Args:\n"
             "    runnable: A sys::Runnable instance to run in the thread.\n"
             "              The ThreadGroup takes ownership of this object.")
        .def("joinAll", 
             &mt::ThreadGroup::joinAll,
             nb::call_guard<nb::gil_scoped_release>(),
             "Wait for all threads to complete.")
        .def("isPinToCPUEnabled", &mt::ThreadGroup::isPinToCPUEnabled,
             "Check whether CPU pinning is enabled.\n\n"
             "Returns:\n"
             "    True if CPU pinning is enabled, False otherwise");
}
