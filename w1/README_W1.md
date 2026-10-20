# W1 — Kisan Voice project site (`index.html`)

A single self-contained page: live decoder, compression comparison, mesh simulation
charts + animation, honest built-vs-planned table. No build step, no tracking, no
external data (dictionaries, charts and animation are embedded). Opens from a file or
hosts on GitHub Pages as one link.

## Deploy on GitHub Pages (free)
1. Put `index.html` at the repo root (or in `/docs`).
2. GitHub → repo **Settings → Pages**.
3. **Source:** Deploy from a branch → `main` → `/ (root)` (or `/docs`) → Save.
4. Wait ~1 min; your link is `https://<user>.github.io/<repo>/`.

## Test on a phone before sharing
- Opens fast on mobile data; layout fits a narrow screen.
- Demo: change region/crop and advisory — message, SMS code and packet update.
- Template entry (e.g. weather, with a `days` box) fills the number into the message.
- Language toggle switches Urdu ⇄ Roman Urdu; Urdu shows right-to-left.
- "Listen" speaks via the device voice (quality varies; ur-PK if installed).
- "Decode a code" box: `KV2 PCT 1` works; a bad code shows a clear ⚠ error.
- Evidence charts and the village animation load; pilot shows **[PILOT RESULTS COMING]**.

## Honest notes
- The demo's JS is verified **identical to the Python** on all 121 entries (parity test).
- All advisories are `draft` — the page is a technical demo, not approved farmer advice.
- Fill in the `[GitHub link]`, `[your email]`, and the 2-minute video before sharing widely.
