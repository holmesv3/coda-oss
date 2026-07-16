"""
Type stubs for coda_sio_lite module.

This module provides the C++ bindings for SIO (Simple Image Output) file I/O.
SIO is a simple binary image format with header metadata.

For the complete Python API with NumPy integration, see the parent module
documentation (use `from coda.sio_lite import ...` instead of importing
this module directly).

Classes:
    FileHeader: SIO file header with metadata and element type definitions
    FileWriter: Write SIO files from raw pointers or NumPy arrays
    StreamReader: Read SIO data from input streams
    FileReader: Read SIO files with seeking support

Note:
    This is the low-level C++ binding module. The parent sio_lite module
    provides higher-level Python functions (read, write) that integrate
    with NumPy arrays.
"""

from typing import Any, List, overload
from numpy.typing import NDArray

class FileHeader:
    """
    SIO file header containing metadata and element type information.
    
    Defines the dimensions (lines, elements), data type, and optional
    user-defined metadata fields.
    """
    
    # Element type constants
    UNSIGNED: int
    SIGNED: int
    FLOAT: int
    COMPLEX_UNSIGNED: int
    COMPLEX_SIGNED: int
    COMPLEX_FLOAT: int
    N_BYTE_UNSIGNED: int
    N_BYTE_SIGNED: int
    
    @overload
    def __init__(self) -> None:
        """Create empty header."""
        ...
    
    @overload
    def __init__(self, numLines: int, numElements: int, 
                 elementSize: int, elementType: int) -> None:
        """
        Create header with dimensions and element type.
        
        Args:
            numLines: Number of lines (rows)
            numElements: Number of elements per line (columns)
            elementSize: Size of each element in bytes
            elementType: Element type constant (UNSIGNED, SIGNED, FLOAT, etc.)
        """
        ...
    
    def getLength(self) -> int:
        """
        Get header length in bytes.
        
        Returns:
            Size of header structure
        """
        ...
    
    def getNumLines(self) -> int:
        """
        Get number of lines (rows).
        
        Returns:
            Number of lines in image
        """
        ...
    
    def setNumLines(self, numLines: int) -> None:
        """Set number of lines."""
        ...
    
    def getNumElements(self) -> int:
        """
        Get number of elements per line (columns).
        
        Returns:
            Number of elements (width)
        """
        ...
    
    def setNumElements(self, numElements: int) -> None:
        """Set number of elements per line."""
        ...
    
    def getElementSize(self) -> int:
        """
        Get element size in bytes.
        
        Returns:
            Size of each element
        """
        ...
    
    def setElementSize(self, elementSize: int) -> None:
        """Set element size in bytes."""
        ...
    
    def getElementType(self) -> int:
        """
        Get element type constant.
        
        Returns:
            Element type (UNSIGNED, SIGNED, FLOAT, etc.)
        """
        ...
    
    def setElementType(self, elementType: int) -> None:
        """Set element type."""
        ...
    
    def getElementTypeAsString(self) -> str:
        """
        Get element type as human-readable string.
        
        Returns:
            String description of element type
        """
        ...
    
    def getVersion(self) -> int:
        """Get SIO format version."""
        ...
    
    def setVersion(self, version: int) -> None:
        """Set SIO format version."""
        ...
    
    def isDifferentByteOrdering(self) -> bool:
        """
        Check if file byte order differs from system.
        
        Returns:
            True if byte swapping is needed
        """
        ...
    
    def userDataFieldExists(self, key: str) -> bool:
        """
        Check if user data field exists.
        
        Args:
            key: Field name
            
        Returns:
            True if field exists in header
        """
        ...
    
    def getUserData(self, key: str) -> List[int]:
        """
        Get user data field as byte list.
        
        Args:
            key: Field name
            
        Returns:
            List of bytes for field value
            
        Raises:
            Exception: If field does not exist
        """
        ...
    
    @overload
    def addUserData(self, key: str, value: str) -> None:
        """
        Add string user data field.
        
        Args:
            key: Field name
            value: String value
        """
        ...
    
    @overload
    def addUserData(self, key: str, value: int) -> None:
        """
        Add integer user data field.
        
        Args:
            key: Field name
            value: Integer value
        """
        ...


