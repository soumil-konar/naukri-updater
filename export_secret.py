import os
import gzip
import base64

AUTH_FILE = "naukri_auth.json"

def export_compressed_secret():
    if not os.path.exists(AUTH_FILE):
        print(f"[!] Error: '{AUTH_FILE}' not found. Please run 'python save_session.py' first.")
        return

    with open(AUTH_FILE, "rb") as f:
        raw_data = f.read()

    compressed = gzip.compress(raw_data)
    encoded = base64.b64encode(compressed).decode("utf-8")

    print("=================================================================")
    print("👉 COPY THE STRING BELOW AND PASTE IT AS YOUR 'NAUKRI_AUTH_JSON' SECRET:")
    print("=================================================================\n")
    print(encoded)
    print("\n=================================================================")
    print(f"[✓] Original Size: {len(raw_data)} bytes -> Compressed: {len(encoded)} characters")
    print("=================================================================")

if __name__ == "__main__":
    export_compressed_secret()
