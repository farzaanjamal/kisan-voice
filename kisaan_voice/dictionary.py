"""Load + validate v2 dictionaries. Validation errors always name the entry id."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional

import jsonschema

_SCHEMA_PATH = Path(__file__).with_name("dictionary.schema.json")


class DictionaryError(Exception):
    pass


class Dictionary:
    def __init__(self, data: dict):
        self.data = data
        self.code = data["code"]
        self.id = data["dictionary_id"]
        self.version = data["dictionary_version"]
        self.region = data["region"]
        self.crop = data["crop"]
        self.languages = data["languages"]
        self._by_id: Dict[int, dict] = {e["id"]: e for e in data["entries"]}
        self._by_code: Dict[str, dict] = {e["code"]: e for e in data["entries"]}

    def entry(self, entry_id: int) -> dict:
        if entry_id not in self._by_id:
            raise DictionaryError(f"unknown entry id {entry_id} in dictionary {self.code}")
        return self._by_id[entry_id]

    @property
    def entries(self) -> List[dict]:
        return self.data["entries"]


def _schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate(data: dict) -> None:
    """Schema check + the semantic checks the schema can't express."""
    try:
        jsonschema.validate(data, _schema())
    except jsonschema.ValidationError as e:
        where = "/".join(str(p) for p in e.path) or "(root)"
        raise DictionaryError(f"schema error at {where}: {e.message}") from None

    ids, codes = set(), set()
    langs = set(data["languages"])
    for e in data["entries"]:
        eid = e["id"]
        if eid in ids:
            raise DictionaryError(f"duplicate entry id {eid}")
        ids.add(eid)
        if e["code"] in codes:
            raise DictionaryError(f"duplicate entry code {e['code']} (id {eid})")
        codes.add(e["code"])
        if not e.get("sources"):
            raise DictionaryError(f"entry id {eid} has no sources")
        # every declared language present, or explicitly marked missing
        for lang in langs:
            if lang not in e["text"] and e["text"].get(lang) != "[MISSING]":
                if lang not in e["text"]:
                    raise DictionaryError(
                        f"entry id {eid} missing text for language '{lang}' "
                        f"(use '[MISSING]' to mark intentionally absent)")


def load_dictionary(path: str) -> Dictionary:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(data)
    return Dictionary(data)


def select_dictionary(region: str, crop: str, directory: str) -> Optional[Dictionary]:
    for p in sorted(Path(directory).glob("*_v*.json")):
        try:
            d = load_dictionary(str(p))
        except DictionaryError:
            continue
        if d.region.lower() == region.lower() and d.crop.lower() == crop.lower():
            return d
    return None
