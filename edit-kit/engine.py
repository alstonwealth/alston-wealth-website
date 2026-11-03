import subprocess, os, math, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir("/tmp/claude-0/-home-claude/555cd3a5-fd5b-54c8-8899-6c427ac58d18/scratchpad/edit")
F = "fonts/package/files/archivo-latin-%d-normal.woff"
_fc = {}
def f(w, s):
    k = (w, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(F % w, int(s))
    return _fc[k]
W, H, FPS = 1920, 1080, 30
CREAM = (250, 246, 236); NAVY = (22, 35, 58); INK = (17, 17, 17); GREEN = (22, 150, 70); RED = (214, 40, 40)
BLUE = (37, 99, 235); GREY = (110, 110, 110); YTRED = (255, 0, 0); WHITE = (255, 255, 255); BRASS = (201, 162, 107)
TR = 0.35  # transition seconds
SUB_T = 13.0; CLICK_T = 14.2; SUB_END = 16.8

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0, min(1, x)); c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- PIP ----------
D = 360
mask = Image.new("L", (D * 4, D * 4), 0); ImageDraw.Draw(mask).ellipse([0, 0, D * 4 - 1, D * 4 - 1], fill=255)
mask = mask.resize((D, D), Image.LANCZOS)
ring = Image.new("RGBA", (D + 24, D + 24), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
rd.ellipse([0, 0, D + 23, D + 23], fill=WHITE)
shadow = Image.new("RGBA", (D + 80, D + 80), (0, 0, 0, 0)); ImageDraw.Draw(shadow).ellipse([30, 40, D + 50, D + 60], fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
PX, PY = W - D - 70, H - D - 70
def pip(frame, scale=1.0):
    crop = frame.crop((660, 220, 1260, 820)).resize((D, D), Image.LANCZOS)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay.alpha_composite(shadow, (PX - 40, PY - 40)); lay.alpha_composite(ring, (PX - 12, PY - 12))
    c = crop.convert("RGBA"); c.putalpha(mask); lay.alpha_composite(c, (PX, PY))
    if scale < 1:
        s = max(0.01, scale); cx, cy = PX + D / 2, PY + D / 2
        lay = lay.resize((int(W * s), int(H * s)), Image.LANCZOS)
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); out.alpha_composite(lay, (int(cx - cx * s), int(cy - cy * s))); lay = out
    return lay

# ---------- slides ----------
def base_slide(kicker, title):
    im = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 18, H], fill=NAVY)
    d.text((110, 90), kicker, font=f(800, 34), fill=BRASS)
    d.text((110, 140), title, font=f(900, 84), fill=NAVY)
    return im

def pop_text(im, xy, s, font, fill, p, anchor="la", stroke=0, sf=WHITE):
    if p <= 0: return
    sc = 0.6 + 0.4 * back(p)
    tmp = Image.new("RGBA", (1, 1)); dd = ImageDraw.Draw(tmp)
    bb = dd.textbbox((0, 0), s, font=font, anchor="la", stroke_width=stroke)
    w, h = bb[2] + 20, bb[3] + 20
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(t).text((10, 10), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=sf)
    t = t.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
    a = t.getchannel("A").point(lambda v: int(v * min(1, p * 3))); t.putalpha(a)
    x, y = xy
    if anchor == "mm": x -= t.width / 2; y -= t.height / 2
    elif anchor == "la": x -= (t.width - w) / 2 * 0; y -= 0
    im.alpha_composite(t, (int(x), int(y)))
def bell(d, cx, cy, s, col):
    d.pieslice([cx - s, cy - s, cx + s, cy + s * 1.2], 180, 360, fill=col)
    d.rectangle([cx - s, cy, cx + s, cy + s * 0.55], fill=col)
    d.rounded_rectangle([cx - s * 1.25, cy + s * 0.5, cx + s * 1.25, cy + s * 0.75], radius=4, fill=col)
    d.ellipse([cx - s * 0.3, cy + s * 0.75, cx + s * 0.3, cy + s * 1.2], fill=col)

