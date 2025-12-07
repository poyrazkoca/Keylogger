# Detection Techniques

## 1. Process Explorer (Effective)
As noted in our findings, standard Task Manager is insufficient.
1. Open **Sysinternals Process Explorer**.
2. Go to **Find** > **Find Handle or DLL**.
3. Search for `key_log.txt`.
4. [cite_start]**Result:** The tool identifies the `python.exe` process holding the handle to our log file, revealing the malware[cite: 114].

## 2. Network Monitoring (N/A)
[cite_start]Since this project is scoped for local logging only[cite: 28], network monitoring tools (Wireshark) will show no traffic, confirming the "Scope Limitation" compliance.