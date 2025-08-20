#!/usr/bin/env python3
"""
Manual Build and Release Script for TimeTracker Pro
This script builds the executable locally and creates a release package
"""

import os
import sys
import shutil
import subprocess
import zipfile
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def create_icon():
    """Create the icon file if it doesn't exist"""
    if not os.path.exists('icon.ico'):
        print("🔄 Creating icon file...")
        try:
            import create_icon
            create_icon.create_simple_icon()
            with open('icon.ico', 'wb') as f:
                f.write(create_icon.create_simple_icon())
            print("✅ Icon file created")
        except Exception as e:
            print(f"⚠️  Could not create icon: {e}")
            # Create empty icon file
            with open('icon.ico', 'wb') as f:
                f.write(b'')
            print("Created empty icon file")

def build_with_pyinstaller():
    """Try to build with PyInstaller"""
    print("\n🚀 Attempting PyInstaller build...")
    
    # Install PyInstaller if not available
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        if not run_command("python -m pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    # Build the executable
    build_command = 'pyinstaller --onefile --windowed --name "TimeTracker-Pro" --icon=icon.ico main.py'
    if run_command(build_command, "Building executable with PyInstaller"):
        return True
    
    # Try with python -m PyInstaller if direct command fails
    build_command = 'python -m PyInstaller --onefile --windowed --name "TimeTracker-Pro" --icon=icon.ico main.py'
    if run_command(build_command, "Building executable with PyInstaller (module mode)"):
        return True
    
    return False

def build_with_cx_freeze():
    """Try to build with cx_Freeze as fallback"""
    print("\n🔄 Attempting cx_Freeze build...")
    
    # Install cx_Freeze if not available
    try:
        import cx_Freeze
        print("✅ cx_Freeze already installed")
    except ImportError:
        print("📦 Installing cx_Freeze...")
        if not run_command("python -m pip install cx_Freeze", "Installing cx_Freeze"):
            return False
    
    # Build the executable
    if run_command("python setup.py build_exe", "Building executable with cx_Freeze"):
        return True
    
    return False

def create_release_package():
    """Create the release package with all necessary files"""
    print("\n📦 Creating release package...")
    
    # Create distribution directory
    package_dir = "TimeTracker-Pro-Portable"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Find the executable
    exe_path = None
    if os.path.exists("dist/TimeTracker-Pro.exe"):
        exe_path = "dist/TimeTracker-Pro.exe"
        exe_name = "TimeTracker-Pro.exe"
    elif os.path.exists("build/exe.win-amd64-3.10/main.exe"):
        exe_path = "build/exe.win-amd64-3.10/main.exe"
        exe_name = "TimeTracker-Pro.exe"
    else:
        print("❌ No executable found! Build failed.")
        return False
    
    # Copy executable
    shutil.copy2(exe_path, os.path.join(package_dir, exe_name))
    print(f"✅ Copied executable: {exe_name}")
    
    # Copy documentation and scripts
    files_to_copy = [
        "README.md",
        "TESTING_GUIDE.md", 
        "manual_build.md",
        "build.bat",
        "build.ps1",
        "run_tests.bat",
        "run_tests.ps1"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✅ Copied: {file}")
    
    # Create run script
    run_script = """@echo off
echo Starting TimeTracker Pro...
echo.
TimeTracker-Pro.exe
pause
"""
    with open(os.path.join(package_dir, "Run-TimeTracker.bat"), 'w') as f:
        f.write(run_script)
    print("✅ Created: Run-TimeTracker.bat")
    
    # Create installation instructions
    install_instructions = """# TimeTracker Pro - Portable Installation

## Quick Start
1. Extract this zip file to any folder
2. Double-click 'TimeTracker-Pro.exe' to run the application
3. Or use 'Run-TimeTracker.bat' for a more user-friendly startup

## What's Included
- TimeTracker-Pro.exe - The main application
- README.md - Complete documentation
- TESTING_GUIDE.md - Testing instructions
- Build scripts for developers

## System Requirements
- Windows 10/11
- No Python installation required
- ~50MB RAM when running

## Data Location
Your time tracking data will be saved in the same folder as the executable:
- config.json - Application settings
- work_hours.json - Your time tracking data
- backups/ - Automatic backups

## Support
Visit: https://github.com/MagnusOestlund/timetracker
"""
    
    with open(os.path.join(package_dir, "INSTALL.md"), 'w', encoding='utf-8') as f:
        f.write(install_instructions)
    print("✅ Created: INSTALL.md")
    
    return True

def create_zip_file():
    """Create the final zip file"""
    print("\n🗜️ Creating zip file...")
    
    package_dir = "TimeTracker-Pro-Portable"
    zip_filename = "TimeTracker-Pro-Windows.zip"
    
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    # Get file size
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"✅ Created: {zip_filename} ({size_mb:.1f} MB)")
    
    return zip_filename

def main():
    """Main build process"""
    print("🚀 TimeTracker Pro - Manual Build and Release")
    print("=" * 50)
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("❌ This script is designed for Windows only")
        return
    
    # Create icon
    create_icon()
    
    # Try to build with PyInstaller first
    if build_with_pyinstaller():
        print("✅ PyInstaller build successful!")
    elif build_with_cx_freeze():
        print("✅ cx_Freeze build successful!")
    else:
        print("❌ All build methods failed!")
        return
    
    # Create release package
    if not create_release_package():
        return
    
    # Create zip file
    zip_filename = create_zip_file()
    
    print("\n🎉 Build completed successfully!")
    print("=" * 50)
    print(f"📦 Release package: {zip_filename}")
    print(f"📁 Package contents: TimeTracker-Pro-Portable/")
    
    print("\n📤 To upload to GitHub:")
    print("1. Go to: https://github.com/MagnusOestlund/timetracker/releases")
    print("2. Click 'Create a new release'")
    print("3. Tag version: v1.0.0 (or your desired version)")
    print("4. Title: TimeTracker Pro v1.0.0")
    print("5. Upload the zip file as a release asset")
    print("6. Add release notes and publish!")
    
    print(f"\n💡 The zip file '{zip_filename}' is ready for upload!")
    
    # Clean up build artifacts (optional)
    cleanup = input("\n🧹 Clean up build artifacts? (y/n): ").lower().strip()
    if cleanup == 'y':
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("TimeTracker-Pro-Portable"):
            shutil.rmtree("TimeTracker-Pro-Portable")
        print("✅ Build artifacts cleaned up")

if __name__ == "__main__":
    main() 