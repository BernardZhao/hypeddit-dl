"""
Command-Line Interface for hypeddit-dl
"""

import sys
import argparse
import asyncio
from pathlib import Path
from .core import download_track

VERSION = "0.1.0"

def parse_args():
    parser = argparse.ArgumentParser(
        prog="hypeddit-dl",
        description="Automated, zero-clutter downloader for Hypeddit music download gates.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Hypeddit track URL to download (e.g. https://hypeddit.com/artist/track)",
    )
    parser.add_argument(
        "--batch", "-b",
        metavar="FILE",
        help="Path to a text file containing a list of Hypeddit URLs (one per line)",
    )
    parser.add_argument(
        "--dest", "-d",
        default=str(Path.home() / "Downloads"),
        help="Directory where downloaded audio files should be saved (default: ~/Downloads)",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser with visible UI (useful for initial login or debugging)",
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=60,
        help="Timeout in seconds to wait for download to trigger (default: 60)",
    )
    parser.add_argument(
        "--email", "-e",
        help="Custom email address to use for email verification gates",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"hypeddit-dl v{VERSION}",
    )
    return parser.parse_args()

async def async_main():
    args = parse_args()

    if not args.url and not args.batch:
        print("Error: Please provide a Hypeddit URL or a --batch file.\n")
        print("Usage: hypeddit-dl https://hypeddit.com/artist/track")
        print("       hypeddit-dl --batch urls.txt")
        sys.exit(1)

    urls = []
    if args.url:
        urls.append(args.url.strip())
    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            print(f"Error: Batch file '{args.batch}' not found.")
            sys.exit(1)
        with open(batch_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    headless = not args.no_headless

    print(f"\n🎧 hypeddit-dl v{VERSION}")
    print(f"📁 Destination: {args.dest}")
    print(f"⚙️  Headless: {headless} | Timeout: {args.timeout}s\n")

    successful = 0
    failed = 0

    for i, u in enumerate(urls, 1):
        if len(urls) > 1:
            print(f"[{i}/{len(urls)}] Processing: {u}")
        result = await download_track(
            url=u,
            dest_dir=args.dest,
            headless=headless,
            timeout=args.timeout,
            email=args.email,
        )
        if result.get("success"):
            successful += 1
            print(f"  [✓] Successfully downloaded: {result['filename']}\n")
        else:
            failed += 1
            print(f"  [✗] Failed to download: {result.get('error', 'Unknown error')}\n")

    if len(urls) > 1:
        print(f"✨ Finished batch: {successful} downloaded, {failed} failed.")

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\n[!] Download canceled by user.")
        sys.exit(130)

if __name__ == "__main__":
    main()
