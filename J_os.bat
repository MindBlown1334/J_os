@echo off
setlocal enabledelayedexpansion

set count=0
for /f "tokens=*" %%a in ('python get_settings.py') do (
    set /a count+=1
    if !count! EQU 1 set WIDTH=%%a
    if !count! EQU 2 set HEIGHT=%%a
)

title J_OS
mode %WIDTH%, %HEIGHT%
color 0F
python main.py
pause
