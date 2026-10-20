// Parity test: JS core must reproduce Python's output for every entry.
const fs = require("fs");
const KV = require("./kv_core.js");
const expected = JSON.parse(fs.readFileSync("expected_parity.json", "utf8"));
const dicts = fs.readdirSync("../dictionaries").filter(f => f.endsWith("_v2.json"))
  .map(f => JSON.parse(fs.readFileSync("../dictionaries/" + f, "utf8")));
const byCode = Object.fromEntries(dicts.map(d => [d.code, d]));

let fail = 0;
for (const r of expected) {
  const d = byCode[r.code];
  const e = KV.entryById(d, r.id);
  const sv = {}; (e.slots || []).forEach(s => { sv[s.name] = s.min; });
  const sms = KV.encodeSms(d, r.id, sv);
  const bin = KV.toHex(KV.encodeBinary(d, r.id, sv, 1, 4, 0));
  const dec = KV.decodeSms(sms, [d], "ur");
  const seg = KV.countSegments(dec.message);
  const smsSeg = KV.countSegments(sms).segments;
  const problems = [];
  if (sms !== r.sms) problems.push(`sms ${sms}!=${r.sms}`);
  if (bin !== r.binary_hex) problems.push(`bin ${bin}!=${r.binary_hex}`);
  if (dec.message !== r.msg_ur) problems.push("msg");
  if (seg.encoding !== r.enc || seg.length !== r.length || seg.segments !== r.segments)
    problems.push(`seg ${seg.encoding}/${seg.length}/${seg.segments}`);
  if (smsSeg !== r.sms_segments) problems.push("smsSeg");
  if (problems.length) { fail++; if (fail <= 5) console.log(`${r.code}-${r.id}:`, problems.join("; ")); }
}
console.log(fail === 0
  ? `PARITY OK — JS matches Python on all ${expected.length} entries`
  : `PARITY FAILED on ${fail}/${expected.length}`);
process.exit(fail ? 1 : 0);
