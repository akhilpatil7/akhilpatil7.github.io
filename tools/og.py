#!/usr/bin/env python3
"""
Generate 1200x630 Open Graph / Twitter cards for every page on the site.

Run:  python tools/og.py
Out:  images/og/*.png

Deliberately dependency-light: Pillow plus fonts that ship with Windows,
chosen to echo the site's Cormorant / JetBrains Mono / DM Sans pairing.
"""
import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "og")
POSTS_DIR = os.path.join(ROOT, "content", "posts")

W, H = 1200, 630
PAD = 84

BG      = (247, 248, 252)
SURFACE = (255, 255, 255)
DOT     = (216, 220, 234)
TXT     = (15, 17, 23)
TXT2    = (90, 97, 120)
TXT3    = (146, 152, 174)
BORDER  = (226, 229, 239)
ACCENT  = (12, 122, 88)
BLUE    = (26, 112, 224)

FONTS = "C:/Windows/Fonts/"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

F_DISP    = lambda s: font("constan.ttf",  s)   # Constantia — display serif
F_DISP_B  = lambda s: font("constanb.ttf", s)
F_MONO    = lambda s: font("consola.ttf",  s)   # Consolas — mono
F_MONO_B  = lambda s: font("consolab.ttf", s)
F_UI      = lambda s: font("segoeuisl.ttf", s)  # Segoe UI Semilight — body
F_UI_B    = lambda s: font("segoeuib.ttf",  s)


# ── primitives ────────────────────────────────────────────────────────
def tracked(draw, xy, text, fnt, fill, tracking=2.0):
    """Draw letter-spaced text (Pillow has no tracking); returns end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x - tracking


def tracked_width(draw, text, fnt, tracking=2.0):
    return sum(draw.textlength(c, font=fnt) for c in text) + tracking * (len(text) - 1)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, max_w, max_lines, hi=64, lo=34):
    """Largest display size at which `text` wraps into <= max_lines."""
    for size in range(hi, lo - 1, -2):
        f = F_DISP(size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines, size
    f = F_DISP(lo)
    return f, wrap(draw, text, f, max_w)[:max_lines], lo


def dot_grid(img):
    d = ImageDraw.Draw(img)
    for y in range(0, H, 28):
        for x in range(0, W, 28):
            d.point((x, y), fill=DOT)
            d.point((x + 1, y), fill=DOT)
            d.point((x, y + 1), fill=DOT)
            d.point((x + 1, y + 1), fill=DOT)


def lift_motif(img, x0, y0, w, h, alpha=42):
    """The site's signature incrementality curve: control flat, treatment lifts."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    def pts(fn, n=60):
        return [(x0 + w * i / n, y0 + h - h * fn(i / n)) for i in range(n + 1)]

    control = pts(lambda t: 0.30 + 0.16 * t)
    treat = pts(lambda t: 0.30 + 0.16 * t if t < 0.5 else 0.38 + 1.34 * (t - 0.5) ** 1.35)

    d.polygon(
        [(p[0], p[1]) for p in treat[30:]] + [(p[0], p[1]) for p in reversed(control[30:])],
        fill=ACCENT + (int(alpha * 0.32),),
    )
    d.line([(x0, y0 + h - h * 0.30), (x0 + w, y0 + h - h * 0.30)], fill=TXT3 + (alpha,), width=1)
    d.line(control, fill=BLUE + (alpha + 26,), width=3)
    d.line(treat, fill=ACCENT + (alpha + 78,), width=4)
    d.line([(x0 + w * 0.5, y0), (x0 + w * 0.5, y0 + h)], fill=TXT3 + (alpha,), width=1)
    img.alpha_composite(layer)


def card(eyebrow, title, sub=None, filename="card.png"):
    img = Image.new("RGBA", (W, H), BG + (255,))
    dot_grid(img)
    lift_motif(img, W - 470, H - 400, 400, 300)

    d = ImageDraw.Draw(img)

    # left accent spine
    d.rectangle([0, 0, 5, H], fill=ACCENT)

    # eyebrow
    fe = F_MONO_B(17)
    y = PAD + 4
    tracked(d, (PAD, y), eyebrow.upper(), fe, ACCENT, tracking=3.2)
    y += 34
    d.line([(PAD, y), (PAD + 300, y)], fill=BORDER, width=1)

    # title
    y += 46
    max_w = W - PAD * 2 - 150
    f, lines, size = fit(d, title, max_w, 4)
    lh = int(size * 1.16)
    for ln in lines:
        d.text((PAD, y), ln, font=f, fill=TXT)
        y += lh

    # optional subtitle
    if sub:
        y += 16
        fs = F_UI(23)
        for ln in wrap(d, sub, fs, max_w)[:2]:
            d.text((PAD, y), ln, font=fs, fill=TXT2)
            y += 34

    # footer
    fy = H - PAD - 46
    d.line([(PAD, fy - 26), (W - PAD, fy - 26)], fill=BORDER, width=1)

    box = 46
    d.rectangle([PAD, fy, PAD + box, fy + box], fill=ACCENT)
    fm = F_DISP_B(22)
    mw = d.textlength("AP", font=fm)
    d.text((PAD + (box - mw) / 2, fy + 9), "AP", font=fm, fill=SURFACE)

    d.text((PAD + box + 18, fy + 2), "Akhil Patil", font=F_UI_B(23), fill=TXT)
    tracked(d, (PAD + box + 20, fy + 30), "SR. MARKETING ANALYST", F_MONO(14), TXT3, tracking=1.6)

    url = "akhilpatil7.github.io"
    fu = F_MONO(16)
    uw = tracked_width(d, url, fu, 1.8)
    tracked(d, (W - PAD - uw, fy + 16), url, fu, TXT2, tracking=1.8)

    os.makedirs(OUT, exist_ok=True)
    img.convert("RGB").save(os.path.join(OUT, filename), "PNG", optimize=True)
    return filename


# ── content ───────────────────────────────────────────────────────────
def frontmatter(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---", raw, re.S)
    fm = {}
    for line in m.group(1).splitlines():
        if ": " not in line:
            continue
        k, v = line.split(": ", 1)
        fm[k.strip()] = v.strip().strip('"')
    return fm


def main():
    meta = json.load(open(os.path.join(ROOT, "content", "posts.json"), encoding="utf-8"))
    made = []

    made.append(card(
        "Portfolio · Marketing Analytics",
        "Akhil Patil — proving what marketing actually works",
        "Incrementality testing, media analytics and applied ML at Plymouth Rock Assurance.",
        "home.png",
    ))

    made.append(card(
        "Field Notes · Essays",
        meta["site"]["blogTitle"] + " — writing on causal measurement",
        meta["site"]["blogTagline"],
        "blog.png",
    ))

    for key, cat in meta["categories"].items():
        made.append(card("Field Notes · Topic", cat["title"], None, "topic-" + key + ".png"))

    for fname, p in meta["posts"].items():
        fm = frontmatter(os.path.join(POSTS_DIR, fname))
        cat = meta["categories"][p["category"]]["label"]
        made.append(card("Field Notes · " + cat, fm["title"], None, p["slug"] + ".png"))

    print("Generated {} OG cards -> images/og/".format(len(made)))


if __name__ == "__main__":
    main()
