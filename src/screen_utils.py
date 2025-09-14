from __future__ import annotations

from typing import Tuple

def get_primary_screen_size() -> Tuple[int, int]:
    try:
        from screeninfo import get_monitors
        mons = get_monitors()
        if not mons:
            raise RuntimeError("No monitors detected")
        # Pick primary or the first
        primary = next((m for m in mons if getattr(m, 'is_primary', False)), mons[0])
        return primary.width, primary.height
    except Exception:
        # Fallback to common 1920x1080
        return 1920, 1080