class FileWriter:
    """
    Write SIO files from headers and data.
    
    Supports writing from raw memory pointers or NumPy arrays.
    """
    
    @overload
    def __init__(self, outputFile: str) -> None:
        """
        Create writer for file.
        
        Args:
            outputFile: Path to output file
        """
        ...
    
    @overload
    def __init__(self, stream: Any, adopt: bool = True) -> None:
        """
        Create writer for output stream.
        
        Args:
            stream: OutputStream object
            adopt: If True, writer takes ownership of stream
        """
        ...
    
    def write(self, header: FileHeader, data: int) -> None:
        """
        Write header and data from raw pointer.
        
        Args:
            header: File header
            data: Memory pointer (integer address) to data
            
        Note:
            This is a low-level method. Use writeArray() for NumPy arrays.
        """
        ...
    
    def writeArray(self, header: FileHeader, array: NDArray[Any]) -> None:
        """
        Write header and data from NumPy array.
        
        Args:
            header: File header
            array: NumPy array to write
            
        Note:
            Array shape must match header dimensions.
        """
        ...


class StreamReader:
    """
    Read SIO data from input stream.
    
    Base class for reading SIO format from any input stream.
    """
    
    @overload
    def __init__(self) -> None:
        """Create uninitialized reader."""
        ...
    
    @overload
    def __init__(self, inputStream: Any, adopt: bool = False) -> None:
        """
        Create reader for input stream.
        
        Args:
            inputStream: InputStream object
            adopt: If True, reader takes ownership of stream
        """
        ...
    
    def setInputStream(self, inputStream: Any, adopt: bool = False) -> None:
        """
        Set input stream.
        
        Args:
            inputStream: InputStream object
            adopt: If True, reader takes ownership
        """
        ...
    
    def getInputStream(self) -> Any:
        """
        Get input stream.
        
        Returns:
            InputStream object
        """
        ...
    
    def getHeader(self) -> FileHeader:
        """
        Get file header.
        
        Returns:
            FileHeader object with metadata
            
        Note:
            Stream must be positioned at start of file
        """
        ...
    
    def read(self, data: int, size: int) -> int:
        """
        Read data to raw pointer.
        
        Args:
            data: Memory pointer (integer address)
            size: Number of bytes to read
            
        Returns:
            Number of bytes actually read
        """
        ...
    
    def readArray(self, array: NDArray[Any]) -> int:
        """
        Read data into NumPy array.
        
        Args:
            array: NumPy array to fill (must be pre-allocated)
            
        Returns:
            Number of bytes read
        """
        ...
    
    def available(self) -> int:
        """
        Get number of bytes available.
        
        Returns:
            Bytes available for reading
        """
        ...


class FileReader(StreamReader):
    """
    Read SIO files with seeking support.
    
    File-based reader that supports random access to SIO data.
    """
    
    @overload
    def __init__(self) -> None:
        """Create uninitialized reader."""
        ...
    
    @overload
    def __init__(self, file: str) -> None:
        """
        Create reader for file.
        
        Args:
            file: Path to SIO file
            
        Raises:
            Exception: If file cannot be opened
        """
        ...
    
    @overload
    def __init__(self, inputStream: Any, adopt: bool = False) -> None:
        """
        Create reader for file input stream.
        
        Args:
            inputStream: FileInputStream object
            adopt: If True, reader takes ownership
        """
        ...
    
    def seek(self, offset: int, whence: int) -> None:
        """
        Seek to position in file.
        
        Args:
            offset: Byte offset
            whence: Reference point (0=start, 1=current, 2=end)
        """
        ...
    
    def tell(self) -> int:
        """
        Get current position.
        
        Returns:
            Current byte offset
        """
        ...
