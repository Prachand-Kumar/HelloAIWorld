"""
SME Agent Nebula Cohort 2 — Daily Status Report Generator
Usage: python generate_report.py <path_to_excel> [--sheet "Master"]
"""

import sys
import os
import base64
import io
import json
import re
from datetime import date, datetime
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from snapshot_manager import save_snapshot, load_latest_snapshot, compute_delta

# ── Cohort members by workload ──────────────────────────────────────────────
COHORT_MEMBERS = {
    "VNet":         ["Saketh Tubati", "Srinath Kotagiri"],
    "AppGW/WAF":    ["Rikesh Saner", "David Ramsay", "Zach Cabrera"],
    "Load Balancer":["Tony Bart"],
    "Hybrid":       ["Ariel Esquivel", "Diego Garro", "Bryan Aguilar",
                     "Kris Martin", "Christian Mailhe", "Swati Sharma", "Kyle Fox"],
}
ALL_MEMBERS = [m for members in COHORT_MEMBERS.values() for m in members]

# ── Azure brand colours ──────────────────────────────────────────────────────
AZ_BLUE    = "#0078D4"
AZ_GREEN   = "#50C878"
AZ_GREY    = "#E0E0E0"
AZ_RED     = "#D64F3B"
AZ_YELLOW  = "#FFB900"


# ── Helpers ──────────────────────────────────────────────────────────────────

def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def normalise_bool(val) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().upper() == "TRUE"
    if isinstance(val, (int, float)):
        return bool(val)
    return False


def member_key(name: str) -> str:
    """Lowercase, strip for fuzzy matching."""
    return name.strip().lower() if isinstance(name, str) else ""


# ── Load & clean data ────────────────────────────────────────────────────────

def load_master(path: str, sheet: str = "Master") -> pd.DataFrame:
    try:
        df = pd.read_excel(path, sheet_name=sheet)
    except Exception:
        # Fall back to first sheet
        df = pd.read_excel(path, sheet_name=0)

    # Normalise column names — strip whitespace
    df.columns = [str(c).strip() for c in df.columns]

    # Rename to canonical names for convenience
    rename = {}
    for col in df.columns:
        low = col.lower()
        if "sap" in low and "path" in low:
            rename[col] = "SAP_Path"
        elif col.lower() == "sap":
            rename[col] = "SAP_Path"
        elif "nebula" in low and "phase" in low:
            rename[col] = "Nebula_Phase"
        elif "ipd" in low and "30" in low:
            rename[col] = "IPD_30"
        elif "sme" in low and "agent" in low and "status" in low:
            rename[col] = "Agent_Status"
        elif "sme" in low and "author" in low:
            rename[col] = "Agent_Author"
        elif "sme" in low and "type" in low:
            rename[col] = "Agent_Type"
        elif "sme" in low and "name" in low:
            rename[col] = "Agent_Name"
    df.rename(columns=rename, inplace=True)

    # Ensure required columns exist
    for req in ["Agent_Status"]:
        if req not in df.columns:
            raise ValueError(f"Could not find column mapping for '{req}'. Columns found: {list(df.columns)}")

    df["Agent_Status_Bool"] = df["Agent_Status"].apply(normalise_bool)
    df["IPD_30"] = pd.to_numeric(df.get("IPD_30", pd.Series(dtype=float)), errors="coerce").fillna(0)

    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)
    return df


# ── Metrics ──────────────────────────────────────────────────────────────────

