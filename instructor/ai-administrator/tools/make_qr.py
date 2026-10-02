#!/usr/bin/env python3
"""Write brand/bot_qr.png for the Telegram bot link used on the 'Join the agent' slide.

Usage: make_qr.py <bot_username_without_@> [out.png]
"""
import sys, pathlib, qrcode
from qrcode.constants import ERROR_CORRECT_M

ROOT = pathlib.Path(__file__).resolve().parent.parent
user = sys.argv[1].lstrip("@")
out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "brand" / "bot_qr.png"
url = f"https://t.me/{user}"
qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=24, border=4)
qr.add_data(url); qr.make(fit=True)
img = qr.make_image(fill_color="#111111", back_color="white").convert("RGB")
img.save(out)
print(out, img.size, url)
