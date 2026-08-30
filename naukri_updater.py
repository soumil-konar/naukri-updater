import time
import os
from playwright.sync_api import sync_playwright

AUTH_FILE = "naukri_auth.json"

def refresh_naukri_profile():
    # If NAUKRI_AUTH_JSON secret/env is provided and file doesn't exist, create it
    if not os.path.exists(AUTH_FILE) and os.environ.get("NAUKRI_AUTH_JSON"):
        print("[+] Creating session state file from NAUKRI_AUTH_JSON environment variable...")
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            f.write(os.environ.get("NAUKRI_AUTH_JSON"))

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

        # Give it a moment to load dynamic scripts
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