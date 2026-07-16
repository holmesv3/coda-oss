"""
Type stubs for coda.sio_lite module.

This module provides high-level NumPy-integrated I/O for SIO (Simple Image Output) files.
SIO is a simple binary image format with header metadata.

Public API:
    Classes:
        FileHeader: SIO file header with metadata
        FileWriter: Write SIO files
        StreamReader: Read SIO streams
        FileReader: Read SIO files (seekable)
    
    Functions:
        read: Read SIO file as NumPy array
        write: Write NumPy array to SIO file
        dtypeFromSioType: Convert SIO type to NumPy dtype
        sioTypeFromDtype: Convert NumPy dtype to SIO type

Example:
    >>> import numpy as np
    >>> from coda.sio_lite import read, write
    >>> 
    >>> # Write array to SIO file
    >>> data = np.random.rand(100, 200).astype('float32')
    >>> write(data, 'output.sio')
    >>> 
    >>> # Read it back
    >>> result = read('output.sio')
    >>> assert np.allclose(data, result)
"""

from typing import Union, Any
import numpy as np
from numpy.typing import NDArray, DTypeLike

# Re-export C++ bindings
from .coda_sio_lite import (
    FileHeader as FileHeader,
    FileWriter as FileWriter,
    StreamReader as StreamReader,
    FileReader as FileReader,
)

def dtypeFromSioType(elementType: int, elementSize: int) -> np.dtype:
    """
    Convert an SIO type & size to a NumPy dtype.
    
    Complex integer types are not supported.
    
    Args:
        elementType: SIO element type constant (e.g., FileHeader.FLOAT)
        elementSize: Size of each element in bytes
    
    Returns:
        Corresponding NumPy data type
    
    Raises:
        Exception: If the element type is unknown or unsupported
    
    Example:
        >>> dtype = dtypeFromSioType(FileHeader.FLOAT, 4)
        >>> assert dtype == np.float32
    """
    ...

def sioTypeFromDtype(dtype: DTypeLike) -> int:
    """
    Convert a NumPy dtype into an SIO type.
    
    Args:
        dtype: NumPy dtype to convert (can be dtype object, string, or type)
    
    Returns:
        SIO element type constant (FileHeader.SIGNED, UNSIGNED, FLOAT, etc.)
    
    Raises:
        Exception: If the dtype kind is unknown or unsupported
    
    Example:
        >>> sio_type = sioTypeFromDtype(np.float32)
        >>> assert sio_type == FileHeader.FLOAT
    """
    ...

def write(numpyArray: NDArray[Any], outputPathname: str, 
          elementType: Union[int, str, type, None] = None) -> None:
    """
    Write a NumPy array to an SIO file.
    
    Args:
        numpyArray: 2D NumPy array to write
        outputPathname: Path to output SIO file
        elementType: Element type for output. Can be:
            - SIO type constant (e.g., FileHeader.FLOAT)
            - NumPy dtype string (e.g., 'float32')
            - NumPy dtype object or type
            - None (uses the array's dtype)
    
    Raises:
        Exception: If array is not 2-dimensional or if data pointer is NULL
    
    Example:
        >>> import numpy as np
        >>> data = np.random.rand(100, 200).astype('float32')
        >>> write(data, 'output.sio')
        >>> # Or specify different output type
        >>> write(data, 'output.sio', 'float64')
    """
    ...

def read(inputPathname: str) -> NDArray[Any]:
    """
    Read an SIO file as a NumPy array.
    
    Args:
        inputPathname: Path to input SIO file
    
    Returns:
        2D NumPy array containing the SIO file data
    
    Raises:
        Exception: If file cannot be read or is malformed
    
    Example:
        >>> data = read('input.sio')
        >>> print(f"Shape: {data.shape}, dtype: {data.dtype}")
    """
    ...

__all__ = [
    'FileHeader',
    'FileWriter',
    'StreamReader',
    'FileReader',
    'read',
    'write',
    'dtypeFromSioType',
    'sioTypeFromDtype',
]
