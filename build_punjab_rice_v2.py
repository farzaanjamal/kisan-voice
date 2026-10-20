"""
Punjab rice (Basmati) v2 — shares the rice core with Sindh rice, with Basmati-specific
entries (approved Basmati varieties, aroma/lodging from excess N, false smut, Nov-Dec
harvest). All draft; no pesticide doses; Punjabi not used (Urdu + Roman only).
Emits the dictionary + expert/native review sheets + coverage note.
"""
import csv, json
from collections import Counter
from pathlib import Path

CODE, DID = "PJR", 5
S = {
 "pr":   [{"link": "https://pakistanrice.com/harvest-calendar/", "note": "Punjab Basmati belt / harvest Nov-Dec — verify RRI Kala Shah Kaku"}],
 "parc": [{"link": "http://www.parc.gov.pk/index.php/en/faq-s/60-faqs/73-rice", "note": "PARC rice FAQ"}],
 "etl":  [{"link": "https://niphm.gov.in/IPMPackages/Rice.pdf", "note": "rice ETLs (India pkg) - confirm for Pakistan"}],
 "mgmt": [{"link": "https://austinpublishinggroup.com/ebooks/food-security/chapters/Rice-Production-1006.pdf", "note": "Pakistan rice pest/disease mgmt"}],
 "none": [{"link": "[NEEDS SOURCE]", "note": "confirm with RRI Kala Shah Kaku / Punjab Agri Dept"}],
}
rows = []
def E(i, code, cat, stage, urg, ur, rom, conf, src, gloss, slots=None):
    rows.append((i, code, cat, stage, urg, ur, rom, conf, src, gloss, slots))

# ---- WATER / IRRIGATION ----
E(1,"PJR-IRR-001","irrigation","any","advice",
  "پانی کھیت میں مسلسل کھڑا نہ رہنے دیں؛ باری باری سکھائیں، اس سے بھوری پھدکی کم ہوتی ہے۔",
  "Pani khet mein musalsal khara na rehnay dein; baari baari sukhayein, is se bhoori phudki kam hoti hai.",
  "high", S["mgmt"], "AWD: don't keep water standing; dry intermittently (cuts BPH)")
E(2,"PJR-IRR-002","irrigation","flowering","advice",
  "پھول اور دانہ بننے کے وقت کھیت میں مناسب پانی رکھیں۔",
  "Phool aur dana bannay ke waqt khet mein munasib pani rakhein.",
  "medium", S["parc"], "Keep adequate water at flowering/grain-fill")
E(3,"PJR-IRR-003","irrigation","harvest","advice",
  "کٹائی سے پہلے کھیت کا پانی نکال دیں تاکہ زمین سخت ہو اور کٹائی آسان ہو۔",
  "Katai se pehlay khet ka pani nikaal dein taakay zameen sakht ho aur katai aasan ho.",
  "medium", S["none"], "Drain field before harvest for easier cutting")
# ---- FERTILIZER (Basmati: excess N -> lodging + aroma loss) ----
E(4,"PJR-FRT-001","fertilizer","any","advice",
  "کھاد مٹی کے ٹیسٹ کے مطابق ڈالیں اور زرعی افسر سے مشورہ کریں۔",
  "Khaad mitti ke test ke mutabiq daalein aur zarai officer se mashwara karein.",
  "medium", S["none"], "Fertilise per soil test; consult officer")
E(5,"PJR-FRT-002","fertilizer","any","advice",
  "نائٹروجن ایک ساتھ نہیں، دو تین بار میں ڈالیں۔",
  "Nitrogen aik saath nahin, 2-3 baar mein daalein.",
  "high", S["parc"], "Apply nitrogen in 2-3 splits")
E(6,"PJR-FRT-003","fertilizer","any","warning",
  "باسمتی میں نائٹروجن زیادہ نہ ڈالیں؛ اس سے فصل گر جاتی ہے اور خوشبو کم ہوتی ہے۔",
  "Basmati mein nitrogen zyada na daalein; is se fasal gir jaati hai aur khushbu kam hoti hai.",
  "medium", S["mgmt"], "Don't over-apply nitrogen to Basmati - it causes lodging and cuts aroma")
