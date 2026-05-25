"""
Snapshot Manager — saves and loads daily snapshots for delta comparison.
Snapshots are stored as JSON in the snapshots/ folder relative to CWD.
"""

import os
import json
from datetime import datetime
from glob import glob

SNAPSHOT_DIR = "snapshots"


def save_snapshot(data: dict) -> str:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SNAPSHOT_DIR, f"snapshot_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"timestamp": ts, **data}, f, indent=2)
    return path


def load_latest_snapshot(exclude_current: bool = True) -> dict | None:
    """
    Load the most recent snapshot.
    If exclude_current is True, skips the snapshot created in this same run
    (i.e., returns the one from a previous run/day).
    """
    pattern = os.path.join(SNAPSHOT_DIR, "snapshot_*.json")
    files   = sorted(glob(pattern))

    if not files:
        return None

    # Skip the very last file if it was just written moments ago
    candidates = files[:-1] if exclude_current and len(files) > 1 else files
    if not candidates:
        return None

    with open(candidates[-1], encoding="utf-8") as f:
        return json.load(f)


def compute_delta(prev: dict, curr: dict) -> dict:
    delta = {}

    if "sap_pct" in prev and "sap_pct" in curr:
        delta["prev_sap_pct"]    = prev["sap_pct"]
        delta["curr_sap_pct"]    = curr["sap_pct"]
        delta["sap_pct_change"]  = round(curr["sap_pct"] - prev["sap_pct"], 1)

    if "ipd_pct" in prev and "ipd_pct" in curr:
        delta["prev_ipd_pct"]    = prev["ipd_pct"]
        delta["curr_ipd_pct"]    = curr["ipd_pct"]
        delta["ipd_pct_change"]  = round(curr["ipd_pct"] - prev["ipd_pct"], 1)

    prev_authors = set(prev.get("authors", []))
    curr_authors = set(curr.get("authors", []))
    delta["new_authors"]     = sorted(curr_authors - prev_authors)
    delta["removed_authors"] = sorted(prev_authors - curr_authors)

    prev_active = prev.get("active_sap", 0)
    curr_active = curr.get("active_sap", 0)
    delta["new_active_saps"] = curr_active - prev_active

    return delta


def list_snapshots() -> list[dict]:
    """Return metadata of all saved snapshots (newest first)."""
    pattern = os.path.join(SNAPSHOT_DIR, "snapshot_*.json")
    files   = sorted(glob(pattern), reverse=True)
    results = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        results.append({
            "file":      os.path.basename(f),
            "timestamp": data.get("timestamp"),
            "sap_pct":   data.get("sap_pct"),
            "ipd_pct":   data.get("ipd_pct"),
        })
    return results
