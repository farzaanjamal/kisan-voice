"""KPK maize v2 — built from the maize R1 brief. FAW front and centre; harvest/storage
weighted for the Oct season. All draft; no doses; Pashto left to a native speaker.
Emits dictionary + expert/native review sheets + coverage note."""
import csv, json
from collections import Counter
from pathlib import Path

CODE, DID = "KPM", 8
S = {
 "kp":   [{"link":"https://zarat.kp.gov.pk/assets/uploads/publications/Maize%20Production%20Technology.pdf","note":"KP Maize Production Technology (CCRI Pirsabak) — official"}],
 "toa":  [{"link":"https://www.timesofagriculture.pk/maize-production-in-pakistan/","note":"maize sowing windows / IPM"}],
 "faw":  [{"link":"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12027892/","note":"fall armyworm in Pakistan (study)"}],
 "mgmt": [{"link":"https://www.khethari.com/blogs/news/pests-and-diseases-of-maize-a-complete-guide-for-farmers","note":"maize pests/diseases guide — verify CCRI Pirsabak"}],
 "none": [{"link":"[NEEDS SOURCE]","note":"confirm with CCRI Pirsabak / KP Agri Dept"}],
}
rows = []
def E(i,c,cat,st,u,ur,ro,cf,sr,gl,sl=None): rows.append((i,c,cat,st,u,ur,ro,cf,sr,gl,sl))