# ---- VARIETY / NURSERY / SOWING / SEED (Basmati) ----
E(7,"PJR-VAR-001","variety","sowing","advice",
  "پنجاب کے لیے منظور شدہ باسمتی قسم کاشت کریں (مثلاً سپر باسمتی، باسمتی-515)۔",
  "Punjab ke liye manzoor-shuda Basmati qism kaasht karein (misaal: Super Basmati, Basmati-515).",
  "medium", S["pr"], "Plant a Punjab-approved Basmati variety (e.g. Super Basmati, Basmati-515)")
E(8,"PJR-SOW-001","sowing","sowing","advice",
  "پنیری پچیس سے تیس دن میں لگائیں؛ زیادہ پرانی پنیری پیداوار کم کرتی ہے۔",
  "Paneeri 25-30 din mein lagayein; zyada purani paneeri paidawar kam karti hai.",
  "high", S["parc"], "Transplant nursery at 25-30 days; old nursery cuts yield")
E(9,"PJR-SOW-002","sowing","sowing","advice",
  "باسمتی کی پنیری بروقت لگائیں؛ تاخیر سے خوشبو اور معیار کم ہوتا ہے۔",
  "Basmati ki paneeri barwaqt lagayein; taakheer se khushbu aur miyaar kam hota hai.",
  "medium", S["pr"], "Transplant Basmati on time; delay reduces aroma and quality")
E(10,"PJR-SOW-003","sowing","sowing","advice",
  "ہر جگہ دو پنیری لگائیں تاکہ فصل اچھی کھڑی ہو۔",
  "Har jagah do paneeri lagayein taakay fasal achhi khari ho.",
  "medium", S["parc"], "Plant two seedlings per hill for a good stand")
E(11,"PJR-SED-001","seed","sowing","advice",
  "تصدیق شدہ اور صاف باسمتی بیج استعمال کریں تاکہ قسم خالص رہے۔",
  "Tasdeeq-shuda aur saaf Basmati beej istemal karein taakay qism khaalis rahay.",
  "medium", S["pr"], "Use certified, clean Basmati seed to keep the variety pure")
# ---- WEEDS ----
E(12,"PJR-WED-001","weeds","any","advice",
  "پنیری اور کھیت کو جڑی بوٹیوں سے پاک رکھیں تاکہ غذا اور پانی فصل کو ملے۔",
  "Paneeri aur khet ko jari bootiyon se paak rakhein taakay ghiza aur pani fasal ko milay.",
  "medium", S["none"], "Keep nursery and field weed-free")
# ---- PEST ----
E(13,"PJR-PST-001","pest_alert","any","advice",
  "ہر ہفتے کھیت دیکھیں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔",
  "Har haftay khet dekhein; keeron ki tadaad dekh kar hi spray karein.",
  "high", S["etl"], "Scout weekly; spray only on pest counts")
E(14,"PJR-PST-002","pest_alert","vegetative","warning",
  "نئی فصل میں بیچ کا شگوفہ سوکھ جائے تو تنا چھیدک کا حملہ ہے؛ افسر سے مشورہ کریں۔",
  "Nai fasal mein beech ka shiguufa sookh jaye to tana chhedak ka hamla hai; officer se mashwara karein.",
  "medium", S["etl"], "Dead central shoot = stem borer; consult officer")
E(15,"PJR-PST-003","pest_alert","harvest","advice",
  "کٹائی کے بعد مڈھ اور پرالی کھیت میں دبا دیں؛ اس سے تنا چھیدک کے کیڑے مر جاتے ہیں۔",
  "Katai ke baad mandh aur parali khet mein daba dein; is se tana chhedak ke keeray mar jatay hain.",
  "high", S["mgmt"], "Bury stubble/straw after harvest (kills stem-borer larvae)")
