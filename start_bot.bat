@echo off
title Bot de Pesca - Prodigy RP
color 0A

echo ===============================================
echo   BOT DE PESCA AUTOMATIZADO
echo   Servidor: Prodigy RP
echo ===============================================
echo.
echo [AVISO] Use por sua conta e risco!
echo.
echo Controles:
echo   F6  - Iniciar/Pausar bot
echo   ESC - Parar completamente
echo   Mover mouse p/ canto superior esquerdo - Emergencia
echo.
echo ===============================================
echo.

C:\Users\vdesg\AppData\Local\Python\bin\python.exe fishing_bot.py

if errorlevel 1 (
    echo.
    echo ERRO ao executar o bot!
    echo Verifique se as dependencias estao instaladas.
    echo Execute: setup.bat
    pause
)
