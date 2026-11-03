from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
F = "fonts/package/files/archivo-latin-%d-normal.woff"
f = lambda w, s: ImageFont.truetype(F % w, s)
W, H = 1280, 720
BLACK = (17, 17, 17); WHITE = (255, 255, 255); RED = (226, 35, 35); GREEN = (22, 163, 74)
BLUE = (37, 99, 235); YEL = (255, 214, 0); CREAM = (250, 246, 236); NAVY = (22, 35, 58)

def bg_solid(c, glow=None):
    im = Image.new("RGB", (W, H), c)
    if glow:
        g = Image.new("L", (W, H), 0); d = ImageDraw.Draw(g)
        d.ellipse([650, -150, 1450, 850], fill=140); g = g.filter(ImageFilter.GaussianBlur(170))
        im = Image.composite(Image.new("RGB", (W, H), glow), im, g)
    return im.convert("RGBA")

def person(n, cx, h=980, top=60, flip=False):
    p = Image.open(f"photos/cut_{n}.png")
    bb = p.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox(); p = p.crop(bb)
    if flip: p = p.transpose(Image.FLIP_LEFT_RIGHT)
    s = h / p.height; p = p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)
    # clean edge: erode alpha slightly + feather (removes halo fringe)
    a = p.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2)); p.putalpha(a)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); x = int(cx - p.width / 2)
    sh = Image.new("RGBA", p.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.45)).filter(ImageFilter.GaussianBlur(18)))
    lay.alpha_composite(sh, (x - 14, top + 10)); lay.alpha_composite(p, (x, top))
    return lay

def txt(d, xy, s, size, fill, stroke=0, sc=BLACK, anchor="la", w=900):
    d.text(xy, s, font=f(w, size), fill=fill, stroke_width=stroke, stroke_fill=sc, anchor=anchor)

def box_text(d, x, y, s, size, fg, bg, pad=18, r=12):
    fo = f(900, size); tw = d.textlength(s, font=fo)
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + size * 1.18 + pad * 0.6], radius=r, fill=bg)
    d.text((x + pad, y + pad * 0.25), s, font=fo, fill=fg)
    return x + tw + pad * 2

def bucket(im, cx, base_y, w, h, col, label, fill_frac=0.75):
    d = ImageDraw.Draw(im)
    top_w, bot_w = w, int(w * 0.78)
    poly = [(cx - top_w / 2, base_y - h), (cx + top_w / 2, base_y - h), (cx + bot_w / 2, base_y), (cx - bot_w / 2, base_y)]
    d.polygon(poly, fill=col, outline=BLACK, width=6)
    # rim
    d.ellipse([cx - top_w / 2 - 6, base_y - h - 22, cx + top_w / 2 + 6, base_y - h + 22], fill=tuple(max(0, c - 40) for c in col), outline=BLACK, width=6)
    # handle
    d.arc([cx - top_w / 2 + 10, base_y - h - 90, cx + top_w / 2 - 10, base_y - h + 30], 200, 340, fill=BLACK, width=7)
    fo = f(900, 30 if len(label) > 6 else 44)
    d.text((cx, base_y - h * 0.45), label, font=fo, fill=WHITE, anchor="mm", stroke_width=3, stroke_fill=BLACK)

def num_badge(d, cx, cy, n, col=BLACK):
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=WHITE, outline=col, width=6)
    d.text((cx, cy + 2), str(n), font=f(900, 44), fill=col, anchor="mm")

def big_x(d, cx, cy, s=70, width=22):
    d.line([cx - s, cy - s, cx + s, cy + s], fill=RED, width=width)
    d.line([cx - s, cy + s, cx + s, cy - s], fill=RED, width=width)

# ---------- WHICH ACCOUNT FIRST ----------
def wf_A():  # three buckets, wrong order crossed out
    im = bg_solid(CREAM, glow=(255, 236, 200))
    d = ImageDraw.Draw(im)
    txt(d, (40, 26), "WRONG", 160, RED, stroke=6)
    txt(d, (44, 186), "ORDER?", 120, BLACK)
    xs = [120, 320, 520]; cols = [GREEN, RED, BLUE]; labs = ["CASH", "UNTAXED", "ROTH"]
    for x, c, l in zip(xs, cols, labs): bucket(im, x, 680, 180, 180, c, l)
    d = ImageDraw.Draw(im)
    for i, x in enumerate(xs): num_badge(d, x, 410, i + 1)
    d.line([40, 560, 620, 470], fill=RED, width=18)
    im.alpha_composite(person("1877", 1000, h=1000, top=40))
    im.convert("RGB").save("Thumbnail-WhichFirst-C1.jpg", quality=92)

