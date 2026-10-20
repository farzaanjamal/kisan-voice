"""KPK sugarcane v2 — from the sugarcane R1 brief. Red rot + borer complex + autumn
planting front and centre. All draft; no doses; Pashto left to a native speaker.
Emits dictionary + expert/native review sheets + coverage note."""
import csv, json
from collections import Counter
from pathlib import Path

CODE, DID = "KPS", 9
S = {
 "scri": [{"link":"https://agrires.kp.gov.pk/page/sugar_crops_research_institute_mardan_khyber_pakhtunkhwa","note":"SCRI Mardan (KP) production technology — official"}],
 "parc": [{"link":"http://parc.gov.pk/index.php/en/csi/137-narc/crop-sciences-institue/711-sugar-crops-research-program","note":"PARC Sugar Crops Research Program"}],
 "toa":  [{"link":"https://www.timesofagriculture.pk/sugarcane-farming-in-pakistan-2025/","note":"sugarcane practices (planting, harvest, pyrilla)"}],
 "mgmt": [{"link":"http://psst.org.pk/Agriworkshop14/03-ADVANCE%20SUGARCANE%20PRODUCTION%20TECHNOLOGY-RanaZulfiqar%20Ali.pdf","note":"advanced sugarcane production technology — verify SCRI Mardan"}],
 "none": [{"link":"[NEEDS SOURCE]","note":"confirm with SCRI Mardan / KP Agri Dept"}],
}
rows = []
def E(i,c,cat,st,u,ur,ro,cf,sr,gl,sl=None): rows.append((i,c,cat,st,u,ur,ro,cf,sr,gl,sl))

