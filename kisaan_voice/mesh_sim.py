"""
S1 — village-scale BLE managed-flooding simulator.

Honest scope: this models *message propagation over a topology* (who relays, TTL,
duplicate suppression, packet loss, a simple collision penalty). It does NOT model
the radio physically. Range here is a PLACEHOLDER until the nRF two-phone RSSI test
is pasted in (see RadioModel). Packet SIZE is taken from the real v2 binary encoder,
so the "does it fit / airtime" reasoning is grounded; delivery itself depends on
topology + strategy, not on the 1-2 bytes of size variation.

Managed flooding (as in Bluetooth Mesh): a node that hears a NEW message id
rebroadcasts it once (after random jitter) with TTL-1, keeps a duplicate cache, and
drops it at TTL 0. We compare three relay strategies and stress the network.
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .encoding import encode_binary
from .dictionary import Dictionary


# ----------------------------- radio -----------------------------
@dataclass
class RadioModel:
    """PLACEHOLDER link model. Replace range_m from a real RSSI-vs-distance test.

    A link exists if distance <= range_m; each delivery then succeeds with
    probability (1 - packet_loss), reduced further when many neighbours transmit
    in the same round (a crude collision penalty).
    """
    range_m: float = 60.0          # outdoor BLE adv, optimistic placeholder
    packet_loss: float = 0.10      # per-link base loss
    collision_penalty: float = 0.08  # extra loss per concurrent transmitter in range
    is_placeholder: bool = True

    @classmethod
    def outdoor(cls): return cls(range_m=60.0, packet_loss=0.10)
    @classmethod
    def indoor(cls):  return cls(range_m=15.0, packet_loss=0.20)


# ----------------------------- village -----------------------------
def make_village(n: int, area_km: float, seed: int,
                 cluster_frac: float = 0.3) -> np.ndarray:
    """Positions (metres) for n phones in an area_km x area_km square:
    most households clustered in a settlement core, the rest scattered as field
    nodes. Clusters are broad and few so the settlement stays one connected mass
    (a tight-but-separated set of clusters would fragment the graph artificially)."""
    rng = np.random.default_rng(seed)
    side = area_km * 1000.0
    n_cluster = int(n * cluster_frac)
    n_field = n - n_cluster
    n_houses = max(1, n_cluster // 20)              # few, broad clusters
    centres = rng.uniform(side * 0.2, side * 0.8, size=(n_houses, 2))  # near the core
    idx = rng.integers(0, n_houses, size=n_cluster)
    clustered = np.clip(centres[idx] + rng.normal(0, side * 0.09, size=(n_cluster, 2)), 0, side)
    scattered = rng.uniform(0, side, size=(n_field, 2))
    return np.vstack([clustered, scattered])


def adjacency(pos: np.ndarray, range_m: float) -> List[np.ndarray]:
    """Neighbour index lists by Euclidean range."""
    d = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    return [np.where(row <= range_m)[0] for row in d]


# ----------------------------- simulate -----------------------------
@dataclass
class SimResult:
    delivery: float            # fraction of nodes that received
    avg_hops: float
    max_hops: int
    transmissions: int
    overhead: float            # transmissions per delivered node
    rounds: int
    trace: list = field(default_factory=list)   # per-round newly-reached (for animation)


def simulate(pos: np.ndarray, radio: RadioModel, ttl: int, strategy: str = "all",
             relay_p: float = 1.0, designated_frac: float = 0.2,
             active_mask: np.ndarray | None = None, seed: int = 0,
             record_trace: bool = False) -> SimResult:
    n = len(pos)
    rng = np.random.default_rng(seed)
    nbrs = adjacency(pos, radio.range_m)
    if active_mask is None:
        active_mask = np.ones(n, bool)
    designated = rng.random(n) < designated_frac

    received = np.zeros(n, bool)
    hops = np.full(n, -1)
    origin = int(np.argmax(active_mask))     # first active node
    received[origin] = True; hops[origin] = 0
    to_transmit = [origin]
    transmissions = 0
    rounds = 0
    trace = [[origin]] if record_trace else []

    while to_transmit:
        rounds += 1
        # transmitter set this round, filtered by strategy
        txers = []
        for u in to_transmit:
            if hops[u] >= ttl:            # no hops left
                continue
            if strategy == "probabilistic" and rng.random() > relay_p and u != origin:
                continue
            if strategy == "designated" and not designated[u] and u != origin:
                continue
            txers.append(u)
        # count concurrent transmitters in range of each node (for collision)
        tx_in_range = np.zeros(n, int)
        for u in txers:
            tx_in_range[nbrs[u]] += 1
        newly = []
        for u in txers:
            transmissions += 1
            for v in nbrs[u]:
                if received[v] or not active_mask[v]:
                    continue
                loss = radio.packet_loss + radio.collision_penalty * max(0, tx_in_range[v] - 1)
                if rng.random() > min(0.95, loss):   # delivery succeeds
                    received[v] = True
                    hops[v] = hops[u] + 1
                    newly.append(v)
        if record_trace:
            trace.append(newly)
        to_transmit = newly

    reached = received & active_mask
    n_active = int(active_mask.sum())
    delivered = int(reached.sum())
    hop_vals = hops[reached & (hops > 0)]
    return SimResult(
        delivery=delivered / n_active if n_active else 0.0,
        avg_hops=float(hop_vals.mean()) if len(hop_vals) else 0.0,
        max_hops=int(hop_vals.max()) if len(hop_vals) else 0,
        transmissions=transmissions,
        overhead=transmissions / delivered if delivered else float("inf"),
        rounds=rounds, trace=trace,
    )


def packet_size_bytes(d: Dictionary) -> int:
    """Real worst-case v2 binary packet size, to ground airtime claims."""
    worst = 0
    for e in d.entries:
        vals = {s["name"]: s.get("max", 1) for s in e.get("slots", [])}
        worst = max(worst, len(encode_binary(d, e["id"], vals or None, msg_id=65535, ttl=7, hop=7)))
    return worst
