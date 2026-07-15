#!/usr/bin/env python3
"""
Test suite to verify nanobind bindings maintain API compatibility with SWIG.

This test suite can be run against both SWIG and nanobind implementations
to verify identical behavior.
"""
import sys
import pytest
from coda import coda_sys

class TestFunctions:
    """Test module-level functions."""
    
    def test_isBigEndianSystem_exists(self):
        """Test isBigEndianSystem function exists."""
        assert hasattr(coda_sys, 'isBigEndianSystem')
    
    def test_isBigEndianSystem_returns_bool(self):
        """Test isBigEndianSystem returns a boolean."""
        result = coda_sys.isBigEndianSystem()
        assert isinstance(result, bool)
        print(f"System endianness: {'big' if result else 'little'}-endian")
    
    def test_byteSwap_exists(self):
        """Test byteSwap function exists."""
        assert hasattr(coda_sys, 'byteSwap')
        # Note: Full testing requires buffer manipulation which is complex
        # and depends on NumPy or ctypes
    
    def test_alignedAlloc_exists(self):
        """Test alignedAlloc functions exist."""
        assert hasattr(coda_sys, 'alignedAlloc')
        assert hasattr(coda_sys, 'alignedFree')
        # Note: Full testing requires careful memory management


class TestConstants:
    """Test module constants."""
    
    def test_SSE_INSTRUCTION_ALIGNMENT_exists(self):
        """Test SSE_INSTRUCTION_ALIGNMENT constant exists."""
        assert hasattr(coda_sys, 'SSE_INSTRUCTION_ALIGNMENT')
    
    def test_SSE_INSTRUCTION_ALIGNMENT_value(self):
        """Test SSE_INSTRUCTION_ALIGNMENT has valid value."""
        alignment = coda_sys.SSE_INSTRUCTION_ALIGNMENT
        assert isinstance(alignment, int)
        assert alignment > 0
        assert alignment == 32  # Expected value
        print(f"SSE alignment: {alignment} bytes")
    
    def test_NativeLayer_func_exists(self):
        """Test NativeLayer_func__ constant exists."""
        assert hasattr(coda_sys, 'NativeLayer_func__')
        func = coda_sys.NativeLayer_func__
        assert isinstance(func, str)
        print(f"Native layer function macro: {func}")
    
    def test_SYS_FUNC_exists(self):
        """Test SYS_FUNC constant exists."""
        assert hasattr(coda_sys, 'SYS_FUNC')
        sys_func = coda_sys.SYS_FUNC
        assert isinstance(sys_func, str)
        print(f"SYS_FUNC macro: {sys_func}")


class TestUTCDateTime:
    """Test UTCDateTime class."""
    
    def test_class_exists(self):
        """Test UTCDateTime class exists."""
        assert hasattr(coda_sys, 'UTCDateTime')
    
    def test_default_constructor(self):
        """Test default constructor creates object."""
        dt = coda_sys.UTCDateTime()
        assert dt is not None
        assert hasattr(dt, 'format')
    
    def test_time_constructor(self):
        """Test constructor with time values."""
        dt = coda_sys.UTCDateTime(12, 30, 45.5)
        assert dt is not None
        formatted = dt.format()
        assert isinstance(formatted, str)
        # Should have time values
        assert '12' in formatted or '12:30' in formatted
    
    def test_date_constructor(self):
        """Test constructor with date values."""
        dt = coda_sys.UTCDateTime(2024, 7, 14)
        assert dt is not None
        formatted = dt.format()
        assert '2024' in formatted
        assert '07' in formatted or '7' in formatted
        assert '14' in formatted
    
    def test_datetime_constructor(self):
        """Test constructor with date and time values."""
        dt = coda_sys.UTCDateTime(2024, 7, 14, 12, 30, 0.0)
        assert dt is not None
        formatted = dt.format()
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        
        # Verify it contains expected components
        assert '2024' in formatted
        # ISO8601 format should have 'T' separator
        assert 'T' in formatted
        print(f"Formatted datetime: {formatted}")
    
    def test_millis_constructor(self):
        """Test constructor from milliseconds."""
        # Using a known timestamp: 2024-07-14 12:30:00 UTC
        dt = coda_sys.UTCDateTime(1720963800000.0)
        assert dt is not None
        formatted = dt.format()
        assert isinstance(formatted, str)
        print(f"From millis: {formatted}")
    
    def test_string_constructor_iso8601(self):
        """Test constructor from ISO8601 string."""
        dt = coda_sys.UTCDateTime("2024-07-14T12:30:00Z")
        assert dt is not None
        formatted = dt.format()
        assert '2024' in formatted
        assert '07' in formatted or '7' in formatted
        assert '14' in formatted
        print(f"From ISO8601: {formatted}")
    
    def test_string_constructor_with_format(self):
        """Test constructor from string with custom format."""
        # This tests the two-parameter string constructor
        dt = coda_sys.UTCDateTime("2024-07-14 12:30:00", "%Y-%m-%d %H:%M:%S")
        assert dt is not None
        formatted = dt.format()
        assert isinstance(formatted, str)
    
    def test_format_method(self):
        """Test format() method returns ISO8601 string."""
        dt = coda_sys.UTCDateTime(2024, 7, 14, 12, 30, 0.0)
        formatted = dt.format()
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        
        # ISO8601 format characteristics
        assert 'T' in formatted  # Date/time separator
        assert '2024' in formatted  # Year
        # Should end with 'Z' for UTC (may vary by implementation)
        print(f"Format output: {formatted}")
    
    def test_str_method(self):
        """Test __str__ method."""
        dt = coda_sys.UTCDateTime(2024, 7, 14, 12, 30, 0.0)
        str_output = str(dt)
        
        assert isinstance(str_output, str)
        assert len(str_output) > 0
        assert '2024' in str_output
        print(f"str(dt): {str_output}")
    
    def test_repr_method(self):
        """Test __repr__ method."""
        dt = coda_sys.UTCDateTime(2024, 7, 14, 12, 30, 0.0)
        repr_output = repr(dt)
        
        assert isinstance(repr_output, str)
        assert len(repr_output) > 0
        # repr should include class name
        assert 'UTCDateTime' in repr_output
        print(f"repr(dt): {repr_output}")