E(1,"KPS-VAR-001","variety","sowing","advice","لال سڑن (ریڈ راٹ) برداشت کرنے والی منظور شدہ قسم کاشت کریں۔","Laal sarran (red rot) bardasht karnay wali manzoor-shuda qism kaasht karein.","high",S["scri"],"Plant a red-rot-resistant approved variety")
E(2,"KPS-VAR-002","variety","sowing","advice","گنے کا بیج (ٹکڑے) صرف صحت مند، بیماری سے پاک فصل سے لیں۔","Ganay ka beej (tukray) sirf sehatmand, bimaari se paak fasal se lein.","high",S["scri"],"Take seed-cane (setts) only from a healthy, disease-free crop")
E(3,"KPS-SOW-001","sowing","sowing","warning","خزاں کی فصل ستمبر-اکتوبر میں کاشت کریں؛ بروقت کاشت سے پیداوار اور چینی بہتر ہوتی ہے۔","Khizaan ki fasal September-October mein kaasht karein; barwaqt kaasht se paidawar aur cheeni behtar hoti hai.","high",S["scri"],"Plant the autumn crop Sept-Oct; timely planting improves yield and sugar")
E(4,"KPS-SOW-002","sowing","sowing","advice","تین آنکھوں والے ٹکڑے نوے سینٹی میٹر فاصلے پر، تین سے پانچ سینٹی میٹر گہرائی میں لگائیں۔","Teen aankhon walay tukray 90 cm faaslay par, 3 se 5 cm gehrai mein lagayein.","high",S["scri"],"Plant 3-budded setts at 90 cm row spacing, 3-5 cm deep")
E(5,"KPS-SOW-003","sowing","sowing","advice","گنے کے ٹکڑوں کا علاج کریں تاکہ دیمک اور بیماری سے بچاؤ ہو۔","Ganay ke tukron ka ilaaj karein taakay deemak aur bimaari se bachao ho.","medium",S["mgmt"],"Treat the setts against termites and disease")
E(6,"KPS-SOW-004","sowing","sowing","advice","کاشت سے پہلے گہری ہل اور ہمواری کریں؛ پھلی دار فصل کے بعد گنا بہتر ہوتا ہے۔","Kaasht se pehlay gehri hal aur hamwaari karein; phalidaar fasal ke baad ganna behtar hota hai.","medium",S["scri"],"Deep-plough and level before planting; cane does better after a legume")
E(7,"KPS-FRT-001","fertilizer","any","advice","کھاد مٹی کے ٹیسٹ کے مطابق ڈالیں اور زرعی افسر سے مشورہ کریں۔","Khaad mitti ke test ke mutabiq daalein aur zarai officer se mashwara karein.","medium",S["none"],"Fertilise per soil test; consult officer")
E(8,"KPS-FRT-002","fertilizer","sowing","advice","کاشت کے وقت سارا فاسفورس اور پوٹاش اور نائٹروجن کا کچھ حصہ ڈالیں؛ باقی نائٹروجن قسطوں میں۔","Kaasht ke waqt saara phosphorus aur potash aur nitrogen ka kuch hissa daalein; baqi nitrogen qiston mein.","high",S["scri"],"At planting apply all P & K and part of the N; the rest of the N in splits")
E(9,"KPS-FRT-003","fertilizer","any","advice","نائٹروجن ضرورت سے زیادہ نہ ڈالیں؛ اس سے پائرلا بڑھتا ہے۔","Nitrogen zaroorat se zyada na daalein; is se pyrilla barhta hai.","high",S["toa"],"Don't over-apply nitrogen - it increases pyrilla")
E(10,"KPS-IRR-001","irrigation","any","advice","گنے کو پوری نشوونما میں مناسب پانی دیں۔","Ganay ko poori nashonuma mein munasib pani dein.","medium",S["scri"],"Give cane adequate water through its growth")
E(11,"KPS-IRR-002","irrigation","any","warning","کھیت میں پانی کھڑا نہ رہنے دیں؛ زیادہ پانی سے تنا چھیدک اور لال سڑن بڑھتے ہیں۔","Khet mein pani khara na rehnay dein; zyada pani se tana chhedak aur laal sarran barhtay hain.","high",S["mgmt"],"Don't let water stand - waterlogging raises top borer and red rot")
E(12,"KPS-IRR-003","irrigation","harvest","advice","کٹائی سے کچھ پہلے پانی کم کر دیں تاکہ چینی کی مقدار بہتر ہو۔","Katai se kuch pehlay pani kam kar dein taakay cheeni ki miqdaar behtar ho.","medium",S["toa"],"Reduce water before harvest to improve sugar content")
E(13,"KPS-WED-001","weeds","vegetative","advice","شروع کے سو دنوں میں جڑی بوٹیاں ختم کریں اور دو بار گوڈی کریں۔","Shuru ke 100 dinon mein jari bootiyan khatam karein aur do baar godi karein.","high",S["mgmt"],"Remove weeds in the first ~100 days and inter-culture twice")
E(14,"KPS-WED-002","weeds","any","advice","کھیت کے کنارے اور اردگرد صفائی رکھیں؛ یہ کیڑوں کا ٹھکانہ ہیں۔","Khet ke kinaray aur ird-gird safai rakhein; ye keeron ka thikana hain.","medium",S["scri"],"Keep field borders clean - they harbour pests")
E(15,"KPS-PST-001","pest_alert","any","advice","ہر ہفتے کھیت دیکھیں؛ کیڑوں کی تعداد دیکھ کر ہی سپرے کریں۔","Har haftay khet dekhein; keeron ki tadaad dekh kar hi spray karein.","high",S["none"],"Scout weekly; spray only on pest counts")
E(16,"KPS-PST-002","pest_alert","vegetative","warning","نئی فصل میں مرکزی شگوفہ سوکھ جائے تو چھیدک (گڑوا) کا حملہ ہے؛ متاثرہ شگوفے کاٹ کر تلف کریں اور افسر سے رجوع کریں۔","Nai fasal mein markazi shiguufa sookh jaye to chhedak (gurwa) ka hamla hai; mutasira shigufay kaat kar talaf karein aur officer se rujoo karein.","high",S["scri"],"Dead central shoot = borer; cut & destroy affected shoots, consult officer")
E(17,"KPS-PST-003","pest_alert","any","advice","کھیت سے سوکھا کچرا اور باقیات بروقت ہٹا کر تلف کریں؛ اس سے چھیدک کم ہوتے ہیں۔","Khet se sookha kachra aur baqiyaat barwaqt hata kar talaf karein; is se chhedak kam hotay hain.","high",S["parc"],"Remove and destroy dry trash/residue promptly - fewer borers")
E(18,"KPS-PST-004","pest_alert","vegetative","advice","مئی-جون میں مٹی چڑھائیں؛ اس سے گرداسپور چھیدک باہر نہیں آ پاتا۔","May-June mein mitti charhayein; is se Gurdaspur chhedak bahar nahin aa paata.","high",S["parc"],"Earth up in May-June; it stops the Gurdaspur borer emerging")
E(19,"KPS-PST-005","pest_alert","any","warning","پتوں پر چپچپاہٹ اور سیاہ کالک (پائرلا) ہو تو زیادہ نائٹروجن نہ ڈالیں اور افسر سے مشورہ کریں۔","Patton par chipchipaahat aur siyah kaalik (pyrilla) ho to zyada nitrogen na daalein aur officer se mashwara karein.","medium",S["toa"],"Sticky leaves + black sooty mould (pyrilla) -> cut nitrogen, consult officer")
E(20,"KPS-PST-006","pest_alert","any","advice","چھیدک اور پائرلا کے خلاف مددگار کیڑے (ٹرائیکوگراما، ایپی ریکینیا) استعمال کریں؛ یہ ادارے سے ملتے ہیں۔","Chhedak aur pyrilla ke khilaaf madadgaar keeray (Trichogramma, Epiricania) istemal karein; ye idaaray se miltay hain.","medium",S["parc"],"Use biocontrol (Trichogramma, Epiricania) from the institute against borers/pyrilla")
E(21,"KPS-PST-007","pest_alert","any","advice","چھیدک پتنگوں کو پکڑنے کے لیے مارچ تا اکتوبر روشنی کے جال (لائٹ ٹریپ) لگائیں۔","Chhedak patangon ko pakarnay ke liye March ta October roshni ke jaal (light trap) lagayein.","medium",S["mgmt"],"Use light traps March-October to catch borer moths")
E(22,"KPS-PST-008","pest_alert","harvest","advice","زیادہ متاثرہ کھیت کی مونڈھی (رتون) نہ رکھیں۔","Zyada mutasira khet ki moondhi (ratoon) na rakhein.","medium",S["mgmt"],"Don't keep a ratoon from a heavily infested field")
E(23,"KPS-DIS-001","disease_alert","vegetative","urgent","اوپر کے پتے پیلے ہو کر سوکھیں اور تنا چیر کر اندر سرخ رنگ میں سفید دھبے اور کھٹی بو ہو تو یہ لال سڑن ہے۔","Ooper ke pattay peelay ho kar sookhein aur tana cheer kar andar surkh rang mein safaid dhabbay aur khatti boo ho to ye laal sarran hai.","high",S["scri"],"Top leaves yellow & dry; split stalk shows red with white patches + sour smell = red rot")
E(24,"KPS-DIS-002","disease_alert","any","warning","لال سڑن کا علاج نہیں؛ مزاحم قسم اور بیماری سے پاک بیج لگائیں اور متاثرہ جھنڈ نکال کر تلف کریں۔","Laal sarran ka ilaaj nahin; muzahim qism aur bimaari se paak beej lagayein aur mutasira jhund nikaal kar talaf karein.","high",S["scri"],"Red rot has no cure - resistant variety, disease-free setts, remove & destroy affected clumps")
E(25,"KPS-DIS-003","disease_alert","flowering","advice","چابک جیسی سیاہ بیماری (کنڈوا) والے پودے نکال کر تلف کریں اور مزاحم قسم لگائیں۔","Chaabuk jaisi siyah bimaari (kandwa) walay poday nikaal kar talaf karein aur muzahim qism lagayein.","low",S["mgmt"],"Remove & destroy whip-smut plants, plant a resistant variety")
E(26,"KPS-DIS-004","disease_alert","any","advice","پتلی اور بونی مونڈھی سے بچنے کے لیے بیماری سے پاک بیج استعمال کریں اور فصلوں میں ردوبدل کریں۔","Patli aur bonay moondhi se bachnay ke liye bimaari se paak beej istemal karein aur faslon mein radd-o-badal karein.","low",S["mgmt"],"Use disease-free setts and rotate crops to avoid ratoon stunting")
E(27,"KPS-WEA-001","weather_alert","any","warning","اگلے {days} دنوں میں تیز بارش متوقع ہے؛ کھیت سے فالتو پانی نکالیں اور کھاد ڈالنا روک دیں۔","Aglay {days} dinon mein tez barish mutawaqqa hai; khet se faltu pani nikaalein aur khaad daalna rok dein.","medium",S["none"],"Heavy rain in {days} days -> drain field, stop fertiliser",[{"name":"days","type":"int","min":1,"max":7}])
E(28,"KPS-WEA-002","weather_alert","any","advice","سردی اور کہر سے بچاؤ کے لیے بروقت کاشت کریں اور مٹی چڑھائیں۔","Sardi aur kahr se bachao ke liye barwaqt kaasht karein aur mitti charhayein.","medium",S["scri"],"Protect against frost by timely planting and earthing up")
E(29,"KPS-WEA-003","weather_alert","any","advice","تیز ہوا میں گنا گرنے سے بچانے کے لیے سہارا دیں یا باندھیں۔","Tez hawa mein ganna girnay se bachanay ke liye sahaara dein ya baandhein.","medium",S["mgmt"],"Prop or tie cane to prevent wind lodging")
E(30,"KPS-HRV-001","harvest","harvest","advice","گنا پوری پختگی پر کاٹیں تاکہ چینی کی مقدار زیادہ ہو۔","Ganna poori pukhtagi par kaatein taakay cheeni ki miqdaar zyada ho.","high",S["toa"],"Harvest cane at full maturity for higher sugar")
E(31,"KPS-HRV-002","harvest","harvest","advice","کٹائی کے وقت پتے اچھی طرح اتاریں تاکہ گنا صاف رہے۔","Katai ke waqt pattay achhi tarah utaarein taakay ganna saaf rahay.","medium",S["toa"],"Strip leaves well at harvest for clean cane")
E(32,"KPS-HRV-003","harvest","harvest","warning","کاٹا ہوا گنا چوبیس سے اڑتالیس گھنٹوں میں مل تک پہنچائیں؛ دیر سے چینی کم ہو جاتی ہے۔","Kaata hua ganna 24 se 48 ghanton mein mill tak pohanchayein; der se cheeni kam ho jaati hai.","high",S["toa"],"Deliver cut cane to the mill within 24-48 hours - sugar drops with delay")
E(33,"KPS-SAF-001","safety","any","warning","سپرے کرتے وقت دستانے، ماسک اور ڈھکے ہوئے کپڑے پہنیں۔","Spray kartay waqt dastanay, mask aur dhakay huay kapray pehnein.","medium",S["none"],"Wear gloves, mask, covered clothes when spraying")
E(34,"KPS-SAF-002","safety","any","warning","ہوا کے رخ کے خلاف سپرے نہ کریں؛ دوسروں اور جانوروں کو دور رکھیں۔","Hawa ke rukh ke khilaaf spray na karein; doosron aur jaanwaron ko door rakhein.","medium",S["none"],"Don't spray against the wind; keep others/animals away")
E(35,"KPS-SAF-003","safety","any","warning","سپرے کے بعد ہاتھ اور منہ دھوئیں اور کپڑے بدلیں۔","Spray ke baad haath aur mooh dhoyein aur kapray badlein.","medium",S["none"],"Wash hands & face, change clothes after spraying")
E(36,"KPS-SAF-004","safety","any","warning","زہریلی دوا اصل لیبل والے ڈبے میں، کھانے اور بچوں سے دور رکھیں۔","Zehreeli dawa asal label walay dabbay mein, khaanay aur bachon se door rakhein.","medium",S["none"],"Store pesticide in its labelled container, away from food/children")
E(37,"KPS-SAF-005","safety","any","urgent","زہر لگنے کی علامت (متلی، چکر) پر فوراً طبی مدد لیں اور دوا کا لیبل ساتھ لے جائیں۔","Zehr lagnay ki alamat (matli, chakkar) par foran tibbi madad lein aur dawa ka label saath le jayein.","medium",S["none"],"Poisoning signs (nausea, dizziness) -> get medical help, take the label")
E(38,"KPS-SAF-006","safety","harvest","warning","سپرے کے بعد لیبل پر دیے گئے وقفے سے پہلے کٹائی نہ کریں۔","Spray ke baad label par diye gaye waqfay se pehlay katai na karein.","medium",S["none"],"Don't harvest before the label's pre-harvest interval")

