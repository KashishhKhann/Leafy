"""
SQLite Database module for Leafy
Handles persistent storage of notes, history, settings, and cache
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from logger import log_info, log_error

DB_PATH = Path(__file__).parent / 'data' / 'leafy.db'


class Database:
    """SQLite database manager for Leafy."""
    
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.db_path = DB_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Notes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tags TEXT
                )
            ''')
            
            # Command history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    status TEXT DEFAULT 'executed',
                    duration REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    result TEXT
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    type TEXT DEFAULT 'string',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Response cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS response_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_hash TEXT UNIQUE NOT NULL,
                    query_type TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ttl_seconds INTEGER DEFAULT 86400
                )
            ''')
            
            # Create indexes for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_notes_title ON notes(title)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_command_history_timestamp ON command_history(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cache_query_hash ON response_cache(query_hash)')
            
            conn.commit()
            log_info("Database initialized")
        except Exception as e:
            log_error("DATABASE", "Failed to initialize database", str(e))
        finally:
            conn.close()
    
    # ============ NOTES OPERATIONS ============
    
    def save_note(self, title: str, content: str, tags: str = "") -> bool:
        """Save or update a note."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO notes (title, content, tags, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (title, content, tags))
            
            conn.commit()
            log_info(f"Note saved: {title}")
            return True
        except Exception as e:
            log_error("DATABASE", f"Failed to save note: {title}", str(e))
            return False
        finally:
            conn.close()
    
    def get_note(self, title: str) -> Optional[Dict]:
        """Retrieve a note by title."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM notes WHERE title = ?', (title,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            log_error("DATABASE", f"Failed to get note: {title}", str(e))
            return None
        finally:
            conn.close()
    
    def search_notes(self, keyword: str) -> List[Dict]:
        """Search notes by keyword."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM notes 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_at DESC
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            log_error("DATABASE", f"Failed to search notes: {keyword}", str(e))
            return []
        finally:
            conn.close()
    
    def delete_note(self, title: str) -> bool:
        """Delete a note."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM notes WHERE title = ?', (title,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            log_error("DATABASE", f"Failed to delete note: {title}", str(e))
            return False
        finally:
            conn.close()
    
    def list_notes(self, limit: int = 50) -> List[Dict]:
        """List all notes."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, title, created_at, updated_at 
                FROM notes 
                ORDER BY updated_at DESC 
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            log_error("DATABASE", "Failed to list notes", str(e))
            return []
        finally:
            conn.close()
    
    # ============ COMMAND HISTORY OPERATIONS ============
    
    def add_command(self, command: str, status: str = "executed", 
                   duration: float = 0, result: str = "") -> bool:
        """Add command to history."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO command_history (command, status, duration, result)
                VALUES (?, ?, ?, ?)
            ''', (command, status, duration, result))
            
            conn.commit()
            return True
        except Exception as e:
            log_error("DATABASE", f"Failed to add command: {command}", str(e))
            return False
        finally:
            conn.close()
    
    def search_commands(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Search command history."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM command_history 
                WHERE command LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (f'%{keyword}%', limit))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            log_error("DATABASE", f"Failed to search commands: {keyword}", str(e))
            return []
        finally:
            conn.close()
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        """Get recent command history."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM command_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            log_error("DATABASE", "Failed to get command history", str(e))
            return []
        finally:
            conn.close()
    
    def clear_old_history(self, days: int = 30) -> int:
        """Delete command history older than specified days."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM command_history 
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            log_error("DATABASE", f"Failed to clear old history", str(e))
            return 0
        finally:
            conn.close()
    
    # ============ SETTINGS OPERATIONS ============
    
    def set_setting(self, key: str, value: Any, value_type: str = "string") -> bool:
        """Set a configuration setting."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Convert value to string if needed
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            else:
                value = str(value)
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, type, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (key, value, value_type))
            
            conn.commit()
            return True
        except Exception as e:
            log_error("DATABASE", f"Failed to set setting: {key}", str(e))
            return False
        finally:
            conn.close()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT value, type FROM settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            
            if not row:
                return default
            
            value, value_type = row[0], row[1]
            
            # Convert based on type
            if value_type == "json":
                return json.loads(value)
            elif value_type == "int":
                return int(value)
            elif value_type == "float":
                return float(value)
            elif value_type == "bool":
                return value.lower() in ('true', '1', 'yes')
            else:
                return value
        except Exception as e:
            log_error("DATABASE", f"Failed to get setting: {key}", str(e))
            return default
        finally:
            conn.close()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT key, value, type FROM settings')
            settings = {}
            
            for row in cursor.fetchall():
                key, value, value_type = row[0], row[1], row[2]
                
                # Convert based on type
                if value_type == "json":
                    settings[key] = json.loads(value)
                elif value_type == "int":
                    settings[key] = int(value)
                elif value_type == "float":
                    settings[key] = float(value)
                elif value_type == "bool":
                    settings[key] = value.lower() in ('true', '1', 'yes')
                else:
                    settings[key] = value
            
            return settings
        except Exception as e:
            log_error("DATABASE", "Failed to get all settings", str(e))
            return {}
        finally:
            conn.close()
    
    # ============ CACHE OPERATIONS ============
    
    def cache_response(self, query_hash: str, query_type: str, 
                      response: str, ttl_seconds: int = 86400) -> bool:
        """Cache an API response."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO response_cache 
                (query_hash, query_type, response, ttl_seconds, created_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (query_hash, query_type, response, ttl_seconds))
            
            conn.commit()
            return True
        except Exception as e:
            log_error("DATABASE", f"Failed to cache response: {query_hash}", str(e))
            return False
        finally:
            conn.close()
    
    def get_cached_response(self, query_hash: str) -> Optional[str]:
        """Get cached response if not expired."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT response FROM response_cache 
                WHERE query_hash = ? 
                AND datetime(created_at, '+' || ttl_seconds || ' seconds') > datetime('now')
            ''', (query_hash,))
            
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            log_error("DATABASE", f"Failed to get cached response: {query_hash}", str(e))
            return None
        finally:
            conn.close()
    
    def clear_expired_cache(self) -> int:
        """Delete expired cache entries."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM response_cache 
                WHERE datetime(created_at, '+' || ttl_seconds || ' seconds') <= datetime('now')
            ''')
            
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            log_error("DATABASE", "Failed to clear expired cache", str(e))
            return 0
        finally:
            conn.close()
    
    def clear_all_cache(self) -> int:
        """Clear all cache."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM response_cache')
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            log_error("DATABASE", "Failed to clear all cache", str(e))
            return 0
        finally:
            conn.close()
    
    # ============ BACKUP/RESTORE ============
    
    def backup(self, backup_path: Optional[str] = None) -> bool:
        """Backup database to file."""
        try:
            if not backup_path:
                backup_path = self.db_path.parent / f'leafy_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            
            conn = self.get_connection()
            backup_conn = sqlite3.connect(str(backup_path))
            
            with backup_conn:
                conn.backup(backup_conn)
            
            conn.close()
            backup_conn.close()
            log_info(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            log_error("DATABASE", "Failed to backup database", str(e))
            return False
    
    def restore(self, backup_path: str) -> bool:
        """Restore database from backup."""
        try:
            backup_path = Path(backup_path)
            if not backup_path.exists():
                log_error("DATABASE", "Backup file not found", str(backup_path))
                return False
            
            backup_conn = sqlite3.connect(str(backup_path))
            conn = self.get_connection()
            
            with conn:
                backup_conn.backup(conn)
            
            backup_conn.close()
            conn.close()
            log_info(f"Database restored from: {backup_path}")
            return True
        except Exception as e:
            log_error("DATABASE", "Failed to restore database", str(e))
            return False
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            cursor.execute('SELECT COUNT(*) FROM notes')
            stats['notes'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['commands'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM response_cache')
            stats['cache_entries'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM settings')
            stats['settings'] = cursor.fetchone()[0]
            
            return stats
        except Exception as e:
            log_error("DATABASE", "Failed to get database stats", str(e))
            return {}
        finally:
            conn.close()


# Global database instance
db = Database()
