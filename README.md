# ⏱️ TimeTracker Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional time tracking application built with Python and Tkinter, designed for freelancers, consultants, and professionals who need to track time spent on projects and generate detailed reports.

## 🚀 Features

### **Core Time Tracking**
- **Start/Stop/Pause Timer** - Simple timer controls with pause/resume functionality
- **Project Management** - Create, edit, and manage multiple projects with status tracking
- **Notes & Descriptions** - Add detailed notes for each time entry
- **Automatic Duration Calculation** - Precise time tracking with HH:MM:SS format

### **Advanced Project Management**
- **Project Status** - Active/Inactive project management
- **Invoice Flags** - Mark projects as billable or non-billable
- **Project Descriptions** - Detailed project information and notes
- **Project Selection** - Easy switching between multiple projects

### **Invoice & Billing Features**
- **Invoice Rates** - Set hourly rates per project with currency support
- **Invoiced Status Tracking** - Mark time entries as invoiced or pending
- **Bulk Operations** - Select multiple entries for bulk status updates
- **Export for Billing** - Generate CSV reports for client invoicing

### **Data Management & Reports**
- **Time Entries View** - Comprehensive list with filtering and editing
- **Date Range Filtering** - Filter entries by specific date ranges
- **Status Filtering** - Filter by invoiced status (All/Invoiced/Not Invoiced)
- **Multiple Selection** - Select multiple entries for bulk operations
- **CSV Import/Export** - Import existing data or export for analysis

### **Analytics & Reporting**
- **Summary Reports** - Overview of total time, projects, and invoicing status
- **Weekly Breakdown** - Time tracking analysis by week
- **Invoicing Reports** - Detailed breakdown of billable vs. non-billable time
- **Project Analytics** - Time distribution across projects
- **Filtered Reports** - Date-specific analytics and insights

### **Data Security & Backup**
- **Automatic Backups** - Configurable auto-backup system
- **Manual Backups** - Create backups on demand
- **Backup Restoration** - Restore data from previous backups
- **Data Validation** - Comprehensive error checking and validation

### **Modern User Interface**
- **Professional Design** - Modern color palette and typography
- **Responsive Layout** - Scrollable interface for all content areas
- **Intuitive Navigation** - Menu-based organization with quick access
- **Date Picker Widgets** - User-friendly calendar selection for date filtering
- **Hover Effects** - Interactive buttons with visual feedback

## 🛠️ Installation

### **Option 1: Download Pre-built Executable (Recommended)**

