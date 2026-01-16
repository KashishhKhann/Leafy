import json
import os
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path(__file__).parent / 'data' / 'command_history.json'

# Create data directory if it doesn't exist
HISTORY_FILE.parent.mkdir(exist_ok=True)


class CommandHistory:
    """Manage command history with search and replay capabilities."""
    
    def __init__(self, max_size=500):
        self.max_size = max_size
        self.history = self._load_history()
    
    def _load_history(self):
        """Load history from file."""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                return []
        return []
    
    def _save_history(self):
        """Save history to file."""
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history[-self.max_size:], f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add(self, command, status="executed", duration=0):
        """Add command to history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'status': status,
            'duration': duration
        }
        self.history.append(entry)
        self._save_history()
    
    def search(self, keyword):
        """Search history by keyword."""
        return [h for h in self.history if keyword.lower() in h['command'].lower()]
    
    def get_recent(self, count=10):
        """Get recent commands."""
        return self.history[-count:]
    
    def get_most_used(self, count=5):
        """Get most frequently used commands."""
        from collections import Counter
        commands = [h['command'] for h in self.history]
        most_common = Counter(commands).most_common(count)
        return [{'command': cmd, 'count': count} for cmd, count in most_common]
    
    def clear(self):
        """Clear all history."""
        self.history = []
        self._save_history()


class Notes:
    """Manage notes with persistent storage."""
    
    NOTES_DIR = Path(__file__).parent / 'data' / 'notes'
    
    def __init__(self):
        self.NOTES_DIR.mkdir(exist_ok=True)
    
    def save_note(self, title, content, add_timestamp=False):
        """Save a note with timestamp."""
        if add_timestamp:
            content = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {content}"
        
        # Sanitize filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_title:
            safe_title = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        file_path = self.NOTES_DIR / f"{safe_title}.txt"
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving note: {e}")
            return False
    
    def get_note(self, title):
        """Retrieve a note."""
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        file_path = self.NOTES_DIR / f"{safe_title}.txt"
        
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading note: {e}")
        return None
    
    def list_notes(self):
        """List all available notes."""
        try:
            return [f.stem for f in self.NOTES_DIR.glob('*.txt')]
        except Exception as e:
            print(f"Error listing notes: {e}")
            return []
    
    def delete_note(self, title):
        """Delete a note."""
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        file_path = self.NOTES_DIR / f"{safe_title}.txt"
        
        try:
            if file_path.exists():
                file_path.unlink()
                return True
        except Exception as e:
            print(f"Error deleting note: {e}")
        return False
