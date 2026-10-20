"""Generate a self-contained HTML animation of one advisory flooding a village."""
import json
import numpy as np
from kisaan_voice.mesh_sim import RadioModel, make_village, simulate, adjacency

pos = make_village(80, 0.25, seed=3)
radio = RadioModel.outdoor()
r = simulate(pos, radio, ttl=6, strategy="all", seed=3, record_trace=True)
nbrs = adjacency(pos, radio.range_m)
edges = [[int(i), int(j)] for i, ns in enumerate(nbrs) for j in ns if j > i]
data = {"pos": pos.tolist(), "edges": edges,
        "trace": [[int(x) for x in rnd] for rnd in r.trace],
        "range": radio.range_m, "delivery": round(r.delivery, 2)}

html = """<!doctype html><html><head><meta charset="utf-8">
<title>Kisan Voice — advisory spreading</title>
<style>body{margin:0;background:#0c3d20;color:#eafff0;font-family:system-ui;text-align:center}
canvas{background:#0f4a28;border-radius:10px;margin-top:12px;max-width:95vw}
button{background:#e8b53a;border:0;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer;margin:10px}
h3{margin:14px 0 0}</style></head><body>
<h3>One advisory flooding a village (simulated)</h3>
<div id="s">round 0</div><canvas id="c" width="560" height="560"></canvas><br>
<button onclick="play()">▶ Play</button>
<script>
const D=__DATA__;const cv=document.getElementById('c'),x=cv.getContext('2d');
const S=cv.width, mx=Math.max(...D.pos.map(p=>p[0])), my=Math.max(...D.pos.map(p=>p[1]));
const sc=p=>[30+p[0]/mx*(S-60),30+p[1]/my*(S-60)];
let reached=new Set(), round=0;
function draw(){x.clearRect(0,0,S,S);
 x.strokeStyle='rgba(255,255,255,.08)';
 D.edges.forEach(([a,b])=>{const A=sc(D.pos[a]),B=sc(D.pos[b]);x.beginPath();x.moveTo(...A);x.lineTo(...B);x.stroke();});
 D.pos.forEach((p,i)=>{const P=sc(p);x.beginPath();x.arc(P[0],P[1],i===0?8:5,0,7);
  x.fillStyle=i===0?'#e8b53a':reached.has(i)?'#7bdca0':'#2b6b45';x.fill();});
 document.getElementById('s').textContent='round '+round+'  ·  reached '+reached.size+'/'+D.pos.length+'  ·  final delivery '+(D.delivery*100)+'%';}
function play(){reached=new Set();round=0;draw();
 let i=0;const t=setInterval(()=>{if(i>=D.trace.length){clearInterval(t);return;}
  D.trace[i].forEach(n=>reached.add(n));round=i;draw();i++;},600);}
draw();
</script></body></html>"""
open("s1_out/village_animation.html","w",encoding="utf-8").write(html.replace("__DATA__", json.dumps(data)))
print("wrote s1_out/village_animation.html  (reached",
      sum(len(t) for t in r.trace), "of", len(pos), "nodes over", len(r.trace), "rounds)")
