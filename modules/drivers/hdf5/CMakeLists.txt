if(HDF5_HOME STREQUAL "")
    include(FetchContent)
    set(HDF5_ENABLE_ZLIB_SUPPORT ON)
    set(HDF5_BUILD_EXAMPLES OFF)
    set(BUILD_TESTING OFF)
    FetchContent_Declare(HDF5
        URL "${CMAKE_CURRENT_SOURCE_DIR}/hdf5-2.0.0.tar.gz"
    URL_HASH "SHA256=3e6ae0430995c8ae724688c866f4dbb6feba9c6220583d72049fbb9b006c1cd5")
    FetchContent_MakeAvailable(HDF5)
else()
    find_package(HDF5 REQUIRED COMPONENTS C CXX PATHS ${HDF5_HOME})
endif()
