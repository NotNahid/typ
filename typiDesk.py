"""
TypiDesk - Universal Desktop AI Assistant
Transforms text with inline commands using AI

Backend engine for the TypiDesk application.
"""

import os
import re
import sys
import threading
from datetime import datetime
import google.generativeai as genai
from pynput import keyboard

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

class Config:
    """Configuration class - edit your settings here"""
    
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-1.5-flash"
    DEBUG = True
    ACTIVATION_KEY = keyboard.Key.space

# ============================================================================ 
# AI BACKEND
# ============================================================================ 

class AIBackend:
    """Handles all AI transformations using Google Gemini"""
    
    def __init__(self, api_key, model="gemini-1.5-flash"):
        if not api_key:
            print("\n⚠️  ERROR: Please set the GEMINI_API_KEY environment variable!")
            print("Get a free API key at: https://makersuite.google.com/app/apikey\n")
            sys.exit(1)
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        
        self.prompts = {
            "fix": "Fix grammar, spelling, and punctuation errors. Return ONLY the corrected text, nothing else.",
            "polite": "Rewrite this text to be more polite, professional, and respectful. Maintain the core message but improve tone. Return ONLY the rewritten text.",
            "casual": "Rewrite this text in a casual, friendly, conversational tone. Make it sound natural and relaxed. Return ONLY the rewritten text.",
            "summ": "Summarize this text concisely. Capture the key points in 2-3 sentences. Return ONLY the summary.",
            "expand": "Expand and elaborate on this text. Add more detail, examples, and explanation while maintaining the original meaning. Return ONLY the expanded text.",
            "short": "Make this text more concise. Remove unnecessary words while keeping the core meaning. Return ONLY the shortened text.",
            "trans": "Translate this text to {target_lang}. Return ONLY the translation, nothing else.",
            "explain": "Explain this concept in simple terms that anyone can understand. Return ONLY the explanation.",
            "code": "Convert this description into working code. Be specific and practical. Return ONLY the code.",
        }
    
    def transform(self, text, command, modifier=None):
        try:
            prompt_template = self.prompts.get(command)
            if not prompt_template:
                return f"❌ Unknown command: ?{command}"
            
            if command == "trans":
                target_lang = "English"
                if modifier:
                    lang_codes = {
                        "es": "Spanish", "fr": "French", "de": "German", 
                        "it": "Italian", "pt": "Portuguese", "ru": "Russian",
                        "ja": "Japanese", "ko": "Korean", "zh": "Chinese",
                        "ar": "Arabic", "hi": "Hindi", "bn": "Bengali"
                    }
                    target_lang = lang_codes.get(modifier, modifier.upper())
                prompt_template = prompt_template.format(target_lang=target_lang)
            
            full_prompt = f"{prompt_template}\n\nText:\n{text}"
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "❌ No response from AI"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ============================================================================ 
# COMMAND PARSER
# ============================================================================ 

class CommandParser:
    """Detects and parses inline commands from text"""
    
    COMMAND_PATTERN = r'^(.+?)\?(fix|polite|casual|summ|expand|short|trans|explain|code)(-\w+)?$' 
    
    @staticmethod
    def parse(text):
        match = re.search(CommandParser.COMMAND_PATTERN, text.strip(), re.DOTALL)
        if match:
            main_text = match.group(1).strip()
            command = match.group(2)
            modifier = match.group(3)[1:] if match.group(3) else None
            return main_text, command, modifier
        return None, None, None

# ============================================================================ 
# TYPIDESK ENGINE
# ============================================================================ 

class TypiDesk:
    """Main application engine - designed to be controlled by a GUI"""
    
    def __init__(self, config):
        self.config = config
        self.ai = AIBackend(config.GEMINI_API_KEY, config.GEMINI_MODEL)
        self.parser = CommandParser()
        self.keyboard_controller = keyboard.Controller()
        self.listener = None
        
        self.buffer = ""
        self.transforming = False
        self.stats = {"transformations": 0, "start_time": datetime.now()}
        
    def log(self, message, prefix="ℹ️"):
        if self.config.DEBUG or prefix in ["✅", "🤖", "⚠️", "❌"]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {prefix} {message}")

    def on_press(self, key):
        if self.transforming:
            return

        try:
            if key == keyboard.Key.space:
                self.buffer += " "
            elif key == keyboard.Key.backspace:
                self.buffer = self.buffer[:-1]
            elif hasattr(key, 'char') and key.char is not None:
                self.buffer += key.char
            
            if key == self.config.ACTIVATION_KEY:
                self.process_buffer()

        except Exception as e:
            self.log(f"Error on key press: {e}", "❌")

    def process_buffer(self):
        text, command, modifier = self.parser.parse(self.buffer)
        
        if command:
            self.transforming = True
            self.log(f"Detected command: ?{command}" + (f"-{modifier}" if modifier else ""), "🤖")
            
            result = self.ai.transform(text, command, modifier)
            
            if result.startswith("❌"):
                self.log(result, "❌")
                self.transforming = False
                return

            delete_count = len(self.buffer)
            self.log(f"Deleting {delete_count} characters...")
            for _ in range(delete_count):
                self.keyboard_controller.press(keyboard.Key.backspace)
                self.keyboard_controller.release(keyboard.Key.backspace)
            
            self.log(f"Typing result: {result[:50]}...")
            self.keyboard_controller.type(result)
            
            self.stats["transformations"] += 1
            self.log(f"✨ Transformed! (Total: {self.stats['transformations']})", "✅")
            self.buffer = ""
            self.transforming = False

    def start(self):
        if self.listener is None:
            self.log("Starting keyboard listener...", "✅")
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

    def pause(self):
        if self.listener and self.listener.running:
            self.log("Pausing keyboard listener...", "⚠️")
            self.listener.stop()
            self.listener = None

    def stop(self):
        self.log("Stopping TypiDesk engine...", "👋")
        if self.listener:
            self.listener.stop()
