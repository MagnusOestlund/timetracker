# TimeTracker Test Runner (PowerShell Version)
# Run this script with: .\run_tests.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TimeTracker Test Runner" -ForegroundColor Cyan
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

Write-Host "Python found. Running tests..." -ForegroundColor Green
Write-Host ""

# Run the test suite
python test_timetracker.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "    ALL TESTS PASSED! 🎉" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your TimeTracker application is working correctly!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "    SOME TESTS FAILED! ❌" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the test output above for details." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Test run completed." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit" 