exec(open("/tmp/claude-0/-home-claude/555cd3a5-fd5b-54c8-8899-6c427ac58d18/scratchpad/edit/engine.py").read())
S1 = base_slide("THE 4% RULE", "The old rule of thumb")
S2 = base_slide("THE MATH", "What $1 million pays you")
S3 = base_slide("ADD SOCIAL SECURITY", "Your monthly paycheck")
exec(open("l2_slides_part.py").read())

S4 = base_slide("IS IT ENOUGH?", "Three things decide it")
def g4(t):  # 76.8-84.7
    im = S4.copy()
    steps(im, t, [(77.4, "1", "What you actually spend"), (78.0, "2", "When you retire", GREY), (78.4, "3", "What kind of money it is", GREY)])
    pop_text(im, (110, 900), "Not what you think you spend", f(800, 56), RED, (t - 79.6) / 0.35)
    return im

S5 = base_slide("1 · WHAT YOU SPEND", "Do this one time")
def g5(t):  # 111.6-123.0
    im = S5.copy()
    steps(im, t, [(111.9, "1", "Pull 12 months of bank statements"), (112.8, "2", "Add your credit card statements"), (113.8, "3", "Add it all up")])
    stamp(im, 120.0, t, "USUALLY HIGHER THAN YOU THINK", 760, 950, size=48, rot=-4)
    return im

S6 = base_slide("1 · WHAT YOU SPEND", "The first years cost the most")
def g6(t):  # 124.2-143.6
    im = S6.copy(); d = ImageDraw.Draw(im)
    base = 930; labels = ["Early years", "Middle years", "Later years"]; hs = [470, 300, 250]; cols = [RED, NAVY, NAVY]
    starts = [124.8, 125.4, 125.8]
    for i in range(3):
        x = 160 + i * 360; hh = grow_bar(d, x, base, 260, hs[i], (t - starts[i]) / 0.7, cols[i])
        pop_text(im, (x + 130, base + 50), labels[i], f(800, 44), INK, (t - starts[i]) / 0.3, anchor="mm")
    d.line([120, base, 1240, base], fill=NAVY, width=6)
    for j, (tt, s) in enumerate([(128.6, "Travel"), (129.4, "Fix up the house"), (130.2, "Help the kids")]):
        pop_text(im, (1260, 380 + j * 90), s, f(800, 52), RED, (t - tt) / 0.3)
    return im

S7 = base_slide("2 · WHEN YOU RETIRE", "Retire before 65?")
def g7(t):  # 143.9-158.0
    im = S7.copy(); d = ImageDraw.Draw(im)
    pop_text(im, (110, 300), "No Medicare yet", f(900, 110), NAVY, (t - 146.0) / 0.4)
    pop_text(im, (110, 470), "Health insurance for a couple:", f(700, 56), GREY, (t - 149.6) / 0.35)
    pop_text(im, (110, 540), "$1,000+ a month", f(900, 150), RED, (t - 151.0) / 0.4)
    pop_text(im, (110, 760), "Straight out of your $40,000", f(800, 64), NAVY, (t - 154.0) / 0.35)
    return im

S8 = base_slide("3 · WHAT KIND OF MONEY", "Untaxed money isn't all yours")
def g8(t):  # 158.3-179.1
    im = S8.copy(); d = ImageDraw.Draw(im)
    x0, y0, wfull, hh = 110, 380, 1250, 170
    p = ease((t - 160.6) / 0.6)
    if p > 0:
        d.rounded_rectangle([x0, y0, x0 + wfull * p, y0 + hh], radius=16, fill=GREEN)
        pop_text(im, (x0 + 40, y0 + 40), "$1,000,000", f(900, 80), WHITE, (t - 160.9) / 0.3)
    pop_text(im, (110, 300), "In the plan from your old job, or another untaxed account", f(700, 40), GREY, (t - 161.0) / 0.3)
    q = ease((t - 170.6) / 0.6)
    if q > 0:
        tx = wfull * 0.175 * q
        d.rounded_rectangle([x0 + wfull - tx, y0, x0 + wfull, y0 + hh], radius=16, fill=RED)
        pop_text(im, (x0 + wfull - 150, y0 + hh + 20), "Taxes", f(800, 50), RED, (t - 171.0) / 0.3)
    pop_text(im, (110, 680), "Worth about", f(700, 56), GREY, (t - 174.2) / 0.3)
    pop_text(im, (110, 740), "$800,000 – $850,000", f(900, 110), NAVY, (t - 174.6) / 0.4)
    return im

