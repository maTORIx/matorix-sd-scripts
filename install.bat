set "FILE_PATH=%~dp0"
set "DIR_PATH=%~dp0"
set "DIR_PATH=%DIR_PATH:~0,-1%"
for %%i in ("%DIR_PATH%") do set "DIR_NAME=%%~nxi"
set "TARGET_DIR=sd-scripts"

if not "%DIR_NAME%"=="%TARGET_DIR%" (
  echo %DIR_NAME%
  echo %TARGET_DIR%
  echo Error: The script must be run from the "%TARGET_DIR%" directory.
  exit /b 1
)

call venv/Scripts/activate
pip install onnxruntime
cd ..
if not exist "matorix-sd-scripts" git clone https://github.com/matorix/matorix-sd-scripts
cd matorix-sd-scripts
git pull
call setup.bat

exit /b 0