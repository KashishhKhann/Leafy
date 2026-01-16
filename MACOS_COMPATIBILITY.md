# Leafy macOS Compatibility - Complete

## What's Been Done

Leafy is now **fully compatible with macOS**, Windows, and Linux. All platform-specific code has been abstracted and optimized for each OS.

## Key Changes for macOS Support

### 1. **Platform-Specific Utilities** (`platform_utils.py`)
- Automatic platform detection (Windows/macOS/Linux)
- Cross-platform application launching
- Native keyboard shortcuts for each OS
- Screenshot handling for each platform
- System control (shutdown, restart, sleep, logout)
- Trash/recycle bin emptying for all platforms

### 2. **Text-to-Speech Engine**
- **macOS**: Uses native `nsss` (Neural Speech Synthesis System)
- **Windows**: Uses `sapi5` (built-in)
- **Linux**: Uses `espeak` or similar

### 3. **System Commands Handled**
| Action | Windows | macOS | Linux |
|--------|---------|-------|-------|
| Window Switch | Alt+Tab | Cmd+Tab | Alt+Tab |
| Screenshot | pyautogui | screencapture | gnome-screenshot |
| Sleep | shutdown /h | pmset sleepnow | systemctl suspend |
| Shutdown | shutdown /s | osascript | shutdown -h |
| Restart | shutdown /r | osascript | shutdown -r |
| Empty Trash | winshell | rm ~/.Trash/* | rm ~/.local/share/Trash/* |

### 4. **macOS-Specific Features**
- Uses AppleScript (osascript) for system operations
- Native Cocoa integration via Tkinter
- Proper microphone permission handling
- System speech synthesis
- Cmd+Tab application switching

## New Files Created

| File | Purpose |
|------|---------|
| `platform_utils.py` | Cross-platform compatibility layer |
| `MACOS_SETUP.md` | macOS-specific setup guide |
| `setup_macos.sh` | Automated setup script for macOS |
| `check_compatibility.py` | System requirements checker |
| `.gitignore` | Protects sensitive files |

## Getting Started on macOS

### Quickest Method (One Command):
```bash
bash setup_macos.sh
```

### Manual Method:
```bash
# 1. Clone/download the project
cd ~/path/to/Leafy

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
nano .env  # Add your API keys

# 5. Run the app
python Leafy.py
```

## Security Improvements

- DONE: API keys now stored in `.env` (not hardcoded)
- DONE: Input sanitization to prevent injection attacks
- DONE: Sensitive data not logged
- DONE: `.gitignore` prevents committing secrets
- DONE: Proper error handling without exposing details

## Enhanced Features

- DONE: **Real-time GUI Output**: See conversation in the app
- DONE: **Command History**: Track and replay commands
- DONE: **System Monitoring**: Check microphone & internet status
- DONE: **Better Logging**: Detailed logs in `logs/` directory
- DONE: **Persistent Storage**: Notes and history saved locally
- DONE: **Cross-Platform**: Works identically on all major OS

## Testing on macOS

Run the compatibility checker:
```bash
python check_compatibility.py
```

This checks:
- DONE: Python version (3.8+)
- DONE: Required modules
- DONE: File structure
- DONE: Microphone access
- DONE: Directory permissions

## Voice Commands (All Platforms)

```
Greetings: "How are you?", "Tell me a joke"
Time: "What's the time?"
Notes: "Write a note", "Show notes"
Search: "Search for [query]", "Where is [location]"
Media: "Play music", "Open YouTube"
System: "Take a screenshot", "Check CPU"
Control: "Sleep", "Restart", "Shutdown", "Empty trash"
History: "Show history", "Repeat last command"
```

## Troubleshooting for macOS

### Microphone Permission
```bash
# Go to: System Preferences → Security & Privacy → Microphone
# Make sure Python/Terminal is in the allowed list
```

### Audio Issues
```bash
# Test audio setup
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"
```

### API Problems
```bash
# Check logs
tail -f logs/leafy_*.log

# Verify API keys
nano .env  # Make sure keys aren't placeholder text
```

## File Structure

```
Leafy/
├── Leafy.py                  # Main application
├── config.py                 # Configuration
├── logger.py                 # Logging system
├── utils.py                  # Utilities
├── storage.py                # Data storage
├── platform_utils.py        # OS compatibility
├── requirements.txt          # Dependencies
├── .env.example              # Config template
├── INSTALL.md                # Installation guide
├── MACOS_SETUP.md            # macOS guide
├── setup_macos.sh            # Auto setup
├── check_compatibility.py    # System check
├── logs/                     # Activity logs
├── data/
│   ├── notes/                   # Stored notes
│   └── command_history.json     # History
└── README.md                 # Main readme
```

## What Works on All Platforms

DONE: Voice recognition and text-to-speech  
DONE: Wikipedia searches  
DONE: WolframAlpha calculations  
DONE: News retrieval  
DONE: Note taking and storage  
DONE: Command history and replay  
DONE: System monitoring (CPU, battery)  
DONE: Music playback  
DONE: Screenshots  
DONE: Web navigation  
DONE: System control (sleep, restart, etc.)  

## Platform-Specific Behavior

### macOS Features
- Uses native AppleScript for system operations
- Cmd+Tab for window switching (instead of Alt+Tab)
- System speech synthesis (no external voices needed)
- Native microphone integration
- Proper permission handling

### Windows Features
- SAPI5 text-to-speech
- Alt+Tab window switching
- Recycle Bin management
- Native Windows file dialogs

### Linux Features
- D-Bus integration for system control
- PulseAudio support
- Alternative TTS engines (espeak, festival)
- DBus session control

## Performance Optimization

- DONE: Lazy loading of modules
- DONE: Async GUI updates
- DONE: Efficient file I/O with context managers
- DONE: Optimized voice recognition timeout
- DONE: Cached system checks

## Known Limitations

1. **Windows-specific apps**: Can't launch Photoshop, etc. on macOS
2. **System-level operations**: Some require elevated privileges
3. **Internet-dependent**: News and calculations need internet
4. **Microphone quality**: Depends on hardware setup

## You're All Set!

Leafy is now a true cross-platform assistant. Run `python Leafy.py` and enjoy voice-controlled productivity on macOS, Windows, or Linux!

For issues or contributions, check the GitHub repository.

**Happy voice commanding!**
