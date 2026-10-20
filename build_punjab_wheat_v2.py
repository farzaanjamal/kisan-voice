"""
Punjab wheat v2 — shares the wheat core with KPK wheat, with Punjab-specific
entries (sowing window 1-20 Nov irrigated, seed rate, varieties, rice-wheat
rotation). All draft; no fungicide doses; Pashto not used (Urdu + Roman only).
Emits the dictionary + expert/native review sheets + coverage note.
"""
import csv, json
from collections import Counter
from pathlib import Path

CODE, DID = "PJW", 4
S = {
 "pw":   [{"link": "https://pakera.pk/wheat-sowing-punjab-2026-seed-subsidy/", "note": "Punjab wheat sowing window/varieties 2026 — verify agripunjab.gov.pk"}],
 "parc": [{"link": "http://www.parc.gov.pk/index.php/en/faq-s/60-faqs/270-faqs-wheat", "note": "PARC wheat FAQ"}],
 "rust": [{"link": "https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2024.1494566/full", "note": "stripe-rust resistance in recent Pakistani cultivars"}],
 "none": [{"link": "[NEEDS SOURCE]", "note": "confirm with Punjab Agriculture Dept / AARI Faisalabad"}],
}
rows = []  # (id, code, cat, stage, urg, ur, rom, conf, src, gloss, slots)

def E(i, code, cat, stage, urg, ur, rom, conf, src, gloss, slots=None):
    rows.append((i, code, cat, stage, urg, ur, rom, conf, src, gloss, slots))

# ---- VARIETY ----
E(1,"PJW-VAR-001","variety","sowing","advice",
  "پنجاب کے لیے زنگ (کنگی) برداشت کرنے والی منظور شدہ قسم کاشت کریں (مثلاً اکبر-2019، دلکش-2020)۔",
  "Punjab ke liye zang (kangi) bardasht karnay wali manzoor-shuda qism kaasht karein (misaal: Akbar-2019, Dilkash-2020).",
  "medium", S["pw"], "Choose a Punjab rust-resistant approved variety (e.g. Akbar-2019, Dilkash-2020)")
E(2,"PJW-VAR-002","variety","sowing","advice",
  "صرف ایک حساس قسم پر انحصار نہ کریں؛ تازہ منظور شدہ مزاحم قسم چنیں۔",
  "Sirf aik hassaas qism par inhisaar na karein; taaza manzoor-shuda muzahim qism chunein.",
  "medium", S["rust"], "Don't rely on one susceptible variety; pick a current resistant one")
# ---- SOWING / LAND PREP (Punjab specifics) ----
E(3,"PJW-SOW-001","sowing","sowing","advice",
  "کاشت سے پہلے کھیت اچھی طرح ہموار کریں اور گلی سڑی گوبر کی کھاد ڈالیں۔",
  "Kaasht se pehlay khet achhi tarah hamwaar karein aur gali sari gobar ki khaad daalein.",
  "high", S["parc"], "Level the field well and add well-rotted farmyard manure before sowing")
E(4,"PJW-SOW-002","sowing","sowing","warning",
  "آبپاش زمین پر گندم یکم تا بیس نومبر کاشت کریں؛ یہی بہترین وقت ہے۔",
  "Aabpaash zameen par gandum 1 ta 20 November kaasht karein; yehi behtareen waqt hai.",
  "high", S["pw"], "Sow wheat 1-20 November on irrigated land (best window)")
E(5,"PJW-SOW-003","sowing","sowing","advice",
  "بارانی زمین پر گندم پندرہ اکتوبر تا پندرہ نومبر کاشت کریں۔",
  "Baarani zameen par gandum 15 October ta 15 November kaasht karein.",
  "high", S["pw"], "Sow wheat 15 Oct-15 Nov on rainfed (barani) land")
E(6,"PJW-SOW-004","sowing","sowing","warning",
  "بیس نومبر کے بعد ہر دن کی تاخیر پیداوار گھٹاتی ہے؛ جلد کاشت کریں۔",
  "20 November ke baad har din ki taakheer paidawar ghataati hai; jald kaasht karein.",
  "high", S["pw"], "Each day's delay after 20 Nov lowers yield - sow early")
