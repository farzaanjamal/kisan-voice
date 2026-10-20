package org.kisaanvoice.mesh

/**
 * Binary mesh packet — byte-for-byte identical to the tested Python v2 encoder
 * (kisaan_voice/encoding.py). Layout:
 *
 *   [0] format_version (=2)
 *   [1] dictionary_id
 *   [2] dictionary_version
 *   [.] entry_id            (LEB128 varint)
 *   [.] slot_count          (1 byte)  then each slot value as a varint
 *   [.] message_id          (2 bytes, big-endian)
 *   [.] ttl                 (1 byte)
 *   [.] hop                 (1 byte)
 *
 * Worst case in the sample dictionary = 10 bytes, so it fits a legacy 31-byte BLE
 * advertisement with room to spare.
 */
data class Packet(
    val dictId: Int,
    val dictVersion: Int,
    val entryId: Int,
    val slots: List<Int>,
    val msgId: Int,
    val ttl: Int,
    val hop: Int
) {
    fun toBytes(): ByteArray {
        val out = ArrayList<Byte>()
        out.add(FORMAT_VERSION.toByte())
        out.add((dictId and 0xFF).toByte())
        out.add((dictVersion and 0xFF).toByte())
        writeVarint(out, entryId)
        out.add((slots.size and 0xFF).toByte())
        for (s in slots) writeVarint(out, s)
        out.add(((msgId shr 8) and 0xFF).toByte())
        out.add((msgId and 0xFF).toByte())
        out.add((ttl and 0xFF).toByte())
        out.add((hop and 0xFF).toByte())
        return out.toByteArray()
    }

    /** New packet for relaying: one hop consumed. */
    fun forRelay(): Packet = copy(ttl = ttl - 1, hop = hop + 1)

    val expired: Boolean get() = ttl <= 0

    companion object {
        const val FORMAT_VERSION = 2

        fun fromBytes(b: ByteArray): Packet? {
            if (b.size < 4 || (b[0].toInt() and 0xFF) != FORMAT_VERSION) return null
            var i = 1
            val dictId = b[i++].toInt() and 0xFF
            val dictVersion = b[i++].toInt() and 0xFF
            val (entryId, i2) = readVarint(b, i); i = i2
            val slotCount = b[i++].toInt() and 0xFF
            val slots = ArrayList<Int>(slotCount)
            repeat(slotCount) { val (v, ni) = readVarint(b, i); slots.add(v); i = ni }
            if (i + 4 > b.size) return null
            val msgId = ((b[i].toInt() and 0xFF) shl 8) or (b[i + 1].toInt() and 0xFF); i += 2
            val ttl = b[i++].toInt() and 0xFF
            val hop = b[i].toInt() and 0xFF
            return Packet(dictId, dictVersion, entryId, slots, msgId, ttl, hop)
        }

        private fun writeVarint(out: ArrayList<Byte>, nIn: Int) {
            var n = nIn
            while (true) {
                val part = n and 0x7F
                n = n ushr 7
                out.add((part or if (n != 0) 0x80 else 0).toByte())
                if (n == 0) break
            }
        }

        private fun readVarint(b: ByteArray, startIn: Int): Pair<Int, Int> {
            var shift = 0; var n = 0; var i = startIn
            while (true) {
                val x = b[i++].toInt() and 0xFF
                n = n or ((x and 0x7F) shl shift)
                if (x and 0x80 == 0) break
                shift += 7
            }
            return Pair(n, i)
        }

        fun toHex(b: ByteArray): String = b.joinToString("") { "%02x".format(it) }

        /**
         * Cross-check against the Python output. In Python:
         *   encode_binary(D, 1, None, msg_id=1, ttl=4, hop=0).hex() == "020102010000010400"
         * Call Packet.selfTest() once at startup; it must return true.
         */
        fun selfTest(): Boolean {
            val p = Packet(dictId = 1, dictVersion = 2, entryId = 1, slots = emptyList(),
                           msgId = 1, ttl = 4, hop = 0)
            return toHex(p.toBytes()) == "020102010000010400"
        }
    }
}
