"""
D2 — build the v2 kpk_wheat dictionary from the R1 (kpk_wheat) brief.

Honest rules: all status="draft"; no fungicide/pesticide doses; timely sowing +
rust-resistant variety foregrounded (the season's live decisions); Pashto NOT included
(unreliable to auto-translate) — draft ships Urdu + Roman Urdu only. Not padded to 60.
"""
import json

CODE = "KPW"
S = {
    "kp":   [{"link": "https://zarat.kp.gov.pk/assets/uploads/publications/Wheat%20Production%20Technology.pdf", "note": "KP Agri Dept — Wheat Production Technology (official)"}],
    "parc": [{"link": "http://www.parc.gov.pk/index.php/en/faq-s/60-faqs/270-faqs-wheat", "note": "PARC wheat FAQ"}],
    "tarnab":[{"link": "https://www.researchgate.net/publication/280722592", "note": "ARI Tarnab sowing-date/seed-rate study"}],
    "rust": [{"link": "https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2024.1494566/full", "note": "stripe-rust resistance in recent Pakistani cultivars"}],
    "none": [{"link": "[NEEDS SOURCE]", "note": "confirm with ARI Tarnab / KP Agri Dept"}],
}

def E(id, code, cat, stage, urg, ur, rom, conf, src, slots=None, speech=None):
    e = {"id": id, "code": code, "category": cat, "crop_stage": stage, "urgency": urg,
         "text": {"ur": ur, "roman_ur": rom}, "sources": src, "confidence": conf, "status": "draft"}
    if slots: e["slots"] = slots
    if speech: e["speech_text"] = speech
    return e

