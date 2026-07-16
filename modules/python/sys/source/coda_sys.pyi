"""
Type stubs for coda_sys module.

This module provides system-level utilities including date/time handling,
byte order operations, and memory alignment functions.

Classes:
    UTCDateTime: UTC date/time representation with multiple construction options

Functions:
    isBigEndianSystem: Check system byte order
    byteSwap: Swap byte order of data in-place or to output buffer
    alignedAlloc: Allocate aligned memory
    alignedFree: Free aligned memory

Constants:
    SSE_INSTRUCTION_ALIGNMENT: Alignment requirement for SSE instructions
    NativeLayer_func__: Native layer function identifier
    SYS_FUNC: System function macro value
"""

from typing import Any, overload

# Module constants
SSE_INSTRUCTION_ALIGNMENT: int
NativeLayer_func__: str
SYS_FUNC: str


def isBigEndianSystem() -> bool:
    """
    Check if the current system uses big-endian byte order.
    
    Returns:
        True if system is big-endian, False if little-endian
    """
    ...


@overload
def byteSwap(buffer: Any, elemSize: int, numElems: int) -> None:
    """
    Swap byte order of elements in buffer (in-place).
    
    Args:
        buffer: Memory buffer (capsule or array interface)
        elemSize: Size of each element in bytes
        numElems: Number of elements to swap
    """
    ...


@overload
def byteSwap(buffer: Any, elemSize: int, numElems: int, outputBuffer: Any) -> None:
    """
    Swap byte order of elements from input to output buffer.
    
    Args:
        buffer: Input memory buffer
        elemSize: Size of each element in bytes
        numElems: Number of elements to swap
        outputBuffer: Output memory buffer
    """
    ...


@overload
def alignedAlloc(size: int) -> Any:
    """
    Allocate aligned memory with default alignment.
    
    Args:
        size: Number of bytes to allocate
        
    Returns:
        Memory capsule pointer to aligned memory
        
    Note:
        Must be freed with alignedFree()
    """
    ...


@overload
def alignedAlloc(size: int, alignment: int) -> Any:
    """
    Allocate aligned memory with specified alignment.
    
    Args:
        size: Number of bytes to allocate
        alignment: Alignment requirement in bytes (must be power of 2)
        
    Returns:
        Memory capsule pointer to aligned memory
        
    Note:
        Must be freed with alignedFree()
    """
    ...


def alignedFree(p: Any) -> None:
    """
    Free memory allocated by alignedAlloc.
    
    Args:
        p: Memory capsule returned by alignedAlloc()
    """
    ...


class UTCDateTime:
    """
    UTC date and time representation.
    
    Provides comprehensive date/time handling with multiple construction
    options including current time, component-based, timestamp-based, and
    string parsing (ISO8601 and custom formats).
    """
    
    @overload
    def __init__(self) -> None:
        """Initialize with current UTC time."""
        ...
    
    @overload
    def __init__(self, hour: int, minute: int, second: float) -> None:
        """
        Initialize with time only (date defaults to epoch).
        
        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second with fractional part (0.0-59.999...)
        """
        ...
    
    @overload
    def __init__(self, year: int, month: int, day: int) -> None:
        """
        Initialize with date only (time defaults to midnight).
        
        Args:
            year: Year
            month: Month (1-12)
            day: Day of month (1-31)
        """
        ...
    
    @overload
    def __init__(self, year: int, month: int, day: int, 
                 hour: int, minute: int, second: float) -> None:
        """
        Initialize with complete date and time.
        
        Args:
            year: Year
            month: Month (1-12)
            day: Day of month (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second with fractional part (0.0-59.999...)
        """
        ...
    
    @overload
    def __init__(self, timeInMillis: float) -> None:
        """
        Initialize from timestamp in milliseconds since epoch.
        
        Args:
            timeInMillis: Milliseconds since Unix epoch (1970-01-01 00:00:00 UTC)
        """
        ...
    
    @overload
    def __init__(self, time: str) -> None:
        """
        Initialize by parsing ISO8601 date/time string.
        
        Args:
            time: ISO8601 formatted string (e.g., "2024-01-15T10:30:45.123Z")
            
        Raises:
            Exception: If string cannot be parsed
        """
        ...
    
    @overload
    def __init__(self, time: str, format: str) -> None:
        """
        Initialize by parsing date/time string with custom format.
        
        Args:
            time: Date/time string
            format: Format string (strptime-style)
            
        Raises:
            Exception: If string cannot be parsed with given format
        """
        ...
    
    def format(self) -> str:
        """
        Format as ISO8601 string.
        
        Returns:
            ISO8601 formatted date/time string
        """
        ...
    
    def __repr__(self) -> str:
        """Return detailed string representation."""
        ...
    
    def __str__(self) -> str:
        """Return ISO8601 formatted string."""
        ...
