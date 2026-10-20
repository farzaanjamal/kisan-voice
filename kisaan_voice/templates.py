"""Typed template slots. No untranslated free text can ever enter a message."""
from __future__ import annotations
import re
from typing import Any, Dict, List


class SlotError(ValueError):
    pass


def validate_and_render(text: str, slots: List[dict], values: Dict[str, Any]) -> str:
    """Fill {name} placeholders after checking each value against its slot spec."""
    spec = {s["name"]: s for s in slots}
    needed = set(re.findall(r"\{(\w+)\}", text))
    if needed != set(spec.keys()):
        raise SlotError(f"template placeholders {needed} != slot defs {set(spec.keys())}")
    out = text
    for name, s in spec.items():
        if name not in values:
            raise SlotError(f"missing slot value: {name}")
        v = values[name]
        if s["type"] == "int":
            iv = int(v)
            lo, hi = s.get("min"), s.get("max")
            if (lo is not None and iv < lo) or (hi is not None and iv > hi):
                raise SlotError(f"slot '{name}'={iv} out of range [{lo},{hi}]")
            rendered = str(iv)
        elif s["type"] == "enum":
            table = s.get("values", {})
            if str(v) not in table:
                raise SlotError(f"slot '{name}'='{v}' not in enum {list(table)}")
            rendered = str(table[str(v)])   # already-translated value
        else:
            raise SlotError(f"unknown slot type: {s['type']}")
        out = out.replace("{" + name + "}", rendered)
    return out
