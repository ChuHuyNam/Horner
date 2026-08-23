@echo off
setlocal
py -m pip install --upgrade pyinstaller
if errorlevel 1 exit /b 1
py -m PyInstaller --noconfirm --clean --onefile --windowed --name HornerCalculator horner_calculator.py
if errorlevel 1 exit /b 1
echo.
echo Da tao: dist\HornerCalculator.exe
endlocal
