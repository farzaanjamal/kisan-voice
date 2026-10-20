import json, copy, pytest
from kisaan_voice import validate, DictionaryError

BASE = json.load(open("dictionaries/punjab_cotton_v2.json"))

def test_good_dictionary_validates():
    validate(copy.deepcopy(BASE))

def test_duplicate_id_rejected():
    d = copy.deepcopy(BASE); d["entries"][1]["id"] = d["entries"][0]["id"]
    with pytest.raises(DictionaryError): validate(d)

def test_missing_source_rejected():
    d = copy.deepcopy(BASE); d["entries"][0]["sources"] = []
    with pytest.raises(DictionaryError): validate(d)

def test_missing_language_text_rejected():
    d = copy.deepcopy(BASE); d["entries"][0]["text"].pop("roman_ur")
    with pytest.raises(DictionaryError): validate(d)
