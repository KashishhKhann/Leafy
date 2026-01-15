"""
Async operations wrapper for Leafy
Runs long-running tasks asynchronously to keep GUI responsive
"""

import threading
import time
from typing import Callable, Optional, Any
from logger import log_info, log_error


class AsyncTask:
    """Represents an async task."""
    
    def __init__(self, task_id: str, func: Callable, args=None, kwargs=None):
        self.task_id = task_id
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.result = None
        self.error = None
        self.is_running = False
        self.is_completed = False
        self.progress = 0
        self.thread = None
    
    def run(self):
        """Run the task."""
        self.is_running = True
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.is_completed = True
            self.progress = 100
            log_info(f"Async task completed: {self.task_id}")
        except Exception as e:
            self.error = str(e)
            log_error("ASYNC", f"Task failed: {self.task_id}", str(e))
        finally:
            self.is_running = False
    
    def start(self):
        """Start the task in a background thread."""
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
    
    def wait(self, timeout: Optional[float] = None) -> Any:
        """Wait for task to complete and return result."""
        if self.thread:
            self.thread.join(timeout)
        return self.result


class AsyncManager:
    """Manage async tasks."""
    
    def __init__(self):
        self.tasks = {}
    
    def create_task(self, task_id: str, func: Callable, 
                   args=None, kwargs=None) -> AsyncTask:
        """Create an async task."""
        task = AsyncTask(task_id, func, args, kwargs)
        self.tasks[task_id] = task
        return task
    
    def run_async(self, task_id: str, func: Callable, 
                 args=None, kwargs=None) -> AsyncTask:
        """Create and start an async task."""
        task = self.create_task(task_id, func, args, kwargs)
        task.start()
        return task
    
    def get_task(self, task_id: str) -> Optional[AsyncTask]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def is_running(self, task_id: str) -> bool:
        """Check if task is running."""
        task = self.get_task(task_id)
        return task.is_running if task else False
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task (note: can only wait for it to finish)."""
        task = self.get_task(task_id)
        if task:
            # Note: Python doesn't have true thread cancellation
            # We can only wait for it to finish
            return True
        return False
    
    def get_result(self, task_id: str) -> Optional[Any]:
        """Get task result (blocks if not ready)."""
        task = self.get_task(task_id)
        if task:
            if not task.is_completed and task.thread:
                task.thread.join()
            return task.result
        return None
    
    def clear_completed(self):
        """Remove completed tasks."""
        self.tasks = {k: v for k, v in self.tasks.items() if not v.is_completed}
    
    def get_stats(self):
        """Get stats on running tasks."""
        running = sum(1 for t in self.tasks.values() if t.is_running)
        completed = sum(1 for t in self.tasks.values() if t.is_completed)
        return {'running': running, 'completed': completed, 'total': len(self.tasks)}


# Global async manager
async_manager = AsyncManager()


# Convenience decorators and functions

def run_async(func: Callable, *args, **kwargs) -> AsyncTask:
    """Run a function asynchronously."""
    task_id = f"{func.__name__}_{time.time()}"
    return async_manager.run_async(task_id, func, args, kwargs)


def run_async_with_callback(func: Callable, callback: Callable, 
                            *args, **kwargs) -> AsyncTask:
    """Run function async and call callback when done."""
    def wrapper():
        result = func(*args, **kwargs)
        callback(result)
        return result
    
    return run_async(wrapper)


class AsyncOperation:
    """Context manager for async operations."""
    
    def __init__(self, task_id: str, func: Callable, args=None, kwargs=None,
                 on_complete: Optional[Callable] = None):
        self.task_id = task_id
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.on_complete = on_complete
        self.task = None
    
    def __enter__(self):
        """Start async operation."""
        if self.on_complete:
            self.task = run_async_with_callback(
                self.func, self.on_complete, *self.args, **self.kwargs
            )
        else:
            self.task = async_manager.run_async(
                self.task_id, self.func, self.args, self.kwargs
            )
        return self.task
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Optionally wait for completion."""
        pass


# Example usage functions

def example_long_task(duration: int = 5):
    """Example long-running task."""
    for i in range(duration):
        time.sleep(1)
        log_info(f"Long task progress: {i+1}/{duration}")
    return f"Completed after {duration} seconds"


if __name__ == "__main__":
    # Test async operations
    print("Testing async operations...")
    
    task = run_async(example_long_task, 3)
    print(f"Task started: {task.task_id}")
    print(f"Running: {task.is_running}")
    
    result = task.wait(timeout=5)
    print(f"Result: {result}")
    print(f"Completed: {task.is_completed}")
