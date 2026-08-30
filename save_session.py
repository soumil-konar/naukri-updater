from playwright.sync_api import sync_playwright

def save_session():
    with sync_playwright() as p:
        # Launch Chromium with custom user agent
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("[+] Opening Naukri login page...")
        page.goto("https://www.naukri.com/nlogin/login")

        print("\n=======================================================")
        print("👉 Please log in using Google in the opened browser window.")
        print("👉 Once your dashboard/profile loads, press ENTER in this terminal.")
        print("=======================================================\n")
        
        input("Press Enter here AFTER you have successfully logged in: ")

        # Save the cookies and session state
        context.storage_state(path="naukri_auth.json")
        print("[✓] Session state successfully saved to 'naukri_auth.json'!")
        browser.close()

if __name__ == "__main__":
    save_session()