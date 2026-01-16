# macOS Setup Guide for Leafy

## Quick Start (5 minutes)

### 1. Prerequisites Check

```bash
# Check Python version (need 3.8+)
python3 --version

# Check if you have git (optional but recommended)
git --version
```

### 2. Get the Code

```bash
# Option A: Clone from GitHub
git clone https://github.com/KashishhKhann/Leafy.git
cd Leafy

# Option B: Download and extract ZIP file
cd ~/Downloads/Leafy  # or wherever you extracted it
```

### 3. Setup Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) at the start of your terminal prompt
```

### 4. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### 5. Configure API Keys

```bash
# Copy example configuration
cp .env.example .env

# Edit the file with your API keys
nano .env  # or use your favorite editor

# Get free API keys from:
# - WolframAlpha: https://developer.wolframalpha.com/
# - NewsAPI: https://newsapi.org/
```

### 6. Grant Microphone Permission

macOS requires explicit permission for microphone access. When you run Leafy:

1. Launch the app: `python Leafy.py`
2. Click "Start Assistant"
3. macOS will show a permission dialog
4. Click **"Allow"** to grant microphone access
5. Restart the app if needed

**Note**: If you denied permission, you can re-enable it:
- System Preferences → Security & Privacy → Microphone
- Find Python or Terminal in the list and toggle ON

### 7. Run the Application

```bash
# Make sure venv is activated (you see (venv) in prompt)
python Leafy.py
```

## Troubleshooting

### Issue: "Command not found: python3"

**Solution**: Install Python using Homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

### Issue: Microphone not working

**Check 1**: Grant permission
```bash
# System Preferences → Security & Privacy → Microphone
# Make sure Python/Terminal is allowed
```

**Check 2**: Test microphone
```bash
# In Terminal, run:
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"
```

### Issue: "Permission denied" errors

**Solution**: Make sure you're in the Leafy directory with proper permissions:
```bash
cd ~/path/to/Leafy
chmod u+rwx Leafy.py
chmod u+rwx -R logs/
chmod u+rwx -R data/
```

### Issue: "ModuleNotFoundError"

**Solution**: Make sure virtual environment is activated:
```bash
# You should see (venv) in your prompt
source venv/bin/activate

# If that doesn't work, try:
which python  # Should show path ending in /venv/bin/python

# Then try running again:
python Leafy.py
```

### Issue: Speech/Audio not working

**Solution 1**: Reinstall pyttsx3
```bash
pip uninstall pyttsx3
pip install pyttsx3
```

**Solution 2**: Check system audio settings
```
System Preferences → Sound → Output
Make sure your speaker/output is enabled
```

### Issue: "API Error" or "No results"

**Solutions**:
1. Check API keys in `.env` file (make sure they're correct)
2. Verify internet connection: `ping google.com`
3. Check API rate limits (they have daily limits for free tier)
4. Check logs: `tail -f logs/leafy_$(date +%Y%m%d).log`

## Advanced Setup

### Using iTerm2 (Better Terminal)

```bash
# Install iTerm2
brew install iterm2

# Then follow the same steps as above
```

### Running in Background

```bash
# Run as background process
nohup python Leafy.py > leafy.log 2>&1 &

# Check if it's running
ps aux | grep Leafy

# Kill if needed
pkill -f "python Leafy.py"
```

### Creating an Alias for Easy Launch

```bash
# Add to ~/.zshrc (macOS Catalina and newer) or ~/.bash_profile
echo 'alias leafy="cd ~/path/to/Leafy && source venv/bin/activate && python Leafy.py"' >> ~/.zshrc

# Then you can just type:
leafy
```

### Setting Up as macOS App

1. Create a shell script at `~/Applications/Leafy.sh`:
```bash
#!/bin/bash
cd ~/path/to/Leafy
source venv/bin/activate
python Leafy.py
```

2. Make it executable:
```bash
chmod +x ~/Applications/Leafy.sh
```

3. Create an Automator app or use a launcher like `Alfred` or `Spotlight`

## Performance Tips

- Close other applications to free up CPU
- Use headphones for better microphone quality
- Ensure stable internet connection for API calls
- Check logs regularly: `tail -f logs/leafy_*.log`

## Getting Help

1. Check `logs/` directory for detailed error messages
2. Read the README.md for feature documentation
3. Review the troubleshooting section above
4. Check console output for error messages

## Enjoy!

Your Leafy assistant is now ready! Try saying:
- "Hey, how are you?"
- "Tell me a joke"
- "What's the time?"
- "Search for Python documentation"

Happy voice commanding!
