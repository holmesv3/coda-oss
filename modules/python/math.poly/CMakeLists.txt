# Python bindings for math.poly module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building math.poly Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_math_poly
        NB_STATIC
        source/nanobind/math_poly_bindings.cpp
    )
    
    # Link against C++ libraries
    # Note: No numpyutils-c++ dependency - using nanobind ndarray
    target_link_libraries(coda_math_poly PRIVATE 
        math.poly-c++
        math.linear-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_math_poly PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(math.poly-python ALIAS coda_math_poly)
    
    # Install the C++ module to coda/math_poly/ subdirectory
    install(TARGETS coda_math_poly
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda/math_poly"
            ${CODA_INSTALL_OPTION})
    
    # Install the Python helper module (__init__.py)
    install(FILES source/__init__.py
            DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda/math_poly"
            ${CODA_INSTALL_OPTION})

else()
    # ========================================================================
    # SWIG PATH - Traditional bindings
    # ========================================================================
    if (TARGET numpyutils-c++)
        coda_add_swig_python_module(
            TARGET math.poly-python
            PACKAGE coda
            MODULE_NAME math_poly
            MODULE_DEPS math.poly-c++ numpyutils-c++
            PYTHON_DEPS config-python except-python math.linear-python types-python
            INPUT "source/math_poly.i")
    endif()
endif()
