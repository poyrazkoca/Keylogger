"""
Keylogger Log Analyzer and Visualizer
Analyzes keystroke patterns and generates visualizations
"""

import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

class LogAnalyzer:
    def __init__(self, log_file="decrypted_log.txt"):
        self.log_file = log_file
        self.data = self.load_log()
        
    def load_log(self):
        """Load log file"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: {self.log_file} not found!")
            print("Please run decrypt_log.py first!")
            return ""
    
    def extract_timestamps(self):
        """Extract timestamps from log"""
        pattern = r'\[(\d{2}:\d{2}:\d{2})\]'
        timestamps = re.findall(pattern, self.data)
        return timestamps
    
    def count_keystrokes(self):
        """Count total keystrokes"""
        timestamps = self.extract_timestamps()
        return len(timestamps)
    
    def count_special_keys(self):
        """Count special key usage"""
        special_keys = {
            'ENTER': len(re.findall(r'\[ENTER\]', self.data)),
            'BACKSPACE': len(re.findall(r'\[BACKSPACE\]', self.data)),
            'TAB': len(re.findall(r'\[TAB\]', self.data)),
            'SHIFT': len(re.findall(r'\[SHIFT\]', self.data)),
            'CTRL': len(re.findall(r'\[CTRL\]', self.data)),
            'CAPSLOCK': len(re.findall(r'\[CAPSLOCK\]', self.data))
        }
        return special_keys
    
    def analyze_typing_speed(self):
        """Analyze typing speed over time"""
        timestamps = self.extract_timestamps()
        if len(timestamps) < 2:
            return []
        
        hourly_counts = {}
        for ts in timestamps:
            hour = ts.split(':')[0]
            hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
        
        return sorted(hourly_counts.items())
    
    def get_most_common_chars(self, top_n=10):
        """Get most frequently pressed characters"""
        # Extract all characters (excluding special keys)
        chars = re.findall(r'\] ([a-zA-Z0-9])', self.data)
        counter = Counter(chars)
        return counter.most_common(top_n)
    
    def generate_report(self):
        """Generate analysis report"""
        print("\n" + "="*60)
        print("KEYSTROKE LOG ANALYSIS REPORT")
        print("="*60 + "\n")
        
        total = self.count_keystrokes()
        print(f"Total Keystrokes: {total}")
        
        special = self.count_special_keys()
        print("\nSpecial Keys Usage:")
        for key, count in special.items():
            print(f"  {key}: {count}")
        
        common_chars = self.get_most_common_chars()
        print("\nMost Common Characters:")
        for char, count in common_chars:
            print(f"  '{char}': {count} times")
        
        typing_speed = self.analyze_typing_speed()
        print("\nHourly Activity:")
        for hour, count in typing_speed:
            print(f"  {hour}:00 - {count} keystrokes")
    
    def visualize_data(self):
        """Create visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Keylogger Data Analysis', fontsize=16, fontweight='bold')
        
        # 1. Special Keys Usage
        special = self.count_special_keys()
        axes[0, 0].bar(special.keys(), special.values(), color='#FF6B6B')
        axes[0, 0].set_title('Special Keys Usage', fontweight='bold')
        axes[0, 0].set_xlabel('Key Type')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Most Common Characters
        common_chars = self.get_most_common_chars()
        chars, counts = zip(*common_chars) if common_chars else ([], [])
        axes[0, 1].bar(chars, counts, color='#4ECDC4')
        axes[0, 1].set_title('Most Common Characters', fontweight='bold')
        axes[0, 1].set_xlabel('Character')
        axes[0, 1].set_ylabel('Frequency')
        
        # 3. Hourly Activity
        typing_speed = self.analyze_typing_speed()
        if typing_speed:
            hours, counts = zip(*typing_speed)
            axes[1, 0].plot(hours, counts, marker='o', linewidth=2, color='#95E1D3')
            axes[1, 0].fill_between(range(len(hours)), counts, alpha=0.3, color='#95E1D3')
            axes[1, 0].set_title('Keystroke Activity by Hour', fontweight='bold')
            axes[1, 0].set_xlabel('Hour')
            axes[1, 0].set_ylabel('Keystrokes')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Summary Statistics
        total = self.count_keystrokes()
        special_total = sum(special.values())
        regular = total - special_total
        
        sizes = [regular, special_total]
        labels = ['Regular Keys', 'Special Keys']
        colors = ['#FFD93D', '#FF6B6B']
        
        axes[1, 1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                      startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        axes[1, 1].set_title('Key Type Distribution', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('keystroke_analysis.png', dpi=300, bbox_inches='tight')
        print("\n[✓] Visualization saved as 'keystroke_analysis.png'")
        plt.show()

def main():
    analyzer = LogAnalyzer()
    analyzer.generate_report()
    
    # Generate visualizations
    try:
        analyzer.visualize_data()
    except Exception as e:
        print(f"\n[!] Could not generate visualizations: {e}")

if __name__ == "__main__":
    main()