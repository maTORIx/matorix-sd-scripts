cd /d %~dp0

set CONFIG_FILE=config.json
set JSON_KEY=sd_scripts_path
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

@REM pip install
pip install -r requirements.txt

@REM Download Waifu Diffusion repo, model and tags
if not exist "SW_CV_ModelZoo" git clone https://github.com/SmilingWolf/SW-CV-ModelZoo SW_CV_ModelZoo
if not exist "models" mkdir models
cd models
if not exist "wd14" mkdir wd14
cd wd14
if not exist "model.onnx" (
    powershell -Command "Invoke-WebRequest -Uri https://huggingface.co/SmilingWolf/wd-v1-4-swinv2-tagger-v2/resolve/main/model.onnx -OutFile model.onnx -UseBasicParsing -Verbose"
)
if not exist "selected_tags.csv" (
    powershell -Command "Invoke-WebRequest -Uri https://huggingface.co/SmilingWolf/wd-v1-4-swinv2-tagger-v2/resolve/main/selected_tags.csv -OutFile selected_tags.csv -UseBasicParsing -Verbose"
)