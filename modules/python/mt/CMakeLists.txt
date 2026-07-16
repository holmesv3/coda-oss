# Python bindings for mt module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building mt Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_mt
        NB_STATIC
        source/nanobind/mt_bindings.cpp
    )
    
    # Link against C++ libraries
    target_link_libraries(coda_mt PRIVATE mt-c++ sys-c++ except-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_mt PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(mt-python ALIAS coda_mt)
    
    # Install the module
    install(TARGETS coda_mt
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})
    
    # Install stub file for type checking
    install(FILES source/coda_mt.pyi
            DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})

else()
    # ========================================================================
    # SWIG PATH - Traditional bindings
    # ========================================================================
    coda_add_swig_python_module(
        TARGET mt-python
        PACKAGE coda
        MODULE_NAME mt
        MODULE_DEPS mt-c++ sys-c++
        PYTHON_DEPS config-python except-python mem-python types-python
        INPUT "source/mt.i")
endif()
