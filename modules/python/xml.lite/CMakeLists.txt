# Python bindings for xml.lite module
# Supports both SWIG (traditional) and nanobind (modern) implementations

if(NOT ENABLE_PYTHON)
    return()
endif()

if(USE_NANOBIND)
    # ========================================================================
    # NANOBIND PATH - Modern C++17 bindings
    # ========================================================================
    message(STATUS "Building xml.lite Python bindings with nanobind")
    
    # Find Python and nanobind
    set(Python_FIND_VIRTUALENV ONLY)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
    find_package(nanobind CONFIG REQUIRED)
    
    # Create the Python extension module
    nanobind_add_module(
        coda_xml_lite
        NB_STATIC
        source/nanobind/xml_lite_bindings.cpp
    )
    
    # Link against C++ libraries
    target_link_libraries(coda_xml_lite PRIVATE xml.lite-c++ io-c++)
    
    # Set C++17 standard (required by nanobind)
    set_target_properties(coda_xml_lite PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED ON
    )
    
    # Create alias for compatibility
    add_library(xml.lite-python ALIAS coda_xml_lite)
    
    # Install the module
    install(TARGETS coda_xml_lite
            LIBRARY DESTINATION "${CODA_PYTHON_SITE_PACKAGES}/coda"
            ${CODA_INSTALL_OPTION})

else()
    # ========================================================================
    # SWIG PATH - Traditional bindings
    # ========================================================================
    coda_add_swig_python_module(
        TARGET xml.lite-python
        PACKAGE coda
        MODULE_NAME xml_lite
        MODULE_DEPS xml.lite-c++
        PYTHON_DEPS config-python
        INPUT "source/xml_lite.i")
endif()
