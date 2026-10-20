"""Assemble the self-contained Kisaan Voice W1 site (index.html)."""
import base64, glob, json, sys
from pathlib import Path
sys.path.insert(0, "..")
from kisaan_voice import benchmark

def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()

# real compression stats, computed now
stats = []
for p in sorted(glob.glob("../dictionaries/*_v2.json")):
    s = benchmark.run(p, out_dir="../benchmark_out")["summary"]
    stats.append({"crop": Path(p).stem.replace("_v2", ""), **s})
agg_entries = sum(s["entries"] for s in stats)
collapsed = sum(int(s["messages_2plus_segments_now_1_code_segment"].split("/")[0]) for s in stats)
med = round(sum(s["median_binary_size_reduction_vs_ucs2_pct"] for s in stats) / len(stats), 1)

DICTS = [json.loads(Path(p).read_text(encoding="utf-8")) for p in sorted(glob.glob("../dictionaries/*_v2.json"))]
KV_JS = Path("kv_core.js").read_text(encoding="utf-8")
BENCH = b64("../benchmark_out/benchmark.png", "image/png")
DENS = b64("../s1_out/delivery_vs_density.png", "image/png")
TTL = b64("../s1_out/delivery_vs_ttl.png", "image/png")
ANIM = "data:text/html;base64," + base64.b64encode(
    Path("../s1_out/village_animation.html").read_bytes()).decode()

