@echo off

:: 提示用户输入第一个参数
:: set /p param1="IN Cif Folder Path: "

:: 提示用户输入第二个参数
:: set /p param2="Out Bond&Angle txt Folder Path: "

set param1=%1
set param2=%2
"C:\\Program Files (x86)\\BIOVIA\\Materials Studio 19.1\\etc\\Scripting\\bin\\RunMatScript.bat" -np 1 -project GetBondAngle -- %param1% %param2%