import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
import csv
from datetime import datetime, timedelta
import shutil
from typing import List, Dict, Any

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱️ TimeTracker Pro")
        self.root.geometry("620x620")
        self.root.configure(bg="#FAFBFC")
        
        # Modern color palette
        self.colors = {
            'bg_primary': '#FAFBFC',
            'bg_secondary': '#F8F9FA',
            'bg_card': '#FFFFFF',
            'primary': '#4F46E5',      # Indigo
            'primary_hover': '#4338CA',
            'secondary': '#10B981',     # Emerald
            'secondary_hover': '#059669',
            'accent': '#F59E0B',       # Amber
            'accent_hover': '#D97706',
            'danger': '#EF4444',       # Red
            'danger_hover': '#DC2626',
            'warning': '#F59E0B',      # Amber
            'info': '#3B82F6',         # Blue
            'success': '#10B981',      # Emerald
            'text_primary': '#111827',
            'text_secondary': '#6B7280',
            'text_muted': '#9CA3AF',
            'border': '#E5E7EB',
            'border_focus': '#4F46E5',
            'pause': '#8B5CF6',        # Purple instead of gray
            'pause_hover': '#7C3AED'
        }

        # Configuration
        self.config_file = 'config.json'
        self.data_file = 'work_hours.json'
        self.backup_dir = 'backups'
        
        # Load configuration
        self.load_config()
        
        # State
        self.project_name = tk.StringVar()
        self.start_time = None          # datetime when session started
        self.last_start = None          # datetime when the current running segment started
        self.elapsed_seconds = 0        # total accumulated seconds across segments
        self.is_running = False
        self.is_paused = False
        self.timer_after_id = None

        # Modern typography
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'heading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 11),
            'button': ('Segoe UI', 10, 'bold'),
            'small': ('Segoe UI', 9),
            'timer': ('Segoe UI', 14, 'bold')
        }

        self.create_ui()

    def create_ui(self):
        """Create the modern UI layout"""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], padx=25, pady=25)
        main_frame.pack(expand=True, fill="both")

        # Title section
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="⏱️ TimeTracker Pro", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        )
        title_label.pack()

        # Project input card
        self.create_project_card(main_frame)
        
        # Timer controls card
        self.create_timer_controls(main_frame)
        
        # Feature buttons card
        self.create_feature_buttons(main_frame)
        
        # Settings card
        self.create_settings_card(main_frame)
        
        # Status section
        self.create_status_section(main_frame)

        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_card_frame(self, parent, title=None):
        """Create a modern card-style frame"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], relief='solid', bd=1)
        card.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        
        if title:
            title_label = tk.Label(
                card, 
                text=title, 
                bg=self.colors['bg_card'], 
                fg=self.colors['text_primary'], 
                font=self.fonts['heading']
            )
            title_label.pack(anchor='w', padx=20, pady=(15, 5))
        
        return card

    def create_project_card(self, parent):
        """Create the project input section"""
        card = self.create_card_frame(parent, "📋 Project Details")
        card.pack(fill="x", pady=(0, 15))
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=20, pady=(0, 20))
        content_frame.pack(fill="x")

        # Project Name
        tk.Label(
            content_frame, 
            text="Project Name *", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(anchor="w", pady=(10, 5))

        project_entry = tk.Entry(
            content_frame, 
            textvariable=self.project_name, 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['body'], 
            relief="solid", 
            bd=2,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['border_focus'],
            highlightthickness=1,
            width=50
        )
        project_entry.pack(fill="x", pady=(0, 15))

        # Memo Section
        tk.Label(
            content_frame, 
            text="Notes & Description", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(anchor="w", pady=(0, 5))

        self.memo_text = tk.Text(
            content_frame, 
            height=4, 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['body'], 
            relief="solid", 
            bd=2,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['border_focus'],
            highlightthickness=1,
            wrap=tk.WORD
        )
        self.memo_text.pack(fill="x")

    def create_timer_controls(self, parent):
        """Create the timer control buttons"""
        card = self.create_card_frame(parent, "⏱️ Timer Controls")
        card.pack(fill="x", pady=(0, 15))
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=20, pady=(0, 20))
        content_frame.pack(fill="x")

        # Timer display
        self.elapsed_label = tk.Label(
            content_frame, 
            text="00:00:00", 
            bg=self.colors['bg_card'], 
            fg=self.colors['primary'], 
            font=self.fonts['timer']
        )
        self.elapsed_label.pack(pady=(10, 20))

        # Button frame
        button_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        button_frame.pack()

        # Start Button
        self.start_button = self.create_modern_button(
            button_frame, 
            "▶ Start", 
            self.start_timer,
            bg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            width=12
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        # Pause/Resume Button
        self.pause_button = self.create_modern_button(
            button_frame, 
            "⏸ Pause", 
            self.toggle_pause,
            bg_color=self.colors['pause'],
            hover_color=self.colors['pause_hover'],
            width=12,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=(0, 10))

        # Stop Button
        self.stop_button = self.create_modern_button(
            button_frame, 
            "⏹ Stop", 
            self.stop_timer,
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=12,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT)

    def create_feature_buttons(self, parent):
        """Create the feature access buttons"""
        card = self.create_card_frame(parent, "📊 Features & Tools")
        card.pack(fill="x", pady=(0, 15))
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=20, pady=(0, 20))
        content_frame.pack(fill="x")

        # First row
        row1_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        row1_frame.pack(pady=(10, 10))

        self.create_modern_button(
            row1_frame, 
            "📋 Entries", 
            self.view_entries,
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            row1_frame, 
            "📊 Reports", 
            self.show_reports,
            bg_color=self.colors['pause'],
            hover_color=self.colors['pause_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            row1_frame, 
            "📁 Data", 
            self.import_export_dialog,
            bg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            width=15
        ).pack(side=tk.LEFT)

    def create_settings_card(self, parent):
        """Create the settings section"""
        card = self.create_card_frame(parent, "⚙️ Settings & Backup")
        card.pack(fill="x", pady=(0, 15))
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=20, pady=(0, 20))
        content_frame.pack(fill="x")

        # Settings row
        settings_row = tk.Frame(content_frame, bg=self.colors['bg_card'])
        settings_row.pack(fill="x", pady=(10, 10))

        # Always on Top Toggle
        self.always_on_top = tk.BooleanVar(value=self.config.get('always_on_top', True))
        self.root.attributes("-topmost", self.always_on_top.get())

        always_top_cb = tk.Checkbutton(
            settings_row,
            text="Keep on top",
            variable=self.always_on_top,
            command=self.toggle_always_on_top,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            activebackground=self.colors['bg_card'],
            selectcolor=self.colors['bg_card'],
            anchor="w"
        )
        always_top_cb.pack(side=tk.LEFT, padx=(0, 20))

        # Auto-backup Toggle
        self.auto_backup = tk.BooleanVar(value=self.config.get('auto_backup', True))
        auto_backup_cb = tk.Checkbutton(
            settings_row,
            text="Auto-backup",
            variable=self.auto_backup,
            command=self.toggle_auto_backup,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            activebackground=self.colors['bg_card'],
            selectcolor=self.colors['bg_card'],
            anchor="w"
        )
        auto_backup_cb.pack(side=tk.LEFT, padx=(0, 20))

        # Manual Backup Button
        self.create_modern_button(
            settings_row, 
            "💾 Backup", 
            self.manual_backup,
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=12
        ).pack(side=tk.RIGHT)

    def create_status_section(self, parent):
        """Create the status display section"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        status_frame.pack(fill="x", pady=(10, 0))

        # Status label with modern styling
        self.status_label = tk.Label(
            status_frame, 
            text="Ready to start tracking", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_muted'], 
            font=self.fonts['small']
        )
        self.status_label.pack()

    def create_modern_button(self, parent, text, command, bg_color, hover_color, width=None, state=tk.NORMAL):
        """Create a modern styled button with hover effects"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg='white',
            font=self.fonts['button'],
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            state=state
        )
        
        if width:
            button.config(width=width)
        
        # Add hover effects
        def on_enter(e):
            if button['state'] != 'disabled':
                button.config(bg=hover_color)
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button.config(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button

    # -------------------------------
    # Configuration Management
    # -------------------------------
    def load_config(self):
        """Load application configuration from file"""
        default_config = {
            'always_on_top': True,
            'auto_backup': True,
            'backup_interval_days': 7,
            'theme': 'default'
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in default_config.items():
                        if key not in self.config:
                            self.config[key] = value
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            self.config = default_config
            self.log_error(f"Failed to load config: {e}")

    def save_config(self):
        """Save application configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log_error(f"Failed to save config: {e}")

    def toggle_auto_backup(self):
        """Toggle auto-backup setting"""
        self.config['auto_backup'] = self.auto_backup.get()
        self.save_config()

    # -------------------------------
    # Helpers
    # -------------------------------
    @staticmethod
    def format_seconds(total_seconds: int) -> str:
        total_seconds = int(total_seconds)
        h, rem = divmod(total_seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def toggle_always_on_top(self):
        """Toggle always-on-top setting"""
        self.root.attributes("-topmost", self.always_on_top.get())
        self.config['always_on_top'] = self.always_on_top.get()
        self.save_config()

    def schedule_tick(self):
        # ensure only one scheduled callback alive
        if self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except Exception:
                pass
        self.timer_after_id = self.root.after(1000, self.update_elapsed_time)

    def cancel_tick(self):
        if self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except Exception:
                pass
            self.timer_after_id = None

    def update_elapsed_time(self):
        if not self.is_running or self.is_paused:
            return
        now = datetime.now()
        total = self.elapsed_seconds + int((now - self.last_start).total_seconds())
        self.elapsed_label.config(text=f"{self.format_seconds(total)}")
        self.schedule_tick()

    def log_error(self, message: str):
        """Log error messages to status label"""
        self.status_label.config(text=f"⚠️ {message}", fg=self.colors['danger'])
        self.root.after(5000, lambda: self.status_label.config(text="Ready to start tracking", fg=self.colors['text_muted']))

    def update_status(self, message: str, color=None):
        """Update status label with message"""
        if color is None:
            color = self.colors['success']
        self.status_label.config(text=f"✓ {message}", fg=color)

    def validate_time_format(self, time_str: str) -> bool:
        """Validate time format (HH:MM:SS or MM:SS)"""
        try:
            parts = time_str.split(":")
            if len(parts) not in [2, 3]:
                return False
            
            for part in parts:
                if not part.isdigit():
                    return False
                num = int(part)
                if num < 0:
                    return False
            
            if len(parts) == 3:  # HH:MM:SS
                if int(parts[1]) >= 60 or int(parts[2]) >= 60:
                    return False
            elif len(parts) == 2:  # MM:SS
                if int(parts[1]) >= 60:
                    return False
                    
            return True
        except:
            return False

    def load_data(self) -> List[Dict[str, Any]]:
        """Load time tracking data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            else:
                data = []
            return data
        except Exception as e:
            self.log_error(f"Failed to load data: {e}")
            return []

    def save_data(self, data: List[Dict[str, Any]]):
        """Save time tracking data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            # Auto-backup if enabled
            if self.auto_backup.get():
                self.auto_backup_data()
                
        except Exception as e:
            self.log_error(f"Failed to save data: {e}")

    def auto_backup_data(self):
        """Create automatic backup of data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            shutil.copy2(self.data_file, backup_file)
            
            # Clean up old backups (keep last 10)
            backup_files = sorted([f for f in os.listdir(self.backup_dir) if f.startswith("backup_")])
            if len(backup_files) > 10:
                for old_backup in backup_files[:-10]:
                    os.remove(os.path.join(self.backup_dir, old_backup))
                    
        except Exception as e:
            self.log_error(f"Auto-backup failed: {e}")

    def manual_backup(self):
        """Create manual backup of data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"manual_backup_{timestamp}.json")
            shutil.copy2(self.data_file, backup_file)
            self.update_status(f"Backup created: {os.path.basename(backup_file)}")
        except Exception as e:
            self.log_error(f"Manual backup failed: {e}")

    # -------------------------------
    # Actions
    # -------------------------------
    def start_timer(self):
        if self.is_running:
            return

        project = self.project_name.get().strip()
        if not project:
            messagebox.showwarning("Project Required", "Please enter a project name before starting the timer.")
            return

        # Initialize session state
        self.start_time = datetime.now()
        self.last_start = self.start_time
        self.elapsed_seconds = 0
        self.is_running = True
        self.is_paused = False

        # UI state
        self.start_button.config(state=tk.DISABLED, bg=self.colors['text_muted'])
        self.stop_button.config(state=tk.NORMAL, bg=self.colors['danger'])
        self.pause_button.config(state=tk.NORMAL, text="⏸ Pause", bg=self.colors['pause'])

        # Start ticking
        self.update_elapsed_time()
        self.update_status(f"Timer started for: {project}")

        messagebox.showinfo("Timer Started", f"Timer started for project: {project}")

    def toggle_pause(self):
        if not self.is_running:
            return

        if not self.is_paused:
            # Pause
            self.is_paused = True
            self.elapsed_seconds += int((datetime.now() - self.last_start).total_seconds())
            self.cancel_tick()
            self.pause_button.config(text="▶ Resume", bg=self.colors['secondary'])
            self.update_status("Timer paused")
        else:
            # Resume
            self.is_paused = False
            self.last_start = datetime.now()
            self.pause_button.config(text="⏸ Pause", bg=self.colors['pause'])
            self.update_elapsed_time()
            self.update_status("Timer resumed")

    def stop_timer(self):
        if not self.is_running:
            return

        # Freeze time accounting
        if not self.is_paused:
            self.elapsed_seconds += int((datetime.now() - self.last_start).total_seconds())

        total_seconds = self.elapsed_seconds
        duration_str = self.format_seconds(total_seconds)
        stop_time = datetime.now()

        # Stop UI updates
        self.cancel_tick()

        # Prepare record
        record = {
            "project": self.project_name.get().strip(),
            "memo": self.memo_text.get("1.0", "end-1c").strip(),
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else "",
            "stop_time": stop_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": duration_str,
            "duration_seconds": int(total_seconds),
        }

        # Load existing data and append new record
        data = self.load_data()
        data.append(record)
        self.save_data(data)

        # Reset session state & UI
        self.is_running = False
        self.is_paused = False
        self.start_time = None
        self.last_start = None
        self.elapsed_seconds = 0

        self.start_button.config(state=tk.NORMAL, bg=self.colors['primary'])
        self.stop_button.config(state=tk.DISABLED, bg=self.colors['text_muted'])
        self.pause_button.config(state=tk.DISABLED, text="⏸ Pause", bg=self.colors['text_muted'])
        self.elapsed_label.config(text="00:00:00")
        self.update_status(f"Session saved: {duration_str}")

        messagebox.showinfo("Timer Stopped",
                            f"Timer stopped for project: {record['project']}\n"
                            f"Duration: {duration_str}")

    def view_entries(self):
        entries_window = tk.Toplevel(self.root)
        entries_window.title("📋 View & Edit Entries")
        entries_window.geometry("850x650")
        entries_window.configure(bg=self.colors['bg_primary'])

        # Load data
        data = self.load_data()

        # Header
        header_frame = tk.Frame(entries_window, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="📋 Time Entries", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        ).pack()

        # Main content card
        content_card = tk.Frame(entries_window, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # Listbox + scrollbar in card
        list_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, bg=self.colors['bg_secondary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            list_frame, 
            width=120, 
            height=18, 
            font=self.fonts['body'], 
            yscrollcommand=scrollbar.set,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        listbox.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        def truncate(text, length=40):
            text = text or ""
            return (text[:length] + "…") if len(text) > length else text

        # Populate
        for i, entry in enumerate(data):
            proj = entry.get('project', '')
            st = entry.get('start_time', '')
            et = entry.get('stop_time', '')
            dur = entry.get('duration') or self.format_seconds(entry.get('duration_seconds', 0))
            memo_snippet = truncate(entry.get('memo', ''), 30)
            listbox.insert(tk.END, f"{i+1}. {proj} | {st} - {et} | {dur} | 📝 {memo_snippet}")

        # Buttons frame
        buttons_frame = tk.Frame(content_card, bg=self.colors['bg_card'], pady=20)
        buttons_frame.pack()

        def edit_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an entry to edit.")
                return

            index = selected[0]
            entry = data[index]

            edit_window = tk.Toplevel(entries_window)
            edit_window.title("✏️ Edit Entry")
            edit_window.geometry("580x480")
            edit_window.configure(bg=self.colors['bg_primary'])

            # Header
            header_frame = tk.Frame(edit_window, bg=self.colors['bg_primary'], pady=20)
            header_frame.pack(fill="x")
            
            tk.Label(
                header_frame, 
                text="✏️ Edit Time Entry", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_primary'], 
                font=self.fonts['heading']
            ).pack()

            # Main form card
            form_card = tk.Frame(edit_window, bg=self.colors['bg_card'], relief='solid', bd=1)
            form_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

            form_frame = tk.Frame(form_card, bg=self.colors['bg_card'], padx=25, pady=25)
            form_frame.pack(fill="both", expand=True)

            fields = ["project", "start_time", "stop_time", "duration"]
            entries_widgets = {}

            # Project / start / stop / duration (strings)
            for i, field in enumerate(fields):
                tk.Label(
                    form_frame, 
                    text=field.replace('_', ' ').title(), 
                    bg=self.colors['bg_card'], 
                    fg=self.colors['text_secondary'], 
                    font=self.fonts['body']
                ).grid(row=i, column=0, sticky="w", padx=(0, 15), pady=8)
                
                entry_var = tk.Entry(
                    form_frame, 
                    width=40,
                    bg=self.colors['bg_card'],
                    fg=self.colors['text_primary'],
                    font=self.fonts['body'],
                    relief="solid",
                    bd=2,
                    highlightbackground=self.colors['border'],
                    highlightcolor=self.colors['border_focus'],
                    highlightthickness=1
                )
                entry_var.insert(0, entry.get(field, ""))
                entry_var.grid(row=i, column=1, sticky="w", pady=8)
                entries_widgets[field] = entry_var

            # Memo (multiline)
            tk.Label(
                form_frame, 
                text="Memo", 
                bg=self.colors['bg_card'], 
                fg=self.colors['text_secondary'], 
                font=self.fonts['body']
            ).grid(row=len(fields), column=0, sticky="nw", padx=(0, 15), pady=8)
            
            memo_box = tk.Text(
                form_frame, 
                width=40, 
                height=6,
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary'],
                font=self.fonts['body'],
                relief="solid",
                bd=2,
                highlightbackground=self.colors['border'],
                highlightcolor=self.colors['border_focus'],
                highlightthickness=1,
                wrap=tk.WORD
            )
            memo_box.insert("1.0", entry.get("memo", ""))
            memo_box.grid(row=len(fields), column=1, sticky="w", pady=8)
            entries_widgets["memo"] = memo_box

            def save_changes():
                # Validate time format
                duration_str = entries_widgets["duration"].get().strip()
                if duration_str and not self.validate_time_format(duration_str):
                    messagebox.showerror("Invalid Format", "Duration must be in HH:MM:SS or MM:SS format")
                    return

                # Update string fields
                for field in fields:
                    entry[field] = entries_widgets[field].get()
                # Update memo
                entry["memo"] = entries_widgets["memo"].get("1.0", "end-1c")

                # Try to sync duration_seconds if possible
                entry["duration_seconds"] = self._parse_duration_to_seconds(duration_str)

                data[index] = entry
                self.save_data(data)
                messagebox.showinfo("Saved", "Entry updated successfully.")
                edit_window.destroy()
                entries_window.destroy()
                self.view_entries()

            def delete_entry():
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
                    data.pop(index)
                    self.save_data(data)
                    messagebox.showinfo("Deleted", "Entry deleted successfully.")
                    edit_window.destroy()
                    entries_window.destroy()
                    self.view_entries()

            # Save and Delete buttons
            button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
            button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
            
            self.create_modern_button(
                button_frame, 
                "🗑️ Delete", 
                delete_entry, 
                bg_color=self.colors['danger'],
                hover_color=self.colors['danger_hover'],
                width=12
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            self.create_modern_button(
                button_frame, 
                "💾 Save", 
                save_changes, 
                bg_color=self.colors['secondary'],
                hover_color=self.colors['secondary_hover'],
                width=12
            ).pack(side=tk.RIGHT)

        def delete_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an entry to delete.")
                return

            index = selected[0]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete entry {index+1}?"):
                data.pop(index)
                self.save_data(data)
                messagebox.showinfo("Deleted", "Entry deleted successfully.")
                entries_window.destroy()
                self.view_entries()

        # Action buttons with modern styling
        self.create_modern_button(
            buttons_frame, 
            "✏️ Edit Selected", 
            edit_selected, 
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            buttons_frame, 
            "🗑️ Delete Selected", 
            delete_selected, 
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            buttons_frame, 
            "📊 Export CSV", 
            lambda: self.export_to_csv(data), 
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=15
        ).pack(side=tk.LEFT)

    def show_reports(self):
        """Show time tracking reports and analytics"""
        reports_window = tk.Toplevel(self.root)
        reports_window.title("📊 Time Tracking Reports")
        reports_window.geometry("750x550")
        reports_window.configure(bg=self.colors['bg_primary'])

        # Load data
        data = self.load_data()
        
        if not data:
            # No data message with modern styling
            no_data_frame = tk.Frame(reports_window, bg=self.colors['bg_primary'])
            no_data_frame.pack(expand=True, fill="both")
            
            tk.Label(
                no_data_frame, 
                text="📊 No Data Available", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_primary'], 
                font=self.fonts['title']
            ).pack(expand=True)
            
            tk.Label(
                no_data_frame, 
                text="Start tracking time to see reports here", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_muted'], 
                font=self.fonts['body']
            ).pack()
            return

        # Header
        header_frame = tk.Frame(reports_window, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="📊 Analytics & Reports", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        ).pack()

        # Create notebook for different report types
        notebook = ttk.Notebook(reports_window)
        notebook.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # Summary Report Tab
        summary_frame = tk.Frame(notebook, bg=self.colors['bg_card'])
        notebook.add(summary_frame, text="📈 Summary")

        # Calculate summary statistics
        total_entries = len(data)
        total_seconds = sum(entry.get('duration_seconds', 0) for entry in data)
        total_hours = total_seconds / 3600
        
        # Project breakdown
        project_totals = {}
        for entry in data:
            project = entry.get('project', 'Unknown')
            duration = entry.get('duration_seconds', 0)
            project_totals[project] = project_totals.get(project, 0) + duration

        # Display summary
        summary_text = f"""📊 TIME TRACKING SUMMARY

Total Entries: {total_entries}
Total Time: {self.format_seconds(total_seconds)} ({total_hours:.2f} hours)

🏆 TOP PROJECTS:
"""
        
        # Sort projects by time
        sorted_projects = sorted(project_totals.items(), key=lambda x: x[1], reverse=True)
        for i, (project, duration) in enumerate(sorted_projects[:5], 1):
            hours = duration / 3600
            summary_text += f"\n{i}. {project}: {self.format_seconds(duration)} ({hours:.2f} hours)"

        summary_label = tk.Label(
            summary_frame, 
            text=summary_text, 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_primary'],
            font=self.fonts['body'], 
            justify=tk.LEFT
        )
        summary_label.pack(pady=30, padx=30, anchor="w")

        # Weekly Report Tab
        weekly_frame = tk.Frame(notebook, bg=self.colors['bg_card'])
        notebook.add(weekly_frame, text="📅 Weekly")

        # Calculate weekly totals for last 4 weeks
        weekly_text = "📅 WEEKLY BREAKDOWN (Last 4 weeks):\n\n"
        
        for i in range(4):
            week_start = datetime.now() - timedelta(weeks=i+1)
            week_end = datetime.now() - timedelta(weeks=i)
            
            week_seconds = 0
            week_entries = []
            
            for entry in data:
                try:
                    entry_date = datetime.strptime(entry.get('start_time', ''), "%Y-%m-%d %H:%M:%S")
                    if week_start <= entry_date < week_end:
                        week_seconds += entry.get('duration_seconds', 0)
                        week_entries.append(entry)
                except:
                    continue
            
            week_hours = week_seconds / 3600
            weekly_text += f"Week ending {week_end.strftime('%Y-%m-%d')}: {self.format_seconds(week_seconds)} ({week_hours:.2f} hours) - {len(week_entries)} entries\n"

        weekly_label = tk.Label(
            weekly_frame, 
            text=weekly_text, 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_primary'],
            font=self.fonts['body'], 
            justify=tk.LEFT
        )
        weekly_label.pack(pady=30, padx=30, anchor="w")

        # Export button
        export_frame = tk.Frame(reports_window, bg=self.colors['bg_primary'], pady=10)
        export_frame.pack()
        
        self.create_modern_button(
            export_frame, 
            "📁 Export Report", 
            lambda: self.export_report_to_csv(data),
            bg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            width=20
        ).pack()

    def import_export_dialog(self):
        """Show import/export options dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📁 Data Management")
        dialog.geometry("450x400")
        dialog.configure(bg=self.colors['bg_primary'])

        # Header
        header_frame = tk.Frame(dialog, bg=self.colors['bg_primary'], pady=25)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="📁 Data Management", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        ).pack()

        # Main content card
        content_card = tk.Frame(dialog, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # Buttons frame
        buttons_frame = tk.Frame(content_card, bg=self.colors['bg_card'], pady=30)
        buttons_frame.pack(expand=True)

        # Export to CSV
        self.create_modern_button(
            buttons_frame, 
            "📤 Export to CSV", 
            lambda: self.export_to_csv(self.load_data()),
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=25
        ).pack(pady=12)

        # Import from CSV
        self.create_modern_button(
            buttons_frame, 
            "📥 Import from CSV", 
            self.import_from_csv,
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=25
        ).pack(pady=12)

        # Backup data
        self.create_modern_button(
            buttons_frame, 
            "💾 Create Backup", 
            self.manual_backup,
            bg_color=self.colors['pause'],
            hover_color=self.colors['pause_hover'],
            width=25
        ).pack(pady=12)

        # Restore from backup
        self.create_modern_button(
            buttons_frame, 
            "🔄 Restore from Backup", 
            self.restore_from_backup,
            bg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            width=25
        ).pack(pady=12)

    def export_to_csv(self, data):
        """Export time tracking data to CSV file"""
        if not data:
            messagebox.showwarning("No Data", "No data available to export.")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save CSV file"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['project', 'memo', 'start_time', 'stop_time', 'duration', 'duration_seconds']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for entry in data:
                        writer.writerow(entry)
                
                self.update_status(f"Data exported to {os.path.basename(filename)}")
                messagebox.showinfo("Export Successful", f"Data exported to:\n{filename}")
                
        except Exception as e:
            self.log_error(f"Export failed: {e}")
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

    def export_report_to_csv(self, data):
        """Export report data to CSV file"""
        if not data:
            messagebox.showwarning("No Data", "No data available to export.")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Report CSV file"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['project', 'total_hours', 'total_seconds', 'entry_count']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    
                    # Calculate project totals
                    project_totals = {}
                    for entry in data:
                        project = entry.get('project', 'Unknown')
                        duration = entry.get('duration_seconds', 0)
                        if project not in project_totals:
                            project_totals[project] = {'total_seconds': 0, 'entry_count': 0}
                        project_totals[project]['total_seconds'] += duration
                        project_totals[project]['entry_count'] += 1
                    
                    # Write project summaries
                    for project, stats in project_totals.items():
                        total_hours = stats['total_seconds'] / 3600
                        writer.writerow({
                            'project': project,
                            'total_hours': f"{total_hours:.2f}",
                            'total_seconds': stats['total_seconds'],
                            'entry_count': stats['entry_count']
                        })
                
                self.update_status(f"Report exported to {os.path.basename(filename)}")
                messagebox.showinfo("Export Successful", f"Report exported to:\n{filename}")
                
        except Exception as e:
            self.log_error(f"Report export failed: {e}")
            messagebox.showerror("Export Error", f"Failed to export report: {e}")

    def import_from_csv(self):
        """Import time tracking data from CSV file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Select CSV file to import"
            )
            
            if filename:
                imported_data = []
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Validate required fields
                        if row.get('project') and row.get('start_time'):
                            imported_data.append(row)
                
                if imported_data:
                    # Load existing data and append imported data
                    existing_data = self.load_data()
                    existing_data.extend(imported_data)
                    self.save_data(existing_data)
                    
                    self.update_status(f"Imported {len(imported_data)} entries from {os.path.basename(filename)}")
                    messagebox.showinfo("Import Successful", f"Imported {len(imported_data)} entries successfully.")
                else:
                    messagebox.showwarning("Import Warning", "No valid data found in the CSV file.")
                    
        except Exception as e:
            self.log_error(f"Import failed: {e}")
            messagebox.showerror("Import Error", f"Failed to import data: {e}")

    def restore_from_backup(self):
        """Restore data from a backup file"""
        try:
            # List available backups
            backup_files = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            
            if not backup_files:
                messagebox.showinfo("No Backups", "No backup files found.")
                return
            
            # Create backup selection dialog
            backup_dialog = tk.Toplevel(self.root)
            backup_dialog.title("🔄 Restore from Backup")
            backup_dialog.geometry("550x450")
            backup_dialog.configure(bg=self.colors['bg_primary'])
            
            # Header
            header_frame = tk.Frame(backup_dialog, bg=self.colors['bg_primary'], pady=20)
            header_frame.pack(fill="x")
            
            tk.Label(
                header_frame, 
                text="🔄 Restore from Backup", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_primary'], 
                font=self.fonts['title']
            ).pack()
            
            tk.Label(
                header_frame, 
                text="Select a backup file to restore:", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_secondary'], 
                font=self.fonts['body']
            ).pack(pady=(5, 0))
            
            # Main content card
            content_card = tk.Frame(backup_dialog, bg=self.colors['bg_card'], relief='solid', bd=1)
            content_card.pack(fill="both", expand=True, padx=25, pady=(0, 25))

            # Backup listbox
            list_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
            list_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            scrollbar = tk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            backup_listbox = tk.Listbox(
                list_frame, 
                font=self.fonts['body'], 
                yscrollcommand=scrollbar.set,
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary'],
                selectbackground=self.colors['primary'],
                selectforeground='white',
                relief='flat',
                bd=0,
                highlightthickness=0
            )
            backup_listbox.pack(side=tk.LEFT, fill="both", expand=True)
            scrollbar.config(command=backup_listbox.yview)
            
            # Populate backup list
            for backup_file in sorted(backup_files, reverse=True):
                backup_listbox.insert(tk.END, backup_file)
            
            def restore_selected():
                selected = backup_listbox.curselection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select a backup file.")
                    return
                
                backup_file = backup_files[selected[0]]
                backup_path = os.path.join(self.backup_dir, backup_file)
                
                if messagebox.askyesno("Confirm Restore", 
                                     f"Are you sure you want to restore from {backup_file}?\n"
                                     "This will replace your current data!"):
                    try:
                        # Create backup of current data before restoring
                        current_backup = os.path.join(self.backup_dir, f"pre_restore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                        if os.path.exists(self.data_file):
                            shutil.copy2(self.data_file, current_backup)
                        
                        # Restore from backup
                        shutil.copy2(backup_path, self.data_file)
                        
                        self.update_status(f"Data restored from {backup_file}")
                        messagebox.showinfo("Restore Successful", f"Data restored from {backup_file}")
                        backup_dialog.destroy()
                        
                    except Exception as e:
                        self.log_error(f"Restore failed: {e}")
                        messagebox.showerror("Restore Error", f"Failed to restore data: {e}")
            
            # Restore button
            button_frame = tk.Frame(content_card, bg=self.colors['bg_card'], pady=20)
            button_frame.pack()
            
            self.create_modern_button(
                button_frame, 
                "🔄 Restore Selected", 
                restore_selected,
                bg_color=self.colors['accent'],
                hover_color=self.colors['accent_hover'],
                width=20
            ).pack()
            
        except Exception as e:
            self.log_error(f"Backup restore failed: {e}")
            messagebox.showerror("Backup Error", f"Failed to access backup directory: {e}")

    # Utility to parse HH:MM:SS safely
    def _parse_duration_to_seconds(self, s: str) -> int:
        try:
            parts = s.split(":")
            if len(parts) == 3:
                h, m, sec = parts
            elif len(parts) == 2:  # MM:SS
                h, m, sec = 0, parts[0], parts[1]
            else:
                return 0
            h = int(h)
            m = int(m)
            sec = int(sec)
            return h*3600 + m*60 + sec
        except Exception:
            return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()

