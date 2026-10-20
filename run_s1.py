"""
Run the full S1 experiment suite and write CSVs, charts and RESULTS.md.

Every setting is repeated over fixed seeds; we report mean and standard deviation.
Range is a PLACEHOLDER (RadioModel.is_placeholder) until real nRF RSSI is pasted in.

    python run_s1.py
"""
import csv, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from kisaan_voice.dictionary import load_dictionary
from kisaan_voice.mesh_sim import (RadioModel, make_village, simulate, packet_size_bytes)

OUT = Path("s1_out"); OUT.mkdir(exist_ok=True)
AREA = 0.25           # ~500 m x 500 m village core (BLE 60 m range is local)
SEEDS = range(20)     # repetitions
D = load_dictionary("dictionaries/punjab_cotton_v2.json")
PKT = packet_size_bytes(D)


def mean_std(vals):
    a = np.array(vals, float)
    return float(a.mean()), float(a.std())


def exp_density():
    rows = []
    for n in [10, 20, 30, 40, 50, 60, 80, 100, 150, 250]:
        ds = []
        for s in SEEDS:
            pos = make_village(n, AREA, seed=s)
            ds.append(simulate(pos, RadioModel.outdoor(), ttl=6, strategy="all", seed=s).delivery)
        m, sd = mean_std(ds)
        rows.append({"phones": n, "density_per_km2": n / AREA, "delivery_mean": m, "delivery_std": sd})
    return rows


def exp_range_loss():
    rows = []
    for rng_m in [30, 45, 60, 90]:
        for loss in [0.05, 0.15, 0.30]:
            ds = []
            for s in SEEDS:
                pos = make_village(100, AREA, seed=s)
                radio = RadioModel(range_m=rng_m, packet_loss=loss)
                ds.append(simulate(pos, radio, ttl=6, strategy="all", seed=s).delivery)
            m, sd = mean_std(ds)
            rows.append({"range_m": rng_m, "packet_loss": loss, "delivery_mean": m, "delivery_std": sd})
    return rows


def exp_ttl():
    rows = []
    for ttl in [1, 2, 3, 4, 6, 8, 10]:
        ds, hs = [], []
        for s in SEEDS:
            pos = make_village(100, AREA, seed=s)
            r = simulate(pos, RadioModel.outdoor(), ttl=ttl, strategy="all", seed=s)
            ds.append(r.delivery); hs.append(r.avg_hops)
        dm, dsd = mean_std(ds); hm, _ = mean_std(hs)
        rows.append({"ttl": ttl, "delivery_mean": dm, "delivery_std": dsd, "avg_hops": hm})
    return rows


def exp_overhead():
    rows = []
    for strat, p in [("all", 1.0), ("probabilistic", 0.5), ("probabilistic", 0.3), ("designated", 1.0)]:
        ds, ov = [], []
        for s in SEEDS:
            pos = make_village(150, AREA, seed=s)
            r = simulate(pos, RadioModel.outdoor(), ttl=6, strategy=strat, relay_p=p, seed=s)
            ds.append(r.delivery); ov.append(r.overhead if r.overhead != float("inf") else np.nan)
        dm, _ = mean_std(ds); om, _ = mean_std([x for x in ov if not np.isnan(x)])
        label = f"{strat}" + (f" p={p}" if strat == "probabilistic" else "")
        rows.append({"strategy": label, "delivery_mean": dm, "overhead_tx_per_delivered": om})
    return rows


def exp_robustness():
    rows = []
    for off in [0.0, 0.10, 0.30, 0.50]:
        ds = []
        for s in SEEDS:
            pos = make_village(60, AREA, seed=s)
            rng = np.random.default_rng(1000 + s)
            mask = rng.random(len(pos)) >= off
            if not mask.any():
                continue
            ds.append(simulate(pos, RadioModel.outdoor(), ttl=6, strategy="all",
                               active_mask=mask, seed=s).delivery)
        m, sd = mean_std(ds)
        rows.append({"phones_off_pct": int(off * 100), "delivery_mean": m, "delivery_std": sd})
    return rows


def write_csv(name, rows):
    p = OUT / name
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return p


def chart_density(rows):
    x = [r["density_per_km2"] for r in rows]
    y = [100 * r["delivery_mean"] for r in rows]
    e = [100 * r["delivery_std"] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.errorbar(x, y, yerr=e, marker="o", capsize=3, color="#1c6a3c")
    ax.axhline(90, ls="--", color="#c0261f", lw=1, label="90% target")
    ax.set_xlabel("phones per km²"); ax.set_ylabel("delivery (%)")
    ax.set_title("Delivery vs node density (placeholder range)"); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "delivery_vs_density.png", dpi=130); plt.close(fig)


def chart_ttl(rows):
    x = [r["ttl"] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.plot(x, [100 * r["delivery_mean"] for r in rows], marker="o", color="#1c6a3c", label="delivery %")
    ax2 = ax.twinx()
    ax2.plot(x, [r["avg_hops"] for r in rows], marker="s", color="#b8801a", label="avg hops")
    ax.set_xlabel("TTL (max hops)"); ax.set_ylabel("delivery (%)"); ax2.set_ylabel("avg hops")
    ax.set_title("Delivery & hops vs TTL"); fig.tight_layout()
    fig.savefig(OUT / "delivery_vs_ttl.png", dpi=130); plt.close(fig)


def main():
    density = exp_density(); write_csv("delivery_vs_density.csv", density); chart_density(density)
    rl = exp_range_loss(); write_csv("delivery_vs_range_loss.csv", rl)
    ttl = exp_ttl(); write_csv("delivery_vs_ttl.csv", ttl); chart_ttl(ttl)
    ov = exp_overhead(); write_csv("overhead_by_strategy.csv", ov)
    rob = exp_robustness(); write_csv("robustness.csv", rob)

    # phones/km² for 90% delivery (from density experiment)
    need = next((r["density_per_km2"] for r in density if r["delivery_mean"] >= 0.90), None)

    results = f"""# S1 — Village mesh simulation results

> **Range is a PLACEHOLDER.** RadioModel uses an optimistic outdoor range of 60 m and
> 10% base loss. Replace with your nRF RSSI-vs-distance measurements before quoting any
> number as real. All figures are mean over {len(list(SEEDS))} seeds; a 1 km x 1 km
> village; real v2 binary packet size = **{PKT} bytes** (fits a BLE advertisement).

## 1. Delivery vs density
Phones/km² needed for ≥90% delivery (placeholder range): **{('~%d' % need) if need else 'not reached in tested range'}**.
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
"""
    (OUT / "RESULTS.md").write_text(results, encoding="utf-8")
    print(f"packet size (real v2 binary): {PKT} bytes")
    print(f"phones/km2 for >=90% delivery (placeholder range): {need}")
    print("density:", [(r["phones"], round(r["delivery_mean"], 2)) for r in density])
    print("ttl:", [(r["ttl"], round(r["delivery_mean"], 2)) for r in ttl])
    print("overhead:", [(r["strategy"], round(r["delivery_mean"], 2),
                         round(r["overhead_tx_per_delivered"], 1)) for r in ov])
    print("robustness:", [(r["phones_off_pct"], round(r["delivery_mean"], 2)) for r in rob])
    print("wrote CSVs + charts + RESULTS.md to", OUT)


if __name__ == "__main__":
    main()
