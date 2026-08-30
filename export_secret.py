import os
import gzip
import base64
import subprocess

AUTH_FILE = "naukri_auth.json"
OUTPUT_FILE = "secret_for_github.txt"

def export_compressed_secret():
    if not os.path.exists(AUTH_FILE):
        print(f"[!] Error: '{AUTH_FILE}' not found. Please run 'python save_session.py' first.")
        return

    with open(AUTH_FILE, "rb") as f:
        raw_data = f.read()

    compressed = gzip.compress(raw_data)
    encoded = base64.b64encode(compressed).decode("utf-8")

    # Save to a clean dedicated file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(encoded)

    # Attempt to copy to clipboard if wl-copy / xclip is present
    copied_to_clipboard = False
    try:
        proc = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
        proc.communicate(encoded.encode("utf-8"))
        if proc.returncode == 0:
            copied_to_clipboard = True
    except Exception:
        pass

    print("\n" + "=" * 65)
    if copied_to_clipboard:
        print("📋 Secret has been COPIED to your clipboard automatically!")
    else:
        print(f"📄 Clean secret saved to file: '{OUTPUT_FILE}'")
    print(f"📦 Size: {len(raw_data)} bytes -> Compressed: {len(encoded)} characters")
    print("=" * 65)
    print("\n👉 Paste this into GitHub Secret 'NAUKRI_AUTH_JSON':\n")
    print(encoded)
    print("\n" + "=" * 65 + "\n")

if __name__ == "__main__":
    export_compressed_secret()
