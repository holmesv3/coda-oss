"""
Type stubs for coda_types module.

This module provides coordinate types and vector containers commonly used
in image processing and geospatial applications.

Classes:
    RowColDouble: 2D coordinate with double-precision row/col values
    RowColInt: 2D coordinate with signed integer row/col values
    RowColSizeT: 2D coordinate with unsigned size_t row/col values
    RgAzDouble: Range/Azimuth coordinate with double-precision values
    VectorRowColInt: Vector container for RowColInt objects
    VectorRowColDouble: Vector container for RowColDouble objects
    VectorSizeT: Vector container for size_t values
    VectorString: Vector container for strings
"""

from typing import List, Tuple, Union, overload

class RowColDouble:
    """
    Two-dimensional coordinate with double-precision row and column values.
    
    Supports arithmetic operations with other RowColDouble instances and scalars.
    """
    
    row: float
    col: float
    
    @overload
    def __init__(self) -> None:
        """Initialize with row=0.0, col=0.0."""
        ...
    
    @overload
    def __init__(self, row: float, col: float) -> None:
        """Initialize with specified row and column values."""
        ...
    
    # Arithmetic operators with RowColDouble
    def __add__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    def __sub__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    def __mul__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    def __truediv__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    
    # Augmented assignment operators
    def __iadd__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    def __isub__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    def __imul__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    def __itruediv__(self, other: Union[RowColDouble, float]) -> RowColDouble: ...
    
    # Comparison operators
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    
    # String representation
    def __repr__(self) -> str: ...
    
    # Pickle support
    def __getstate__(self) -> Tuple[float, float]: ...
    def __setstate__(self, state: Tuple[float, float]) -> None: ...


class RowColInt:
    """
    Two-dimensional coordinate with signed integer row and column values.
    
    Supports arithmetic operations with other RowColInt instances and scalars.
    """
    
    row: int
    col: int
    
    @overload
    def __init__(self) -> None:
        """Initialize with row=0, col=0."""
        ...
    
    @overload
    def __init__(self, row: int, col: int) -> None:
        """Initialize with specified row and column values."""
        ...
    
    # Arithmetic operators
    def __add__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    def __sub__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    def __mul__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    def __truediv__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    
    # Augmented assignment operators
    def __iadd__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    def __isub__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    def __imul__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    def __itruediv__(self, other: Union[RowColInt, int]) -> RowColInt: ...
    
    # Comparison operators
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    
    # String representation
    def __repr__(self) -> str: ...
    
    # Pickle support
    def __getstate__(self) -> Tuple[int, int]: ...
    def __setstate__(self, state: Tuple[int, int]) -> None: ...


class RowColSizeT:
    """
    Two-dimensional coordinate with unsigned size_t row and column values.
    
    Supports arithmetic operations with other RowColSizeT instances and scalars.
    """
    
    row: int  # Note: Python int for size_t
    col: int
    
    @overload
    def __init__(self) -> None:
        """Initialize with row=0, col=0."""
        ...
    
    @overload
    def __init__(self, row: int, col: int) -> None:
        """Initialize with specified row and column values."""
        ...
    
    # Arithmetic operators
    def __add__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    def __sub__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    def __mul__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    def __truediv__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    
    # Augmented assignment operators
    def __iadd__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    def __isub__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    def __imul__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    def __itruediv__(self, other: Union[RowColSizeT, int]) -> RowColSizeT: ...
    
    # Comparison operators
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    
    # String representation
    def __repr__(self) -> str: ...
    
    # Pickle support
    def __getstate__(self) -> Tuple[int, int]: ...
    def __setstate__(self, state: Tuple[int, int]) -> None: ...


class RgAzDouble:
    """
    Range/Azimuth coordinate with double-precision values.
    
    Used for radar and sensor coordinate systems where 'rg' represents
    range (distance) and 'az' represents azimuth (angle).
    """
    
    rg: float
    az: float
    
    @overload
    def __init__(self) -> None:
        """Initialize with rg=0.0, az=0.0."""
        ...
    
    @overload
    def __init__(self, rg: float, az: float) -> None:
        """Initialize with specified range and azimuth values."""
        ...
    
    # Arithmetic operators
    def __add__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    def __sub__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    def __mul__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    def __truediv__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    
    # Augmented assignment operators
    def __iadd__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    def __isub__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    def __imul__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    def __itruediv__(self, other: Union[RgAzDouble, float]) -> RgAzDouble: ...
    
    # Comparison operators
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    
    # String representation
    def __repr__(self) -> str: ...
    
    # Pickle support
    def __getstate__(self) -> Tuple[float, float]: ...
    def __setstate__(self, state: Tuple[float, float]) -> None: ...