E(7,"PJW-SOW-005","sowing","sowing","advice",
  "چھٹے کے بجائے ڈرل سے کاشت کریں؛ فصل یکساں اور بیج کم لگتا ہے۔",
  "Chhittay ke bajaye drill se kaasht karein; fasal yaksaan aur beej kam lagta hai.",
  "high", S["pw"], "Drill-sow rather than broadcast (even stand, less seed)")
E(8,"PJW-SOW-006","seed","sowing","advice",
  "آبپاش بروقت کاشت کے لیے تقریباً چالیس کلو بیج فی ایکڑ ڈالیں؛ دیر سے کاشت پر زیادہ۔",
  "Aabpaash barwaqt kaasht ke liye taqreeban 40 kilo beej fi acre daalein; der se kaasht par zyada.",
  "medium", S["pw"], "~40 kg seed/acre for timely irrigated sowing; more if late")
E(9,"PJW-ROT-001","sowing","sowing","advice",
  "چاول یا باسمتی کے بعد گندم بروقت کاشت کریں اور دھان کی باقیات کا مناسب انتظام کریں۔",
  "Chawal ya basmati ke baad gandum barwaqt kaasht karein aur dhaan ki baqiyaat ka munasib intizam karein.",
  "medium", S["none"], "Sow wheat on time after rice/basmati; manage rice residue (rice-wheat)")
# ---- SEED ----
E(10,"PJW-SED-001","seed","sowing","advice",
  "تصدیق شدہ قسم کا بیج استعمال کریں۔",
  "Tasdeeq-shuda qism ka beej istemal karein.",
  "medium", S["pw"], "Use certified-variety seed")
E(11,"PJW-SED-002","seed","sowing","advice",
  "بیج کا علاج کریں تاکہ کنڈوا اور دیمک سے بچاؤ ہو۔",
  "Beej ka ilaaj karein taakay kandwa aur deemak se bachao ho.",
  "medium", S["pw"], "Treat seed against smut and termite")
# ---- FERTILIZER ----
E(12,"PJW-FRT-001","fertilizer","sowing","advice",
  "کاشت کے وقت ڈی اے پی (فاسفورس) ڈالیں؛ اس سے جڑیں اور پھٹاؤ مضبوط ہوتے ہیں۔",
  "Kaasht ke waqt DAP (phosphorus) daalein; is se jaren aur phutao mazboot hotay hain.",
  "medium", S["parc"], "Apply DAP (phosphorus) at sowing for strong roots/tillering")
E(13,"PJW-FRT-002","fertilizer","any","advice",
  "نائٹروجن ایک ساتھ نہیں، دو بار میں ڈالیں اور مٹی کے ٹیسٹ کے مطابق رکھیں۔",
  "Nitrogen aik saath nahin, do baar mein daalein aur mitti ke test ke mutabiq rakhein.",
  "medium", S["parc"], "Apply nitrogen in two splits, per soil test")
E(14,"PJW-FRT-003","fertilizer","any","advice",
  "نائٹروجن ضرورت سے زیادہ نہ ڈالیں؛ اس سے پیلا کنگی بڑھتا ہے۔",
  "Nitrogen zaroorat se zyada na daalein; is se peela kangi barhta hai.",
  "medium", S["rust"], "Don't over-apply nitrogen (worsens yellow rust)")
# ---- IRRIGATION ----
E(15,"PJW-IRR-001","irrigation","vegetative","advice",
  "پہلا پانی کاشت کے بیس پچیس دن بعد (جڑ بننے پر) دیں۔",
  "Pehla pani kaasht ke 20-25 din baad (jar bannay par) dein.",
  "medium", S["parc"], "First irrigation ~20-25 days after sowing (crown-root)")
E(16,"PJW-IRR-002","irrigation","any","advice",
  "پھٹاؤ، گابھے اور دانہ بننے کے وقت پانی کی کمی نہ ہونے دیں۔",
  "Phutao, gaabhay aur dana bannay ke waqt pani ki kami na honay dein.",
  "high", S["parc"], "No water shortage at tillering, booting, grain-filling")
