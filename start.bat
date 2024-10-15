REM Go to the batch file's current directory
cd /d "%~dp0"

REM Activate the virtual environment
CALL backenv\Scripts\activate

REM Run run.py and host it on port 5000
set FLASK_APP=run.py
set FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000