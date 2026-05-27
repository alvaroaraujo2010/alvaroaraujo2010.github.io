"""
Nuevo banner 1584×396:
- Fondo fotográfico moderno desde internet (paleta navy/teal).
- Información del banner anterior reorganizada.
- Tu foto HD integrada en el lado derecho.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "public" / "assets" / "images"
PHOTO = Path(r"D:\RECIBIDOS\foto-alvaro.png")

W, H = 1584, 396
PHOTO_BOX = (1030, 26, 1560, 370)
PHOTO_RADIUS = 32

BG_CACHE = OUT_DIR / "banner-bg-coder-workspace.jpg"
# Imagen profesional de workspace tech con tonos navy/teal de Unsplash.
BG_URL = (
    "https://unsplash.com/photos/FjtWczJWRlc/download?force=true"
)

NAVY_950 = (10, 22, 40)
NAVY_900 = (15, 33, 55)
TEAL_500 = (30, 168, 159)
TEAL_300 = (94, 196, 188)
WHITE = (255, 255, 255)


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


def font_path(name: str) -> Path:
    path = Path(r"C:\Windows\Fonts") / name
    if path.exists():
        return path
    return Path(r"C:\Windows\Fonts\arial.ttf")


def fnt(size: int, *, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    if italic:
        name = "segoeuii.ttf"
        if not font_path(name).exists():
            name = "ariali.ttf"
    elif bold:
        name = "segoeuib.ttf"
        if not font_path(name).exists():
            name = "arialbd.ttf"
    else:
        name = "segoeui.ttf"
        if not font_path(name).exists():
            name = "arial.ttf"
    return ImageFont.truetype(str(font_path(name)), size)


def download_bg() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if BG_CACHE.exists():
        return
    req = urllib.request.Request(BG_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        BG_CACHE.write_bytes(resp.read())


def load_background() -> Image.Image:
    if not BG_CACHE.exists():
        download_bg()
    bg = Image.open(BG_CACHE).convert("RGB")
    return ImageOps.fit(bg, (W, H), method=Image.Resampling.LANCZOS)


def apply_overlay(bg: Image.Image) -> Image.Image:
    """Oscurece y unifica con la paleta del sitio."""
    base = bg.convert("RGBA")
    overlay = Image.new("RGBA", (W, H))
    px = overlay.load()
    for x in range(W):
        t = x / (W - 1)
        alpha = int(170 + 60 * t)
        r = int(NAVY_950[0] * (1 - t * 0.25) + NAVY_900[0] * t * 0.25)
        g = int(NAVY_950[1] * (1 - t * 0.25) + NAVY_900[1] * t * 0.25)
        b = int(NAVY_950[2] * (1 - t * 0.25) + NAVY_900[2] * t * 0.25)
        for y in range(H):
            vy = y / (H - 1)
            row_boost = int(15 * (1 - vy))
            px[x, y] = (r, g, b, min(255, alpha + row_boost))
    out = Image.alpha_composite(base, overlay)

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-120, H - 260, 520, H + 100), fill=(*TEAL_500, 55))
    gd.ellipse((360, -180, 940, 240), fill=(*TEAL_300, 35))
    out = Image.alpha_composite(out, glow)
    return out.filter(ImageFilter.GaussianBlur(radius=0.5))


def draw_left_block(canvas: Image.Image) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    panel = (40, 40, 560, 340)
    d.rounded_rectangle(panel, radius=24, fill=(8, 18, 32, 210))
    d.rounded_rectangle(panel, radius=24, outline=(20, 110, 120, 110), width=2)

    name_y = panel[1] + 34
    d.text((panel[0] + 32, name_y), "ALVARO", font=fnt(32, bold=True), fill=WHITE)
    d.text((panel[0] + 32, name_y + 40), "ARAÚJO", font=fnt(64, bold=True), fill=TEAL_300)

    y = name_y + 120
    d.text(
        (panel[0] + 32, y),
        "Ingeniero de Sistemas · +13 años",
        font=fnt(20),
        fill=(230, 240, 250),
    )
    y += 34
    d.text(
        (panel[0] + 32, y),
        "Software · Web · PCs · TIC · IA · Consultoría",
        font=fnt(18),
        fill=(220, 232, 245),
    )
    y += 38
    d.text(
        (panel[0] + 32, y),
        "Medellín · Todo Colombia  |  +57 301 245 59 94",
        font=fnt(18),
        fill=(210, 224, 238),
    )

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(layer)
    canvas.paste(canvas_rgba.convert("RGB"))


def draw_slogan(canvas: Image.Image) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    tx = 620
    ty = 150
    f1 = fnt(46, bold=True)
    f2 = fnt(36, italic=True)

    for dx, dy in ((3, 3), (2, 2), (1, 1)):
        d.text((tx + dx, ty + dy), "Tecnología", font=f1, fill=(0, 0, 0, 180))
        d.text((tx + dx, ty + 60 + dy), "que funciona", font=f2, fill=(0, 0, 0, 150))

    d.text((tx, ty), "Tecnología", font=f1, fill=WHITE)
    d.text((tx, ty + 60), "que funciona", font=f2, fill=TEAL_300)

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(layer)
    canvas.paste(canvas_rgba.convert("RGB"))


def paste_portrait(canvas: Image.Image) -> None:
    left, top, right, bottom = PHOTO_BOX
    tw, th = right - left, bottom - top

    portrait = fit_photo(Image.open(PHOTO), tw, th)
    mask = rounded_mask((tw, th), PHOTO_RADIUS)

    frame = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle(
        (0, 0, frame.size[0] - 1, frame.size[1] - 1),
        radius=PHOTO_RADIUS + 4,
        fill=(6, 14, 28, 200),
        outline=(30, 150, 150, 230),
        width=2,
    )

    base = canvas.convert("RGBA")
    base.alpha_composite(frame, (left - 4, top - 4))
    canvas.paste(base.convert("RGB"))

    canvas_rgba = canvas.convert("RGBA")
    portrait_rgba = portrait.convert("RGBA")
    canvas_rgba.paste(portrait_rgba, (left, top), mask)
    canvas.paste(canvas_rgba.convert("RGB"))


def compose() -> Image.Image:
    bg = apply_overlay(load_background())
    draw_left_block(bg)
    draw_slogan(bg)
    paste_portrait(bg)
    return bg.convert("RGBA")


def save_rgb(im: Image.Image, png: Path, jpg: Path | None = None) -> None:
    rgb = Image.new("RGB", im.size, NAVY_900)
    if im.mode == "RGBA":
        rgb.paste(im, mask=im.split()[3])
    else:
        rgb = im.convert("RGB")
    rgb.save(png, format="PNG", optimize=True)
    if jpg:
        rgb.save(jpg, format="JPEG", quality=98, subsampling=0)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    banner = compose()
    save_rgb(banner, OUT_DIR / "01_banner_linkedin_1584x396.png", OUT_DIR / "01_banner_linkedin_1584x396.jpg")
    big = banner.resize((3168, 792), Image.Resampling.LANCZOS)
    save_rgb(big, OUT_DIR / "01_banner_linkedin_3168x792.png")
    print("Banner OK — diseño nuevo con foto y fondo moderno")


if __name__ == "__main__":
    main()
