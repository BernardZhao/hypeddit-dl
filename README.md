# 🎵 hypeddit-dl

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Automated%20With-Playwright-orange.svg)](https://playwright.dev)

An automated, zero-clutter CLI downloader and Python library for **Hypeddit** music download gates.

Hypeddit is widely used by DJs and electronic music producers to distribute free tracks, edits, bootlegs, and WAV/FLAC masters. However, downloading a single track typically requires manually clicking through multiple "follow gates" (SoundCloud follow/like/comment, Spotify follow, Instagram, TikTok, YouTube, email entry, etc.).

**`hypeddit-dl` automates this entire flow in seconds, downloading the high-fidelity master file directly to your disk without polluting your social media accounts with spam follows or comments.**

---

## ✨ Features

- ⚡ **Fully Automated**: Clicks through email walls, SoundCloud, Spotify, Instagram, YouTube, TikTok, Facebook, and donation steps automatically.
- 🧹 **Zero Account Clutter**: Doesn't leave spam comments, likes, or hundreds of followings on your accounts.
- 🎧 **Direct High-Res Masters**: Captures the original master audio files distributed by artists (Lossless WAV, FLAC, AIFF, and 320 kbps MP3).
- 🪟 **Headless & Background Friendly**: Runs completely headlessly via Chromium, or visibly with `--no-headless` for debugging.
- 📦 **Batch Downloading**: Pass a list of URLs in a text file to download multiple tracks sequentially.
- 🐍 **Python Library**: Easily integrate into DJ library managers, music archivers, or scripts via `from hypeddit_dl import download_track`.
- 🧩 **Bonus Userscript**: Includes a standalone Tampermonkey / Violentmonkey userscript for desktop browser users.

---

## 🚀 Installation

### Option 1: Install from GitHub
```bash
git clone https://github.com/BernardZhao/hypeddit-dl.git
cd hypeddit-dl
pip install -e .
playwright install chromium
```

### Option 2: Requirements Only
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 💻 CLI Usage

### Download a single track
```bash
hypeddit-dl https://hypeddit.com/artist/track-name
```

### Specify download folder
```bash
hypeddit-dl https://hypeddit.com/artist/track-name --dest ~/Music/DJ_Edits
```

### Batch download multiple tracks
Create a text file (e.g. `tracks.txt`):
```text
https://hypeddit.com/artist1/edit1
https://hypeddit.com/artist2/bootleg2
```
Then run:
```bash
hypeddit-dl --batch tracks.txt --dest ~/Downloads
```

### CLI Options

| Flag | Short | Default | Description |
| :--- | :---: | :---: | :--- |
| `url` | | | Hypeddit track URL to download |
| `--batch` | `-b` | | Text file with URLs (one per line) |
| `--dest` | `-d` | `~/Downloads` | Directory where downloaded audio is saved |
| `--no-headless` | | `False` | Show browser window during execution |
| `--timeout` | `-t` | `60` | Timeout in seconds waiting for download |
| `--email` | `-e` | *auto* | Custom email to provide to email gates |
| `--version` | `-v` | | Show version and exit |

---

## 🐍 Python API

You can easily integrate `hypeddit-dl` into your own Python scripts:

```python
import asyncio
from hypeddit_dl import download_track

async def main():
    result = await download_track(
        url="https://hypeddit.com/headhigh/astherushcomes",
        dest_dir="~/Music",
        headless=True
    )
    
    if result["success"]:
        print(f"Downloaded: {result['filename']}")
        print(f"Path: {result['file_path']}")
        print(f"Size: {round(result['size_bytes'] / (1024*1024), 2)} MB")
    else:
        print(f"Failed: {result['error']}")

asyncio.run(main())
```

---

## 🧩 Standalone Userscript (Tampermonkey)

If you prefer downloading directly in your personal browser (Chrome, Firefox, Safari):

1. Install [Tampermonkey](https://www.tampermonkey.net/) or [Violentmonkey](https://violentmonkey.github.io/).
2. Open [`userscript/hypeddit-bypasser.user.js`](userscript/hypeddit-bypasser.user.js).
3. Create a new script in your userscript manager and paste the code.
4. When you visit any Hypeddit gate, it will automatically click through the steps and trigger the download button.

---

## 🛠️ How It Works

1. **DOM Injection**: Uses Playwright's `add_init_script` to inject a MutationObserver before page scripts run.
2. **Carousel Transitioning**: Detects active slider classes (`email`, `sc`, `sp`, `ig`, `yt`, `tk`, `dw`) and simulates user interactions.
3. **Popup Interception**: Automatically handles popups triggered by social links, auto-closing dummy tabs and preventing browser hanging.
4. **Download Capture**: Listens to the browser's download stream and saves the resulting file with its original filename and extension.

---

## ⚖️ License

Distributed under the [MIT License](LICENSE).
