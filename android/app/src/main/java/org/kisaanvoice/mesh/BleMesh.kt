package org.kisaanvoice.mesh

import android.annotation.SuppressLint
import android.bluetooth.BluetoothManager
import android.bluetooth.le.*
import android.content.Context
import android.os.Handler
import android.os.Looper
import android.os.ParcelUuid
import kotlin.random.Random

/**
 * Managed-flooding BLE mesh over legacy advertisements (manufacturer-specific data,
 * test company id 0xFFFF). A node that hears a NEW message id rebroadcasts it once
 * after random jitter with TTL-1 / hop+1, keeps a duplicate cache, and drops at TTL 0.
 *
 * UNTESTED on hardware in this build. Designed as a FOREGROUND, screen-on demo —
 * Android background BLE limits make a continuous background mesh impractical, which
 * is why the architecture uses a village gateway (see CAPABILITIES.md / S1 RESULTS).
 */
class BleMesh(
    private val ctx: Context,
    private val nodeId: Int,
    private val onEvent: (String) -> Unit,
    private val onMessage: (Packet) -> Unit
) {
    enum class Role { ORIGIN, RELAY, DESTINATION }

    private val mgr = ctx.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
    private val adapter get() = mgr.adapter
    private val advertiser: BluetoothLeAdvertiser? get() = adapter?.bluetoothLeAdvertiser
    private val scanner: BluetoothLeScanner? get() = adapter?.bluetoothLeScanner
    private val handler = Handler(Looper.getMainLooper())

    private val seen = LinkedHashSet<Int>()          // bounded duplicate cache
    private var role = Role.RELAY
    var forcedChainHop: Int? = null                  // demo: accept only this hop index

    private var scanCb: ScanCallback? = null
    private var advCb: AdvertiseCallback? = null

    companion object { const val COMPANY_ID = 0xFFFF; const val SEEN_CAP = 1024 }

    fun start(role: Role) {
        this.role = role
        if (adapter == null || !adapter.isEnabled) { onEvent("Bluetooth is off"); return }
        if (advertiser == null) { onEvent("This phone can't BLE-advertise"); return }
        startScanning()
        onEvent("started as $role (node $nodeId)")
    }

    fun stop() {
        try { scanCb?.let { scanner?.stopScan(it) } } catch (_: SecurityException) {}
        try { advCb?.let { advertiser?.stopAdvertising(it) } } catch (_: SecurityException) {}
        onEvent("stopped")
    }

    /** ORIGIN: inject a fresh advisory into the mesh. */
    fun originSend(entryId: Int, slots: List<Int>, ttl: Int) {
        val pkt = Packet(dictId = 1, dictVersion = 2, entryId = entryId, slots = slots,
                         msgId = Random.nextInt(1, 65535), ttl = ttl, hop = 0)
        markSeen(pkt.msgId)
        advertiseBurst(pkt)
        onEvent("origin sent msg ${pkt.msgId} entry $entryId ttl $ttl")
    }

    @SuppressLint("MissingPermission")
    private fun startScanning() {
        val filter = ScanFilter.Builder()
            .setManufacturerData(COMPANY_ID, byteArrayOf()).build()
        val settings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY).build()
        scanCb = object : ScanCallback() {
            override fun onScanResult(type: Int, result: ScanResult) {
                val raw = result.scanRecord?.getManufacturerSpecificData(COMPANY_ID) ?: return
                val pkt = Packet.fromBytes(raw) ?: return
                onPacket(pkt)
            }
        }
        try { scanner?.startScan(listOf(filter), settings, scanCb!!) }
        catch (e: SecurityException) { onEvent("scan permission missing") }
    }

    private fun onPacket(pkt: Packet) {
        if (pkt.msgId in seen) return                        // duplicate suppressed
        forcedChainHop?.let { if (pkt.hop != it) return }    // forced-chain demo filter
        markSeen(pkt.msgId)
        onEvent("heard msg ${pkt.msgId} entry ${pkt.entryId} hop ${pkt.hop} ttl ${pkt.ttl}")
        if (role == Role.DESTINATION) { onMessage(pkt); return }
        val relayed = pkt.forRelay()
        if (!relayed.expired) {
            val jitter = Random.nextLong(120, 400)           // avoid synchronised collisions
            handler.postDelayed({ advertiseBurst(relayed) }, jitter)
        }
    }

    @SuppressLint("MissingPermission")
    private fun advertiseBurst(pkt: Packet) {
        val adv = advertiser ?: return
        advCb?.let { try { adv.stopAdvertising(it) } catch (_: SecurityException) {} }
        val data = AdvertiseData.Builder()
            .addManufacturerData(COMPANY_ID, pkt.toBytes())
            .setIncludeDeviceName(false).build()
        val settings = AdvertiseSettings.Builder()
            .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
            .setConnectable(false)
            .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH).build()
        advCb = object : AdvertiseCallback() {
            override fun onStartFailure(code: Int) { onEvent("advertise failed ($code)") }
        }
        try {
            adv.startAdvertising(settings, data, advCb)
            handler.postDelayed({ try { adv.stopAdvertising(advCb!!) } catch (_: SecurityException) {} }, 900)
        } catch (e: SecurityException) { onEvent("advertise permission missing") }
    }

    private fun markSeen(id: Int) {
        seen.add(id)
        if (seen.size > SEEN_CAP) seen.iterator().let { if (it.hasNext()) { it.next(); it.remove() } }
    }
}