E(17,"PJW-IRR-003","irrigation","any","advice",
  "تیز بارش میں کھیت سے فالتو پانی نکالنے کا بندوبست رکھیں۔",
  "Tez barish mein khet se faltu pani nikaalnay ka bandobast rakhein.",
  "low", S["none"], "Arrange drainage for heavy rain")
# ---- WEEDS ----
E(18,"PJW-WED-001","weeds","vegetative","advice",
  "جڑی بوٹیاں (جنگلی جئی، ڈمبی سٹی) شروع میں ہی قابو کریں؛ یہ گندم کی غذا لے جاتی ہیں۔",
  "Jari bootiyan (jangli jai, dumbi sitti) shuru mein hi qaboo karein; ye gandum ki ghiza le jaati hain.",
  "high", S["parc"], "Control weeds (wild oat, Phalaris) early - they steal nutrients")
E(19,"PJW-WED-002","weeds","vegetative","advice",
  "جڑی بوٹیوں کی دوا بروقت اور لیبل کے مطابق استعمال کریں؛ افسر سے مشورہ کریں۔",
  "Jari bootiyon ki dawa barwaqt aur label ke mutabiq istemal karein; officer se mashwara karein.",
  "medium", S["none"], "Use weedicide on time, per label; consult officer")
# ---- DISEASE (yellow rust headline) ----
E(20,"PJW-DIS-001","disease_alert","vegetative","urgent",
  "پتوں پر پیلے دھاری دار دھبے (پیلا کنگی) نظر آئیں تو فوراً زرعی افسر سے رجوع کریں۔",
  "Patton par peelay dhaari-daar dhabbay (peela kangi) nazar aayein to foran zarai officer se rujoo karein.",
  "high", S["rust"], "Yellow striped leaf spots (yellow rust) -> consult officer urgently")
E(21,"PJW-DIS-002","disease_alert","vegetative","warning",
  "سردی اور دھند میں پیلا کنگی بڑھتا ہے؛ گابھے سے پہلے فصل کا معائنہ کریں۔",
  "Sardi aur dhund mein peela kangi barhta hai; gaabhay se pehlay fasal ka moaina karein.",
  "high", S["rust"], "Yellow rust rises in cold/fog -> scout before booting")
E(22,"PJW-DIS-003","disease_alert","any","advice",
  "پیلا کنگی سے بچاؤ کے لیے زیادہ نائٹروجن نہ ڈالیں اور مزاحم قسم لگائیں۔",
  "Peela kangi se bachao ke liye zyada nitrogen na daalein aur muzahim qism lagayein.",
  "high", S["rust"], "Prevent yellow rust: avoid excess N, plant resistant variety")
E(23,"PJW-DIS-004","disease_alert","vegetative","warning",
  "پتوں پر بھورے نارنجی دھبے (بھوری کنگی) ہوں تو معائنہ کریں اور افسر سے مشورہ کریں۔",
  "Patton par bhooray narangi dhabbay (bhoori kangi) hon to moaina karein aur officer se mashwara karein.",
  "medium", S["rust"], "Brown/orange spots (brown rust) -> scout, consult officer")
E(24,"PJW-DIS-005","disease_alert","sowing","advice",
  "کھلی کنڈوا سے بچاؤ کے لیے علاج شدہ اور تصدیق شدہ بیج استعمال کریں۔",
  "Khuli kandwa se bachao ke liye ilaaj-shuda aur tasdeeq-shuda beej istemal karein.",
  "medium", S["pw"], "Prevent loose smut with treated, certified seed")
# ---- PEST ----
E(25,"PJW-PST-001","pest_alert","any","advice",
  "ہر ہفتے کھیت دیکھیں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔",
  "Har haftay khet dekhein; keeron ki tadaad dekh kar hi spray karein.",
  "high", S["none"], "Scout weekly; spray only on pest counts")