E(16,"PJR-PST-004","pest_alert","tillering","warning",
  "بھوری پھدکی سے پتے پیلے بھورے ہوں تو پانی کھڑا نہ رکھیں اور افسر سے رجوع کریں۔",
  "Bhoori phudki se pattay peelay bhooray hon to pani khara na rakhein aur officer se rujoo karein.",
  "high", S["mgmt"], "Hopperburn (yellow-brown patches) = BPH; drain water, consult officer")
E(17,"PJR-PST-005","pest_alert","tillering","warning",
  "اگر بھوری پھدکی فی بوٹا دس پندرہ سے زیادہ ہو تو افسر سے مشورہ کر کے عمل کریں۔",
  "Agar bhoori phudki fi boota 10-15 se zyada ho to officer se mashwara kar ke amal karein.",
  "medium", S["etl"], "BPH over ~10-15/hill -> consult officer")
E(18,"PJR-PST-006","pest_alert","vegetative","advice",
  "پتے لپٹے اور دھاگے سے جڑے ہوں تو پتہ لپیٹ کیڑا ہے؛ معائنہ کریں اور مددگار کیڑے بچائیں۔",
  "Pattay liptay aur dhaagay se juray hon to patta lapet keera hai; moaina karein aur madadgaar keeray bachayein.",
  "medium", S["mgmt"], "Folded, silk-tied leaves = leaf folder; scout, protect natural enemies")
E(19,"PJR-PST-007","pest_alert","any","advice",
  "مکڑی اور لیڈی برڈ جیسے مددگار کیڑوں کو بچائیں؛ یہ پھدکیاں کھاتے ہیں۔",
  "Makri aur lady bird jaisay madadgaar keeron ko bachayein; ye phudkiyan khatay hain.",
  "medium", S["mgmt"], "Protect spiders/ladybirds - they eat hoppers")
E(20,"PJR-PST-008","pest_alert","any","advice",
  "غیر ضروری سپرے سے گریز کریں؛ اس سے بھوری پھدکی اور بڑھ سکتی ہے۔",
  "Ghair-zaroori spray se gurez karein; is se bhoori phudki aur barh sakti hai.",
  "medium", S["mgmt"], "Avoid unnecessary sprays (can worsen BPH)")
# ---- DISEASE (add false smut for Basmati) ----
E(21,"PJR-DIS-001","disease_alert","vegetative","warning",
  "پتوں پر بلاسٹ کے نوکدار دھبے ہوں تو زیادہ نائٹروجن نہ ڈالیں اور افسر سے مشورہ کریں۔",
  "Patton par blast ke nokdaar dhabbay hon to zyada nitrogen na daalein aur officer se mashwara karein.",
  "medium", S["etl"], "Pointed blast lesions -> cut nitrogen, consult officer")
E(22,"PJR-DIS-002","disease_alert","vegetative","warning",
  "اگر فی پتہ تین سے پانچ بلاسٹ کے دھبے ہوں تو افسر سے رجوع کریں۔",
  "Agar fi patta 3 se 5 blast ke dhabbay hon to officer se rujoo karein.",
  "medium", S["etl"], "~3-5 blast lesions/leaf -> consult officer")
E(23,"PJR-DIS-003","disease_alert","vegetative","warning",
  "بیکٹیریل جھلساؤ میں پتوں کے کنارے پیلے ہو کر سوکھیں؛ نائٹروجن کم کریں اور متاثرہ باقیات ہٹائیں۔",
  "Bacterial jhulsao mein patton ke kinaray peelay ho kar sookhein; nitrogen kam karein aur mutasira baqiyaat hataayein.",
  "medium", S["mgmt"], "Bacterial blight (yellow drying leaf edges) -> reduce N, remove debris")