E(1,"KPM-VAR-001","variety","sowing","advice","منظور شدہ مکئی کی قسم کاشت کریں (مثلاً اعظم، جلال، پہاڑی)۔","Manzoor-shuda makai ki qism kaasht karein (misaal: Azam, Jalal, Pahari).","medium",S["kp"],"Plant an approved maize variety (e.g. Azam, Jalal, Pahari)")
E(2,"KPM-VAR-002","variety","sowing","advice","صحت مند اور تصدیق شدہ بیج چنیں؛ بیمار بھٹوں سے بیج نہ رکھیں۔","Sehatmand aur tasdeeq-shuda beej chunein; bimaar bhutton se beej na rakhein.","medium",S["kp"],"Choose healthy certified seed; don't keep seed from diseased cobs")
E(3,"KPM-SOW-001","sowing","sowing","warning","مکئی مقررہ وقت پر کاشت کریں؛ دیر سے کاشت پیداوار کم کرتی ہے۔","Makai muqarrara waqt par kaasht karein; der se kaasht paidawar kam karti hai.","high",S["toa"],"Sow maize at the recommended time; late sowing cuts yield")
E(4,"KPM-SOW-002","sowing","sowing","warning","ساتھ والے کھیتوں میں مختلف اوقات پر کاشت نہ کریں؛ اس سے فال آرمی ورم پھیلتا ہے۔","Saath walay kheton mein mukhtalif auqaat par kaasht na karein; is se fall armyworm phailta hai.","high",S["kp"],"Don't sow adjacent fields at different times - it spreads fall armyworm")
E(5,"KPM-SOW-003","sowing","harvest","advice","فصل کے بعد گہری ہل چلائیں تاکہ زمین میں چھپے کیڑے باہر آ کر مر جائیں۔","Fasal ke baad gehri hal chalayein taakay zameen mein chhupay keeray bahar aa kar mar jayein.","high",S["kp"],"Deep-plough after the crop to expose and kill soil-hidden pests")
E(6,"KPM-SED-001","seed","sowing","advice","تصدیق شدہ بیج استعمال کریں۔","Tasdeeq-shuda beej istemal karein.","medium",S["kp"],"Use certified seed")
E(7,"KPM-SED-002","seed","sowing","advice","بیج کا علاج کریں تاکہ شوٹ فلائی، تنا چھیدک اور شروع میں فال آرمی ورم سے بچاؤ ہو۔","Beej ka ilaaj karein taakay shoot fly, tana chhedak aur shuru mein fall armyworm se bachao ho.","medium",S["kp"],"Treat seed against shoot fly, stem borer and early fall armyworm")
E(8,"KPM-FRT-001","fertilizer","any","advice","کھاد مٹی کے ٹیسٹ کے مطابق ڈالیں اور زرعی افسر سے مشورہ کریں۔","Khaad mitti ke test ke mutabiq daalein aur zarai officer se mashwara karein.","medium",S["none"],"Fertilise per soil test; consult officer")
E(9,"KPM-FRT-002","fertilizer","any","advice","مکئی کو نائٹروجن زیادہ چاہیے؛ اسے دو تین بار میں ڈالیں۔","Makai ko nitrogen zyada chahiye; ise 2-3 baar mein daalein.","high",S["kp"],"Maize needs plenty of nitrogen - apply it in 2-3 splits")
E(10,"KPM-FRT-003","fertilizer","sowing","advice","کاشت کے وقت ڈی اے پی (فاسفورس) ڈالیں تاکہ جڑیں مضبوط ہوں۔","Kaasht ke waqt DAP (phosphorus) daalein taakay jaren mazboot hon.","medium",S["none"],"Apply DAP (phosphorus) at sowing for strong roots")
E(11,"KPM-IRR-001","irrigation","flowering","warning","بال اور ریشہ آنے کے وقت پانی کی کمی نہ ہونے دیں؛ یہی سب سے نازک وقت ہے۔","Baal aur resha aanay ke waqt pani ki kami na honay dein; yehi sab se naazuk waqt hai.","high",S["kp"],"No water shortage at silking - the most critical stage")
E(12,"KPM-IRR-002","irrigation","any","advice","ہر نازک مرحلے (گھٹنے تک، پھول اور بال) پر مناسب پانی دیں۔","Har naazuk marhalay (ghutnay tak, phool aur baal) par munasib pani dein.","medium",S["kp"],"Water adequately at each critical stage (knee-high, tasseling, silking)")
E(13,"KPM-IRR-003","irrigation","any","advice","تیز بارش میں کھیت سے فالتو پانی نکالنے کا بندوبست رکھیں۔","Tez barish mein khet se faltu pani nikaalnay ka bandobast rakhein.","low",S["none"],"Arrange drainage for heavy rain")
E(14,"KPM-WED-001","weeds","vegetative","advice","پہلے چار چھ ہفتوں میں جڑی بوٹیاں ختم کریں؛ یہ مکئی کی غذا لے جاتی ہیں۔","Pehlay 4-6 hafton mein jari bootiyan khatam karein; ye makai ki ghiza le jaati hain.","high",S["toa"],"Remove weeds in the first 4-6 weeks - they steal maize's nutrients")
E(15,"KPM-WED-002","weeds","any","advice","کھیت کے کنارے اور اردگرد کی بوٹیاں بھی صاف رکھیں؛ یہ کیڑوں کا ٹھکانہ ہیں۔","Khet ke kinaray aur ird-gird ki bootiyan bhi saaf rakhein; ye keeron ka thikana hain.","medium",S["kp"],"Keep field borders weed-free too - they harbour pests")
E(16,"KPM-PST-001","pest_alert","any","advice","ہر ہفتے کھیت دیکھیں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔","Har haftay khet dekhein; keeron ki tadaad dekh kar hi spray karein.","high",S["none"],"Scout weekly; spray only on pest counts")
E(17,"KPM-PST-002","pest_alert","vegetative","warning","فال آرمی ورم سے پتوں پر سوراخ اور گوبھ میں بھورا برادہ نظر آئے تو انڈے اور سنڈیاں ہاتھ سے چن کر تلف کریں۔","Fall armyworm se patton par suraakh aur gobh mein bhoora burada nazar aaye to anday aur sundiyan haath se chun kar talaf karein.","high",S["kp"],"FAW: ragged leaf holes + sawdust frass in whorl -> hand-pick & destroy egg masses/larvae")
E(18,"KPM-PST-003","pest_alert","vegetative","urgent","فال آرمی ورم کا حملہ زیادہ ہو تو زرعی افسر سے مشورہ کر کے عمل کریں۔","Fall armyworm ka hamla zyada ho to zarai officer se mashwara kar ke amal karein.","high",S["faw"],"Heavy FAW attack -> consult officer before acting")
E(19,"KPM-PST-004","pest_alert","vegetative","warning","نئی فصل میں مرکزی شگوفہ سوکھ جائے (ڈیڈ ہارٹ) تو تنا چھیدک کا حملہ ہے؛ افسر سے رجوع کریں۔","Nai fasal mein markazi shiguufa sookh jaye (dead heart) to tana chhedak ka hamla hai; officer se rujoo karein.","medium",S["mgmt"],"Dead central shoot = stem borer; consult officer")
E(20,"KPM-PST-005","pest_alert","harvest","advice","کٹائی کے بعد مڈھ اور باقیات تلف کریں اور گہری ہل چلائیں؛ اس سے تنا چھیدک کم ہوتا ہے۔","Katai ke baad mandh aur baqiyaat talaf karein aur gehri hal chalayein; is se tana chhedak kam hota hai.","high",S["kp"],"Destroy stubble and deep-plough after harvest -> fewer stem borers")
E(21,"KPM-PST-006","pest_alert","seedling","advice","شوٹ فلائی سے چھوٹے پودوں کا شگوفہ سوکھے تو بیج کے علاج اور بروقت کاشت سے بچاؤ کریں۔","Shoot fly se chhotay podon ka shiguufa sookhay to beej ke ilaaj aur barwaqt kaasht se bachao karein.","medium",S["kp"],"Shoot fly dead-heart in seedlings -> prevent with seed treatment and timely sowing")
E(22,"KPM-PST-007","pest_alert","any","advice","پتوں اور پھول پر تیلا (ایفڈ) جمع ہو تو معائنہ کریں اور مددگار کیڑے بچائیں۔","Patton aur phool par teela (aphid) jama ho to moaina karein aur madadgaar keeray bachayein.","medium",S["mgmt"],"Aphids on leaves/tassel -> scout, protect natural enemies")
E(23,"KPM-PST-008","pest_alert","any","advice","ٹرائیکوگراما اور لیڈی برڈ جیسے مددگار کیڑوں کو بچائیں؛ یہ نقصان دہ کیڑے کھاتے ہیں۔","Trichogramma aur lady bird jaisay madadgaar keeron ko bachayein; ye nuqsaan-deh keeray khatay hain.","medium",S["kp"],"Protect helpful insects (Trichogramma, ladybirds) - they eat pests")
E(24,"KPM-DIS-001","disease_alert","vegetative","warning","پتوں پر لمبے خاکستری سگار نما دھبے (جھلساؤ) ہوں تو مزاحم قسم لگائیں اور مسلسل مکئی نہ کاشت کریں۔","Patton par lambay khaakistari cigar-numa dhabbay (jhulsao) hon to muzahim qism lagayein aur musalsal makai na kaasht karein.","low",S["mgmt"],"Long grey cigar-shaped leaf lesions (blight) -> resistant variety, avoid continuous maize")
E(25,"KPM-DIS-002","disease_alert","flowering","advice","تنے یا بھٹے میں سڑن ہو تو فاصلہ مناسب رکھیں، زیادہ نمی سے بچیں اور بروقت کٹائی کریں۔","Tanay ya bhutte mein sarran ho to faasla munasib rakhein, zyada nami se bachein aur barwaqt katai karein.","low",S["mgmt"],"Stalk/ear rot -> proper spacing, avoid humidity, harvest on time")
E(26,"KPM-DIS-003","disease_alert","flowering","warning","پھول یا بھٹے کی جگہ سیاہ کنڈوا بنے تو متاثرہ پودے نکالیں اور علاج شدہ بیج استعمال کریں۔","Phool ya bhutte ki jagah siyah kandwa banay to mutasira poday nikaalein aur ilaaj-shuda beej istemal karein.","low",S["mgmt"],"Black smut galls on tassel/cob -> remove plants, use treated seed")
E(27,"KPM-DIS-004","disease_alert","any","advice","مکئی کے بعد دوسری فصل کاشت کریں (ردوبدل)؛ مسلسل مکئی بیماریاں بڑھاتی ہے۔","Makai ke baad doosri fasal kaasht karein (radd-o-badal); musalsal makai bimariyan barhati hai.","medium",S["kp"],"Rotate after maize - continuous maize increases disease")
E(28,"KPM-WEA-001","weather_alert","any","warning","اگلے {days} دنوں میں تیز بارش متوقع ہے؛ آبپاشی اور کھاد ڈالنا روک دیں۔","Aglay {days} dinon mein tez barish mutawaqqa hai; aabpashi aur khaad daalna rok dein.","medium",S["none"],"Heavy rain in {days} days -> stop irrigation and fertiliser",[{"name":"days","type":"int","min":1,"max":7}])
E(29,"KPM-WEA-002","weather_alert","any","advice","تیز ہوا یا بارش سے فصل گر سکتی ہے؛ لمبی فصل میں پانی نہ کھڑا کریں اور پکی فصل بروقت کاٹیں۔","Tez hawa ya barish se fasal gir sakti hai; lambi fasal mein pani na khara karein aur pakki fasal barwaqt kaatein.","medium",S["none"],"Wind/rain can lodge the crop -> don't waterlog tall crop, harvest ripe crop promptly")
E(30,"KPM-WEA-003","weather_alert","flowering","advice","بال آنے کے وقت گرمی نقصان دیتی ہے؛ اس وقت پانی ضرور دیں۔","Baal aanay ke waqt garmi nuqsaan deti hai; is waqt pani zaroor dein.","high",S["kp"],"Heat at silking harms set -> ensure irrigation then")
E(31,"KPM-HRV-001","harvest","harvest","advice","جب دانے سخت ہو جائیں اور بھٹے کا چھلکا خشک ہو تو کٹائی کریں۔","Jab daanay sakht ho jayein aur bhutte ka chhilka khushk ho to katai karein.","high",S["kp"],"Harvest when grains are hard and the husk is dry")
E(32,"KPM-HRV-002","harvest","harvest","advice","بھٹے کاٹ کر اچھی طرح خشک کریں، پھر دانے نکالیں۔","Bhutte kaat kar achhi tarah khushk karein, phir daanay nikaalein.","high",S["kp"],"Dry the cobs well, then shell the grain")
E(33,"KPM-HRV-003","harvest","harvest","advice","گہائی اور صفائی صاف جگہ پر کریں تاکہ دانہ صاف رہے۔","Gahai aur safai saaf jagah par karein taakay dana saaf rahay.","medium",S["none"],"Thresh/clean on a clean surface for clean grain")
E(34,"KPM-STO-001","storage","harvest","advice","دانہ اچھی طرح خشک کر کے (کم نمی) صاف اور بند جگہ رکھیں۔","Dana achhi tarah khushk kar ke (kam nami) saaf aur band jagah rakhein.","medium",S["kp"],"Dry grain to low moisture; store clean and closed")
E(35,"KPM-STO-002","storage","harvest","advice","ذخیرے میں سسری (ویول) سے بچاؤ کے لیے دانہ خشک رکھیں اور صاف بند برتن استعمال کریں۔","Zakheeray mein sussri (weevil) se bachao ke liye dana khushk rakhein aur saaf band bartan istemal karein.","medium",S["mgmt"],"Protect stored grain from maize weevil - keep it dry in clean closed containers")
E(36,"KPM-SAF-001","safety","any","warning","سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔","Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.","medium",S["none"],"Wear gloves, mask, covered clothes when spraying")
E(37,"KPM-SAF-002","safety","any","warning","ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔","Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.","medium",S["none"],"Don't spray against the wind; keep others/animals away")
E(38,"KPM-SAF-003","safety","any","warning","سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔","Spray ke baad haath aur mooh dhoyein aur kapray badlein.","medium",S["none"],"Wash hands & face, change clothes after spraying")
E(39,"KPM-SAF-004","safety","any","warning","زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔","Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.","medium",S["none"],"Store pesticide in its labelled container, away from food/children")
E(40,"KPM-SAF-005","safety","any","urgent","زہر لگنے کی علامت (متلی، چکر) پر فوراً طبی مدد لیں اور دوا کا لیبل ساتھ لے جائیں۔","Zehr lagnay ki alamat (matli, chakkar) par foran tibbi madad lein aur dawa ka label saath le jayein.","medium",S["none"],"Poisoning signs (nausea, dizziness) -> get medical help, take the label")
E(41,"KPM-SAF-006","safety","harvest","warning","سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے کٹائی نہ کریں۔","Spray ke baad label par diye gaye waqfay se pehlay katai na karein.","medium",S["none"],"Don't harvest before the label's pre-harvest interval")

