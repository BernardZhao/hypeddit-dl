# 🎵 hypeddit-dl

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Automated%20With-Playwright-orange.svg)](https://playwright.dev)

A CLI downloader and Python library for **Hypeddit** music download links.

Works for Soundcloud gates as of September 2026.
It seems like Hypeddit no longer can perform actions on behalf of your Soundcloud account, so we just need to automate clicking through.

*Was originally made with agent help for quick personal scripting.*

---

## 🚀 Installation

### Install from GitHub
```bash
git clone https://github.com/BernardZhao/hypeddit-dl.git
cd hypeddit-dl
pip install -e .
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

## ⚖️ License

Distributed under the [MIT License](LICENSE).
