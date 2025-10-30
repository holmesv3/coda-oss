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

CODA may be built using CMake.
```sh
# starting from base directory of repo, make a build directory and cd into it
mkdir build
cd build

# configure
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=[install path]

# build and install in parallel
cmake --build . -t install -j

# run unit tests (optional)
ctest
```

Enabling a debugger
-------------------
`-g` and its variants can be achieved at configure time using `-DCMAKE_BUILD_TYPE=Debug`

Compilation Options
-------------------
To print all available options (accessible via `cmake -D<option>=<val>`)
```sh
mkdir build && cd build
cmake .. -LH
```

Common Errors
-------------
    Fatal Python error: initfsencoding: unable to load the file system codec
    ModuleNotFoundError: No module named 'encodings'

Problem: Python is unable to find its `modules` directory, necessary for using the Python C API.

Solution: Set the `PYTHONHOME` environment variable. On Windows, this may look like:

    set PYTHONHOME=C:\ProgramData\Anaconda3\
