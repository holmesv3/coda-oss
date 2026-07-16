"""
Type stubs for coda_mt module.

This module provides multithreading support for parallel processing.
It includes thread management, work distribution, and abstractions for
running tasks across multiple CPU cores.

Classes:
    Runnable: Abstract base class for thread worker tasks
    ThreadPlanner: Work distribution calculator for parallel processing
    ThreadGroup: Thread pool manager for executing parallel tasks

Note:
    Operations in this module release the Python GIL where appropriate,
    allowing true parallel execution of C++ code.
"""

from typing import Tuple

class Runnable:
    """
    Abstract base class for thread worker tasks.
    
    Subclass this in Python to define work that will be executed by threads.
    The run() method will be called in a separate thread context.
    
    Example:
        class MyTask(Runnable):
            def run(self):
                # Do work here
                pass
    """
    
    def run(self) -> None:
        """
        Execute the task.
        
        This method must be overridden in subclasses to define the work
        to be performed by the thread. Called automatically by ThreadGroup.
        """
        ...


class ThreadPlanner:
    """
    Work distribution calculator for parallel processing.
    
    Divides a fixed amount of work (numElements) across a specified number
    of threads, calculating optimal start indices and workload per thread.
    Handles cases where work cannot be evenly divided.
    """
    
    def __init__(self, numElements: int, numThreads: int) -> None:
        """
        Initialize planner for distributing work across threads.
        
        Args:
            numElements: Total number of work items to distribute
            numThreads: Desired number of threads to use
            
        Note:
            Actual number of threads used may be less than requested if
            numElements < numThreads.
        """
        ...
    
    def getNumElementsPerThread(self) -> int:
        """
        Get typical number of elements each thread will process.
        
        Returns:
            Base number of elements per thread (some threads may get +1)
        """
        ...
    
    def getThreadInfo(self, threadNum: int) -> Tuple[bool, int, int]:
        """
        Get work assignment for a specific thread.
        
        Args:
            threadNum: Thread index (0-based)
            
        Returns:
            Tuple of (isValid, startElement, numElementsThisThread) where:
                - isValid: True if this thread has work to do
                - startElement: Index of first element for this thread
                - numElementsThisThread: Number of elements for this thread
                
        Example:
            planner = ThreadPlanner(100, 4)
            valid, start, count = planner.getThreadInfo(0)
            if valid:
                # Process elements from start to start+count
                pass
        """
        ...
    
    def getNumThreadsThatWillBeUsed(self) -> int:
        """
        Get actual number of threads that will be used.
        
        Returns:
            Number of threads with work assigned (may be less than requested)
        """
        ...


class ThreadGroup:
    """
    Thread pool manager for executing parallel tasks.
    
    Manages creation and lifecycle of worker threads. Threads are created
    with Runnable tasks and can be joined to wait for completion.
    Optionally supports CPU affinity (thread pinning).
    """
    
    def __init__(self, pinToCPU: bool = False) -> None:
        """
        Initialize thread group.
        
        Args:
            pinToCPU: If True, pin threads to specific CPU cores for better
                     cache locality (platform-dependent behavior)
        """
        ...
    
    def createThread(self, runnable: Runnable) -> None:
        """
        Create and start a new thread with the given task.
        
        The thread takes ownership of the Runnable and will execute its
        run() method. The thread starts immediately upon creation.
        
        Args:
            runnable: Task to execute in new thread (ownership transferred)
            
        Note:
            The Runnable object should not be used after passing to this method
            as ownership is transferred to the thread.
        """
        ...
    
    def joinAll(self) -> None:
        """
        Wait for all threads in the group to complete.
        
        Blocks until all threads have finished executing their run() methods.
        After this call returns, all threads have terminated.
        """
        ...
    
    def isPinToCPUEnabled(self) -> bool:
        """
        Check if CPU pinning is enabled.
        
        Returns:
            True if threads are pinned to specific CPU cores
        """
        ...
