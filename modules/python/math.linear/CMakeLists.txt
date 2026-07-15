# Python bindings for math.linear module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building math.linear Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_math_linear
        NB_STATIC
        source/nanobind/math_linear_bindings.cpp
    )
    
    # Link against C++ libraries
    target_link_libraries(coda_math_linear PRIVATE 
        math.linear-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_math_linear PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(math.linear-python ALIAS coda_math_linear)
    
    # Install the C++ module to coda/math_linear/ subdirectory
    install(TARGETS coda_math_linear
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda/math_linear"
            ${CODA_INSTALL_OPTION})
    
    # Install the Python helper module (__init__.py)
    install(FILES source/__init__.py
            DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda/math_linear"
            ${CODA_INSTALL_OPTION})

else()
    # ========================================================================
    # SWIG PATH - Traditional bindings
    # ========================================================================
    coda_add_swig_python_module(
        TARGET math.linear-python
        PACKAGE coda
        MODULE_NAME math_linear
        MODULE_DEPS math.linear-c++
        PYTHON_DEPS config-python except-python types-python
        INPUT "source/math_linear.i")
endif()
