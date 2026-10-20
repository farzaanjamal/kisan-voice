from kisaan_voice.segments import count_segments, is_gsm7

def test_gsm7_detection():
    assert is_gsm7("Hello 123")
    assert not is_gsm7("سفید مکھی")          # Urdu -> not GSM-7

def test_gsm7_segment_boundaries():
    assert count_segments("a"*160)["segments"] == 1
    assert count_segments("a"*161)["segments"] == 2      # 153-char multipart
    r = count_segments("a"*160); assert r["encoding"] == "GSM-7"

def test_ucs2_urdu_segments():
    # Urdu uses UCS-2: 70 per single, 67 per multipart segment
    r = count_segments("ا"*70); assert r["encoding"] == "UCS-2" and r["segments"] == 1
    assert count_segments("ا"*71)["segments"] == 2
    assert count_segments("ا"*134)["segments"] == 2      # 2*67
    assert count_segments("ا"*135)["segments"] == 3
