@echo off

@REM Go to current directory.
cd /d "%~dp0"

@REM Create a virtual environment
IF NOT EXIST "backenv\Scripts\activate.bat" (
    python -m venv backenv
) ELSE (
    echo Virtual environment already exists
)

@REM REM Activate the virtual environment
IF EXIST "backenv\Scripts\activate" (
    CALL backenv\Scripts\activate
) ELSE (
    echo Virtual environment doesn't exist
)

@REM REM Install pymongo and flask
pip install -r requirements.txt

@REM REM Deactivate the virtual environment
deactivate

@REM echo Setup complete.
pause