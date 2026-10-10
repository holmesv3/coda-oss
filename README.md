     _________________________
    |   ____  _||_  ___  __   |
    |  /___ \/_||_\| __\/  \  |
    | //   \// || \||  \\ _ \ |
    | ||   [===||===]  ||(_)| |
    | ||   _|| || |||  ||__ | |
    | \\ _/ |\_||_/||__/|| || |
    |  \___/ \_||_/|___/|| || |
    |__________||_____________|

CODA is a set of modules, and each module, while complimentary to one another, has
a very specific and largely independent purpose.

CODA follows [Semantic Versioning](https://semver.org/).

Building CODA
--------------

CODA uses CMake. See [CMakeOptions.md](./docs/CMakeOptions.md) for detailed CMake build instructions.

Sample Build Scenario
---------------------

The following assumes you are at the root of the repository. This will
- Configure a `Release` build with the system default compilers in the directory `${PWD}/build_dir` with a default installation path of `${PWD}/install`
- Compile and install all targets with 16 threads

```bash
cmake -B build_dir -DCMAKE_INSTALL_PREFIX=install -DCMAKE_BUILD_TYPE=Release
cmake --build build_dir --target install -j16
```

Enabling a debugger
-------------------
`-g` and its variants can be achieved at configure time by setting `-DCMAKE_BUILD_TYPE=Debug`
