@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Set the FLASK_APP environment variable if needed
set FLASK_APP=flaskr

REM Run the Flask application
flask run

REM Keep the command prompt open after running the application
cmd /K
