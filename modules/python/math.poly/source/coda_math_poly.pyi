"""
Type stubs for coda_math_poly module.

This module provides polynomial types and fitting functions for 1D and 2D polynomials.
Supports NumPy array conversion and evaluation over sequences.

Classes:
    Poly1D: 1D polynomial with double coefficients
    Poly2D: 2D polynomial with double coefficients  
    PolyVector3: 1D polynomial with Vector3 coefficients
    StdVectorDouble: STL vector of doubles
    Vector3Coefficients: STL vector of Vector3 objects

Functions:
    fit: Fit polynomial to data (overloaded for 1D and 2D)
"""

from typing import List, Dict, Any, Union, overload
import numpy as np
from numpy.typing import NDArray

# Import Vector3 type from math_linear
from ..math_linear import Vector3, VectorDouble, MatrixDouble

class StdVectorDouble:
    """STL vector<double> wrapper."""
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, i: int) -> float: ...
    def __setitem__(self, i: int, val: float) -> None: ...
    def append(self, val: float) -> None: ...


class Vector3Coefficients:
    """STL vector<Vector3> wrapper for polynomial coefficients."""
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, i: int) -> Vector3: ...
    def __setitem__(self, i: int, val: Vector3) -> None: ...
    def append(self, val: Vector3) -> None: ...


class Poly1D:
    """
    One-dimensional polynomial with double coefficients.
    
    Represents polynomial P(x) = c[0] + c[1]*x + c[2]*x^2 + ... + c[n]*x^n
    where c are the coefficients and n is the order.
    
    Supports evaluation via __call__, indexing of coefficients, and
    conversion to/from NumPy arrays.
    """
    
    @overload
    def __init__(self) -> None:
        """Create empty polynomial (order -1)."""
        ...
    
    @overload
    def __init__(self, order: int) -> None:
        """
        Create polynomial of given order with zero coefficients.
        
        Args:
            order: Polynomial order (degree)
        """
        ...
    
    @overload
    def __init__(self, coeffs: List[float]) -> None:
        """
        Create polynomial from coefficient list.
        
        Args:
            coeffs: List of coefficients [c0, c1, c2, ..., cn]
                   where P(x) = c0 + c1*x + c2*x^2 + ... + cn*x^n
        """
        ...
    
    def order(self) -> int:
        """
        Get polynomial order (degree).
        
        Returns:
            Highest power of x with non-zero coefficient
        """
        ...
    
    def size(self) -> int:
        """
        Get number of coefficients.
        
        Returns:
            Number of coefficients (order + 1)
        """
        ...
    
    def empty(self) -> bool:
        """
        Check if polynomial is empty.
        
        Returns:
            True if polynomial has no coefficients
        """
        ...
    
    def coeffs(self) -> List[float]:
        """
        Get coefficients as list.
        
        Returns:
            List of all coefficients
        """
        ...
    
    def __getitem__(self, i: int) -> float:
        """
        Get coefficient at index.
        
        Args:
            i: Coefficient index (0 to order)
            
        Returns:
            Coefficient value
        """
        ...
    
    def __setitem__(self, i: int, val: float) -> None:
        """
        Set coefficient at index.
        
        Args:
            i: Coefficient index (0 to order)
            val: New coefficient value
        """
        ...
    
    def __str__(self) -> str:
        """Return string representation of polynomial."""
        ...
    
    def __deepcopy__(self, memo: Dict[int, Any]) -> Poly1D:
        """
        Create deep copy.
        
        Args:
            memo: Copy memo dictionary
            
        Returns:
            New Poly1D instance
        """
        ...
    
    @overload
    def __call__(self, input: float) -> float:
        """
        Evaluate polynomial at single point.
        
        Args:
            input: X value
            
        Returns:
            P(input)
        """
        ...
    
    @overload
    def __call__(self, input: List[float]) -> List[float]:
        """
        Evaluate polynomial at multiple points.
        
        Args:
            input: List of X values
            
        Returns:
            List of P(x) for each x in input
        """
        ...
    
    def asArray(self) -> NDArray[np.float64]:
        """
        Convert coefficients to NumPy array.
        
        Returns:
            1D NumPy array of coefficients
        """
        ...
    
    @staticmethod
    def fromArray(array: NDArray[np.float64]) -> Poly1D:
        """
        Create polynomial from NumPy array of coefficients.
        
        Args:
            array: 1D NumPy array of coefficients
            
        Returns:
            New Poly1D instance
        """
        ...
    
    def __getstate__(self) -> bytes:
        """Pickle support."""
        ...
    
    def __setstate__(self, state: bytes) -> None:
        """Pickle support."""
        ...


