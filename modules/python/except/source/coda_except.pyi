"""
Type stubs for coda_except module.

This module provides exception handling with context tracking and stack traces.
The exception model supports source location tracking (file, line, function) and
nested context information for debugging.

Classes:
    Context: Exception context with source location and message
    Trace: Stack trace container for exception propagation
    Throwable: Base throwable class with trace support
    Exception: Standard exception class inheriting from Throwable

Note:
    C++ exceptions are automatically translated to Python RuntimeError
    when crossing the language boundary.
"""

from typing import overload

class Context:
    """
    Exception context containing source location and message information.
    
    Captures where an exception occurred (file, line, function) along with
    optional timestamp and message. Used to build detailed stack traces.
    """
    
    mMessage: str
    mTime: str
    mFunc: str
    mFile: str
    mLine: int
    
    @overload
    def __init__(self, file: str, line: int, func: str) -> None:
        """Initialize context with source location."""
        ...
    
    @overload
    def __init__(self, file: str, line: int, func: str, time: str, message: str) -> None:
        """Initialize context with full information."""
        ...
    
    def getMessage(self) -> str:
        """Get the exception message."""
        ...
    
    def getTime(self) -> str:
        """Get the timestamp when context was created."""
        ...
    
    def getFunction(self) -> str:
        """Get the function name where exception occurred."""
        ...
    
    def getFile(self) -> str:
        """Get the source file name."""
        ...
    
    def getLine(self) -> int:
        """Get the line number in source file."""
        ...
    
    def __str__(self) -> str:
        """Return formatted context string."""
        ...


class Trace:
    """
    Stack trace container for exception propagation.
    
    Maintains a list of Context objects representing the call stack
    when an exception was thrown and rethrown through different layers.
    """
    
    def __init__(self) -> None:
        """Initialize empty trace."""
        ...
    
    def pushContext(self, context: Context) -> None:
        """
        Add a context to the trace stack.
        
        Args:
            context: Context object with source location information
        """
        ...
    
    def getSize(self) -> int:
        """
        Return the number of contexts in the trace.
        
        Returns:
            Number of stack frames
        """
        ...
    
    def __str__(self) -> str:
        """
        Return formatted trace string with all contexts.
        
        Returns:
            Multi-line string showing complete stack trace
        """
        ...


class Throwable:
    """
    Base throwable class with message and trace support.
    
    Provides the foundation for CODA-OSS exception hierarchy. Contains
    a message describing the error and a Trace object tracking where
    the exception occurred and was rethrown.
    """
    
    @overload
    def __init__(self) -> None:
        """Initialize with empty message."""
        ...
    
    @overload
    def __init__(self, message: str) -> None:
        """Initialize with message."""
        ...
    
    @overload
    def __init__(self, context: Context) -> None:
        """Initialize with context (extracts message from context)."""
        ...
    
    def getMessage(self) -> str:
        """
        Get the exception message.
        
        Returns:
            Exception message string
        """
        ...
    
    def getTrace(self) -> Trace:
        """
        Get the exception trace.
        
        Returns:
            Trace object containing stack information
        """
        ...
    
    def getType(self) -> str:
        """
        Get the exception type name.
        
        Returns:
            String identifying the exception type
        """
        ...
    
    def toString(self) -> str:
        """
        Convert exception to detailed string.
        
        Returns:
            String with message and trace information
        """
        ...
    
    def backtrace(self) -> str:
        """
        Get formatted backtrace string.
        
        Returns:
            Multi-line string showing exception backtrace
        """
        ...
    
    def getBacktrace(self) -> str:
        """
        Get formatted backtrace string (alias for backtrace).
        
        Returns:
            Multi-line string showing exception backtrace
        """
        ...
    
    def __str__(self) -> str:
        """Return string representation of exception."""
        ...


class Exception(Throwable):
    """
    Standard exception class for CODA-OSS.
    
    Inherits from Throwable and provides the same interface.
    This is the primary exception type used throughout CODA-OSS.
    Can be constructed from another Throwable to wrap or rethrow.
    """
    
    @overload
    def __init__(self) -> None:
        """Initialize with empty message."""
        ...
    
    @overload
    def __init__(self, message: str) -> None:
        """Initialize with message."""
        ...
    
    @overload
    def __init__(self, context: Context) -> None:
        """Initialize with context."""
        ...
    
    @overload
    def __init__(self, throwable: Throwable, context: Context) -> None:
        """
        Initialize by wrapping another Throwable with new context.
        
        Args:
            throwable: Exception to wrap
            context: New context to add to trace
        """
        ...
