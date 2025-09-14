from __future__ import annotations

import ctypes
import os
from pathlib import Path
from PIL import Image

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02


def set_wallpaper(image_path: Path) -> None:
    """Set Windows desktop wallpaper.

    Windows expects BMP for SystemParametersInfo on older versions; on modern versions JPEG works if using registry ActiveDesktop settings. We'll ensure BMP to be safe.
    """
    img_path = Path(image_path)
    img_path = img_path.resolve()
    bmp_path = img_path.with_suffix('.bmp')

    # Convert to BMP to maximize compatibility
    try:
        with Image.open(img_path) as im:
            im.convert('RGB').save(bmp_path, 'BMP')
    except Exception as e:
        raise RuntimeError(f"Failed to convert image to BMP: {e}")

    # Update the wallpaper
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, str(bmp_path), SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )
    if not result:
        raise OSError("SystemParametersInfoW failed to set wallpaper.")
