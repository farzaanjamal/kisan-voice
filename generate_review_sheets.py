"""
D3 (sheets) — generate the review CSVs a busy expert / native speaker can fill in,
plus a coverage note. English glosses live here (reviewer metadata, not dictionary
content). Keep in sync by regenerating whenever the dictionary changes.
"""
import csv, json
from collections import Counter
from pathlib import Path

D = json.load(open("dictionaries/punjab_cotton_v2.json", encoding="utf-8"))
OUT = Path("pilot/review"); OUT.mkdir(parents=True, exist_ok=True)

GLOSS = {
 1:"CLCuV prevention: sow early, balanced fertiliser, clear weeds",
 2:"Remove & destroy leaf-curl-infected plants",
 3:"Whitefly spreads leaf curl virus — monitor & control it",
 4:"Bacterial blight — remove affected leaves, consult officer",
 5:"Boll rot in high humidity — ventilate, pick on time",
 6:"Choose a leaf-curl-tolerant approved variety",
 7:"Sow cotton April–mid May; avoid very late sowing",
 8:"Early sowing lowers leaf curl virus risk",
 9:"Use certified, treated seed; ask officer for seed rate",
 10:"Fertilise per soil test; consult officer",
 11:"Don't over-apply nitrogen — it worsens whitefly/virus",
 12:"Apply balanced NPK for a strong crop",
 13:"Avoid water stress at flowering",
 14:"Water regularly during boll formation",
 15:"Arrange drainage for heavy rain",
 16:"Clear host weeds in & around field (whitefly/virus refuge)",
 17:"Scout weekly; spray only based on pest counts",
 18:"Whitefly over ~4–5/leaf → consult officer before acting",
 19:"Jassid leaf-margin yellowing/curling → scout, consult officer",
 20:"Pink bollworm/soft bolls → remove & destroy infested bolls, contact officer",
 21:"~5% damaged fruiting bodies → consult officer",
 22:"Use pheromone traps to monitor pink bollworm",
 23:"Thrips curl young leaves; usually no spray — keep scouting",
 24:"Mealybug → remove affected branches, keep area clean",
 25:"Avoid unnecessary sprays — causes resistance",
 26:"Protect helpful insects (ladybirds) — they eat pests",
 27:"Heavy rain in {days} days → stop irrigation & fertiliser",
 28:"Rain expected → delay picking until dry, cover picked cotton",
 29:"Whitefly surges after heatwaves → scout more",
 30:"High humidity risks boll rot → pick on time",
 31:"Pick after dew clears, in dry weather",
 32:"Pick regularly so cotton doesn't fall & spoil",
 33:"Keep lint free of soil/leaves/threads for quality",
 34:"Keep stained/wet cotton separate",
 35:"Store picked cotton dry & clean; protect from moisture",
 36:"Wear gloves, mask, covered clothes when spraying",
 37:"Don't spray against the wind; keep others/animals away",
 38:"Wash hands & face, change clothes after spraying",
 39:"Store pesticide in its labelled container, away from food/children",
 40:"Poisoning signs (nausea, dizziness) → get medical help now, take the label",
 41:"Don't pick before the label's pre-harvest interval",
}

# ---- expert review sheet ----
with open(OUT/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id","code","category","crop_stage","urgency","english_meaning",
                "urdu_message","source_link","confidence",
                "correct? (yes/no/partly)","suggested_change","comments"])
    for e in D["entries"]:
        w.writerow([e["id"],e["code"],e["category"],e["crop_stage"],e["urgency"],
                    GLOSS.get(e["id"],""), e["text"]["ur"],
                    e["sources"][0]["link"], e["confidence"], "","",""])

# ---- native-speaker sheet ----
with open(OUT/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["id","english_meaning","urdu_text","roman_ur_text",
                "understandable? (yes/no)","natural? (yes/no)","corrected_text"])
    for e in D["entries"]:
        w.writerow([e["id"],GLOSS.get(e["id"],""),e["text"]["ur"],
                    e["text"]["roman_ur"],"","",""])

# ---- covering note ----
(OUT/"covering_note.md").write_text(
"""# Covering note to send with each review sheet

**To the agronomist (English):**
Thank you for helping. Attached are ~41 short cotton advisories for Punjab, each a
draft. For each row, please mark correct / partly / no, and add a change if needed.
I have deliberately written NO pesticide doses — where a pest crosses a threshold the
message says "consult your extension officer and follow the label". If a dose or
timing should be stated from an official source, please note the source. Nothing will
be sent to a farmer until you have signed off. ~45 minutes. Thank you.

**To the native speaker (Urdu/Roman — native-check this note too):**
یہ کسانوں کے لیے مختصر زرعی پیغامات ہیں۔ براہِ کرم ہر جملے کے بارے میں بتائیں کہ کیا
یہ سمجھ آتا ہے اور قدرتی لگتا ہے؛ اگر ٹھیک نہ ہو تو درست جملہ لکھ دیں۔ شکریہ۔
""", encoding="utf-8")

# ---- coverage note ----
cats = Counter(e["category"] for e in D["entries"])
conf = Counter(e["confidence"] for e in D["entries"])
low = [f"{e['code']} ({GLOSS.get(e['id'],'')})" for e in D["entries"] if e["confidence"]=="low"]
cov = f"""# D2 — Coverage & confidence (punjab_cotton v2, draft)

**{len(D['entries'])} draft entries.** All `status: draft` — none sendable until reviewed.

## By category
{chr(10).join(f"- {k}: {v}" for k,v in sorted(cats.items()))}

## By confidence
{chr(10).join(f"- {k}: {v}" for k,v in conf.items())}

## Honest gaps (NOT padded to 60)
- **fertilizer / irrigation / sowing are thin** — R1 gave no sourced doses or
  schedules, so I did not invent entries to hit a target. These grow once the
  official PAD/AARI leaflet is pulled.
- **CLCuV is now first** and spans prevention, roguing, and vector control.
- Only two numbers appear in any message (whitefly ~4–5/leaf, bollworm 5% damage),
  both from sourced studies; no pesticide doses anywhere.

## Lowest-confidence entries (review first)
{chr(10).join(f"- {x}" for x in low)}
"""
(OUT/"../../D2_COVERAGE.md").resolve()  # noqa
Path("D2_COVERAGE.md").write_text(cov, encoding="utf-8")

print("wrote:", *[str(p) for p in OUT.glob("*")], "and D2_COVERAGE.md", sep="\n  ")
