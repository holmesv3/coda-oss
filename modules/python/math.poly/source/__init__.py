"""
CODA-OSS math.poly Python Module
=================================

Provides polynomial types and fitting operations.

Public API
----------
Classes:
    Poly1D - 1D polynomial with double coefficients
    Poly2D - 2D polynomial with double coefficients
    PolyVector3 - 1D polynomial with Vector3 coefficients

Functions:
    fit(x, y, order) - Fit 1D polynomial to data
    fit(x, y, z, orderX, orderY) - Fit 2D polynomial to data
"""

# Import all C++ bindings
from .coda_math_poly import *
