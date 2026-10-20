import pytest
from kisaan_voice import load_dictionary, encode_sms, decode_sms, encode_binary, decode_binary, EncodingError

D = load_dictionary("dictionaries/punjab_cotton_v2.json")

def test_roundtrip_every_entry_every_language():
    for e in D.entries:
        vals = {s["name"]: s.get("min", 1) for s in e.get("slots", [])}
        for lang in D.languages:
            sms = encode_sms(D, e["id"], vals)
            out = decode_sms(sms, [D], lang)
            assert out["entry_id"] == e["id"]
            assert out["message"]                      # non-empty
            # binary round-trip too
            b = encode_binary(D, e["id"], vals, msg_id=7)
            out2 = decode_binary(b, [D], lang)
            assert out2["message"] == out["message"]

def test_sms_code_is_gsm7_and_tiny():
    from kisaan_voice.segments import is_gsm7, count_segments
    sms = encode_sms(D, 1)
    assert is_gsm7(sms) and count_segments(sms)["segments"] == 1

def test_template_slot_fills_and_validates():
    tpl = next(e for e in D.entries if e.get("slots"))    # find the templated entry
    slot = tpl["slots"][0]
    good = encode_sms(D, tpl["id"], {slot["name"]: slot["min"]})
    out = decode_sms(good, [D], "ur")
    assert str(slot["min"]) in out["message"]
    with pytest.raises(EncodingError):                    # above max -> rejected
        decode_sms(f"KV2 PCT {tpl['id']} {slot['max'] + 1}", [D], "ur")

def test_unknown_code_errors_not_guesses():
    with pytest.raises(EncodingError):
        decode_sms("KV2 PCT 999", [D], "ur")
    with pytest.raises(EncodingError):
        decode_sms("hello world", [D], "ur")

def test_version_mismatch_refuses():
    b = bytearray(encode_binary(D, 1, None, msg_id=1))
    b[2] = 99                                            # corrupt dictionary_version
    with pytest.raises(EncodingError):
        decode_binary(bytes(b), [D], "ur")

def test_fallback_to_urdu_when_language_absent():
    out = decode_sms(encode_sms(D, 1), [D], "sd")        # sindhi absent -> falls back
    assert out["language"] in ("ur", "roman_ur")
