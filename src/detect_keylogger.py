import psutil

suspicious_processes = ["python.exe", "keylogger", "pynput", "keyboard"]

print("Scanning running processes...\n")

found = False
for proc in psutil.process_iter(['name', 'cmdline']):
    try:
        name = proc.info['name']
        cmdline = proc.info['cmdline']
        
        # Handle None cmdline
        cmd = " ".join(cmdline) if cmdline else ""

        for keyword in suspicious_processes:
            if keyword.lower() in name.lower() or keyword.lower() in cmd.lower():
                print(f"[!] Suspicious process detected: {name}")
                print(f"    Command: {cmd}")
                print()
                found = True

    except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
        pass

if not found:
    print("No suspicious activity detected.")