@echo off
REM ========================================
REM R2 SSL 문제 해결 패키지 업그레이드
REM ========================================

echo ========================================
echo   패키지 업그레이드 시작
echo ========================================
echo.

echo 1. urllib3 업그레이드...
pip install --upgrade urllib3 certifi

echo.
echo 2. boto3 업그레이드...
pip install --upgrade boto3

echo.
echo 3. requests 업그레이드...
pip install --upgrade requests

echo.
echo ========================================
echo   업그레이드 완료!
echo ========================================
echo.
echo 새 터미널을 열고 R2탐색기를 실행하세요.
pause
