exec(open("/tmp/claude-0/-home-claude/555cd3a5-fd5b-54c8-8899-6c427ac58d18/scratchpad/edit/engine.py").read())

def bucket_icon(d, cx, base_y, w, h, col, label, a=255):
    top_w, bot_w = w, int(w * 0.8)
    poly = [(cx - top_w / 2, base_y - h), (cx + top_w / 2, base_y - h), (cx + bot_w / 2, base_y), (cx - bot_w / 2, base_y)]
    d.polygon(poly, fill=col + (a,), outline=INK + (a,), width=6)
    d.ellipse([cx - top_w / 2 - 6, base_y - h - 22, cx + top_w / 2 + 6, base_y - h + 22], fill=tuple(max(0, c - 40) for c in col) + (a,), outline=INK + (a,), width=6)
    d.text((cx, base_y - h * 0.45), label, font=f(900, 44), fill=WHITE + (a,), anchor="mm", stroke_width=3, stroke_fill=INK + (a,))

S1 = base_slide("THE BASICS", "3 kinds of money in retirement")
def g1(t):  # 17.9-57.2
    im = S1.copy()
    items = [(21.9, GREEN, "SAVINGS", "Already taxed", "Bank, brokerage account", 23.0),
             (28.6, RED, "UNTAXED", "Taxed coming out", "Plan from your old job, or where you moved it", 45.3),
             (50.6, BLUE, "ROTH", "Tax-free", "Grows tax-free, comes out tax-free", 52.8)]
    for i, (tt, col, lab, l1, l2, t2) in enumerate(items):
        p = ease((t - tt) / 0.45)
        if p <= 0: continue
        cx = 300 + i * 520; a = int(255 * p)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        bucket_icon(d, cx, 640 + int((1 - p) * 60), 300, 260, col, lab, a)
        im.alpha_composite(lay)
        pop_text(im, (cx, 720), l1, f(900, 48), col, (t - (tt + 0.4)) / 0.3, anchor="mm")
        pop_text(im, (cx, 790), l2 if len(l2) < 26 else l2[:26].rsplit(" ", 1)[0], f(600, 32), GREY, (t - t2) / 0.3, anchor="mm")
        if len(l2) >= 26: pop_text(im, (cx, 835), l2[len(l2[:26].rsplit(" ", 1)[0]) + 1:], f(600, 32), GREY, (t - t2) / 0.3, anchor="mm")
    return im

S2 = base_slide("THE COMMON ADVICE", "What most people hear")
def g2(t):  # 57.4-81.3
    im = S2.copy()
    steps(im, t, [(59.0, "1", "Spend your savings first", GREEN), (60.6, "2", "Then the untaxed account", RED), (63.0, "3", "Save the Roth for last", BLUE)])
    if t > 73.7: pop_text(im, (110, 900), "Looks great at first: almost no tax", f(800, 56), GREEN, (t - 73.7) / 0.35)
    return im

S3 = base_slide("THE PROBLEM", "The untaxed account keeps growing")
def g3(t):  # 94.6-122.3
    im = S3.copy(); d = ImageDraw.Draw(im)
    base = 920; x0 = 140; bw = 70; gap = 22
    bal = [200, 230, 260, 290, 330, 370, 410, 450]
    for i, h in enumerate(bal):
        grow_bar(d, x0 + i * (bw + gap), base, bw, h, (t - (94.8 + i * 0.12)) / 0.5, (160, 170, 185))
    d.line([110, base, x0 + 8 * (bw + gap) + 20, base], fill=NAVY, width=6)
    pop_text(im, (x0, base + 20), "Account balance", f(700, 36), GREY, (t - 95.0) / 0.3)
    stamp(im, 97.6, t, "AGE 73–75", 1150, 320, col=NAVY, rot=0, size=56)
    pop_text(im, (990, 390), "Forced withdrawals start", f(800, 48), NAVY, (t - 98.4) / 0.3)
    for j, h in enumerate([90, 130, 170]):
        grow_bar(d, 1000 + j * 110, base, 80, h, (t - (101.4 + j * 0.5)) / 0.5, RED)
    pop_text(im, (990, 455), "and they get bigger", f(700, 40), RED, (t - 103.0) / 0.3)
    pop_text(im, (990, 515), "+ Social Security", f(800, 48), BLUE, (t - 106.6) / 0.3)
    stamp(im, 109.0, t, "TAX BRACKET JUMPS", 1150, 1000, size=48, rot=-3)
    pop_text(im, (990, 580), "+ Medicare costs more", f(800, 42), RED, (t - 116.0) / 0.3)
    return im