1. **Download the latest release** from [GitHub Releases](https://github.com/MagnusOestlund/timetracker/releases)
2. **Extract the ZIP file** to your desired location
3. **Run `Run-TimeTracker.bat`** (Windows) to start the application
4. **No Python installation required!**

### **Option 2: Run from Source**

#### **Prerequisites**
- Python 3.7 or higher
- Tkinter (usually included with Python)

#### **Installation Steps**
```bash
# Clone the repository
git clone https://github.com/MagnusOestlund/timetracker.git
cd timetracker

# Install dependencies (if any)
pip install -r requirements.txt

# Run the application
python main.py
```

## 📖 User Guide

### **Getting Started**
1. **Launch the application** - The main window will open with project selection
2. **Select or create a project** - Choose from existing projects or create a new one
3. **Add project details** - Enter project name, status, and description
4. **Start tracking time** - Click "▶ Start" to begin timing
5. **Add notes** - Use the memo field to describe what you're working on
6. **Stop when done** - Click "⏹ Stop" to end the session

### **Project Management**
- **Create Projects**: Tools → Project Management → Add Project
- **Set Status**: Mark projects as Active or Inactive
- **Invoice Flags**: Set whether projects should be invoiced
- **Edit Projects**: Modify existing project details
- **Delete Projects**: Remove unused projects (with confirmation)

### **Invoice Rates**
- **Set Hourly Rates**: Tools → Invoice Rates → Add Rate
- **Currency Support**: USD, EUR, GBP, SEK, NOK, DKK
- **Project-Specific Rates**: Different rates for different projects
- **Rate Management**: Edit or delete rates as needed

### **Time Entry Management**
- **View Entries**: View → Time Entries
- **Date Filtering**: Use From/To date pickers to filter entries
- **Status Filtering**: Filter by invoiced status
- **Multiple Selection**: Ctrl+Click or Shift+Click to select multiple entries
- **Bulk Operations**: Edit, delete, or toggle invoiced status for multiple entries

### **Reports & Analytics**
- **Summary Reports**: View → Reports & Analytics → Summary tab
- **Weekly Breakdown**: View → Reports & Analytics → Weekly tab
- **Invoicing Reports**: View → Reports & Analytics → Invoicing tab
- **Date Filtering**: Apply date ranges to reports
- **Export Reports**: Download filtered data as CSV

### **Data Management**
- **Import CSV**: File → Import from CSV
- **Export CSV**: File → Export to CSV
- **Create Backups**: File → Create Backup or Tools → Settings
- **Restore Backups**: File → Restore from Backup
- **Auto-Backup**: Configure automatic backup frequency

## ⚙️ Settings & Configuration

### **Application Settings**
- **Always on Top**: Keep window above other applications
- **Auto-Backup**: Automatically create backups when saving
- **Backup Retention**: Keep last 10 backup files
- **Theme**: Choose application appearance

### **Data Files**
- **work_hours.json**: Time tracking data
- **projects.json**: Project management data
- **invoice_rates.json**: Billing rates and currencies
- **config.json**: Application configuration
- **backups/**: Backup file directory

## 🧪 Testing

The application includes a comprehensive test suite with **43 tests** covering:

- **Core Functionality**: Timer operations, data management
- **UI Components**: Menu creation, button functionality
- **Data Validation**: Date parsing, time format validation
- **Project Management**: CRUD operations, status tracking
- **Date Filtering**: Range validation, error handling
- **Invoiced Status**: Toggle functionality, multiple selection
- **Error Handling**: Edge cases, invalid input handling

### **Run Tests**
```bash
# Run all tests
python -m unittest test_timetracker.py -v

# Run specific test class
python -m unittest test_timetracker.TestTimeTracker -v
```

## 🎨 Modern UI Design

### **Color Palette**
- **Primary**: Indigo (#4F46E5) - Main actions and highlights
- **Secondary**: Emerald (#10B981) - Success states and confirmations
- **Accent**: Amber (#F59E0B) - Warnings and special actions
- **Danger**: Red (#EF4444) - Destructive actions
- **Background**: Light gray (#FAFBFC) - Clean, professional appearance

### **Typography**
- **Title**: Segoe UI 16pt Bold - Main headings
- **Heading**: Segoe UI 12pt Bold - Section headers
- **Body**: Segoe UI 11pt - Regular text
- **Button**: Segoe UI 10pt Bold - Action buttons
- **Small**: Segoe UI 9pt - Secondary information

### **Layout Features**
- **Card-based Design**: Clean, organized content sections
- **Responsive Scrolling**: All content areas are scrollable
- **Hover Effects**: Interactive feedback on buttons
- **Consistent Spacing**: Professional padding and margins
- **Modern Icons**: Emoji-based visual indicators

## 🔧 Development

### **Project Structure**
```
timetracker/
├── main.py                 # Main application file
├── test_timetracker.py     # Comprehensive test suite
├── README.md              # This documentation
├── requirements.txt       # Python dependencies
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       └── build-release.yml
└── data/                 # Application data files
    ├── work_hours.json
    ├── projects.json
    ├── invoice_rates.json
    └── config.json
```

### **Key Classes**
- **`TimeTrackerApp`**: Main application class with UI and logic
- **`DatePicker`**: Custom date selection widget with calendar popup
- **Test Classes**: Comprehensive testing for all functionality

### **Building Executables**
The project includes automated build workflows:

1. **GitHub Actions**: Automatic builds on releases
2. **Manual Build Script**: `manual_build_release.py` for local builds
3. **Multiple Build Tools**: PyInstaller and cx_Freeze support

## 🚀 Recent Updates

### **Version 1.0 - Current Release**
- ✅ **Date Filtering System** - Comprehensive date range filtering for entries and reports
- ✅ **DatePicker Widget** - User-friendly calendar popup for date selection
- ✅ **Enhanced Reports** - Filtered reports with date-specific analytics
- ✅ **Multiple Selection** - Bulk operations for time entries
- ✅ **Invoiced Status Toggle** - Smart toggle between Yes/No states
- ✅ **Scrollbar Improvements** - Fixed scrollbar conflicts and mousewheel handling
- ✅ **Comprehensive Testing** - 43 tests covering all major functionality
- ✅ **Error Handling** - Robust error handling and user feedback
- ✅ **Modern UI** - Professional appearance with hover effects

### **Previous Major Features**
- **Project Management System** - Full CRUD operations for projects
- **Invoice Rates Management** - Hourly rates with currency support
- **Data Import/Export** - CSV support for data migration
- **Automatic Backups** - Configurable backup system
- **Modern Interface** - Professional design overhaul

## 🐛 Troubleshooting

### **Common Issues**

#### **Application Won't Start**
- Ensure Python 3.7+ is installed
- Check that Tkinter is available
- Verify all required files are present

#### **Data Not Saving**
- Check file permissions in the application directory
- Verify disk space is available
- Check for antivirus interference

#### **Date Filtering Errors**
- Ensure dates are in YYYY-MM-DD format
- Check that "From" date is before "To" date
- Clear filters and try again

#### **Scrollbar Issues**
- Restart the application
- Check for multiple instances running
- Clear application cache if needed

### **Error Messages**
- **⚠️ Warning**: Non-critical issues with helpful guidance
- **✓ Success**: Confirmation of successful operations
- **❌ Error**: Critical errors requiring attention

### **Getting Help**
1. **Check the logs** - Error messages provide specific guidance
2. **Review this README** - Comprehensive documentation
3. **Run tests** - Verify functionality with test suite
4. **GitHub Issues** - Report bugs or request features

## 📊 Test Coverage

The application includes **43 comprehensive tests** covering:

- **Core Functionality**: 15 tests
- **UI Components**: 8 tests  
- **Data Management**: 10 tests
- **Project Management**: 5 tests
- **Date Handling**: 5 tests

**Test Results**: All tests passing ✅

## 🤝 Contributing

### **How to Contribute**
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Submit a pull request**

### **Development Guidelines**
- **Follow PEP 8** - Python style guidelines
- **Add tests** - New features require test coverage
- **Update documentation** - Keep README current
- **Test thoroughly** - Ensure all functionality works

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer & Liability

### **Important Legal Notice**
This software is provided for **educational and personal use** purposes. The authors and contributors are **not responsible** for any financial, legal, or business decisions made based on the data generated by this application.

### **Usage Limitations**
- **Not intended for critical business operations** without proper validation
- **Users should verify time tracking accuracy** for billing purposes
- **Backup your data regularly** - the application includes backup features
- **Consult professionals** for business decisions, tax purposes, or legal compliance
- **Test thoroughly** in your environment before production use

### **Data & Privacy**
- **Local storage only** - no data is transmitted to external servers
- **User responsibility** - you are responsible for your data security
- **No warranty** - data integrity is not guaranteed
- **Backup regularly** - use the built-in backup features

### **Professional Use**
- **Freelancers**: Verify time accuracy before client billing
- **Consultants**: Ensure compliance with client requirements
- **Businesses**: Test thoroughly before replacing existing systems
- **Legal/Medical**: Ensure compliance with industry regulations

### **What We're NOT Responsible For**
- ❌ **Financial losses** from incorrect time tracking
- ❌ **Legal issues** from non-compliance with regulations
- ❌ **Data loss** from system failures or user errors
- ❌ **Business decisions** made based on application data
- ❌ **Client disputes** over billing accuracy
- ❌ **Regulatory compliance** in your industry

### **What We ARE Responsible For**
- ✅ **Open source code** - freely available and modifiable
- ✅ **Documentation** - comprehensive user and developer guides
- ✅ **Testing** - 43+ tests ensuring core functionality
- ✅ **Community support** - through GitHub issues and discussions
- ✅ **Continuous improvement** - regular updates and bug fixes

**By using this software, you acknowledge that you understand these limitations and accept full responsibility for your usage and any consequences thereof.**

## 🙏 Acknowledgments

- **Python Community** - For the excellent Tkinter framework
- **Open Source Contributors** - For inspiration and best practices
- **Testing Community** - For comprehensive testing methodologies

---

**TimeTracker Pro** - Professional time tracking made simple! ⏱️✨

*Built with ❤️ using Python and Tkinter*#   T r i g g e r   w o r k f l o w  
 