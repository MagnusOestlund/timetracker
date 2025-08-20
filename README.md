# ⏱️ TimeTracker Pro

A professional desktop time tracking application built with Python and Tkinter. Track your work hours, manage projects, and generate detailed reports with automatic backup and data export capabilities.

![TimeTracker Pro](https://img.shields.io/badge/version-1.0-blue) ![Python](https://img.shields.io/badge/python-3.7+-green) ![License](https://img.shields.io/badge/license-MIT-blue) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## 🚀 Features

### ⏲️ **Core Time Tracking**
- **Start/Stop/Pause Timer** - Full control over your time tracking sessions
- **Project Management** - Track time for different projects with custom names
- **Memo/Notes** - Add detailed notes about what you were working on
- **Real-time Display** - Live elapsed time counter with HH:MM:SS format
- **Session Management** - Pause and resume functionality for interruptions

### 🎨 **Modern Professional UI**
- **Menu Bar Navigation** - Organized File, View, Tools, and Help menus
- **Quick Actions Panel** - Easy access to frequently used functions
- **Card-Based Layout** - Modern, clean interface with visual hierarchy
- **Professional Color Scheme** - Indigo, emerald, and amber accent colors
- **Hover Effects** - Interactive buttons with smooth color transitions
- **Always-on-Top Option** - Keep the window visible while working

### 📊 **Reports & Analytics**
- **Summary Reports** - Total time, entry counts, and project breakdowns
- **Weekly Analysis** - Last 4 weeks of time tracking data
- **Top Projects** - See which projects consume the most time
- **Detailed Statistics** - Hours worked, entries logged, and performance metrics
- **Export Reports** - Save analytics data to CSV format

### 💾 **Data Management**
- **Automatic Backup** - Configurable auto-backup with retention policy
- **Manual Backup** - On-demand backup creation with timestamps
- **Data Recovery** - Restore from any backup with pre-restore safety backups
- **CSV Export/Import** - Full data portability and integration capabilities
- **JSON Storage** - Human-readable data format for easy access

### ⚙️ **Advanced Features**
- **Dedicated Settings Dialog** - Comprehensive configuration management
- **About Dialog** - Application information and feature overview
- **Data Validation** - Input validation and error handling
- **Edit Entries** - Modify existing time entries with full validation
- **Delete Entries** - Remove unwanted entries with confirmation dialogs
- **Status Updates** - Real-time feedback with icons and color coding
- **Professional Typography** - Segoe UI font family for Windows consistency

## 📋 Requirements

- **Python 3.7+** (with tkinter support)
- **Windows 10/11** (primary platform)
- **~10MB disk space** for application and data
- **Minimal RAM usage** (~50MB when running)

## 🛠️ Installation

### Option 1: Run from Source
```bash
# Clone the repository
git clone https://github.com/MagnusOestlund/timetracker.git
cd timetracker

# Run the application
python main.py
```

### Option 2: Build Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Run the automated build script
build.bat
# OR
.\build.ps1

# Find your executable in the dist/ folder
```

## 🎯 Quick Start

1. **Launch the application** by running `main.py` or the executable
2. **Enter a project name** in the "Project Details" section
3. **Add notes** (optional) in the description field
4. **Click "▶ Start"** to begin tracking time
5. **Use "⏸ Pause"** to temporarily stop without ending the session
6. **Click "⏹ Stop"** when finished to save the entry

## 📖 User Guide

### Navigation
The application features a **professional menu bar** with organized sections:
- **📁 File**: Export/Import data, create/restore backups, exit
- **👁️ View**: Access time entries and reports
- **🛠️ Tools**: Data management and settings
- **❓ Help**: About dialog with application information

### Quick Actions Panel
The main interface includes a **Quick Actions** section with:
- **📋 View Entries**: See and edit your time tracking history
- **📊 Reports**: Generate analytics and export reports
- **📁 Data Tools**: Import/export and backup management
- **⚙️ Settings**: Configure application preferences
- **💾 Quick Backup**: Create instant data backups
- **❓ Help**: Access application information

### Starting a Time Tracking Session
1. Enter your project name in the **Project Details** card (required)
2. Add optional notes about your work in the description field
3. Click the **▶ Start** button in the Timer Controls
4. The timer will begin counting and display elapsed time

### Managing Active Sessions
- **⏸ Pause**: Temporarily stop the timer without ending the session
- **▶ Resume**: Continue timing from where you paused
- **⏹ Stop**: End the session and save the entry to your data file

### Viewing and Editing Entries
1. Use **📋 View Entries** from Quick Actions or View menu
2. Select any entry from the modern list interface
3. Click **✏️ Edit Selected** to modify details
4. Update project names, times, durations, or memos
5. Changes are validated and saved automatically

### Generating Reports
1. Click **📊 Reports** from Quick Actions or View menu
2. View the **📈 Summary** tab for overall statistics
3. Check the **📅 Weekly** tab for recent activity breakdown
4. Use **📁 Export Report** to save analytics data to CSV

### Data Management
Access through **📁 Data Tools** or the File menu:
1. **📤 Export to CSV**: Save your data in spreadsheet format
2. **📥 Import from CSV**: Add data from external sources
3. **💾 Create Backup**: Manual backup of your current data
4. **🔄 Restore from Backup**: Recover from previous backups

### Settings & Configuration
Access via **⚙️ Settings** button or Tools menu:
- **Keep window on top**: Toggle always-on-top behavior
- **Automatically create backups**: Enable/disable automatic backups
- **Manual Backup**: Create backups on-demand
- Settings are saved automatically and persist between sessions

## 📁 File Structure

```
TimeTracker/
├── main.py                 # Main application file
├── config.json            # Application configuration (auto-created)
├── work_hours.json        # Time tracking data (auto-created)
├── backups/               # Automatic and manual backups
│   ├── backup_YYYYMMDD_HHMMSS.json
│   └── manual_backup_YYYYMMDD_HHMMSS.json
├── test_timetracker.py    # Comprehensive test suite
├── build.bat              # Windows build script
├── build.ps1              # PowerShell build script
├── run_tests.bat          # Test runner (Windows)
├── run_tests.ps1          # Test runner (PowerShell)
├── requirements.txt       # Dependencies documentation
├── TESTING_GUIDE.md       # Testing instructions
├── manual_build.md        # Manual build guide
└── README.md             # This file
```

## 🔧 Development

### Running Tests
```bash
# Run all tests
python test_timetracker.py

# Or use the test runners
run_tests.bat        # Windows
.\run_tests.ps1      # PowerShell

# Run specific test categories
python -m unittest test_timetracker.TestTimeTracker -v
python -m unittest test_timetracker.TestTimeTrackerIntegration -v
```

### Test Coverage
- **28 comprehensive tests** covering all functionality
- **Unit tests** for individual components and UI elements
- **Integration tests** for complete workflows
- **Performance tests** for large datasets
- **Edge case handling** and error conditions
- **UI structure validation** for menu bar and quick actions

### Building Executables
The application includes automated build scripts that handle:
- **Multiple build methods** (PyInstaller, cx_Freeze)
- **SSL certificate issues** in corporate environments
- **Fallback options** if primary tools fail
- **Clean output** with success/failure reporting

## 📊 Data Format

### Time Entry Structure
```json
{
  "project": "Project Name",
  "memo": "Description of work done",
  "start_time": "2024-01-15 09:00:00",
  "stop_time": "2024-01-15 10:30:00",
  "duration": "01:30:00",
  "duration_seconds": 5400
}
```

### Configuration Structure
```json
{
  "always_on_top": true,
  "auto_backup": true,
  "backup_interval_days": 7,
  "theme": "default"
}
```

## 🛡️ Data Safety

### Automatic Backups
- **Triggered** on every data save operation
- **Retention** policy keeps last 10 backups
- **Timestamped** files for easy identification
- **Configurable** via settings dialog

### Manual Backups
- **On-demand** backup creation via Quick Actions or File menu
- **Timestamped** with "manual_backup_" prefix
- **No automatic cleanup** - retained indefinitely
- **Status feedback** confirms successful creation

### Data Recovery
- **Restore from any backup** with modern file selection dialog
- **Pre-restore backup** created automatically for safety
- **Validation** ensures data integrity during restore
- **Confirmation dialogs** prevent accidental data loss

## 🎨 Customization

### Modern UI Design
The application features a professional color scheme:
- **Background Primary**: Light gray (`#FAFBFC`)
- **Background Secondary**: Off-white (`#F8F9FA`)
- **Card Background**: Pure white (`#FFFFFF`)
- **Primary**: Indigo (`#4F46E5`)
- **Secondary**: Emerald (`#10B981`)
- **Accent**: Amber (`#F59E0B`)
- **Danger**: Red (`#EF4444`)
- **Text Primary**: Dark gray (`#111827`)

### Typography
- **Title**: Segoe UI 16pt Bold
- **Heading**: Segoe UI 12pt Bold
- **Body**: Segoe UI 11pt
- **Button**: Segoe UI 10pt Bold
- **Timer**: Segoe UI 14pt Bold

### Extending Functionality
The modular design makes it easy to add:
- **New report types** in the `show_reports()` method
- **Additional export formats** by extending export methods
- **Custom validation** in the `validate_time_format()` method
- **New configuration options** in the settings dialog
- **Additional UI cards** using the `create_card_frame()` method

## 🐛 Troubleshooting

### Common Issues

#### **Application Won't Start**
- Verify Python 3.7+ is installed
- Check that tkinter is available: `python -c "import tkinter"`
- Ensure you're in the correct directory

#### **Timer Not Working**
- Verify project name is entered (required field)
- Check for error messages in the status bar (⚠️ prefix)
- Restart the application if timer appears stuck

#### **Data Not Saving**
- Check file permissions in the application directory
- Verify disk space is available
- Look for error messages in the status bar

#### **Build Failures**
- Run build scripts as administrator
- Check internet connectivity for package downloads
- Try alternative build methods (cx_Freeze if PyInstaller fails)

### Getting Help
1. Check the **status bar** for error messages (⚠️ icon)
2. Use the **❓ Help** button or menu for application information
3. Review the **TESTING_GUIDE.md** for detailed troubleshooting
4. Run the **test suite** to verify functionality
5. Check **file permissions** and disk space

## 📈 Performance

### Benchmarks
- **Startup time**: <2 seconds
- **Data loading**: 1000+ entries in <1 second
- **Memory usage**: ~50MB typical, ~100MB with large datasets
- **File operations**: Efficient JSON handling with compression
- **UI responsiveness**: Real-time updates with minimal CPU usage

### Scalability
- **Tested with 1000+ entries** without performance degradation
- **Efficient data structures** for fast searching and filtering
- **Lazy loading** for large datasets in reports
- **Automatic cleanup** of old backup files

## 🔒 Security

### Data Protection
- **Local storage only** - no cloud or network transmission
- **File permissions** respect system security settings
- **Backup encryption** (manual process if required)
- **No sensitive data collection** - only project time tracking

### Privacy
- **No telemetry** or usage tracking
- **No internet connectivity** required
- **Offline operation** for complete privacy
- **User-controlled data** with full export capabilities

## 🤝 Contributing

### Development Setup
1. **Fork** the repository
2. **Clone** your fork locally
3. **Run tests** to verify setup: `python test_timetracker.py`
4. **Make changes** with appropriate test coverage
5. **Submit pull request** with clear description

### Code Style
- **PEP 8** compliance for Python code
- **Descriptive variable names** and function documentation
- **Comprehensive error handling** with user-friendly messages
- **Test coverage** for new functionality
- **Modern UI patterns** following the established design system

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Python Software Foundation** for the excellent Python language
- **Tkinter team** for the robust GUI framework
- **Contributors** who help improve the application
- **Users** who provide feedback and feature requests

## 📞 Support

### Documentation
- **README.md** - This comprehensive guide
- **TESTING_GUIDE.md** - Detailed testing instructions
- **manual_build.md** - Step-by-step build process

### Community
- **Issues**: Report bugs or request features via GitHub issues
- **Discussions**: Share usage tips and get help from the community
- **Pull Requests**: Contribute improvements and new features

---

**TimeTracker Pro** - Professional time tracking made simple. Track your productivity, analyze your work patterns, and take control of your time management with this powerful, privacy-focused desktop application featuring a modern, intuitive interface.

*Built with ❤️ using Python and Tkinter* 