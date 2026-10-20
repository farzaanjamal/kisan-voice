# S1 — Village mesh simulation results

> **Range is a PLACEHOLDER.** RadioModel uses an optimistic outdoor range of 60 m and
> 10% base loss. Replace with your nRF RSSI-vs-distance measurements before quoting any
> number as real. All figures are mean over 20 seeds; a 1 km x 1 km
> village; real v2 binary packet size = **10 bytes** (fits a BLE advertisement).

## 1. Delivery vs density
Phones/km² needed for ≥90% delivery (placeholder range): **~200**.
See `delivery_vs_density.csv` and `delivery_vs_density.png`.

## 2. Delivery vs range & packet loss
`delivery_vs_range_loss.csv` — shorter range and higher loss both cut delivery; the
network is far more sensitive to range (topology connectivity) than to per-link loss.

## 3. Delivery & hops vs TTL
`delivery_vs_ttl.csv` / `delivery_vs_ttl.png` — delivery climbs with TTL until the
network is spanned, then flattens; average hop count keeps the message within a few hops.

## 4. Overhead per relay strategy
`overhead_by_strategy.csv` — "all relay" gives the highest delivery but the most
transmissions per delivered node (battery cost); probabilistic/designated relaying
trade a little delivery for much lower overhead.

## 5. Robustness (phones switched off)
`robustness.csv` — delivery degrades gracefully as 10/30/50% of phones go offline,
rather than collapsing — the store-and-forward flood routes around gaps.

## Assumptions and limitations (read before quoting)
- **Range is placeholder, not measured** — the single biggest caveat.
- No terrain, walls, or antenna orientation; a disc range model.
- Collision is a crude per-round penalty, not a real CSMA/BLE PHY model.
- One broadcast to the whole village; "delivery" = fraction of nodes reached.
- Phones assumed willing to relay in the foreground; real Android/iOS background BLE
  limits mean a village GATEWAY is the realistic exit, as noted in the architecture.
- Results show *relative* behaviour (how density/TTL/strategy matter), not absolute
  field performance. Calibrate with the nRF test, then re-run.