entries = [
    # ---- VARIETY (rust-resistant is the headline decision) ----
    E(1,"KPW-VAR-001","variety","sowing","advice",
      "پیلا کنگی (یلو رسٹ) برداشت کرنے والی منظور شدہ قسم کاشت کریں۔",
      "Peela kangi (yellow rust) bardasht karnay wali manzoor-shuda qism kaasht karein.",
      "high", S["rust"]),
    E(2,"KPW-VAR-002","variety","sowing","advice",
      "صرف ایک حساس قسم پر انحصار نہ کریں؛ تازہ منظور شدہ مزاحم قسم چنیں۔",
      "Sirf aik hassaas qism par inhisaar na karein; taaza manzoor-shuda muzahim qism chunein.",
      "medium", S["rust"]),

    # ---- SOWING / LAND PREP (timely sowing = the season's message) ----
    E(3,"KPW-SOW-001","sowing","sowing","advice",
      "کاشت سے پہلے کھیت اچھی طرح ہموار کریں اور گوبر کی کھاد ڈالیں۔",
      "Kaasht se pehlay khet achhi tarah hamwaar karein aur gobar ki khaad daalein.",
      "high", S["kp"]),
    E(4,"KPW-SOW-002","sowing","sowing","warning",
      "گندم وقت پر کاشت کریں (پچیس اکتوبر سے پندرہ نومبر)؛ دیر سے کاشت پیداوار کم کرتی ہے۔",
      "Gandum waqt par kaasht karein (25 October se 15 November); der se kaasht paidawar kam karti hai.",
      "high", S["kp"]),
    E(5,"KPW-SOW-003","sowing","sowing","warning",
      "بیس نومبر کے بعد ہر دن کی تاخیر پیداوار گھٹاتی ہے؛ جلد کاشت کریں۔",
      "20 November ke baad har din ki taakheer paidawar ghataati hai; jald kaasht karein.",
      "high", S["tarnab"]),
    E(6,"KPW-SOW-004","sowing","sowing","advice",
      "چھٹے کے بجائے ڈرل سے کاشت کریں؛ فصل یکساں اور بیج کم لگتا ہے۔",
      "Chhittay ke bajaye drill se kaasht karein; fasal yaksaan aur beej kam lagta hai.",
      "high", S["kp"]),

    # ---- SEED ----
    E(7,"KPW-SED-001","seed","sowing","advice",
      "تصدیق شدہ قسم کا بیج استعمال کریں۔",
      "Tasdeeq-shuda qism ka beej istemal karein.",
      "medium", S["kp"]),
    E(8,"KPW-SED-002","seed","sowing","advice",
      "بیج کا علاج کریں تاکہ کنڈوا اور دیمک سے بچاؤ ہو۔",
      "Beej ka ilaaj karein taakay kandwa aur deemak se bachao ho.",
      "medium", S["kp"]),

    # ---- FERTILIZER ----
    E(9,"KPW-FRT-001","fertilizer","sowing","advice",
      "کاشت کے وقت ڈی اے پی (فاسفورس) ڈالیں؛ اس سے جڑیں اور پھٹاؤ مضبوط ہوتے ہیں۔",
      "Kaasht ke waqt DAP (phosphorus) daalein; is se jaren aur phutao mazboot hotay hain.",
      "medium", S["parc"]),
    E(10,"KPW-FRT-002","fertilizer","any","advice",
      "نائٹروجن ایک ساتھ نہیں، دو بار میں ڈالیں اور مٹی کے ٹیسٹ کے مطابق رکھیں۔",
      "Nitrogen aik saath nahin, do baar mein daalein aur mitti ke test ke mutabiq rakhein.",
      "medium", S["parc"]),
    E(11,"KPW-FRT-003","fertilizer","any","advice",
      "نائٹروجن ضرورت سے زیادہ نہ ڈالیں؛ اس سے پیلا کنگی بڑھتا ہے۔",
      "Nitrogen zaroorat se zyada na daalein; is se peela kangi barhta hai.",
      "medium", S["rust"]),

    # ---- IRRIGATION ----
    E(12,"KPW-IRR-001","irrigation","vegetative","advice",
      "پہلا پانی کاشت کے بیس پچیس دن بعد (جڑ بننے پر) دیں۔",
      "Pehla pani kaasht ke 20-25 din baad (jar bannay par) dein.",
      "medium", S["parc"]),
    E(13,"KPW-IRR-002","irrigation","any","advice",
      "پھٹاؤ، گابھے اور دانہ بننے کے وقت پانی کی کمی نہ ہونے دیں۔",
      "Phutao, gaabhay aur dana bannay ke waqt pani ki kami na honay dein.",
      "high", S["parc"]),
    E(14,"KPW-IRR-003","irrigation","any","advice",
      "تیز بارش میں کھیت سے فالتو پانی نکالنے کا بندوبست رکھیں۔",
      "Tez barish mein khet se faltu pani nikaalnay ka bandobast rakhein.",
      "low", S["none"]),

    # ---- WEEDS ----
    E(15,"KPW-WED-001","weeds","vegetative","advice",
      "جڑی بوٹیاں (جنگلی جئی وغیرہ) شروع میں ہی قابو کریں؛ یہ گندم کی غذا لے جاتی ہیں۔",
      "Jari bootiyan (jangli jai waghaira) shuru mein hi qaboo karein; ye gandum ki ghiza le jaati hain.",
      "high", S["parc"]),
    E(16,"KPW-WED-002","weeds","vegetative","advice",
      "جڑی بوٹیوں کی دوا بروقت اور لیبل کے مطابق استعمال کریں؛ افسر سے مشورہ کریں۔",
      "Jari bootiyon ki dawa barwaqt aur label ke mutabiq istemal karein; officer se mashwara karein.",
      "medium", S["none"]),

    # ---- DISEASE (yellow rust is the headline) ----
    E(17,"KPW-DIS-001","disease_alert","vegetative","urgent",
      "پتوں پر پیلے دھاری دار دھبے (پیلا کنگی) نظر آئیں تو فوراً زرعی افسر سے رجوع کریں۔",
      "Patton par peelay dhaari-daar dhabbay (peela kangi) nazar aayein to foran zarai officer se rujoo karein.",
      "high", S["rust"]),
    E(18,"KPW-DIS-002","disease_alert","vegetative","warning",
      "سردی اور دھند میں پیلا کنگی بڑھتا ہے؛ گابھے سے پہلے فصل کا معائنہ کریں۔",
      "Sardi aur dhund mein peela kangi barhta hai; gaabhay se pehlay fasal ka moaina karein.",
      "high", S["rust"]),
    E(19,"KPW-DIS-003","disease_alert","any","advice",
      "پیلا کنگی سے بچاؤ کے لیے زیادہ نائٹروجن نہ ڈالیں اور مزاحم قسم لگائیں۔",
      "Peela kangi se bachao ke liye zyada nitrogen na daalein aur muzahim qism lagayein.",
      "high", S["rust"]),
    E(20,"KPW-DIS-004","disease_alert","vegetative","warning",
      "پتوں پر بھورے نارنجی دھبے (بھوری کنگی) ہوں تو معائنہ کریں اور افسر سے مشورہ کریں۔",
      "Patton par bhooray narangi dhabbay (bhoori kangi) hon to moaina karein aur officer se mashwara karein.",
      "medium", S["rust"]),
    E(21,"KPW-DIS-005","disease_alert","sowing","advice",
      "کھلی کنڈوا سے بچاؤ کے لیے علاج شدہ اور تصدیق شدہ بیج استعمال کریں۔",
      "Khuli kandwa se bachao ke liye ilaaj-shuda aur tasdeeq-shuda beej istemal karein.",
      "medium", S["kp"]),

    # ---- PEST ALERTS ----
    E(22,"KPW-PST-001","pest_alert","any","advice",
      "ہر ہفتے کھیت دیکھیں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔",
      "Har haftay khet dekhein; keeron ki tadaad dekh kar hi spray karein.",
      "high", S["none"]),
    E(23,"KPW-PST-002","pest_alert","any","advice",
      "پتوں اور بالوں پر چیپا (ایفڈ) جمع ہو تو معائنہ کریں اور مددگار کیڑے بچائیں۔",
      "Patton aur baalon par cheepa (aphid) jama ho to moaina karein aur madadgaar keeray bachayein.",
      "low", S["none"]),
    E(24,"KPW-PST-003","pest_alert","vegetative","warning",
      "دیمک سے پودے مرجھائیں تو بیج یا زمین کا علاج کریں اور کھیت سے کچرا ہٹائیں۔",
      "Deemak se poday murjhaayein to beej ya zameen ka ilaaj karein aur khet se kachra hataayein.",
      "medium", S["kp"]),
    E(25,"KPW-PST-004","pest_alert","any","warning",
      "فوجی سنڈی پتے کھا جائے تو رات کو معائنہ کریں اور افسر سے رجوع کریں۔",
      "Fouji sundi pattay kha jaye to raat ko moaina karein aur officer se rujoo karein.",
      "low", S["none"]),
    E(26,"KPW-PST-005","pest_alert","any","advice",
      "لیڈی برڈ جیسے مددگار کیڑوں کو بچائیں؛ یہ چیپا کھاتے ہیں۔",
      "Lady bird jaisay madadgaar keeron ko bachayein; ye cheepa khatay hain.",
      "medium", S["none"]),

    # ---- WEATHER (templated) ----
    E(27,"KPW-WEA-001","weather_alert","any","warning",
      "اگلے {days} دنوں میں تیز بارش متوقع ہے؛ آبپاشی اور کھاد ڈالنا روک دیں۔",
      "Aglay {days} dinon mein tez barish mutawaqqa hai; aabpashi aur khaad daalna rok dein.",
      "medium", S["none"],
      slots=[{"name":"days","type":"int","min":1,"max":7}]),
    E(28,"KPW-WEA-002","weather_alert","harvest","warning",
      "بارش یا اولوں کا خطرہ ہے؛ پکی فصل بروقت کاٹیں اور ڈھانپ کر خشک رکھیں۔",
      "Barish ya olon ka khatra hai; pakki fasal barwaqt kaatein aur dhaanp kar khushk rakhein.",
      "low", S["none"]),
    E(29,"KPW-WEA-003","weather_alert","vegetative","advice",
      "دھند اور نمی میں پیلا کنگی تیزی سے پھیلتا ہے؛ معائنہ بڑھا دیں۔",
      "Dhund aur nami mein peela kangi tezi se phailta hai; moaina barha dein.",
      "high", S["rust"]),

    # ---- HARVEST / STORAGE ----
    E(30,"KPW-HRV-001","harvest","harvest","advice",
      "جب دانہ سخت اور بھوسہ پیلا ہو جائے تو کٹائی کریں۔",
      "Jab dana sakht aur bhoosa peela ho jaye to katai karein.",
      "high", S["kp"]),
    E(31,"KPW-HRV-002","harvest","harvest","advice",
      "پکنے پر بروقت کٹائی کریں تاکہ دانہ جھڑنے سے نقصان نہ ہو۔",
      "Paknay par barwaqt katai karein taakay dana jharnay se nuqsaan na ho.",
      "high", S["kp"]),
    E(32,"KPW-HRV-003","harvest","harvest","advice",
      "گہائی کی جگہ صاف رکھیں تاکہ دانہ صاف اور ملاوٹ سے پاک رہے۔",
      "Gahai ki jagah saaf rakhein taakay dana saaf aur milaawat se paak rahay.",
      "medium", S["none"]),
    E(33,"KPW-STO-001","storage","harvest","advice",
      "دانہ اچھی طرح خشک کر کے صاف اور بند جگہ رکھیں؛ گودام کے کیڑوں سے بچائیں۔",
      "Dana achhi tarah khushk kar ke saaf aur band jagah rakhein; godaam ke keeron se bachayein.",
      "low", S["none"]),

    # ---- SAFETY ----
    E(34,"KPW-SAF-001","safety","any","warning",
      "سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔",
      "Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.",
      "medium", S["none"]),
    E(35,"KPW-SAF-002","safety","any","warning",
      "ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔",
      "Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.",
      "medium", S["none"]),
    E(36,"KPW-SAF-003","safety","any","warning",
      "سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔",
      "Spray ke baad haath aur mooh dhoyein aur kapray badlein.",
      "medium", S["none"]),
    E(37,"KPW-SAF-004","safety","any","warning",
      "زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔",
      "Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.",
      "medium", S["none"]),
    E(38,"KPW-SAF-005","safety","any","urgent",
      "زہر لگنے کی علامت (متلی، چکر) پر فوراً طبی مدد لیں اور دوا کا لیبل ساتھ لے جائیں۔",
      "Zehr lagnay ki alamat (matli, chakkar) par foran tibbi madad lein aur dawa ka label saath le jayein.",
      "medium", S["none"]),
    E(39,"KPW-SAF-006","safety","harvest","warning",
      "سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے کٹائی نہ کریں۔",
      "Spray ke baad label par diye gaye waqfay se pehlay katai na karein.",
      "medium", S["none"]),
]

doc = {"format_version": 2, "dictionary_id": 3, "code": CODE,
       "region": "kpk", "crop": "wheat", "dictionary_version": 1,
       "languages": ["ur", "roman_ur"], "entries": entries}

with open("dictionaries/kpk_wheat_v2.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

from collections import Counter
print(f"entries: {len(entries)}")
print("by category:", dict(Counter(e["category"] for e in entries)))
print("by confidence:", dict(Counter(e["confidence"] for e in entries)))