S4 = base_slide("THE WIDOW'S TAX", "When one spouse passes")
def g4(t):  # 136.0-153.7
    im = S4.copy(); d = ImageDraw.Draw(im)
    base = 900
    pop_text(im, (360, base + 30), "Married", f(800, 50), NAVY, (t - 136.2) / 0.3, anchor="mm")
    grow_bar(d, 210, base, 300, 480, (t - 136.4) / 0.6, NAVY)
    pop_text(im, (360, base - 540), "Brackets", f(700, 40), GREY, (t - 137.0) / 0.3, anchor="mm")
    pop_text(im, (860, base + 30), "Single", f(800, 50), RED, (t - 139.8) / 0.3, anchor="mm")
    grow_bar(d, 710, base, 300, 240, (t - 143.2) / 0.6, RED)
    pop_text(im, (860, base - 300), "About half", f(800, 44), RED, (t - 143.6) / 0.3, anchor="mm")
    d.line([150, base, 1080, base], fill=NAVY, width=6)
    pop_text(im, (1140, 330), "Same money", f(900, 80), NAVY, (t - 146.0) / 0.35)
    pop_text(im, (1140, 430), "Bigger tax bill", f(900, 80), RED, (t - 147.0) / 0.35)
    pop_text(im, (1140, 545), "You didn't avoid the tax.", f(700, 44), GREY, (t - 149.0) / 0.3)
    pop_text(im, (1140, 600), "You pushed it.", f(800, 44), INK, (t - 150.8) / 0.3)
    return im

S5 = base_slide("WHAT USUALLY WORKS BETTER", "Every single year")
def g5(t):  # 153.8-175.4
    im = S5.copy()
    steps(im, t, [(156.0, "1", "Fill low brackets from the untaxed account", RED), (161.6, "2", "Cover the rest from savings", GREEN),
                  (165.0, "3", "Roth last, or for a big one-time cost", BLUE)], size=46, w=1300)
    pop_text(im, (180, 900), "New roof · new car", f(700, 44), GREY, (t - 169.8) / 0.3)
    return im

S6 = base_slide("THE NUMBER TO KNOW", "Married couple · 2026")
def g6(t):  # 175.5-206.3
    im = S6.copy(); d = ImageDraw.Draw(im)
    pop_text(im, (110, 280), "$100,000", f(900, 170), NAVY, (t - 177.8) / 0.4)
    pop_text(im, (120, 480), "of taxable income, after deductions", f(700, 46), GREY, (t - 181.8) / 0.3)
    x0, y0, hh = 110, 590, 120
    p = ease((t - 183.6) / 0.6)
    if p > 0:
        d.rounded_rectangle([x0, y0, x0 + 820 * p, y0 + hh], radius=14, fill=GREEN)
        pop_text(im, (x0 + 30, y0 + 22), "12% bracket", f(900, 60), WHITE, (t - 184.0) / 0.3)
    q = ease((t - 186.2) / 0.5)
    if q > 0:
        d.rounded_rectangle([x0 + 830, y0, x0 + 830 + 520 * q, y0 + hh], radius=14, fill=RED)
        pop_text(im, (x0 + 860, y0 + 22), "22%", f(900, 60), WHITE, (t - 186.6) / 0.3)
    pop_text(im, (110, 780), "Pay 10–12% now", f(900, 70), GREEN, (t - 196.0) / 0.35)
    pop_text(im, (110, 870), "instead of 22–24% later", f(900, 70), RED, (t - 198.4) / 0.35)
    stamp(im, 202.6, t, "ABOUT 10¢ SAVED PER $1", 1150, 360, col=GREEN, rot=-6, size=52)
    return im

S7 = base_slide("AN EXAMPLE", "Bill & Susan · both 65")
def g7(t):  # 206.6-222.2
    im = S7.copy()
    steps(im, t, [(213.0, "$", "$200,000 in savings", GREEN), (214.2, "$", "$900,000 untaxed", RED), (217.2, "$", "$100,000 in a Roth", BLUE),
                  (220.2, "↓", "They spend about $90,000 a year", NAVY)], y0=300, gap=165, size=56)
    return im

def tax_years(d, im, t, t0, heights, col_fn, label_t=None):
    base = 900; x0 = 150; bw = 64; gap = 18
    for i, h in enumerate(heights):
        grow_bar(d, x0 + i * (bw + gap), base, bw, h, (t - (t0 + i * 0.12)) / 0.5, col_fn(i))
    d.line([120, base, x0 + len(heights) * (bw + gap) + 10, base], fill=NAVY, width=6)
    pop_text(im, (x0, base + 18), "65", f(800, 40), GREY, (t - t0) / 0.3)
    pop_text(im, (x0 + 8 * (bw + gap), base + 18), "73", f(800, 40), NAVY, (t - t0) / 0.3)
    pop_text(im, (x0 + 13 * (bw + gap), base + 18), "Survivor", f(800, 36), RED, (t - t0) / 0.3)
    pop_text(im, (x0 + 4, 300), "Taxes each year", f(700, 40), GREY, (t - t0) / 0.3)