def cursor(lay, x, y, pressed):
    c = Image.new("RGBA", (60, 80), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
    pts = [(4, 4), (4, 60), (18, 47), (28, 72), (38, 67), (28, 43), (46, 43)]
    cd.polygon(pts, fill=WHITE, outline=INK); cd.line(pts + [pts[0]], fill=INK, width=4)
    if pressed: c = c.resize((52, 70), Image.LANCZOS)
    lay.alpha_composite(c, (int(x), int(y)))

_lg = Image.open("aw_icon.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
_lm = Image.new("L", (368, 368), 0); ImageDraw.Draw(_lm).ellipse([0, 0, 367, 367], fill=255); _lg.putalpha(_lm.resize((92, 92), Image.LANCZOS))
LOGO = _lg
def subscribe(im, t):
    if not (SUB_T < t < SUB_END): return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pin = ease((t - SUB_T) / 0.35); pout = ease((t - (SUB_END - 0.4)) / 0.4)
    y = 1100 - 200 * pin + 220 * pout
    x0 = 90
    # channel chip
    d.rounded_rectangle([x0, y, x0 + 700, y + 120], radius=60, fill=(255, 255, 255, 240))
    lay.alpha_composite(LOGO, (int(x0 + 14), int(y + 14)))
    d.text((x0 + 125, y + 30), "Alston Wealth", font=f(800, 34), fill=INK)
    d.text((x0 + 125, y + 72), "New videos Mon & Thu", font=f(500, 24), fill=GREY)
    subbed = t >= CLICK_T
    bxl = x0 + 420; bx = [bxl, y + 25, bxl + 265, y + 95]
    if subbed:
        d.rounded_rectangle(bx, radius=35, fill=(229, 229, 229)); d.text(((bx[0] + bx[2]) / 2 + 10, y + 60), "Subscribed", font=f(700, 30), fill=INK, anchor="mm")
        ang = math.sin((t - CLICK_T) * 30) * 18 * max(0, 1 - (t - CLICK_T) / 0.9)
        b = Image.new("RGBA", (60, 60), (0, 0, 0, 0)); bell(ImageDraw.Draw(b), 30, 26, 14, INK)
        b = b.rotate(ang, resample=Image.BICUBIC); lay.alpha_composite(b, (bx[0] + 6, int(y + 30)))
    else:
        d.rounded_rectangle(bx, radius=35, fill=(255, 0, 0)); d.text(((bx[0] + bx[2]) / 2, y + 60), "Subscribe", font=f(700, 32), fill=WHITE, anchor="mm")
    # cursor path
    if t > SUB_T + 0.4:
        p = ease((t - (SUB_T + 0.4)) / (CLICK_T - SUB_T - 0.5))
        cx = 1100 + (bxl + 150 - 1100) * p; cy = 760 + (y + 55 - 760) * p
        cursor(lay, cx, cy, CLICK_T <= t < CLICK_T + 0.15)
    im.alpha_composite(lay)

# ---------- generic helpers ----------
def steps(im, t, items, y0=330, gap=190, w=1240, x0=110, size=60):
    for i, it in enumerate(items):
        st, n, s = it[0], it[1], it[2]
        p = ease((t - st) / 0.45)
        if p <= 0: continue
        y = y0 + i * gap; x = x0 - int((1 - p) * 120); a = int(255 * p)
        card = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, w - 1, 149], radius=26, fill=WHITE + (a,), outline=(225, 218, 200, a), width=3)
        col = it[3] if len(it) > 3 else NAVY
        cd.ellipse([30, 25, 130, 125], fill=col + (a,)); cd.text((80, 76), n, font=f(900, 60), fill=WHITE + (a,), anchor="mm")
        cd.text((170, 75), s, font=f(800, size), fill=INK + (a,), anchor="lm")
        im.alpha_composite(card, (x, y))

def grow_bar(d, x, base, w, h, p, col, label=None, im=None, lab_col=WHITE, size=54):
    hh = h * ease(p)
    if hh <= 1: return 0
    d.rounded_rectangle([x, base - hh, x + w, base], radius=10, fill=col)
    return hh