def wf_B():  # yellow, "NOT THIS FIRST" with savings bucket + arrow
    im = bg_solid(YEL)
    d = ImageDraw.Draw(im)
    txt(d, (44, 40), "DON'T SPEND", 104, BLACK)
    txt(d, (44, 150), "THIS FIRST", 104, BLACK)
    bucket(im, 270, 650, 260, 250, GREEN, "SAVINGS")
    d = ImageDraw.Draw(im)
    # red arrow pointing down at bucket
    d.polygon([(470, 330), (560, 330), (560, 400), (610, 400), (515, 480), (420, 400), (470, 400)], fill=RED, outline=BLACK)
    im.alpha_composite(person("1877", 980, h=1000, top=40))
    im.convert("RGB").save("Thumbnail-WhichFirst-C2.jpg", quality=92)

def wf_C():  # white, tax spike chart at 73
    im = bg_solid(WHITE)
    d = ImageDraw.Draw(im)
    txt(d, (44, 36), "THE TAX", 120, BLACK)
    txt(d, (44, 160), "BOMB AT 73", 120, RED, stroke=4)
    base = 640; x0 = 60; bw = 46; gap = 14
    hs = [40, 45, 50, 48, 52, 55, 190, 230, 260]
    for i, hh in enumerate(hs):
        x = x0 + i * (bw + gap)
        col = (160, 170, 185) if i < 6 else RED
        d.rectangle([x, base - hh, x + bw, base], fill=col, outline=BLACK, width=3)
    d.line([60, base, x0 + len(hs) * (bw + gap), base], fill=BLACK, width=6)
    txt(d, (x0 + 6 * (bw + gap) + 30, base + 8), "73", 44, BLACK, anchor="ma")
    txt(d, (x0 + 60, base + 8), "65", 44, (120, 120, 120), anchor="ma")
    im.alpha_composite(person("1867", 1000, h=1000, top=40))
    im.convert("RGB").save("Thumbnail-WhichFirst-C3.jpg", quality=92)

# ---------- IS $1M ENOUGH ----------
def mm_A():  # $1,000,000 -> $3,333/mo
    im = bg_solid(WHITE)
    d = ImageDraw.Draw(im)
    txt(d, (44, 60), "$1,000,000", 132, GREEN, stroke=5)
    d.polygon([(250, 250), (330, 250), (330, 330), (390, 330), (290, 420), (190, 330), (250, 330)], fill=BLACK)
    txt(d, (44, 440), "$3,333", 160, RED, stroke=6)
    txt(d, (56, 630), "A MONTH?!", 64, BLACK)
    im.alpha_composite(person("1867", 1060, h=1000, top=40))
    im.convert("RGB").save("Thumbnail-1Million-C1.jpg", quality=92)

def mm_B():  # yellow, ENOUGH? with money stack
    im = bg_solid(YEL)
    d = ImageDraw.Draw(im)
    txt(d, (44, 30), "$1M", 230, BLACK)
    txt(d, (50, 280), "ENOUGH?", 126, WHITE, stroke=9)
    # bill stack
    for i in range(6):
        y = 640 - i * 26
        d.rounded_rectangle([60, y - 40, 420, y], radius=6, fill=(46, 160, 90), outline=BLACK, width=4)
        d.ellipse([215, y - 34, 265, y - 6], outline=(20, 90, 50), width=4)
    im.alpha_composite(person("1867", 1060, h=1000, top=40))
    im.convert("RGB").save("Thumbnail-1Million-C2.jpg", quality=92)

def mm_C():  # crash in year one
    im = bg_solid(WHITE)
    d = ImageDraw.Draw(im)
    txt(d, (44, 36), "YEAR ONE", 120, BLACK)
    txt(d, (44, 160), "CRASH", 150, RED, stroke=5)
    # line chart: 1M then drop
    pts = [(70, 420), (170, 410), (240, 430), (300, 620), (370, 600), (440, 640), (520, 610)]
    d.line(pts, fill=RED, width=20, joint="curve")
    txt(d, (70, 360), "$1M", 54, GREEN)
    txt(d, (340, 650), "-20%", 54, RED, anchor="la")
    im.alpha_composite(person("1862", 1010, h=1000, top=40))
    im.convert("RGB").save("Thumbnail-1Million-C3.jpg", quality=92)

for fn in (wf_A, wf_B, wf_C, mm_A, mm_B, mm_C): fn()
s = Image.new("RGB", (1920, 720), WHITE)
for i, fn in enumerate(["Thumbnail-WhichFirst-C1.jpg", "Thumbnail-WhichFirst-C2.jpg", "Thumbnail-WhichFirst-C3.jpg",
                        "Thumbnail-1Million-C1.jpg", "Thumbnail-1Million-C2.jpg", "Thumbnail-1Million-C3.jpg"]):
    s.paste(Image.open(fn).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
s.save("test/thumbs3.jpg", quality=88)
