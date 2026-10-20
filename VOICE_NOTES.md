# V1 — Urdu voice notes

**Why a hybrid (generate-once, play-offline) is the right design:** the advisory set
is finite, so synthesise each approved message to an MP3 **once** with a cloud ur-PK
voice, cache the file, and the phone plays it offline forever — no per-play cost, no
connectivity needed in the field. The farmer app already does live device TTS as an
instant fallback.

**Voices:** Microsoft Azure / edge-tts offer Pakistani Urdu neural voices
`ur-PK-UzmaNeural` (female) and `ur-PK-AsadNeural` (male); Google Cloud also has
ur-PK. For a finite dictionary, pre-recorded/cached clips beat live TTS on cost and
reliability.

**Run it on your machine (not the sandbox):**
```bash
pip install edge-tts
# approve some dictionary entries first (status: approved), then:
python -m kisaan_voice.voice dictionaries/punjab_cotton_v2.json --voice ur-PK-UzmaNeural
```
It writes `audio/PCT/<id>_ur.mp3` and a `manifest.csv`. Fixing a mispronounced word:
change only that entry's `speech_text` (respell the word phonetically), re-run.

**Honest limitation:** this needs internet (the endpoint is online) and was NOT run
in the build sandbox, which blocks that endpoint. Languages without a good free voice
(e.g. Saraiki) become a roadmap item — a human recording — rather than a faked clip.
