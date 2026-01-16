import os
import sys
import socket
import subprocess
from pathlib import Path
from logger import log_error, log_info


def check_microphone():
    """Check if microphone is available."""
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            log_info("Microphone detected and working")
            return True
    except Exception as e:
        log_error("MICROPHONE", "Microphone not available", str(e))
        return False


def check_internet():
    """Check if internet connection is available."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        log_info("Internet connection available")
        return True
    except (OSError, socket.timeout):
        log_error("NETWORK", "No internet connection", "")
        return False


def check_api_keys():
    """Verify API keys are configured."""
    from dotenv import load_dotenv
    
    # Load .env file
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        log_error("CONFIG", ".env file not found", f"Create from .env.example at {env_file}")
        return False
    
    load_dotenv(env_file)
    
    wolfram_key = os.getenv('WOLFRAM_API_KEY')
    news_key = os.getenv('NEWS_API_KEY')
    
    missing_keys = []
    
    if not wolfram_key or wolfram_key == 'your_wolfram_api_key_here':
        missing_keys.append('WOLFRAM_API_KEY')
    
    if not news_key or news_key == 'your_news_api_key_here':
        missing_keys.append('NEWS_API_KEY')
    
    if missing_keys:
        log_error("CONFIG", f"Missing API keys: {', '.join(missing_keys)}", 
                 "Update .env file with your actual API keys")
        return False
    
    log_info("All API keys configured")
    return True


def sanitize_input(user_input):
    """Sanitize user input to prevent injection attacks."""
    if not isinstance(user_input, str):
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['$', '`', '|', ';', '&', '>', '<', '\n', '\r']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    
    return user_input.strip()


def validate_query(query):
    """Validate if query is meaningful."""
    if not query or len(query) < 2:
        return False
    
    # Filter out common non-commands
    noise_words = ['the', 'a', 'an', 'and', 'or', 'is', 'are']
    if query.lower() in noise_words:
        return False
    
    return True


def check_system_requirements():
    """Check all system requirements before starting."""
    log_info("Checking system requirements...")
    
    checks = {
        'Microphone': check_microphone(),
        'Internet': check_internet(),
        'API Keys': check_api_keys()
    }
    
    failed = [name for name, result in checks.items() if not result]
    
    if failed:
        log_error("STARTUP", f"Failed checks: {', '.join(failed)}", "")
        return False
    
    log_info("All system checks passed")
    return True


def get_system_info():
    """Get system information for logging."""
    return {
        'platform': sys.platform,
        'python_version': sys.version,
        'machine': os.uname().machine if hasattr(os, 'uname') else 'unknown'
    }
