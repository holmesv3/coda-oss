"""
Type stubs for coda.math_poly module.

Re-exports all classes and functions from the C++ binding module.
"""

from .coda_math_poly import (
    Poly1D as Poly1D,
    Poly2D as Poly2D,
    PolyVector3 as PolyVector3,
    StdVectorDouble as StdVectorDouble,
    Vector3Coefficients as Vector3Coefficients,
    fit as fit,
)

__all__ = [
    'Poly1D',
    'Poly2D',
    'PolyVector3',
    'StdVectorDouble',
    'Vector3Coefficients',
    'fit',
]
