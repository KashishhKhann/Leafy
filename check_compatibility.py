#!/usr/bin/env python3
"""
System compatibility checker for Leafy
Tests all required components before running the app
"""

import sys
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("FAILED: Python 3.8+ required")
        print(f"   Current: Python {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"DONE: Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_module(module_name, import_name=None):
    """Check if a Python module is installed."""
    import_name = import_name or module_name
    try:
        importlib.import_module(import_name)
        print(f"DONE: {module_name}")
        return True
    except ImportError:
        print(f"FAILED: {module_name} - Install with: pip install {module_name}")
        return False


def check_platform():
    """Display platform information."""
    platform_name = {
        'win32': 'Windows',
        'darwin': 'macOS',
        'linux': 'Linux',
    }.get(sys.platform, 'Unknown')
    
    print(f"DONE: Platform: {platform_name}")
    return True


def check_files():
    """Check if required files exist."""
    required_files = [
        'Leafy.py',
        'config.py',
        'logger.py',
        'utils.py',
        'storage.py',
        'platform_utils.py',
        '.env.example',
        'requirements.txt',
    ]
    
    base_path = Path(__file__).parent
    all_exist = True
    
    for filename in required_files:
        file_path = base_path / filename
        if file_path.exists():
            print(f"DONE: {filename}")
        else:
            print(f"FAILED: {filename} - Missing!")
            all_exist = False
    
    return all_exist


def check_env():
    """Check if .env file exists."""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print("DONE: .env file configured")
        return True
    else:
        print("WARN: .env file not found")
        print("   Run: cp .env.example .env")
        return False


def check_directories():
    """Check if required directories can be created."""
    base_path = Path(__file__).parent
    dirs = ['logs', 'data', 'data/notes']
    
    all_ok = True
    for dirname in dirs:
        dir_path = base_path / dirname
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"DONE: {dirname}/")
        except Exception as e:
            print(f"FAILED: {dirname}/ - Error: {e}")
            all_ok = False
    
    return all_ok


def check_microphone():
    """Check if microphone is accessible."""
    try:
        import speech_recognition as sr
        with sr.Microphone() as source:
            print("DONE: Microphone detected")
            return True
    except Exception as e:
        print(f"WARN: Microphone not accessible: {e}")
        return False


def main():
    print("Leafy Compatibility Check")
    print("=" * 40)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Platform", check_platform),
        ("Required Files", check_files),
        ("Configuration", check_env),
        ("Directories", check_directories),
    ]
    
    print("Core Requirements:")
    print("-" * 40)
    all_passed = True
    for name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"FAILED: {name}: {e}")
            all_passed = False
        print()
    
    print("Python Dependencies:")
    print("-" * 40)
    modules = [
        ('pyttsx3', 'pyttsx3'),
        ('speech_recognition', 'speech_recognition'),
        ('playsound', 'playsound'),
        ('wikipedia', 'wikipedia'),
        ('PIL', 'PIL'),
        ('psutil', 'psutil'),
        ('pyjokes', 'pyjokes'),
        ('wolframalpha', 'wolframalpha'),
    ]
    
    for display_name, import_name in modules:
        check_module(display_name, import_name)
    print()
    
    print("System Features:")
    print("-" * 40)
    check_microphone()
    print()
    
    if all_passed:
        print("=" * 40)
        print("DONE: All checks passed!")
        print()
        print("You're ready to run Leafy:")
        print("  python Leafy.py")
    else:
        print("=" * 40)
        print("WARN: Some checks failed.")
        print("Please fix the issues above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
