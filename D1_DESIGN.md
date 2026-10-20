# D1 — Dictionary format v2 (design note)

**Goal:** compact codes, easy to extend, safe to update, simple enough to explain
in an interview. Every choice below is one sentence.

## Entry schema
Validated by `kisaan_voice/dictionary.schema.json` (JSON Schema draft-07). Required
per entry: `id` (integer, never reused), `code` (`PCT-PST-012` = dictionary-category-
number), `category` (fixed list), `crop_stage`, `urgency`, `text{lang}`, `sources`
(≥1), `confidence`, `status`. Optional: `speech_text{lang}`, `slots`, `season_months`,
`source_summary`, `reviewed_by` (role, not name), `reviewed_on`.

- **id vs code:** `id` is the stable integer that the binary form carries; `code` is
  the human-readable label. ids are never reused, so an old packet can never resolve
  to a new message.
- **status** gates sending: only `approved` entries may reach a farmer (enforced in P2).
- **Fixed category list:** sowing, variety, seed, fertilizer, irrigation, weeds,
  pest_alert, disease_alert, weather_alert, harvest, storage, safety, market_info.

## Typed template slots
A slot is `int` (with min/max) or `enum` (value → already-translated string). The
renderer refuses any value outside the spec, so **no untranslated free text can ever
enter a message** (`templates.py`). Templates multiply coverage without new entries:
one "rain in {days} days" entry serves every day-count.

## Two encodings of one advisory
**SMS form** (stays in GSM-7, so it never bloats to UCS-2):
```
KV2 PCT 4 3      = format marker | dictionary code | entry id | slot value(s)
```
**Binary form** (for a BLE advertisement):
```
byte 0        format_version (=2)
byte 1        dictionary_id
byte 2        dictionary_version
varint        entry_id
byte          slot_count,  then each slot value as a varint
bytes 2       message_id (uint16)
byte          ttl
byte          hop
```
Measured worst case in the sample dictionary: **10 bytes**, well inside the ~27
usable bytes of a 31-byte legacy advertisement (test: `test_binary_fits_ble.py`).
Escape hatch for the future: BLE 5 extended advertising allows up to 255 bytes, but
support varies on cheap phones — so v2 is built to fit the legacy budget.

## Versioning safety
The binary form carries `dictionary_version`. On a mismatch the decoder **raises
rather than guessing** (`test_version_mismatch_refuses`) — a device with the wrong
dictionary never shows a wrong message. New entries get new ids; old codes keep working.

## Example entries
See `dictionaries/punjab_cotton_v2.json`. Every entry there is `status: draft` with
`sources: [NEEDS SOURCE]` — they are migrated placeholders for wiring and benchmarking,
**not approved advice**, pending R1 sourcing and expert review.
