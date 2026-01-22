import os
import sys
import asynci
import subprocess
import logging
import builtins
import json
import time
from datetime import date
from dotenv import load_dotenv
import threading
import tkinter as tk
import google.genai
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions, function_tool
from livekit.plugins import (
    openai as lk_openai,
    noise_cancellation,
)
# FIXED: Correct Google Realtime import
from livekit.plugins.google.beta import realtime as google_realtime

# ---------------------- YOUR MODULE IMPORTS ----------------------
from jarvis_prompts import behavior_prompts, Reply_prompts
from jarvis_screenshot import screenshot_tool
from jarvis_google_search import google_search, get_current_datetime
from jarvis_memory import load_memory, save_memory, get_recent_conversations, add_memory_entry
from memory_inter import MEMORY_KEYWORDS, inject_memory_context
from jarvis_get_whether import get_weather
from jarvis_window_CTRL import open, close, folder_file
from jarvis_file_opner import Play_file

from jarvis_gui import open_gui
from keyboard_mouse_CTRL import (
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    swipe_gesture_tool,
    press_hotkey_tool,
    control_volume_tool
)
from mouse_scroll import (
    slow_scroll_tool_once,
    start_slow_scroll_tool,
    stop_slow_scroll_tool
)
from jarvis_music_tools import activate_music, deactivate_music, play_song

from delete_file import send_file_and_delete
from lock import activate_sleep_mode, lock_screen, shutdown_pc, cancel_shutdown
from jarvis_whatapp import whatsapp_main  

from jarvis_screen_reader import (
    read_file_tool,
    read_screen_tool,
    read_screen_area_tool,
    list_supported_formats_tool
)
from chess_game import JarvisChessGUI
from real_stock import realtime_stock_advisor


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ENABLE_MEMORY_INTERCEPTOR = True

# ==============================================================================
# YOUR EXISTING FUNCTION TOOLS (unchanged)
# ==============================================================================
@function_tool
async def jarvis_auto_code(prompt: str, filename: str = "output.py") -> str:
    # ... your existing code unchanged
    pass

@function_tool
async def doctor_strange_effect() -> str:
    # ... unchanged
    pass
@function_tool
async def activate_ironman_shoot() -> str:
    # ... unchanged
    pass

@function_tool
async def chess_game() -> str:
    # ...unchanged
    pass


@function_tool
async def jarvis_code_generator(topic: str) -> str:
    # ... unchanged
    pass

@function_tool
async def generate_code_file(language: str = "python", content: str = "print('Hello, Jarvis')") -> str:
    # ... unchanged
    pass

