"""
Performance Benchmark Tool for Keylogger
Measures CPU, memory, and disk impact
"""

import psutil
import time
import os
from datetime import datetime

class PerformanceBenchmark:
    def __init__(self, duration=30):
        self.duration = duration
        self.samples = []
        
    def find_keylogger_process(self):
        """Find the keylogger process"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info.get('cmdline', [])).lower()
                    if 'keylogger' in cmdline:
                        return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return None
    
    def measure_baseline(self):
        """Measure system baseline without keylogger"""
        print("="*70)
        print("PERFORMANCE BENCHMARK - BASELINE MEASUREMENT")
        print("="*70)
        print("\n[*] Measuring system baseline (10 seconds)...\n")
        
        cpu_samples = []
        mem_samples = []
        
        for i in range(10):
            cpu_samples.append(psutil.cpu_percent(interval=1))
            mem_samples.append(psutil.virtual_memory().percent)
            print(f"    Sample {i+1}/10: CPU={cpu_samples[-1]:.1f}% RAM={mem_samples[-1]:.1f}%")
        
        baseline = {
            'cpu': sum(cpu_samples) / len(cpu_samples),
            'memory': sum(mem_samples) / len(mem_samples)
        }
        
        print(f"\n[+] Baseline CPU Usage: {baseline['cpu']:.2f}%")
        print(f"[+] Baseline Memory Usage: {baseline['memory']:.2f}%\n")
        
        return baseline
    
    def monitor_performance(self, process):
        """Monitor keylogger performance"""
        print("="*70)
        print("PERFORMANCE BENCHMARK - KEYLOGGER RUNNING")
        print("="*70)
        print(f"\n[*] Monitoring for {self.duration} seconds...")
        print("[*] Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        sample_count = 0
        
        try:
            while (time.time() - start_time) < self.duration:
                try:
                    cpu_percent = process.cpu_percent(interval=1)
                    mem_info = process.memory_info()
                    mem_mb = mem_info.rss / 1024 / 1024
                    
                    io_counters = process.io_counters()
                    
                    sample = {
                        'timestamp': datetime.now(),
                        'cpu_percent': cpu_percent,
                        'memory_mb': mem_mb,
                        'read_bytes': io_counters.read_bytes,
                        'write_bytes': io_counters.write_bytes
                    }
                    
                    self.samples.append(sample)
                    sample_count += 1
                    
                    elapsed = time.time() - start_time
                    remaining = self.duration - elapsed
                    print(f"\rSample {sample_count}: CPU={cpu_percent:.1f}% | RAM={mem_mb:.1f}MB | Remaining={remaining:.0f}s   ", end='')
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    print("\n[!] Process terminated or access denied")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n[*] Monitoring stopped by user")
        
        print(f"\n\n[+] Collected {len(self.samples)} samples\n")
    
    def analyze_results(self, baseline):
        """Analyze and display performance results"""
        if not self.samples:
            print("[!] No samples collected")
            return None
        
        print("="*70)
        print("PERFORMANCE ANALYSIS RESULTS")
        print("="*70)
        print()
        
        cpu_values = [s['cpu_percent'] for s in self.samples]
        mem_values = [s['memory_mb'] for s in self.samples]
        
        stats = {
            'cpu_avg': sum(cpu_values) / len(cpu_values),
            'cpu_max': max(cpu_values),
            'cpu_min': min(cpu_values),
            'mem_avg': sum(mem_values) / len(mem_values),
            'mem_max': max(mem_values),
            'mem_min': min(mem_values)
        }
        
        if len(self.samples) > 1:
            first_sample = self.samples[0]
            last_sample = self.samples[-1]
            
            total_read = (last_sample['read_bytes'] - first_sample['read_bytes']) / 1024 / 1024
            total_write = (last_sample['write_bytes'] - first_sample['write_bytes']) / 1024 / 1024
            duration = (last_sample['timestamp'] - first_sample['timestamp']).total_seconds()
            
            stats['disk_read_mb'] = total_read
            stats['disk_write_mb'] = total_write
            stats['duration'] = duration
        
        print("[CPU USAGE]")
        print(f"  Average: {stats['cpu_avg']:.2f}%")
        print(f"  Maximum: {stats['cpu_max']:.2f}%")
        print(f"  Minimum: {stats['cpu_min']:.2f}%")
        
        if baseline:
            cpu_overhead = stats['cpu_avg'] - baseline['cpu']
            print(f"  Overhead vs Baseline: +{cpu_overhead:.2f}%")
        
        print()
        
        print("[MEMORY USAGE]")
        print(f"  Average: {stats['mem_avg']:.2f} MB")
        print(f"  Maximum: {stats['mem_max']:.2f} MB")
        print(f"  Minimum: {stats['mem_min']:.2f} MB")
        print()
        
        if 'disk_read_mb' in stats:
            print("[DISK I/O]")
            print(f"  Total Read: {stats['disk_read_mb']:.2f} MB")
            print(f"  Total Write: {stats['disk_write_mb']:.2f} MB")
            print(f"  Duration: {stats['duration']:.1f} seconds")
            print()
        
        print("[PERFORMANCE RATING]")
        
        rating_points = 100
        
        if stats['cpu_avg'] > 10:
            rating_points -= 30
            cpu_rating = "POOR"
        elif stats['cpu_avg'] > 5:
            rating_points -= 15
            cpu_rating = "FAIR"
        elif stats['cpu_avg'] > 2:
            rating_points -= 5
            cpu_rating = "GOOD"
        else:
            cpu_rating = "EXCELLENT"
        
        if stats['mem_avg'] > 100:
            rating_points -= 20
            mem_rating = "POOR"
        elif stats['mem_avg'] > 50:
            rating_points -= 10
            mem_rating = "FAIR"
        elif stats['mem_avg'] > 25:
            rating_points -= 5
            mem_rating = "GOOD"
        else:
            mem_rating = "EXCELLENT"
        
        print(f"  CPU Impact: {cpu_rating} ({stats['cpu_avg']:.2f}%)")
        print(f"  Memory Impact: {mem_rating} ({stats['mem_avg']:.1f} MB)")
        print(f"\n  Overall Score: {rating_points}/100")
        
        if rating_points >= 90:
            print(f"  Verdict: EXCELLENT - Minimal system impact")
        elif rating_points >= 75:
            print(f"  Verdict: GOOD - Acceptable performance")
        elif rating_points >= 60:
            print(f"  Verdict: FAIR - Noticeable impact")
        else:
            print(f"  Verdict: POOR - Significant system impact")
        
        print()
        print("="*70)
        
        return stats

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║        KEYLOGGER PERFORMANCE BENCHMARK TOOL v1.0              ║
    ║        System Impact Analysis & Resource Monitoring           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    benchmark = PerformanceBenchmark(duration=30)
    
    baseline = benchmark.measure_baseline()
    
    input("\n[*] Start the keylogger NOW, then press ENTER to begin monitoring...")
    
    print("\n[*] Searching for keylogger process...")
    process = benchmark.find_keylogger_process()
    
    if not process:
        print("[!] Keylogger process not found!")
        print("[!] Make sure keylogger.py is running")
        return
    
    print(f"[+] Found process: {process.info['name']} (PID: {process.pid})\n")
    
    benchmark.monitor_performance(process)
    
    stats = benchmark.analyze_results(baseline)
    
    print("[+] Benchmark complete!\n")

if __name__ == "__main__":
    main()