"""CLI:  python -m kisaan_voice demo --region punjab --crop cotton
          python -m kisaan_voice validate --dir dictionaries"""
import argparse, sys
from pathlib import Path
from . import (select_dictionary, load_dictionary, encode_sms, decode_sms,
               encode_binary, decode_binary, count_segments, DictionaryError)


def _demo(args):
    d = select_dictionary(args.region, args.crop, args.dir)
    if not d:
        print(f"no dictionary for {args.region}/{args.crop}", file=sys.stderr); return 1
    print(f"dictionary {d.code} v{d.version}  ({len(d.entries)} entries)\n")
    for e in d.entries:
        if e.get("slots"):           # show a template filled with an example value
            vals = {s["name"]: (s.get("min", 1)) for s in e["slots"]}
            sms = encode_sms(d, e["id"], vals)
            dec = decode_sms(sms, [d], "ur")
            binary = encode_binary(d, e["id"], vals, msg_id=1)
        else:
            sms = encode_sms(d, e["id"])
            dec = decode_sms(sms, [d], "ur")
            binary = encode_binary(d, e["id"], None, msg_id=1)
        full = dec["message"]
        seg = count_segments(full)
        print(f"[{e['code']}] status={e['status']}")
        print(f"  SMS code : {sms!r}  ({len(sms)} chars, {count_segments(sms)['segments']} seg)")
        print(f"  binary   : {binary.hex()}  ({len(binary)} bytes)")
        print(f"  full {seg['encoding']}: {full}")
        print(f"             -> {seg['length']} units, {seg['segments']} SMS segment(s)\n")
    return 0


def _validate(args):
    rc = 0
    for p in sorted(Path(args.dir).glob("*_v*.json")):
        try:
            d = load_dictionary(str(p))
            print(f"OK   {p.name}  ({len(d.entries)} entries)")
        except DictionaryError as e:
            print(f"FAIL {p.name}: {e}"); rc = 1
    return rc


def main():
    ap = argparse.ArgumentParser(prog="kisaan_voice")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pd = sub.add_parser("demo"); pd.add_argument("--region", required=True)
    pd.add_argument("--crop", required=True); pd.add_argument("--dir", default="dictionaries")
    pd.set_defaults(fn=_demo)
    pv = sub.add_parser("validate"); pv.add_argument("--dir", default="dictionaries")
    pv.set_defaults(fn=_validate)
    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
