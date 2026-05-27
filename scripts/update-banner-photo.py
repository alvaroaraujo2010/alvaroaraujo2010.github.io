# -*- coding: utf-8 -*-
"""Banner kit + foto HD (legado). Usar build-banner.py para fondo sin rayas."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
KIT = Path(r"D:\MARCA\kit_marketing_alvaro_araujo_independiente\01_banner_linkedin_1584x396.jpg")
PHOTO = Path(r"D:\MARCA\foto-alvaro.png")
OUT_DIR = ROOT / "public" / "assets" / "images"

PHOTO_BOX = (1015, 22, 1560, 374)
PHOTO_RADIUS = 32

# Sello: esquina inferior derecha de "Tecnología que funciona" (1584×396)
STAMP_CENTER = (892, 232)
STAMP_LOGO_PX = 96


def trim_white_border(im: Image.Image, threshold: int = 240) -> Image.Image:
    px = im.load()
    w, h = im.size

    def row_border(y: int) -> bool:
        return (
            sum(1 for x in range(w) if px[x, y][0] >= threshold and px[x, y][1] >= threshold and px[x, y][2] >= threshold)
            >= w * 0.8
        )

    def col_border(x: int) -> bool:
        return (
            sum(1 for y in range(h) if px[x, y][0] >= threshold and px[x, y][1] >= threshold and px[x, y][2] >= threshold)
            >= h * 0.8
        )

    top, bottom, left, right = 0, h - 1, 0, w - 1
    while top < h - 1 and row_border(top):
        top += 1
    while bottom > top and row_border(bottom):
        bottom -= 1
    while left < w - 1 and col_border(left):
        left += 1
    while right > left and col_border(right):
        right -= 1

    cropped = im.crop((left, top, right + 1, bottom + 1))
    if cropped.size != (1584, 396):
        cropped = cropped.resize((1584, 396), Image.Resampling.LANCZOS)
    return cropped


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def fit_photo(photo: Image.Image, tw: int, th: int) -> Image.Image:
    photo = photo.convert("RGB")
    pw, ph = photo.size
    aspect = tw / th
    if pw / ph > aspect:
        nw = int(ph * aspect)
        left = (pw - nw) // 2
        crop = photo.crop((left, 0, left + nw, ph))
    else:
        nh = int(pw / aspect)
        top = max(0, int(ph * 0.03))
        crop = photo.crop((0, top, pw, min(ph, top + nh)))
    return crop.resize((tw, th), Image.Resampling.LANCZOS)


def draw_logo_rgba(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cx = cy = size / 2
    react = (97, 218, 251, 255)
    stroke = max(2, round(size * 0.035))
    rx, ry = size * 0.33, size * 0.115
    for deg in (0, 60, 120):
        layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=react, width=stroke)
        layer = layer.rotate(-deg, center=(cx, cy), resample=Image.Resampling.BICUBIC)
        img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)
    nr = max(3, round(size * 0.05))
    d.ellipse([cx - nr, cy - nr, cx + nr, cy + nr], fill=react)
    sh = size * 0.2
    shield = [
        (cx, cy - sh),
        (cx + sh * 0.9, cy - sh * 0.3),
        (cx + sh * 0.9, cy + sh * 0.55),
        (cx, cy + sh * 1.1),
        (cx - sh * 0.9, cy + sh * 0.55),
        (cx - sh * 0.9, cy - sh * 0.3),
    ]
    d.polygon(shield, fill=(221, 0, 49, 255), outline=(255, 255, 255, 255), width=1)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", round(size * 0.2))
    d.text((cx, cy), "A", fill=(255, 255, 255, 255), font=font, anchor="mm")
    return img


def to_black_stamp(im: Image.Image, alpha: int = 195) -> Image.Image:
    px = im.convert("RGBA").load()
    w, h = im.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    opx = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 25:
                opx[x, y] = (8, 8, 8, min(255, int(a * alpha / 255)))
    return out


def build_stamp(logo_px: int) -> Image.Image:
    pad = 10
    logo = to_black_stamp(draw_logo_rgba(logo_px))
    font_sm = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 10)
    t1, t2 = "MARCA", "REGISTRADA"
    tmp = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    b1 = td.textbbox((0, 0), t1, font=font_sm)
    b2 = td.textbbox((0, 0), t2, font=font_sm)
    sw = logo_px + pad * 2
    sh = logo_px + pad + (b1[3] - b1[1]) + (b2[3] - b2[1]) + 10 + pad
    stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    stamp.alpha_composite(logo, (pad, pad))
    sd = ImageDraw.Draw(stamp)
    ty = logo_px + pad + 2
    sd.text(((sw - (b1[2] - b1[0])) // 2, ty), t1, fill=(8, 8, 8, 215), font=font_sm)
    sd.text(
        ((sw - (b2[2] - b2[0])) // 2, ty + b1[3] - b1[1] + 1),
        t2,
        fill=(8, 8, 8, 215),
        font=font_sm,
    )
    sd.ellipse([2, 2, sw - 3, sh - 3], outline=(10, 10, 10, 165), width=2)
    return stamp.rotate(-8, expand=True, resample=Image.Resampling.BICUBIC).filter(
        ImageFilter.GaussianBlur(radius=0.25)
    )


def apply_stamp(banner: Image.Image, scale: float) -> Image.Image:
    stamp = build_stamp(int(STAMP_LOGO_PX * scale))
    cx = int(STAMP_CENTER[0] * scale)
    cy = int(STAMP_CENTER[1] * scale)
    sw, sh = stamp.size
    x, y = cx - sw // 2, cy - sh // 2
    out = banner.convert("RGBA")
    out.alpha_composite(stamp, (x, y))
    return out


def compose(scale: float = 1.0) -> Image.Image:
    banner = Image.open(KIT).convert("RGB")
    banner = trim_white_border(banner)
    if scale != 1.0:
        banner = banner.resize((int(1584 * scale), int(396 * scale)), Image.Resampling.LANCZOS)

    box = tuple(int(v * scale) for v in PHOTO_BOX)
    left, top, right, bottom = box
    tw, th = right - left, bottom - top
    portrait = fit_photo(Image.open(PHOTO), tw, th)
    banner.paste(portrait, (left, top), rounded_mask((tw, th), int(PHOTO_RADIUS * scale)))

    return banner.convert("RGBA")


def save_rgb(im: Image.Image, png: Path, jpg: Path | None = None) -> None:
    rgb = Image.new("RGB", im.size, (15, 33, 55))
    if im.mode == "RGBA":
        rgb.paste(im, mask=im.split()[3])
    else:
        rgb = im.convert("RGB")
    rgb.save(png, format="PNG", optimize=True)
    if jpg:
        rgb.save(jpg, format="JPEG", quality=98, subsampling=0)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    b1 = compose(1.0)
    save_rgb(b1, OUT_DIR / "01_banner_linkedin_1584x396.png", OUT_DIR / "01_banner_linkedin_1584x396.jpg")
    save_rgb(compose(2.0), OUT_DIR / "01_banner_linkedin_3168x792.png")
    print("Banner OK — sin borde blanco, sin sello")


if __name__ == "__main__":
    main()
