"""Fill src/ from config.json into dist/, stamp the current month, zip it, and list what's unfinished.
Usage: python3 -I build.py <alston_dir>
"""
import json, re, sys, shutil, pathlib, datetime, zipfile

ROOT = pathlib.Path(sys.argv[1])
PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
# "preview" builds into dist-preview/ and fills empty photo slots from preview-photos/.
# Those stand-in images never reach dist/, so they can't ship to the live site by accident.
SRC, DIST = ROOT / "src", ROOT / ("dist-preview" if PREVIEW else "dist") / "site"
cfg = {k: v for k, v in json.loads((ROOT / "config.json").read_text()).items() if not k.startswith("_")}

MONTHS = [
    ("January", "Where do I actually stand?", "Net worth, real spending, and the one ratio the whole year turns on.", "01-the-baseline"),
    ("February", "Will it last?", "How long the money holds — and how the answer changes if the first five years go badly.", "02-longevity-check"),
    ("March", "How does a pile become a paycheck?", "What's guaranteed for life, what's variable, and the gap between them.", "03-paycheck-builder"),
    ("April", "When should I take Social Security?", "The largest single decision most households make — and why the survivor benefit matters more than the breakeven.", "04-claiming-decision"),
    ("May", "What about health insurance?", "Bridging to 65, the subsidy cliff, and what Medicare does not cover.", "05-coverage-bridge"),
    ("June", "What if one of us dies?", "Income falls more than 20% and the tax bill often rises. Entirely predictable.", "06-survivor-check"),
    ("July", "What will I owe this year?", "Build the number now so December isn't a guess — then fix your withholding.", "07-the-projection"),
    ("August", "Is this my low-tax window?", "What the next dollar actually costs — not what the bracket table says.", "08-the-window"),
    ("September", "What if one of us needs care?", "What care costs, what Medicare pays for, and what a long event does to the healthy spouse.", "09-the-care-gap"),
    ("October", "Is my coverage still right?", "Formularies and networks change every year. Open enrollment closes December 7.", "10-the-plan-review"),
    ("November", "What is due by December 31?", "Distributions, conversions, harvesting, charitable transfers — all in one month.", "11-the-execution-sheet"),
    ("December", "How did the year go?", "Close every open item, then look back at the decisions rather than the balance.", "12-the-year-in-review"),
]
today = datetime.date.today()
name, q, t, tool = MONTHS[today.month - 1]
cfg.update(MO_NAME=name, MO_Q=q, MO_T=t, MO_READ=f"read/{today.month:02d}.html", MO_TOOL=f"tools/{tool}.html",
           MONTH_YEAR=today.strftime("%B %Y"),
           PHONE_TEL=re.sub(r"[^\d+]", "", cfg["PHONE"]) or "#")

if DIST.parent.exists():
    shutil.rmtree(DIST.parent)
shutil.copytree(SRC, DIST, ignore=shutil.ignore_patterns("_partials"))
if PREVIEW and (ROOT / "preview-photos").exists():
    for ph in (ROOT / "preview-photos").iterdir():
        if ph.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and not (SRC / "images" / ph.name).exists():
            shutil.copy(ph, DIST / "images" / ph.name)
# ── Insights (the blog). Each post is content/posts/<date>-<slug>.html: a JSON header in an
#    HTML comment, then the article body. Posts dated in the future, or marked "draft", are skipped,
#    so a post can be queued and goes live on the first build on or after its date.
POSTS = []
for pf in sorted((ROOT / "content" / "posts").glob("*.html")) if (ROOT / "content" / "posts").exists() else []:
    raw = pf.read_text()
    meta = json.loads(re.match(r"\s*<!--(.*?)-->", raw, re.S).group(1))
    meta["body"] = raw.split("-->", 1)[1].strip()
    if meta.get("draft") or datetime.date.fromisoformat(meta["date"]) > today:
        continue
    POSTS.append(meta)