E(24,"PJR-DIS-004","disease_alert","flowering","warning",
  "باسمتی کے دانوں پر سبز سیاہ گانٹھیں (فالس سمٹ) ہوں تو متاثرہ بالیاں ہٹائیں اور افسر سے مشورہ کریں۔",
  "Basmati ke daanon par sabz siyah ganthein (false smut) hon to mutasira baliyan hataayein aur officer se mashwara karein.",
  "low", S["mgmt"], "Greenish-black grain balls (false smut) -> remove affected panicles, consult officer")
E(25,"PJR-DIS-005","disease_alert","flowering","advice",
  "پتے کی نیام پر خاکستری دھبے (شیتھ بلائٹ) ہوں تو بوائی گھنی نہ کریں اور ہوا کا گزر رکھیں۔",
  "Pattay ki niyaam par khaakistari dhabbay (sheath blight) hon to bouai ghani na karein aur hawa ka guzar rakhein.",
  "low", S["mgmt"], "Grey sheath lesions -> avoid dense planting, improve airflow")
E(26,"PJR-DIS-006","disease_alert","harvest","advice",
  "کٹائی کے بعد پرالی اور مڈھ کھیت میں دبا دیں تاکہ بیماریاں کم ہوں۔",
  "Katai ke baad parali aur mandh khet mein daba dein taakay bimariyan kam hon.",
  "medium", S["mgmt"], "Bury straw/stubble after harvest to cut disease")
# ---- WEATHER ----
E(27,"PJR-WEA-001","weather_alert","any","warning",
  "اگلے {days} دنوں میں تیز بارش متوقع ہے؛ کھیت سے فالتو پانی نکالیں اور کھاد ڈالنا روک دیں۔",
  "Aglay {days} dinon mein tez barish mutawaqqa hai; khet se faltu pani nikaalein aur khaad daalna rok dein.",
  "medium", S["none"], "Heavy rain in {days} days -> drain field, stop fertiliser",
  [{"name":"days","type":"int","min":1,"max":7}])
E(28,"PJR-WEA-002","weather_alert","harvest","warning",
  "بارش متوقع ہے؛ پکی فصل بروقت کاٹیں اور کٹی فصل ڈھانپ کر خشک رکھیں۔",
  "Barish mutawaqqa hai; pakki fasal barwaqt kaatein aur kati fasal dhaanp kar khushk rakhein.",
  "low", S["none"], "Rain expected -> harvest ripe crop promptly, cover & dry cut crop")
E(29,"PJR-WEA-003","weather_alert","tillering","advice",
  "گرمی اور کھڑے پانی میں بھوری پھدکی بڑھتی ہے؛ پانی باری باری سکھائیں اور معائنہ بڑھائیں۔",
  "Garmi aur kharay pani mein bhoori phudki barhti hai; pani baari baari sukhayein aur moaina barhayein.",
  "medium", S["mgmt"], "Heat + standing water boosts BPH -> dry intermittently, scout more")
# ---- HARVEST / STORAGE (Basmati Nov-Dec) ----
E(30,"PJR-HRV-001","harvest","harvest","advice",
  "جب اسی سے پچاسی فیصد بالیاں پک جائیں تو باسمتی کی کٹائی کریں (عموماً نومبر-دسمبر)۔",
  "Jab 80 se 85 percent baliyan pak jayein to Basmati ki katai karein (umooman November-December).",
  "medium", S["pr"], "Harvest Basmati when 80-85% panicles ripen (usually Nov-Dec)")
E(31,"PJR-HRV-002","harvest","harvest","advice",
  "کٹی ہوئی فصل دو تین دن کھیت میں خشک ہونے دیں، پھر گہائی کریں۔",
  "Kati hui fasal 2-3 din khet mein khushk honay dein, phir gahai karein.",
  "high", S["parc"], "Let cut crop dry 2-3 days before threshing")
E(32,"PJR-HRV-003","harvest","harvest","advice",
  "گہائی کی جگہ صاف رکھیں تاکہ دانہ صاف اور ملاوٹ سے پاک رہے۔",
  "Gahai ki jagah saaf rakhein taakay dana saaf aur milaawat se paak rahay.",
  "medium", S["parc"], "Keep threshing floor clean for clean, unmixed grain")
