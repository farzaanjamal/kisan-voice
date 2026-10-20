# S2 — Kisaan Voice Mesh (Android relay app)

**Status: real Kotlin, NOT yet compiled or hardware-tested.** It was written outside
Android Studio (no toolchain / phones available in the build sandbox). Build it on
your machine; expect to fix small issues an IDE will flag. The binary codec, however,
is verified against the Python: `Packet.selfTest()` must print "codec self-test OK".

## What it does
A foreground BLE **managed-flooding** relay. Roles: **Origin** (injects an advisory),
**Relay** (rebroadcasts new ids with TTL-1, hop+1, duplicate cache, drop at TTL 0),
**Destination** (decodes offline from the bundled dictionary and shows the Urdu
message). Packets ride in BLE manufacturer-specific data (test company id 0xFFFF);
worst-case packet = 10 bytes, inside the 31-byte legacy advertisement.

## Build & install
1. Open `android/` in Android Studio (Giraffe+). Let it sync Gradle.
2. On each phone: enable Developer Options → USB debugging.
3. Run ▶ to install, or `./gradlew assembleDebug` and share `app-debug.apk`
   (allow "install unknown apps" on the phone).
4. Grant Bluetooth (and, on Android ≤11, Location) permissions when asked; keep BT on.
5. Uninstall afterwards: long-press the app → Uninstall.

## Test plan (feed results back into S1)
- **Self-test:** on launch the log shows "codec self-test OK (matches Python)".
- **1 hop:** phone A = Origin (node 1), phone B = Destination (node 2). A → Send →
  B shows the Urdu advisory. Record round-trip feel.
- **2 hops, forced chain:** A = Origin, B = Relay, C = Destination. Set
  `forcedChainHop` (B accepts hop 0, C accepts hop 1) so multi-hop works even with the
  phones close together; record that the chain was forced.
- **Natural chain:** same, no forcing, phones spaced ~20–40 m; record delivery.
- **Distances:** repeat at 5/10/20/30 m, indoor vs outdoor; note successes.
- Export the log (Share) → CSV; use the delivery/hop numbers to calibrate `RadioModel`
  in `run_s1.py`, then re-run S1 with real range.

## Honest limitations
- Foreground + screen-on only. Android background BLE limits make a continuous
  background mesh impractical — the production design uses a **village gateway**.
- Legacy advertising carries one small packet at a time; this is a demo flood, not a
  throughput-optimised stack.
- Forced-chain uses the hop field, not a per-packet sender id (keeps the packet format
  identical to the Python). Natural multi-hop depends on real spacing/range.
- Not tested on hardware here. The codec is the only part proven (against Python).
