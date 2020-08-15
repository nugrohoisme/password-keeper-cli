@echo off

cd /d %~dp0
CALL venv\Scripts\activate
python3 password.py
CALL deactivate
echo.
pause