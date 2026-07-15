#!/usr/bin/env python3
"""
Test suite for coda_io module.
"""
import pytest

try:
    from coda import coda_io
except ImportError as e:
    pytest.skip(f"coda_io module not available: {e}", allow_module_level=True)


def test_write_string():
    """Test writing string to StringStream."""
    stream = coda_io.StringStream()
    stream.write('text')
    assert stream.str() == 'text'


def test_write_bytes():
    """Test writing bytes to StringStream."""
    stream = coda_io.StringStream()
    bytes_input = bytes('text', 'utf-8')
    stream.writeBytes(bytes_input)
    assert stream.str() == 'text'


def test_string_stream_empty():
    """Test empty StringStream."""
    stream = coda_io.StringStream()
    assert stream.str() == ''


def test_string_stream_multiple_writes():
    """Test multiple writes to StringStream."""
    stream = coda_io.StringStream()
    stream.write('hello')
    stream.write(' ')
    stream.write('world')
    assert stream.str() == 'hello world'
