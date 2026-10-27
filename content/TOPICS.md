# Insights — topic queue

Each post answers one question people actually type into Google, in plain language, and points to
the tool on the site that runs the numbers. Work top to bottom unless something timely jumps the queue.
Status: `published` · `queued` (written, future date) · `next` · blank (not started).

| # | Question (the title) | Topic | Points to | Status |
|---|---|---|---|---|
| 1 | When should you take Social Security if your spouse is younger? | Social Security | claiming decision, survivor check | published 2026-10-26 |
| 2 | Which account should you take money from first in retirement? | Distribution planning | paycheck builder | next |
| 3 | What happens when you inherit a retirement account? The 10-year rule in plain English | Estate and legacy | the projection, the window | |
| 4 | How much can you safely spend in retirement? | Distribution planning | longevity check | |
| 5 | Required minimum distributions: when they start and how to keep them from raising your taxes | Taxes | execution sheet | |
| 6 | Is a Roth conversion worth it after you retire? | Taxes | the window | |
| 7 | What happens to your Social Security when your spouse dies? | Social Security | survivor check | |
| 8 | Lump sum or monthly pension: how to decide | Distribution planning | pension election | |
| 9 | Should you pay off your mortgage before you retire? | Distribution planning | mortgage payoff | |
| 10 | Retiring before 65: how to cover health insurance until Medicare | Health coverage | coverage bridge | |
| 11 | How Medicare premiums go up with your income, and how to avoid it | Taxes | the projection | |
| 12 | What a market drop in your first years of retirement really does to your plan | Investments | longevity check | |
| 13 | How to give to charity straight from your retirement account | Taxes | execution sheet | |
| 14 | Beneficiary designations: the mistakes that override your will | Estate and legacy | survivor check | |
| 15 | Why your tax bill can go up after your spouse dies | Taxes | survivor check | |
| 16 | How much does long-term care cost, and how do you plan for it? | Care | the care gap | |
| 17 | Bond ladder, annuity or delaying Social Security: three ways to build a retirement paycheck | Distribution planning | paycheck builder | |
| 18 | How taxes on Social Security actually work | Taxes | the projection | |
| 19 | What to do with your old employer retirement plan when you retire | Distribution planning | the baseline | |
| 20 | Leaving money to your kids: tax-smart ways to pass it on | Estate and legacy | the window | |
| 21 | The year-end retirement checklist: what has to happen by December 31 | Taxes | execution sheet | |
| 22 | How to know if you're on track to retire | Planning | the baseline | |
| 23 | Medicare open enrollment: why your plan needs a check-up every year | Health coverage | the plan review | |
| 24 | What a retirement plan review should actually cover | Planning | year in review | |

## Timely slots
- Nov–Dec: #21 (year-end checklist), #13 (charitable giving before Dec 31), #23 (open enrollment ends Dec 7)
- Jan: #22, #5 — Apr: new Social Security figures — Aug: #6 (low-tax window)

## How a post gets made
1. Pick the next topic. 2. Write it in `content/posts/YYYY-MM-DD-slug.html` (JSON header + body).
3. Push to `main`; Netlify builds it into /insights/, the sitemap and feed.xml.
A post dated in the future stays hidden until the first build on or after that date.
