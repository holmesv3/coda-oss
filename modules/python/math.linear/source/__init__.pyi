"""
Type stubs for coda.math_linear module.

Re-exports all classes and functions from the C++ binding module.
"""

from .coda_math_linear import (
    Vector2 as Vector2,
    Vector3 as Vector3,
    VectorDouble as VectorDouble,
    MatrixDouble as MatrixDouble,
    Matrix1x1 as Matrix1x1,
    Matrix1x2 as Matrix1x2,
    Matrix1x3 as Matrix1x3,
    Matrix2x1 as Matrix2x1,
    Matrix2x2 as Matrix2x2,
    Matrix2x3 as Matrix2x3,
    Matrix2x7 as Matrix2x7,
    Matrix3x1 as Matrix3x1,
    Matrix3x2 as Matrix3x2,
    Matrix3x3 as Matrix3x3,
    Matrix3x7 as Matrix3x7,
    Matrix7x2 as Matrix7x2,
    Matrix7x3 as Matrix7x3,
    Matrix7x7 as Matrix7x7,
    cross as cross,
)

__all__ = [
    'Vector2',
    'Vector3',
    'VectorDouble',
    'MatrixDouble',
    'Matrix1x1',
    'Matrix1x2',
    'Matrix1x3',
    'Matrix2x1',
    'Matrix2x2',
    'Matrix2x3',
    'Matrix2x7',
    'Matrix3x1',
    'Matrix3x2',
    'Matrix3x3',
    'Matrix3x7',
    'Matrix7x2',
    'Matrix7x3',
    'Matrix7x7',
    'cross',
]
