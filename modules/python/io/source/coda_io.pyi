"""
Type stubs for coda_io module.

This module provides stream I/O abstractions for reading and writing data.
The stream hierarchy supports basic I/O operations, seekable streams, and
bidirectional streams with both input and output capabilities.

Classes:
    InputStream: Abstract base class for input streams
    OutputStream: Abstract base class for output streams
    BidirectionalStream: Stream supporting both input and output
    Seekable: Interface for seekable streams
    SeekableInputStream: Input stream with seek support
    SeekableOutputStream: Output stream with seek support
    StringStream: In-memory stream for string/bytes I/O
    FileInputStream: File-based input stream
    FileOutputStream: File-based output stream

The module follows standard Python I/O conventions with read/write/seek methods.
"""

from typing import Union, overload

class Seekable:
    """
    Interface for streams that support seeking to arbitrary positions.
    
    Provides seek() and tell() methods for position management.
    """
    
    def seek(self, offset: int, whence: int) -> None:
        """
        Seek to position in stream.
        
        Args:
            offset: Byte offset
            whence: Reference point (0=start, 1=current, 2=end)
        """
        ...
    
    def tell(self) -> int:
        """
        Get current position in stream.
        
        Returns:
            Current byte offset from start of stream
        """
        ...


class InputStream:
    """
    Abstract base class for input streams.
    
    Provides methods for reading bytes from a stream and querying
    available data.
    """
    
    def read(self, size: int) -> bytes:
        """
        Read up to size bytes from stream.
        
        Args:
            size: Maximum number of bytes to read
            
        Returns:
            Bytes read from stream (may be fewer than requested)
        """
        ...
    
    def available(self) -> int:
        """
        Get number of bytes available for reading without blocking.
        
        Returns:
            Number of bytes available
        """
        ...


class OutputStream:
    """
    Abstract base class for output streams.
    
    Provides methods for writing data and flushing buffers.
    """
    
    def write(self, data: Union[str, bytes]) -> None:
        """
        Write data to stream.
        
        Args:
            data: String or bytes to write
        """
        ...
    
    def flush(self) -> None:
        """
        Flush any buffered data to underlying storage.
        """
        ...


class BidirectionalStream(InputStream):
    """
    Stream supporting both input and output operations.
    
    Inherits read operations from InputStream and adds write operations.
    Useful for sockets, pipes, and in-memory buffers.
    """
    
    def write(self, data: Union[str, bytes]) -> None:
        """
        Write data to stream.
        
        Args:
            data: String or bytes to write
        """
        ...
    
    def flush(self) -> None:
        """
        Flush any buffered data to underlying storage.
        """
        ...


class SeekableInputStream(InputStream):
    """
    Input stream with seeking support.
    
    Combines InputStream functionality with Seekable interface.
    """
    
    def seek(self, offset: int, whence: int) -> None:
        """
        Seek to position in stream.
        
        Args:
            offset: Byte offset
            whence: Reference point (0=start, 1=current, 2=end)
        """
        ...
    
    def tell(self) -> int:
        """
        Get current position in stream.
        
        Returns:
            Current byte offset from start of stream
        """
        ...


class SeekableOutputStream(OutputStream):
    """
    Output stream with seeking support.
    
    Combines OutputStream functionality with Seekable interface.
    """
    
    def seek(self, offset: int, whence: int) -> None:
        """
        Seek to position in stream.
        
        Args:
            offset: Byte offset
            whence: Reference point (0=start, 1=current, 2=end)
        """
        ...
    
    def tell(self) -> int:
        """
        Get current position in stream.
        
        Returns:
            Current byte offset from start of stream
        """
        ...


class StringStream(BidirectionalStream):
    """
    In-memory bidirectional stream for string and bytes I/O.
    
    Useful for testing, buffering, and working with data in memory
    without file system access. Supports both string and bytes operations.
    """
    
    def __init__(self) -> None:
        """Initialize empty string stream."""
        ...
    
    def str(self) -> str:
        """
        Get complete stream contents as string.
        
        Returns:
            All data written to stream as string
        """
        ...
    
    def writeBytes(self, data: bytes) -> None:
        """
        Write raw bytes to stream.
        
        Args:
            data: Bytes to write
        """
        ...


class FileInputStream(SeekableInputStream):
    """
    File-based input stream with seeking support.
    
    Opens a file for reading and provides stream interface with
    random access capabilities.
    """
    
    def __init__(self, filename: str) -> None:
        """
        Open file for reading.
        
        Args:
            filename: Path to file to open
            
        Raises:
            Exception: If file cannot be opened
        """
        ...


class FileOutputStream(SeekableOutputStream):
    """
    File-based output stream with seeking support.
    
    Opens or creates a file for writing and provides stream interface
    with random access capabilities.
    """
    
    @overload
    def __init__(self, filename: str) -> None:
        """
        Open file for writing with default flags (create/truncate).
        
        Args:
            filename: Path to file to open or create
        """
        ...
    
    @overload
    def __init__(self, filename: str, creationFlags: int) -> None:
        """
        Open file for writing with specified creation flags.
        
        Args:
            filename: Path to file to open or create
            creationFlags: File creation mode flags
        """
        ...