def calc_metrics(df: pd.DataFrame) -> dict:
    total_sap   = len(df)
    active_sap  = df["Agent_Status_Bool"].sum()
    total_ipd   = df["IPD_30"].sum()
    covered_ipd = df.loc[df["Agent_Status_Bool"], "IPD_30"].sum()

    sap_pct = round(active_sap / total_sap * 100, 1) if total_sap else 0
    ipd_pct = round(covered_ipd / total_ipd * 100, 1) if total_ipd else 0

    # Engineers who appear as author
    authors_raw = df.get("Agent_Author", pd.Series(dtype=str)).dropna()
    authors_found = set(member_key(a) for a in authors_raw)

    started   = [m for m in ALL_MEMBERS if member_key(m) in authors_found]
    not_started = [m for m in ALL_MEMBERS if member_key(m) not in authors_found]

    # Per-engineer summary
    eng_summary = []
    for group, members in COHORT_MEMBERS.items():
        for m in members:
            rows = df[df.get("Agent_Author", pd.Series(dtype=str))
                        .apply(lambda x: member_key(x) == member_key(m))]
            eng_summary.append({
                "engineer": m,
                "workload": group,
                "agent_count": len(rows),
                "agent_names": "; ".join(rows.get("Agent_Name", pd.Series(dtype=str)).dropna().tolist()),
                "status": "Started" if len(rows) > 0 else "Not Started",
            })

    # IPD by Agent Type
    if "Agent_Type" in df.columns:
        ipd_by_type = (
            df[df["Agent_Status_Bool"]]
            .groupby("Agent_Type")["IPD_30"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )
    else:
        ipd_by_type = {}

    return {
        "total_sap":     int(total_sap),
        "active_sap":    int(active_sap),
        "inactive_sap":  int(total_sap - active_sap),
        "sap_pct":       sap_pct,
        "total_ipd":     float(total_ipd),
        "covered_ipd":   float(covered_ipd),
        "ipd_pct":       ipd_pct,
        "started":       started,
        "not_started":   not_started,
        "eng_summary":   eng_summary,
        "ipd_by_type":   ipd_by_type,
    }


# ── Charts ───────────────────────────────────────────────────────────────────

def chart_sap_donut(m: dict) -> str:
    fig, ax = plt.subplots(figsize=(4, 4))
    sizes  = [m["active_sap"], m["inactive_sap"]]
    colors = [AZ_BLUE, AZ_GREY]
    wedges, _ = ax.pie(sizes, colors=colors, startangle=90,
                       wedgeprops=dict(width=0.55))
    ax.text(0, 0, f'{m["sap_pct"]}%', ha="center", va="center",
            fontsize=22, fontweight="bold", color=AZ_BLUE)
    ax.set_title("SAP Coverage", fontsize=13, fontweight="bold", pad=12)
    legend = [mpatches.Patch(color=AZ_BLUE, label=f'Active ({m["active_sap"]})'),
              mpatches.Patch(color=AZ_GREY, label=f'Not started ({m["inactive_sap"]})')]
    ax.legend(handles=legend, loc="lower center", fontsize=9, frameon=False)
    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)
    return b64


def chart_ipd_donut(m: dict) -> str:
    fig, ax = plt.subplots(figsize=(4, 4))
    covered   = m["covered_ipd"]
    uncovered = m["total_ipd"] - covered
    sizes  = [covered, uncovered] if covered + uncovered > 0 else [1, 0]
    colors = [AZ_GREEN, AZ_RED]
    ax.pie(sizes, colors=colors, startangle=90,
           wedgeprops=dict(width=0.55))
    ax.text(0, 0, f'{m["ipd_pct"]}%', ha="center", va="center",
            fontsize=22, fontweight="bold", color=AZ_GREEN)
    ax.set_title("IPD Volume Coverage", fontsize=13, fontweight="bold", pad=12)
    legend = [
        mpatches.Patch(color=AZ_GREEN, label=f'Covered ({int(covered):,})'),
        mpatches.Patch(color=AZ_RED,   label=f'Uncovered ({int(uncovered):,})'),
    ]
    ax.legend(handles=legend, loc="lower center", fontsize=9, frameon=False)
    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)
    return b64