entries=[]
for (i,c,cat,st,u,ur,ro,cf,sr,gl,sl) in rows:
    e={"id":i,"code":c,"category":cat,"crop_stage":st,"urgency":u,"text":{"ur":ur,"roman_ur":ro},
       "sources":sr,"confidence":cf,"status":"draft"}
    if sl: e["slots"]=sl
    entries.append(e)
doc={"format_version":2,"dictionary_id":DID,"code":CODE,"region":"kpk","crop":"maize",
     "dictionary_version":1,"languages":["ur","roman_ur"],"entries":entries}
Path("dictionaries/kpk_maize_v2.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8")
OUT=Path("pilot/review_kpk_maize"); OUT.mkdir(parents=True,exist_ok=True)
with open(OUT/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","code","category","crop_stage","urgency","english_meaning","urdu_message","source_link","confidence","correct? (yes/no/partly)","suggested_change","comments"])
    for (i,c,cat,st,u,ur,ro,cf,sr,gl,sl) in rows: w.writerow([i,c,cat,st,u,gl,ur,sr[0]["link"],cf,"","",""])
with open(OUT/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","english_meaning","urdu_text","roman_ur_text","pashto_text (please add)","understandable? (yes/no)","natural? (yes/no)","corrected_text"])
    for (i,c,cat,st,u,ur,ro,cf,sr,gl,sl) in rows: w.writerow([i,gl,ur,ro,"","","",""])
cats=Counter(e["category"] for e in entries); conf=Counter(e["confidence"] for e in entries)
Path("D2_COVERAGE_kpk_maize.md").write_text(
 f"# D2 — Coverage (kpk_maize v2, draft)\n\n**{len(entries)} draft entries.** New crop; **fall armyworm** "
 f"management is foregrounded (hand-picking egg masses, no staggered sowing, field sanitation), with "
 f"harvest/storage weighted for the Oct season. All `status: draft`.\n\n"
 f"By category: {dict(sorted(cats.items()))}\nBy confidence: {dict(conf)}\n\n"
 f"Honest notes: variety list must be confirmed with CCRI Pirsabak; no insecticide doses; Pashto not "
 f"included (Urdu + Roman only) — native speaker to add.\n", encoding="utf-8")
print(f"kpk_maize: {len(entries)} entries; by conf {dict(conf)}")