COMMON = [40, 40, 45, 45, 50, 50, 55, 55, 300, 310, 320, 330, 340, 470, 480]
OTHER = [160, 165, 165, 170, 170, 175, 175, 180, 185, 185, 190, 190, 195, 230, 235]
S8 = base_slide("THE COMMON WAY", "Savings first")
def g8(t):  # 222.4-248.7
    im = S8.copy(); d = ImageDraw.Draw(im)
    tax_years(d, im, t, 222.8, COMMON, lambda i: GREEN if i < 8 else RED)
    pop_text(im, (180, 700), "Tiny taxes at first", f(800, 46), GREEN, (t - 226.4) / 0.3)
    stamp(im, 238.6, t, "TAX JUMP", 860, 430, size=60, rot=-6)
    pop_text(im, (1120, 300), "+ Widow's tax", f(800, 46), RED, (t - 244.0) / 0.3)
    return im

S9 = base_slide("THE OTHER WAY", "Fill the 12% bracket every year")
def g9(t):  # 249.0-282.8
    im = S9.copy(); d = ImageDraw.Draw(im)
    if t > 249.2:
        base = 900; x0 = 150; bw = 64; gap = 18
        for i, h in enumerate(COMMON):
            x = x0 + i * (bw + gap); d.rounded_rectangle([x, base - h, x + bw, base], radius=10, outline=(200, 200, 200), width=4)
    tax_years(d, im, t, 250.6, OTHER, lambda i: NAVY)
    pop_text(im, (180, 600), "A little more tax early, at a low rate", f(800, 42), NAVY, (t - 257.0) / 0.3)
    pop_text(im, (1040, 470), "Smaller forced withdrawals", f(800, 42), NAVY, (t - 265.8) / 0.3)
    stamp(im, 268.2, t, "TAX BILL STAYS FLAT", 1350, 380, col=GREEN, rot=-5, size=50)
    pop_text(im, (110, 985), "Same money. Same spending. Different order.", f(900, 50), INK, (t - 279.2) / 0.35)
    return im

S10 = base_slide("THE TAKEAWAY", "")
def g10(t):  # 302.3-312.3
    im = S10.copy()
    pop_text(im, (110, 330), "The order you take money out", f(900, 96), NAVY, (t - 302.5) / 0.4)
    pop_text(im, (110, 460), "is a decision,", f(900, 120), GREEN, (t - 303.8) / 0.4)
    pop_text(im, (110, 600), "not a default.", f(900, 120), RED, (t - 305.0) / 0.4)
    pop_text(im, (110, 800), "Check it every year", f(800, 60), GREY, (t - 307.2) / 0.3)
    return im

G = {"a": g1, "b": g2, "c": g3, "d": g4, "e": g5, "f": g6, "g": g7, "h": g8, "i": g9, "j": g10}
SEGS = [(17.8, 57.2, "a"), (57.4, 81.4, "b"), (94.6, 122.3, "c"), (136.0, 153.7, "d"), (153.85, 175.4, "e"), (175.5, 206.3, "f"),
        (206.5, 222.2, "g"), (222.4, 248.7, "h"), (249.0, 282.8, "i"), (302.3, 312.3, "j")]

def overlay(im, t):
    hook_pop(im, t, "TENS OF THOUSANDS IN TAXES", 5.0, 10.2, size=96)
    chip(im, t, 297.6, 302.0, "Roth conversion on $1.2 million", "WATCH NEXT")

import sys
if len(sys.argv) > 1 and sys.argv[1] == "preview":
    times = [float(x) for x in sys.argv[2].split(",")]
    tiles = []
    for tt in times:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(tt), "-i", "base_L1.mp4", "-frames:v", "1", "test/pv1.png"], check=True)
        fr = Image.open("test/pv1.png").convert("RGBA"); out = fr
        for a, b, k in SEGS:
            if a <= tt <= b: sl = G[k](tt); sl.alpha_composite(pip(fr)); out = sl
        overlay(out, tt); subscribe(out, tt); tiles.append(out.convert("RGB").resize((640, 360)))
    s = Image.new("RGB", (1920, 360 * ((len(tiles) + 2) // 3)))
    for i, tl in enumerate(tiles): s.paste(tl, ((i % 3) * 640, (i // 3) * 360))
    s.save("test/pv_L1.jpg", quality=85)
elif len(sys.argv) > 1 and sys.argv[1] == "render":
    run("base_L1.mp4", SEGS, G, overlay, "Which-Account-First-PIP.mp4")
