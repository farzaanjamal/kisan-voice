"""
D2 — build the v2 punjab_cotton dictionary from the R1 brief.

Honest rules applied:
- Every entry is status="draft" and needs native-speaker + agronomist review.
- No pesticide DOSES are stated; where a threshold is crossed the message defers
  to the extension officer + product label (per project rule + R1).
- Only numbers that appear are sourced (whitefly 4-5/leaf, bollworm 5% damage) or
  are a typed template slot ({days}).
- We do NOT pad to 60 with weak entries. Sparse categories are flagged, not faked.
"""
import json

CODE = "PCT"
SRC = {
    "clcuv": [{"link": "https://mel.cgiar.org/projects/205", "note": "CCRI Multan CLCuV — verify official"}],
    "etl":   [{"link": "https://www.researchgate.net/publication/336834366", "note": "Punjab Pakistan ETL study — verify with CCRI/PAD"}],
    "ipm":   [{"link": "https://www.researchgate.net/figure/Economic-Threshold-Levels-ETLs-of-major-insect-pests-of-cotton_tbl1_281188213", "note": "IPM/ETL — verify official"}],
    "cal":   [{"link": "https://irfarm.com/blogs/latest/seasonal-crop-calendar-pakistan-month-by-month-guide", "note": "crop calendar — verify PAD/AARI"}],
    "none":  [{"link": "[NEEDS SOURCE]", "note": "pull official PAD/AARI leaflet"}],
}

def E(id, code, cat, stage, urg, ur, rom, conf, src, urgent_months=None, slots=None, speech=None):
    e = {
        "id": id, "code": code, "category": cat, "crop_stage": stage, "urgency": urg,
        "text": {"ur": ur, "roman_ur": rom},
        "sources": src, "confidence": conf, "status": "draft",
    }
    if slots: e["slots"] = slots
    if speech: e["speech_text"] = speech
    return e

