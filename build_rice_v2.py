"""
D2 — build the v2 sindh_rice dictionary from the R1 (sindh_rice) brief.

Honest rules: all status="draft"; no pesticide doses; numbers only where sourced
(BPH ~10-15/hill, blast 3-5 lesions/leaf, harvest 85-95% straw panicles); Sindhi is
NOT included (unreliable to auto-translate) and is left for a native speaker — the
draft ships Urdu + Roman Urdu only. Not padded to 60.
"""
import json

CODE = "SNR"
S = {
    "parc": [{"link": "http://www.parc.gov.pk/index.php/en/faq-s/60-faqs/73-rice", "note": "PARC rice FAQ — official"}],
    "policy": [{"link": "https://api.gov.pk/SiteImage/Policy/Rice%20Policy%202022-23.pdf", "note": "Govt Rice Policy 2022-23 (Sindh)"}],
    "etl": [{"link": "https://niphm.gov.in/IPMPackages/Rice.pdf", "note": "rice ETLs (India pkg) — confirm for Pakistan"}],
    "pakrev": [{"link": "https://sciencepublishinggroup.com/article/10.11648/j.aje.20250901.12", "note": "Pakistan rice pest review"}],
    "mgmt": [{"link": "https://austinpublishinggroup.com/ebooks/food-security/chapters/Rice-Production-1006.pdf", "note": "Pakistan rice pest/disease mgmt"}],
    "none": [{"link": "[NEEDS SOURCE]", "note": "pull RRI-Dokri / Sindh Agri Dept leaflet"}],
}

def E(id, code, cat, stage, urg, ur, rom, conf, src, slots=None, speech=None):
    e = {"id": id, "code": code, "category": cat, "crop_stage": stage, "urgency": urg,
         "text": {"ur": ur, "roman_ur": rom}, "sources": src, "confidence": conf, "status": "draft"}
    if slots: e["slots"] = slots
    if speech: e["speech_text"] = speech
    return e

