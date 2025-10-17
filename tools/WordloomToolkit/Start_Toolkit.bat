@echo off
setlocal
chcp 65001 >nul
REM 进入脚本所在目录
pushd "%~dp0"

REM 优先用打包好的 EXE
if exist "WordloomToolkit.exe" (
  start "" "WordloomToolkit.exe"
  goto :EOF
)

REM 回退：用系统 Python 无控制台启动
REM 如你用 py 管理器，可改为：start "" py -3w app.py
start "" pythonw app.py

popd
endlocal
