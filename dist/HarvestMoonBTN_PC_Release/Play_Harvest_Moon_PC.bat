@echo off
setlocal
title Harvest Moon: Back to Nature (PC Port)
cd /d "%~dp0"

if exist "game\*.cue" goto :run_launcher
if exist "game\*.chd" goto :run_launcher
if exist "game\*.iso" goto :run_launcher
if exist "game\*.bin" goto :run_launcher

:missing_disc
cls
echo =======================================================================
echo [PERHATIAN / NOTICE]
echo File disc Harvest Moon: Back to Nature belum ditemukan!
echo.
echo Silakan tempatkan file:
echo   1. Harvest Moon - Back to Nature (USA).cue
echo   2. Harvest Moon - Back to Nature (USA).bin
echo ke dalam folder "game\" sebelum menjalankan port ini.
echo.
echo Baca petunjuk lengkap di: "game\TEMPATKAN_FILE_DISC_DISINI.txt"
echo =======================================================================
echo.
pause
exit /b 1

:run_launcher
if exist "HarvestMoonBTN_Launcher.exe" (
    start "" "HarvestMoonBTN_Launcher.exe"
    exit /b 0
)

start "" "HarvestMoonBTN_Recompiled.exe"
exit /b 0
