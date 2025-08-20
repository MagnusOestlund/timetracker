@echo off
echo ========================================
echo    TimeTracker Build Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo Python found. Checking for packaging tools...
echo.

REM Try to install PyInstaller with different methods
echo Attempting to install PyInstaller...
echo.

REM Method 1: Standard install
echo Method 1: Standard pip install...
pip install pyinstaller
if not errorlevel 1 (
    echo PyInstaller installed successfully!
    goto :build
)

REM Method 2: Trusted host install
echo Method 1 failed. Trying Method 2: Trusted host install...
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyinstaller
if not errorlevel 1 (
    echo PyInstaller installed successfully!
    goto :build
)

REM Method 3: Alternative package index
echo Method 2 failed. Trying Method 3: Alternative package index...
pip install -i https://pypi.org/simple/ pyinstaller
if not errorlevel 1 (
    echo PyInstaller installed successfully!
    goto :build
)

REM Method 4: Try cx_Freeze as alternative
echo All PyInstaller methods failed. Trying cx_Freeze as alternative...
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org cx_Freeze
if not errorlevel 1 (
    echo cx_Freeze installed successfully!
    goto :build_cxfreeze
)

echo.
echo ERROR: Could not install any packaging tools
echo.
echo Possible solutions:
echo 1. Check your internet connection
echo 2. Check if you're behind a corporate firewall
echo 3. Try running as administrator
echo 4. Download PyInstaller manually from https://pypi.org/project/PyInstaller/
echo.
pause
exit /b 1

:build
echo.
echo Building executable with PyInstaller...
echo.

REM Create build directory if it doesn't exist
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM Build the executable
pyinstaller --onefile --windowed --name="TimeTracker" --distpath=./dist --workpath=./build --specpath=./build main.py

if not errorlevel 1 (
    echo.
    echo ========================================
    echo    BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Your executable is located in the 'dist' folder
    echo File: dist\TimeTracker.exe
    echo.
    echo You can now run TimeTracker.exe on any Windows machine
    echo without needing Python installed!
    echo.
) else (
    echo.
    echo Build failed. Trying alternative method...
    goto :build_cxfreeze
)
goto :end

:build_cxfreeze
echo.
echo Building executable with cx_Freeze...
echo.

REM Create setup.py for cx_Freeze
echo from cx_Freeze import setup, Executable > setup.py
echo. >> setup.py
echo build_exe_options = { >> setup.py
echo     "packages": ["tkinter", "json", "os", "csv", "datetime", "shutil"], >> setup.py
echo     "excludes": [], >> setup.py
echo     "include_files": [] >> setup.py
echo } >> setup.py
echo. >> setup.py
echo setup( >> setup.py
echo     name="TimeTracker", >> setup.py
echo     version="1.0", >> setup.py
echo     description="Professional Time Tracking Application", >> setup.py
echo     options={"build_exe": build_exe_options}, >> setup.py
echo     executables=[Executable("main.py", base="Win32GUI")] >> setup.py
echo ) >> setup.py

REM Build with cx_Freeze
python setup.py build

if not errorlevel 1 (
    echo.
    echo ========================================
    echo    BUILD SUCCESSFUL with cx_Freeze!
    echo ========================================
    echo.
    echo Your executable is located in the 'build' folder
    echo Check the build subdirectory for TimeTracker.exe
    echo.
) else (
    echo.
    echo Both build methods failed.
    echo Please check the error messages above.
    echo.
)

:end
echo.
echo Build process completed.
echo.
pause 