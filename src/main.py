from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path

from verse_store import VerseStore
from image_renderer import render_wallpaper
from wallpaper import set_wallpaper
from screen_utils import get_primary_screen_size


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Bible verse wallpaper rotator")
    p.add_argument("--verses", type=Path, default=Path("data/verses.json"), help="Path to verses JSON")
    p.add_argument("--font", type=Path, default=None, help="Path to .ttf/.otf font to use")
    p.add_argument("--mode", choices=["random", "sequential"], default="random", help="Verse selection mode")
    p.add_argument("--interval", type=int, default=300, help="Seconds between updates (ignored if --once)")
    p.add_argument("--out", type=Path, default=Path("cache/wallpaper.jpg"), help="Output wallpaper image path")
    p.add_argument("--once", action="store_true", help="Generate and set wallpaper once, then exit")
    return p.parse_args()


def pick_verse(store: VerseStore, mode: str):
    return store.next() if mode == "sequential" else store.random()


def update_wallpaper(verses_path: Path, out_path: Path, mode: str, font_path: Path | None) -> None:
    store = VerseStore(verses_path)
    verse = pick_verse(store, mode)
    width, height = get_primary_screen_size()
    out_img = render_wallpaper(verse.text, verse.ref, (width, height), out_path, font_path)
    set_wallpaper(out_img)


def main() -> int:
    args = parse_args()

    stop = False

    def handle_sigint(signum, frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)

    if args.once:
        update_wallpaper(args.verses, args.out, args.mode, args.font)
        return 0

    # Continuous mode
    while not stop:
        try:
            update_wallpaper(args.verses, args.out, args.mode, args.font)
        except Exception as e:
            # Print and continue after a short delay
            print(f"Error: {e}")
        # Sleep in small chunks to allow quick Ctrl+C
        remaining = max(5, args.interval)
        while remaining > 0 and not stop:
            chunk = min(1, remaining)
            time.sleep(chunk)
            remaining -= chunk
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
