import asyncio
import os
import subprocess
import sys
import time
import textwrap
import pyautogui
import pyperclip
from datetime import datetime

try:
    from livekit.agents import function_tool
except Exception:
    def function_tool(f):
        return f

@function_tool
async def jarvis_auto_code_writer(
    language: str,
    task: str,
    filename: str = "",
    run_after_writing: bool = False
) -> str:
    """
    Advanced code writer that opens VS Code, creates a file, and types code line-by-line.
    
    Args:
        language: Programming language (python, js, html, css, etc.)
        task: Description of what the code should do
        filename: Optional specific filename
    """
    try:
        # 1. Generate Code Content
        code_content = generate_advanced_template(language, task)
        
        # 2. Determine File Path
        if not filename:
            ext = get_extension(language)
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"jarvis_generated_{timestamp}{ext}"
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        generated_dir = os.path.join(base_dir, "generated_code")
        os.makedirs(generated_dir, exist_ok=True)
        file_path = os.path.join(generated_dir, filename)

        # 3. Create Empty File (to open in VS Code)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

        # 4. Open VS Code
        print(f"🚀 Opening VS Code for: {filename}")
        # Use 'code' command to open the file in VS Code
        try:
            subprocess.Popen(["code", file_path], shell=True)
        except Exception:
            # Fallback for Windows if 'code' isn't in shell path directly
            os.system(f"code {file_path}")
            
        # 5. Wait for VS Code to focus
        await asyncio.sleep(4) # Give VS Code time to open and focus

        # 6. Type Code Line by Line
        print(f"⌨️ Writing code to {filename}...")
        lines = code_content.split('\n')
        
        # Initial wait for editor to be ready
        await asyncio.sleep(1)
        
        for line in lines:
            if not line.strip():
                pyautogui.press('enter')
                continue
                
            # Use pyperclip for faster and character-safe typing of each line
            pyperclip.copy(line)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            await asyncio.sleep(0.05) # Reduced delay for faster typing

        # 7. Final Save and Format
        await asyncio.sleep(0.5)
        pyautogui.hotkey('ctrl', 's')
        # Optional: Try to format code if extension is installed (Shift+Alt+F)
        pyautogui.hotkey('shift', 'alt', 'f')
        await asyncio.sleep(0.5)
        pyautogui.hotkey('ctrl', 's')
        
        if run_after_writing:
            print(f"🚀 Running generated code: {file_path}")
            try:
                if language.lower() == "python":
                    subprocess.Popen([sys.executable, file_path], close_fds=True)
                elif language.lower() == "html":
                    if os.name == "nt": # Windows
                        os.startfile(file_path)
                    elif sys.platform == "darwin": # macOS
                        subprocess.Popen(["open", file_path])
                    else: # Linux
                        subprocess.Popen(["xdg-open", file_path])
                elif language.lower() in ["javascript", "js"]:
                    # For JS, we might need node, or open in browser if it's a frontend script
                    # For now, let's assume node for backend JS or just open the file
                    try:
                        subprocess.Popen(["node", file_path], close_fds=True)
                    except FileNotFoundError:
                        print("Node.js not found. Cannot run JavaScript file directly.")
                        if os.name == "nt": # Windows
                            os.startfile(file_path)
                        elif sys.platform == "darwin": # macOS
                            subprocess.Popen(["open", file_path])
                        else: # Linux
                            subprocess.Popen(["xdg-open", file_path])
                else:
                    print(f"No specific run command for language: {language}. Opening file.")
                    if os.name == "nt": # Windows
                        os.startfile(file_path)
                    elif sys.platform == "darwin": # macOS
                        subprocess.Popen(["open", file_path])
                    else: # Linux
                        subprocess.Popen(["xdg-open", file_path])
                return f"✅ Code successfully written to {filename}, opened in VS Code, and executed."
            except Exception as run_e:
                return f"✅ Code successfully written to {filename} and opened in VS Code, but failed to execute: {run_e}"
        
        return f"✅ Code successfully written to {filename} and opened in VS Code."

    except Exception as e:
        return f"❌ Failed to auto-write code: {e}"