POSTS.sort(key=lambda m: m["date"], reverse=True)
TPL = (SRC / "_partials" / "post.html").read_text() if POSTS else ""
def esc(t): return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
def nice(d): return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")
if POSTS:
    (DIST / "insights").mkdir(exist_ok=True)
    for m in POSTS:
        tools = "".join(f'<p><a class="aw-more" href="../{u}">{esc(t)}</a></p>' for u, t in m.get("tools", []))
        schema = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": m["title"],
            "description": m["description"], "datePublished": m["date"], "dateModified": m.get("updated", m["date"]),
            "author": {"@id": "{{SITE_URL}}/about.html#alex"}, "publisher": {"@id": "{{SITE_URL}}/#org"},
            "mainEntityOfPage": "{{SITE_URL}}/insights/" + m["slug"] + ".html",
            "image": "{{SITE_URL}}/" + m.get("image", "og-image.png")})
        page = (TPL.replace("%TITLE%", esc(m["title"])).replace("%DESC%", esc(m["description"]))
                   .replace("%SLUG%", m["slug"]).replace("%TOPIC%", esc(m.get("topic", "Insights")))
                   .replace("%DATE%", m["date"]).replace("%NICEDATE%", nice(m["date"]))
                   .replace("%AUTHOR%", esc(m.get("author", "Alex Alston"))).replace("%TOOLS%", tools)
                   .replace("%SCHEMA%", schema).replace("%IMAGE%", "{{SITE_URL}}/" + m.get("image", "og-image.png")).replace("%BODY%", m["body"]))
        (DIST / "insights" / f'{m["slug"]}.html').write_text(page)
    cards = "".join(
        f'<a class="aw-card" href="{m["slug"]}.html"><p class="aw-post-meta">{esc(m.get("topic","Insights"))} · {nice(m["date"])}</p>'
        f'<h2 class="aw-h3" style="font-size:23px">{esc(m["title"])}</h2><p>{esc(m["description"])}</p><span class="aw-more">Read</span></a>'
        for m in POSTS)
    idx = (SRC / "_partials" / "insights-index.html").read_text().replace("%CARDS%", cards)
    (DIST / "insights" / "index.html").write_text(idx)

PARTS = {k: (SRC / "_partials" / f"{k.lower()}.html").read_text() for k in ("HEAD", "HEADER", "FOOTER")}
cfg["YEAR"] = str(today.year)
FAVICON = ('<link rel="icon" href="{{P}}favicon.svg" type="image/svg+xml">'
           '<link rel="icon" href="{{P}}favicon.ico" sizes="any">'
           '<link rel="apple-touch-icon" href="{{P}}apple-touch-icon.png">\n')

unknown = set()
for f in DIST.rglob("*"):
    if f.suffix not in (".html", ".js", ".css"):
        continue
    s = f.read_text()
    if f.suffix == ".html":
        for k, v in PARTS.items():
            s = s.replace(f"<!--AW:{k}-->", v)
        if 'rel="icon"' not in s:
            s = s.replace("</head>", FAVICON + "</head>", 1)
        s = s.replace("{{P}}", "../" * (len(f.relative_to(DIST).parts) - 1))
        # one canonical address per page, so Google treats alstonwealth.com as the original
        rel = f.relative_to(DIST).as_posix()
        if 'rel="canonical"' not in s and 'name="robots" content="noindex"' not in s:
            url = "{{SITE_URL}}/" + ("" if rel == "index.html" else rel[:-10] if rel.endswith("/index.html") else rel)
            s = s.replace("</head>", f'<link rel="canonical" href="{url}">\n</head>', 1)
    def fill(m):
        k = m.group(1)
        if k not in cfg:
            unknown.add(k); return m.group(0)
        v = cfg[k]
        return v.replace("&", "&amp;") if f.suffix == ".html" and k in ("DISCLOSURE", "ADDRESS") else v
    s = re.sub(r"\{\{([A-Z_]+)\}\}", fill, s)
    if f.suffix == ".html":
        # Photo slots whose file isn't in images/ yet: a team headshot becomes a navy brand tile,
        # every other slot is left out entirely. Drop the photo into src/images/ and rebuild to bring it back.
        def photo(m):
            fig = m.group(0)
            src = re.search(r'<img src="([^"]+)"', fig)
            if not src or (f.parent / src.group(1)).exists():
                return fig
            if "headshot-" in src.group(1):
                up = "../" * (len(f.relative_to(DIST).parts) - 1)
                return f'<div class="aw-mono aw-r45"><img src="{up}favicon.svg" alt="" width="96" height="96"></div>'
            return ""
        s = re.sub(r'<figure class="aw-ph[^"]*"[^>]*>.*?</figure>', photo, s, flags=re.S)
        s = re.sub(r'<div class="aw-split-media"[^>]*>\s*</div>', "", s)
        # Contact details still in [brackets] are left off the page rather than shown as brackets.
        for key in ("EMAIL", "PHONE"):
            if cfg[key].startswith("["):
                s = re.sub(r'<[a-z]+ [^>]*data-needs="%s"[^>]*>.*?<!--/needs-->' % key, "", s, flags=re.S)
    # the static grid highlight, so the page is right even before scripts run
    if f.name == "index.html" and f.parent == DIST:
        s = s.replace(f'class="mo" href="read/{today.month:02d}.html"', f'class="mo is-now" href="read/{today.month:02d}.html"')
    f.write_text(s)
