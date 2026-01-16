"""
Platform-specific utilities for Windows, macOS, and Linux compatibility.
"""

import os
import sys
import subprocess
from logger import log_info, log_error


def get_platform():
    """Get current platform identifier."""
    if sys.platform == 'win32':
        return 'windows'
    elif sys.platform == 'darwin':
        return 'macos'
    elif sys.platform.startswith('linux'):
        return 'linux'
    return 'unknown'


def open_application(app_name):
    """Open an application in a cross-platform way."""
    platform = get_platform()
    
    try:
        if platform == 'macos':
            subprocess.Popen(['open', '-a', app_name])
        elif platform == 'windows':
            subprocess.Popen(['start', app_name], shell=True)
        elif platform == 'linux':
            subprocess.Popen([app_name])
        log_info(f"Opened application: {app_name}")
    except Exception as e:
        log_error("APP_LAUNCH", f"Failed to open {app_name}", str(e))


def open_url(url):
    """Open URL in default browser."""
    try:
        if get_platform() == 'macos':
            subprocess.Popen(['open', url])
        elif get_platform() == 'windows':
            subprocess.Popen(['start', url], shell=True)
        elif get_platform() == 'linux':
            subprocess.Popen(['xdg-open', url])
        log_info(f"Opened URL: {url}")
    except Exception as e:
        log_error("URL_OPEN", f"Failed to open {url}", str(e))


def switch_window():
    """Switch between windows using keyboard shortcuts."""
    platform = get_platform()
    
    try:
        if platform == 'macos':
            subprocess.call(['osascript', '-e', 
                           'tell application "System Events" to key code 48 using command down'])
        elif platform == 'windows':
            import pyautogui
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')
        elif platform == 'linux':
            import pyautogui
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')
        log_info("Switched window")
    except Exception as e:
        log_error("WINDOW_SWITCH", "Failed to switch window", str(e))


def take_screenshot(filename):
    """Take a screenshot in a cross-platform way."""
    platform = get_platform()
    
    try:
        if platform == 'macos':
            subprocess.call(['screencapture', f'{filename}.png'])
        elif platform == 'windows':
            import pyautogui
            img = pyautogui.screenshot()
            img.save(f'{filename}.png')
        elif platform == 'linux':
            subprocess.call(['gnome-screenshot', '-f', f'{filename}.png'])
        log_info(f"Screenshot saved: {filename}.png")
    except Exception as e:
        log_error("SCREENSHOT", "Failed to take screenshot", str(e))


def system_shutdown(delay=10):
    """Shutdown system."""
    platform = get_platform()
    
    try:
        if platform == 'windows':
            subprocess.call(['shutdown', '/s', '/t', str(delay)])
        elif platform == 'macos':
            subprocess.call(['osascript', '-e', 
                           f'tell application "System Events" to shut down with state saved preference yes'])
        elif platform == 'linux':
            subprocess.call(['shutdown', '-h', str(delay)])
        log_info("System shutdown initiated")
    except Exception as e:
        log_error("SHUTDOWN", "Failed to shutdown system", str(e))


def system_restart(delay=10):
    """Restart system."""
    platform = get_platform()
    
    try:
        if platform == 'windows':
            subprocess.call(['shutdown', '/r', '/t', str(delay)])
        elif platform == 'macos':
            subprocess.call(['osascript', '-e', 
                           f'tell application "System Events" to restart with state saved preference yes'])
        elif platform == 'linux':
            subprocess.call(['shutdown', '-r', str(delay)])
        log_info("System restart initiated")
    except Exception as e:
        log_error("RESTART", "Failed to restart system", str(e))


def system_sleep():
    """Put system to sleep."""
    platform = get_platform()
    
    try:
        if platform == 'windows':
            subprocess.call(['shutdown', '/h'])
        elif platform == 'macos':
            subprocess.call(['pmset', 'sleepnow'])
        elif platform == 'linux':
            subprocess.call(['systemctl', 'suspend'])
        log_info("System sleep initiated")
    except Exception as e:
        log_error("SLEEP", "Failed to sleep system", str(e))


def system_logout():
    """Logout from system."""
    platform = get_platform()
    
    try:
        if platform == 'windows':
            subprocess.call(['shutdown', '/l'])
        elif platform == 'macos':
            subprocess.call(['osascript', '-e', 
                           'tell application "System Events" to log out'])
        elif platform == 'linux':
            subprocess.call(['loginctl', 'terminate-session', 'self'])
        log_info("System logout initiated")
    except Exception as e:
        log_error("LOGOUT", "Failed to logout", str(e))


def empty_trash():
    """Empty trash/recycle bin."""
    platform = get_platform()
    
    try:
        if platform == 'windows':
            import winshell
            winshell.recycle_bin().empty(confirm=True, show_progress=False, sound=True)
        elif platform == 'macos':
            subprocess.call(['rm', '-rf', os.path.expanduser('~/.Trash/*')])
        elif platform == 'linux':
            subprocess.call(['rm', '-rf', os.path.expanduser('~/.local/share/Trash/*')])
        log_info("Trash emptied")
    except Exception as e:
        log_error("EMPTY_TRASH", "Failed to empty trash", str(e))


def get_application_path(app_name):
    """Get the path to an application."""
    platform = get_platform()
    app_name_lower = app_name.lower()
    
    paths = {
        'macos': {
            'chrome': '/Applications/Google Chrome.app',
            'safari': '/Applications/Safari.app',
            'firefox': '/Applications/Firefox.app',
            'vscode': '/Applications/Visual Studio Code.app',
            'photoshop': '/Applications/Adobe Photoshop 2021.app',
            'word': '/Applications/Microsoft Word.app',
            'excel': '/Applications/Microsoft Excel.app',
        },
        'windows': {
            'chrome': 'chrome',
            'firefox': 'firefox',
            'vscode': 'code',
            'photoshop': 'Photoshop',
        },
        'linux': {
            'chrome': 'google-chrome',
            'firefox': 'firefox',
            'vscode': 'code',
        }
    }
    
    return paths.get(platform, {}).get(app_name_lower, app_name)


def focus_window(app_name):
    """Bring application window to focus."""
    platform = get_platform()
    
    try:
        if platform == 'macos':
            script = f'tell application "{app_name}" to activate'
            subprocess.call(['osascript', '-e', script])
        elif platform == 'windows':
            try:
                subprocess.call(['wmctrl', '-a', app_name])
            except:
                pass
        log_info(f"Focused window: {app_name}")
    except Exception as e:
        log_error("FOCUS_WINDOW", f"Failed to focus {app_name}", str(e))