E(26,"PJW-PST-002","pest_alert","any","advice",
  "پتوں اور بالوں پر چیپا (ایفڈ) جمع ہو تو معائنہ کریں اور مددگار کیڑے بچائیں۔",
  "Patton aur baalon par cheepa (aphid) jama ho to moaina karein aur madadgaar keeray bachayein.",
  "low", S["none"], "Aphid colonies on leaves/ears -> scout, protect natural enemies")
E(27,"PJW-PST-003","pest_alert","vegetative","warning",
  "دیمک سے پودے مرجھائیں تو بیج یا زمین کا علاج کریں اور کھیت سے کچرا ہٹائیں۔",
  "Deemak se poday murjhaayein to beej ya zameen ka ilaaj karein aur khet se kachra hataayein.",
  "medium", S["pw"], "Termite wilting -> treat seed/soil, remove debris")
E(28,"PJW-PST-004","pest_alert","any","warning",
  "فوجی سنڈی پتے کھا جائے تو رات کو معائنہ کریں اور افسر سے رجوع کریں۔",
  "Fouji sundi pattay kha jaye to raat ko moaina karein aur officer se rujoo karein.",
  "low", S["none"], "Army worm chewing leaves -> scout at night, consult officer")
E(29,"PJW-PST-005","pest_alert","any","advice",
  "لیڈی برڈ جیسے مددگار کیڑوں کو بچائیں؛ یہ چیپا کھاتے ہیں۔",
  "Lady bird jaisay madadgaar keeron ko bachayein; ye cheepa khatay hain.",
  "medium", S["none"], "Protect ladybirds - they eat aphids")
# ---- WEATHER ----
E(30,"PJW-WEA-001","weather_alert","any","warning",
  "اگلے {days} دنوں میں تیز بارش متوقع ہے؛ آبپاشی اور کھاد ڈالنا روک دیں۔",
  "Aglay {days} dinon mein tez barish mutawaqqa hai; aabpashi aur khaad daalna rok dein.",
  "medium", S["none"], "Heavy rain in {days} days -> stop irrigation and fertiliser",
  [{"name":"days","type":"int","min":1,"max":7}])
E(31,"PJW-WEA-002","weather_alert","harvest","warning",
  "بارش یا اولوں کا خطرہ ہے؛ پکی فصل بروقت کاٹیں اور ڈھانپ کر خشک رکھیں۔",
  "Barish ya olon ka khatra hai; pakki fasal barwaqt kaatein aur dhaanp kar khushk rakhein.",
  "low", S["none"], "Rain/hail risk -> harvest ripe crop promptly, cover & dry")
E(32,"PJW-WEA-003","weather_alert","vegetative","advice",
  "دھند اور نمی میں پیلا کنگی تیزی سے پھیلتا ہے؛ معائنہ بڑھا دیں۔",
  "Dhund aur nami mein peela kangi tezi se phailta hai; moaina barha dein.",
  "high", S["rust"], "Fog/humidity spreads yellow rust fast -> scout more")
# ---- HARVEST / STORAGE ----
E(33,"PJW-HRV-001","harvest","harvest","advice",
  "جب دانہ سخت اور بھوسہ پیلا ہو جائے تو کٹائی کریں۔",
  "Jab dana sakht aur bhoosa peela ho jaye to katai karein.",
  "high", S["pw"], "Harvest when grain is hard and straw yellow")
E(34,"PJW-HRV-002","harvest","harvest","advice",
  "پکنے پر بروقت کٹائی کریں تاکہ دانہ جھڑنے سے نقصان نہ ہو۔",
  "Paknay par barwaqt katai karein taakay dana jharnay se nuqsaan na ho.",
  "high", S["pw"], "Harvest promptly at ripeness to avoid shattering loss")
E(35,"PJW-HRV-003","harvest","harvest","advice",
  "گہائی کی جگہ صاف رکھیں تاکہ دانہ صاف اور ملاوٹ سے پاک رہے۔",
  "Gahai ki jagah saaf rakhein taakay dana saaf aur milaawat se paak rahay.",
  "medium", S["none"], "Keep threshing floor clean for clean, unmixed grain")