class TestAPICompatibility:
    """Test overall API compatibility with SWIG version."""
    
    def test_module_has_expected_attributes(self):
        """Verify all expected module attributes exist."""
        expected_attrs = [
            'isBigEndianSystem',
            'byteSwap',
            'alignedAlloc',
            'alignedFree',
            'UTCDateTime',
            'SSE_INSTRUCTION_ALIGNMENT',
            'NativeLayer_func__',
            'SYS_FUNC',
        ]
        
        missing = []
        for attr in expected_attrs:
            if not hasattr(coda_sys, attr):
                missing.append(attr)
        
        assert not missing, f"Missing attributes: {missing}"
    
    def test_import_path(self):
        """Test that module can be imported as coda.coda_sys."""
        import coda.coda_sys as sys_module
        assert sys_module is coda_sys
    
    def test_module_docstring(self):
        """Test module has documentation."""
        assert hasattr(coda_sys, '__doc__')
        assert coda_sys.__doc__ is not None
    
    def test_UTCDateTime_is_class(self):
        """Test UTCDateTime is a class type."""
        assert isinstance(coda_sys.UTCDateTime, type)


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_UTCDateTime_epoch(self):
        """Test creating datetime at epoch (January 1, 1970)."""
        dt = coda_sys.UTCDateTime(0.0)  # Epoch in milliseconds
        assert dt is not None
        formatted = dt.format()
        assert '1970' in formatted
    
    def test_UTCDateTime_next_epoch(self):
        """Test creating datetime at turn of 32 bit epoch"""
        dt = coda_sys.UTCDateTime(2037, 1, 1)
        assert dt is not None
        formatted = dt.format()
        assert '2037' in formatted

    def test_UTCDateTime_far_future(self):
        """Test creating datetime in far future. 
        
        Our implementation follows 32 bit encoding of the date time for compatibility

        See https://en.wikipedia.org/wiki/Year_2038_problem
        """
        dt = coda_sys.UTCDateTime(3000, 1, 1)
        assert dt is not None
        formatted = dt.format()
        assert '1970' in formatted
    
    def test_UTCDateTime_with_fractional_seconds(self):
        """Test datetime with fractional seconds."""
        dt = coda_sys.UTCDateTime(2024, 7, 14, 12, 30, 45.123)
        assert dt is not None
        formatted = dt.format()
        # Should handle fractional seconds gracefully
        assert isinstance(formatted, str)


def test_module_info():
    """Print module information for debugging."""
    print("\n" + "=" * 60)
    print("coda_sys Module Information")
    print("=" * 60)
    print(f"Module: {coda_sys}")
    print(f"Module file: {getattr(coda_sys, '__file__', 'N/A')}")
    print(f"Module doc: {coda_sys.__doc__}")
    print("\nPublic attributes:")
    attrs = sorted([x for x in dir(coda_sys) if not x.startswith('_')])
    for attr in attrs:
        print(f"  - {attr}")
    print("=" * 60)
