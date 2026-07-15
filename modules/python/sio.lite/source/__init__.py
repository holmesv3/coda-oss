"""
CODA-OSS sio.lite Python Module
================================

Provides high-level NumPy-integrated I/O for SIO (Simple Image Output) files.

Public API
----------
Classes:
    FileHeader - SIO file header with metadata
    FileWriter - Write SIO files
    StreamReader - Read SIO streams
    FileReader - Read SIO files (seekable)

Functions:
    read(filename) - Read SIO file as NumPy array
    write(array, filename, elementType=None) - Write NumPy array to SIO file
    dtypeFromSioType(elementType, elementSize) - Convert SIO type to NumPy dtype
    sioTypeFromDtype(dtype) - Convert NumPy dtype to SIO type

Example
-------
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

# Import C++ bindings
from .coda_sio_lite import (
    FileHeader,
    FileWriter,
    StreamReader,
    FileReader
)

import numpy


def dtypeFromSioType(elementType, elementSize):
    """
    Convert an SIO type & size to a NumPy dtype.
    
    Complex integer types are not supported.
    
    Parameters
    ----------
    elementType : int
        SIO element type constant (e.g., FileHeader.FLOAT)
    elementSize : int
        Size of each element in bytes
    
    Returns
    -------
    numpy.dtype
        Corresponding NumPy data type
    
    Raises
    ------
    Exception
        If the element type is unknown or unsupported
    """
    typeMap = {
        FileHeader.UNSIGNED: 'uint',
        FileHeader.SIGNED: 'int',
        FileHeader.FLOAT: 'float',
        FileHeader.COMPLEX_FLOAT: 'complex'
    }
    
    if elementType not in typeMap:
        raise Exception("Unknown element type: " + str(elementType))
    
    dtypeStr = "%s%s" % (typeMap[elementType], elementSize * 8)
    
    return numpy.dtype(dtypeStr)


def sioTypeFromDtype(dtype):
    """
    Convert a NumPy dtype into an SIO type.
    
    Parameters
    ----------
    dtype : dtype or str or type
        NumPy dtype to convert
    
    Returns
    -------
    int
        SIO element type constant
    
    Raises
    ------
    Exception
        If the dtype kind is unknown or unsupported
    """
    # Handle dtypes, strings, numpy types
    dt = numpy.dtype(dtype)
    
    kindToType = {
        'i': FileHeader.SIGNED,
        'u': FileHeader.UNSIGNED,
        'f': FileHeader.FLOAT,
        'c': FileHeader.COMPLEX_FLOAT
    }
    
    if dt.kind not in kindToType:
        raise Exception("Unknown element type: " + str(dt.kind))
    
    return kindToType[dt.kind]


def write(numpyArray, outputPathname, elementType=None):
    """
    Write a NumPy array to an SIO file.
    
    Parameters
    ----------
    numpyArray : numpy.ndarray
        2D NumPy array to write
    outputPathname : str
        Path to output SIO file
    elementType : int or str or dtype, optional
        Element type for output. Can be:
        - SIO type constant (e.g., FileHeader.FLOAT)
        - NumPy dtype string (e.g., 'float32')
        - NumPy dtype object or type
        If None, uses the array's dtype
    
    Raises
    ------
    Exception
        If array is not 2-dimensional or if data pointer is NULL
    """
    # Make sure this array is sized properly
    if len(numpyArray.shape) != 2:
        raise Exception("Only 2 dimensional images are supported")
    if elementType is None:
        elementType = numpyArray.dtype

    if type(elementType) != int:
        elementType = sioTypeFromDtype(elementType)

    if not numpyArray.flags['C_CONTIGUOUS']:
        numpyArray = numpy.ascontiguousarray(numpyArray)

    header = FileHeader(numpyArray.shape[0],
                        numpyArray.shape[1],
                        numpyArray.strides[1],
                        elementType)

    pointer, ro = numpyArray.__array_interface__['data']

    if pointer == 0 or pointer == None:
        raise Exception("Attempting to write a NULL image")

    writer = FileWriter(outputPathname)
    writer.write(header, pointer)


def read(inputPathname):
    """
    Read an SIO file as a NumPy array.
    
    Parameters
    ----------
    inputPathname : str
        Path to input SIO file
    
    Returns
    -------
    numpy.ndarray
        2D NumPy array containing the SIO file data
    """
    reader = FileReader(inputPathname)
    header = reader.getHeader()

    elementSize = header.getElementSize()
    dtype = dtypeFromSioType(header.getElementType(), elementSize)

    numpyArray = numpy.empty(shape = (header.getNumLines(),
                                      header.getNumElements()),
                             dtype = dtype)
    pointer, ro = numpyArray.__array_interface__['data']
    reader.read(pointer, numpyArray.shape[0] * numpyArray.shape[1] * elementSize)
    return numpyArray


# Public API
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
