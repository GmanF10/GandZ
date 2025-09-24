@echo off
setlocal
cd /d %~dp0\zeno_sidecar
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py %*
