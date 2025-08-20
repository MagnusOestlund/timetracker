@echo off
echo ========================================
echo    TimeTracker Test Runner
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

echo Python found. Running tests...
echo.

REM Run the test suite
python test_timetracker.py

if not errorlevel 1 (
    echo.
    echo ========================================
    echo    ALL TESTS PASSED! 🎉
    echo ========================================
    echo.
    echo Your TimeTracker application is working correctly!
    echo.
) else (
    echo.
    echo ========================================
    echo    SOME TESTS FAILED! ❌
    echo ========================================
    echo.
    echo Please check the test output above for details.
    echo.
)

echo Test run completed.
echo.
pause 