# Criado por Melhym Quemel <mpquemel@gmail.com>

import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "gemini_api": "", "openai_api": "", "openrouter_api": "", 
        "ollama_url": "http://localhost:11434/v1", "provider": "Google Gemini", "model": ""
    }

def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)