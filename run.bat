@echo off
for /f "tokens=1,* delims==" %%A in (.env) do (
    if "%%A"=="AGENT_DIR" set AGENT_DIR=%%B
)
cd /d %AGENT_DIR%
call .venv\Scripts\activate.bat
python main.py