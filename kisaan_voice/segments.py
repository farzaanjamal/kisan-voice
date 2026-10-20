"""SMS encoding + segment counting for GSM-7 and UCS-2 (UCS-2 is what Urdu uses)."""
from __future__ import annotations

# GSM 03.38 basic + basic-extension character sets
_GSM_BASIC = (
    "@\u00a3$\u00a5\u00e8\u00e9\u00f9\u00ec\u00f2\u00c7\n\u00d8\u00f8\r\u00c5\u00e5"
    "\u0394_\u03a6\u0393\u039b\u03a9\u03a0\u03a8\u03a3\u0398\u039e\x1b\u00c6\u00e6\u00df\u00c9"
    " !\"#\u00a4%&'()*+,-./0123456789:;<=>?"
    "\u00a1ABCDEFGHIJKLMNOPQRSTUVWXYZ\u00c4\u00d6\u00d1\u00dc\u00a7"
    "\u00bfabcdefghijklmnopqrstuvwxyz\u00e4\u00f6\u00f1\u00fc\u00e0"
)
_GSM_EXT = "\f^{}\\[~]|\u20ac"
_GSM_SET = set(_GSM_BASIC) | set(_GSM_EXT)


def is_gsm7(text: str) -> bool:
    return all(ch in _GSM_SET for ch in text)


def _gsm7_len(text: str) -> int:
    # extension chars take 2 septets
    return sum(2 if ch in _GSM_EXT else 1 for ch in text)


def count_segments(text: str) -> dict:
    """Return encoding, logical length, and number of SMS segments."""
    if is_gsm7(text):
        enc, length = "GSM-7", _gsm7_len(text)
        single, multi = 160, 153
    else:
        enc, length = "UCS-2", len(text)   # Urdu -> UCS-2, 1 unit per code unit
        single, multi = 70, 67
    if length <= single:
        segments = 1
    else:
        segments = -(-length // multi)     # ceil
    return {"encoding": enc, "length": length, "segments": segments}