@function_tool
async def create_jarvis_website() -> str:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        site_dir = os.path.join(base_dir, "website")
        os.makedirs(site_dir, exist_ok=True)
        index_path = os.path.join(site_dir, "index.html")
        html = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jarvis</title><style>body{font-family:Segoe UI,system-ui,-apple-system;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;background:#0a0f1a;color:#e6edf3}.card{background:#111827;border:1px solid #1f2937;border-radius:16px;padding:32px;box-shadow:0 10px 30px rgba(0,0,0,.4);max-width:720px}h1{margin:0 0 12px;font-size:32px}p{margin:8px 0 0;line-height:1.6;color:#9ca3af}.badge{display:inline-block;background:#1f2937;color:#a7f3d0;border:1px solid #10b981;padding:4px 10px;border-radius:999px;font-size:12px;margin-top:12px}.actions{margin-top:20px;display:flex;gap:10px}.btn{padding:10px 14px;border-radius:10px;border:1px solid #374151;background:#0b1324;color:#e6edf3;cursor:pointer}.btn:hover{background:#0e172a}</style></head><body><div class="card"><h1>Jarvis Personal Assistant</h1><p>Voice-ready assistant with WhatsApp automation, image generation, and desktop control.</p><div class="badge">Online</div><div class="actions"><button class="btn" onclick="alert('Hello, Sir!')">Ping</button><a class="btn" href=\"https://web.whatsapp.com\" target=\"_blank\">Open WhatsApp Web</a></div></div></body></html>"""
        with builtins.open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        try:
            if os.name == "nt":
                os.startfile(index_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", index_path])
            else:
                subprocess.Popen(["xdg-open", index_path])
        except Exception:
            pass
        return f"✅ Website created and opened: {index_path}"
    except Exception as e:
        return f"❌ Website creation failed: {e}"

@function_tool
async def create_image(prompt: str, size: str = "512x512") -> str:
    try:
        return await generate_magic_image(prompt, size)
    except Exception as e:
        return f"❌ Image generation failed: {e}"
# 🔥 ✅ NEW WHATSAPP VOICE AUTOMATION TOOL (exactly like your other tools)
@function_tool
async def send_whatsapp_message(contact: str, message: str = "") -> str:
    """Send WhatsApp message via voice/text command. Say 'send WhatsApp message to Mom: Hi there'"""
    try:
        print(f"📱 JARVIS: Sending WhatsApp to {contact}: {message}")
        # Call your existing whatsapp_main function
        if message:
            result = whatsapp_main(contact=contact, message=message)
        else:
            # Voice mode - will prompt for message
            result = whatsapp_main(contact=contact)
        
        if "success" in result.lower() or "sent" in result.lower():
            return f"✅ WhatsApp sent to **{contact}**: {message}"
        else:
            return f"⚠️ WhatsApp issue: {result}"
    except Exception as e:
        return f"❌ WhatsApp failed: {e}"

@function_tool
async def open_whatsapp() -> str:
    """Open WhatsApp Desktop"""
    try:
        result = whatsapp_main(action="open")
        return "✅ WhatsApp opened" if "success" in result.lower() else f"⚠️ {result}"
    except Exception as e:
        return f"❌ WhatsApp open failed: {e}"

@function_tool
async def whatapps_auto_reply() -> str:
    try:
        result = whatsapp_main(action="reply_voice")
        return "✅ WhatsApp auto reply sent" if "success" in str(result).lower() else f"⚠️ {result}"
    except Exception as e:
        return f"❌ WhatsApp auto reply failed: {e}"

# ==============================================================================
# ASSISTANT CLASS - WHATSAPP TOOLS ADDED
# ==============================================================================
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=behavior_prompts,
            tools=[
                # ... all your existing tools unchanged
                google_search,
                get_current_datetime,
                get_weather,
                open,
                close,
                load_memory,
                save_memory,
                get_recent_conversations,
                add_memory_entry,
                folder_file,
                Play_file,
                screenshot_tool,
                activate_sleep_mode,
                lock_screen,
                shutdown_pc,
                cancel_shutdown,
                move_cursor_tool,
                mouse_click_tool,
                scroll_cursor_tool,
                type_text_tool,
                press_key_tool,
                press_hotkey_tool,
                control_volume_tool,
                swipe_gesture_tool,
                # Mouse scroll tools
                slow_scroll_tool_once,
                start_slow_scroll_tool,
                stop_slow_scroll_tool,
                # Screen reader tools
                read_file_tool,
                read_screen_tool,
                read_screen_area_tool,
                list_supported_formats_tool,
                activate_music,
                deactivate_music,
                create_jarvis_website,   
                play_song,
                
              
                
                generate_magic_image,
                doctor_strange_effect,
                jarvis_auto_code,
             
                # 🔥 ✅ NEW WHATSAPP VOICE TOOLS
                send_whatsapp_message,
                open_whatsapp,
                whatapps_auto_reply,
                chess_game,
                jarvis_code_generator,
                
                
            ]
        )

# ---------------------- REAL-TIME HUD STATE EXPORTER ----------------------
def update_jarvis_state(text, speaker="jarvis", data_type="transcript"):
    """Update shared state file for the Hotkey HUD to display"""
    try:
        state_file = os.path.join(os.path.dirname(__file__), "jarvis_state.json")
        state = {
            "text": text,
            "speaker": speaker,
            "data_type": data_type,
            "timestamp": time.time()
        }
        with builtins.open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to update jarvis_state.json: {e}")

# ==============================================================================
# ENTRYPOINT (unchanged - your fixed version)
# ==============================================================================
async def entrypoint(ctx: agents.JobContext):
    max_retries = 6
    retry_count = 1
    base_wait_time = 3
    
    while retry_count < max_retries:
        session = None
        try:
            print(f"\n🚀 Starting agent session (attempt {retry_count + 1}/{max_retries})...")
            
            # Google Realtime primary
            try:
                session = AgentSession(
                    llm=google_realtime.RealtimeModel(voice="Charon")
                )
                await session.start(
                    room=ctx.room,
                    agent=Assistant(),
                    room_input_options=RoomInputOptions(
                        noise_cancellation=noise_cancellation.BVC(),
                        video_enabled=True
                    )
                

                # Attach transcript listeners for real-time HUD
                @session.on("assistant_transcript")
                def on_assistant_transcript(transcript):
                    if transcript.text:
                        update_jarvis_state(transcript.text, speaker="jarvis", data_type="transcript")

                @session.on("user_transcript")
                def on_user_transcript(transcript):
                    if transcript.text:
                        update_jarvis_state(transcript.text, speaker="user", data_type="transcript")

                @session.on("function_call_completed")
                def on_function_call_completed(tool_call):
                    """Show tool results on HUD (e.g. Google Search results)"""
                    if tool_call.function_info.name == "google_search":
                        update_jarvis_state(f"SEARCH RESULTS: {tool_call.result}", speaker="jarvis", data_type="tool_result")
                    elif tool_call.function_info.name == "type_text_tool":
                        update_jarvis_state("TYPING IN ACTIVE WINDOW...", speaker="jarvis", data_type="status")

                print("✅ Google Realtime voice model + WhatsApp ready!")
                break
            except Exception as e_google:
                print(f"⚠️ Google Realtime failed: {e_google}")
                
                # OpenAI fallback
                if os.getenv("OPENAI_API_KEY"):
                    try:
                        session = AgentSession(
                            llm=lk_openai.realtime.RealtimeModel()
                        )
                        await session.start(
                            room=ctx.room,
                            agent=Assistant(),
                            room_input_options=RoomInputOptions(
                                noise_cancellation=noise_cancellation.BVC(),
                                video_enabled=True
                            )
                        )

                        # Attach transcript listeners for real-time HUD (OpenAI fallback)
                        @session.on("assistant_transcript")
                        def on_assistant_transcript_oa(transcript):
                            if transcript.text:
                                update_jarvis_state(transcript.text, speaker="jarvis", data_type="transcript")

                        @session.on("user_transcript")
                        def on_user_transcript_oa(transcript):
                            if transcript.text:
                                update_jarvis_state(transcript.text, speaker="user", data_type="transcript")

                        @session.on("function_call_completed")
                        def on_function_call_completed_oa(tool_call):
                            if tool_call.function_info.name == "google_search":
                                update_jarvis_state(f"SEARCH RESULTS: {tool_call.result}", speaker="jarvis", data_type="tool_result")
                            elif tool_call.function_info.name == "type_text_tool":
                                update_jarvis_state("TYPING IN ACTIVE WINDOW...", speaker="jarvis", data_type="status")

                        print("✅ OpenAI Realtime + WhatsApp ready!")
                        break
                    except Exception as e_openai:
                        print(f"❌ OpenAI fallback failed: {e_openai}")
                        break
                else:
                    print("ℹ️ No OpenAI key - WhatsApp tools still available via GUI")
                    break
                
            await ctx.connect()
            print("✅ Connected - Say 'send WhatsApp message to [contact]'!")
            
            # Greeting with WhatsApp mention
            instructions = f"{Reply_prompts}\n\n**NEW**: Say 'send WhatsApp message to Mom: Hi' or 'open WhatsApp'"
            
            if ENABLE_MEMORY_INTERCEPTOR:
                try:
                    memory_context = await get_recent_conversations(limit=5)
                    if "अभी तक कोई बातचीत याद नहीं है" not in memory_context:
                        instructions += f"\n\n[RECENT CONTEXT]\n{memory_context}\n[/CONTEXT]"
                except:
                    pass
            
            await session.generate_reply(instructions=instructions)
            print("✅ Jarvis ready with WhatsApp voice control!")
            break
            
        except Exception as e:
            print(f"❌ Error (attempt {retry_count+1}): {e}")
            retry_count += 1
            if retry_count < max_retries:
                await asyncio.sleep(base_wait_time * retry_count)
            else:
                print("❌ Max retries exceeded - check WhatsApp Desktop is running")
                break
        finally:
            if session:
                try:
                    await session.stop()
                except:
                    pass

# ==============================================================================
# MAIN (removed duplicate)
# ==============================================================================
if __name__ == "__main__":
    main()
