# Python bindings for io module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building io Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_io
        NB_STATIC
        source/nanobind/io_bindings.cpp
    )
    
    # Link against C++ io library
    target_link_libraries(coda_io PRIVATE io-c++ sys-c++ except-c++)
    
    # Include directories
    target_include_directories(coda_io PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/source/nanobind
        ${CMAKE_SOURCE_DIR}/modules/c++/io/include
    )
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_io PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(io-python ALIAS coda_io)
    
    # Install the module
    install(TARGETS coda_io
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})

else()
    # Original SWIG build
    coda_add_swig_python_module(
        TARGET io-python
        PACKAGE coda
        MODULE_NAME coda_io
        MODULE_DEPS io-c++
        PYTHON_DEPS config-python
        INPUT "source/io.i")
endif()
