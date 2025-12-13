"""
Log Decryptor Tool
Decrypts and displays encrypted keylogger logs
"""

from cryptography.fernet import Fernet
import sys

def decrypt_log(log_file="encrypted_log.txt", key_file="secret.key", output_file="decrypted_log.txt"):
    """Decrypt the encrypted log file"""
    try:
        # Load encryption key
        with open(key_file, 'rb') as f:
            key = f.read()
        
        cipher = Fernet(key)
        
        # Read and decrypt log file
        with open(log_file, 'rb') as f:
            encrypted_lines = f.readlines()
        
        decrypted_content = []
        for line in encrypted_lines:
            if line.strip():
                try:
                    decrypted = cipher.decrypt(line.strip()).decode()
                    decrypted_content.append(decrypted)
                except Exception as e:
                    print(f"Error decrypting line: {e}")
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(decrypted_content))
        
        print(f"\n✓ Successfully decrypted log file!")
        print(f"✓ Output saved to: {output_file}")
        print(f"\n--- DECRYPTED CONTENT ---\n")
        print(''.join(decrypted_content))
        
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        decrypt_log(log_file=sys.argv[1])
    else:
        decrypt_log()