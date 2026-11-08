@echo off
title Harvest Moon: Back to Nature (PC Port)
cd /d "%~dp0recomp_project\build\Release"
if exist "HarvestMoonBTN_Launcher.exe" (
    start "" "HarvestMoonBTN_Launcher.exe"
    exit /b 0
)
start "" "HarvestMoonBTN_Recompiled.exe"
