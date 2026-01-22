import os
import asyncio
import webbrowser
import urllib.parse
from pynput.keyboard import Key, Controller as KeyboardController

try:
    from livekit.agents import function_tool
except ImportError:
    def function_tool(func):
        return func

from fuzzywuzzy import process

keyboard = KeyboardController()

def _find_first_audio(paths):
    exts = {".mp3", ".wav", ".m4a", ".flac"}
    for base in paths:
        if not base or not os.path.isdir(base):
            continue
        try:
            for root, dirs, files in os.walk(base):
                for name in files:
                    _, ext = os.path.splitext(name)
                    if ext.lower() in exts:
                        return os.path.join(root, name)
                break
        except Exception:
            continue
    return None

def _find_system_media():
    candidates = [
        r"C:\\Windows\\Media",
        r"C:\\Windows\\Media\\Windows Notify.wav",
        r"C:\\Windows\\Media\\tada.wav",
    ]
    for path in candidates:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for name in files:
                    if name.lower().endswith(".wav"):
                        return os.path.join(root, name)
        elif os.path.isfile(path):
            return path
    return None

def _try_start_player():
    user_music = os.path.join(os.path.expanduser("~"), "Music")
    audio = _find_first_audio([
        user_music,
        r"D:\\Music",
        r"D:\\Songs",
        r"C:\\Music",
        r"E:\\Music",
    ]) or _find_system_media()

    if audio and os.path.isfile(audio):
        try:
            os.startfile(audio)
            return True
        except Exception:
            pass

    try:
        webbrowser.open("https://music.youtube.com/watch?v=jfKfPfyJRdk&autoplay=1")
        return True
    except Exception:
        return False

@function_tool
async def activate_music(prompt: str = "") -> str:
    try:
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        await asyncio.sleep(0.2)
        return "✅ Music toggled"
    except Exception:
        started = _try_start_player()
        return "✅ Music started" if started else "❌ Unable to start music"

@function_tool
async def deactivate_music() -> str:
    try:
        keyboard.press(Key.media_play_pause)
        keyboard.release(Key.media_play_pause)
        await asyncio.sleep(0.2)
        return "✅ Music paused"
    except Exception:
        return "❌ Unable to pause music"

def _index_audio(paths):
    items = []
    exts = {".mp3", ".wav", ".m4a", ".flac"}
    for base in paths:
        if not base or not os.path.isdir(base):
            continue
        try:
            for root, _, files in os.walk(base):
                for name in files:
                    _, ext = os.path.splitext(name)
                    if ext.lower() in exts:
                        items.append({"name": os.path.splitext(name)[0], "path": os.path.join(root, name)})
                break
        except Exception:
            continue
    return items

def _search_audio(query, items):
    names = [i["name"] for i in items]
    if not names:
        return None
    best, score = process.extractOne(query, names)
    if score >= 70:
        for i in items:
            if i["name"] == best:
                return i
    return None

@function_tool
async def play_song(name: str) -> str:
    bases = [
        os.path.join(os.path.expanduser("~"), "Music"),
        r"D:\\Music",
        r"D:\\Songs",
        r"C:\\Music",
        r"E:\\Music",
    ]
    items = _index_audio(bases)
    item = _search_audio(name.strip(), items) if name else None
    if item:
        try:
            os.startfile(item["path"]) if os.name == "nt" else webbrowser.open(item["path"]) 
            return f"✅ Playing: {item['name']}"
        except Exception:
            pass
    q = urllib.parse.quote_plus(name or "lofi music")
    try:
        webbrowser.open(f"https://music.youtube.com/search?q={q}")
        return f"✅ Playing online: {name or 'lofi music'}"
    except Exception:
        return "❌ Unable to play song"
