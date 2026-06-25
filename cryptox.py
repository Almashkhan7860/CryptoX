#!/usr/bin/env python3
# ============================================
#   CryptoX - Hash & Encryption Tool
#   By: Almash Coder
#   For: Cybersecurity Learners & CTF Players
# ============================================

import hashlib
import bcrypt
import os
import sys
from cryptography.fernet import Fernet
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
  ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██╗  ██╗
 ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗╚██╗██╔╝
 ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║ ╚███╔╝ 
 ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║ ██╔██╗ 
 ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██╔╝ ██╗
  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Fore.YELLOW}        Hash Identifier | Decryptor | Encryptor Tool
{Fore.RED}        [ For Educational & CTF Purposes Only ]
{Style.RESET_ALL}
"""

def identify_hash(h):
    """Identifies common hash types based on length and signatures."""
    length = len(h)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    elif length == 128:
        return "SHA512"
    elif h.startswith("$2b$") or h.startswith("$2a$") or h.startswith("$2y$"):
        return "BCRYPT"
    else:
        return "Unknown"

def generate_hash():
    print(f"\n{Fore.CYAN}[ Hash Generator ]{Style.RESET_ALL}")
    text = input(f"{Fore.YELLOW}Text daalo: {Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}MD5     : {hashlib.md5(text.encode()).hexdigest()}")
    print(f"SHA1    : {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"SHA256  : {hashlib.sha256(text.encode()).hexdigest()}")
    print(f"SHA512  : {hashlib.sha512(text.encode()).hexdigest()}")

    # Bcrypt returns bytes, decoding for clean presentation
    hashed = bcrypt.hashpw(text.encode(), bcrypt.gensalt())
    print(f"BCRYPT  : {hashed.decode()}{Style.RESET_ALL}")

def crack_hash():
    print(f"\n{Fore.CYAN}[ Hash Cracker ]{Style.RESET_ALL}")
    print(f"{Fore.RED}[!] Sirf apne hashes test karo!{Style.RESET_ALL}\n")

    target = input(f"{Fore.YELLOW}Hash daalo: {Style.RESET_ALL}").strip()
    hash_type = identify_hash(target)
    print(f"{Fore.CYAN}[*] Hash Type: {hash_type}{Style.RESET_ALL}")

    if hash_type == "Unknown":
        print(f"{Fore.RED}[!] Unsupported format or invalid hash.{Style.RESET_ALL}")
        return

    wordlist = input(f"{Fore.YELLOW}Wordlist file path (ya Enter for default): {Style.RESET_ALL}").strip()

    if not wordlist:
        words = ["password", "123456", "admin", "letmein",
                 "qwerty", "abc123", "password123", "root",
                 "toor", "test", "hello", "welcome", "1234"]
    else:
        try:
            with open(wordlist, "r", errors="ignore") as f:
                words = f.read().splitlines()
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Wordlist file nahi mili!{Style.RESET_ALL}")
            return

    print(f"\n{Fore.CYAN}[*] Cracking shuru...{Style.RESET_ALL}")
    
    for word in words:
        found = False
        try:
            if hash_type == "MD5":
                if hashlib.md5(word.encode()).hexdigest() == target:
                    found = True
            elif hash_type == "SHA1":
                if hashlib.sha1(word.encode()).hexdigest() == target:
                    found = True
            elif hash_type == "SHA256":
                if hashlib.sha256(word.encode()).hexdigest() == target:
                    found = True
            elif hash_type == "SHA512":
                if hashlib.sha512(word.encode()).hexdigest() == target:
                    found = True
            elif hash_type == "BCRYPT":
                # Bcrypt comparisons require the targeted hash as the second argument
                if bcrypt.checkpw(word.encode(), target.encode()):
                    found = True
        except Exception:
            continue

        if found:
            print(f"\n{Fore.GREEN}[✓] Password Mila: {word}{Style.RESET_ALL}")
            return

    print(f"{Fore.RED}[✗] Password nahi mila wordlist mein!{Style.RESET_ALL}")

def file_encryptor():
    print(f"\n{Fore.CYAN}[ File Encryptor/Decryptor ]{Style.RESET_ALL}")
    print(f"1. File Encrypt karo")
    print(f"2. File Decrypt karo")
    choice = input(f"\n{Fore.YELLOW}Choose: {Style.RESET_ALL}")

    if choice == "1":
        filepath = input(f"{Fore.YELLOW}File path: {Style.RESET_ALL}").strip()
        if not os.path.exists(filepath):
            print(f"{Fore.RED}[!] Target file exist nahi karti!{Style.RESET_ALL}")
            return
        try:
            key = Fernet.generate_key()
            f = Fernet(key)
            with open(filepath, "rb") as file:
                data = file.read()
            encrypted = f.encrypt(data)
            with open(filepath + ".encrypted", "wb") as file:
                file.write(encrypted)
            with open("secret.key", "wb") as kf:
                kf.write(key)
            print(f"{Fore.GREEN}[✓] File encrypt ho gayi: {filepath}.encrypted")
            print(f"[✓] Key save hui: secret.key (MAT BHOOLNA!){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

    elif choice == "2":
        filepath = input(f"{Fore.YELLOW}Encrypted file path: {Style.RESET_ALL}").strip()
        keypath = input(f"{Fore.YELLOW}Key file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(filepath) or not os.path.exists(keypath):
            print(f"{Fore.RED}[!] Missing file or missing key structural paths!{Style.RESET_ALL}")
            return
        try:
            with open(keypath, "rb") as kf:
                key = kf.read()
            f = Fernet(key)
            with open(filepath, "rb") as file:
                data = file.read()
            decrypted = f.decrypt(data)
            out = filepath.replace(".encrypted", ".decrypted")
            if out == filepath:
                out = filepath + ".decrypted"
            with open(out, "wb") as file:
                file.write(decrypted)
            print(f"{Fore.GREEN}[✓] File decrypt ho gayi: {out}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def text_encryptor():
    print(f"\n{Fore.CYAN}[ Text Encryptor/Decryptor ]{Style.RESET_ALL}")
    print("1. Text Encrypt karo")
    print("2. Text Decrypt karo")
    choice = input(f"\n{Fore.YELLOW}Choose: {Style.RESET_ALL}")

    if choice == "1":
        text = input(f"{Fore.YELLOW}Text daalo: {Style.RESET_ALL}")
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted = f.encrypt(text.encode()).decode()
        print(f"\n{Fore.GREEN}[✓] Encrypted: {encrypted}")
        print(f"[✓] Key: {key.decode()}")
        print(f"{Fore.RED}[!] Key save kar lo!{Style.RESET_ALL}")

    elif choice == "2":
        encrypted = input(f"{Fore.YELLOW}Encrypted text: {Style.RESET_ALL}").strip().encode()
        key = input(f"{Fore.YELLOW}Key daalo: {Style.RESET_ALL}").strip().encode()
        try:
            f = Fernet(key)
            decrypted = f.decrypt(encrypted).decode()
            print(f"\n{Fore.GREEN}[✓] Decrypted: {decrypted}{Style.RESET_ALL}")
        except Exception:
            print(f"{Fore.RED}[!] Wrong key ya corrupted data!{Style.RESET_ALL}")

def main():
    print(BANNER)
    while True:
        print(f"\n{Fore.CYAN}{'─'*45}")
        print(f"  1. 🔍 Hash Identify Karo")
        print(f"  2. 🔨 Hash Generate Karo")
        print(f"  3. 💥 Hash Crack Karo (Wordlist)")
        print(f"  4. 📁 File Encrypt/Decrypt")
        print(f"  5. 💬 Text Encrypt/Decrypt")
        print(f"  6. 🚪 Exit")
        print(f"{'─'*45}{Style.RESET_ALL}")

        choice = input(f"\n{Fore.YELLOW}[CryptoX]> {Style.RESET_ALL}")

        if choice == "1":
            h = input(f"{Fore.YELLOW}Hash daalo: {Style.RESET_ALL}").strip()
            print(f"{Fore.GREEN}[*] Type: {identify_hash(h)}{Style.RESET_ALL}")
        elif choice == "2":
            generate_hash()
        elif choice == "3":
            crack_hash()
        elif choice == "4":
            file_encryptor()
        elif choice == "5":
            text_encryptor()
        elif choice == "6":
            print(f"{Fore.RED}\n[!] Thanks For Use ! 👋{Style.RESET_ALL}")
            sys.exit()
        else:
            print(f"{Fore.RED}[!] Wrong choice!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
