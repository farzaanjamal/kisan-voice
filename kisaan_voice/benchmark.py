"""
Honest compression benchmark.

Compares, per advisory: the full Urdu message vs general-purpose compressors
(zlib, brotli) vs our dictionary approach (SMS form / binary form).

The honest result (measured, not assumed): on these ~50-90 character Urdu
messages, zlib manages only a modest cut (~25-30%) and brotli does a bit better
(~40%) -- neither comes remotely close to our ~9-byte code. Our win does NOT
come from clever compression; it comes from the receiver already holding the
dictionary, so only a tiny reference has to travel. On *much* shorter strings
general compressors would do even worse (header overhead), but we report what
actually happens on this corpus rather than the worst case.
"""
from __future__ import annotations
import csv, zlib
from pathlib import Path
from statistics import median

from .dictionary import load_dictionary
from .encoding import encode_sms, encode_binary, decode_sms
from .segments import count_segments

try:
    import brotli
    _HAVE_BROTLI = True
except ImportError:
    _HAVE_BROTLI = False


def run(dict_path: str, out_dir: str = "benchmark_out") -> dict:
    d = load_dictionary(dict_path)
    Path(out_dir).mkdir(exist_ok=True)
    rows = []
    for e in d.entries:
        vals = {s["name"]: s.get("min", 1) for s in e.get("slots", [])}
        full = decode_sms(encode_sms(d, e["id"], vals), [d], "ur")["message"]
        u8 = full.encode("utf-8")
        ucs2_bytes = len(full) * 2
        seg_full = count_segments(full)
        sms = encode_sms(d, e["id"], vals)
        binary = encode_binary(d, e["id"], vals or None, msg_id=1)
        rows.append({
            "code": e["code"],
            "full_chars": len(full),
            "full_utf8_bytes": len(u8),
            "full_ucs2_bytes": ucs2_bytes,
            "full_sms_segments": seg_full["segments"],
            "zlib_bytes": len(zlib.compress(u8, 9)),
            "brotli_bytes": len(brotli.compress(u8)) if _HAVE_BROTLI else "",
            "our_sms_chars": len(sms),
            "our_sms_segments": count_segments(sms)["segments"],
            "our_binary_bytes": len(binary),
        })

    csv_path = Path(out_dir) / "benchmark.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    # summary
    saved_vs_ucs2 = [1 - r["our_binary_bytes"] / r["full_ucs2_bytes"] for r in rows]
    multi_to_single = sum(1 for r in rows if r["full_sms_segments"] >= 2 and r["our_sms_segments"] == 1)
    zlib_expanded = sum(1 for r in rows if r["zlib_bytes"] >= r["full_utf8_bytes"])
    summary = {
        "entries": len(rows),
        "median_binary_size_reduction_vs_ucs2_pct": round(100 * median(saved_vs_ucs2), 1),
        "messages_2plus_segments_now_1_code_segment": f"{multi_to_single}/{len(rows)}",
        "zlib_made_it_BIGGER_count": f"{zlib_expanded}/{len(rows)}",
        "dictionary_size_kb": round(Path(dict_path).stat().st_size / 1024, 1),
        "key_limitation": "receiver must hold the dictionary; a code is meaningless without it",
    }

    _chart(rows, Path(out_dir) / "benchmark.png")
    return {"csv": str(csv_path), "chart": str(Path(out_dir) / "benchmark.png"),
            "summary": summary, "rows": rows}


def _chart(rows, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels = [r["code"].replace("PCT-", "") for r in rows]
    x = range(len(rows))
    full = [r["full_utf8_bytes"] for r in rows]
    zl = [r["zlib_bytes"] for r in rows]
    ours = [r["our_binary_bytes"] for r in rows]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    w = 0.27
    ax.bar([i - w for i in x], full, w, label="full Urdu (UTF-8)", color="#9aa0aa")
    ax.bar(list(x), zl, w, label="zlib-compressed", color="#c99a2e")
    ax.bar([i + w for i in x], ours, w, label="our binary code", color="#1c6a3c")
    ax.set_ylabel("bytes on the wire"); ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_title("Bytes to transmit one advisory: full text vs zlib vs dictionary code")
    ax.legend(fontsize=9); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


if __name__ == "__main__":
    import json, sys
    res = run(sys.argv[1] if len(sys.argv) > 1 else "dictionaries/punjab_cotton_v2.json")
    print(json.dumps(res["summary"], indent=2))
    print("wrote", res["csv"], "and", res["chart"])
