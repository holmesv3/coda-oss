#!/usr/bin/env python3
"""
Test suite for coda_except module.
"""
import pytest

try:
    from coda import coda_except
except ImportError as e:
    pytest.skip(f"coda_except module not available: {e}", allow_module_level=True)


class TestContext:
    """Test Context class."""
    
    def test_constructor_with_args(self):
        """Test Context constructor with file, line, func."""
        ctx = coda_except.Context("test.cpp", 42, "testFunction")
        assert ctx.getFile() == "test.cpp"
        assert ctx.getLine() == 42
        assert ctx.getFunction() == "testFunction"
    
    def test_constructor_full(self):
        """Test Context constructor with all arguments."""
        ctx = coda_except.Context("test.cpp", 42, "testFunction", 
                                   "2024-07-14", "Error message")
        assert ctx.getFile() == "test.cpp"
        assert ctx.getLine() == 42
        assert ctx.getFunction() == "testFunction"
        assert ctx.getTime() == "2024-07-14"
        assert ctx.getMessage() == "Error message"
    
    def test_members_accessible(self):
        """Test Context public members are accessible."""
        ctx = coda_except.Context("test.cpp", 42, "testFunc")
        ctx.mFile = "modified.cpp"
        ctx.mLine = 100
        ctx.mFunc = "modifiedFunc"
        ctx.mTime = "2024-07-14"
        ctx.mMessage = "Modified message"
        
        assert ctx.mFile == "modified.cpp"
        assert ctx.mLine == 100
        assert ctx.mFunc == "modifiedFunc"
        assert ctx.mTime == "2024-07-14"
        assert ctx.mMessage == "Modified message"
    
    def test_str_representation(self):
        """Test Context string representation."""
        ctx = coda_except.Context("test.cpp", 42, "testFunction")
        str_repr = str(ctx)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0


class TestTrace:
    """Test Trace class."""
    
    def test_default_constructor(self):
        """Test Trace default constructor."""
        trace = coda_except.Trace()
        assert trace is not None
        assert trace.getSize() == 0
    
    def test_push_context(self):
        """Test pushing contexts to trace."""
        trace = coda_except.Trace()
        ctx1 = coda_except.Context("file1.cpp", 10, "func1")
        ctx2 = coda_except.Context("file2.cpp", 20, "func2")
        
        trace.pushContext(ctx1)
        assert trace.getSize() == 1
        
        trace.pushContext(ctx2)
        assert trace.getSize() == 2
    
    def test_str_representation(self):
        """Test Trace string representation."""
        trace = coda_except.Trace()
        trace.pushContext(coda_except.Context("test.cpp", 42, "testFunc"))
        str_repr = str(trace)
        assert isinstance(str_repr, str)


class TestThrowable:
    """Test Throwable class."""
    
    def test_default_constructor(self):
        """Test Throwable default constructor."""
        t = coda_except.Throwable()
        assert t is not None
    
    def test_constructor_with_message(self):
        """Test Throwable constructor with message."""
        t = coda_except.Throwable("Test error message")
        assert t.getMessage() == "Test error message"
    
    def test_constructor_with_context(self):
        """Test Throwable constructor with Context."""
        ctx = coda_except.Context("test.cpp", 42, "testFunc", "", "Error")
        t = coda_except.Throwable(ctx)
        assert t is not None
        assert "Error" in t.getMessage() or t.getTrace().getSize() > 0
    
    def test_get_type(self):
        """Test Throwable getType method."""
        t = coda_except.Throwable("Test")
        assert t.getType() == "Throwable"
    
    def test_to_string(self):
        """Test Throwable toString method."""
        t = coda_except.Throwable("Test error")
        s = t.toString()
        assert isinstance(s, str)
        assert "Test error" in s or "Throwable" in s
    
    def test_str_method(self):
        """Test Throwable __str__ method."""
        t = coda_except.Throwable("Test error")
        s = str(t)
        assert isinstance(s, str)
        assert len(s) > 0
    
    def test_backtrace(self):
        """Test Throwable backtrace method."""
        t = coda_except.Throwable("Test")
        result = t.backtrace()
        assert result is not None
        backtrace = t.getBacktrace()
        assert isinstance(backtrace, list)


class TestException:
    """Test Exception class."""
    
    def test_default_constructor(self):
        """Test Exception default constructor."""
        e = coda_except.Exception()
        assert e is not None
    
    def test_constructor_with_message(self):
        """Test Exception constructor with message."""
        e = coda_except.Exception("Exception message")
        assert e.getMessage() == "Exception message"
    
    def test_constructor_with_context(self):
        """Test Exception constructor with Context."""
        ctx = coda_except.Context("test.cpp", 42, "testFunc", "", "Error")
        e = coda_except.Exception(ctx)
        assert e is not None
    
    def test_inherits_from_throwable(self):
        """Test Exception inherits Throwable methods."""
        e = coda_except.Exception("Test")
        assert hasattr(e, 'getMessage')
        assert hasattr(e, 'getTrace')
        assert hasattr(e, 'toString')
    
    def test_get_type(self):
        """Test Exception getType returns 'Exception'."""
        e = coda_except.Exception("Test")
        assert e.getType() == "Exception"


class TestExceptionHandling:
    """Test exception translator functionality."""
    
    def test_exception_in_python(self):
        """Test creating and using exceptions in Python."""
        e = coda_except.Exception("Python error")
        assert e.getMessage() == "Python error"
        
        # Can be used in Python code
        try:
            msg = e.getMessage()
            assert msg == "Python error"
        except Exception as ex:
            pytest.fail(f"Should not raise exception: {ex}")
