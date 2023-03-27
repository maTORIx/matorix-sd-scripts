set "FILE_PATH=%~dp0"
set "DIR_NAME=%~n0"
set "TARGET_DIR=sd-scripts"

REM ディレクトリ名が"sd-scripts"でない場合、エラーをはいて終了
if not "%DIR_NAME%"=="%TARGET_DIR%" (
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