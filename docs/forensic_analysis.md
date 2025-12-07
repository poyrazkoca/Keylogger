# Forensic Analysis Report: Keylogger Artifacts & Removal

**Project Phase:** Phase 4 (Analysis and Reporting)
**Subject:** Custom Python Keylogger (`simple_logger.py`)

## 1. Executive Summary
This report documents the forensic artifacts left behind by the execution of the custom keylogger developed in Phase 1. The analysis confirms that the malware operates locally, creating specific file system and memory artifacts, but leaves no network or registry footprints, complying with the project's scope limitations.

## 2. Artifacts Discovered

### A. File System Artifacts
The primary indicator of compromise (IOC) is the creation of a log file containing captured keystrokes.
* **File Name:** `key_log.txt` 
* **Location:** `...\logs\key_log.txt`
* **Content:** Plaintext log entries with timestamps (e.g., `2025-11-29 14:30:01 : [ENTER]`).
* **Creation Time:** Corresponds to the execution start time of the script.

### B. Memory & Process Artifacts
The keylogger runs as a Python script, which obfuscates its presence under a generic system process name.
* **Process Name:** `python.exe` (or `pythonw.exe` if run in background).
* **Command Line Argument:** The full command line reveals the script path: `python.exe ...\src\simple_logger.py`.
* **Open Handles:** Using **Process Explorer**, the process was found to hold an exclusive lock on the `key_log.txt` file, which served as the "smoking gun" for detection.

### C. Persistence Mechanisms (Registry/Startup)
* **Finding:** None.
* **Analysis:** Consistent with the project scope, no keys were added to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`. The malware does not survive a system reboot.

### D. Network Artifacts
* **Finding:** None.
* **Analysis:** No outbound TCP/UDP connections were initiated. [cite_start]Wireshark traces remained silent regarding this process, confirming the air-gapped nature of the threat.

## 3. Removal & Remediation (Incident Response)

To effectively remove the keylogger from the infected system, the following procedure was established:

1.  **Terminate the Process:**
    * Open **Task Manager** or **Process Explorer**.
    * Locate the `python.exe` process.
    * *Verification:* Check the "Command Line" column to ensure it is running `simple_logger.py`.
    * Right-click and select **End Task** (or **Kill Process**).

2.  **Delete Malicious Files:**
    * Navigate to the directory containing the script.
    * Delete `simple_logger.py`.
    * Delete the `logs` folder containing `key_log.txt`.

3.  **Sanitize Environment:**
    * Empty the Recycle Bin to prevent recovery.
    * (Optional) Run a full scan with Windows Defender to ensure no secondary payloads were introduced (though none were part of this project).

## 4. Conclusion
The forensic analysis demonstrates that while the keylogger is effective at capturing input, it is "noisy" in terms of file system changes. The lack of persistence and rootkit-like hiding techniques makes it vulnerable to detection by standard tools like Process Explorer, provided the analyst knows what to look for (open file handles).