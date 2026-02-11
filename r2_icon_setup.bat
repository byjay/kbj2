@echo off
REM R2 탐색기 바로가기 아이콘 설정

set SHORTCUT=%USERPROFILE%\Desktop\R2탐색기.url
set ICON=F:\kbj2\r2_icon.ico

REM .url 파일에 아이콘 설정
echo [InternetShortcut] > "%SHORTCUT%"
echo URL=python.exe "F:\kbj2\main.py" r2 explore >> "%SHORTCUT%"
echo IconFile=%ICON% >> "%SHORTCUT%"
echo IconIndex=0 >> "%SHORTCUT%

echo 바로가기 아이콘이 설정되었습니다.
pause