entries = [
    # ----- DISEASE: cotton leaf curl virus FIRST (the headline Punjab disease) -----
    E(1,"PCT-DIS-001","disease_alert","any","warning",
      "پتہ مروڑ وائرس سے بچاؤ: جلد کاشت کریں، متوازن کھاد دیں اور جڑی بوٹیاں ختم کریں۔",
      "Patta maror virus se bachao: jald kaasht karein, mutawazin khaad dein aur jari bootiyan khatam karein.",
      "high", SRC["clcuv"]),
    E(2,"PCT-DIS-002","disease_alert","any","urgent",
      "پتہ مروڑ والے پودے فوراً نکال کر تلف کریں تاکہ وائرس آگے نہ پھیلے۔",
      "Patta maror walay poday foran nikaal kar talaf karein taakay virus aagay na phaile.",
      "medium", SRC["clcuv"]),
    E(3,"PCT-DIS-003","disease_alert","any","warning",
      "سفید مکھی پتہ مروڑ وائرس پھیلاتی ہے؛ اس کی تعداد پر نظر رکھیں اور قابو کریں۔",
      "Safaid makhi patta maror virus phailati hai; is ki tadaad par nazar rakhein aur qaboo karein.",
      "high", SRC["clcuv"]),
    E(4,"PCT-DIS-004","disease_alert","vegetative","warning",
      "کپاس میں بیکٹیریل بلائٹ کی علامت ہو تو متاثرہ پتے ہٹائیں اور زرعی افسر سے رجوع کریں۔",
      "Kapas mein bacterial blight ki alamat ho to mutasira pattay hataayein aur zarai officer se rujoo karein.",
      "low", SRC["none"]),
    E(5,"PCT-DIS-005","disease_alert","harvest","warning",
      "زیادہ نمی میں بول سڑ سکتے ہیں؛ ہوا کا گزر رکھیں اور بروقت چنائی کریں۔",
      "Zyada nami mein bol sarr saktay hain; hawa ka guzar rakhein aur barwaqt chunai karein.",
      "low", SRC["none"]),

    # ----- VARIETY / SOWING / SEED -----
    E(6,"PCT-VAR-001","variety","sowing","advice",
      "کاشت کے لیے پتہ مروڑ وائرس برداشت کرنے والی منظور شدہ قسم چنیں۔",
      "Kaasht ke liye patta maror virus bardasht karnay wali manzoor-shuda qism chunein.",
      "medium", SRC["clcuv"]),
    E(7,"PCT-SOW-001","sowing","sowing","advice",
      "کپاس اپریل سے وسط مئی میں کاشت کریں؛ بہت دیر سے کاشت نقصان دہ ہے۔",
      "Kapas April se wast-e-May mein kaasht karein; bohat der se kaasht nuqsaan-deh hai.",
      "medium", SRC["cal"]),
    E(8,"PCT-SOW-002","sowing","sowing","advice",
      "جلد کاشت سے پتہ مروڑ وائرس کا خطرہ کم ہوتا ہے۔",
      "Jald kaasht se patta maror virus ka khatra kam hota hai.",
      "medium", SRC["clcuv"]),
    E(9,"PCT-SED-001","seed","sowing","advice",
      "تصدیق شدہ اور علاج شدہ بیج استعمال کریں؛ مقدار کے لیے زرعی افسر سے مشورہ کریں۔",
      "Tasdeeq-shuda aur ilaaj-shuda beej istemal karein; miqdaar ke liye zarai officer se mashwara karein.",
      "low", SRC["none"]),

    # ----- FERTILIZER -----
    E(10,"PCT-FRT-001","fertilizer","any","advice",
      "کھاد مٹی کے ٹیسٹ کے مطابق ڈالیں اور زرعی افسر سے مشورہ کریں۔",
      "Khaad mitti ke test ke mutabiq daalein aur zarai officer se mashwara karein.",
      "medium", SRC["none"]),
    E(11,"PCT-FRT-002","fertilizer","any","advice",
      "نائٹروجن ضرورت سے زیادہ نہ ڈالیں؛ اس سے سفید مکھی اور وائرس بڑھتے ہیں۔",
      "Nitrogen zaroorat se zyada na daalein; is se safaid makhi aur virus barhtay hain.",
      "medium", SRC["clcuv"]),
    E(12,"PCT-FRT-003","fertilizer","any","advice",
      "متوازن کھاد (این، پی، کے) دیں تاکہ فصل مضبوط رہے۔",
      "Mutawazin khaad (N, P, K) dein taakay fasal mazboot rahay.",
      "low", SRC["none"]),

    # ----- IRRIGATION -----
    E(13,"PCT-IRR-001","irrigation","flowering","advice",
      "پھول آنے پر کپاس کو پانی کی کمی نہ ہونے دیں۔",
      "Phool aanay par kapas ko pani ki kami na honay dein.",
      "medium", SRC["cal"]),
    E(14,"PCT-IRR-002","irrigation","boll","advice",
      "بول بننے کے وقت پانی باقاعدگی سے دیں۔",
      "Bol bannay ke waqt pani baqaidagi se dein.",
      "medium", SRC["cal"]),
    E(15,"PCT-IRR-003","irrigation","any","advice",
      "تیز بارش میں کھیت سے فالتو پانی نکالنے کا بندوبست رکھیں۔",
      "Tez barish mein khet se faltu pani nikaalnay ka bandobast rakhein.",
      "low", SRC["none"]),

    # ----- WEEDS -----
    E(16,"PCT-WED-001","weeds","any","advice",
      "کھیت اور اردگرد جڑی بوٹیاں ختم کریں؛ یہ سفید مکھی اور وائرس کا ٹھکانہ ہیں۔",
      "Khet aur ird-gird jari bootiyan khatam karein; ye safaid makhi aur virus ka thikana hain.",
      "high", SRC["clcuv"]),

    # ----- PEST ALERTS (scout -> ETL -> defer dose to officer/label) -----
    E(17,"PCT-PST-001","pest_alert","any","advice",
      "ہر ہفتے کھیت کا معائنہ کریں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔",
      "Har haftay khet ka moaina karein; keeron ki tadaad dekh kar hi spray karein.",
      "high", SRC["ipm"]),
    E(18,"PCT-PST-002","pest_alert","flowering","warning",
      "اگر سفید مکھی ہر پتے پر چار پانچ سے زیادہ ہو تو افسر سے مشورہ کر کے عمل کریں۔",
      "Agar safaid makhi har pattay par 4-5 se zyada ho to officer se mashwara kar ke amal karein.",
      "medium", SRC["etl"]),
    E(19,"PCT-PST-003","pest_alert","vegetative","warning",
      "جیسڈ سے پتوں کے کنارے پیلے ہو کر مڑ جائیں تو معائنہ کریں اور ضرورت پر افسر سے رجوع کریں۔",
      "Jassid se patton ke kinaray peelay ho kar murr jaayein to moaina karein aur zaroorat par officer se rujoo karein.",
      "medium", SRC["etl"]),
    E(20,"PCT-PST-004","pest_alert","boll","urgent",
      "نرم کچے بول اور گلابی سنڈی نظر آئے تو متاثرہ بول توڑ کر تلف کریں اور افسر سے رابطہ کریں۔",
      "Naram kachay bol aur gulabi sundi nazar aaye to mutasira bol torr kar talaf karein aur officer se rabta karein.",
      "medium", SRC["ipm"]),
    E(21,"PCT-PST-005","pest_alert","fruiting","warning",
      "اگر پانچ فیصد پھل یا بول کیڑے سے خراب ہوں تو افسر سے مشورہ کریں۔",
      "Agar 5 percent phal ya bol keeray se kharab hon to officer se mashwara karein.",
      "medium", SRC["ipm"]),
    E(22,"PCT-PST-006","pest_alert","boll","advice",
      "گلابی سنڈی کی نگرانی کے لیے کھیت میں فیرومون ٹریپ لگائیں۔",
      "Gulabi sundi ki nigrani ke liye khet mein pheromone trap lagaayein.",
      "medium", SRC["ipm"]),
    E(23,"PCT-PST-007","pest_alert","seedling","advice",
      "تھرپس سے نئے پتے مڑ سکتے ہیں؛ عموماً سپرے کی ضرورت نہیں، معائنہ کرتے رہیں۔",
      "Thrips se naye pattay murr saktay hain; umooman spray ki zaroorat nahin, moaina kartay rahein.",
      "low", SRC["etl"]),
    E(24,"PCT-PST-008","pest_alert","any","advice",
      "میلی بگ نظر آئے تو متاثرہ شاخیں ہٹائیں اور اردگرد صفائی رکھیں۔",
      "Mealybug nazar aaye to mutasira shaakhein hataayein aur ird-gird safai rakhein.",
      "low", SRC["none"]),
    E(25,"PCT-PST-009","pest_alert","any","advice",
      "غیر ضروری سپرے سے گریز کریں؛ اس سے کیڑے دوا کے خلاف مزاحم ہو جاتے ہیں۔",
      "Ghair-zaroori spray se gurez karein; is se keeray dawa ke khilaaf muzahim ho jaatay hain.",
      "medium", SRC["ipm"]),
    E(26,"PCT-PST-010","pest_alert","any","advice",
      "لیڈی برڈ جیسے مددگار کیڑوں کو بچائیں؛ یہ نقصان دہ کیڑے کھاتے ہیں۔",
      "Lady bird jaisay madadgaar keeron ko bachaayein; ye nuqsaan-deh keeray khaatay hain.",
      "low", SRC["ipm"]),

    # ----- WEATHER ALERTS (templated) -----
    E(27,"PCT-WEA-001","weather_alert","any","warning",
      "اگلے {days} دنوں میں تیز بارش متوقع ہے؛ آبپاشی اور کھاد ڈالنا روک دیں۔",
      "Aglay {days} dinon mein tez barish mutawaqqa hai; aabpashi aur khaad daalna rok dein.",
      "medium", SRC["cal"],
      slots=[{"name":"days","type":"int","min":1,"max":7}]),
    E(28,"PCT-WEA-002","weather_alert","harvest","warning",
      "بارش متوقع ہے؛ چنائی خشک موسم تک روک دیں اور چنی ہوئی روئی ڈھانپ کر رکھیں۔",
      "Barish mutawaqqa hai; chunai khushk mausam tak rok dein aur chuni hui rooi dhaanp kar rakhein.",
      "low", SRC["none"]),
    E(29,"PCT-WEA-003","weather_alert","any","advice",
      "گرمی کی لہر کے بعد سفید مکھی تیزی سے بڑھتی ہے؛ معائنہ بڑھا دیں۔",
      "Garmi ki lehar ke baad safaid makhi tezi se barhti hai; moaina barha dein.",
      "medium", SRC["etl"]),
    E(30,"PCT-WEA-004","weather_alert","harvest","advice",
      "زیادہ نمی میں بول سڑنے کا خطرہ ہے؛ بروقت چنائی کریں۔",
      "Zyada nami mein bol sarnay ka khatra hai; barwaqt chunai karein.",
      "low", SRC["none"]),

    # ----- HARVEST / STORAGE -----
    E(31,"PCT-HRV-001","harvest","harvest","advice",
      "چنائی اوس ختم ہونے کے بعد، خشک موسم میں کریں۔",
      "Chunai os khatam honay ke baad, khushk mausam mein karein.",
      "medium", SRC["cal"]),
    E(32,"PCT-HRV-002","harvest","harvest","advice",
      "چنائی باقاعدگی سے کریں تاکہ روئی زمین پر گر کر خراب نہ ہو۔",
      "Chunai baqaidagi se karein taakay rooi zameen par gir kar kharab na ho.",
      "medium", SRC["cal"]),
    E(33,"PCT-HRV-003","harvest","harvest","advice",
      "روئی کو مٹی، پتوں اور دھاگوں سے پاک رکھیں تاکہ معیار بہتر رہے۔",
      "Rooi ko mitti, patton aur dhaagon se paak rakhein taakay miyaar behtar rahay.",
      "medium", SRC["none"]),
    E(34,"PCT-HRV-004","harvest","harvest","advice",
      "داغ دار یا گیلی روئی الگ رکھیں تاکہ اچھی روئی خراب نہ ہو۔",
      "Daagh-daar ya geeli rooi alag rakhein taakay achhi rooi kharab na ho.",
      "low", SRC["none"]),
    E(35,"PCT-STO-001","storage","harvest","advice",
      "چنی ہوئی روئی خشک اور صاف جگہ رکھیں؛ نمی سے بچائیں۔",
      "Chuni hui rooi khushk aur saaf jagah rakhein; nami se bachaayein.",
      "low", SRC["none"]),

    # ----- SAFETY -----
    E(36,"PCT-SAF-001","safety","any","warning",
      "سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔",
      "Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.",
      "medium", SRC["none"]),
    E(37,"PCT-SAF-002","safety","any","warning",
      "ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔",
      "Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.",
      "medium", SRC["none"]),
    E(38,"PCT-SAF-003","safety","any","warning",
      "سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔",
      "Spray ke baad haath aur mooh dhoyein aur kapray badlein.",
      "medium", SRC["none"]),
    E(39,"PCT-SAF-004","safety","any","warning",
      "زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔",
      "Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.",
      "medium", SRC["none"]),
    E(40,"PCT-SAF-005","safety","any","urgent",
      "زہر لگنے کی علامت (متلی، چکر) پر فوراً طبی مدد لیں اور دوا کا لیبل ساتھ لے جائیں۔",
      "Zehr lagnay ki alamat (matli, chakkar) par foran tibbi madad lein aur dawa ka label saath le jaayein.",
      "medium", SRC["none"]),
    E(41,"PCT-SAF-006","safety","harvest","warning",
      "سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے چنائی نہ کریں۔",
      "Spray ke baad label par diye gaye waqfay se pehlay chunai na karein.",
      "medium", SRC["none"]),
]

doc = {
    "format_version": 2, "dictionary_id": 1, "code": CODE,
    "region": "punjab", "crop": "cotton", "dictionary_version": 2,
    "languages": ["ur", "roman_ur"], "entries": entries,
}

with open("dictionaries/punjab_cotton_v2.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

# coverage report
from collections import Counter
cats = Counter(e["category"] for e in entries)
conf = Counter(e["confidence"] for e in entries)
print(f"entries: {len(entries)}  (dictionary_version bumped to 2)")
print("by category:", dict(cats))
print("by confidence:", dict(conf))
