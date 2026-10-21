"""
Jinx Companion Server
A Windows desktop chat app that reads Minecraft ATM10 save files.
Uses only Python standard library (http.server).
"""

import os
import json
import re
import urllib.request
import urllib.error
import http.server
import socketserver
import webbrowser
import threading
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
from html import escape as html_escape

# Local imports
from gamestate import build_game_state

# Constants
HOST = '127.0.0.1'
PORT = 8720
TEMPLATE_DIR = Path(__file__).parent / 'templates'
CONFIG_FILE = Path(__file__).parent / 'config.json'

# Default configuration
DEFAULT_CONFIG = {
    "llm_base_url": "http://127.0.0.1:31415/v1",
    "api_key": "",
    "model": "auto",
    "fallback_base_url": "http://127.0.0.1:8080/v1",
    "minecraft_instance_path": "",
    "world_name": ""
}


def load_config():
    """Load configuration from config.json, return defaults if not found."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, PermissionError):
        pass
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to config.json."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except (PermissionError, IOError):
        return False


def get_template(name):
    """Load an HTML template."""
    template_path = TEMPLATE_DIR / name
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body><h1>Template not found</h1></body>
</html>"""


def build_system_prompt(config):
    """Build the system prompt with persona and game state."""
    # Get game state
    instance_path = config.get('minecraft_instance_path', '')
    world_name = config.get('world_name', '')
    
    if instance_path and world_name:
        game_state = build_game_state(instance_path, world_name)
    else:
        game_state = "No Minecraft save path configured. Set your instance path and world name in Settings."
    
    # Build persona prompt
    system_prompt = (
        "You are Jinx, a sharp, friendly companion who knows Minecraft: All the Mods 10 deeply. "
        "You help the player progress and answer general questions too. "
        "Here is the player's current game state, read from their actual save files:\n"
        f"{game_state}\n\n"
        "Use this information to answer questions about progress and what to do next. "
        "Be helpful, concise, and friendly. If you don't know something, say so."
    )
    
    return system_prompt


def call_llm(base_url, api_key, model, messages, timeout=120):
    """
    Call an OpenAI-compatible LLM endpoint.
    Returns the reply text or raises an exception.
    """
    # Ensure base_url ends with /v1
    if not base_url.endswith('/v1'):
        if base_url.endswith('/'):
            base_url = base_url.rstrip('/') + '/v1'
        else:
            base_url = base_url + '/v1'
    
    url = f"{base_url}/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    payload = {
        'model': model,
        'messages': messages,
        'temperature': 0.7,
        'max_tokens': 2048,
        'stream': False
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                raise ValueError("No choices in response")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.read else str(e)
        raise Exception(f"HTTP Error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {str(e.reason)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response: {str(e)}")
    except Exception as e:
        raise Exception(f"LLM call failed: {str(e)}")


def handle_chat_request(config, request_data):
    """
    Handle a POST /chat request.
    request_data: {"message": "...", "history": [...]}
    Returns: {"reply": "..."}
    """
    try:
        message = request_data.get('message', '')
        history = request_data.get('history', [])
        
        # Build conversation messages
        system_prompt = build_system_prompt(config)
        
        messages = [
            {'role': 'system', 'content': system_prompt}
        ]
        
        # Add history
        for msg in history:
            if isinstance(msg, dict):
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                messages.append({'role': role, 'content': content})
        
        # Add user message
        messages.append({'role': 'user', 'content': message})
        
        # Try primary LLM
        base_url = config.get('llm_base_url', DEFAULT_CONFIG['llm_base_url'])
        api_key = config.get('api_key', '')
        model = config.get('model', DEFAULT_CONFIG['model'])
        
        try:
            reply = call_llm(base_url, api_key, model, messages, timeout=120)
            return {"reply": reply}
        except Exception as e:
            # Try fallback
            fallback_url = config.get('fallback_base_url', DEFAULT_CONFIG['fallback_base_url'])
            if fallback_url and fallback_url != base_url:
                try:
                    reply = call_llm(fallback_url, api_key, model, messages, timeout=120)
                    return {"reply": reply}
                except Exception as fallback_e:
                    # Both failed
                    error_msg = f"Both LLM endpoints failed. Primary: {str(e)}, Fallback: {str(fallback_e)}"
                    return {"reply": f"[Error: {html_escape(error_msg)}]"}
            else:
                # No fallback or same as primary
                error_msg = str(e)
                return {"reply": f"[Error: {html_escape(error_msg)}]"}
    
    except Exception as e:
        # Any other error
        error_msg = str(e)
        return {"reply": f"[Error: {html_escape(error_msg)}]"}


class JinxRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for Jinx Companion."""
    
    # Override to disable directory listings and use our own routing
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self._serve_chat_page()
        else:
            # For other files (CSS, JS if we had any), fall back to default
            super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self._send_json_error(400, "Invalid JSON")
            return
        
        # Route based on path
        if self.path == '/chat':
            self._handle_chat_post(request_data)
        elif self.path == '/settings':
            self._handle_settings_post(request_data)
        else:
            self._send_json_error(404, "Not found")
    
    def _serve_chat_page(self):
        """Serve the main chat page with current config."""
        try:
            config = load_config()
            template = get_template('index.html')
            
            # Inject config into template
            config_json = json.dumps(config)
            template = template.replace('{{CONFIG}}', config_json)
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(template.encode('utf-8')))
            self.end_headers()
            self.wfile.write(template.encode('utf-8'))
        except Exception as e:
            self._send_json_error(500, str(e))
    
    def _handle_chat_post(self, request_data):
        """Handle POST /chat."""
        try:
            config = load_config()
            response = handle_chat_request(config, request_data)
            self._send_json(response)
        except Exception as e:
            self._send_json_error(500, str(e))
    
    def _handle_settings_post(self, request_data):
        """Handle POST /settings."""
        try:
            # Merge new settings with existing
            config = load_config()
            config.update(request_data)
            
            if save_config(config):
                self._send_json({"status": "ok", "config": config})
            else:
                self._send_json_error(500, "Failed to save config")
        except Exception as e:
            self._send_json_error(500, str(e))
    
    def _send_json(self, data):
        """Send a JSON response."""
        response = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    def _send_json_error(self, code, message):
        """Send a JSON error response."""
        response = json.dumps({"error": message}).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
    
    # Disable logging to console for cleaner output
    def log_message(self, format, *args):
        pass


def start_server():
    """Start the Jinx Companion server."""
    config = load_config()
    
    print("=" * 60)
    print("Jinx Companion Server")
    print("=" * 60)
    print(f"Server starting on http://{HOST}:{PORT}")
    print(f"LLM Base URL: {config.get('llm_base_url', DEFAULT_CONFIG['llm_base_url'])}")
    print(f"Fallback URL: {config.get('fallback_base_url', DEFAULT_CONFIG['fallback_base_url'])}")
    print(f"Model: {config.get('model', DEFAULT_CONFIG['model'])}")
    print("=" * 60)
    
    # Create server
    handler = JinxRequestHandler
    with socketserver.TCPServer((HOST, PORT), handler) as httpd:
        print(f"Serving on http://{HOST}:{PORT}")
        
        # Open browser in a separate thread
        def open_browser():
            try:
                webbrowser.open(f'http://{HOST}:{PORT}')
            except Exception as e:
                print(f"Could not open browser: {e}")
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        except Exception as e:
            print(f"Server error: {e}")


if __name__ == '__main__':
    start_server()
