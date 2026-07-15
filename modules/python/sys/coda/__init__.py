"""CODA-OSS Python package namespace."""
# Namespace package - allows multiple coda-* packages to coexist
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
