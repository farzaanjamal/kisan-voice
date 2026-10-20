from kisaan_voice import load_dictionary, encode_binary

D = load_dictionary("dictionaries/punjab_cotton_v2.json")
USABLE_ADV_BYTES = 27     # 31-byte legacy adv - 2 (flags AD) - 2 (mfr header/company id) approx

def test_every_packet_fits_in_ble_advertisement():
    worst = 0
    for e in D.entries:
        vals = {s["name"]: s.get("max", 1) for s in e.get("slots", [])}
        b = encode_binary(D, e["id"], vals or None, msg_id=65535, ttl=7, hop=7)
        worst = max(worst, len(b))
    assert worst <= USABLE_ADV_BYTES, f"packet {worst}B exceeds {USABLE_ADV_BYTES}B budget"
