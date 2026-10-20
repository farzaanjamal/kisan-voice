"""
Sindh wheat + Sindh cotton v2 — transform the existing wheat/cotton cores, swap in
Sindh-specific entries (sowing windows, varieties, rotation, Sindh risks), emit the
dictionaries + expert/native review sheets + coverage. All draft; no doses; Sindhi
left to a native speaker (Urdu + Roman only).
"""
import csv, json
from collections import Counter
from pathlib import Path

def gloss_map(sheet_path):
    m = {}
    with open(sheet_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            suffix = "-".join(row["code"].split("-")[1:])      # VAR-001
            m[suffix] = row["english_meaning"]
    return m

def build(base_dict, base_sheet, new_code, new_id, region, crop, overrides, adds, cov):
    d = json.loads(Path(base_dict).read_text(encoding="utf-8"))
    glosses = gloss_map(base_sheet)
    old_prefix = d["code"]
    d["dictionary_id"], d["code"], d["region"], d["crop"], d["dictionary_version"] = \
        new_id, new_code, region, crop, 1
    rows = []  # (id, code, cat, stage, urg, ur, rom, conf, src, gloss, slots)
    for e in d["entries"]:
        suffix = "-".join(e["code"].split("-")[1:])
        e["code"] = e["code"].replace(old_prefix, new_code, 1)
        g = glosses.get(suffix, "")
        if suffix in overrides:
            o = overrides[suffix]
            e["text"]["ur"], e["text"]["roman_ur"] = o["ur"], o["rom"]
            e["confidence"], e["sources"] = o["conf"], o["src"]
            g = o["gloss"]
        rows.append((e["id"], e["code"], e["category"], e["crop_stage"], e["urgency"],
                     e["text"]["ur"], e["text"]["roman_ur"], e["confidence"], e["sources"],
                     g, e.get("slots")))
    nid = max(e["id"] for e in d["entries"])
    for a in adds:
        nid += 1
        code = f"{new_code}-{a['suffix']}"
        e = {"id": nid, "code": code, "category": a["cat"], "crop_stage": a["stage"],
             "urgency": a["urg"], "text": {"ur": a["ur"], "roman_ur": a["rom"]},
             "sources": a["src"], "confidence": a["conf"], "status": "draft"}
        if a.get("slots"): e["slots"] = a["slots"]
        d["entries"].append(e)
        rows.append((nid, code, a["cat"], a["stage"], a["urg"], a["ur"], a["rom"],
                     a["conf"], a["src"], a["gloss"], a.get("slots")))

    Path(f"dictionaries/{region}_{crop}_v2.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    out = Path(f"pilot/review_{region}_{crop}"); out.mkdir(parents=True, exist_ok=True)
    with open(out/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["id","code","category","crop_stage","urgency","english_meaning",
            "urdu_message","source_link","confidence","correct? (yes/no/partly)","suggested_change","comments"])
        for r in rows: w.writerow([r[0],r[1],r[2],r[3],r[4],r[9],r[5],r[8][0]["link"],r[7],"","",""])
    with open(out/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["id","english_meaning","urdu_text","roman_ur_text",
            "sindhi_text (please add)","understandable? (yes/no)","natural? (yes/no)","corrected_text"])
        for r in rows: w.writerow([r[0],r[9],r[5],r[6],"","","",""])
    cats=Counter(e["category"] for e in d["entries"]); conf=Counter(e["confidence"] for e in d["entries"])
    Path(f"D2_COVERAGE_{region}_{crop}.md").write_text(
        f"# D2 — Coverage ({region}_{crop} v2, draft)\n\n**{len(d['entries'])} draft entries.** {cov}\n\n"
        f"By category: {dict(sorted(cats.items()))}\nBy confidence: {dict(conf)}\n\n"
        f"All `status: draft`; no doses; Sindhi not included (Urdu + Roman only) — native speaker to add.\n",
        encoding="utf-8")
    print(f"{region}_{crop}: {len(d['entries'])} entries; by conf {dict(conf)}")

# ---------- sources ----------
SW = [{"link":"https://sagpme.com/assets/docs/Sindh-Major-Crop-Sowing-Dates.pdf","note":"Sindh wheat sowing dates — official"}]
SWV = [{"link":"https://www.timesofagriculture.pk/wheat-cultivation-in-pakistan-2025/","note":"Sindh wheat varieties — verify WRI Sakrand"}]
SC = [{"link":"https://www.timesofagriculture.pk/cotton-production-in-pakistan/","note":"Sindh cotton varieties/sowing — verify CRI Sakrand"}]
SCV = [{"link":"https://www.theigc.org/sites/default/files/2015/02/Rana-Et-Al-2013-Working-Paper.pdf","note":"Sindh early sowing escapes CLCuV"}]

# ---------- Sindh WHEAT (base: Punjab wheat core) ----------
build("dictionaries/punjab_wheat_v2.json", "pilot/review_punjab_wheat/expert_review_sheet.csv",
  "SNW", 6, "sindh", "wheat",
  overrides={
    "VAR-001": {"ur":"سندھ کے لیے منظور شدہ گرمی برداشت کرنے والی قسم کاشت کریں (مثلاً ٹی ڈی-1، بینظیر)۔",
                "rom":"Sindh ke liye manzoor-shuda garmi bardasht karnay wali qism kaasht karein (misaal: TD-1, Benazir).",
                "gloss":"Choose a Sindh-approved, heat-tolerant wheat variety (e.g. TD-1, Benazir)","conf":"medium","src":SWV},
    "SOW-002": {"ur":"سندھ میں گندم یکم تا تیس نومبر کاشت کریں؛ جلد کاشت گرمی کے نقصان سے بچاتی ہے۔",
                "rom":"Sindh mein gandum 1 ta 30 November kaasht karein; jald kaasht garmi ke nuqsaan se bachati hai.",
                "gloss":"Sow wheat 1-30 November in Sindh; early sowing avoids terminal-heat loss","conf":"high","src":SW},
    "SOW-003": {"ur":"دیر سے کاشت (دسمبر) میں بیج کی مقدار بڑھا دیں۔",
                "rom":"Der se kaasht (December) mein beej ki miqdaar barha dein.",
                "gloss":"If sowing late (December), increase the seed rate","conf":"medium","src":SW},
  },
  adds=[
    {"suffix":"SOW-007","cat":"sowing","stage":"any","urg":"warning",
     "ur":"سندھ میں گرمی گندم کو نقصان دیتی ہے؛ بروقت کاشت کریں اور دانہ بننے پر پانی یقینی بنائیں۔",
     "rom":"Sindh mein garmi gandum ko nuqsaan deti hai; barwaqt kaasht karein aur dana bannay par pani yaqeeni banayein.",
     "conf":"high","src":SWV,"gloss":"Heat harms Sindh wheat - sow on time and ensure water at grain-fill"},
    {"suffix":"ROT-002","cat":"sowing","stage":"sowing","urg":"advice",
     "ur":"کپاس کے بعد گندم بروقت کاشت کریں (کپاس-گندم ردوبدل)۔",
     "rom":"Kapas ke baad gandum barwaqt kaasht karein (kapas-gandum radd-o-badal).",
     "conf":"medium","src":SW,"gloss":"Sow wheat on time after cotton (cotton-wheat rotation)"},
  ],
  cov="Shares the wheat core with KPK/Punjab wheat; Sindh entries cover the **1-30 Nov window**, **heat-tolerant Sindh varieties (TD-1, Benazir)**, terminal-heat risk, and the cotton-wheat rotation.")

# ---------- Sindh COTTON (base: Punjab cotton core) ----------
build("dictionaries/punjab_cotton_v2.json", "pilot/review/expert_review_sheet.csv",
  "SNC", 7, "sindh", "cotton",
  overrides={
    "VAR-001": {"ur":"سندھ کے لیے منظور شدہ قسم کاشت کریں (مثلاً سی آر آئی ایس-342، سندھ-1)۔",
                "rom":"Sindh ke liye manzoor-shuda qism kaasht karein (misaal: CRIS-342, Sindh-1).",
                "gloss":"Choose a Sindh-approved cotton variety (e.g. CRIS-342, Sindh-1)","conf":"medium","src":SC},
    "SOW-001": {"ur":"سندھ میں کپاس جلد کاشت کریں (مارچ کے آخر تا اپریل)؛ جلد کاشت پتہ مروڑ وائرس سے بچاتی ہے۔",
                "rom":"Sindh mein kapas jald kaasht karein (March ke aakhir ta April); jald kaasht patta maror virus se bachati hai.",
                "gloss":"Sow cotton early in Sindh (late March-April); early sowing escapes leaf curl virus","conf":"high","src":SCV},
  },
  adds=[
    {"suffix":"PST-011","cat":"pest_alert","stage":"any","urg":"advice",
     "ur":"سندھ کی نمی اور گرم راتوں میں سفید مکھی تیزی سے بڑھتی ہے؛ معائنہ بڑھائیں۔",
     "rom":"Sindh ki nami aur garam raaton mein safaid makhi tezi se barhti hai; moaina barhayein.",
     "conf":"medium","src":SC,"gloss":"Sindh's humidity and warm nights boost whitefly - scout more"},
    {"suffix":"ROT-001","cat":"harvest","stage":"harvest","urg":"advice",
     "ur":"چنائی کے بعد گندم بروقت کاشت کریں (کپاس-گندم ردوبدل)۔",
     "rom":"Chunai ke baad gandum barwaqt kaasht karein (kapas-gandum radd-o-badal).",
     "conf":"medium","src":SC,"gloss":"Sow wheat on time after picking (cotton-wheat rotation)"},
  ],
  cov="Shares the cotton core with Punjab cotton; Sindh entries cover **early sowing (late March-April) to escape CLCuV**, **Sindh varieties (CRIS-342, Sindh-1)**, humidity-driven whitefly, and the cotton-wheat rotation.")