class VectorRowColInt:
    """
    Vector container for RowColInt objects.
    
    Provides list-like interface with indexing, iteration, and modification.
    """
    
    def __init__(self) -> None:
        """Initialize empty vector."""
        ...
    
    def __len__(self) -> int:
        """Return number of elements."""
        ...
    
    def __getitem__(self, index: int) -> RowColInt:
        """Get element at index."""
        ...
    
    def __setitem__(self, index: int, value: RowColInt) -> None:
        """Set element at index."""
        ...
    
    def __delitem__(self, index: int) -> None:
        """Delete element at index."""
        ...
    
    def __iter__(self):
        """Return iterator over elements."""
        ...
    
    def append(self, value: RowColInt) -> None:
        """Append element to end."""
        ...
    
    def clear(self) -> None:
        """Remove all elements."""
        ...
    
    def extend(self, other: VectorRowColInt) -> None:
        """Extend vector with elements from other."""
        ...
    
    def insert(self, index: int, value: RowColInt) -> None:
        """Insert element at index."""
        ...
    
    def pop(self, index: int = -1) -> RowColInt:
        """Remove and return element at index."""
        ...
    
    # Pickle support
    def __getstate__(self) -> bytes: ...
    def __setstate__(self, state: bytes) -> None: ...


class VectorRowColDouble:
    """
    Vector container for RowColDouble objects.
    
    Provides list-like interface with indexing, iteration, and modification.
    """
    
    def __init__(self) -> None:
        """Initialize empty vector."""
        ...
    
    def __len__(self) -> int:
        """Return number of elements."""
        ...
    
    def __getitem__(self, index: int) -> RowColDouble:
        """Get element at index."""
        ...
    
    def __setitem__(self, index: int, value: RowColDouble) -> None:
        """Set element at index."""
        ...
    
    def __delitem__(self, index: int) -> None:
        """Delete element at index."""
        ...
    
    def __iter__(self):
        """Return iterator over elements."""
        ...
    
    def append(self, value: RowColDouble) -> None:
        """Append element to end."""
        ...
    
    def clear(self) -> None:
        """Remove all elements."""
        ...
    
    def extend(self, other: VectorRowColDouble) -> None:
        """Extend vector with elements from other."""
        ...
    
    def insert(self, index: int, value: RowColDouble) -> None:
        """Insert element at index."""
        ...
    
    def pop(self, index: int = -1) -> RowColDouble:
        """Remove and return element at index."""
        ...
    
    # Pickle support
    def __getstate__(self) -> bytes: ...
    def __setstate__(self, state: bytes) -> None: ...


class VectorSizeT:
    """
    Vector container for size_t (unsigned integer) values.
    
    Provides list-like interface with indexing, iteration, and modification.
    """
    
    def __init__(self) -> None:
        """Initialize empty vector."""
        ...
    
    def __len__(self) -> int:
        """Return number of elements."""
        ...
    
    def __getitem__(self, index: int) -> int:
        """Get element at index."""
        ...
    
    def __setitem__(self, index: int, value: int) -> None:
        """Set element at index."""
        ...
    
    def __delitem__(self, index: int) -> None:
        """Delete element at index."""
        ...
    
    def __iter__(self):
        """Return iterator over elements."""
        ...
    
    def append(self, value: int) -> None:
        """Append element to end."""
        ...
    
    def clear(self) -> None:
        """Remove all elements."""
        ...
    
    def extend(self, other: VectorSizeT) -> None:
        """Extend vector with elements from other."""
        ...
    
    def insert(self, index: int, value: int) -> None:
        """Insert element at index."""
        ...
    
    def pop(self, index: int = -1) -> int:
        """Remove and return element at index."""
        ...


class VectorString:
    """
    Vector container for string values.
    
    Provides list-like interface with indexing, iteration, and modification.
    """
    
    def __init__(self) -> None:
        """Initialize empty vector."""
        ...
    
    def __len__(self) -> int:
        """Return number of elements."""
        ...
    
    def __getitem__(self, index: int) -> str:
        """Get element at index."""
        ...
    
    def __setitem__(self, index: int, value: str) -> None:
        """Set element at index."""
        ...
    
    def __delitem__(self, index: int) -> None:
        """Delete element at index."""
        ...
    
    def __iter__(self):
        """Return iterator over elements."""
        ...
    
    def append(self, value: str) -> None:
        """Append element to end."""
        ...
    
    def clear(self) -> None:
        """Remove all elements."""
        ...
    
    def extend(self, other: VectorString) -> None:
        """Extend vector with elements from other."""
        ...
    
    def insert(self, index: int, value: str) -> None:
        """Insert element at index."""
        ...
    
    def pop(self, index: int = -1) -> str:
        """Remove and return element at index."""
        ...