S9 = base_slide("INFLATION", "Your paycheck has to grow")
def g9(t):  # 179.3-194.5
    im = S9.copy(); d = ImageDraw.Draw(im)
    base = 930
    grow_bar(d, 200, base, 300, 400, (t - 181.6) / 0.7, NAVY)
    pop_text(im, (350, base - 470), "$40,000", f(900, 70), NAVY, (t - 182.0) / 0.3, anchor="mm")
    pop_text(im, (350, base + 50), "Today", f(800, 46), INK, (t - 181.8) / 0.3, anchor="mm")
    grow_bar(d, 640, base, 300, 540, (t - 183.6) / 0.8, RED)
    pop_text(im, (790, base - 610), "$54,000", f(900, 70), RED, (t - 184.2) / 0.3, anchor="mm")
    pop_text(im, (790, base + 50), "In 10 years", f(800, 46), INK, (t - 183.8) / 0.3, anchor="mm")
    d.line([140, base, 1000, base], fill=NAVY, width=6)
    pop_text(im, (1080, 420), "At 3% a year", f(800, 60), GREY, (t - 180.6) / 0.3)
    pop_text(im, (1080, 500), "just to stay even", f(800, 60), GREY, (t - 192.2) / 0.3)
    return im

S10 = base_slide("THE BIGGEST RISK", "A bad first year")
def g10(t):  # 199.4-223.6
    im = S10.copy(); d = ImageDraw.Draw(im)
    pts = [(150, 380), (420, 380), (560, 690), (760, 690)]
    pop_text(im, (110, 300), "$1,000,000", f(900, 64), GREEN, (t - 199.8) / 0.3)
    e = poly_progress(d, pts[:2], (t - 200.2) / 0.6, NAVY)
    if t > 204.6:
        poly_progress(d, pts[1:], (t - 204.6) / 0.9, RED)
        pop_text(im, (300, 480), "-20%", f(900, 90), RED, (t - 205.2) / 0.3)
    pop_text(im, (560, 730), "About $760,000", f(900, 80), RED, (t - 210.0) / 0.35)
    pop_text(im, (1000, 330), "To get back to $1 million:", f(700, 50), GREY, (t - 214.0) / 0.3)
    pop_text(im, (1000, 400), "+32%", f(900, 170), NAVY, (t - 218.2) / 0.4)
    pop_text(im, (1000, 600), "not 20%", f(800, 60), RED, (t - 216.4) / 0.3)
    pop_text(im, (110, 900), "...while you keep taking money out every year", f(800, 50), INK, (t - 220.6) / 0.35)
    return im

S11 = base_slide("SAME $1 MILLION", "Two retirees, two outcomes")
def g11(t):  # 223.9-255.4
    im = S11.copy(); d = ImageDraw.Draw(im)
    x0, base = 150, 900
    d.line([x0, base, 1380, base], fill=NAVY, width=5); d.line([x0, 330, x0, base], fill=NAVY, width=5)
    good = [(150, 560), (300, 500), (450, 520), (600, 450), (750, 470), (900, 420), (1050, 440), (1200, 400), (1350, 410)]
    bad = [(150, 560), (300, 720), (450, 740), (600, 760), (750, 800), (900, 830), (1050, 860), (1200, 890), (1290, 900)]
    poly_progress(d, good, (t - 226.4) / 3.0, GREEN, 14)
    poly_progress(d, bad, (t - 226.4) / 3.0, RED, 14)
    pop_text(im, (1390, 380), "Good first years", f(800, 44), GREEN, (t - 229.6) / 0.3)
    pop_text(im, (1120, 790), "Runs out", f(800, 44), RED, (t - 232.0) / 0.3)
    pop_text(im, (360, 760), "Bad year one", f(800, 40), RED, (t - 238.6) / 0.3)
    pop_text(im, (160, 950), "Sequence of returns risk", f(900, 56), NAVY, (t - 252.0) / 0.35)
    return im

