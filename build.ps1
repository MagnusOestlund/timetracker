# TimeTracker Build Script (PowerShell Version)
# Run this script in PowerShell with: .\build.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TimeTracker Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python found. Checking for packaging tools..." -ForegroundColor Green
Write-Host ""

# Function to try installing PyInstaller
function Install-PyInstaller {
    Write-Host "Attempting to install PyInstaller..." -ForegroundColor Yellow
    Write-Host ""
    
    # Method 1: Standard install
    Write-Host "Method 1: Standard pip install..." -ForegroundColor Cyan
    try {
        pip install pyinstaller
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PyInstaller installed successfully!" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Method 1 failed." -ForegroundColor Red
    }
    
    # Method 2: Trusted host install
    Write-Host "Method 1 failed. Trying Method 2: Trusted host install..." -ForegroundColor Cyan
    try {
        pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyinstaller
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PyInstaller installed successfully!" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Method 2 failed." -ForegroundColor Red
    }
    
    # Method 3: Alternative package index
    Write-Host "Method 2 failed. Trying Method 3: Alternative package index..." -ForegroundColor Cyan
    try {
        pip install -i https://pypi.org/simple/ pyinstaller
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PyInstaller installed successfully!" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Method 3 failed." -ForegroundColor Red
    }
    
    return $false
}

# Function to try installing cx_Freeze
function Install-cxFrezee {
    Write-Host "All PyInstaller methods failed. Trying cx_Freeze as alternative..." -ForegroundColor Cyan
    try {
        pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org cx_Freeze
        if ($LASTEXITCODE -eq 0) {
            Write-Host "cx_Freeze installed successfully!" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "cx_Freeze installation failed." -ForegroundColor Red
    }
    return $false
}

# Try to install PyInstaller
$pyinstallerInstalled = Install-PyInstaller

if (-not $pyinstallerInstalled) {
    $cxfreezeInstalled = Install-cxFrezee
    
    if (-not $cxfreezeInstalled) {
        Write-Host ""
        Write-Host "ERROR: Could not install any packaging tools" -ForegroundColor Red
        Write-Host ""
        Write-Host "Possible solutions:" -ForegroundColor Yellow
        Write-Host "1. Check your internet connection" -ForegroundColor White
        Write-Host "2. Check if you're behind a corporate firewall" -ForegroundColor White
        Write-Host "3. Try running as administrator" -ForegroundColor White
        Write-Host "4. Download PyInstaller manually from https://pypi.org/project/PyInstaller/" -ForegroundColor White
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Build the executable
if ($pyinstallerInstalled) {
    Write-Host ""
    Write-Host "Building executable with PyInstaller..." -ForegroundColor Green
    Write-Host ""
    
    # Create build directories
    if (-not (Test-Path "build")) { New-Item -ItemType Directory -Name "build" }
    if (-not (Test-Path "dist")) { New-Item -ItemType Directory -Name "dist" }
    
    # Build the executable
    pyinstaller --onefile --windowed --name="TimeTracker" --distpath=./dist --workpath=./build --specpath=./build main.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "    BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your executable is located in the 'dist' folder" -ForegroundColor White
        Write-Host "File: dist\TimeTracker.exe" -ForegroundColor White
        Write-Host ""
        Write-Host "You can now run TimeTracker.exe on any Windows machine" -ForegroundColor White
        Write-Host "without needing Python installed!" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "Build failed. Trying alternative method..." -ForegroundColor Yellow
        $pyinstallerInstalled = $false
    }
}

if (-not $pyinstallerInstalled) {
    Write-Host ""
    Write-Host "Building executable with cx_Freeze..." -ForegroundColor Green
    Write-Host ""
    
    # Create setup.py for cx_Freeze
    $setupContent = @"
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter", "json", "os", "csv", "datetime", "shutil"],
    "excludes": [],
    "include_files": []
}

setup(
    name="TimeTracker",
    version="1.0",
    description="Professional Time Tracking Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI")]
)
"@
    
    $setupContent | Out-File -FilePath "setup.py" -Encoding UTF8
    
    # Build with cx_Freeze
    python setup.py build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "    BUILD SUCCESSFUL with cx_Freeze!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your executable is located in the 'build' folder" -ForegroundColor White
        Write-Host "Check the build subdirectory for TimeTracker.exe" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "Both build methods failed." -ForegroundColor Red
        Write-Host "Please check the error messages above." -ForegroundColor Yellow
        Write-Host ""
    }
}

Write-Host ""
Write-Host "Build process completed." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit" 