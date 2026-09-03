"""
Core Hypeddit Download Engine using Playwright
"""

import os
import sys
import time
import random
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

MODULE_DIR = Path(__file__).parent
BYPASSER_JS_PATH = MODULE_DIR / "bypasser.js"
DEFAULT_PROFILE_DIR = Path.home() / ".local" / "share" / "hypeddit_profile"
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads"

def load_env():
    env_locations = [
        Path.cwd() / ".env",
        MODULE_DIR / ".env",
        Path.home() / "Library/CloudStorage/GoogleDrive-bernard.zhao.us@gmail.com/My Drive/scratch/library_management/.env",
    ]
    for env_path in env_locations:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if "=" in line and not line.strip().startswith("#"):
                        k, v = line.strip().split("=", 1)
def ensure_chromium_installed():
    """Checks if Chromium binary is installed, auto-installs if missing."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            exec_path = p.chromium.executable_path
            if not os.path.exists(exec_path):
                raise FileNotFoundError()
    except Exception:
        import subprocess
        print("[*] Chromium binary not found. Auto-installing Chromium via Playwright...", flush=True)
        try:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        except Exception as err:
            print(f"[!] Auto-install note: {err}. Please run 'playwright install chromium' manually.", flush=True)

async def download_track(
    url: str,
    dest_dir: str = str(DEFAULT_DOWNLOAD_DIR),
    headless: bool = True,
    timeout: int = 60,
    email: str = None,
    name: str = None,
    user_data_dir: str = str(DEFAULT_PROFILE_DIR),
    on_status: callable = None,
) -> dict:
    """
    Automates the download of a track from a Hypeddit fangate URL.
    """
    load_env()
    ensure_chromium_installed()
    dest_path = Path(dest_dir).expanduser().resolve()
    dest_path.mkdir(parents=True, exist_ok=True)
    profile_path = Path(user_data_dir).expanduser().resolve()
    profile_path.mkdir(parents=True, exist_ok=True)

    # Clean up stale locks if any
    lock_file = profile_path / "SingletonLock"
    if lock_file.exists():
        try:
            lock_file.unlink()
        except Exception:
            pass

    def log(msg: str):
        if on_status:
            on_status(msg)
        else:
            print(f"[*] {msg}", flush=True)

    start_time = time.time()
    log(f"Target URL: {url}")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(profile_path),
            headless=headless,
            accept_downloads=True,
            viewport={"width": 1280, "height": 800},
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # Inject SoundCloud cookie if available
        sc_token = os.environ.get("SOUNDCLOUD_OAUTH_TOKEN")
        if sc_token:
            await context.add_cookies([
                {
                    "name": "oauth_token",
                    "value": sc_token,
                    "domain": ".soundcloud.com",
                    "path": "/",
                    "secure": True
                }
            ])

        # Inject user script
        if BYPASSER_JS_PATH.exists():
            await context.add_init_script(path=str(BYPASSER_JS_PATH))
            log(f"Injected userscript: {BYPASSER_JS_PATH.name}")

        page = await context.new_page()

        download_captured = asyncio.Future()

        def on_download(download):
            log(f"Download initiated: {download.suggested_filename}")
            if not download_captured.done():
                download_captured.set_result(download)

        page.on("download", on_download)
        page.on("console", lambda msg: log(f"  [browser] {msg.text}"))

        # Popup handler
        async def on_popup(popup_page):
            try:
                await popup_page.wait_for_load_state("domcontentloaded")
                submit_btn = await popup_page.wait_for_selector('button[type="submit"], input[type="submit"]', timeout=6000)
                if submit_btn:
                    await submit_btn.click()
            except Exception:
                pass

        context.on("page", lambda p: asyncio.create_task(on_popup(p)))

        log(f"Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        except Exception as e:
            log(f"Navigation note: {e}")

        log("Waiting for bypasser script and download trigger...")
        try:
            download = await asyncio.wait_for(download_captured, timeout=timeout)
            filename = download.suggested_filename
            final_file_path = dest_path / filename
            await download.save_as(str(final_file_path))
            size_bytes = final_file_path.stat().st_size
            elapsed = round(time.time() - start_time, 1)

            log(f"Saved: {final_file_path.name} ({round(size_bytes / (1024*1024), 2)} MB in {elapsed}s)")
            await context.close()
            return {
                "success": True,
                "file_path": str(final_file_path),
                "filename": filename,
                "size_bytes": size_bytes,
                "duration_seconds": elapsed,
            }
        except asyncio.TimeoutError:
            log("Timed out waiting for automated download.")
            await context.close()
            return {
                "success": False,
                "error": "Timeout waiting for download",
                "file_path": None,
            }
        except Exception as e:
            log(f"Error: {e}")
            await context.close()
            return {
                "success": False,
                "error": str(e),
                "file_path": None,
            }
