# Keylogger Detection & Prevention Project

A simple educational keylogger implementation with detection capabilities, designed for cybersecurity learning in a controlled VM environment.

## ⚠️ Disclaimer

This project is for **educational purposes only**. It demonstrates how keyloggers work and how to detect them. 

- **Only run in a virtual machine (VM)**
- **Never use on systems you don't own**
- **Unauthorized keylogging is illegal**
- This tool is meant for learning cybersecurity concepts

## 🎯 Project Features

### Keylogger (`keylogger.py`)
✅ Logs keystrokes to a local text file
✅ Takes screenshots on every mouse click
✅ Captures both regular characters and special keys
✅ Organized screenshot storage with timestamps
✅ Clean, readable log format

### Detection Script (`detect_keylogger.py`)
✅ Scans running processes for suspicious activity
✅ Identifies Python-based keyloggers
✅ Detects pynput and keyboard libraries in use
✅ Shows matched keywords and process details

### performance metrics (`performance_benchmark.py`)
✅ Makes CPU, RAM, memory and time measurements
✅ Comparison between before/after

## 📋 Requirements

- Python 3.14
- Windows OS (tested on Windows VM Home)

## 💻 Usage

### Running the Keylogger

**⚠️ Only run in a VM!**

```bash
python keylogger.py
```

- Logs will be saved to `log.txt`
- Screenshots will be saved in `screenshots/` folder
- Press `Ctrl+C` to stop

### Detecting the Keylogger

In a separate terminal:

```bash
python detect_keylogger.py
```

This will scan for suspicious processes and alert you if the keylogger is running.

## 🔧 How It Works

### Keylogger
1. Uses `pynput` to monitor keyboard and mouse events
2. Logs keystrokes with proper character handling
3. Captures screenshots using PIL's `ImageGrab` on mouse clicks
4. Stores everything locally in organized files

### Detection
1. Uses `psutil` to enumerate running processes
2. Checks process names and command lines for suspicious keywords
3. Identifies Python processes running keylogger-related code
4. Reports findings with PID and matched keywords

## 🛡️ Defense Mechanisms

This project demonstrates:
- How keyloggers capture data
- How to detect suspicious processes
- Basic process monitoring techniques
- Importance of security awareness

## 📝 Sample Output

### Keylogger Log (`log.txt`)
```
Hello World This is a test
[2024-12-13 10:30:45] - Mouse Click at (500, 300) - screenshot saved
username123[TAB]password456[ENTER]
```

### Detection Output
```
Scanning running processes...

[!] Suspicious process detected: python.exe (PID: 12345)
    Matched keywords: python.exe, keylogger, pynput
    Command: C:\Users\...\keylogger.py

Total suspicious processes found: 1
```

## 🎓 Learning Objectives

- Understanding how keyloggers operate
- Process monitoring and detection techniques
- Python programming for security tools
- Ethical considerations in cybersecurity
- Importance of running suspicious code in isolated environments

## ⚖️ Legal Notice

**This software is provided for educational purposes only.** Unauthorized access to computer systems is illegal. Always obtain proper authorization before testing security tools. The authors are not responsible for misuse of this software.

---

**Remember: Always practice ethical hacking and respect privacy laws!** 🔒

