---
name: nebula-sme-status-report
description: "Generate a daily SME Agent status report for the Nebula Cohort 2 program and email it to Support Leadership. Use this skill whenever Prachand asks for a Nebula status report, SME Agent coverage report, daily leadership update on Cohort 2, agent build progress, or engineer coverage tracking. Also trigger when asked about who hasn't started their agent, IPD coverage, or delta/changes from the previous day's report. The deliverable is an HTML report (ready to email) plus embedded charts."
---

# Nebula SME Agent – Daily Status Report Skill

Generates a daily HTML status report for Support Leadership covering the SME Agent Nebula Cohort 2 build progress. Compares against yesterday's snapshot to surface changes (delta).

## Data Sources

### 1. Tracking Spreadsheet (Required)
SharePoint URL: `https://microsoft.sharepoint.com/:x:/t/AzureSupportVMEnablement/...`

The user must provide the Excel file. Options:
- **Download**: Open the SharePoint link → File → Download → save as `cohort2-tracker.xlsx` in the working directory
- **M365 Tool**: If WorkIQ/Graph access is available, use `workiq-ask_work_iq` to query the file

**Master Sheet columns to use:**

| Column | Meaning |
|---|---|
| SAP / SAP Path | Problem area / customer scenario |
| Nebula Phase | Rollout phase (e.g., Phase 1) |
| IPD Last 30 days | Case volume for that SAP (last 30 days) |
| SME Agent Status | TRUE = agent completed or in-progress; FALSE/empty = needs pickup |
| SME Agent Author | Name of the engineer building the agent |
| SME Agent Type | Cohort group / workload type |
| SME Agent Name | Name of the agent scenario |

### 2. Teams Channel (Optional — paste highlights)
Channel: **SME Agent for Nebula – Cohort 2**

Ask the user: "Do you have any updates from the Teams channel to include? You can paste them and I'll summarize."
If WorkIQ M365 access is available, try: `workiq-ask_work_iq` → "Summarize recent messages in the SME Agent for Nebula Cohort 2 Teams channel"

---

## Cohort Members

See `references/cohort-members.md` for the full list of members by workload group.

These are the engineers expected to appear in the **SME Agent Author** column. Anyone from the list NOT appearing in the Author column = **has not started**.

---

## Workflow

### Step 1 — Get the Excel file
If the user hasn't provided the file, ask:
> "Please download the tracker spreadsheet from SharePoint and share it here (or save it as `cohort2-tracker.xlsx` in the working directory). Alternatively, I can try to fetch a summary via M365 Copilot if that's connected."

### Step 2 — Run the report generator
```bash
python scripts/generate_report.py cohort2-tracker.xlsx
```

This script:
1. Reads the **Master** sheet from the Excel file
2. Saves a timestamped snapshot to `snapshots/` folder (for delta tracking)
3. Loads yesterday's snapshot if it exists and computes the delta
4. Calculates all metrics (see below)
5. Generates four charts (PNG, embedded in report)
6. Outputs `report_YYYYMMDD.html` — ready to email

### Step 3 — Add Teams channel summary
Paste any Teams channel highlights into the `## Teams Channel Updates` section of the report, or use WorkIQ to generate one.

### Step 4 — Send the report
Open `report_YYYYMMDD.html` in a browser → Print → Save as PDF, or paste the HTML content directly into an Outlook email.

---

## Metrics Calculated

| Metric | How |
|---|---|
| **SAP Coverage %** | `count(Status=TRUE) / total_SAPs × 100` |
| **IPD Coverage %** | `sum(IPD where Status=TRUE) / sum(all IPD) × 100` |
| **Agents Deployed vs In-Progress** | Status=TRUE + Author filled = In-Progress; treat as best proxy |
| **Engineers Not Started** | Cohort members whose name does NOT appear in Author column |
| **IPD Coverage by SME Agent Type** | Grouped sum of IPD by Agent Type where Status=TRUE |
| **Delta from Yesterday** | New TRUE statuses, new authors, IPD coverage change |

---

## Report Structure

ALWAYS use this exact structure for the HTML report:

```
# SME Agent Nebula Cohort 2 — Daily Status Report
📅 [Date] | Prepared by: Prachand Kumar | Azure Networking CSS

## 🎯 Executive Snapshot
[3-bullet summary: coverage today, delta from yesterday, top risk]

## 📊 Coverage Metrics
- SAP Coverage: X of Y SAPs (Z%)
- IPD Coverage: X of Y IPD volume (Z%)
- Agents In-Progress: N
- Engineers Not Started: N of 12

## 📈 Charts
[Chart 1: SAP Coverage Donut — TRUE vs FALSE/empty]
[Chart 2: IPD Coverage Donut — covered vs uncovered IPD]
[Chart 3: Engineer Progress Bar — started vs not-started by workload group]
[Chart 4: IPD Coverage by SME Agent Type Bar chart]

## 👥 Engineer Status
[Table: Engineer | Workload | Agent Name | Status | SAP Count]

## 🔄 Delta from Yesterday
[What changed since the previous report — new agents started, coverage change]

## 💬 Teams Channel Highlights
[Summary of key updates from "SME Agent for Nebula – Cohort 2"]

## ⚠️ Risks & Actions
[Action | Owner | Due | Impact]
```

---

## Chart Specifications

Generate using **matplotlib** and embed as base64 PNG in the HTML (no external file dependencies):

1. **SAP Coverage Donut** — TRUE count vs FALSE/empty count, with % label
2. **IPD Coverage Donut** — IPD volume covered vs uncovered
3. **Engineer Progress Bar** — grouped by workload; stacked: started / not-started
4. **IPD by Agent Type Bar** — horizontal bar chart sorted by IPD volume

Color palette:
- Completed/started: `#0078D4` (Azure blue)
- In-progress: `#50C878` (green)
- Not started: `#E0E0E0` (light grey)
- Uncovered: `#D64F3B` (red-orange)

---

## Snapshot & Delta Logic

- Snapshots saved to `snapshots/snapshot_YYYYMMDD_HHMMSS.json`
- On each run, the script finds the most recent previous snapshot
- Delta shows: new agents (Status flipped to TRUE), new authors added, coverage % change
- If no previous snapshot exists, report says "First run — baseline established"

---

## Email Formatting Tips

- Subject line: `SME Agent Nebula Cohort 2 — Status Report [DATE]`
- To: Support Leadership distribution list
- The HTML report renders well in Outlook when pasted directly
- Attach the HTML file as backup

---

## Reference Files

- `references/cohort-members.md` — Full cohort member list by workload
- `scripts/generate_report.py` — Main report generation script
- `scripts/snapshot_manager.py` — Snapshot save/load/delta logic
