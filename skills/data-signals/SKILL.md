---
name: data-signals
description: >
  Data, Signals & Analytical Thinking skill for the SPM AI Agent.
  Use this skill when the user needs to analyze support data, identify top drivers,
  run KQL queries, build dashboards, detect anomalies, or produce trend-analysis packs.
  Triggers: "top drivers", "SAP movers", "IPD trends", "KQL", "Kusto query",
  "dashboard", "anomaly", "metrics", "trend analysis", "MTTR", "CSAT", "case volume".
---

# Data, Signals & Analytical Thinking

> *The SPM converts raw signals into actionable insights and prioritized workstreams.*

## Overview

This skill enables the agent to pull raw data from Kusto, ADO, and case systems, then transform it into actionable insights — SAP movers, trend packs, anomaly alerts, and metric snapshots. It powers the analytical backbone of every SPM cycle.

## Capabilities

1. Perform pattern and trend analysis across cases, telemetry, support signals, and product data.
2. Identify top support drivers and high-impact issues using multi-source data insights.
3. Track key metrics: Incidents Per Day (IPD), CSAT, Days To Close (DTC), Self-Help Success (SHS), and custom KPIs.
4. Convert raw signals into actionable insights and prioritized workstreams with clear owners.
5. Author, validate, and version KQL queries against Kusto clusters for incident trends, case volumes, and resolution-time distributions.
6. Build and refresh dashboard views (Power BI / Excel) aligned to QBR and business-review cadences.
7. Produce trend-analysis packs showing week-over-week and period-over-period movement of top drivers (SAP movers).
8. Detect anomalies in support-volume or MTTR metrics and raise early-warning flags.
9. Synthesize multi-source data (ADO, Kusto, case systems) into unified metric snapshots for leadership reviews.
10. Conduct competitive analysis: evaluate similar products/tools, identify differentiation gaps.
11. Conduct market analysis: size the addressable customer base, assess customer needs.
12. Compute cost/COGS impact estimates from case-volume and engineering-effort data.

## Workflow

### Step 1 — Define the Query
Identify what signal is needed (IPD trends? Top drivers? CSAT movement?) and select the data source:
- **Kusto**: `supportrptwus3prod.westus3.kusto.windows.net` / `KPISupportData`
- **ADO**: Open work items via WIQL
- **Case systems**: Via Kusto views or direct API

### Step 2 — Execute the Query
Use `spm-prototype/src/clients/kusto_client.py` for KQL or `ado_client.py` for WIQL. Apply time-range filters, product filters (PESID from `pgcss_owners.yaml`), and severity breakdowns.

Example KQL pattern:
```kql
SupportIncidents
| where ProductId in ("15922", "16757")           // AppGW, Bastion
| where CreatedTime between (ago(14d) .. now())
| summarize IPD = count() by bin(CreatedTime, 1d), ProductName
| order by CreatedTime desc
```

### Step 3 — Compute Movers
Use `spm-prototype/src/compute_movers.py` to rank drivers by volume delta (week-over-week). Flag any driver with Δ > threshold (from `settings.yaml`).

### Step 4 — Detect Anomalies
Compare current-period metrics against rolling averages. Flag:
- IPD spike > 2σ above 4-week mean
- MTTR increase > 20% period-over-period
- CSAT drop > 5 points

### Step 5 — Produce Output
Generate one or more of:
- **SAP Movers Table** (Template B from spec)
- **Trend Chart** (SVG via `generate_report.py`)
- **Metric Snapshot** (table for leadership review)
- **Signal Pack** (`signal_pack.json` with all raw + computed data)

## Integration Points

- **Kusto Client**: `spm-prototype/src/clients/kusto_client.py`
- **ADO Client**: `spm-prototype/src/clients/ado_client.py`
- **Compute Movers**: `spm-prototype/src/compute_movers.py`
- **Compute Forecast**: `spm-prototype/src/compute_forecast.py`
- **Collect Signals**: `spm-prototype/src/collect_signals.py`
- **Product Catalog**: `spm-prototype/config/settings.yaml` (PESIDs, thresholds)
- **Report Generator**: `spm-prototype/src/generate_report.py` (SVG charts, HTML output)

## Output Schema — SAP Movers Table

| Rank | Driver | Evidence | Impact | Owner | Next Step | Due | ADO Link |
|------|--------|----------|--------|-------|-----------|-----|----------|
| 1 | {{driver}} | {{Kusto query / case IDs}} | {{customer impact}} | {{owner}} | {{action}} | {{date}} | {{URL}} |

## Quality Criteria

- Every driver row has ≥ 1 evidence artifact linked
- Movers table produced with volume delta and severity distribution
- Anomaly flags raised within same cycle as detection
- KQL queries versioned and reproducible
- Data freshness: signals no older than 48 hours at time of report
