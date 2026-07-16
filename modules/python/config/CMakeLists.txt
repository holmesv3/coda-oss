# Python bindings for config module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building config Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_config
        NB_STATIC
        source/nanobind/config_bindings.cpp
    )
    
    # No C++ library dependencies for config module
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_config PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(config-python ALIAS coda_config)
    
    # Install the module
    install(TARGETS coda_config
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})
    
    # Install stub file for type checking
    install(FILES source/coda_config.pyi
            DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})

else()
    # Original SWIG build
    coda_add_swig_python_module(
        TARGET config-python
        PACKAGE coda
        MODULE_NAME coda_config
        INPUT "source/config.i")
endif()