def chart_engineer_progress(m: dict) -> str:
    groups = list(COHORT_MEMBERS.keys())
    started_counts    = []
    not_started_counts = []
    for g in groups:
        members = COHORT_MEMBERS[g]
        s   = sum(1 for e in m["eng_summary"] if e["workload"] == g and e["status"] == "Started")
        ns  = sum(1 for e in m["eng_summary"] if e["workload"] == g and e["status"] == "Not Started")
        started_counts.append(s)
        not_started_counts.append(ns)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    x = range(len(groups))
    bars1 = ax.bar(x, started_counts,    color=AZ_BLUE,  label="Started",     width=0.45)
    bars2 = ax.bar(x, not_started_counts, color=AZ_GREY, label="Not Started", width=0.45,
                   bottom=started_counts)
    ax.set_xticks(list(x))
    ax.set_xticklabels(groups, fontsize=9)
    ax.set_ylabel("Engineers", fontsize=9)
    ax.set_title("Engineer Progress by Workload", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9, frameon=False)

    for bar, val in zip(bars1, started_counts):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                    str(val), ha="center", va="center", fontsize=9, color="white", fontweight="bold")

    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)
    return b64


def chart_ipd_by_type(m: dict) -> str:
    ipd_by_type = m["ipd_by_type"]
    if not ipd_by_type:
        return ""

    labels = list(ipd_by_type.keys())
    values = [ipd_by_type[k] for k in labels]

    fig, ax = plt.subplots(figsize=(6, max(3, len(labels) * 0.5 + 1)))
    colors = [AZ_BLUE if i % 2 == 0 else "#005A9E" for i in range(len(labels))]
    bars = ax.barh(labels, values, color=colors)
    ax.set_xlabel("IPD Volume (Last 30 days)", fontsize=9)
    ax.set_title("IPD Coverage by SME Agent Type", fontsize=13, fontweight="bold")
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height()/2,
                f'{int(val):,}', va="center", fontsize=8)
    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)
    return b64


# ── HTML Report ──────────────────────────────────────────────────────────────

def img_tag(b64: str) -> str:
    if not b64:
        return "<p><em>Chart not available (no Agent Type data)</em></p>"
    return f'<img src="data:image/png;base64,{b64}" style="max-width:480px;border-radius:8px;">'


def delta_section(delta: dict | None) -> str:
    if delta is None:
        return "<p><em>First run — baseline established today.</em></p>"
    rows = []
    if delta.get("sap_pct_change") is not None:
        sign = "+" if delta["sap_pct_change"] >= 0 else ""
        rows.append(f"<li>SAP Coverage: <strong>{sign}{delta['sap_pct_change']:.1f}pp</strong> "
                    f"({delta['prev_sap_pct']}% → {delta['curr_sap_pct']}%)</li>")
    if delta.get("ipd_pct_change") is not None:
        sign = "+" if delta["ipd_pct_change"] >= 0 else ""
        rows.append(f"<li>IPD Coverage: <strong>{sign}{delta['ipd_pct_change']:.1f}pp</strong> "
                    f"({delta['prev_ipd_pct']}% → {delta['curr_ipd_pct']}%)</li>")
    if delta.get("new_authors"):
        rows.append(f"<li>New engineers started: <strong>{', '.join(delta['new_authors'])}</strong></li>")
    if delta.get("new_active_saps"):
        rows.append(f"<li>New SAPs activated: <strong>{delta['new_active_saps']}</strong></li>")
    if not rows:
        rows.append("<li>No changes detected since last snapshot.</li>")
    return "<ul>" + "".join(rows) + "</ul>"


def eng_table(eng_summary: list) -> str:
    rows = ""
    for e in eng_summary:
        status_style = 'color:#0078D4;font-weight:bold' if e["status"] == "Started" else 'color:#999'
        agent_names = e["agent_names"] if e["agent_names"] else "—"
        rows += (f'<tr><td>{e["engineer"]}</td><td>{e["workload"]}</td>'
                 f'<td>{e["agent_count"]}</td><td>{agent_names}</td>'
                 f'<td style="{status_style}">{e["status"]}</td></tr>')
    return rows


