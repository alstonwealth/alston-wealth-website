def g1(t):
    im = S1.copy(); d = ImageDraw.Draw(im)
    steps = [(24.6, "1", "Year one: take out 4%"), (30.8, "2", "Raise it for inflation every year"), (33.0, "3", "It should last about 30 years")]
    for i, (st, n, s) in enumerate(steps):
        p = ease((t - st) / 0.45)
        if p <= 0: continue
        y = 330 + i * 190; x = 110 - int((1 - p) * 120)
        a = int(255 * p)
        card = Image.new("RGBA", (1240, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, 1239, 149], radius=26, fill=WHITE + (a,), outline=(225, 218, 200, a), width=3)
        cd.ellipse([30, 25, 130, 125], fill=NAVY + (a,)); cd.text((80, 76), n, font=f(900, 60), fill=WHITE + (a,), anchor="mm")
        cd.text((170, 75), s, font=f(800, 60), fill=INK + (a,), anchor="lm")
        im.alpha_composite(card, (x, y))
    return im

def g2(t):
    im = S2.copy(); d = ImageDraw.Draw(im)
    pop_text(im, (110, 300), "$1,000,000", f(900, 150), GREEN, (t - 35.2) / 0.4)
    pop_text(im, (1090, 318), "× 4%", f(900, 130), NAVY, (t - 36.3) / 0.4)
    if t > 37.1:
        p = ease((t - 37.1) / 0.4); d.rectangle([110, 500, 110 + int(1440 * p), 510], fill=NAVY)
    if t > 37.4:
        v = int(40000 * ease((t - 37.4) / 0.9)); pop_text(im, (110, 540), f"${v:,}", f(900, 170), NAVY, (t - 37.4) / 0.3)
        pop_text(im, (110 + ImageDraw.Draw(im).textlength("$40,000", font=f(900, 170)) + 40, 620), "a year", f(700, 70), GREY, (t - 38.2) / 0.3)
    pop_text(im, (110, 740), "About $3,300 a month", f(900, 100), RED, (t - 39.8) / 0.4)
    if t > 42.4:
        p = back((t - 42.4) / 0.35)
        st = Image.new("RGBA", (560, 130), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([4, 4, 555, 125], radius=18, outline=RED, width=10); sd.text((280, 66), "BEFORE TAXES", font=f(900, 64), fill=RED, anchor="mm")
        st = st.rotate(-8, expand=True, resample=Image.BICUBIC)
        sc = max(0.05, 1.6 - 0.6 * p); st = st.resize((int(st.width * sc), int(st.height * sc)), Image.LANCZOS)
        im.alpha_composite(st, (int(500 - st.width / 2), int(965 - st.height / 2)))
    return im

def g3(t):
    im = S3.copy(); d = ImageDraw.Draw(im)
    bx, bw, base = 180, 300, 960; unit = 0.085  # px per $
    d.line([120, base, 620, base], fill=NAVY, width=6)
    h1 = 3300 * unit * ease((t - 62.6) / 0.8)
    if h1 > 0:
        d.rounded_rectangle([bx, base - h1, bx + bw, base], radius=10, fill=GREEN)
        if t > 63.2: pop_text(im, (bx + bw / 2, base - h1 / 2), "$3,300", f(900, 64), WHITE, (t - 63.2) / 0.3, anchor="mm")
    if t > 63.0: pop_text(im, (530, 790), "From your $1 million", f(800, 54), GREEN, (t - 63.0) / 0.35)
    h2 = 3500 * unit * ease((t - 67.0) / 0.9)
    if h2 > 0:
        top = base - h1 - 8
        d.rounded_rectangle([bx, top - h2, bx + bw, top], radius=10, fill=BLUE)
        if t > 67.6: pop_text(im, (bx + bw / 2, top - h2 / 2), "$3–4K", f(900, 64), WHITE, (t - 67.6) / 0.3, anchor="mm")
    if t > 67.2: pop_text(im, (530, 470), "Social Security", f(800, 54), BLUE, (t - 67.2) / 0.35)
    if t > 67.4: pop_text(im, (530, 535), "for a married couple", f(600, 42), GREY, (t - 67.4) / 0.35)
    if t > 72.0:
        pop_text(im, (1080, 255), "About", f(700, 50), GREY, (t - 72.0) / 0.3)
        pop_text(im, (1080, 300), "$7,000", f(900, 150), NAVY, (t - 72.0) / 0.4)
        pop_text(im, (1085, 465), "a month, before taxes", f(700, 46), GREY, (t - 72.4) / 0.35)
    if t > 75.7:
        p = (t - 75.7) / 0.35
        pop_text(im, (1080, 540), "Enough?", f(900, 110), RED, p)
    return im
def g12(t):
    if t < 35.0: return g1(t)
    if t < 35.35:
        p = ease((t - 35.0) / 0.35); return Image.blend(g1(34.95), g2(t), p)
    return g2(t)