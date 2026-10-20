package org.kisaanvoice.mesh

import android.content.Context
import org.json.JSONObject

/**
 * Offline dictionary: loads the bundled v2 JSON from assets and decodes an entry id
 * (+ slot values) into the full message. Fallback order: requested lang -> ur -> roman_ur.
 * Never returns a wrong message: unknown id or dictionary-version mismatch returns null.
 */
class Dictionary private constructor(
    val id: Int, val version: Int, val code: String,
    private val entries: Map<Int, JSONObject>
) {
    /** slotValues are POSITIONAL, in the same order the binary packet carries them. */
    fun decode(entryId: Int, slotValues: List<Int>, lang: String): String? {
        val e = entries[entryId] ?: return null
        val text = e.getJSONObject("text")
        val order = listOf(lang, "ur", "roman_ur")
        var raw: String? = null
        for (l in order) {
            if (text.has(l) && text.getString(l) != "[MISSING]") { raw = text.getString(l); break }
        }
        var msg = raw ?: return null
        if (e.has("slots")) {
            val slots = e.getJSONArray("slots")
            if (slotValues.size < slots.length()) return null
            for (k in 0 until slots.length()) {
                val s = slots.getJSONObject(k)
                val name = s.getString("name")
                val v = slotValues[k]
                if (s.getString("type") == "int") {
                    val lo = if (s.has("min")) s.getInt("min") else Int.MIN_VALUE
                    val hi = if (s.has("max")) s.getInt("max") else Int.MAX_VALUE
                    if (v < lo || v > hi) return null       // out of range -> refuse
                    msg = msg.replace("{$name}", v.toString())
                }
            }
        }
        return msg
    }

    companion object {
        fun fromAssets(ctx: Context, name: String): Dictionary {
            val raw = ctx.assets.open(name).bufferedReader().use { it.readText() }
            val j = JSONObject(raw)
            val arr = j.getJSONArray("entries")
            val map = HashMap<Int, JSONObject>()
            for (i in 0 until arr.length()) {
                val e = arr.getJSONObject(i); map[e.getInt("id")] = e
            }
            return Dictionary(j.getInt("dictionary_id"), j.getInt("dictionary_version"),
                              j.getString("code"), map)
        }
    }
}