stats_rows = "".join(
    f"<tr><td>{s['crop']}</td><td>{s['entries']}</td>"
    f"<td>{s['median_binary_size_reduction_vs_ucs2_pct']}%</td>"
    f"<td>{s['messages_2plus_segments_now_1_code_segment']}</td></tr>" for s in stats)

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Kisan Voice — compressed farming advisories for low-connectivity Pakistan</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@500;700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
 :root{--field:#14532d;--field-dk:#0c3d20;--wheat:#e8b53a;--paper:#fbf7ec;--ink:#1b1a17;
   --ink-soft:#56534b;--line:#e4dcc6;--alert:#c0261f;--ok:#1c6a3c}
 *{box-sizing:border-box}
 body{margin:0;font-family:Inter,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.6}
 .ur{font-family:"Noto Nastaliq Urdu",serif;direction:rtl}
 .wrap{max-width:960px;margin:0 auto;padding:0 18px}
 header{background:radial-gradient(120% 90% at 100% 0,#1c6a3c,var(--field) 55%,var(--field-dk));
   color:#fff;padding:54px 0 48px}
 header h1{font-size:40px;margin:0 0 6px;font-weight:800}
 header .ur{font-size:30px;font-weight:700}
 header p{font-size:19px;max-width:640px;opacity:.95}
 .btn{display:inline-block;background:var(--wheat);color:#1b1a17;font-weight:700;border:0;
   border-radius:12px;padding:13px 22px;cursor:pointer;text-decoration:none;font-size:16px}
 section{padding:40px 0;border-bottom:1px solid var(--line)}
 h2{font-size:26px;margin:0 0 6px}
 h2 .n{color:var(--wheat);font-weight:800;margin-right:8px}
 .sub{color:var(--ink-soft);margin:0 0 20px}
 .demo{display:grid;grid-template-columns:1fr 1fr;gap:18px}
 @media(max-width:760px){.demo{grid-template-columns:1fr}header h1{font-size:32px}}
 .card{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px}
 label{display:block;font-weight:600;font-size:13px;margin:10px 0 4px}
 select,input[type=number],input[type=text]{width:100%;padding:11px;border:1px solid var(--line);
   border-radius:10px;font-size:15px;font-family:inherit;background:#fff}
 .seg{display:flex;gap:8px;margin-top:10px}
 .seg button{flex:1;padding:9px;border:1px solid var(--line);background:#fff;border-radius:9px;cursor:pointer;font-weight:600}
 .seg button.on{background:var(--field);color:#fff;border-color:var(--field)}
 .msg{font-size:23px;min-height:72px;margin:6px 0 10px}
 .listen{background:var(--field);color:#fff;border:0;border-radius:11px;padding:12px 16px;
   font-weight:700;cursor:pointer;font-size:16px}
 .cmp{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
 .cmp .k{font-size:12px;color:var(--ink-soft);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
 .cmp .v{font-family:ui-monospace,monospace;font-size:13px;word-break:break-all}
 .bars{margin-top:14px}
 .bar{height:26px;border-radius:7px;color:#fff;font-size:12px;font-weight:700;
   display:flex;align-items:center;padding:0 10px;margin-top:6px;white-space:nowrap}
 table{width:100%;border-collapse:collapse;margin-top:10px}
 th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);font-size:14px}
 th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink-soft)}
 .two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
 @media(max-width:760px){.two,.cmp,.demo{grid-template-columns:1fr}}
 .pill{display:inline-block;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}
 .built{background:#dff0e4;color:#14532d}.plan{background:#f3e7c7;color:#7a5a12}
 img.chart{width:100%;border:1px solid var(--line);border-radius:12px;margin-top:10px}
 .note{background:#fff8e6;border:1px solid #ead9a6;border-radius:10px;padding:12px;font-size:13px;color:#6b5618}
 iframe{width:100%;height:640px;border:1px solid var(--line);border-radius:12px;margin-top:10px}
 .flow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:14px;margin-top:8px}
 .flow .node{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-weight:600}
 .flow .ar{color:var(--wheat);font-weight:800}
 footer{padding:34px 0;color:var(--ink-soft);font-size:14px}
 a{color:var(--ok)}
 .diag{color:var(--alert);font-weight:700}
</style>
</head>
<body>
<header><div class="wrap">
  <div class="ur">کسان آواز</div>
  <h1>Kisan Voice</h1>
  <p>Farming advisories for small farmers in low-connectivity Pakistan: the advice lives in
     an offline dictionary, so only a tiny code (~9 bytes / one SMS) has to travel — and any
     phone that holds the dictionary speaks the full message in Urdu.</p>
  <a class="btn" href="#demo">Try the live demo ↓</a>
</div></header>

<section id="demo"><div class="wrap">
  <h2><span class="n">1</span>Live demo — a code becomes advice</h2>
  <p class="sub">Pick an advisory. The page encodes it to an SMS code and a Bluetooth packet, then
     decodes it back — using the <b>exact same rules as the Python package, verified identical on
     all __AGG__ entries</b>.</p>
  <div class="demo">
    <div class="card">
      <label>Region &amp; crop</label>
      <select id="dict"></select>
      <label>Advisory</label>
      <select id="entry"></select>
      <div id="slotBox"></div>
      <label>Language</label>
      <div class="seg" id="langSeg">
        <button data-l="ur" class="on">اردو Urdu</button>
        <button data-l="roman_ur">Roman Urdu</button>
      </div>
      <div class="note" style="margin-top:12px">Regional languages (Sindhi, Pashto, Saraiki) are
        planned — they need a native speaker, so the draft ships Urdu + Roman Urdu only.</div>
    </div>
    <div class="card">
      <div class="ur msg" id="msg" dir="auto"></div>
      <button class="listen" id="listen">▶ Listen (device voice)</button>
      <div class="cmp">
        <div><div class="k">SMS code</div><div class="v" id="smsCode"></div><div class="v" id="smsMeta"></div></div>
        <div><div class="k">Bluetooth packet</div><div class="v" id="binCode"></div><div class="v" id="binMeta"></div></div>
      </div>
      <div class="bars" id="bars"></div>
    </div>
  </div>

  <div class="card" style="margin-top:16px">
    <label>Decode any code yourself (e.g. <code>KV2 PCT 1</code> or <code>KV2 SNR 5</code>)</label>
    <div style="display:flex;gap:8px">
      <input type="text" id="decIn" value="KV2 KPW 4" spellcheck="false">
      <button class="listen" id="decBtn" style="flex:0 0 auto">Decode</button>
    </div>
    <div class="ur msg" id="decOut" dir="auto" style="min-height:40px"></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2><span class="n">2</span>How it works</h2>
  <p class="sub">Complexity stays in the infrastructure; the farmer just receives useful advice.</p>
  <div class="flow">
    <span class="node">Officer picks advisory</span><span class="ar">→</span>
    <span class="node">encode → tiny code</span><span class="ar">→</span>
    <span class="node">SMS or Bluetooth relay</span><span class="ar">→</span>
    <span class="node">phone holds dictionary</span><span class="ar">→</span>
    <span class="node">full Urdu — text or voice</span>
  </div>
</div></section>

<section><div class="wrap">
  <h2><span class="n">3</span>Evidence</h2>
  <p class="sub">Real numbers from the code in this repo. Pilot numbers are not invented — they
     appear only after a real pilot.</p>

  <h3>Compression — why not just gzip?</h3>
  <p>Because the win isn't clever compression; it's that the receiver already holds the dictionary,
     so only a reference travels. Across all three draft dictionaries (__AGG__ advisories), the
     median message is about <b>__MED__% smaller</b> as a binary code, and <b>__COLL__</b> messages
     that would need two SMS collapse into a single code.</p>
  <table><tr><th>Crop</th><th>Entries</th><th>Median size cut</th><th>2+ SMS → 1 code</th></tr>__ROWS__</table>
  <img class="chart" src="__BENCH__" alt="compression benchmark: full Urdu vs zlib vs dictionary code">

  <h3 style="margin-top:26px">Mesh simulation <span class="diag">(simulation — placeholder range)</span></h3>
  <p>A village managed-flooding simulator (store-and-forward, TTL, duplicate suppression). Range is
     a placeholder until a two-phone nRF test calibrates it, so these show <b>relative</b> behaviour,
     not field performance.</p>
  <div class="two">
    <img class="chart" src="__DENS__" alt="delivery vs density">
    <img class="chart" src="__TTL__" alt="delivery vs TTL">
  </div>
  <p style="margin-top:14px">Watch one advisory flood a village (synthetic demo):</p>
  <iframe src="__ANIM__" title="village mesh animation"></iframe>

  <h3 style="margin-top:26px">Pilot</h3>
  <div class="note"><b>[ PILOT RESULTS COMING ]</b> — a small, consented 7-day pilot is planned.
     No pilot numbers are shown until they are real.</div>
</div></section>

<section><div class="wrap">
  <h2><span class="n">4</span>Built vs in progress</h2>
  <div class="two">
    <div class="card">
      <p><span class="pill built">BUILT &amp; TESTED</span></p>
      <ul>
        <li>v2 dictionary format + schema validation</li>
        <li>SMS code + Bluetooth packet; language fallback; version safety</li>
        <li>GSM-7 / UCS-2 segment counting</li>
        <li>Three cited draft dictionaries (cotton, rice, wheat — __AGG__ entries)</li>
        <li>Compression benchmark; village mesh simulator</li>
        <li>This demo (JS verified identical to Python)</li>
      </ul>
    </div>
    <div class="card">
      <p><span class="pill plan">IN PROGRESS / PLANNED</span></p>
      <ul>
        <li>Agronomist approval of advisories (none sent until approved)</li>
        <li>Native Sindhi / Pashto translations</li>
        <li>Urdu voice clips (generator ready)</li>
        <li>Android phone-to-phone relay app (code ready, untested on hardware)</li>
        <li>Real nRF range calibration for the mesh</li>
        <li>The 7-day farmer pilot</li>
      </ul>
    </div>
  </div>
</div></section>

<footer><div class="wrap">
  <p><b>Sources &amp; review.</b> Advisories are drafted from official Pakistani sources
     (Punjab/Sindh/KP agriculture departments, PARC, ARI Tarnab, CCRI Multan, RRI Dokri) and are
     marked for expert review — reviewers will be credited by role with their permission.</p>
  <p>Code &amp; technical report: <a href="#">[GitHub link]</a> · Contact: [your email] ·
     Built for farmers in Pakistan.</p>
</div></footer>

<script>__KVJS__</script>
<script>
const DICTS = __DICTS__;
let curLang = "ur", curDict = DICTS[0];

const $ = id => document.getElementById(id);
function fillDicts(){
  $("dict").innerHTML = DICTS.map((d,i)=>`<option value="${i}">${d.region} · ${d.crop} (${d.code})</option>`).join("");
}
function fillEntries(){
  $("entry").innerHTML = curDict.entries.map(e=>`<option value="${e.id}">${e.code} · ${e.category}</option>`).join("");
}
function slotInputs(e){
  if(!e.slots || !e.slots.length){ $("slotBox").innerHTML=""; return; }
  $("slotBox").innerHTML = e.slots.map(s=>
    `<label>${s.name} (${s.min}–${s.max})</label><input type="number" id="slot_${s.name}" value="${s.min}" min="${s.min}" max="${s.max}">`).join("");
}
function slotVals(e){
  const v={}; (e.slots||[]).forEach(s=>{ v[s.name]=parseInt($("slot_"+s.name).value,10)||s.min; }); return v;
}
function ucs2bytes(s){ return Array.from(s).length*2; }

function render(){
  const e = KV.entryById(curDict, parseInt($("entry").value,10));
  slotInputsIfNeeded(e);
  const sv = slotVals(e);
  let out;
  try{ out = KV.decodeSms(KV.encodeSms(curDict,e.id,sv),[curDict],curLang); }
  catch(err){ $("msg").textContent = err.message; return; }
  $("msg").textContent = out.message;
  $("msg").dir = out.language==="ur" ? "rtl" : "ltr";
  const sms = KV.encodeSms(curDict,e.id,sv);
  const bin = KV.toHex(KV.encodeBinary(curDict,e.id,sv,1,4,0));
  const segFull = KV.countSegments(out.message), segSms = KV.countSegments(sms);
  $("smsCode").textContent = sms;
  $("smsMeta").textContent = `${sms.length} chars · ${segSms.segments} SMS segment`;
  $("binCode").textContent = bin;
  $("binMeta").textContent = `${bin.length/2} bytes`;
  // bars: full UCS-2 message vs binary code
  const full = ucs2bytes(out.message), code = bin.length/2, max = Math.max(full,code);
  $("bars").innerHTML =
    `<div class="k">Bytes on the wire</div>`+
    `<div class="bar" style="width:${Math.max(16,full/max*100)}%;background:#9aa0aa">full Urdu: ${full} B · ${segFull.segments} SMS</div>`+
    `<div class="bar" style="width:${Math.max(16,code/max*100)}%;background:var(--field)">our code: ${code} B · 1 SMS</div>`;
}
let _lastEntryId=null;
function slotInputsIfNeeded(e){ if(e.id!==_lastEntryId){ slotInputs(e); _lastEntryId=e.id; } }

function speak(){
  const t=$("msg").textContent; if(!("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(t); u.lang="ur-PK"; u.rate=.9;
  const v=speechSynthesis.getVoices().find(v=>/ur[-_]PK/i.test(v.lang))||speechSynthesis.getVoices().find(v=>/^ur/i.test(v.lang));
  if(v) u.voice=v; speechSynthesis.speak(u);
}

$("dict").onchange = ()=>{ curDict=DICTS[+$("dict").value]; fillEntries(); _lastEntryId=null; render(); };
$("entry").onchange = render;
$("slotBox").oninput = render;
$("listen").onclick = speak;
document.querySelectorAll("#langSeg button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll("#langSeg button").forEach(x=>x.classList.remove("on"));
  b.classList.add("on"); curLang=b.dataset.l; render();
});
$("decBtn").onclick = ()=>{
  try{ const o=KV.decodeSms($("decIn").value,DICTS,curLang);
    $("decOut").textContent=o.message; $("decOut").dir=o.language==="ur"?"rtl":"ltr"; }
  catch(err){ $("decOut").textContent="⚠ "+err.message; $("decOut").dir="ltr"; }
};

fillDicts(); fillEntries(); render();
</script>
</body>
</html>
"""

HTML = (HTML.replace("__KVJS__", KV_JS)
            .replace("__DICTS__", json.dumps(DICTS, ensure_ascii=False))
            .replace("__BENCH__", BENCH).replace("__DENS__", DENS).replace("__TTL__", TTL)
            .replace("__ANIM__", ANIM).replace("__ROWS__", stats_rows)
            .replace("__AGG__", str(agg_entries)).replace("__MED__", str(med))
            .replace("__COLL__", str(collapsed)))
Path("index.html").write_text(HTML, encoding="utf-8")
print(f"wrote index.html  ({len(HTML)//1024} KB)  entries={agg_entries} median={med}% collapsed={collapsed}")
