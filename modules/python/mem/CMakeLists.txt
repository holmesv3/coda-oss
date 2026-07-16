# Python bindings for mem module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building mem Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_mem
        NB_STATIC
        source/nanobind/mem_bindings.cpp
    )
    
    # Link against C++ mem library
    target_link_libraries(coda_mem PRIVATE mem-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_mem PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(mem-python ALIAS coda_mem)
    
    # Install the module
    install(TARGETS coda_mem
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})
    
    # Install stub file for type checking
    install(FILES source/coda_mem.pyi
            DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})

else()
    # ========================================================================
    # SWIG PATH - Traditional bindings
    # ========================================================================
    coda_add_swig_python_module(
        TARGET mem-python
        PACKAGE coda
        MODULE_NAME mem
        MODULE_DEPS mem-c++
        PYTHON_DEPS config-python
        INPUT "source/mem.i")
endif()
