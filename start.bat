@echo off
setlocal
cd /d %~dp0


set CONFIG_FILE=config.json
set JSON_KEY=sd_scripts_path

rem check if the config file exists
if not exist "%CONFIG_FILE%" (
  echo Error: The config file "%CONFIG_FILE%" does not exist.
  exit /b 1
)

rem parse the json and get the value of sd_scripts_path
for /f "usebackq tokens=2 delims=:," %%a in (`type "%CONFIG_FILE%" ^| find /i "%JSON_KEY%"`) do (
  set SD_SCRIPTS_PATH=%%~a
)

rem check if the sd_scripts_path is set
if not defined SD_SCRIPTS_PATH (
  echo Error: The sd_scripts_path is not set in the config file "%CONFIG_FILE%".
  exit /b 1
)

rem activate the virtual environment
set "SD_SCRIPTS_PATH=%SD_SCRIPTS_PATH:\\=\%"
set "SD_SCRIPTS_PATH=%SD_SCRIPTS_PATH:~1%"
call "%SD_SCRIPTS_PATH%\venv\Scripts\activate"

python main.py