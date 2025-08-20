import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
import csv
from datetime import datetime, timedelta
import shutil
from typing import List, Dict, Any

class DatePicker:
    """Custom date picker widget for better date selection"""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.date_var = kwargs.get('textvariable', tk.StringVar())
        self.width = kwargs.get('width', 12)
        self.font = kwargs.get('font', ('Segoe UI', 11))
        self.bg = kwargs.get('bg', '#FFFFFF')
        self.fg = kwargs.get('fg', '#111827')
        
        # Current date
        self.current_date = datetime.now()
        self.selected_date = self.current_date
        
        # Create the main entry widget
        self.entry = tk.Entry(
            parent,
            textvariable=self.date_var,
            width=self.width,
            font=self.font,
            relief="solid",
            bd=1,
            bg=self.bg,
            fg=self.fg
        )
        
        # Create calendar button
        self.calendar_button = tk.Button(
            parent,
            text="📅",
            font=('Segoe UI', 10),
            relief="flat",
            bd=0,
            bg=self.bg,
            fg=self.fg,
            cursor="hand2",
            command=self.show_calendar
        )
        
        # Calendar popup
        self.calendar_popup = None
        
        # Pack widgets
        self.entry.pack(side=tk.LEFT)
        self.calendar_button.pack(side=tk.LEFT, padx=(2, 0))
        
        # Bind events
        self.entry.bind('<FocusIn>', self.on_entry_focus)
        self.entry.bind('<Key>', self.on_entry_key)
        
        # Set initial value to current date (not placeholder)
        self.date_var.set(self.current_date.strftime("%Y-%m-%d"))
    
    def on_entry_focus(self, event):
        """Handle entry focus - show calendar if empty"""
        if not self.date_var.get().strip():
            self.show_calendar()
    
    def on_entry_key(self, event):
        """Handle key input in entry"""
        if event.keysym == 'Return':
            self.validate_and_format_date()
    
    def validate_and_format_date(self):
        """Validate and format the date in the entry"""
        try:
            date_str = self.date_var.get().strip()
            if date_str:
                # Try to parse the date
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
                self.selected_date = parsed_date
                self.date_var.set(parsed_date.strftime("%Y-%m-%d"))
        except ValueError:
            # Invalid date, reset to current
            self.date_var.set(self.current_date.strftime("%Y-%m-%d"))
    
    def show_calendar(self):
        """Show the calendar popup"""
        if self.calendar_popup:
            self.calendar_popup.destroy()
        
        # Create popup window
        self.calendar_popup = tk.Toplevel(self.parent)
        self.calendar_popup.title("Select Date")
        self.calendar_popup.geometry("280x320")
        self.calendar_popup.configure(bg='#FAFBFC')
        self.calendar_popup.resizable(False, False)
        
        # Position popup near the entry
        x = self.parent.winfo_rootx() + self.entry.winfo_width()
        y = self.parent.winfo_rooty() + self.entry.winfo_height()
        self.calendar_popup.geometry(f"+{x}+{y}")
        
        # Make popup modal
        self.calendar_popup.transient(self.parent)
        self.calendar_popup.grab_set()
        
        # Header frame
        header_frame = tk.Frame(self.calendar_popup, bg='#4F46E5', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Month/Year navigation
        nav_frame = tk.Frame(header_frame, bg='#4F46E5')
        nav_frame.pack(expand=True)
        
        # Previous month button
        prev_button = tk.Button(
            nav_frame,
            text="◀",
            font=('Segoe UI', 12, 'bold'),
            bg='#4F46E5',
            fg='white',
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.previous_month
        )
        prev_button.pack(side=tk.LEFT, padx=10)
        
        # Month/Year label
        self.month_year_label = tk.Label(
            nav_frame,
            text=self.current_date.strftime("%B %Y"),
            font=('Segoe UI', 12, 'bold'),
            bg='#4F46E5',
            fg='white'
        )
        self.month_year_label.pack(side=tk.LEFT, padx=20)
        
        # Next month button
        next_button = tk.Button(
            nav_frame,
            text="▶",
            font=('Segoe UI', 12, 'bold'),
            bg='#4F46E5',
            fg='white',
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.next_month
        )
        next_button.pack(side=tk.LEFT, padx=10)
        
        # Days of week header
        days_frame = tk.Frame(self.calendar_popup, bg='#FAFBFC')
        days_frame.pack(fill="x", padx=10, pady=5)
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            day_label = tk.Label(
                days_frame,
                text=day,
                font=('Segoe UI', 9, 'bold'),
                bg='#FAFBFC',
                fg='#6B7280',
                width=3
            )
            day_label.grid(row=0, column=i, padx=1, pady=2)
        
        # Calendar grid
        self.calendar_frame = tk.Frame(self.calendar_popup, bg='#FAFBFC')
        self.calendar_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Populate calendar
        self.populate_calendar()
        
        # Today button
        today_button = tk.Button(
            self.calendar_popup,
            text="Today",
            font=('Segoe UI', 10),
            bg='#10B981',
            fg='white',
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.go_to_today
        )
        today_button.pack(pady=10)
        
        # Bind popup close
        self.calendar_popup.bind('<Escape>', lambda e: self.calendar_popup.destroy())
        self.calendar_popup.bind('<FocusOut>', lambda e: self.calendar_popup.after(100, self.check_focus))
    
    def check_focus(self):
        """Check if popup should be closed"""
        try:
            if self.calendar_popup and not self.calendar_popup.focus_get():
                self.calendar_popup.destroy()
                self.calendar_popup = None
        except:
            pass
    
    def previous_month(self):
        """Go to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.month_year_label.config(text=self.current_date.strftime("%B %Y"))
        self.populate_calendar()
    
    def next_month(self):
        """Go to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.month_year_label.config(text=self.current_date.strftime("%B %Y"))
        self.populate_calendar()
    
    def go_to_today(self):
        """Go to current month and select today's date"""
        self.current_date = datetime.now()
        self.selected_date = self.current_date
        self.month_year_label.config(text=self.current_date.strftime("%B %Y"))
        self.populate_calendar()
    
    def populate_calendar(self):
        """Populate the calendar grid with dates"""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Get first day of month and number of days
        first_day = self.current_date.replace(day=1)
        start_weekday = first_day.weekday()  # Monday = 0, Sunday = 6
        if start_weekday == 6:  # Sunday
            start_weekday = 0
        else:
            start_weekday += 1
        
        # Get last day of month
        if self.current_date.month == 12:
            next_month = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            next_month = self.current_date.replace(month=self.current_date.month + 1)
        last_day = (next_month - timedelta(days=1)).day
        
        # Create calendar grid
        day_num = 1
        for week in range(6):  # 6 weeks max
            for day in range(7):  # 7 days per week
                if week == 0 and day < start_weekday:
                    # Empty cell before month starts
                    empty_label = tk.Label(
                        self.calendar_frame,
                        text="",
                        font=('Segoe UI', 9),
                        bg='#FAFBFC',
                        width=3,
                        height=2
                    )
                    empty_label.grid(row=week, column=day, padx=1, pady=1)
                elif day_num <= last_day:
                    # Date cell
                    date_button = tk.Button(
                        self.calendar_frame,
                        text=str(day_num),
                        font=('Segoe UI', 9),
                        bg='#FFFFFF',
                        fg='#111827',
                        relief="flat",
                        bd=1,
                        cursor="hand2",
                        width=3,
                        height=2,
                        command=lambda d=day_num: self.select_date(d)
                    )
                    
                    # Highlight today's date
                    if (day_num == datetime.now().day and 
                        self.current_date.month == datetime.now().month and 
                        self.current_date.year == datetime.now().year):
                        date_button.config(bg='#10B981', fg='white')
                    
                    # Highlight selected date
                    if (day_num == self.selected_date.day and 
                        self.current_date.month == self.selected_date.month and 
                        self.current_date.year == self.selected_date.year):
                        date_button.config(bg='#4F46E5', fg='white')
                    
                    date_button.grid(row=week, column=day, padx=1, pady=1)
                    day_num += 1
                else:
                    # Empty cell after month ends
                    empty_label = tk.Label(
                        self.calendar_frame,
                        text="",
                        font=('Segoe UI', 9),
                        bg='#FAFBFC',
                        width=3,
                        height=2
                    )
                    empty_label.grid(row=week, column=day, padx=1, pady=1)
    
    def select_date(self, day):
        """Select a date from the calendar"""
        self.selected_date = self.current_date.replace(day=day)
        self.date_var.set(self.selected_date.strftime("%Y-%m-%d"))
        
        # Close popup
        if self.calendar_popup:
            self.calendar_popup.destroy()
            self.calendar_popup = None

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱️ TimeTracker Pro")
        self.root.geometry("900x800")
        self.root.configure(bg="#FAFBFC")
        
        # Window management - track open dialogs and prevent multiple instances
        self.open_dialogs = {}
        
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
        self.projects_file = 'projects.json'
        self.invoice_rates_file = 'invoice_rates.json'
        
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
        
        # Project management
        self.projects = []
        self.current_project_id = None
        self.invoice_rates = {}
        
        # Load projects and invoice rates
        self.load_projects()
        self.load_invoice_rates()

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
        # Create menu bar
        self.create_menu_bar()
        
        # Main container with scrollbar
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame with padding
        main_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_primary'], padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            try:
                if canvas and canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        canvas.bind("<MouseWheel>", _on_mousewheel)

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
        
        # Status section
        self.create_status_section(main_frame)

        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="📤 Export to CSV", command=lambda: self.export_to_csv(self.load_data()))
        file_menu.add_command(label="📥 Import from CSV", command=self.import_from_csv)
        file_menu.add_separator()
        file_menu.add_command(label="💾 Create Backup", command=self.manual_backup)
        file_menu.add_command(label="💾 Quick Backup", command=self.manual_backup)
        file_menu.add_command(label="🔄 Restore from Backup", command=self.restore_from_backup)
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.root.quit)
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        view_menu.add_command(label="📋 Time Entries", command=self.view_entries)
        view_menu.add_command(label="📊 Reports & Analytics", command=self.show_reports)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🛠️ Tools", menu=tools_menu)
        tools_menu.add_command(label="📋 Project Management", command=self.show_project_manager)
        tools_menu.add_command(label="💰 Invoice Rates", command=self.show_invoice_rates)
        tools_menu.add_command(label="⚙️ Data Management", command=self.import_export_dialog)
        tools_menu.add_command(label="🔧 Settings", command=self.show_settings)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="📖 About", command=self.show_about)

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
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=20, pady=20)
        content_frame.pack(fill="x")

        # Project Selection
        project_selection_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        project_selection_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            project_selection_frame, 
            text="Select Project *", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(anchor="w", pady=(0, 5))

        # Project selector frame
        selector_frame = tk.Frame(project_selection_frame, bg=self.colors['bg_card'])
        selector_frame.pack(fill="x")

        # Project dropdown
        self.project_var = tk.StringVar()
        self.project_dropdown = ttk.Combobox(
            selector_frame,
            textvariable=self.project_var,
            state="readonly",
            font=self.fonts['body'],
            width=40
        )
        self.project_dropdown.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        
        # Update project list
        self.update_project_dropdown()
        
        # Bind selection change
        self.project_dropdown.bind('<<ComboboxSelected>>', self.on_project_selected)

        # Project management buttons
        self.create_modern_button(
            selector_frame,
            "➕ New",
            self.show_project_manager,
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=8
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.create_modern_button(
            selector_frame,
            "✏️ Edit",
            self.show_project_manager,
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=8
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.create_modern_button(
            selector_frame,
            "💰 Rates",
            self.show_invoice_rates,
            bg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            width=8
        ).pack(side=tk.LEFT)

        # Project Name (for backward compatibility and editing)
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
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=20, pady=20)
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

        # Invoiced toggle - REMOVED per user request
        # invoiced_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        # invoiced_frame.pack(pady=(15, 0))
        # 
        # self.invoiced_var = tk.BooleanVar(value=False)
        # invoiced_checkbox = tk.Checkbutton(
        #     invoiced_frame,
        #     text="💰 Mark as Invoiced",
        #     variable=self.invoiced_var,
        #     bg=self.colors['bg_card'],
        #     fg=self.colors['text_primary'],
        #     font=self.fonts['body'],
        #     activebackground=self.colors['bg_card'],
        #     selectcolor=self.colors['bg_card'],
        #     anchor="w"
        # )
        # invoiced_checkbox.pack()

    def create_settings_card(self, parent):
        """Create the settings section"""
        card = self.create_card_frame(parent, "⚙️ Quick Settings")
        card.pack(fill="x", pady=(0, 15))
        
        content_frame = tk.Frame(card, bg=self.colors['bg_card'], padx=25, pady=20)
        content_frame.pack(fill="x")

        # Settings info
        info_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        info_frame.pack(fill="x", pady=10)

        tk.Label(
            info_frame,
            text="ℹ️ Use the Settings button above for full configuration options",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=self.fonts['small']
        ).pack(anchor="w")

        # Quick backup button
        backup_frame = tk.Frame(content_frame, bg=self.colors['bg_card'])
        backup_frame.pack(fill="x", pady=10)

        self.create_modern_button(
            backup_frame, 
            "💾 Quick Backup", 
            self.manual_backup,
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=18
        ).pack()

    def create_status_section(self, parent):
        """Create the status display section"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        status_frame.pack(fill="x", pady=10)

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

    def load_projects(self):
        """Load projects from file"""
        try:
            if os.path.exists(self.projects_file):
                with open(self.projects_file, 'r', encoding='utf-8') as f:
                    self.projects = json.load(f)
                    if not isinstance(self.projects, list):
                        self.projects = []
            else:
                # Create default project if none exist
                self.projects = [{
                    'id': 'default',
                    'name': 'Default Project',
                    'status': 'Active',
                    'invoice': 'No',
                    'description': 'Default project for time tracking'
                }]
                self.save_projects()
        except Exception as e:
            self.log_error(f"Failed to load projects: {e}")
            self.projects = []

    def save_projects(self):
        """Save projects to file"""
        try:
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                json.dump(self.projects, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log_error(f"Failed to save projects: {e}")

    def load_invoice_rates(self):
        """Load invoice rates from file"""
        try:
            if os.path.exists(self.invoice_rates_file):
                with open(self.invoice_rates_file, 'r', encoding='utf-8') as f:
                    self.invoice_rates = json.load(f)
                    if not isinstance(self.invoice_rates, dict):
                        self.invoice_rates = {}
            else:
                # Create default invoice rates
                self.invoice_rates = {
                    'default': {
                        'rate': 50.0,
                        'currency': 'USD'
                    }
                }
                self.save_invoice_rates()
        except Exception as e:
            self.log_error(f"Failed to load invoice rates: {e}")
            self.invoice_rates = {}

    def save_invoice_rates(self):
        """Save invoice rates to file"""
        try:
            with open(self.invoice_rates_file, 'w', encoding='utf-8') as f:
                json.dump(self.invoice_rates, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log_error(f"Failed to save invoice rates: {e}")

    def get_project_by_id(self, project_id):
        """Get project by ID"""
        for project in self.projects:
            if project.get('id') == project_id:
                return project
        return None

    def get_current_project(self):
        """Get current selected project"""
        if self.current_project_id:
            return self.get_project_by_id(self.current_project_id)
        return None

    def toggle_auto_backup(self):
        """Toggle auto-backup setting"""
        if hasattr(self, 'auto_backup') and self.auto_backup:
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
        if hasattr(self, 'always_on_top') and self.always_on_top:
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
            if self.config.get('auto_backup', True):
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
        
        # Reset invoiced checkbox - REMOVED since checkbox was removed
        # self.invoiced_var.set(False)

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
            "invoiced": "No",  # Default to not invoiced
            "project_id": self.current_project_id  # Store project ID for reference
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
        entries_window = self.create_dialog("view_entries", "📋 View & Edit Entries", "850x750")
        
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
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        # Listbox + scrollbar in card
        list_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Filter options
        filter_frame = tk.Frame(list_frame, bg=self.colors['bg_card'])
        filter_frame.pack(fill="x", pady=(0, 10))
        
        # Date filter section
        date_filter_frame = tk.Frame(filter_frame, bg=self.colors['bg_card'])
        date_filter_frame.pack(fill="x", pady=(0, 10))
        
        # From date
        from_date_frame = tk.Frame(date_filter_frame, bg=self.colors['bg_card'])
        from_date_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            from_date_frame, 
            text="From:", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        from_date_var = tk.StringVar()
        from_date_picker = DatePicker(
            from_date_frame,
            textvariable=from_date_var,
            width=12,
            font=self.fonts['body'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        
        # To date
        to_date_frame = tk.Frame(date_filter_frame, bg=self.colors['bg_card'])
        to_date_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            to_date_frame, 
            text="To:", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        to_date_var = tk.StringVar()
        to_date_picker = DatePicker(
            to_date_frame,
            textvariable=to_date_var,
            width=12,
            font=self.fonts['body'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        
        # Clear dates button
        clear_dates_button = self.create_modern_button(
            date_filter_frame,
            "🗑️ Clear",
            lambda: self.clear_date_filters(from_date_var, to_date_var),
            bg_color=self.colors['text_secondary'],
            hover_color=self.colors['text_primary'],
            width=8
        )
        clear_dates_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Status filter
        status_filter_frame = tk.Frame(filter_frame, bg=self.colors['bg_card'])
        status_filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            status_filter_frame, 
            text="Status:", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            status_filter_frame, 
            textvariable=filter_var, 
            values=["All", "Invoiced", "Not Invoiced"], 
            state="readonly", 
            font=self.fonts['body'],
            width=15
        )
        filter_combo.pack(side=tk.LEFT)
        
        # Apply filter button (will be configured after listbox is created)
        filter_button = self.create_modern_button(
            status_filter_frame,
            "🔄 Apply",
            lambda: None,  # Placeholder
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=8
        )
        filter_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Multiple selection instructions
        instruction_frame = tk.Frame(list_frame, bg=self.colors['bg_card'])
        instruction_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            instruction_frame, 
            text="💡 Tip: Use Ctrl+Click or Shift+Click to select multiple entries for bulk operations", 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['small']
        ).pack(anchor="w")

        # Listbox
        listbox = tk.Listbox(
            list_frame, 
            width=120, 
            height=18, 
            font=self.fonts['body'], 
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0,
            selectmode=tk.EXTENDED  # Enable multiple selection
        )
        listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Create scrollbar after listbox
        entries_scrollbar = tk.Scrollbar(list_frame, bg=self.colors['bg_secondary'])
        entries_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbar and listbox
        listbox.config(yscrollcommand=entries_scrollbar.set)
        entries_scrollbar.config(command=listbox.yview)

        # Store filtered data and mapping for operations
        filtered_data = []
        original_to_filtered_mapping = {}  # Maps original indices to filtered indices
        
        def refresh_listbox_with_fresh_data():
            """Refresh the listbox with fresh data from file"""
            try:
                # Always load fresh data from file
                fresh_data = self.load_data()
                
                # Clear current entries
                listbox.delete(0, tk.END)
                
                # Repopulate with fresh data
                for i, entry in enumerate(fresh_data):
                    proj = entry.get('project', '')
                    st = entry.get('start_time', '')
                    et = entry.get('stop_time', '')
                    dur = entry.get('duration') or self.format_seconds(entry.get('duration_seconds', 0))
                    memo_snippet = truncate(entry.get('memo', ''), 30)
                    invoiced_status = entry.get('invoiced', 'No')
                    invoiced_icon = "💰" if invoiced_status == "Yes" else "📝"
                    listbox.insert(tk.END, f"{i+1}. {proj} | {st} - {et} | {dur} | {invoiced_icon} {invoiced_status} | 📝 {memo_snippet}")
                    
            except Exception as e:
                self.log_error(f"Failed to refresh listbox: {e}")

        def apply_filter():
            """Apply the selected filter to the listbox"""
            try:
                filter_value = filter_var.get()
                from_date = from_date_var.get().strip()
                to_date = to_date_var.get().strip()
                
                listbox.delete(0, tk.END)
                
                # Always use fresh data for filtering
                fresh_data = self.load_data()
                filtered_data.clear()
                original_to_filtered_mapping.clear()
                
                # First filter by status
                if filter_value == "All":
                    status_filtered = fresh_data
                elif filter_value == "Invoiced":
                    status_filtered = [entry for entry in fresh_data if entry.get('invoiced') == 'Yes']
                elif filter_value == "Not Invoiced":
                    status_filtered = [entry for entry in fresh_data if entry.get('invoiced') != 'Yes']
                else:
                    status_filtered = fresh_data
                
                # Then filter by date range if specified
                if from_date or to_date:
                    for i, entry in enumerate(status_filtered):
                        try:
                            entry_date = datetime.strptime(entry.get('start_time', ''), "%Y-%m-%d %H:%M:%S").date()
                            
                            # Check from date
                            if from_date:
                                try:
                                    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
                                    if entry_date < from_date_obj:
                                        continue
                                except ValueError:
                                    pass  # Invalid date format, skip this filter
                            
                            # Check to date
                            if to_date:
                                try:
                                    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
                                    if entry_date > to_date_obj:
                                        continue
                                except ValueError:
                                    pass  # Invalid date format, skip this filter
                            
                            # Store the filtered entry and its original index
                            original_index = fresh_data.index(entry)
                            filtered_data.append(entry)
                            original_to_filtered_mapping[original_index] = len(filtered_data) - 1
                            
                        except (ValueError, TypeError):
                            # If date parsing fails, include the entry
                            original_index = fresh_data.index(entry)
                            filtered_data.append(entry)
                            original_to_filtered_mapping[original_index] = len(filtered_data) - 1
                else:
                    # No date filtering, use status filtered data
                    for i, entry in enumerate(status_filtered):
                        original_index = fresh_data.index(entry)
                        filtered_data.append(entry)
                        original_to_filtered_mapping[original_index] = len(filtered_data) - 1
                
                # Populate with filtered data
                for i, entry in enumerate(filtered_data):
                    proj = entry.get('project', '')
                    st = entry.get('start_time', '')
                    et = entry.get('stop_time', '')
                    dur = entry.get('duration') or self.format_seconds(entry.get('duration_seconds', 0))
                    memo_snippet = truncate(entry.get('memo', ''), 30)
                    invoiced_status = entry.get('invoiced', 'No')
                    invoiced_icon = "💰" if invoiced_status == "Yes" else "📝"
                    listbox.insert(tk.END, f"{i+1}. {proj} | {st} - {et} | {dur} | {invoiced_icon} {invoiced_status} | 📝 {memo_snippet}")
                    
            except Exception as e:
                self.log_error(f"Failed to apply filter: {e}")
        
        # Now configure the filter functionality
        filter_combo.bind('<<ComboboxSelected>>', lambda e: apply_filter())
        filter_button.config(command=apply_filter)

        def truncate(text, length=40):
            text = text or ""
            return (text[:length] + "…") if len(text) > length else text

        # Initial population
        apply_filter()

        # Buttons frame
        buttons_frame = tk.Frame(content_card, bg=self.colors['bg_card'], pady=20)
        buttons_frame.pack()

        def edit_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an entry to edit.")
                return

            # For editing, we only work with the first selected entry
            filtered_index = selected[0]
            
            # Get the actual entry from filtered data
            if filtered_index >= len(filtered_data):
                messagebox.showerror("Error", "Entry no longer exists.")
                return
            entry = filtered_data[filtered_index]
            
            # Find the original index in the full dataset
            original_index = None
            for orig_idx, filtered_idx in original_to_filtered_mapping.items():
                if filtered_idx == filtered_index:
                    original_index = orig_idx
                    break
            
            if original_index is None:
                messagebox.showerror("Error", "Could not locate original entry.")
                return
            
            # Show info if multiple entries were selected
            if len(selected) > 1:
                messagebox.showinfo("Multiple Selection", f"Multiple entries selected ({len(selected)}). Only the first entry will be edited.")

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
            form_card.pack(fill="both", expand=True, padx=25, pady=25)

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

            # Invoiced status
            tk.Label(
                form_frame, 
                text="Invoiced", 
                bg=self.colors['bg_card'], 
                fg=self.colors['text_secondary'], 
                font=self.fonts['body']
            ).grid(row=len(fields)+1, column=0, sticky="w", padx=(0, 15), pady=8)
            
            invoiced_var = tk.StringVar(value=entry.get("invoiced", "No"))
            invoiced_combo = ttk.Combobox(
                form_frame, 
                textvariable=invoiced_var, 
                values=["Yes", "No"], 
                state="readonly", 
                font=self.fonts['body'],
                width=37
            )
            invoiced_combo.grid(row=len(fields)+1, column=1, sticky="w", pady=8)
            entries_widgets["invoiced"] = invoiced_var

            def save_changes():
                # Validate time format
                duration_str = entries_widgets["duration"].get().strip()
                if duration_str and not self.validate_time_format(duration_str):
                    messagebox.showerror("Invalid Format", "Duration must be in HH:MM:SS or MM:SS format")
                    return

                # Get fresh data and update
                fresh_data = self.load_data()
                if original_index >= len(fresh_data):
                    messagebox.showerror("Error", "Entry no longer exists.")
                    return

                # Update string fields
                for field in fields:
                    fresh_data[original_index][field] = entries_widgets[field].get()
                # Update memo
                fresh_data[original_index]["memo"] = entries_widgets["memo"].get("1.0", "end-1c")
                # Update invoiced status
                fresh_data[original_index]["invoiced"] = entries_widgets["invoiced"].get()

                # Try to sync duration_seconds if possible
                fresh_data[original_index]["duration_seconds"] = self._parse_duration_to_seconds(duration_str)

                self.save_data(fresh_data)
                messagebox.showinfo("Saved", "Entry updated successfully.")
                edit_window.destroy()
                # Refresh the listbox with fresh data
                apply_filter()

            def delete_entry():
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
                    # Get fresh data and delete
                    fresh_data = self.load_data()
                    if original_index < len(fresh_data):
                        fresh_data.pop(original_index)
                        self.save_data(fresh_data)
                        messagebox.showinfo("Deleted", "Entry deleted successfully.")
                        edit_window.destroy()
                        # Refresh the listbox with fresh data
                        apply_filter()

            # Save and Delete buttons
            button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
            button_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=20)
            
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

            # Handle multiple deletions
            if len(selected) == 1:
                filtered_index = selected[0]
                if filtered_index >= len(filtered_data):
                    messagebox.showerror("Error", "Entry no longer exists.")
                    return
                
                # Find the original index
                original_index = None
                for orig_idx, filtered_idx in original_to_filtered_mapping.items():
                    if filtered_idx == filtered_index:
                        original_index = orig_idx
                        break
                
                if original_index is None:
                    messagebox.showerror("Error", "Could not locate original entry.")
                    return
                
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this entry?"):
                    # Get fresh data and delete
                    fresh_data = self.load_data()
                    if original_index < len(fresh_data):
                        fresh_data.pop(original_index)
                        self.save_data(fresh_data)
                        messagebox.showinfo("Deleted", "Entry deleted successfully.")
                        # Refresh the listbox with fresh data
                        apply_filter()
            else:
                # Multiple deletions
                count = len(selected)
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {count} selected entries?"):
                    # Get fresh data and delete
                    fresh_data = self.load_data()
                    original_indices_to_delete = []
                    
                    # Find all original indices for selected filtered entries
                    for filtered_index in selected:
                        if filtered_index < len(filtered_data):
                            for orig_idx, filtered_idx in original_to_filtered_mapping.items():
                                if filtered_idx == filtered_index:
                                    original_indices_to_delete.append(orig_idx)
                                    break
                    
                    # Delete in reverse order to maintain indices
                    for original_index in sorted(original_indices_to_delete, reverse=True):
                        if original_index < len(fresh_data):
                            fresh_data.pop(original_index)
                    
                    self.save_data(fresh_data)
                    messagebox.showinfo("Deleted", f"{count} entries deleted successfully.")
                    # Refresh the listbox with fresh data
                    apply_filter()

        # Action buttons with modern styling
        self.create_modern_button(
            buttons_frame, 
            "✏️ Edit Selected (1st)", 
            edit_selected, 
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=18
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            buttons_frame, 
            "🗑️ Delete Selected", 
            delete_selected, 
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=18
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            buttons_frame, 
            "💰 Toggle Invoiced", 
            self.mark_as_invoiced, 
            bg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            width=18
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            buttons_frame, 
            "📊 Export CSV", 
            lambda: self.export_to_csv(filtered_data), 
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=15
        ).pack(side=tk.LEFT)

    def show_reports(self):
        """Show time tracking reports and analytics"""
        reports_window = self.create_dialog("reports", "📊 Time Tracking Reports", "750x550")
        
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
        
        # Date filter controls for reports
        date_filter_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'], pady=10)
        date_filter_frame.pack()
        
        # From date
        from_date_label = tk.Label(
            date_filter_frame, 
            text="From:", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        )
        from_date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        reports_from_date_var = tk.StringVar()
        reports_from_date_picker = DatePicker(
            date_filter_frame,
            textvariable=reports_from_date_var,
            width=12,
            font=self.fonts['body'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        
        # To date
        to_date_label = tk.Label(
            date_filter_frame, 
            text="To:", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        )
        to_date_label.pack(side=tk.LEFT, padx=(0, 5))
        
        reports_to_date_var = tk.StringVar()
        reports_to_date_picker = DatePicker(
            date_filter_frame,
            textvariable=reports_to_date_var,
            width=12,
            font=self.fonts['body'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        
        # Apply date filter button
        apply_date_filter_button = self.create_modern_button(
            date_filter_frame,
            "🔄 Apply Date Filter",
            lambda: self.apply_reports_date_filter(data, reports_from_date_var, reports_to_date_var),
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        )
        apply_date_filter_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear date filter button
        clear_reports_date_button = self.create_modern_button(
            date_filter_frame,
            "🗑️ Clear",
            lambda: self.clear_reports_date_filters(reports_from_date_var, reports_to_date_var),
            bg_color=self.colors['text_secondary'],
            hover_color=self.colors['text_primary'],
            width=8
        )
        clear_reports_date_button.pack(side=tk.LEFT)

        # Create notebook for different report types
        notebook = ttk.Notebook(reports_window)
        notebook.pack(fill="both", expand=True, padx=25, pady=25)

        # Summary Report Tab
        summary_frame = tk.Frame(notebook, bg=self.colors['bg_card'])
        notebook.add(summary_frame, text="📈 Summary")

        # Create scrollable frame for summary
        summary_canvas = tk.Canvas(summary_frame, bg=self.colors['bg_card'], highlightthickness=0)
        summary_scrollbar = tk.Scrollbar(summary_frame, orient="vertical", command=summary_canvas.yview)
        summary_scrollable_frame = tk.Frame(summary_canvas, bg=self.colors['bg_card'])
        
        summary_scrollable_frame.bind(
            "<Configure>",
            lambda e: summary_canvas.configure(scrollregion=summary_canvas.bbox("all"))
        )
        
        summary_canvas.create_window((0, 0), window=summary_scrollable_frame, anchor="nw")
        summary_canvas.configure(yscrollcommand=summary_scrollbar.set)
        
        # Pack canvas and scrollbar
        summary_canvas.pack(side="left", fill="both", expand=True)
        summary_scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to summary canvas
        def _on_summary_mousewheel(event):
            try:
                if summary_canvas and summary_canvas.winfo_exists() and summary_canvas.winfo_manager():
                    summary_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        summary_canvas.bind("<MouseWheel>", _on_summary_mousewheel)

        # Calculate summary statistics
        total_entries = len(data)
        total_seconds = sum(entry.get('duration_seconds', 0) for entry in data)
        total_hours = total_seconds / 3600
        
        # Invoiced status breakdown
        invoiced_seconds = sum(entry.get('duration_seconds', 0) for entry in data if entry.get('invoiced') == 'Yes')
        not_invoiced_seconds = total_seconds - invoiced_seconds
        invoiced_hours = invoiced_seconds / 3600
        not_invoiced_hours = not_invoiced_seconds / 3600
        
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

💰 INVOICING STATUS:
• Invoiced: {self.format_seconds(invoiced_seconds)} ({invoiced_hours:.2f} hours)
• Not Invoiced: {self.format_seconds(not_invoiced_seconds)} ({not_invoiced_hours:.2f} hours)

📋 TOP PROJECTS:
"""
        
        # Sort projects by time
        sorted_projects = sorted(project_totals.items(), key=lambda x: x[1], reverse=True)
        for i, (project, duration) in enumerate(sorted_projects[:5], 1):
            hours = duration / 3600
            summary_text += f"\n{i}. {project}: {self.format_seconds(duration)} ({hours:.2f} hours)"

        summary_label = tk.Label(
            summary_scrollable_frame, 
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

        # Create scrollable frame for weekly
        weekly_canvas = tk.Canvas(weekly_frame, bg=self.colors['bg_card'], highlightthickness=0)
        weekly_scrollbar = tk.Scrollbar(weekly_frame, orient="vertical", command=weekly_canvas.yview)
        weekly_scrollable_frame = tk.Frame(weekly_canvas, bg=self.colors['bg_card'])
        
        weekly_scrollable_frame.bind(
            "<Configure>",
            lambda e: weekly_canvas.configure(scrollregion=weekly_canvas.bbox("all"))
        )
        
        weekly_canvas.create_window((0, 0), window=weekly_scrollable_frame, anchor="nw")
        weekly_canvas.configure(yscrollcommand=weekly_scrollbar.set)
        
        # Pack canvas and scrollbar
        weekly_canvas.pack(side="left", fill="both", expand=True)
        weekly_scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to weekly canvas
        def _on_weekly_mousewheel(event):
            try:
                if weekly_canvas and weekly_canvas.winfo_exists() and weekly_canvas.winfo_manager():
                    weekly_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        weekly_canvas.bind("<MouseWheel>", _on_weekly_mousewheel)

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
            weekly_scrollable_frame, 
            text=weekly_text, 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_primary'],
            font=self.fonts['body'], 
            justify=tk.LEFT
        )
        weekly_label.pack(pady=30, padx=30, anchor="w")

        # Invoicing Report Tab
        invoicing_frame = tk.Frame(notebook, bg=self.colors['bg_card'])
        notebook.add(invoicing_frame, text="💰 Invoicing")

        # Create scrollable frame for invoicing
        invoicing_canvas = tk.Canvas(invoicing_frame, bg=self.colors['bg_card'], highlightthickness=0)
        invoicing_scrollbar = tk.Scrollbar(invoicing_frame, orient="vertical", command=invoicing_canvas.yview)
        invoicing_scrollable_frame = tk.Frame(invoicing_canvas, bg=self.colors['bg_card'])
        
        invoicing_scrollable_frame.bind(
            "<Configure>",
            lambda e: invoicing_canvas.configure(scrollregion=invoicing_canvas.bbox("all"))
        )
        
        invoicing_canvas.create_window((0, 0), window=invoicing_scrollable_frame, anchor="nw")
        invoicing_canvas.configure(yscrollcommand=invoicing_scrollbar.set)
        
        # Pack canvas and scrollbar
        invoicing_canvas.pack(side="left", fill="both", expand=True)
        invoicing_scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to invoicing canvas
        def _on_invoicing_mousewheel(event):
            try:
                if invoicing_canvas and invoicing_canvas.winfo_exists() and invoicing_canvas.winfo_manager():
                    invoicing_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        invoicing_canvas.bind("<MouseWheel>", _on_invoicing_mousewheel)

        # Calculate invoicing statistics
        invoiced_entries = [entry for entry in data if entry.get('invoiced') == 'Yes']
        not_invoiced_entries = [entry for entry in data if entry.get('invoiced') != 'Yes']
        
        invoiced_seconds = sum(entry.get('duration_seconds', 0) for entry in invoiced_entries)
        not_invoiced_seconds = sum(entry.get('duration_seconds', 0) for entry in not_invoiced_entries)
        
        invoiced_hours = invoiced_seconds / 3600
        not_invoiced_hours = not_invoiced_seconds / 3600
        
        # Project invoicing breakdown
        project_invoicing = {}
        for entry in data:
            project = entry.get('project', 'Unknown')
            if project not in project_invoicing:
                project_invoicing[project] = {'invoiced': 0, 'not_invoiced': 0}
            
            if entry.get('invoiced') == 'Yes':
                project_invoicing[project]['invoiced'] += entry.get('duration_seconds', 0)
            else:
                project_invoicing[project]['not_invoiced'] += entry.get('duration_seconds', 0)

        # Display invoicing report
        invoicing_text = f"""💰 INVOICING REPORT

📊 OVERVIEW:
• Total Invoiced: {self.format_seconds(invoiced_seconds)} ({invoiced_hours:.2f} hours)
• Total Not Invoiced: {self.format_seconds(not_invoiced_seconds)} ({not_invoiced_hours:.2f} hours)
• Invoiced Entries: {len(invoiced_entries)}
• Pending Entries: {len(not_invoiced_entries)}

📋 PROJECT BREAKDOWN:
"""
        
        # Sort projects by total time
        sorted_projects = sorted(project_invoicing.items(), 
                               key=lambda x: x[1]['invoiced'] + x[1]['not_invoiced'], 
                               reverse=True)
        
        for project, stats in sorted_projects[:8]:  # Show top 8 projects
            total_project_time = stats['invoiced'] + stats['not_invoiced']
            total_project_hours = total_project_time / 3600
            invoiced_project_hours = stats['invoiced'] / 3600
            not_invoiced_project_hours = stats['not_invoiced'] / 3600
            
            invoicing_text += f"\n• {project}:"
            invoicing_text += f"\n  - Total: {self.format_seconds(total_project_time)} ({total_project_hours:.2f} hours)"
            invoicing_text += f"\n  - Invoiced: {self.format_seconds(stats['invoiced'])} ({invoiced_project_hours:.2f} hours)"
            invoicing_text += f"\n  - Pending: {self.format_seconds(stats['not_invoiced'])} ({not_invoiced_project_hours:.2f} hours)"

        invoicing_label = tk.Label(
            invoicing_scrollable_frame, 
            text=invoicing_text, 
            bg=self.colors['bg_card'], 
            fg=self.colors['text_primary'],
            font=self.fonts['body'], 
            justify=tk.LEFT
        )
        invoicing_label.pack(pady=30, padx=30, anchor="w")

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
        dialog = self.create_dialog("data_management", "📁 Data Management", "450x400")
        
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
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

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
                    fieldnames = ['project', 'memo', 'start_time', 'stop_time', 'duration', 'duration_seconds', 'invoiced', 'project_id']
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
                            # Ensure new fields exist with defaults
                            if 'invoiced' not in row:
                                row['invoiced'] = 'No'
                            if 'project_id' not in row:
                                row['project_id'] = None
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
            backup_dialog = self.create_dialog("backup_restore", "🔄 Restore from Backup", "550x450")
            
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
            content_card.pack(fill="both", expand=True, padx=25, pady=25)

            # Backup listbox
            list_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
            list_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Listbox with scrollbar
            backup_scrollbar = tk.Scrollbar(list_frame)
            backup_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            backup_listbox = tk.Listbox(
                list_frame, 
                font=self.fonts['body'], 
                yscrollcommand=backup_scrollbar.set,
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary'],
                selectbackground=self.colors['primary'],
                selectforeground='white',
                relief='flat',
                bd=0,
                highlightthickness=0
            )
            backup_listbox.pack(side=tk.LEFT, fill="both", expand=True)
            backup_scrollbar.config(command=backup_listbox.yview)
            
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

    def show_settings(self):
        """Show the settings dialog"""
        settings_window = self.create_dialog("settings", "⚙️ Settings", "500x400")
        
        # Header
        header_frame = tk.Frame(settings_window, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="⚙️ Application Settings", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        ).pack()

        # Main content card
        content_card = tk.Frame(settings_window, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        settings_frame = tk.Frame(content_card, bg=self.colors['bg_card'], padx=25, pady=25)
        settings_frame.pack(fill="both", expand=True)

        # Always on Top Toggle
        self.always_on_top = tk.BooleanVar(value=self.config.get('always_on_top', True))

        always_top_cb = tk.Checkbutton(
            settings_frame,
            text="Keep window on top of other applications",
            variable=self.always_on_top,
            command=self.toggle_always_on_top,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            activebackground=self.colors['bg_card'],
            selectcolor=self.colors['bg_card'],
            anchor="w"
        )
        always_top_cb.pack(anchor="w", pady=10)

        # Auto-backup Toggle
        self.auto_backup = tk.BooleanVar(value=self.config.get('auto_backup', True))
        auto_backup_cb = tk.Checkbutton(
            settings_frame,
            text="Automatically create backups when saving data",
            variable=self.auto_backup,
            command=self.toggle_auto_backup,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            activebackground=self.colors['bg_card'],
            selectcolor=self.colors['bg_card'],
            anchor="w"
        )
        auto_backup_cb.pack(anchor="w", pady=10)

        # Backup retention info
        info_frame = tk.Frame(settings_frame, bg=self.colors['bg_card'])
        info_frame.pack(fill="x", pady=20)
        
        tk.Label(
            info_frame,
            text="ℹ️ Auto-backups keep the last 10 backup files",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=self.fonts['small']
        ).pack(anchor="w")

        # Buttons
        button_frame = tk.Frame(settings_frame, bg=self.colors['bg_card'])
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        self.create_modern_button(
            button_frame, 
            "💾 Manual Backup", 
            self.manual_backup,
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            button_frame, 
            "✅ Close", 
            settings_window.destroy,
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        ).pack(side=tk.RIGHT)

    def show_about(self):
        """Show the about dialog"""
        about_window = self.create_dialog("about", "📖 About TimeTracker Pro", "450x350")
        
        # Header
        header_frame = tk.Frame(about_window, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="⏱️ TimeTracker Pro", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['primary'], 
            font=self.fonts['title']
        ).pack()
        
        tk.Label(
            header_frame, 
            text="Professional Time Tracking Application", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_secondary'], 
            font=self.fonts['body']
        ).pack(pady=(5, 0))

        # Main content card
        content_card = tk.Frame(about_window, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        about_frame = tk.Frame(content_card, bg=self.colors['bg_card'], padx=25, pady=25)
        about_frame.pack(fill="both", expand=True)

        # Version and features
        about_text = """Version 1.0

🚀 Features:
• Start/Stop/Pause Timer
• Project Management
• Notes & Descriptions
• Time Entry Management
• Reports & Analytics
• Data Import/Export
• Automatic Backups
• Modern UI Design

🛠️ Built with:
• Python 3.7+
• Tkinter GUI Framework
• JSON Data Storage
• Comprehensive Testing

📁 Data Management:
• Local storage only
• CSV import/export
• Automatic backups
• Data validation

🎨 Modern Design:
• Professional appearance
• Intuitive interface
• Responsive controls
• Hover effects"""

        about_label = tk.Label(
            about_frame,
            text=about_text,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            justify=tk.LEFT
        )
        about_label.pack(anchor="w")

        # Close button
        button_frame = tk.Frame(about_frame, bg=self.colors['bg_card'])
        button_frame.pack(side=tk.BOTTOM, pady=20)
        
        self.create_modern_button(
            button_frame, 
            "✅ Close", 
            about_window.destroy,
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        ).pack()

    def show_project_manager(self):
        """Show the project management dialog"""
        project_window = self.create_dialog("project_manager", "📋 Project Management", "700x500")
        
        # Header
        header_frame = tk.Frame(project_window, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="📋 Project Management", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        ).pack()

        # Main content card
        content_card = tk.Frame(project_window, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        # Projects list
        list_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Listbox with scrollbar
        projects_scrollbar = tk.Scrollbar(list_frame)
        projects_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.projects_listbox = tk.Listbox(
            list_frame,
            font=self.fonts['body'],
            yscrollcommand=projects_scrollbar.set,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.projects_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        projects_scrollbar.config(command=self.projects_listbox.yview)

        # Update projects list
        self.update_projects_listbox()

        # Buttons frame
        buttons_frame = tk.Frame(content_card, bg=self.colors['bg_card'], pady=20)
        buttons_frame.pack()

        self.create_modern_button(
            buttons_frame,
            "➕ Add Project",
            lambda: self.add_edit_project(),
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            buttons_frame,
            "✏️ Edit Project",
            lambda: self.add_edit_project(self.get_selected_project()),
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            buttons_frame,
            "🗑️ Delete Project",
            self.delete_project,
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            buttons_frame,
            "✅ Close",
            project_window.destroy,
            bg_color=self.colors['text_secondary'],
            hover_color=self.colors['text_primary'],
            width=15
        ).pack(side=tk.RIGHT)

    def show_invoice_rates(self):
        """Show the invoice rates dialog"""
        rates_window = self.create_dialog("invoice_rates", "💰 Invoice Rates", "600x500")
        
        # Header
        header_frame = tk.Frame(rates_window, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="💰 Invoice Rates", 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['title']
        ).pack()

        # Main content card
        content_card = tk.Frame(rates_window, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        # Rates list
        list_frame = tk.Frame(content_card, bg=self.colors['bg_card'])
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Listbox with scrollbar
        rates_scrollbar = tk.Scrollbar(list_frame)
        rates_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.rates_listbox = tk.Listbox(
            list_frame,
            font=self.fonts['body'],
            yscrollcommand=rates_scrollbar.set,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.rates_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        rates_scrollbar.config(command=self.rates_listbox.yview)

        # Update rates list
        self.update_rates_listbox()

        # Buttons frame
        buttons_frame = tk.Frame(content_card, bg=self.colors['bg_card'], pady=20)
        buttons_frame.pack()

        self.create_modern_button(
            buttons_frame,
            "➕ Add Rate",
            lambda: self.add_edit_rate(),
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            buttons_frame,
            "✏️ Edit Rate",
            lambda: self.add_edit_rate(self.get_selected_rate()),
            bg_color=self.colors['info'],
            hover_color='#2563EB',
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            buttons_frame,
            "🗑️ Delete Rate",
            self.delete_rate,
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.create_modern_button(
            buttons_frame,
            "✅ Close",
            rates_window.destroy,
            bg_color=self.colors['text_secondary'],
            hover_color=self.colors['text_primary'],
            width=15
        ).pack(side=tk.RIGHT)

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

    def update_project_dropdown(self):
        """Update the project dropdown with current projects"""
        try:
            # Filter only active projects
            active_projects = [p for p in self.projects if p.get('status') == 'Active']
            
            # Create display names
            project_names = [f"{p['name']} ({p['status']}, Invoice: {p['invoice']})" for p in active_projects]
            
            # Update dropdown
            self.project_dropdown['values'] = project_names
            
            # Set current selection if available
            if self.current_project_id:
                current_project = self.get_current_project()
                if current_project and current_project.get('status') == 'Active':
                    current_name = f"{current_project['name']} ({current_project['status']}, Invoice: {current_project['invoice']})"
                    if current_name in project_names:
                        self.project_var.set(current_name)
                        return
            
            # Set first active project if none selected
            if project_names:
                self.project_var.set(project_names[0])
                self.current_project_id = active_projects[0]['id']
                self.project_name.set(active_projects[0]['name'])
        except Exception as e:
            self.log_error(f"Failed to update project dropdown: {e}")

    def on_project_selected(self, event=None):
        """Handle project selection change"""
        try:
            selected = self.project_var.get()
            if not selected:
                return
            
            # Find the selected project
            for project in self.projects:
                project_name = f"{project['name']} ({project['status']}, Invoice: {project['invoice']})"
                if project_name == selected:
                    self.current_project_id = project['id']
                    self.project_name.set(project['name'])
                    break
        except Exception as e:
            self.log_error(f"Failed to handle project selection: {e}")

    def update_projects_listbox(self):
        """Update the projects listbox"""
        try:
            self.projects_listbox.delete(0, tk.END)
            for project in self.projects:
                status_icon = "🟢" if project.get('status') == 'Active' else "🔴"
                invoice_icon = "💰" if project.get('invoice') == 'Yes' else "📝"
                display_text = f"{status_icon} {project['name']} - {project['status']} - {invoice_icon} {project['invoice']}"
                self.projects_listbox.insert(tk.END, display_text)
        except Exception as e:
            self.log_error(f"Failed to update projects listbox: {e}")

    def update_rates_listbox(self):
        """Update the rates listbox"""
        try:
            self.rates_listbox.delete(0, tk.END)
            for project_id, rate_data in self.invoice_rates.items():
                project = self.get_project_by_id(project_id)
                project_name = project['name'] if project else project_id
                display_text = f"{project_name}: {rate_data['rate']} {rate_data['currency']}/hour"
                self.rates_listbox.insert(tk.END, display_text)
        except Exception as e:
            self.log_error(f"Failed to update rates listbox: {e}")

    def get_selected_project(self):
        """Get the selected project from listbox"""
        try:
            selection = self.projects_listbox.curselection()
            if selection:
                return self.projects[selection[0]]
            return None
        except Exception as e:
            self.log_error(f"Failed to get selected project: {e}")
            return None

    def get_selected_rate(self):
        """Get the selected rate from listbox"""
        try:
            selection = self.rates_listbox.curselection()
            if selection:
                project_ids = list(self.invoice_rates.keys())
                if selection[0] < len(project_ids):
                    return project_ids[selection[0]]
            return None
        except Exception as e:
            self.log_error(f"Failed to get selected rate: {e}")
            return None

    def add_edit_project(self, project=None):
        """Add or edit a project"""
        # Create project dialog
        dialog = self.create_dialog("add_edit_project", "✏️ Add/Edit Project" if not project else "✏️ Edit Project", "500x600")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        title = "✏️ Add New Project" if not project else "✏️ Edit Project"
        tk.Label(
            header_frame, 
            text=title, 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['heading']
        ).pack()

        # Main content card
        content_card = tk.Frame(dialog, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        form_frame = tk.Frame(content_card, bg=self.colors['bg_card'], padx=25, pady=25)
        form_frame.pack(fill="both", expand=True)

        # Project fields
        fields = {}
        
        # Project Name
        tk.Label(form_frame, text="Project Name *", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(form_frame, width=50, font=self.fonts['body'], relief="solid", bd=2)
        name_entry.pack(fill="x", pady=(0, 15))
        fields['name'] = name_entry
        
        # Status
        tk.Label(form_frame, text="Status", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
        status_var = tk.StringVar(value="Active")
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=["Active", "Inactive"], state="readonly", font=self.fonts['body'])
        status_combo.pack(fill="x", pady=(0, 15))
        fields['status'] = status_var
        
        # Invoice
        tk.Label(form_frame, text="Invoice", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
        invoice_var = tk.StringVar(value="No")
        invoice_combo = ttk.Combobox(form_frame, textvariable=invoice_var, values=["Yes", "No"], state="readonly", font=self.fonts['body'])
        invoice_combo.pack(fill="x", pady=(0, 15))
        fields['invoice'] = invoice_var
        
        # Description
        tk.Label(form_frame, text="Description", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
        desc_text = tk.Text(form_frame, height=4, font=self.fonts['body'], relief="solid", bd=2, wrap=tk.WORD)
        desc_text.pack(fill="x", pady=(0, 20))
        fields['description'] = desc_text

        # Pre-fill fields if editing
        if project:
            name_entry.insert(0, project.get('name', ''))
            status_var.set(project.get('status', 'Active'))
            invoice_var.set(project.get('invoice', 'No'))
            desc_text.insert("1.0", project.get('description', ''))

        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        button_frame.pack(side=tk.BOTTOM)
        
        self.create_modern_button(
            button_frame,
            "💾 Save",
            lambda: self.save_project(fields, project, dialog),
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=12
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            button_frame,
            "❌ Cancel",
            dialog.destroy,
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=12
        ).pack(side=tk.RIGHT)

    def save_project(self, fields, project=None, dialog=None):
        """Save project data"""
        try:
            name = fields['name'].get().strip()
            if not name:
                messagebox.showerror("Error", "Project name is required!")
                return
            
            project_data = {
                'id': project['id'] if project else f"project_{len(self.projects) + 1}",
                'name': name,
                'status': fields['status'].get(),
                'invoice': fields['invoice'].get(),
                'description': fields['description'].get("1.0", "end-1c").strip()
            }
            
            if project:
                # Update existing project
                for i, p in enumerate(self.projects):
                    if p['id'] == project['id']:
                        self.projects[i] = project_data
                        break
            else:
                # Add new project
                self.projects.append(project_data)
                
                # Create default invoice rate
                self.invoice_rates[project_data['id']] = {
                    'rate': 50.0,
                    'currency': 'USD'
                }
                self.save_invoice_rates()
            
            self.save_projects()
            self.update_project_dropdown()
            
            if hasattr(self, 'projects_listbox'):
                self.update_projects_listbox()
            
            if dialog:
                dialog.destroy()
                
            messagebox.showinfo("Success", "Project saved successfully!")
            
        except Exception as e:
            self.log_error(f"Failed to save project: {e}")
            messagebox.showerror("Error", f"Failed to save project: {e}")

    def delete_project(self):
        """Delete selected project"""
        try:
            project = self.get_selected_project()
            if not project:
                messagebox.showwarning("Warning", "Please select a project to delete.")
                return
            
            if project['id'] == 'default':
                messagebox.showwarning("Warning", "Cannot delete the default project.")
                return
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete project '{project['name']}'?"):
                # Remove project
                self.projects = [p for p in self.projects if p['id'] != project['id']]
                
                # Remove invoice rate
                if project['id'] in self.invoice_rates:
                    del self.invoice_rates[project['id']]
                    self.save_invoice_rates()
                
                # Update current project if it was deleted
                if self.current_project_id == project['id']:
                    self.current_project_id = None
                    self.project_name.set("")
                
                self.save_projects()
                self.update_project_dropdown()
                self.update_projects_listbox()
                
                messagebox.showinfo("Success", "Project deleted successfully!")
                
        except Exception as e:
            self.log_error(f"Failed to delete project: {e}")
            messagebox.showerror("Error", f"Failed to delete project: {e}")

    def add_edit_rate(self, project_id=None):
        """Add or edit invoice rate"""
        # Create rate dialog
        dialog = self.create_dialog("add_edit_rate", "💰 Add/Edit Invoice Rate" if not project_id else "💰 Edit Invoice Rate", "400x400")
        
        # Header
        header_frame = tk.Frame(dialog, bg=self.colors['bg_primary'], pady=20)
        header_frame.pack(fill="x")
        
        title = "💰 Add New Invoice Rate" if not project_id else "💰 Edit Invoice Rate"
        tk.Label(
            header_frame, 
            text=title, 
            bg=self.colors['bg_primary'], 
            fg=self.colors['text_primary'], 
            font=self.fonts['heading']
        ).pack()

        # Main content card
        content_card = tk.Frame(dialog, bg=self.colors['bg_card'], relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, padx=25, pady=25)

        form_frame = tk.Frame(content_card, bg=self.colors['bg_card'], padx=25, pady=25)
        form_frame.pack(fill="both", expand=True)

        # Project selection (if adding new)
        if not project_id:
            tk.Label(form_frame, text="Project", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
            project_var = tk.StringVar()
            project_combo = ttk.Combobox(form_frame, textvariable=project_var, state="readonly", font=self.fonts['body'])
            project_combo['values'] = [p['name'] for p in self.projects]
            project_combo.pack(fill="x", pady=(0, 15))
            
            if self.projects:
                project_combo.set(self.projects[0]['name'])
        else:
            project_var = None

        # Rate
        tk.Label(form_frame, text="Hourly Rate *", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
        rate_entry = tk.Entry(form_frame, width=20, font=self.fonts['body'], relief="solid", bd=2)
        rate_entry.pack(fill="x", pady=(0, 15))
        
        # Currency
        tk.Label(form_frame, text="Currency", bg=self.colors['bg_card'], fg=self.colors['text_secondary'], font=self.fonts['body']).pack(anchor="w", pady=(0, 5))
        currency_var = tk.StringVar(value="USD")
        currency_combo = ttk.Combobox(form_frame, textvariable=currency_var, values=["USD", "EUR", "GBP", "SEK", "NOK", "DKK"], state="readonly", font=self.fonts['body'])
        currency_combo.pack(fill="x", pady=(0, 20))

        # Pre-fill fields if editing
        if project_id:
            rate_data = self.invoice_rates.get(project_id, {})
            rate_entry.insert(0, str(rate_data.get('rate', 50.0)))
            currency_var.set(rate_data.get('currency', 'USD'))

        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        button_frame.pack(side=tk.BOTTOM)
        
        self.create_modern_button(
            button_frame,
            "💾 Save",
            lambda: self.save_rate(project_var, rate_entry, currency_var, project_id, dialog),
            bg_color=self.colors['secondary'],
            hover_color=self.colors['secondary_hover'],
            width=12
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_modern_button(
            button_frame,
            "❌ Cancel",
            dialog.destroy,
            bg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            width=12
        ).pack(side=tk.RIGHT)

    def save_rate(self, project_var, rate_entry, currency_var, project_id=None, dialog=None):
        """Save invoice rate data"""
        try:
            rate_str = rate_entry.get().strip()
            if not rate_str:
                messagebox.showerror("Error", "Rate is required!")
                return
            
            try:
                rate = float(rate_str)
                if rate < 0:
                    messagebox.showerror("Error", "Rate must be positive!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Rate must be a valid number!")
                return
            
            currency = currency_var.get()
            
            if not project_id:
                # Find project by name
                project_name = project_var.get()
                project = None
                for p in self.projects:
                    if p['name'] == project_name:
                        project = p
                        break
                
                if not project:
                    messagebox.showerror("Error", "Please select a valid project!")
                    return
                
                project_id = project['id']
            
            # Save rate
            self.invoice_rates[project_id] = {
                'rate': rate,
                'currency': currency
            }
            
            self.save_invoice_rates()
            
            if hasattr(self, 'rates_listbox'):
                self.update_rates_listbox()
            
            if dialog:
                dialog.destroy()
                
            messagebox.showinfo("Success", "Invoice rate saved successfully!")
            
        except Exception as e:
            self.log_error(f"Failed to save invoice rate: {e}")
            messagebox.showerror("Error", f"Failed to save invoice rate: {e}")

    def delete_rate(self):
        """Delete selected invoice rate"""
        try:
            project_id = self.get_selected_rate()
            if not project_id:
                messagebox.showwarning("Warning", "Please select a rate to delete.")
                return
            
            project = self.get_project_by_id(project_id)
            project_name = project['name'] if project else project_id
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the invoice rate for '{project_name}'?"):
                del self.invoice_rates[project_id]
                self.save_invoice_rates()
                self.update_rates_listbox()
                messagebox.showinfo("Success", "Invoice rate deleted successfully!")
                
        except Exception as e:
            self.log_error(f"Failed to delete invoice rate: {e}")
            messagebox.showerror("Error", f"Failed to delete invoice rate: {e}")

    def mark_as_invoiced(self):
        """Mark selected time entries as invoiced"""
        try:
            # Get the current view_entries window
            entries_window = None
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel) and widget.title() == "📋 View & Edit Entries":
                    entries_window = widget
                    break
            else:
                messagebox.showwarning("Warning", "Please open the View Entries window first.")
                return
            
            # Find the listbox in the entries window
            listbox = None
            for widget in entries_window.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Listbox):
                                    listbox = grandchild
                                    break
            
            if not listbox:
                messagebox.showwarning("Warning", "Could not find entries list.")
                return
            
            # Get selection
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an entry to mark as invoiced.")
                return
            
            # Load data and update
            data = self.load_data()
            updated_count = 0
            
            if len(selection) == 1:
                # Single selection - toggle status
                filtered_index = selection[0]
                
                # We need to find the actual entry in the filtered view
                # Since we can't directly access the filtered_data from here,
                # we'll work with the current listbox content
                if filtered_index < listbox.size():
                    # Get the entry text to extract project and time info
                    entry_text = listbox.get(filtered_index)
                    # Parse the entry to find the original entry in data
                    # This is a fallback approach - ideally we'd have access to filtered_data
                    for i, entry in enumerate(data):
                        if (entry.get('project', '') in entry_text and 
                            entry.get('start_time', '') in entry_text):
                            current_status = entry.get('invoiced', 'No')
                            new_status = 'Yes' if current_status == 'No' else 'No'
                            
                            entry['invoiced'] = new_status
                            updated_count = 1
                            
                            status_text = "invoiced" if new_status == 'Yes' else "not invoiced"
                            self.update_status(f"Entry marked as {status_text}")
                            break
            else:
                # Multiple selection - toggle status for each entry
                count = len(selection)
                if messagebox.askyesno("Confirm Bulk Update", f"Toggle invoiced status for {count} selected entries?"):
                    # For multiple selection, we'll need to find each entry
                    for filtered_index in selection:
                        if filtered_index < listbox.size():
                            entry_text = listbox.get(filtered_index)
                            for i, entry in enumerate(data):
                                if (entry.get('project', '') in entry_text and 
                                    entry.get('start_time', '') in entry_text):
                                    # Toggle the status: Yes -> No, No -> Yes
                                    current_status = entry.get('invoiced', 'No')
                                    new_status = 'Yes' if current_status == 'No' else 'No'
                                    data[i]['invoiced'] = new_status
                                    updated_count += 1
                                    break
                    
                    self.update_status(f"{updated_count} entries status toggled")
                else:
                    return
            
            if updated_count > 0:
                # Save changes
                self.save_data(data)
                
                # Refresh the listbox content by triggering a filter refresh
                # We'll need to find and call the apply_filter function
                # For now, let's just refresh the entire window
                entries_window.destroy()
                self.view_entries()
                
        except Exception as e:
            self.log_error(f"Failed to mark as invoiced: {e}")
            messagebox.showerror("Error", f"Failed to mark as invoiced: {e}")

    def refresh_entries_listbox(self, listbox, data=None):
        """Refresh the entries listbox with updated data"""
        try:
            # Always load fresh data from file to ensure consistency
            if data is None:
                data = self.load_data()
            
            # Clear current entries
            listbox.delete(0, tk.END)
            
            def truncate(text, length=40):
                text = text or ""
                return (text[:length] + "…") if len(text) > length else text
            
            # Repopulate with updated data
            for i, entry in enumerate(data):
                proj = entry.get('project', '')
                st = entry.get('start_time', '')
                et = entry.get('stop_time', '')
                dur = entry.get('duration') or self.format_seconds(entry.get('duration_seconds', 0))
                memo_snippet = truncate(entry.get('memo', ''), 30)
                invoiced_status = entry.get('invoiced', 'No')
                invoiced_icon = "💰" if invoiced_status == "Yes" else "📝"
                listbox.insert(tk.END, f"{i+1}. {proj} | {st} - {et} | {dur} | {invoiced_icon} {invoiced_status} | 📝 {memo_snippet}")
                
        except Exception as e:
            self.log_error(f"Failed to refresh entries listbox: {e}")

    def clear_date_filters(self, from_date_var, to_date_var):
        """Clear date filters and refresh the listbox"""
        from_date_var.set("")
        to_date_var.set("")
        # Re-apply filter to refresh the listbox
        # This will be handled by the apply_filter function when called

    def apply_reports_date_filter(self, data, from_date_var, to_date_var):
        """Apply date filter to reports data"""
        try:
            from_date = from_date_var.get().strip()
            to_date = to_date_var.get().strip()
            
            # Check if dates are actually set (not placeholder text)
            if from_date and to_date and from_date != "YYYY-MM-DD" and to_date != "YYYY-MM-DD":
                try:
                    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
                    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
                    
                    # Validate date range
                    if from_date_obj > to_date_obj:
                        messagebox.showerror("Invalid Date Range", "From date cannot be after To date")
                        return
                    
                    filtered_data = []
                    for entry in data:
                        try:
                            entry_date = datetime.strptime(entry.get('start_time', ''), "%Y-%m-%d %H:%M:%S").date()
                            if from_date_obj <= entry_date <= to_date_obj:
                                filtered_data.append(entry)
                        except (ValueError, TypeError):
                            # Skip entries with invalid dates
                            continue
                    
                    # Show filtered reports
                    self.show_filtered_reports(filtered_data, from_date, to_date)
                    
                except ValueError as e:
                    messagebox.showerror("Invalid Date Format", f"Please ensure dates are in YYYY-MM-DD format.\n\nError: {str(e)}")
                    return
            else:
                # No valid dates, show all data
                self.show_reports()
                
        except Exception as e:
            self.log_error(f"Failed to apply reports date filter: {e}")
            messagebox.showerror("Error", f"Failed to apply reports date filter: {e}")

    def show_filtered_reports(self, filtered_data, from_date, to_date):
        """Show reports with filtered data"""
        try:
            # Create a new reports window with filtered data
            reports_window = self.create_dialog("filtered_reports", f"📊 Time Tracking Reports (Filtered: {from_date} to {to_date})", "750x550")
            
            if not filtered_data:
                # No filtered data message
                no_data_frame = tk.Frame(reports_window, bg=self.colors['bg_primary'])
                no_data_frame.pack(expand=True, fill="both")
                
                tk.Label(
                    no_data_frame, 
                    text="📊 No Data in Date Range", 
                    bg=self.colors['bg_primary'], 
                    fg=self.colors['text_primary'], 
                    font=self.fonts['title']
                ).pack(expand=True)
                
                tk.Label(
                    no_data_frame, 
                    text=f"No entries found between {from_date} and {to_date}", 
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
                text=f"📊 Analytics & Reports (Filtered: {from_date} to {to_date})", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_primary'], 
                font=self.fonts['title']
            ).pack()
            
            # Show filtered data count
            tk.Label(
                header_frame, 
                text=f"Showing {len(filtered_data)} entries out of {len(self.load_data())} total", 
                bg=self.colors['bg_primary'], 
                fg=self.colors['text_secondary'], 
                font=self.fonts['body']
            ).pack(pady=(5, 0))
            
            # Create notebook for different report types
            notebook = ttk.Notebook(reports_window)
            notebook.pack(fill="both", expand=True, padx=25, pady=25)
            
            # Summary Report Tab
            summary_frame = tk.Frame(notebook, bg=self.colors['bg_card'])
            notebook.add(summary_frame, text="📈 Summary")
            
            # Calculate summary statistics for filtered data
            total_entries = len(filtered_data)
            total_seconds = sum(entry.get('duration_seconds', 0) for entry in filtered_data)
            total_hours = total_seconds / 3600
            
            # Invoiced status breakdown
            invoiced_seconds = sum(entry.get('duration_seconds', 0) for entry in filtered_data if entry.get('invoiced') == 'Yes')
            not_invoiced_seconds = total_seconds - invoiced_seconds
            invoiced_hours = invoiced_seconds / 3600
            not_invoiced_hours = not_invoiced_seconds / 3600
            
            # Project breakdown
            project_totals = {}
            for entry in filtered_data:
                project = entry.get('project', 'Unknown')
                duration = entry.get('duration_seconds', 0)
                project_totals[project] = project_totals.get(project, 0) + duration
            
            # Display summary
            summary_text = f"""📊 FILTERED TIME TRACKING SUMMARY
Date Range: {from_date} to {to_date}

Total Entries: {total_entries}
Total Time: {self.format_seconds(total_seconds)} ({total_hours:.2f} hours)

💰 INVOICING STATUS:
• Invoiced: {self.format_seconds(invoiced_seconds)} ({invoiced_hours:.2f} hours)
• Not Invoiced: {self.format_seconds(not_invoiced_seconds)} ({not_invoiced_hours:.2f} hours)

📋 TOP PROJECTS:
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
            
            # Export button for filtered data
            export_frame = tk.Frame(reports_window, bg=self.colors['bg_primary'], pady=10)
            export_frame.pack()
            
            self.create_modern_button(
                export_frame, 
                "📁 Export Filtered Report", 
                lambda: self.export_to_csv(filtered_data),
                bg_color=self.colors['accent'],
                hover_color=self.colors['accent_hover'],
                width=20
            ).pack()
            
        except Exception as e:
            self.log_error(f"Failed to show filtered reports: {e}")
            messagebox.showerror("Error", f"Failed to show filtered reports: {e}")

    def clear_reports_date_filters(self, from_date_var, to_date_var):
        """Clear date filters for reports"""
        from_date_var.set("")
        to_date_var.set("")

    def create_dialog(self, dialog_type, title, geometry, modal=True):
        """Create a properly positioned dialog with single instance enforcement"""
        # Check if dialog is already open
        if dialog_type in self.open_dialogs and self.open_dialogs[dialog_type].winfo_exists():
            # Bring existing dialog to front
            self.open_dialogs[dialog_type].lift()
            self.open_dialogs[dialog_type].focus_force()
            return self.open_dialogs[dialog_type]
        
        # Create new dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry(geometry)
        dialog.configure(bg=self.colors['bg_primary'])
        
        # Force dialog to appear in front - this is critical!
        dialog.lift()
        dialog.attributes('-topmost', True)
        
        # Position dialog relative to main window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (int(geometry.split('x')[0]) // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (int(geometry.split('x')[1]) // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Make dialog modal if requested - this should keep it in front
        if modal:
            dialog.transient(self.root)
            dialog.grab_set()
            dialog.focus_force()
        
        # Track the dialog
        self.open_dialogs[dialog_type] = dialog
        
        # Handle dialog close
        def on_dialog_close():
            if dialog_type in self.open_dialogs:
                del self.open_dialogs[dialog_type]
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        
        # Final positioning and focus - ensure it's visible
        dialog.lift()
        dialog.focus_force()
        
        return dialog

    def close_dialog(self, dialog_type):
        """Close a specific dialog if it's open"""
        if dialog_type in self.open_dialogs and self.open_dialogs[dialog_type].winfo_exists():
            self.open_dialogs[dialog_type].destroy()
            del self.open_dialogs[dialog_type]

    def close_all_dialogs(self):
        """Close all open dialogs"""
        for dialog_type in list(self.open_dialogs.keys()):
            self.close_dialog(dialog_type)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
