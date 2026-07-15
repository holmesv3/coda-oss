# Python bindings for sio.lite module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings with Python helpers
    # ========================================================================
    message(STATUS "Building sio.lite Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_sio_lite
        NB_STATIC
        source/nanobind/sio_lite_bindings.cpp
    )
    
    # Link against C++ libraries
    target_link_libraries(coda_sio_lite PRIVATE 
        sio.lite-c++ 
        io-c++ 
        sys-c++ 
        except-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_sio_lite PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(sio.lite-python ALIAS coda_sio_lite)
    
    # Install the C++ module to coda/sio_lite/ subdirectory
    install(TARGETS coda_sio_lite
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda/sio_lite"
            ${CODA_INSTALL_OPTION})
    
    # Install the Python helper module (__init__.py)
    install(FILES source/__init__.py
            DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda/sio_lite"
            ${CODA_INSTALL_OPTION})

else()
    # ========================================================================
    # SWIG PATH - Traditional bindings
    # ========================================================================
    coda_add_swig_python_module(
        TARGET sio.lite-python
        PACKAGE coda
        MODULE_NAME sio_lite
        MODULE_DEPS sio.lite-c++
        PYTHON_DEPS config-python io-python sys-python except-python
        INPUT "source/sio_lite.i")
endif()