entries = [
    # ---- WATER / IRRIGATION (the central safe lever for rice) ----
    E(1,"SNR-IRR-001","irrigation","any","advice",
      "پانی کھیت میں مسلسل کھڑا نہ رہنے دیں؛ باری باری سکھائیں، اس سے بھوری پھدکی کم ہوتی ہے۔",
      "Pani khet mein musalsal khara na rehnay dein; baari baari sukhayein, is se bhoori phudki kam hoti hai.",
      "high", S["mgmt"]),
    E(2,"SNR-IRR-002","irrigation","flowering","advice",
      "پھول اور دانہ بننے کے وقت کھیت میں مناسب پانی رکھیں۔",
      "Phool aur dana bannay ke waqt khet mein munasib pani rakhein.",
      "medium", S["parc"]),
    E(3,"SNR-IRR-003","irrigation","harvest","advice",
      "کٹائی سے پہلے کھیت کا پانی نکال دیں تاکہ زمین سخت ہو اور کٹائی آسان ہو۔",
      "Katai se pehlay khet ka pani nikaal dein taakay zameen sakht ho aur katai aasan ho.",
      "medium", S["none"]),

    # ---- FERTILIZER ----
    E(4,"SNR-FRT-001","fertilizer","any","advice",
      "کھاد مٹی کے ٹیسٹ کے مطابق ڈالیں اور زرعی افسر سے مشورہ کریں۔",
      "Khaad mitti ke test ke mutabiq daalein aur zarai officer se mashwara karein.",
      "medium", S["none"]),
    E(5,"SNR-FRT-002","fertilizer","any","advice",
      "نائٹروجن ایک ساتھ نہیں، دو تین بار میں ڈالیں: پنیری لگاتے وقت، پینتیس دن بعد، اور پھول سے پہلے۔",
      "Nitrogen aik saath nahin, 2-3 baar mein daalein: paneeri lagatay waqt, 35 din baad, aur phool se pehlay.",
      "high", S["parc"]),
    E(6,"SNR-FRT-003","fertilizer","any","advice",
      "نائٹروجن ضرورت سے زیادہ نہ ڈالیں؛ اس سے بھوری پھدکی، بلاسٹ اور جھلساؤ بڑھتے ہیں۔",
      "Nitrogen zaroorat se zyada na daalein; is se bhoori phudki, blast aur jhulsao barhtay hain.",
      "high", S["mgmt"]),

    # ---- VARIETY / NURSERY / SOWING / SEED ----
    E(7,"SNR-VAR-001","variety","sowing","advice",
      "بلاسٹ اور بیکٹیریل جھلساؤ برداشت کرنے والی منظور شدہ قسم چنیں۔",
      "Blast aur bacterial jhulsao bardasht karnay wali manzoor-shuda qism chunein.",
      "medium", S["mgmt"]),
    E(8,"SNR-SOW-001","sowing","sowing","advice",
      "پنیری پچیس سے پینتیس دن میں لگائیں؛ زیادہ پرانی پنیری پیداوار کم کرتی ہے۔",
      "Paneeri 25-35 din mein lagayein; zyada purani paneeri paidawar kam karti hai.",
      "high", S["parc"]),
    E(9,"SNR-SOW-002","sowing","sowing","advice",
      "وقت پر کاشت کریں؛ جلد کاشت تنا چھیدک کیڑے سے بچاتی ہے۔",
      "Waqt par kaasht karein; jald kaasht tana chhedak keeray se bachati hai.",
      "medium", S["pakrev"]),
    E(10,"SNR-SOW-003","sowing","sowing","advice",
      "ہر جگہ دو پنیری لگائیں تاکہ فصل اچھی کھڑی ہو۔",
      "Har jagah do paneeri lagayein taakay fasal achhi khari ho.",
      "medium", S["parc"]),
    E(11,"SNR-SED-001","seed","sowing","advice",
      "تصدیق شدہ بیج استعمال کریں اور بیج کا علاج کریں۔",
      "Tasdeeq-shuda beej istemal karein aur beej ka ilaaj karein.",
      "low", S["none"]),

    # ---- WEEDS ----
    E(12,"SNR-WED-001","weeds","any","advice",
      "پنیری اور کھیت کو جڑی بوٹیوں سے پاک رکھیں تاکہ غذا اور پانی فصل کو ملے۔",
      "Paneeri aur khet ko jari bootiyon se paak rakhein taakay ghiza aur pani fasal ko milay.",
      "medium", S["none"]),

    # ---- PEST ALERTS ----
    E(13,"SNR-PST-001","pest_alert","any","advice",
      "ہر ہفتے کھیت دیکھیں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔",
      "Har haftay khet dekhein; keeron ki tadaad dekh kar hi spray karein.",
      "high", S["etl"]),
    E(14,"SNR-PST-002","pest_alert","vegetative","warning",
      "نئی فصل میں بیچ کا شگوفہ سوکھ جائے تو تنا چھیدک کا حملہ ہے؛ افسر سے مشورہ کریں۔",
      "Nai fasal mein beech ka shiguufa sookh jaye to tana chhedak ka hamla hai; officer se mashwara karein.",
      "medium", S["etl"]),
    E(15,"SNR-PST-003","pest_alert","harvest","advice",
      "کٹائی کے بعد مڈھ اور پرالی کھیت میں دبا دیں؛ اس سے تنا چھیدک کے کیڑے مر جاتے ہیں۔",
      "Katai ke baad mandh aur parali khet mein daba dein; is se tana chhedak ke keeray mar jatay hain.",
      "high", S["pakrev"]),
    E(16,"SNR-PST-004","pest_alert","tillering","warning",
      "بھوری پھدکی سے پتے پیلے بھورے ہوں تو پانی کھڑا نہ رکھیں اور افسر سے رجوع کریں۔",
      "Bhoori phudki se pattay peelay bhooray hon to pani khara na rakhein aur officer se rujoo karein.",
      "high", S["mgmt"]),
    E(17,"SNR-PST-005","pest_alert","tillering","warning",
      "اگر بھوری پھدکی فی بوٹا دس پندرہ سے زیادہ ہو تو افسر سے مشورہ کر کے عمل کریں۔",
      "Agar bhoori phudki fi boota 10-15 se zyada ho to officer se mashwara kar ke amal karein.",
      "medium", S["etl"]),
    E(18,"SNR-PST-006","pest_alert","vegetative","advice",
      "پتے لپٹے اور دھاگے سے جڑے ہوں تو پتہ لپیٹ کیڑا ہے؛ معائنہ کریں اور مددگار کیڑے بچائیں۔",
      "Pattay liptay aur dhaagay se juray hon to patta lapet keera hai; moaina karein aur madadgaar keeray bachayein.",
      "medium", S["mgmt"]),
    E(19,"SNR-PST-007","pest_alert","any","advice",
      "مکڑی اور لیڈی برڈ جیسے مددگار کیڑوں کو بچائیں؛ یہ پھدکیاں کھاتے ہیں۔",
      "Makri aur lady bird jaisay madadgaar keeron ko bachayein; ye phudkiyan khatay hain.",
      "medium", S["mgmt"]),
    E(20,"SNR-PST-008","pest_alert","any","advice",
      "غیر ضروری سپرے سے گریز کریں؛ اس سے بھوری پھدکی اور بڑھ سکتی ہے۔",
      "Ghair-zaroori spray se gurez karein; is se bhoori phudki aur barh sakti hai.",
      "medium", S["mgmt"]),
    E(21,"SNR-PST-009","pest_alert","any","advice",
      "پتوں پر سفید دھاریاں یا شگوفوں میں گال نظر آئیں تو معائنہ کریں اور افسر سے رجوع کریں۔",
      "Patton par safaid dhaariyan ya shigufon mein gall nazar aayein to moaina karein aur officer se rujoo karein.",
      "low", S["pakrev"]),

    # ---- DISEASE ALERTS ----
    E(22,"SNR-DIS-001","disease_alert","vegetative","warning",
      "پتوں پر بلاسٹ کے نوکدار دھبے ہوں تو زیادہ نائٹروجن نہ ڈالیں اور افسر سے مشورہ کریں۔",
      "Patton par blast ke nokdaar dhabbay hon to zyada nitrogen na daalein aur officer se mashwara karein.",
      "medium", S["etl"]),
    E(23,"SNR-DIS-002","disease_alert","vegetative","warning",
      "اگر فی پتہ تین سے پانچ بلاسٹ کے دھبے ہوں تو افسر سے رجوع کریں۔",
      "Agar fi patta 3 se 5 blast ke dhabbay hon to officer se rujoo karein.",
      "medium", S["etl"]),
    E(24,"SNR-DIS-003","disease_alert","vegetative","warning",
      "بیکٹیریل جھلساؤ میں پتوں کے کنارے پیلے ہو کر سوکھیں؛ نائٹروجن کم کریں اور متاثرہ باقیات ہٹائیں۔",
      "Bacterial jhulsao mein patton ke kinaray peelay ho kar sookhein; nitrogen kam karein aur mutasira baqiyaat hataayein.",
      "medium", S["mgmt"]),
    E(25,"SNR-DIS-004","disease_alert","flowering","advice",
      "پتے کی نیام پر خاکستری دھبے ہوں تو بوائی گھنی نہ کریں اور ہوا کا گزر رکھیں۔",
      "Pattay ki niyaam par khaakistari dhabbay hon to bouai ghani na karein aur hawa ka guzar rakhein.",
      "low", S["mgmt"]),
    E(26,"SNR-DIS-005","disease_alert","vegetative","warning",
      "ٹنگرو سے پودے بونے اور نارنجی پیلے ہوں تو متاثرہ پودے نکالیں اور سبز تیلے کو قابو کریں۔",
      "Tungro se poday bonay aur narangi peelay hon to mutasira poday nikaalein aur sabz teelay ko qaboo karein.",
      "low", S["mgmt"]),
    E(27,"SNR-DIS-006","disease_alert","harvest","advice",
      "کٹائی کے بعد پرالی اور مڈھ کھیت میں دبا دیں تاکہ بیماریاں کم ہوں۔",
      "Katai ke baad parali aur mandh khet mein daba dein taakay bimariyan kam hon.",
      "medium", S["mgmt"]),

    # ---- WEATHER (templated) ----
    E(28,"SNR-WEA-001","weather_alert","any","warning",
      "اگلے {days} دنوں میں تیز بارش متوقع ہے؛ کھیت سے فالتو پانی نکالیں اور کھاد ڈالنا روک دیں۔",
      "Aglay {days} dinon mein tez barish mutawaqqa hai; khet se faltu pani nikaalein aur khaad daalna rok dein.",
      "medium", S["none"],
      slots=[{"name":"days","type":"int","min":1,"max":7}]),
    E(29,"SNR-WEA-002","weather_alert","harvest","warning",
      "بارش متوقع ہے؛ پکی فصل بروقت کاٹیں اور کٹی فصل ڈھانپ کر خشک رکھیں۔",
      "Barish mutawaqqa hai; pakki fasal barwaqt kaatein aur kati fasal dhaanp kar khushk rakhein.",
      "low", S["none"]),
    E(30,"SNR-WEA-003","weather_alert","tillering","advice",
      "گرمی اور کھڑے پانی میں بھوری پھدکی بڑھتی ہے؛ پانی باری باری سکھائیں اور معائنہ بڑھائیں۔",
      "Garmi aur kharay pani mein bhoori phudki barhti hai; pani baari baari sukhayein aur moaina barhayein.",
      "medium", S["mgmt"]),

    # ---- HARVEST / STORAGE ----
    E(31,"SNR-HRV-001","harvest","harvest","advice",
      "جب پچاسی سے پچانوے فیصد بالیاں بھوسے کے رنگ کی ہو جائیں تو کٹائی کریں۔",
      "Jab 85 se 95 percent baliyan bhoosay ke rang ki ho jayein to katai karein.",
      "high", S["parc"]),
    E(32,"SNR-HRV-002","harvest","harvest","advice",
      "کٹی ہوئی فصل دو تین دن کھیت میں خشک ہونے دیں، پھر گہائی کریں۔",
      "Kati hui fasal 2-3 din khet mein khushk honay dein, phir gahai karein.",
      "high", S["parc"]),
    E(33,"SNR-HRV-003","harvest","harvest","advice",
      "صبح کٹائی کریں اور گہائی کی جگہ صاف رکھیں تاکہ دانہ صاف رہے۔",
      "Subah katai karein aur gahai ki jagah saaf rakhein taakay dana saaf rahay.",
      "medium", S["parc"]),
    E(34,"SNR-HRV-004","harvest","harvest","advice",
      "بیج والی فصل کمبائن سے نہ کاٹیں تاکہ قسمیں آپس میں نہ ملیں۔",
      "Beej wali fasal combine se na kaatein taakay qismein aapas mein na milein.",
      "medium", S["parc"]),
    E(35,"SNR-STO-001","storage","harvest","advice",
      "دانہ اچھی طرح خشک کر کے صاف اور خشک جگہ رکھیں؛ نمی سے بچائیں۔",
      "Dana achhi tarah khushk kar ke saaf aur khushk jagah rakhein; nami se bachayein.",
      "low", S["none"]),

    # ---- SAFETY ----
    E(36,"SNR-SAF-001","safety","any","warning",
      "سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔",
      "Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.",
      "medium", S["none"]),
    E(37,"SNR-SAF-002","safety","any","warning",
      "ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔",
      "Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.",
      "medium", S["none"]),
    E(38,"SNR-SAF-003","safety","any","warning",
      "سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔",
      "Spray ke baad haath aur mooh dhoyein aur kapray badlein.",
      "medium", S["none"]),
    E(39,"SNR-SAF-004","safety","any","warning",
      "زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔",
      "Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.",
      "medium", S["none"]),
    E(40,"SNR-SAF-005","safety","any","urgent",
      "زہر لگنے کی علامت (متلی، چکر) پر فوراً طبی مدد لیں اور دوا کا لیبل ساتھ لے جائیں۔",
      "Zehr lagnay ki alamat (matli, chakkar) par foran tibbi madad lein aur dawa ka label saath le jayein.",
      "medium", S["none"]),
    E(41,"SNR-SAF-006","safety","harvest","warning",
      "سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے کٹائی نہ کریں۔",
      "Spray ke baad label par diye gaye waqfay se pehlay katai na karein.",
      "medium", S["none"]),
]

doc = {"format_version": 2, "dictionary_id": 2, "code": CODE,
       "region": "sindh", "crop": "rice", "dictionary_version": 1,
       "languages": ["ur", "roman_ur"], "entries": entries}

with open("dictionaries/sindh_rice_v2.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

from collections import Counter
print(f"entries: {len(entries)}")
print("by category:", dict(Counter(e["category"] for e in entries)))
print("by confidence:", dict(Counter(e["confidence"] for e in entries)))