E(33,"PJR-HRV-004","harvest","harvest","advice",
  "بیج والی فصل الگ کاٹیں اور الگ رکھیں تاکہ قسمیں آپس میں نہ ملیں۔",
  "Beej wali fasal alag kaatein aur alag rakhein taakay qismein aapas mein na milein.",
  "medium", S["parc"], "Harvest/keep seed crop separately to avoid variety mixing")
E(34,"PJR-STO-001","storage","harvest","advice",
  "دانہ اچھی طرح خشک کر کے صاف اور خشک جگہ رکھیں؛ نمی سے بچائیں۔",
  "Dana achhi tarah khushk kar ke saaf aur khushk jagah rakhein; nami se bachayein.",
  "low", S["none"], "Dry grain well; store clean and dry")
# ---- SAFETY ----
E(35,"PJR-SAF-001","safety","any","warning",
  "سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔",
  "Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.",
  "medium", S["none"], "Wear gloves, mask, covered clothes when spraying")
E(36,"PJR-SAF-002","safety","any","warning",
  "ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔",
  "Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.",
  "medium", S["none"], "Don't spray against the wind; keep others/animals away")
E(37,"PJR-SAF-003","safety","any","warning",
  "سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔",
  "Spray ke baad haath aur mooh dhoyein aur kapray badlein.",
  "medium", S["none"], "Wash hands & face, change clothes after spraying")
E(38,"PJR-SAF-004","safety","any","warning",
  "زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔",
  "Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.",
  "medium", S["none"], "Store pesticide in its labelled container, away from food/children")
E(39,"PJR-SAF-005","safety","any","urgent",
  "زہر لگنے کی علامت (متلی، چکر) پر فوراً طبی مدد لیں اور دوا کا لیبل ساتھ لے جائیں۔",
  "Zehr lagnay ki alamat (matli, chakkar) par foran tibbi madad lein aur dawa ka label saath le jayein.",
  "medium", S["none"], "Poisoning signs (nausea, dizziness) -> get medical help, take the label")
E(40,"PJR-SAF-006","safety","harvest","warning",
  "سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے کٹائی نہ کریں۔",
  "Spray ke baad label par diye gaye waqfay se pehlay katai na karein.",
  "medium", S["none"], "Don't harvest before the label's pre-harvest interval")

entries = []
for (i, code, cat, stage, urg, ur, rom, conf, src, gloss, slots) in rows:
    e = {"id": i, "code": code, "category": cat, "crop_stage": stage, "urgency": urg,
         "text": {"ur": ur, "roman_ur": rom}, "sources": src, "confidence": conf, "status": "draft"}
    if slots: e["slots"] = slots
    entries.append(e)
doc = {"format_version": 2, "dictionary_id": DID, "code": CODE, "region": "punjab",
       "crop": "rice", "dictionary_version": 1, "languages": ["ur", "roman_ur"], "entries": entries}
Path("dictionaries/punjab_rice_v2.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

OUT = Path("pilot/review_punjab_rice"); OUT.mkdir(parents=True, exist_ok=True)
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
Path("D2_COVERAGE_punjab_rice.md").write_text(
f"""# D2 — Coverage (punjab_rice / Basmati v2, draft)

**{len(entries)} draft entries.** Shares the rice core with Sindh rice; Basmati-specific
entries cover approved **Basmati varieties**, the **aroma/lodging** risk from excess
nitrogen, **false smut**, and the **Nov-Dec harvest**. All `status: draft`.

By category: {dict(sorted(cats.items()))}
By confidence: {dict(conf)}

Honest notes: Basmati variety names must be checked against the CURRENT RRI Kala Shah
Kaku / Punjab Agri Dept list; no pesticide doses; Punjabi not included (Urdu + Roman
only) - a native speaker must add it.
""", encoding="utf-8")
print(f"punjab_rice: {len(entries)} entries; by conf {dict(conf)}")