entries=[]
for (i,c,cat,st,u,ur,ro,cf,sr,gl,sl) in rows:
    e={"id":i,"code":c,"category":cat,"crop_stage":st,"urgency":u,"text":{"ur":ur,"roman_ur":ro},
       "sources":sr,"confidence":cf,"status":"draft"}
    if sl: e["slots"]=sl
    entries.append(e)
doc={"format_version":2,"dictionary_id":DID,"code":CODE,"region":"kpk","crop":"sugarcane",
     "dictionary_version":1,"languages":["ur","roman_ur"],"entries":entries}
Path("dictionaries/kpk_sugarcane_v2.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8")
OUT=Path("pilot/review_kpk_sugarcane"); OUT.mkdir(parents=True,exist_ok=True)
with open(OUT/"expert_review_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","code","category","crop_stage","urgency","english_meaning","urdu_message","source_link","confidence","correct? (yes/no/partly)","suggested_change","comments"])
    for (i,c,cat,st,u,ur,ro,cf,sr,gl,sl) in rows: w.writerow([i,c,cat,st,u,gl,ur,sr[0]["link"],cf,"","",""])
with open(OUT/"native_speaker_sheet.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["id","english_meaning","urdu_text","roman_ur_text","pashto_text (please add)","understandable? (yes/no)","natural? (yes/no)","corrected_text"])
    for (i,c,cat,st,u,ur,ro,cf,sr,gl,sl) in rows: w.writerow([i,gl,ur,ro,"","","",""])
cats=Counter(e["category"] for e in entries); conf=Counter(e["confidence"] for e in entries)
Path("D2_COVERAGE_kpk_sugarcane.md").write_text(
 f"# D2 — Coverage (kpk_sugarcane v2, draft)\n\n**{len(entries)} draft entries.** New crop; **red rot** "
 f"(prevention-only) and the **borer complex + pyrilla** are foregrounded, with autumn planting + "
 f"disease-free setts weighted for the Oct season. All `status: draft`.\n\n"
 f"By category: {dict(sorted(cats.items()))}\nBy confidence: {dict(conf)}\n\n"
 f"Honest notes: red-rot-resistant variety list must be confirmed with SCRI Mardan; no insecticide "
 f"doses; Pashto not included (Urdu + Roman only) — native speaker to add.\n", encoding="utf-8")
print(f"kpk_sugarcane: {len(entries)} entries; by conf {dict(conf)}")
