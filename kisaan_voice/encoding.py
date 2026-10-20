"""
Two encodings of one advisory, and decoding with a safe language fallback.

  SMS form   : short ASCII that stays in GSM-7, e.g.  "KV2 PCT 4 3"
               (format marker, dictionary code, entry id, slot values)
  Binary form: compact bytes for a BLE advertisement (<= 27 usable bytes)

Decoding never returns a wrong message: unknown codes, dictionary-version
mismatches and bad slots all raise instead of guessing.
"""
from __future__ import annotations
from typing import Dict, List

from .dictionary import Dictionary, DictionaryError
from .templates import validate_and_render, SlotError

FORMAT_MARKER = "KV2"
FORMAT_VERSION = 2
FALLBACK_ORDER = ["ur", "roman_ur"]   # regional -> urdu -> roman is applied per-call


class EncodingError(Exception):
    pass


# ---------------- varint (LEB128) for the binary form ----------------
def _wv(n: int) -> bytes:
    if n < 0:
        raise EncodingError("varint cannot encode negatives")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def _rv(buf: bytes, i: int):
    shift = n = 0
    while True:
        b = buf[i]; i += 1
        n |= (b & 0x7F) << shift
        if not (b & 0x80):
            return n, i
        shift += 7


# ---------------- SMS form ----------------
def encode_sms(d: Dictionary, entry_id: int, slot_values: Dict[str, int] | None = None) -> str:
    entry = d.entry(entry_id)                      # raises on unknown id
    slot_values = slot_values or {}
    vals = []
    for s in entry.get("slots", []):
        if s["name"] not in slot_values:
            raise EncodingError(f"entry {entry_id} needs slot value '{s['name']}'")
        vals.append(str(int(slot_values[s["name"]])))
    parts = [FORMAT_MARKER, d.code, str(entry_id)] + vals
    return " ".join(parts)


def decode_sms(code: str, dicts: List[Dictionary], lang: str, strict_lang: bool = False) -> dict:
    toks = code.strip().split()
    if len(toks) < 3 or toks[0] != FORMAT_MARKER:
        raise EncodingError(f"not a valid KV2 SMS code: {code!r}")
    _, dcode, sid, *raw_vals = toks
    d = next((x for x in dicts if x.code == dcode), None)
    if d is None:
        raise EncodingError(f"no dictionary with code {dcode!r} loaded")
    try:
        entry = d.entry(int(sid))
    except (ValueError, DictionaryError) as e:
        raise EncodingError(str(e)) from None
    values = {s["name"]: int(v) for s, v in zip(entry.get("slots", []), raw_vals)}
    return _render(d, entry, lang, values, strict_lang)


# ---------------- Binary form ----------------
def encode_binary(d: Dictionary, entry_id: int, slot_values: Dict[str, int] | None,
                  msg_id: int, ttl: int = 4, hop: int = 0) -> bytes:
    entry = d.entry(entry_id)
    out = bytearray([FORMAT_VERSION, d.id & 0xFF, d.version & 0xFF])
    out += _wv(entry_id)
    slots = entry.get("slots", [])
    out.append(len(slots))
    for s in slots:
        out += _wv(int((slot_values or {})[s["name"]]))
    out += bytes([(msg_id >> 8) & 0xFF, msg_id & 0xFF, ttl & 0xFF, hop & 0xFF])
    return bytes(out)


def decode_binary(buf: bytes, dicts: List[Dictionary], lang: str, strict_lang: bool = False) -> dict:
    if len(buf) < 4 or buf[0] != FORMAT_VERSION:
        raise EncodingError("unsupported binary format version")
    did, dver, i = buf[1], buf[2], 3
    d = next((x for x in dicts if x.id == did), None)
    if d is None:
        raise EncodingError(f"no dictionary with id {did} loaded")
    if d.version != dver:
        raise EncodingError(
            f"dictionary version mismatch: packet wants v{dver}, loaded v{d.version} "
            f"-- refusing to decode to avoid showing a wrong message")
    entry_id, i = _rv(buf, i)
    entry = d.entry(entry_id)
    nslots = buf[i]; i += 1
    values = {}
    for s in entry.get("slots", [])[:nslots]:
        v, i = _rv(buf, i)
        values[s["name"]] = v
    return _render(d, entry, lang, values, strict_lang)


# ---------------- shared rendering with fallback ----------------
def _render(d: Dictionary, entry: dict, lang: str, values: dict, strict_lang: bool) -> dict:
    order = [lang] + [l for l in FALLBACK_ORDER if l != lang]
    chosen = None
    for cand in order:
        t = entry["text"].get(cand)
        if t and t != "[MISSING]":
            chosen, used = t, cand
            break
        if strict_lang:
            break
    if chosen is None:
        raise EncodingError(f"no text available for entry {entry['id']} in {order}")
    try:
        message = validate_and_render(chosen, entry.get("slots", []), values) \
            if entry.get("slots") else chosen
    except SlotError as e:
        raise EncodingError(str(e)) from None
    return {"entry_id": entry["id"], "code": entry["code"], "language": used,
            "status": entry["status"], "message": message}