def build_html(m: dict, delta: dict | None, charts: dict,
               report_date: str, teams_highlights: str = "") -> str:
    not_started_list = ", ".join(m["not_started"]) if m["not_started"] else "All engineers have started ✅"

    delta_html = delta_section(delta)

    teams_html = (f"<p>{teams_highlights}</p>"
                  if teams_highlights
                  else "<p><em>No Teams channel updates provided. Paste highlights here or use M365 Copilot to fetch them.</em></p>")

    # Executive snapshot bullets
    delta_bullet = ""
    if delta:
        sign = "+" if delta.get("sap_pct_change", 0) >= 0 else ""
        delta_bullet = f"SAP coverage moved {sign}{delta.get('sap_pct_change', 0):.1f}pp vs yesterday."
    risk_bullet = (f"{len(m['not_started'])} of {len(ALL_MEMBERS)} engineers have not yet started."
                   if m["not_started"] else "All engineers have started their agents.")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Segoe UI, Arial, sans-serif; color:#1a1a1a; max-width:900px; margin:auto; padding:24px; }}
  h1   {{ color:#0078D4; border-bottom:3px solid #0078D4; padding-bottom:8px; }}
  h2   {{ color:#005A9E; margin-top:32px; }}
  .badge {{ display:inline-block; padding:4px 12px; border-radius:12px; font-weight:bold; font-size:0.85em; }}
  .blue  {{ background:#E6F3FB; color:#0078D4; }}
  .green {{ background:#E8F8EE; color:#107C10; }}
  .red   {{ background:#FDE9E7; color:#D64F3B; }}
  .grey  {{ background:#F4F4F4; color:#555; }}
  table  {{ border-collapse:collapse; width:100%; margin-top:12px; }}
  th     {{ background:#0078D4; color:white; padding:8px 12px; text-align:left; font-size:0.9em; }}
  td     {{ padding:7px 12px; border-bottom:1px solid #E5E5E5; font-size:0.88em; }}
  tr:hover td {{ background:#F4F9FF; }}
  .metric-box {{ display:inline-block; border:1px solid #DDD; border-radius:8px;
                 padding:14px 20px; margin:6px; text-align:center; min-width:140px; }}
  .metric-box .val {{ font-size:2em; font-weight:bold; color:#0078D4; }}
  .metric-box .lbl {{ font-size:0.8em; color:#666; margin-top:4px; }}
  .charts {{ display:flex; flex-wrap:wrap; gap:16px; margin-top:16px; }}
  .section {{ background:#FAFAFA; border-left:4px solid #0078D4;
              padding:12px 16px; border-radius:4px; margin-top:8px; }}
  .not-started {{ color:#D64F3B; font-weight:bold; }}
</style>
</head>
<body>

<h1>📊 SME Agent Nebula Cohort 2 — Daily Status Report</h1>
<p>📅 <strong>{report_date}</strong> &nbsp;|&nbsp; Prepared by: <strong>Prachand Kumar</strong> &nbsp;|&nbsp; Azure Networking CSS — Supportability PM</p>

<h2>🎯 Executive Snapshot</h2>
<div class="section">
  <ul>
    <li>SAP Coverage: <strong>{m["sap_pct"]}%</strong> ({m["active_sap"]} of {m["total_sap"]} scenarios have an agent in-scope)</li>
    <li>IPD Coverage: <strong>{m["ipd_pct"]}%</strong> of total case volume ({int(m["covered_ipd"]):,} of {int(m["total_ipd"]):,} IPD)</li>
    <li>{delta_bullet if delta_bullet else "First run — baseline established."}</li>
    <li>⚠️ {risk_bullet}</li>
  </ul>
</div>

<h2>📊 Coverage Metrics</h2>
<div>
  <div class="metric-box"><div class="val">{m["sap_pct"]}%</div><div class="lbl">SAP Coverage</div></div>
  <div class="metric-box"><div class="val">{m["ipd_pct"]}%</div><div class="lbl">IPD Coverage</div></div>
  <div class="metric-box"><div class="val">{m["active_sap"]}</div><div class="lbl">Agents Active / In-Scope</div></div>
  <div class="metric-box"><div class="val">{len(m["started"])} / {len(ALL_MEMBERS)}</div><div class="lbl">Engineers Started</div></div>
</div>

<h2>📈 Visual Summary</h2>
<div class="charts">
  <div>{img_tag(charts.get("sap_donut",""))}</div>
  <div>{img_tag(charts.get("ipd_donut",""))}</div>
  <div>{img_tag(charts.get("eng_progress",""))}</div>
  <div>{img_tag(charts.get("ipd_type",""))}</div>
</div>

<h2>👥 Engineer Status</h2>
<table>
  <thead><tr>
    <th>Engineer</th><th>Workload</th><th>Agents</th><th>Agent Name(s)</th><th>Status</th>
  </tr></thead>
  <tbody>{eng_table(m["eng_summary"])}</tbody>
</table>

<p><strong>Not started:</strong>
  <span class="{'not-started' if m['not_started'] else ''}">{not_started_list}</span>
</p>

<h2>🔄 Delta from Yesterday</h2>
{delta_html}

<h2>💬 Teams Channel Highlights</h2>
<div class="section">{teams_html}</div>

<h2>⚠️ Risks &amp; Recommended Actions</h2>
<table>
  <thead><tr><th>Action</th><th>Owner</th><th>Due</th><th>Impact</th></tr></thead>
  <tbody>
    {''.join(f'<tr><td>Follow up with {e} to start agent build</td><td>Prachand Kumar</td><td>This week</td><td>Coverage gap</td></tr>' for e in m["not_started"])}
    <tr><td>Review agents with Status=TRUE but no Agent Name</td><td>Prachand Kumar</td><td>Next standup</td><td>Data quality</td></tr>
  </tbody>
</table>

<hr style="margin-top:40px;border-color:#EEE;">
<p style="font-size:0.75em;color:#999;">Auto-generated by the Nebula SME Agent Status Report skill &nbsp;|&nbsp; {datetime.now().strftime("%Y-%m-%d %H:%M")} local time</p>
</body>
</html>"""
    return html


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <excel_file> [--sheet <sheet_name>] [--teams '<text>']")
        sys.exit(1)

    excel_path = sys.argv[1]
    sheet_name = "Master"
    teams_text = ""

    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--sheet" and i + 1 < len(sys.argv):
            sheet_name = sys.argv[i + 1]
        if arg == "--teams" and i + 1 < len(sys.argv):
            teams_text = sys.argv[i + 1]

    print(f"📂 Loading: {excel_path} (sheet: {sheet_name})")
    df = load_master(excel_path, sheet_name)
    print(f"   {len(df)} rows loaded")

    metrics = calc_metrics(df)

    # Snapshot & delta
    snapshot_data = {
        "sap_pct":    metrics["sap_pct"],
        "ipd_pct":    metrics["ipd_pct"],
        "active_sap": metrics["active_sap"],
        "authors":    [e["engineer"] for e in metrics["eng_summary"] if e["status"] == "Started"],
    }
    prev = load_latest_snapshot()
    save_snapshot(snapshot_data)
    delta = compute_delta(prev, snapshot_data) if prev else None

    if delta:
        print(f"📊 Delta: SAP {delta.get('sap_pct_change',0):+.1f}pp | IPD {delta.get('ipd_pct_change',0):+.1f}pp")

    # Charts
    charts = {
        "sap_donut":    chart_sap_donut(metrics),
        "ipd_donut":    chart_ipd_donut(metrics),
        "eng_progress": chart_engineer_progress(metrics),
        "ipd_type":     chart_ipd_by_type(metrics),
    }

    today = date.today().strftime("%B %d, %Y")
    html  = build_html(metrics, delta, charts, today, teams_text)

    out_name = f"report_{date.today().strftime('%Y%m%d')}.html"
    with open(out_name, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ Report saved: {out_name}")
    print(f"   SAP Coverage : {metrics['sap_pct']}% ({metrics['active_sap']}/{metrics['total_sap']})")
    print(f"   IPD Coverage : {metrics['ipd_pct']}% ({int(metrics['covered_ipd']):,}/{int(metrics['total_ipd']):,})")
    print(f"   Not started  : {', '.join(metrics['not_started']) if metrics['not_started'] else 'None — all started!'}")


if __name__ == "__main__":
    main()
