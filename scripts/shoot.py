"""Screenshot built pages at desktop and phone width; report console errors and horizontal overflow."""
import sys, pathlib, http.server, threading, functools
from playwright.sync_api import sync_playwright

site, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
pages = sys.argv[3:]
out.mkdir(parents=True, exist_ok=True)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    for w, h, tag in ((1440, 900, "desk"), (390, 844, "phone")):
        ctx = b.new_context(viewport={"width": w, "height": h})
        for pg in pages:
            page = ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(f"http://127.0.0.1:8765/{pg}", wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(400)
            ov = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            name = pg.replace("/", "_").replace(".html", "") + f"-{tag}.png"
            page.screenshot(path=str(out / name), full_page=True)
            print(f"{tag:5} {pg:32} overflow={ov:<4} errors={errs[:2]}")
            page.close()
        ctx.close()
    b.close()
srv.shutdown()