def generate_advanced_template(language: str, task: str) -> str:
    """Generates more robust code templates based on language."""
    lang = language.lower()
    
    if "website" in task.lower() or lang == "html":
        return textwrap.dedent(f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Advanced Website: {task}</title>
                <script src="https://cdn.tailwindcss.com"></script>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                    body {{ font-family: 'Inter', sans-serif; scroll-behavior: smooth; }}
                    .glass {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }}
                </style>
            </head>
            <body class="bg-slate-900 text-white">
                <!-- Navigation -->
                <nav class="fixed w-full z-50 glass py-4 px-8 flex justify-between items-center">
                    <div class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        JARVIS AI
                    </div>
                    <div class="space-x-6">
                        <a href="#home" class="hover:text-blue-400 transition">Home</a>
                        <a href="#features" class="hover:text-blue-400 transition">Features</a>
                        <a href="#contact" class="hover:text-blue-400 transition">Contact</a>
                    </div>
                </nav>

                <!-- Hero Section -->
                <section id="home" class="h-screen flex flex-col justify-center items-center text-center px-4">
                    <h1 class="text-6xl font-extrabold mb-6 animate-pulse">
                        {task}
                    </h1>
                    <p class="text-xl text-slate-400 max-w-2xl mb-8">
                        Experience the next generation of web design powered by JARVIS Automation.
                    </p>
                    <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-bold transition transform hover:scale-105">
                        Get Started
                    </button>
                </section>

                <!-- Features Section -->
                <section id="features" class="py-20 bg-slate-800 px-8">
                    <h2 class="text-4xl font-bold text-center mb-16">Core Features</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div class="glass p-8 rounded-2xl hover:bg-slate-700 transition">
                            <i class="fas fa-bolt text-4xl text-yellow-400 mb-4"></i>
                            <h3 class="text-xl font-bold mb-2">Fast Performance</h3>
                            <p class="text-slate-400">Optimized for speed and efficiency using the latest technologies.</p>
                        </div>
                        <div class="glass p-8 rounded-2xl hover:bg-slate-700 transition">
                            <i class="fas fa-shield-alt text-4xl text-green-400 mb-4"></i>
                            <h3 class="text-xl font-bold mb-2">Secure by Default</h3>
                            <p class="text-slate-400">Advanced security protocols to keep your data safe.</p>
                        </div>
                        <div class="glass p-8 rounded-2xl hover:bg-slate-700 transition">
                            <i class="fas fa-mobile-alt text-4xl text-blue-400 mb-4"></i>
                            <h3 class="text-xl font-bold mb-2">Fully Responsive</h3>
                            <p class="text-slate-400">Looks great on any device, from mobile to desktop.</p>
                        </div>
                    </div>
                </section>

                <!-- Footer -->
                <footer id="contact" class="py-12 text-center border-t border-slate-800">
                    <p class="text-slate-500">© 2024 JARVIS AI - Generated for: {task}</p>
                </footer>

                <script>
                    console.log("JARVIS Website Loaded: {task}");
                </script>
            </body>
            </html>
        ''').strip()

    if lang == "python" or "app" in task.lower():
        if "app" in task.lower():
            return textwrap.dedent(f'''
                import tkinter as tk
                from tkinter import ttk, messagebox
                import json
                import os

                class JarvisApp:
                    def __init__(self, root):
                        self.root = root
                        self.root.title("JARVIS AI App: {task}")
                        self.root.geometry("800x600")
                        self.root.configure(bg="#1e1e2e")

                        self.style = ttk.Style()
                        self.style.theme_use('clam')
                        
                        self.setup_ui()

                    def setup_ui(self):
                        # Main Container
                        main_frame = tk.Frame(self.root, bg="#1e1e2e")
                        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

                        # Header
                        header = tk.Label(main_frame, text="{task}", 
                                         font=("Helvetica", 24, "bold"), 
                                         fg="#cdd6f4", bg="#1e1e2e")
                        header.pack(pady=10)

                        # Content Area
                        self.content_frame = tk.Frame(main_frame, bg="#313244", bd=1, relief=tk.FLAT)
                        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=20)

                        # Status Bar
                        self.status = tk.Label(self.root, text="JARVIS AI System Active", 
                                             bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                             bg="#181825", fg="#a6adc8")
                        self.status.pack(side=tk.BOTTOM, fill=tk.X)

                        # Action Button
                        btn = tk.Button(main_frame, text="Run Task", 
                                       command=self.execute_task,
                                       bg="#89b4fa", fg="#11111b",
                                       font=("Helvetica", 12, "bold"),
                                       padx=20, pady=10, relief=tk.FLAT)
                        btn.pack(pady=10)

                    def execute_task(self):
                        messagebox.showinfo("JARVIS AI", "Executing: {task}")
                        self.status.config(text="Task Completed Successfully")

                if __name__ == "__main__":
                    root = tk.Tk()
                    app = JarvisApp(root)
                    root.mainloop()
            ''').strip()
        
        return textwrap.dedent(f'''
            import os
            import sys
            import time

            def main():
                """
                Task: {task}
                Generated by JARVIS Advanced Code Writer
                """
                print("--- JARVIS AUTOMATION STARTED ---")
                print("Logic: {task}")
                
                # Implementation logic here
                try:
                    # Your code goes here
                    print("Running core logic for: {task}")
                    time.sleep(1)
                except Exception as e:
                    print(f"Error: {{e}}")

                print("--- TASK COMPLETED ---")

            if __name__ == "__main__":
                main()
        ''').strip()
        
    elif lang in ["javascript", "js"]:
        return textwrap.dedent(f'''
            /**
             * Task: {task}
             * Generated by JARVIS Advanced Code Writer
             */
            const fs = require('fs');
            const path = require('path');

            async function runTask() {{
                console.log("🚀 Starting Task: {task}");
                
                try {{
                    // Implementation logic here
                    console.log("Initializing JARVIS core module...");
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    console.log("Processing: {task}");
                }} catch (error) {{
                    console.error("❌ Error:", error);
                }}
                
                console.log("✅ Task Finished");
            }}

            runTask();
        ''').strip()
        
    else:
        return f"# Task: {task}\n# Generated by JARVIS\n\n# Implement {language} code here."

def get_extension(language: str) -> str:
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "js": ".js",
        "html": ".html",
        "css": ".css",
        "java": ".java",
        "cpp": ".cpp",
        "c++": ".cpp"
    }
    return extensions.get(language.lower(), ".txt")

@function_tool
async def jarvis_code_generator(
    language: str,
    task: str,
    style: str = "clean",
    comments: bool = True
) -> str:
    """
    Universal code generator for JARVIS. (Kept for compatibility)
    """
    await asyncio.sleep(0)
    header = f"Language: {language.upper()} | Task: {task}\n"
    code = generate_advanced_template(language, task)
    return f"{header}\n{code}"



