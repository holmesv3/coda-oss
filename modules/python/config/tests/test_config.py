#!/usr/bin/env python3
"""
Test suite for coda_config module.
"""
import pytest

try:
    from coda import coda_config
except ImportError as e:
    pytest.skip(f"coda_config module not available: {e}", allow_module_level=True)


def test_module_exists():
    """Test that coda_config module can be imported."""
    assert coda_config is not None


def test_module_has_doc():
    """Test that module has documentation."""
    assert hasattr(coda_config, '__doc__')
    assert coda_config.__doc__ is not None


def test_module_name():
    """Test that module has correct name."""
    assert coda_config.__name__ == 'coda.coda_config'


def test_module_package():
    """Test that module is in coda package."""
    assert coda_config.__package__ == 'coda'
