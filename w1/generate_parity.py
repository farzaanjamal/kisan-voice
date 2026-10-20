"""Emit expected encode/decode/segment outputs for every entry, for the JS parity test."""
import json, glob, sys
sys.path.insert(0, "..")
from kisaan_voice import load_dictionary, encode_sms, encode_binary, decode_sms, count_segments

rows = []
for path in sorted(glob.glob("../dictionaries/*_v2.json")):
    d = load_dictionary(path)
    for e in d.entries:
        sv = {s["name"]: s.get("min", 1) for s in e.get("slots", [])}
        sms = encode_sms(d, e["id"], sv)
        binary = encode_binary(d, e["id"], sv or None, msg_id=1, ttl=4, hop=0)
        msg = decode_sms(sms, [d], "ur")["message"]
        seg = count_segments(msg)
        rows.append({
            "code": d.code, "id": e["id"], "sms": sms, "binary_hex": binary.hex(),
            "msg_ur": msg, "enc": seg["encoding"], "length": seg["length"],
            "segments": seg["segments"], "sms_segments": count_segments(sms)["segments"],
        })
json.dump(rows, open("expected_parity.json", "w", encoding="utf-8"), ensure_ascii=False)
print("wrote expected_parity.json:", len(rows), "entries")
