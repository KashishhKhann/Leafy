"""
Settings Panel GUI for Leafy
Allows users to customize voice, theme, language, and other preferences
"""

from tkinter import *
from tkinter import ttk, messagebox
from db import db
from logger import log_info


class SettingsWindow:
    """Settings panel window."""
    
    def __init__(self, parent, on_apply=None):
        self.parent = parent
        self.on_apply = on_apply
        self.settings = db.get_all_settings()
        
        self.window = Toplevel(parent)
        self.window.title("Leafy Settings")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_widgets()
        self.load_settings()
        
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create settings widgets."""
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.create_audio_tab(notebook)
        self.create_appearance_tab(notebook)
        self.create_system_tab(notebook)
        self.create_advanced_tab(notebook)
        
        button_frame = Frame(self.window)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        apply_btn = Button(button_frame, text="Apply", command=self.apply_settings,
                          bg="#4CAF50", fg="white", padx=20)
        apply_btn.pack(side=LEFT, padx=5)
        
        reset_btn = Button(button_frame, text="Reset to Defaults", 
                          command=self.reset_defaults, bg="#FF9800", fg="white", padx=20)
        reset_btn.pack(side=LEFT, padx=5)
        
        close_btn = Button(button_frame, text="Close", command=self.window.destroy,
                          bg="#757575", fg="white", padx=20)
        close_btn.pack(side=RIGHT, padx=5)
    
    def create_audio_tab(self, notebook):
        """Create audio settings tab."""
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Audio")
        
        ttk.Label(frame, text="Speech Rate:").grid(row=0, column=0, sticky=W, pady=10)
        self.speech_rate_var = IntVar(value=160)
        speech_rate_scale = ttk.Scale(frame, from_=50, to=300, orient=HORIZONTAL,
                                      variable=self.speech_rate_var)
        speech_rate_scale.grid(row=0, column=1, sticky=EW, pady=10)
        self.speech_rate_label = ttk.Label(frame, text="160")
        self.speech_rate_label.grid(row=0, column=2, padx=10)
        speech_rate_scale.bind("<B1-Motion>", self.update_speech_rate_label)
        
        ttk.Label(frame, text="Speech Volume:").grid(row=1, column=0, sticky=W, pady=10)
        self.speech_volume_var = DoubleVar(value=1.0)
        volume_scale = ttk.Scale(frame, from_=0.0, to=1.0, orient=HORIZONTAL,
                                variable=self.speech_volume_var)
        volume_scale.grid(row=1, column=1, sticky=EW, pady=10)
        self.speech_volume_label = ttk.Label(frame, text="100%")
        self.speech_volume_label.grid(row=1, column=2, padx=10)
        volume_scale.bind("<B1-Motion>", self.update_volume_label)
        
        ttk.Label(frame, text="Voice:").grid(row=2, column=0, sticky=W, pady=10)
        self.voice_var = StringVar(value="default")
        voice_combo = ttk.Combobox(frame, textvariable=self.voice_var,
                                   values=["default", "male", "female"], state="readonly")
        voice_combo.grid(row=2, column=1, sticky=EW, pady=10)
        
        ttk.Label(frame, text="Language:").grid(row=3, column=0, sticky=W, pady=10)
        self.language_var = StringVar(value="en-in")
        language_combo = ttk.Combobox(frame, textvariable=self.language_var,
                                      values=["en-in", "en-us", "en-gb", "es-es", "fr-fr"],
                                      state="readonly")
        language_combo.grid(row=3, column=1, sticky=EW, pady=10)
        
        ttk.Label(frame, text="Microphone:").grid(row=4, column=0, sticky=W, pady=10)
        self.microphone_var = StringVar(value="default")
        microphone_combo = ttk.Combobox(frame, textvariable=self.microphone_var,
                                        values=["default", "headset", "built-in"],
                                        state="readonly")
        microphone_combo.grid(row=4, column=1, sticky=EW, pady=10)
        
        frame.columnconfigure(1, weight=1)
    
    def create_appearance_tab(self, notebook):
        """Create appearance settings tab."""
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Appearance")
        
        ttk.Label(frame, text="Theme:").grid(row=0, column=0, sticky=W, pady=10)
        self.theme_var = StringVar(value="light")
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var,
                                   values=["light", "dark", "auto"], state="readonly")
        theme_combo.grid(row=0, column=1, sticky=EW, pady=10)
        
        ttk.Label(frame, text="Font Size:").grid(row=1, column=0, sticky=W, pady=10)
        self.font_size_var = IntVar(value=9)
        font_size_spin = ttk.Spinbox(frame, from_=8, to=16, textvariable=self.font_size_var)
        font_size_spin.grid(row=1, column=1, sticky=EW, pady=10)
        
        ttk.Label(frame, text="Window Size:").grid(row=2, column=0, sticky=W, pady=10)
        self.window_size_var = StringVar(value="600x700")
        size_combo = ttk.Combobox(frame, textvariable=self.window_size_var,
                                  values=["600x700", "800x900", "1024x768"], state="readonly")
        size_combo.grid(row=2, column=1, sticky=EW, pady=10)
        
        self.timestamps_var = BooleanVar(value=True)
        timestamps_check = ttk.Checkbutton(frame, text="Show Timestamps in Output",
                                          variable=self.timestamps_var)
        timestamps_check.grid(row=3, column=0, columnspan=2, sticky=W, pady=10)
        
        self.notifications_var = BooleanVar(value=True)
        notifications_check = ttk.Checkbutton(frame, text="Enable Desktop Notifications",
                                             variable=self.notifications_var)
        notifications_check.grid(row=4, column=0, columnspan=2, sticky=W, pady=10)
        
        frame.columnconfigure(1, weight=1)
    
    def create_system_tab(self, notebook):
        """Create system settings tab."""
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="System")
        
        self.autostart_var = BooleanVar(value=False)
        autostart_check = ttk.Checkbutton(frame, text="Auto-start on system boot",
                                         variable=self.autostart_var)
        autostart_check.pack(anchor=W, pady=10)
        
        self.minimize_tray_var = BooleanVar(value=False)
        minimize_check = ttk.Checkbutton(frame, text="Minimize to system tray",
                                        variable=self.minimize_tray_var)
        minimize_check.pack(anchor=W, pady=10)
        
        ttk.Label(frame, text="Logging Level:").pack(anchor=W, pady=10)
        self.log_level_var = StringVar(value="INFO")
        log_combo = ttk.Combobox(frame, textvariable=self.log_level_var,
                                values=["DEBUG", "INFO", "WARNING", "ERROR"], state="readonly")
        log_combo.pack(fill=X, pady=5)
        
        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, pady=20)
        
        ttk.Label(frame, text="Cache Settings:", font=("Arial", 10, "bold")).pack(anchor=W, pady=10)
        
        self.enable_cache_var = BooleanVar(value=True)
        cache_check = ttk.Checkbutton(frame, text="Enable response caching",
                                     variable=self.enable_cache_var)
        cache_check.pack(anchor=W, pady=5)
        
        clear_cache_btn = Button(frame, text="Clear Cache", command=self.clear_cache,
                                bg="#FF9800", fg="white", padx=20)
        clear_cache_btn.pack(anchor=W, pady=5)
    
    def create_advanced_tab(self, notebook):
        """Create advanced settings tab."""
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Advanced")
        
        ttk.Label(frame, text="Database Operations:", font=("Arial", 10, "bold")).pack(anchor=W, pady=10)
        
        stats = db.get_stats()
        stats_text = f"""
        Notes: {stats.get('notes', 0)}
        Commands: {stats.get('commands', 0)}
        Cache Entries: {stats.get('cache_entries', 0)}
        Settings: {stats.get('settings', 0)}
        """
        ttk.Label(frame, text=stats_text, justify=LEFT).pack(anchor=W, pady=10)
        
        backup_btn = Button(frame, text="Backup Database", command=self.backup_database,
                           bg="#4CAF50", fg="white", padx=20)
        backup_btn.pack(anchor=W, pady=5, fill=X)
        
        restore_btn = Button(frame, text="Restore Database", command=self.restore_database,
                            bg="#2196F3", fg="white", padx=20)
        restore_btn.pack(anchor=W, pady=5, fill=X)
        
        ttk.Separator(frame, orient=HORIZONTAL).pack(fill=X, pady=20)
        
        clear_history_btn = Button(frame, text="Clear Command History", 
                                  command=self.clear_history,
                                  bg="#f44336", fg="white", padx=20)
        clear_history_btn.pack(anchor=W, pady=5, fill=X)
        
        self.debug_mode_var = BooleanVar(value=False)
        debug_check = ttk.Checkbutton(frame, text="Debug Mode (verbose logging)",
                                     variable=self.debug_mode_var)
        debug_check.pack(anchor=W, pady=10)
    
    def update_speech_rate_label(self, event=None):
        self.speech_rate_label.config(text=str(self.speech_rate_var.get()))
    
    def update_volume_label(self, event=None):
        pct = int(self.speech_volume_var.get() * 100)
        self.speech_volume_label.config(text=f"{pct}%")
    
    def load_settings(self):
        """Load settings from database."""
        try:
            self.speech_rate_var.set(db.get_setting("speech_rate", 160))
            self.speech_volume_var.set(db.get_setting("speech_volume", 1.0))
            self.voice_var.set(db.get_setting("voice", "default"))
            self.language_var.set(db.get_setting("language", "en-in"))
            self.microphone_var.set(db.get_setting("microphone", "default"))
            
            self.theme_var.set(db.get_setting("theme", "light"))
            self.font_size_var.set(db.get_setting("font_size", 9))
            self.window_size_var.set(db.get_setting("window_size", "600x700"))
            self.timestamps_var.set(db.get_setting("show_timestamps", True))
            self.notifications_var.set(db.get_setting("notifications", True))
            
            self.autostart_var.set(db.get_setting("autostart", False))
            self.minimize_tray_var.set(db.get_setting("minimize_tray", False))
            self.log_level_var.set(db.get_setting("log_level", "INFO"))
            self.enable_cache_var.set(db.get_setting("enable_cache", True))
            
            self.debug_mode_var.set(db.get_setting("debug_mode", False))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")
    
    def apply_settings(self):
        """Apply and save settings."""
        try:
            db.set_setting("speech_rate", self.speech_rate_var.get(), "int")
            db.set_setting("speech_volume", self.speech_volume_var.get(), "float")
            db.set_setting("voice", self.voice_var.get())
            db.set_setting("language", self.language_var.get())
            db.set_setting("microphone", self.microphone_var.get())
            
            db.set_setting("theme", self.theme_var.get())
            db.set_setting("font_size", self.font_size_var.get(), "int")
            db.set_setting("window_size", self.window_size_var.get())
            db.set_setting("show_timestamps", self.timestamps_var.get(), "bool")
            db.set_setting("notifications", self.notifications_var.get(), "bool")
            
            db.set_setting("autostart", self.autostart_var.get(), "bool")
            db.set_setting("minimize_tray", self.minimize_tray_var.get(), "bool")
            db.set_setting("log_level", self.log_level_var.get())
            db.set_setting("enable_cache", self.enable_cache_var.get(), "bool")
            
            db.set_setting("debug_mode", self.debug_mode_var.get(), "bool")
            
            log_info("Settings applied successfully")
            messagebox.showinfo("Success", "Settings saved successfully!")
            
            if self.on_apply:
                self.on_apply()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {e}")
    
    def reset_defaults(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            db.get_connection().execute("DELETE FROM settings")
            db.get_connection().commit()
            
            self.load_settings()
            messagebox.showinfo("Success", "Settings reset to defaults!")
    
    def clear_cache(self):
        """Clear cache."""
        if messagebox.askyesno("Confirm", "Clear all cached responses?"):
            cleared = db.clear_all_cache()
            messagebox.showinfo("Success", f"Cleared {cleared} cache entries!")
    
    def backup_database(self):
        """Backup database."""
        if db.backup():
            messagebox.showinfo("Success", "Database backed up successfully!")
        else:
            messagebox.showerror("Error", "Failed to backup database")
    
    def restore_database(self):
        """Restore database."""
        if messagebox.askyesno("Confirm", "Restore from backup? Current data will be replaced."):
            if db.restore(str(db.db_path.parent / "leafy_backup_latest.db")):
                messagebox.showinfo("Success", "Database restored successfully!")
                self.load_settings()
            else:
                messagebox.showerror("Error", "Failed to restore database")
    
    def clear_history(self):
        """Clear command history."""
        if messagebox.askyesno("Confirm", "Clear all command history?"):
            db.get_connection().execute("DELETE FROM command_history")
            db.get_connection().commit()
            messagebox.showinfo("Success", "Command history cleared!")