class Poly2D:
    """
    Two-dimensional polynomial with double coefficients.
    
    Represents polynomial P(x,y) = sum(i=0..orderX, j=0..orderY) c[i][j] * x^i * y^j
    
    Internally stores as list of 1D polynomials (one per power of x),
    where each 1D polynomial represents the y-terms for that x-power.
    """
    
    @overload
    def __init__(self) -> None:
        """Create empty polynomial."""
        ...
    
    @overload
    def __init__(self, orderX: int, orderY: int) -> None:
        """
        Create 2D polynomial with zero coefficients.
        
        Args:
            orderX: Order in X dimension
            orderY: Order in Y dimension
        """
        ...
    
    def orderX(self) -> int:
        """Get order in X dimension."""
        ...
    
    def orderY(self) -> int:
        """Get order in Y dimension."""
        ...
    
    def empty(self) -> bool:
        """Check if polynomial is empty."""
        ...
    
    def coeffs(self) -> List[Poly1D]:
        """
        Get coefficients as list of 1D polynomials.
        
        Returns:
            List where each element is a Poly1D representing y-terms
            for a specific power of x
        """
        ...
    
    def __getitem__(self, idx: tuple[int, int]) -> float:
        """
        Get coefficient at (i, j).
        
        Args:
            idx: Tuple of (x_power, y_power)
            
        Returns:
            Coefficient for x^i * y^j term
        """
        ...
    
    def __setitem__(self, idx: tuple[int, int], val: float) -> None:
        """
        Set coefficient at (i, j).
        
        Args:
            idx: Tuple of (x_power, y_power)
            val: New coefficient value
        """
        ...
    
    def __str__(self) -> str:
        """Return string representation."""
        ...
    
    def __deepcopy__(self, memo: Dict[int, Any]) -> Poly2D:
        """Create deep copy."""
        ...
    
    def __call__(self, x: List[float], y: List[float]) -> List[float]:
        """
        Evaluate polynomial at multiple (x,y) points.
        
        Args:
            x: List of X coordinates
            y: List of Y coordinates (same length as x)
            
        Returns:
            List of P(x[i], y[i]) for each i
        """
        ...
    
    def asArray(self) -> NDArray[np.float64]:
        """
        Convert coefficients to 2D NumPy array.
        
        Returns:
            2D array where element [i,j] is coefficient for x^i * y^j
        """
        ...
    
    @staticmethod
    def fromArray(array: NDArray[np.float64]) -> Poly2D:
        """
        Create 2D polynomial from NumPy array.
        
        Args:
            array: 2D NumPy array of coefficients
            
        Returns:
            New Poly2D instance
        """
        ...
    
    def __getstate__(self) -> bytes:
        """Pickle support."""
        ...
    
    def __setstate__(self, state: bytes) -> None:
        """Pickle support."""
        ...


class PolyVector3:
    """
    One-dimensional polynomial with Vector3 coefficients.
    
    Each coefficient is a 3D vector, allowing polynomial evaluation
    to return 3D vectors. Useful for parametric curves.
    """
    
    @overload
    def __init__(self) -> None:
        """Create empty polynomial."""
        ...
    
    @overload
    def __init__(self, order: int) -> None:
        """
        Create polynomial of given order.
        
        Args:
            order: Polynomial order
        """
        ...
    
    def order(self) -> int:
        """Get polynomial order."""
        ...
    
    def size(self) -> int:
        """Get number of coefficients."""
        ...
    
    def __getitem__(self, i: int) -> Vector3:
        """Get coefficient at index."""
        ...
    
    def __setitem__(self, i: int, val: Vector3) -> None:
        """Set coefficient at index."""
        ...
    
    def __str__(self) -> str:
        """Return string representation."""
        ...
    
    def __deepcopy__(self, memo: Dict[int, Any]) -> PolyVector3:
        """Create deep copy."""
        ...
    
    def __call__(self, input: List[float]) -> List[Vector3]:
        """
        Evaluate polynomial at multiple points.
        
        Args:
            input: List of parameter values
            
        Returns:
            List of Vector3 results
        """
        ...


# Polynomial fitting functions

@overload
def fit(x: List[float], y: List[float], order: int) -> Poly1D:
    """
    Fit 1D polynomial to data using least squares.
    
    Args:
        x: X coordinates
        y: Y values
        order: Polynomial order to fit
        
    Returns:
        Fitted Poly1D
    """
    ...

@overload
def fit(x: VectorDouble, y: VectorDouble, order: int) -> Poly1D:
    """
    Fit 1D polynomial to data using VectorDouble.
    
    Args:
        x: X coordinates as VectorDouble
        y: Y values as VectorDouble
        order: Polynomial order to fit
        
    Returns:
        Fitted Poly1D
    """
    ...

@overload
def fit(x: List[float], y: List[float], z: List[float], 
        orderX: int, orderY: int) -> Poly2D:
    """
    Fit 2D polynomial to data using least squares.
    
    Args:
        x: X coordinates
        y: Y coordinates
        z: Z values (dependent variable)
        orderX: Polynomial order in X
        orderY: Polynomial order in Y
        
    Returns:
        Fitted Poly2D
    """
    ...

@overload
def fit(x: MatrixDouble, y: MatrixDouble, z: MatrixDouble,
        orderX: int, orderY: int) -> Poly2D:
    """
    Fit 2D polynomial to gridded data.
    
    Args:
        x: X coordinates as MatrixDouble
        y: Y coordinates as MatrixDouble
        z: Z values as MatrixDouble
        orderX: Polynomial order in X
        orderY: Polynomial order in Y
        
    Returns:
        Fitted Poly2D
    """
    ...
