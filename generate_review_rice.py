import csv, json
from collections import Counter
from pathlib import Path
D = json.load(open("dictionaries/sindh_rice_v2.json", encoding="utf-8"))
OUT = Path("pilot/review_rice"); OUT.mkdir(parents=True, exist_ok=True)
GLOSS = {
 1:"AWD: don't keep water standing; dry intermittently (cuts BPH)",
 2:"Keep adequate water at flowering/grain-fill",
 3:"Drain field before harvest for easier cutting",
 4:"Fertilise per soil test; consult officer",
 5:"Apply nitrogen in 2-3 splits (transplant, ~35 days, before flowering)",
 6:"Don't over-apply nitrogen (worsens BPH, blast, blight)",
 7:"Choose a blast/blight-tolerant approved variety",
 8:"Transplant nursery at 25-35 days; old nursery cuts yield",
 9:"Plant on time; early planting resists stem borer",
 10:"Plant two seedlings per hill for a good stand",
 11:"Use certified, treated seed",
 12:"Keep nursery and field weed-free",
 13:"Scout weekly; spray only on pest counts",
 14:"Dead central shoot = stem borer; consult officer",
 15:"Bury stubble/straw after harvest (kills stem-borer larvae)",
 16:"Hopperburn (yellow-brown patches) = BPH; drain water, consult officer",
 17:"BPH over ~10-15/hill -> consult officer",
 18:"Folded, silk-tied leaves = leaf folder; scout, protect natural enemies",
 19:"Protect spiders/ladybirds - they eat hoppers",
 20:"Avoid unnecessary sprays (can worsen BPH)",
 21:"White leaf streaks or shoot galls -> scout, consult officer",
 22:"Pointed blast lesions -> cut nitrogen, consult officer",
 23:"~3-5 blast lesions/leaf -> consult officer",
 24:"Bacterial blight (yellow drying leaf edges) -> reduce N, remove debris",
 25:"Grey sheath lesions -> avoid dense planting, improve airflow",
 26:"Tungro (stunted orange-yellow) -> remove plants, control leafhopper",
 27:"Bury straw/stubble after harvest to cut disease",
 28:"Heavy rain in {days} days -> drain field, stop fertiliser",
 29:"Rain expected -> harvest ripe crop promptly, cover & dry cut crop",
 30:"Heat + standing water boosts BPH -> dry intermittently, scout more",
 31:"Harvest when 85-95% panicles are straw-coloured",
 32:"Let cut crop dry 2-3 days before threshing",
 33:"Harvest in the morning; keep threshing floor clean",
 34:"Don't combine-harvest seed crop (avoids variety mixing)",
 35:"Dry grain well; store clean and dry",
 36:"Wear gloves, mask, covered clothes when spraying",
 37:"Don't spray against the wind; keep others/animals away",
 38:"Wash hands & face, change clothes after spraying",
 39:"Store pesticide in its labelled container, away from food/children",
 40:"Poisoning signs (nausea, dizziness) -> get medical help, take the label",
 41:"Don't harvest before the label's pre-harvest interval",
}
with open(OUT/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","code","category","crop_stage","urgency","english_meaning",
        "urdu_message","source_link","confidence","correct? (yes/no/partly)","suggested_change","comments"])
    for e in D["entries"]:
        w.writerow([e["id"],e["code"],e["category"],e["crop_stage"],e["urgency"],GLOSS.get(e["id"],""),
                    e["text"]["ur"],e["sources"][0]["link"],e["confidence"],"","",""])
with open(OUT/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","english_meaning","urdu_text","roman_ur_text",
        "sindhi_text (please add)","understandable? (yes/no)","natural? (yes/no)","corrected_text"])
    for e in D["entries"]:
        w.writerow([e["id"],GLOSS.get(e["id"],""),e["text"]["ur"],e["text"]["roman_ur"],"","","",""])
cats=Counter(e["category"] for e in D["entries"]); conf=Counter(e["confidence"] for e in D["entries"])
low=[f"{e['code']} ({GLOSS.get(e['id'],'')})" for e in D["entries"] if e["confidence"]=="low"]
Path("D2_COVERAGE_rice.md").write_text(f"""# D2 — Coverage & confidence (sindh_rice v2, draft)

**{len(D['entries'])} draft entries.** All `status: draft`; none sendable until reviewed.
Water + nitrogen management is foregrounded (the strongest safe lever for rice).

## By category
{chr(10).join(f"- {k}: {v}" for k,v in sorted(cats.items()))}

## By confidence
{chr(10).join(f"- {k}: {v}" for k,v in conf.items())}

## Honest notes
- **Sindhi is NOT included** — the draft ships Urdu + Roman Urdu only; a native Sindhi
  speaker must add Sindhi (very high regional usage). The native sheet has a blank
  Sindhi column for exactly this.
- Only sourced numbers appear: BPH ~10-15/hill, blast 3-5 lesions/leaf, harvest 85-95%
  straw panicles. No pesticide doses. Not padded to 60.

## Lowest-confidence entries (review first)
{chr(10).join(f"- {x}" for x in low)}
""", encoding="utf-8")
print("rice review sheets + coverage written; entries:", len(D["entries"]))
