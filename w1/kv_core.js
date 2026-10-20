/* Kisaan Voice — browser/node core. Mirrors kisaan_voice (Python) byte-for-byte.
   A node parity test (kv_parity.js) checks this matches Python for every entry. */
(function (root) {
  "use strict";

  // GSM 03.38 basic + extension (identical set to segments.py)
  const GSM_BASIC =
    "@\u00a3$\u00a5\u00e8\u00e9\u00f9\u00ec\u00f2\u00c7\n\u00d8\u00f8\r\u00c5\u00e5" +
    "\u0394_\u03a6\u0393\u039b\u03a9\u03a0\u03a8\u03a3\u0398\u039e\u001b\u00c6\u00e6\u00df\u00c9" +
    " !\"#\u00a4%&'()*+,-./0123456789:;<=>?" +
    "\u00a1ABCDEFGHIJKLMNOPQRSTUVWXYZ\u00c4\u00d6\u00d1\u00dc\u00a7" +
    "\u00bfabcdefghijklmnopqrstuvwxyz\u00e4\u00f6\u00f1\u00fc\u00e0";
  const GSM_EXT = "\f^{}\\[~]|\u20ac";
  const GSM = new Set((GSM_BASIC + GSM_EXT).split(""));
  const EXT = new Set(GSM_EXT.split(""));

  function cp(s) { return Array.from(s); }           // code points, matches Python len

  function isGsm7(s) { return cp(s).every(ch => GSM.has(ch)); }

  function countSegments(s) {
    let enc, length, single, multi;
    if (isGsm7(s)) {
      enc = "GSM-7";
      length = cp(s).reduce((n, ch) => n + (EXT.has(ch) ? 2 : 1), 0);
      single = 160; multi = 153;
    } else {
      enc = "UCS-2"; length = cp(s).length; single = 70; multi = 67;
    }
    const segments = length <= single ? 1 : Math.ceil(length / multi);
    return { encoding: enc, length, segments };
  }

  // ---- varint (LEB128) ----
  function writeVarint(out, n) {
    while (true) { let b = n & 0x7f; n >>>= 7; out.push(b | (n ? 0x80 : 0)); if (!n) break; }
  }
  function readVarint(buf, i) {
    let shift = 0, n = 0;
    while (true) { const x = buf[i++]; n |= (x & 0x7f) << shift; if (!(x & 0x80)) break; shift += 7; }
    return [n, i];
  }
  function toHex(bytes) { return bytes.map(b => b.toString(16).padStart(2, "0")).join(""); }

  const MARKER = "KV2", FORMAT_VERSION = 2;

  function entryById(dict, id) { return dict.entries.find(e => e.id === id); }

  function encodeSms(dict, entryId, slotValues) {
    const e = entryById(dict, entryId);
    const vals = (e.slots || []).map(s => String(parseInt(slotValues[s.name], 10)));
    return [MARKER, dict.code, String(entryId)].concat(vals).join(" ");
  }

  function encodeBinary(dict, entryId, slotValues, msgId, ttl, hop) {
    const e = entryById(dict, entryId);
    const out = [FORMAT_VERSION, dict.dictionary_id & 0xff, dict.dictionary_version & 0xff];
    writeVarint(out, entryId);
    const slots = e.slots || [];
    out.push(slots.length & 0xff);
    slots.forEach(s => writeVarint(out, parseInt(slotValues[s.name], 10)));
    out.push((msgId >> 8) & 0xff, msgId & 0xff, ttl & 0xff, hop & 0xff);
    return out;
  }

  function render(e, lang, slotValues) {
    const order = [lang, "ur", "roman_ur"];
    let text = null, used = null;
    for (const l of order) {
      const t = e.text[l];
      if (t && t !== "[MISSING]") { text = t; used = l; break; }
    }
    if (text == null) throw new Error("no text for entry " + e.id);
    for (const s of (e.slots || [])) {
      const v = parseInt(slotValues[s.name], 10);
      if (s.type === "int") {
        const lo = s.min != null ? s.min : -Infinity, hi = s.max != null ? s.max : Infinity;
        if (v < lo || v > hi) throw new Error("slot '" + s.name + "'=" + v + " out of range");
        text = text.split("{" + s.name + "}").join(String(v));
      }
    }
    return { entry_id: e.id, code: e.code, language: used, status: e.status, message: text };
  }

  function decodeSms(code, dicts, lang) {
    const toks = code.trim().split(/\s+/);
    if (toks.length < 3 || toks[0] !== MARKER) throw new Error("not a valid KV2 code");
    const dict = dicts.find(d => d.code === toks[1]);
    if (!dict) throw new Error("no dictionary with code " + toks[1]);
    const e = entryById(dict, parseInt(toks[2], 10));
    if (!e) throw new Error("unknown entry id " + toks[2] + " in " + dict.code);
    const slotValues = {};
    (e.slots || []).forEach((s, k) => { slotValues[s.name] = parseInt(toks[3 + k], 10); });
    return render(e, lang, slotValues);
  }

  const api = { isGsm7, countSegments, encodeSms, encodeBinary, decodeSms, toHex, entryById };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.KV = api;
})(typeof window !== "undefined" ? window : this);
