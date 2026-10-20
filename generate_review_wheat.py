import csv, json
from collections import Counter
from pathlib import Path
D = json.load(open("dictionaries/kpk_wheat_v2.json", encoding="utf-8"))
OUT = Path("pilot/review_wheat"); OUT.mkdir(parents=True, exist_ok=True)
GLOSS = {
 1:"Choose a yellow-rust-resistant approved variety",
 2:"Don't rely on one susceptible variety; pick a current resistant one",
 3:"Level the field well and add farmyard manure before sowing",
 4:"Sow on time (25 Oct-15 Nov); late sowing cuts yield",
 5:"Each day's delay after 20 Nov lowers yield - sow early",
 6:"Drill-sow rather than broadcast (even stand, less seed)",
 7:"Use certified-variety seed",
 8:"Treat seed against smut and termite",
 9:"Apply DAP (phosphorus) at sowing for strong roots/tillering",
 10:"Apply nitrogen in two splits, per soil test",
 11:"Don't over-apply nitrogen (worsens yellow rust)",
 12:"First irrigation ~20-25 days after sowing (crown-root)",
 13:"No water shortage at tillering, booting, grain-filling",
 14:"Arrange drainage for heavy rain",
 15:"Control weeds (wild oat etc.) early - they steal nutrients",
 16:"Use weedicide on time, per label; consult officer",
 17:"Yellow striped leaf spots (yellow rust) -> consult officer urgently",
 18:"Yellow rust rises in cold/fog -> scout before booting",
 19:"Prevent yellow rust: avoid excess N, plant resistant variety",
 20:"Brown/orange spots (brown rust) -> scout, consult officer",
 21:"Prevent loose smut with treated, certified seed",
 22:"Scout weekly; spray only on pest counts",
 23:"Aphid colonies on leaves/ears -> scout, protect natural enemies",
 24:"Termite wilting -> treat seed/soil, remove debris",
 25:"Army worm chewing leaves -> scout at night, consult officer",
 26:"Protect ladybirds - they eat aphids",
 27:"Heavy rain in {days} days -> stop irrigation and fertiliser",
 28:"Rain/hail risk -> harvest ripe crop promptly, cover & dry",
 29:"Fog/humidity spreads yellow rust fast -> scout more",
 30:"Harvest when grain is hard and straw yellow",
 31:"Harvest promptly at ripeness to avoid shattering loss",
 32:"Keep threshing floor clean for clean, unmixed grain",
 33:"Dry grain well; store clean, closed, safe from storage pests",
 34:"Wear gloves, mask, covered clothes when spraying",
 35:"Don't spray against the wind; keep others/animals away",
 36:"Wash hands & face, change clothes after spraying",
 37:"Store pesticide in its labelled container, away from food/children",
 38:"Poisoning signs (nausea, dizziness) -> get medical help, take the label",
 39:"Don't harvest before the label's pre-harvest interval",
}
with open(OUT/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","code","category","crop_stage","urgency","english_meaning",
        "urdu_message","source_link","confidence","correct? (yes/no/partly)","suggested_change","comments"])
    for e in D["entries"]:
        w.writerow([e["id"],e["code"],e["category"],e["crop_stage"],e["urgency"],GLOSS.get(e["id"],""),
                    e["text"]["ur"],e["sources"][0]["link"],e["confidence"],"","",""])
with open(OUT/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","english_meaning","urdu_text","roman_ur_text",
        "pashto_text (please add)","understandable? (yes/no)","natural? (yes/no)","corrected_text"])
    for e in D["entries"]:
        w.writerow([e["id"],GLOSS.get(e["id"],""),e["text"]["ur"],e["text"]["roman_ur"],"","","",""])
cats=Counter(e["category"] for e in D["entries"]); conf=Counter(e["confidence"] for e in D["entries"])
low=[f"{e['code']} ({GLOSS.get(e['id'],'')})" for e in D["entries"] if e["confidence"]=="low"]
Path("D2_COVERAGE_wheat.md").write_text(f"""# D2 — Coverage & confidence (kpk_wheat v2, draft)

**{len(D['entries'])} draft entries.** All `status: draft`; none sendable until reviewed.
Timely sowing + rust-resistant variety are foregrounded (the live Oct-Nov decisions),
and this dictionary is the **best-sourced** of the three (KP govt leaflet + ARI Tarnab).

## By category
{chr(10).join(f"- {k}: {v}" for k,v in sorted(cats.items()))}

## By confidence
{chr(10).join(f"- {k}: {v}" for k,v in conf.items())}

## Honest notes
- **Pashto is NOT included** - draft ships Urdu + Roman Urdu only; a native Pashto
  speaker must add Pashto (high regional usage in KP). The native sheet has a blank
  Pashto column.
- No fungicide/pesticide doses. Variety resistance is not durable - the "resistant
  variety" messages must be checked against the CURRENT ARI Tarnab recommended list.

## Lowest-confidence entries (review first)
{chr(10).join(f"- {x}" for x in low)}
""", encoding="utf-8")
print("wheat review sheets + coverage written; entries:", len(D["entries"]))
