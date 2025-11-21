if(HIGHFIVE_HOME)
    find_package(HighFive REQUIRED PATHS ${HIGHFIVE_HOME})
else()
    include(FetchContent)
    set(HDF5_USE_STATIC_LIBRARIES ON)
    FetchContent_Declare(highfive
        URL "${CMAKE_CURRENT_SOURCE_DIR}/highfive-37419151.zip"
    URL_HASH "SHA256=692290981abc564c540c4d325377766d1d1a0d2c2b1db8d0cb03766c64cf5c8d")
    FetchContent_MakeAvailable(highfive)
endif()
