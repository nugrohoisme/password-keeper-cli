@echo off

set DIR=%~dp0

CALL %DIR%\venv\Scripts\activate
python3 %DIR%\password.py
CALL deactivate
echo.
pause