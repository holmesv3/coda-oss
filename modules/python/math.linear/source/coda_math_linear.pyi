"""
Type stubs for coda_math_linear module.

This module provides linear algebra types including fixed-size and dynamic
vectors and matrices. Supports basic operations, indexing, and conversion
to/from Python lists.

Classes:
    Vector2: Fixed 2D vector
    Vector3: Fixed 3D vector
    VectorDouble: Dynamic-size vector
    MatrixDouble: Dynamic 2D matrix
    Matrix1x1, Matrix1x2, Matrix1x3: Fixed 1-row matrices
    Matrix2x1, Matrix2x2, Matrix2x3, Matrix2x7: Fixed 2-row matrices
    Matrix3x1, Matrix3x2, Matrix3x3, Matrix3x7: Fixed 3-row matrices
    Matrix7x2, Matrix7x3, Matrix7x7: Fixed 7-row matrices

Functions:
    cross: Compute cross product of two Vector3 objects
"""

from typing import List, Tuple, Any, Dict, overload

class Vector2:
    """
    Fixed-size 2D vector with double-precision elements.
    
    Provides indexed access to two elements and conversion to/from lists.
    """
    
    @overload
    def __init__(self) -> None:
        """Initialize with zeros."""
        ...
    
    @overload
    def __init__(self, values: List[float]) -> None:
        """
        Initialize from list.
        
        Args:
            values: List of 2 float values
        """
        ...
    
    def __getitem__(self, i: int) -> float:
        """
        Get element at index.
        
        Args:
            i: Index (0 or 1)
            
        Returns:
            Element value
        """
        ...
    
    def __setitem__(self, i: int, val: float) -> None:
        """
        Set element at index.
        
        Args:
            i: Index (0 or 1)
            val: New value
        """
        ...
    
    def __str__(self) -> str:
        """Return string representation."""
        ...
    
    def __deepcopy__(self, memo: Dict[int, Any]) -> Vector2:
        """
        Create deep copy.
        
        Args:
            memo: Copy memo dictionary
            
        Returns:
            New Vector2 instance
        """
        ...
    
    def vals(self) -> List[float]:
        """
        Get values as list.
        
        Returns:
            List of 2 float values
        """
        ...
    
    def __getstate__(self) -> bytes:
        """Pickle support."""
        ...
    
    def __setstate__(self, state: bytes) -> None:
        """Pickle support."""
        ...


class Vector3:
    """
    Fixed-size 3D vector with double-precision elements.
    
    Provides indexed access to three elements and conversion to/from lists.
    Used for 3D coordinates and cross product operations.
    """
    
    @overload
    def __init__(self) -> None:
        """Initialize with zeros."""
        ...
    
    @overload
    def __init__(self, values: List[float]) -> None:
        """
        Initialize from list.
        
        Args:
            values: List of 3 float values
        """
        ...
    
    def __getitem__(self, i: int) -> float:
        """Get element at index (0-2)."""
        ...
    
    def __setitem__(self, i: int, val: float) -> None:
        """Set element at index (0-2)."""
        ...
    
    def __str__(self) -> str:
        """Return string representation."""
        ...
    
    def __deepcopy__(self, memo: Dict[int, Any]) -> Vector3:
        """Create deep copy."""
        ...
    
    def vals(self) -> List[float]:
        """
        Get values as list.
        
        Returns:
            List of 3 float values
        """
        ...
    
    def __getstate__(self) -> bytes:
        """Pickle support."""
        ...
    
    def __setstate__(self, state: bytes) -> None:
        """Pickle support."""
        ...


class VectorDouble:
    """
    Dynamic-size vector with double-precision elements.
    
    Resizable vector that can hold any number of elements.
    """
    
    @overload
    def __init__(self, size: int) -> None:
        """
        Initialize with size.
        
        Args:
            size: Number of elements (initialized to zero)
        """
        ...
    
    @overload
    def __init__(self, values: List[float]) -> None:
        """
        Initialize from list.
        
        Args:
            values: List of float values
        """
        ...
    
    def size(self) -> int:
        """
        Get number of elements.
        
        Returns:
            Vector size
        """
        ...
    
    def __getitem__(self, i: int) -> float:
        """Get element at index."""
        ...
    
    def __setitem__(self, i: int, val: float) -> None:
        """Set element at index."""
        ...
    
    def __str__(self) -> str:
        """Return string representation."""
        ...
    
    def vals(self) -> List[float]:
        """
        Get values as list.
        
        Returns:
            List of all elements
        """
        ...


class MatrixDouble:
    """
    Dynamic 2D matrix with double-precision elements.
    
    Resizable matrix with row-major storage and tuple indexing.
    """
    
    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialize matrix with dimensions.
        
        Args:
            rows: Number of rows
            cols: Number of columns
        """
        ...
    
    def rows(self) -> int:
        """Get number of rows."""
        ...
    
    def cols(self) -> int:
        """Get number of columns."""
        ...
    
    def __getitem__(self, idx: Tuple[int, int]) -> float:
        """
        Get element at (row, col).
        
        Args:
            idx: Tuple of (row_index, col_index)
            
        Returns:
            Element value
        """
        ...
    
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None:
        """
        Set element at (row, col).
        
        Args:
            idx: Tuple of (row_index, col_index)
            val: New value
        """
        ...
    
    def __str__(self) -> str:
        """Return string representation."""
        ...
    
    def vals(self) -> List[List[float]]:
        """
        Get values as nested list.
        
        Returns:
            List of rows, each containing list of column values
        """
        ...


# Fixed-size matrix classes (1xN matrices)

class Matrix1x1:
    """Fixed 1x1 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix1x2:
    """Fixed 1x2 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix1x3:
    """Fixed 1x3 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


# Fixed-size matrix classes (2xN matrices)

class Matrix2x1:
    """Fixed 2x1 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix2x2:
    """Fixed 2x2 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix2x3:
    """Fixed 2x3 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix2x7:
    """Fixed 2x7 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


# Fixed-size matrix classes (3xN matrices)

class Matrix3x1:
    """Fixed 3x1 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix3x2:
    """Fixed 3x2 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix3x3:
    """Fixed 3x3 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix3x7:
    """Fixed 3x7 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


# Fixed-size matrix classes (7xN matrices)

class Matrix7x2:
    """Fixed 7x2 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix7x3:
    """Fixed 7x3 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


class Matrix7x7:
    """Fixed 7x7 matrix."""
    def __init__(self) -> None: ...
    def rows(self) -> int: ...
    def cols(self) -> int: ...
    def __getitem__(self, idx: Tuple[int, int]) -> float: ...
    def __setitem__(self, idx: Tuple[int, int], val: float) -> None: ...
    def __str__(self) -> str: ...
    def vals(self) -> List[List[float]]: ...


# Module functions

def cross(a: Vector3, b: Vector3) -> Vector3:
    """
    Compute cross product of two 3D vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cross product a × b
    """
    ...
