# Alston Wealth site — source

- `config.json` — every firm fact on the site: email, phone, office address, Form ADV link,
  disclosure, booking and call links, domain. Anything still in [brackets] shows on the page
  in brackets until it is filled.
- `src/_partials/` — the shared header, footer and head. The build drops them into every page,
  so a nav or footer change is made once.
- `src/` — the pages. Interior pages were converted from the Decision Calendar site;
  the storefront pages (home, services, who we help, how we work, learn, about, contact) are new.
- `scripts/build.py` — fills `src/` from `config.json`, stamps the current month into the
  homepage, writes `dist/site/` and a deployable zip, and lists anything still bracketed.
  Run: `python3 -I scripts/build.py .`
- `scripts/shoot.py` — screenshots pages at desktop and phone width and reports script
  errors and sideways scrolling.

Deploy: automatic. This repository (github.com/alstonwealth/alston-wealth-website) is linked to the
Netlify project `alstonwealth`. Every push to `main` makes Netlify run `python3 scripts/build.py .`
and publish `dist/site` (settings in `netlify.toml`). No folder uploads.

## Photos

Each photo slot shows a labelled placeholder until a file with the right name is in `src/images/`.
Drop the file in, rebuild, redeploy — no code changes.

| File | Shot | Used on |
|---|---|---|
| `team-group.jpg` | Alex, Andrew and Michael together. Portrait (4:5) for the homepage, also cropped 4:3 on About | Home hero, About |
| `headshot-alex.jpg` | Alex headshot, 4:5 (currently the existing photo) | Home, About |
| `headshot-andrew.jpg` | Andrew headshot, 4:5, same light and background as Alex | Home, About |
| `headshot-aaron.jpg` | Aaron headshot, 4:5, same light and background (Board Member) | Home, About |
| `headshot-michael.jpg` | Michael headshot, 4:5, same light and background | Home, About |
| `michael-document.jpg` | Michael holding the original incorporation document, 4:5 | Home |
| `incorporation-document.jpg` | Flat full-page scan of the document | About |
| `working-zoom.jpg` | Alex on a video call, from beside the screen, 3:2 | How we work |
| `working-review.jpg` | Alex and Andrew going over a printed plan, 3:2 | How we work |

## Hero video

Full-width montage behind the homepage headline: office → porch couple → father and son →
meeting table → handshake (last, by Alex's choice), about 4 seconds each with crossfades, looping
seamlessly (16 s). A navy tint over the footage keeps the headline readable.

Two versions, and each visitor downloads only one:
- desktop `src/media/hero-montage.webm` / `.mp4` (1280×720, about 2.7 MB) and `hero-poster.jpg`
- phone `hero-montage-mobile.webm` / `.mp4` (405×720, about 1.1 MB) and `hero-poster-mobile.jpg`.
  Each scene is cropped to its own subject, so phones don't land on an empty wall. The porch
  couple sit too far apart to crop, so that scene shows the whole frame over a blurred copy.

Source clips (AI-generated in Gemini, image first then animated, faceless by design) are in
`source-video/`. Rebuild everything with `scripts/build-hero-montage.sh <scratch_dir>` from the
alston/ folder. Scene order, start times and phone crop positions are the table at the top of
that script. The porch clip has a morph at 4.0–4.8 s, so only the part after 5.2 s is used.
