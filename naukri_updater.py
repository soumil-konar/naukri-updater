import time
import os
import gzip
import base64
from playwright.sync_api import sync_playwright

AUTH_FILE = "naukri_auth.json"

def restore_auth_file():
    """Restores naukri_auth.json from NAUKRI_AUTH_JSON secret (supports raw JSON or base64+gzip)."""
    if not os.path.exists(AUTH_FILE) and os.environ.get("NAUKRI_AUTH_JSON"):
        auth_data = os.environ.get("NAUKRI_AUTH_JSON").strip()
        try:
            # Try decompressing base64+gzipped payload first
            decompressed = gzip.decompress(base64.b64decode(auth_data)).decode("utf-8")
            with open(AUTH_FILE, "w", encoding="utf-8") as f:
                f.write(decompressed)
            print("[+] Session state restored from compressed secret.")
        except Exception:
            # Fall back to raw JSON string
            with open(AUTH_FILE, "w", encoding="utf-8") as f:
                f.write(auth_data)
            print("[+] Session state restored from raw JSON secret.")

def refresh_naukri_profile():
    restore_auth_file()

    if not os.path.exists(AUTH_FILE):
        print(f"[!] Error: '{AUTH_FILE}' not found. Please run 'python save_session.py' locally or set NAUKRI_AUTH_JSON secret.")
        return

    # Check headless mode: defaults to True for CI / server environments
    headless_env = os.environ.get("HEADLESS", "true").strip().lower()
    is_headless = headless_env not in ["false", "0", "no"]

    print(f"[+] Starting Playwright (Headless: {is_headless})...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=is_headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        context = browser.new_context(
            storage_state=AUTH_FILE,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("[+] Navigating directly to profile page...")
        page.goto("https://www.naukri.com/mnjuser/profile", wait_until="domcontentloaded", timeout=60000)

        # Wait for dynamic components to settle
        page.wait_for_timeout(3000)

        if "login" in page.url:
            print("[!] Session expired or login required. Please re-run 'python save_session.py' and update your GitHub secret.")
            browser.close()
            return

        print("[+] Session active. Locating Resume Headline section...")
        page.wait_for_selector("div.resumeHeadline", timeout=15000)
        headline_card = page.locator("div.resumeHeadline")
        edit_button = headline_card.locator("span.edit.icon").first
        edit_button.click()

        # Wait for headline text area
        page.wait_for_selector("#resumeHeadlineTxt", state="visible", timeout=10000)
        current_headline = page.input_value("#resumeHeadlineTxt").strip()
        print(f"[+] Current Headline: {current_headline}")

        # Toggle trailing period to register a modification
        if current_headline.endswith("."):
            updated_headline = current_headline[:-1]
        else:
            updated_headline = current_headline + "."

        page.fill("#resumeHeadlineTxt", updated_headline)
        time.sleep(1)

        # Target the specific Save button inside the Resume Headline form/modal
        save_button = page.locator("form[name='resumeHeadlineForm'] button:has-text('Save'), div.action button.btn-dark-ot:has-text('Save')").first
        save_button.click()

        print("[+] Saved changes. Finalizing...")
        page.wait_for_timeout(3000)

        context.storage_state(path=AUTH_FILE)
        print(f"[✓] Profile successfully refreshed at {time.strftime('%Y-%m-%d %H:%M:%S')}!")
        browser.close()

if __name__ == "__main__":
    refresh_naukri_profile()