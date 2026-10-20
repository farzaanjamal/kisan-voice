"""
V1 — Urdu text-to-speech generator (run locally).

Generates one MP3 per APPROVED entry using edge-tts (free, ur-PK voices Uzma/Asad).
Uses speech_text when present (for respelling mispronounced words), else text.

NOTE: synthesis calls Microsoft's online TTS endpoint, so it must run on your own
machine with internet — it cannot run inside the restricted build sandbox. Nothing
is generated until entries are marked status="approved", by design.

    python -m kisaan_voice.voice dictionaries/punjab_cotton_v2.json --voice ur-PK-UzmaNeural
"""
from __future__ import annotations
import argparse, asyncio, csv
from pathlib import Path
from .dictionary import load_dictionary

DEFAULT_VOICE = "ur-PK-UzmaNeural"   # female; ur-PK-AsadNeural = male


async def _synth(text: str, out: Path, voice: str) -> None:
    import edge_tts  # local dependency
    await edge_tts.Communicate(text, voice).save(str(out))


def generate(dict_path: str, voice: str = DEFAULT_VOICE, lang: str = "ur",
             out_dir: str = "audio", force: bool = False, status: str = "approved") -> None:
    d = load_dictionary(dict_path)
    base = Path(out_dir) / d.code
    base.mkdir(parents=True, exist_ok=True)
    manifest = []
    made = skipped = 0
    for e in d.entries:
        if e["status"] != status:                 # only approved by default
            continue
        if e.get("slots"):                         # templated entries rendered on demand
            continue
        text = (e.get("speech_text", {}) or {}).get(lang) or e["text"].get(lang)
        if not text or text == "[MISSING]":
            continue
        out = base / f"{e['id']}_{lang}.mp3"
        if out.exists() and not force:
            skipped += 1
        else:
            asyncio.run(_synth(text, out, voice))
            made += 1
        manifest.append({"entry_id": e["id"], "code": e["code"], "language": lang,
                         "voice": voice, "file": str(out)})
    with open(base / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["entry_id", "code", "language", "voice", "file"])
        w.writeheader(); w.writerows(manifest)
    print(f"generated {made}, skipped {skipped}, manifest: {base/'manifest.csv'}")
    if not manifest:
        print(f"(no entries with status='{status}' yet — approve some first)")


def main():
    ap = argparse.ArgumentParser(prog="kisaan_voice.voice")
    ap.add_argument("dictionary")
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--lang", default="ur")
    ap.add_argument("--out", default="audio")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--status", default="approved")
    a = ap.parse_args()
    generate(a.dictionary, a.voice, a.lang, a.out, a.force, a.status)


if __name__ == "__main__":
    main()
