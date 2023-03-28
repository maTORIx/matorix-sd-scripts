cd /d %~dp0

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