E(36,"PJW-STO-001","storage","harvest","advice",
  "دانہ اچھی طرح خشک کر کے صاف اور بند جگہ رکھیں؛ گودام کے کیڑوں سے بچائیں۔",
  "Dana achhi tarah khushk kar ke saaf aur band jagah rakhein; godaam ke keeron se bachayein.",
  "low", S["none"], "Dry grain well; store clean, closed, safe from storage pests")
# ---- SAFETY ----
E(37,"PJW-SAF-001","safety","any","warning",
  "سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔",
  "Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.",
  "medium", S["none"], "Wear gloves, mask, covered clothes when spraying")
E(38,"PJW-SAF-002","safety","any","warning",
  "ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔",
  "Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.",
  "medium", S["none"], "Don't spray against the wind; keep others/animals away")
E(39,"PJW-SAF-003","safety","any","warning",
  "سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔",
  "Spray ke baad haath aur mooh dhoyein aur kapray badlein.",
  "medium", S["none"], "Wash hands & face, change clothes after spraying")
E(40,"PJW-SAF-004","safety","any","warning",
  "زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔",
  "Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.",
  "medium", S["none"], "Store pesticide in its labelled container, away from food/children")
E(41,"PJW-SAF-005","safety","harvest","warning",
  "سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے کٹائی نہ کریں۔",
  "Spray ke baad label par diye gaye waqfay se pehlay katai na karein.",
  "medium", S["none"], "Don't harvest before the label's pre-harvest interval")

# -- assemble dict --
entries = []
for (i, code, cat, stage, urg, ur, rom, conf, src, gloss, slots) in rows:
    e = {"id": i, "code": code, "category": cat, "crop_stage": stage, "urgency": urg,
         "text": {"ur": ur, "roman_ur": rom}, "sources": src, "confidence": conf, "status": "draft"}
    if slots: e["slots"] = slots
    entries.append(e)
doc = {"format_version": 2, "dictionary_id": DID, "code": CODE, "region": "punjab",
       "crop": "wheat", "dictionary_version": 1, "languages": ["ur", "roman_ur"], "entries": entries}
Path("dictionaries/punjab_wheat_v2.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

# -- review sheets --
OUT = Path("pilot/review_punjab_wheat"); OUT.mkdir(parents=True, exist_ok=True)
with open(OUT/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","code","category","crop_stage","urgency","english_meaning",
        "urdu_message","source_link","confidence","correct? (yes/no/partly)","suggested_change","comments"])
    for (i,code,cat,stage,urg,ur,rom,conf,src,gloss,slots) in rows:
        w.writerow([i,code,cat,stage,urg,gloss,ur,src[0]["link"],conf,"","",""])
with open(OUT/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","english_meaning","urdu_text","roman_ur_text",
        "understandable? (yes/no)","natural? (yes/no)","corrected_text"])
    for (i,code,cat,stage,urg,ur,rom,conf,src,gloss,slots) in rows:
        w.writerow([i,gloss,ur,rom,"","",""])

cats=Counter(e["category"] for e in entries); conf=Counter(e["confidence"] for e in entries)
Path("D2_COVERAGE_punjab_wheat.md").write_text(
f"""# D2 — Coverage (punjab_wheat v2, draft)

**{len(entries)} draft entries.** Shares the wheat core with KPK wheat; Punjab-specific
entries cover the **1-20 Nov irrigated sowing window**, barani window, ~40 kg seed rate,
Punjab rust-resistant varieties, and the **rice-wheat rotation**. All `status: draft`.

By category: {dict(sorted(cats.items()))}
By confidence: {dict(conf)}

Honest notes: variety names (Akbar-2019, Dilkash-2020) must be checked against the
CURRENT Punjab Agriculture Dept / AARI recommended list; no fungicide doses; Punjabi/
Saraiki not included (Urdu + Roman only) - a native speaker must add them.
""", encoding="utf-8")
print(f"punjab_wheat: {len(entries)} entries; by conf {dict(conf)}")
