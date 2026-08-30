# Naukri Profile Auto-Refresher

An automated script that keeps your Naukri profile active and visible at the top of recruiter searches by periodically updating the resume headline.

## Features
- **Headless Automation**: Runs seamlessly locally and on GitHub Actions.
- **Session-Based Auth**: Uses saved Playwright session cookies so 2FA/Google login isn't needed on each run.
- **Scheduled GitHub Actions Workflow**: Refreshes your profile automatically twice every day (10:00 AM & 5:30 PM IST).

## Setup & Local Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Save Login Session:**
   ```bash
   python save_session.py
   ```
   Follow the prompt in the browser to log in to Naukri. This generates `naukri_auth.json`.

3. **Run Updater:**
   ```bash
   python naukri_updater.py
   ```

## GitHub Actions Deployment

1. Create a **Private** repository on GitHub.
2. Go to **Settings > Secrets and variables > Actions** in your repository.
3. Add a new repository secret named `NAUKRI_AUTH_JSON` and paste the full contents of your local `naukri_auth.json`.
4. Push your code to GitHub.
5. Trigger manually from the **Actions** tab or let the scheduled cron job run automatically.
