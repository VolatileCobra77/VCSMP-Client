@echo off
setlocal

rem Set the project name and paths
echo "making variables"
set "projectName=VCSMP Mod Updater"
set "documentsPath=%USERPROFILE%\Documents"
set "projectPath=%documentsPath%\%projectName%"
set "desktop=%USERPROFILE%\Desktop"

echo Checking Path

rem Create a new directory in the Documents folder
mkdir "%projectPath%" 2>nul
if not exist "%projectPath%" (
    echo Failed to create the project directory.
    exit /b 1
)

echo Copying Files

rem Copy all project files into the new directory
xcopy /s /i *.* "%projectPath%"

cd "%projectPath%"

echo Making Shortcut

rem Create a shortcut to start.bat
echo Set WshShell = CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set shortcut = WshShell.CreateShortcut("VCSMP Mod Updater.lnk") >> CreateShortcut.vbs
echo shortcut.TargetPath = "%projectPath%/run.bat" >> CreateShortcut.vbs
echo shortcut.WorkingDirectory = "%projectPath%" >> CreateShortcut.vbs
echo shortcut.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

rem Add the desired line to run.bat
echo "%USERPROFILE%\Documents\VCSMP Mod Updater\Scripts\python.exe" ./main.py >> run.bat

echo Project setup completed successfully.

rem Open the output directory in File Explorer
start "" "%projectPath%"

exit /b 0