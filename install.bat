@echo off

set DIR=%~dp0

python3 -m virtualenv %DIR%\venv
CALL %DIR%\venv\Scripts\activate
pip install -r %DIR%\package.conf
CALL deactivate
pause