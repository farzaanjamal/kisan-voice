"""
P2 (trial) — consent-checked SMS sender over a MOCK gateway. No SIM, no real delivery.
Demonstrates: consent/active filtering, approved-only safety gate, idempotency (no double
send), per-language decode, segment counting, and a logged summary.

  python p2_sms_trial.py --trial     # allow DRAFT content (mock pipeline test only)
  python p2_sms_trial.py             # LIVE rules: refuses anything not status=approved
"""
import argparse, csv, sys
from pathlib import Path
sys.path.insert(0, ".")
from kisaan_voice import load_dictionary, encode_sms, decode_sms, count_segments

DICTS = {}
def get_dict(region, crop):
    key = (region, crop)
    if key not in DICTS:
        from kisaan_voice import select_dictionary
        DICTS[key] = select_dictionary(region, crop, "dictionaries")
    return DICTS[key]

class MockGateway:
    def __init__(self): self.outbox = []
    def send(self, to, body):
        sid = f"MOCK{len(self.outbox):05d}"; self.outbox.append({"to": to, "sid": sid}); return sid

def run(trial=False):
    gw = MockGateway()
    farmers = list(csv.DictReader(open("pilot/sms_trial/farmers.csv", encoding="utf-8")))
    schedule = list(csv.DictReader(open("pilot/sms_trial/schedule.csv", encoding="utf-8")))
    sent_log, already, stats = [], set(), {
        "sent":0,"blocked_draft":0,"no_consent":0,"inactive":0,"duplicate":0,"by_lang":{}}

    print("="*64)
    print(f"SMS TRIAL  —  mode: {'TRIAL (draft allowed, MOCK only)' if trial else 'LIVE (approved-only)'}")
    print("MOCK gateway: nothing is really sent; numbers are fake test numbers.")
    print("="*64)

    for row in schedule:
        d = get_dict(row["region"], row["crop"])
        if not d: continue
        entry = d.entry(int(row["entry_id"]))
        # approved-only safety gate (the important bit)
        if entry["status"] != "approved" and not trial:
            stats["blocked_draft"] += 1
            print(f"  BLOCKED  {d.code}-{row['entry_id']}  (status={entry['status']}, not approved)")
            continue
        slot_vals = {}
        if entry.get("slots"):
            vals = [v for v in row["slot_values"].split("|") if v != ""]
            slot_vals = {s["name"]: int(vals[i]) for i, s in enumerate(entry["slots"])}
        for f in farmers:
            if f["region"] != row["region"] or f["crop"] != row["crop"]:
                continue
            if f["consent_given"].lower() != "yes": stats["no_consent"] += 1; continue
            if f["active"].lower() != "yes": stats["inactive"] += 1; continue
            key = (f["farmer_id"], d.code, row["entry_id"])
            if key in already: stats["duplicate"] += 1; continue   # idempotency
            already.add(key)
            lang = f["language"]
            out = decode_sms(encode_sms(d, entry["id"], slot_vals), [d], lang)
            body = out["message"] + "\n- Kisan Voice (reply STOP to stop)"
            seg = count_segments(body)
            sid = gw.send(f["phone"], body)
            stats["sent"] += 1
            stats["by_lang"][out["language"]] = stats["by_lang"].get(out["language"], 0) + 1
            sent_log.append({"farmer_id": f["farmer_id"], "code": entry["code"], "lang": out["language"],
                             "chars": len(body), "segments": seg["segments"], "sid": sid, "status": entry["status"]})

    # write log (no phone numbers)
    if sent_log:
        with open("pilot/sms_trial/sent_log.csv","w",newline="",encoding="utf-8") as fp:
            w=csv.DictWriter(fp, fieldnames=list(sent_log[0].keys())); w.writeheader(); w.writerows(sent_log)
    print(f"\n  sent (mock)        : {stats['sent']}")
    print(f"  blocked (draft)    : {stats['blocked_draft']}")
    print(f"  skipped no-consent : {stats['no_consent']}")
    print(f"  skipped inactive   : {stats['inactive']}")
    print(f"  duplicates prevented: {stats['duplicate']}")
    print(f"  by language        : {stats['by_lang']}")
    if sent_log:
        print("\n  sample sent_log (no phone numbers stored):")
        for r in sent_log[:3]:
            print(f"    {r['farmer_id']}  {r['code']}  {r['lang']}  {r['chars']} chars / {r['segments']} SMS  {r['sid']}")
    print("="*64)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--trial", action="store_true"); a = ap.parse_args()
    run(trial=a.trial)
