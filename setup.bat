@echo off
echo ===============================================
echo   BOT DE PESCA - PRODIGY RP
echo ===============================================
echo.
echo Verificando Python...
C:\Users\vdesg\AppData\Local\Python\bin\python.exe --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
C:\Users\vdesg\AppData\Local\Python\bin\python.exe -m pip install -r requirements.txt

echo.
echo ===============================================
echo   Instalacao Completa!
echo ===============================================
echo.
echo Proximos passos:
echo 1. Execute: python calibrate.py
echo    - Calibre a regiao do minigame
echo    - Teste a deteccao
echo.
echo 2. Execute: python fishing_bot.py
echo    - Pressione F6 para iniciar
echo    - Pressione ESC para parar
echo.
echo ===============================================
pause