def poly_progress(d, pts, p, col, width=16):
    p = max(0, min(1, p))
    if p <= 0: return None
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = [math.dist(a, b) for a, b in segs]; tot = sum(L); target = tot * p; out = [pts[0]]
    for (a, b), l in zip(segs, L):
        if target >= l: out.append(b); target -= l
        else:
            r = target / l if l else 0; out.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r)); break
    d.line(out, fill=col, width=width, joint="curve")
    r = width * 0.9; e = out[-1]; d.ellipse([e[0] - r, e[1] - r, e[0] + r, e[1] + r], fill=col)
    return out[-1]

def stamp(im, t0, t, text, cx, cy, col=RED, rot=-8, size=64):
    if t < t0: return
    p = back((t - t0) / 0.35)
    fo = f(900, size); tw = ImageDraw.Draw(im).textlength(text, font=fo)
    st = Image.new("RGBA", (int(tw + 80), int(size * 2)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([4, 4, st.width - 5, st.height - 5], radius=18, outline=col, width=10); sd.text((st.width / 2, st.height / 2 + 2), text, font=fo, fill=col, anchor="mm")
    st = st.rotate(rot, expand=True, resample=Image.BICUBIC)
    sc = max(0.05, 1.6 - 0.6 * p); st = st.resize((max(1, int(st.width * sc)), max(1, int(st.height * sc))), Image.LANCZOS)
    im.alpha_composite(st, (int(cx - st.width / 2), int(cy - st.height / 2)))

def hook_pop(im, t, text, t0, t1, y=900, size=190):
    if t0 < t < t1:
        p = (t - t0) / 0.3; out = 1 - ease((t - (t1 - 0.3)) / 0.3) if t > t1 - 0.3 else 1
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pop_text(lay, (W / 2, y), text, f(900, size), (255, 214, 0), p, anchor="mm", stroke=10, sf=INK)
        if out < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * out)))
        im.alpha_composite(lay)

def chip(im, t, t0, t1, text, sub):
    if not (t0 < t < t1): return
    pin = ease((t - t0) / 0.35); pout = ease((t - (t1 - 0.4)) / 0.4)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x = W - 960 + 1000 * (1 - pin) + 1000 * pout; y = 90
    d.rounded_rectangle([x, y, x + 900, y + 150], radius=24, fill=(255, 255, 255, 245))
    d.rounded_rectangle([x + 20, y + 20, x + 200, y + 130], radius=14, fill=(255, 0, 0))
    d.polygon([(x + 92, y + 48), (x + 92, y + 102), (x + 138, y + 75)], fill=WHITE)
    d.text((x + 225, y + 32), sub, font=f(600, 28), fill=GREY); d.text((x + 225, y + 70), text, font=f(800, 36), fill=INK)
    im.alpha_composite(lay)

def run(SRC, SEGS, G, overlay, out_name, end_clip="end.mp4"):
    DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]))
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    vtmp = out_name + ".v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", vtmp], stdin=subprocess.PIPE)
    fs = W * H * 3; i = 0
    while True:
        buf = dec.stdout.read(fs)
        if len(buf) < fs: break
        t = i / FPS
        fr = Image.frombuffer("RGB", (W, H), buf).convert("RGBA"); out = fr
        for a, b, k in SEGS:
            if a - 0.01 <= t <= b + TR:
                p = ease((t - a) / TR) if t <= b else 1 - ease((t - b) / TR)
                if p <= 0: continue
                sl = G[k](min(t, b)); sl.alpha_composite(pip(fr, scale=0.4 + 0.6 * p))
                out = Image.blend(fr, sl, p) if p < 1 else sl
                break
        overlay(out, t); subscribe(out, t)
        enc.stdin.write(out.convert("RGB").tobytes()); i += 1
        if i % 600 == 0: print(out_name, i, flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()
    # subscribe click sound (subtle mouse click)
    ms = int(CLICK_T * 1000); main = out_name + ".main.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vtmp, "-i", SRC, "-i", "subscribe_click.wav",
                    "-filter_complex", f"[2:a]aformat=channel_layouts=stereo,volume=0.35,adelay={ms}|{ms}[d];[1:a][d]amix=inputs=2:duration=first:normalize=0,aresample=48000[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", main], check=True)
    open(out_name + ".cat.txt", "w").write(f"file '{main}'\nfile '{end_clip}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", out_name + ".cat.txt", "-c", "copy", "-movflags", "+faststart", out_name], check=True)
    print("DONE", out_name, i, flush=True)