S12 = base_slide("THE FIX", "Two buckets of money")
def g12b(t):  # 255.8-268.3
    im = S12.copy(); d = ImageDraw.Draw(im)
    for i, (tt, col, h1, h2, h3) in enumerate([(256.0, GREEN, "SAFE MONEY", "2–3 years of withdrawals", "Cash · quality bonds · guarantees"),
                                               (264.0, BLUE, "GROWTH MONEY", "Left alone to recover", "You never sell at the bottom")]):
        p = ease((t - tt) / 0.45)
        if p <= 0: continue
        x = 110 + i * 680; y = 330 + int((1 - p) * 60); a = int(255 * p)
        c = Image.new("RGBA", (620, 520), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.rounded_rectangle([0, 0, 619, 519], radius=30, fill=WHITE + (a,), outline=col + (a,), width=8)
        cd.rounded_rectangle([0, 0, 619, 120], radius=30, fill=col + (a,)); cd.rectangle([0, 80, 619, 120], fill=col + (a,))
        cd.text((310, 62), h1, font=f(900, 54), fill=WHITE + (a,), anchor="mm")
        cd.text((310, 230), h2, font=f(800, 46), fill=INK + (a,), anchor="mm")
        cd.text((310, 330), h3, font=f(600, 34), fill=GREY + (a,), anchor="mm")
        im.alpha_composite(c, (x, y))
    return im

S13 = base_slide("HOW WE THINK ABOUT IT", "")
def g13(t):  # 282.6-294.3
    im = S13.copy()
    pop_text(im, (110, 330), "Protecting against", f(900, 100), NAVY, (t - 283.0) / 0.4)
    pop_text(im, (110, 460), "a big loss matters more", f(900, 100), RED, (t - 283.6) / 0.4)
    pop_text(im, (110, 590), "than catching a big gain.", f(900, 100), NAVY, (t - 284.4) / 0.4)
    return im

G = {"a": g12, "b": g3, "c": g4, "d": g5, "e": g6, "f": g7, "g": g8, "h": g9, "i": g10, "j": g11, "k": g12b, "l": g13}
SEGS = [(23.7, 44.6, "a"), (62.4, 76.6, "b"), (76.8, 84.8, "c"), (111.6, 123.1, "d"), (124.2, 143.7, "e"), (143.9, 158.1, "f"),
        (158.3, 179.15, "g"), (179.3, 194.5, "h"), (199.3, 223.7, "i"), (223.9, 255.5, "j"), (255.7, 268.4, "k"), (282.6, 294.3, "l")]

def overlay(im, t):
    hook_pop(im, t, "$1,000,000", 0.15, 3.3)

if __name__ == "__main__" or True:
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        times = [float(x) for x in sys.argv[2].split(",")]
        tiles = []
        for tt in times:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(tt), "-i", "base_L2.mp4", "-frames:v", "1", "test/pv.png"], check=True)
            fr = Image.open("test/pv.png").convert("RGBA"); out = fr
            for a, b, k in SEGS:
                if a <= tt <= b: sl = G[k](tt); sl.alpha_composite(pip(fr)); out = sl
            overlay(out, tt); subscribe(out, tt); tiles.append(out.convert("RGB").resize((640, 360)))
        s = Image.new("RGB", (1920, 360 * ((len(tiles) + 2) // 3)))
        for i, tl in enumerate(tiles): s.paste(tl, ((i % 3) * 640, (i // 3) * 360))
        s.save("test/pv_L2.jpg", quality=85)
    elif len(sys.argv) > 1 and sys.argv[1] == "render":
        run("base_L2.mp4", SEGS, G, overlay, "Is-1-Million-Enough-PIP.mp4")
