# Python bindings for sys module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building sys Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(coda_sys NB_STATIC source/sys_bindings.cpp)
    
    # Link against the C++ sys library
    target_link_libraries(coda_sys PRIVATE sys-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_sys PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility with other modules that depend on sys-python
    add_library(sys-python ALIAS coda_sys)
    
    # Install the module
    install(TARGETS coda_sys LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda" ${CODA_INSTALL_OPTION})

else()
    coda_add_swig_python_module(
        TARGET sys-python
        PACKAGE coda
        MODULE_NAME coda_sys
        MODULE_DEPS sys-c++
        PYTHON_DEPS config-python
        INPUT "source/sys.i")
endif()
