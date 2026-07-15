"""
CODA-OSS math.linear Python Module
===================================

Provides linear algebra types and operations.

Public API
----------
Classes:
    Vector2, Vector3 - Fixed-size 2D and 3D vectors
    VectorDouble - Dynamic-size vector
    MatrixDouble - Dynamic-size 2D matrix
    Matrix1x1, Matrix2x2, Matrix3x3, etc. - Fixed-size matrices

Functions:
    cross(a, b) - Compute cross product of two Vector3 objects
"""

# Import all C++ bindings
from .coda_math_linear import *
