@echo off

cd /d %~dp0
python3 -m virtualenv venv
CALL venv\Scripts\activate
pip install -r package.conf
CALL deactivate
pause