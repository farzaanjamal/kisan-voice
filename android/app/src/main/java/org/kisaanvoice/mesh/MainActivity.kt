package org.kisaanvoice.mesh

import android.Manifest
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.view.WindowManager
import android.widget.ArrayAdapter
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import org.kisaanvoice.mesh.databinding.ActivityMainBinding
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : AppCompatActivity() {
    private lateinit var b: ActivityMainBinding
    private var mesh: BleMesh? = null
    private lateinit var dict: Dictionary
    private val log = StringBuilder()
    private val ts get() = SimpleDateFormat("HH:mm:ss", Locale.US).format(Date())

    private val perms = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { startMesh() }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        b = ActivityMainBinding.inflate(layoutInflater); setContentView(b.root)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        dict = Dictionary.fromAssets(this, "punjab_cotton_v2.json")
        event(if (Packet.selfTest()) "codec self-test OK (matches Python)" else "CODEC MISMATCH!")

        b.spinnerRole.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item,
            BleMesh.Role.values().map { it.name })

        b.btnStart.setOnClickListener { requestThenStart() }
        b.btnStop.setOnClickListener { mesh?.stop() }
        b.btnSend.setOnClickListener {
            val entry = b.editEntryId.text.toString().toIntOrNull() ?: 1
            mesh?.originSend(entry, emptyList(), ttl = 4)
        }
        b.btnShare.setOnClickListener {
            startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"; putExtra(Intent.EXTRA_TEXT, log.toString())
            }, "Share mesh log"))
        }
    }

    private fun requestThenStart() {
        val need = if (Build.VERSION.SDK_INT >= 31)
            arrayOf(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_ADVERTISE,
                    Manifest.permission.BLUETOOTH_CONNECT)
        else arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
        perms.launch(need)
    }

    private fun startMesh() {
        val nodeId = b.editNodeId.text.toString().toIntOrNull() ?: 0
        val role = BleMesh.Role.valueOf(b.spinnerRole.selectedItem as String)
        mesh = BleMesh(this, nodeId, onEvent = ::event, onMessage = ::showMessage).also { it.start(role) }
    }

    private fun showMessage(pkt: Packet) {
        val msg = dict.decode(pkt.entryId, pkt.slots, "ur") ?: "[could not decode entry ${pkt.entryId}]"
        runOnUiThread { b.txtMessage.text = msg }
        event("DELIVERED entry ${pkt.entryId}: shown to farmer")
    }

    private fun event(line: String) {
        log.append("$ts,node,$line\n")
        runOnUiThread { b.txtLog.text = log.toString() }
    }
}
