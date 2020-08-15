@echo off

cd /d %~dp0
python3 -m virtualenv venv
CALL venv\Scripts\activate
pip install -r requirements.conf
CALL deactivate
pause