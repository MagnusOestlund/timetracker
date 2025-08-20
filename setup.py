import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help
build_exe_options = {
    "packages": ["tkinter", "json", "os", "csv", "datetime", "shutil", "typing"],
    "excludes": ["unittest", "test"],
    "include_files": [],
    "optimize": 2
}

# Base for Windows GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TimeTracker Pro",
    version="1.0",
    description="Professional time tracking application",
    author="TimeTracker Pro Team",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="TimeTracker-Pro.exe")]
) 