assert not unknown, f"unfilled tokens: {unknown}"

# search files: every indexable page in the sitemap, and a robots file pointing to it
pages = []
for f in sorted(DIST.rglob("*.html")):
    t = f.read_text()
    if 'name="robots" content="noindex"' in t:
        continue
    rel = f.relative_to(DIST).as_posix()
    pages.append(cfg["SITE_URL"] + "/" + ("" if rel == "index.html" else rel[:-10] if rel.endswith("/index.html") else rel))
pages.sort(key=lambda u: (u != cfg["SITE_URL"] + "/", u))
(DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><lastmod>{today.isoformat()}</lastmod></url>\n" for u in pages) + "</urlset>\n")
if POSTS:
    items = "".join(
        f"  <item><title>{esc(m['title'])}</title><link>{cfg['SITE_URL']}/insights/{m['slug']}.html</link>"
        f"<guid>{cfg['SITE_URL']}/insights/{m['slug']}.html</guid>"
        f"<pubDate>{datetime.datetime.combine(datetime.date.fromisoformat(m['date']), datetime.time(12)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>"
        f"<description>{esc(m['description'])}</description></item>\n" for m in POSTS)
    (DIST / "insights" / "feed.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>\n'
        f"  <title>Alston Wealth — Insights</title><link>{cfg['SITE_URL']}/insights/</link>"
        "<description>Plain-English answers to the money decisions around retirement, taxes and legacy.</description>\n"
        + items + "</channel></rss>\n")
(DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {cfg['SITE_URL']}/sitemap.xml\n")

# Clean addresses: the host (Cloudflare Pages) serves about.html at /about and redirects the .html form,
# so every link, canonical, sitemap and feed entry uses the short form. Preview builds keep .html
# so the files still open straight from disk.
if not PREVIEW:
    site = re.escape(cfg["SITE_URL"])
    def clean(path):
        base, _, frag = path.partition("#")
        if base.endswith("index.html"):
            base = base[:-10] or "./"
        elif base.endswith(".html"):
            base = base[:-5]
        return base + ("#" + frag if frag else "")
    absol = re.compile(r"(%s/)([^\"'<>\s]*?\.html(?:#[^\"'<>\s]*)?)(?=[\"'<\s])" % site)
    rel = re.compile(r'(href=")(?!https?:|mailto:|tel:|#|//|data:)([^"]*?\.html(?:#[^"]*)?)(")')
    for f in list(DIST.rglob("*.html")) + list(DIST.rglob("*.xml")):
        s = f.read_text()
        s2 = absol.sub(lambda m: m.group(1) + clean(m.group(2)), s)
        if f.suffix == ".html":
            s2 = rel.sub(lambda m: m.group(1) + clean(m.group(2)) + m.group(3), s2)
        if s2 != s:
            f.write_text(s2)

# what still needs a real fact
todo = sorted({m for f in DIST.rglob("*.html") for m in re.findall(r"\[[^\]\[]{2,300}\]", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", f.read_text(), flags=re.S)))})
print("Still in brackets on the site:")
for x in todo:
    print("  ", x)

if PREVIEW:
    print("preview built", DIST); sys.exit(0)
z = ROOT / "dist" / f"alston-wealth-site-{today.isoformat()}.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(DIST.rglob("*")):
        zf.write(f, f.relative_to(DIST.parent))
print("built", z)
