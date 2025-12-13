"""
Advanced Keylogger Detector Tool
Detects suspicious processes and file operations
"""

import psutil
import os
from datetime import datetime

class KeyloggerDetector:
    def __init__(self):
        self.suspicious_names = ['keylog', 'logger', 'pynput', 'keyboard']
        self.suspicious_files = ['log.txt', 'keylog', 'keys.txt', 'encrypted_log.txt']
        self.suspicious_handles = []
        self.report = []
    
    def check_processes(self):
        """Check for suspicious processes"""
        print("\n[*] Scanning processes...")
        self.report.append("\n=== PROCESS ANALYSIS ===\n")
        
        suspicious_procs = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                pinfo = proc.info
                proc_name = pinfo['name'].lower()
                
                # Check for suspicious process names
                if any(sus in proc_name for sus in self.suspicious_names):
                    suspicious_procs.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'exe': pinfo['exe'],
                        'cmdline': pinfo['cmdline']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if suspicious_procs:
            print(f"[!] Found {len(suspicious_procs)} suspicious process(es)")
            for proc in suspicious_procs:
                msg = f"⚠ SUSPICIOUS: PID {proc['pid']} - {proc['name']}\n"
                msg += f"   Executable: {proc['exe']}\n"
                msg += f"   Command: {' '.join(proc['cmdline']) if proc['cmdline'] else 'N/A'}\n"
                print(msg)
                self.report.append(msg)
        else:
            msg = "✓ No suspicious processes detected\n"
            print(msg)
            self.report.append(msg)
        
        return suspicious_procs
    
    def check_open_files(self):
        """Check for suspicious file handles"""
        print("\n[*] Scanning open file handles...")
        self.report.append("\n=== FILE HANDLE ANALYSIS ===\n")
        
        suspicious_files_found = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Get open files for each process
                open_files = proc.open_files()
                for file in open_files:
                    filename = os.path.basename(file.path).lower()
                    if any(sus in filename for sus in self.suspicious_files):
                        suspicious_files_found.append({
                            'pid': proc.info['pid'],
                            'process': proc.info['name'],
                            'file': file.path
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if suspicious_files_found:
            print(f"[!] Found {len(suspicious_files_found)} suspicious file handle(s)")
            for item in suspicious_files_found:
                msg = f"⚠ SUSPICIOUS FILE: {item['file']}\n"
                msg += f"   Opened by: {item['process']} (PID: {item['pid']})\n"
                print(msg)
                self.report.append(msg)
        else:
            msg = "✓ No suspicious file handles detected\n"
            print(msg)
            self.report.append(msg)
        
        return suspicious_files_found
    
    def check_network_connections(self):
        """Check for suspicious network connections"""
        print("\n[*] Scanning network connections...")
        self.report.append("\n=== NETWORK CONNECTION ANALYSIS ===\n")
        
        suspicious_connections = []
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.status == 'ESTABLISHED' and conn.pid:
                    proc = psutil.Process(conn.pid)
                    proc_name = proc.name().lower()
                    
                    if any(sus in proc_name for sus in self.suspicious_names):
                        suspicious_connections.append({
                            'pid': conn.pid,
                            'process': proc.name(),
                            'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if suspicious_connections:
            print(f"[!] Found {len(suspicious_connections)} suspicious connection(s)")
            for conn in suspicious_connections:
                msg = f"⚠ SUSPICIOUS CONNECTION: {conn['process']} (PID: {conn['pid']})\n"
                msg += f"   Local: {conn['local']} -> Remote: {conn['remote']}\n"
                print(msg)
                self.report.append(msg)
        else:
            msg = "✓ No suspicious network connections detected\n"
            print(msg)
            self.report.append(msg)
        
        return suspicious_connections
    
    def generate_report(self, output_file="detection_report.txt"):
        """Generate detection report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"\n{'='*60}\n"
        header += f"KEYLOGGER DETECTION REPORT\n"
        header += f"Generated: {timestamp}\n"
        header += f"{'='*60}\n"
        
        full_report = header + ''.join(self.report)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        print(f"\n[✓] Report saved to: {output_file}")
        return full_report
    
    def run_full_scan(self):
        """Run complete detection scan"""
        print("\n" + "="*60)
        print("ADVANCED KEYLOGGER DETECTOR")
        print("="*60)
        
        procs = self.check_processes()
        files = self.check_open_files()
        conns = self.check_network_connections()
        
        print("\n" + "="*60)
        print("SCAN SUMMARY")
        print("="*60)
        
        summary = f"\nSuspicious Processes: {len(procs)}\n"
        summary += f"Suspicious File Handles: {len(files)}\n"
        summary += f"Suspicious Connections: {len(conns)}\n"
        
        if procs or files or conns:
            summary += "\n⚠ THREAT DETECTED! Review the findings above.\n"
        else:
            summary += "\n✓ No threats detected. System appears clean.\n"
        
        print(summary)
        self.report.append("\n" + summary)
        
        self.generate_report()

def main():
    detector = KeyloggerDetector()
    detector.run_full_scan()

if __name__ == "__main__":
    main()