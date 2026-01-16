#!/usr/bin/env python3
"""Test script for advanced features: Database, Caching, Async, and Settings."""

import sys
import os
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_database():
    """Test database module."""
    print("\n" + "="*60)
    print("Testing Database Module (db.py)")
    print("="*60)
    
    try:
        from db import db
        
        print("DONE: Testing save_note()...")
        db.save_note("Test Note", "This is a test note", "test,database")
        
        print("DONE: Testing search_notes()...")
        notes = db.search_notes("test")
        assert len(notes) > 0, "No notes found"
        print(f"  Found {len(notes)} note(s)")
        
        print("DONE: Testing set_setting() and get_setting()...")
        db.set_setting('test_setting', 'test_value', 'str')
        value = db.get_setting('test_setting', 'default')
        assert value == 'test_value', f"Setting not saved properly: {value}"
        print(f"  Setting retrieved: {value}")
        
        print("DONE: Testing add_command()...")
        db.add_command('test_command', 'test query')
        
        print("DONE: Testing cache_response()...")
        db.cache_response('test_query_hash', 'wikipedia', 'Test response content', 3600)
        cached = db.get_cached_response('test_query_hash', 'wikipedia')
        assert cached is not None, "Cache not working"
        print(f"  Cached response retrieved: {cached[:50]}...")
        
        print("DONE: Testing get_stats()...")
        stats = db.get_stats()
        print(f"  Database stats: {stats}")
        
        print("DONE: Testing backup()...")
        backup_path = db.backup()
        assert os.path.exists(backup_path), "Backup file not created"
        print(f"  Backup created at: {backup_path}")
        
        print("\nDatabase tests PASSED")
        return True
        
    except Exception as e:
        print(f"\nDatabase test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_caching():
    """Test caching module."""
    print("\n" + "="*60)
    print("Testing Caching Module (cache.py)")
    print("="*60)
    
    try:
        from cache import ResponseCache, get_cached_or_fetch
        
        print("DONE: Testing query hashing...")
        query = "what is python"
        cache = ResponseCache()
        
        print("DONE: Testing cache miss...")
        result = cache.get_cached(query, "wikipedia")
        print(f"  Cache miss (expected): {result is None}")
        
        print("DONE: Testing cache_result()...")
        response = "Python is a programming language"
        cache.cache_result(query, "wikipedia", response, 3600)
        
        print("DONE: Testing cache hit...")
        cached = cache.get_cached(query, "wikipedia")
        assert cached == response, "Cache retrieval failed"
        print(f"  Cache hit successful: {cached}")
        
        print("DONE: Testing get_cached_or_fetch()...")
        
        def fetch_func():
            print("    (Fetch function called - cache miss)")
            return "Fetched content"
        
        result1 = get_cached_or_fetch(query, "wikipedia", fetch_func, 3600)
        result2 = get_cached_or_fetch(query, "wikipedia", fetch_func, 3600)
        print(f"  First call (from cache): {result1}")
        print(f"  Second call (from cache): {result2}")
        
        print("DONE: Testing TTL constants...")
        print(f"  TTL_WIKIPEDIA: {ResponseCache.TTL_WIKIPEDIA} seconds ({ResponseCache.TTL_WIKIPEDIA/86400} days)")
        print(f"  TTL_CALCULATION: {ResponseCache.TTL_CALCULATION} seconds ({ResponseCache.TTL_CALCULATION/86400} days)")
        print(f"  TTL_NEWS: {ResponseCache.TTL_NEWS} seconds ({ResponseCache.TTL_NEWS/86400} days)")
        
        print("\nCaching tests PASSED")
        return True
        
    except Exception as e:
        print(f"\nCaching test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_async_operations():
    """Test async operations module."""
    print("\n" + "="*60)
    print("Testing Async Operations Module (async_ops.py)")
    print("="*60)
    
    try:
        from async_ops import AsyncTask, AsyncManager, run_async, AsyncOperation
        
        print("DONE: Testing AsyncTask class...")
        
        def sample_task():
            time.sleep(0.5)
            return "Task completed"
        
        task = AsyncTask("test", sample_task)
        task.start()
        print(f"  Task started, is_running: {task.is_running}")
        result = task.wait(timeout=5)
        print(f"  Task result: {result}")
        assert result == "Task completed", "Task result incorrect"
        
        print("DONE: Testing AsyncManager...")
        manager = AsyncManager()
        
        def long_task(duration):
            time.sleep(duration)
            return f"Completed in {duration}s"
        
        task_id = "test_task"
        manager.run_async(task_id, long_task, (1,))
        print(f"  Task ID: {task_id}")
        assert manager.is_running(task_id), "Task should be running"
        result = manager.get_result(task_id)
        print(f"  Result: {result}")
        
        print("DONE: Testing run_async() helper...")
        
        def quick_task(x, y):
            return x + y
        
        task = run_async(quick_task, 5, 3)
        result = task.wait()
        print(f"  Async result (5 + 3): {result}")
        assert result == 8, "Calculation incorrect"
        
        print("DONE: Testing AsyncOperation context manager...")
        
        def context_task():
            time.sleep(0.2)
            return "Context task done"
        
        with AsyncOperation("ctx_task", context_task) as task:
            print(f"  Task running in context: {task.is_running}")
            result = task.wait()
        
        print(f"  Result after context: {result}")
        
        print("\nAsync operations tests PASSED")
        return True
        
    except Exception as e:
        print(f"\nAsync operations test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_settings_gui():
    """Test settings GUI module."""
    print("\n" + "="*60)
    print("Testing Settings GUI Module (settings_gui.py)")
    print("="*60)
    
    try:
        from settings_gui import SettingsWindow
        print("DONE: SettingsWindow imported successfully")
        
        required_methods = [
            'apply_settings', 
            'load_settings', 
            'reset_defaults',
            'clear_cache',
            'backup_database',
            'restore_database'
        ]
        
        for method in required_methods:
            assert hasattr(SettingsWindow, method), f"Missing method: {method}"
            print(f"DONE: Method found: {method}")
        
        print("\nSettings GUI tests PASSED (GUI requires Tkinter display)")
        return True
        
    except Exception as e:
        print(f"\nSettings GUI test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("ADVANCED FEATURES TEST SUITE")
    print("="*60)
    
    results = {
        'Database': test_database(),
        'Caching': test_caching(),
        'Async Operations': test_async_operations(),
        'Settings GUI': test_settings_gui(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll advanced features are working correctly!")
        return 0
    else:
        print(f"\n{total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
