---
name: cloudnet-compass
description: >
  Cloudnet Compass — the unified Supportability Intelligence skill for Azure Networking.
  Merges all SPM operational skills (business ownership, data signals, stakeholder management,
  executive storytelling, customer experience, AI automation) with volume analytics skills
  (CX Observe tracking, ICM volume, SAP delta analysis, case clustering, forerunner alerts,
  customer notifications, newsletter narrative, weekly volume reports).
  Use this skill for ANY Azure Networking supportability task: running cycles, analyzing trends,
  identifying top drivers, managing stakeholders, generating reports, tracking volumes,
  clustering cases, drafting exec comms, or automating workflows.
  Triggers: "run cycle", "top drivers", "SAP movers", "volume check", "ICM volume",
  "case clustering", "newsletter", "forerunner alerts", "stakeholder", "RACI", "exec summary",
  "QBR", "customer experience", "deflection", "automation", "weekly report", "compass".
---

# Cloudnet Compass

> *The unified Supportability Intelligence engine for Azure Networking — from raw signals to executive action.*

---

## Overview

Cloudnet Compass is a single, composable skill that consolidates **14 capabilities** across two domains:

| Domain | Source | Capabilities |
|--------|--------|-------------|
| **SPM Operations** | SPM-Agent (Python) | Business cadence, data analysis, stakeholder management, exec comms, CX strategy, AI automation |
| **Volume Analytics** | JRVolumeCheckersAndNewsletter (Node.js) | CX Observe tracking, ICM volume, weekly reports, newsletter narrative, forerunner alerts, case clustering, SAP delta analysis, customer notifications |

---

## Module 1 — Business Ownership & Operational Cadence

> *Run the business rhythm, drive prioritization, ensure closed-loop execution.*

### Capabilities
1. Run end-to-end business rhythm: weekly syncs, bi-weekly supportability reviews, MBR/QBR cadences
2. Drive prioritization using data-backed trade-off analysis
3. Ensure closed-loop execution: assignment → owner → tracked completion → zero dropped items
4. Maintain governance over backlog, risk register, and deliverable pipeline
5. Define and track key success metrics (IPD, CSAT, DTC, SHS)
6. Persist every action item as an ADO work item with owner, due date, tags, parent linkage
7. Reconcile planned vs. actual delivery each cycle with variance commentary

### Workflow
```
Collect Signals → Compute Movers → Draft Agenda → Run Meeting
→ Capture Decisions → Persist to ADO → Distribute Recap → Carry Forward
```

### Integration
- **Pipeline**: `spm-prototype/src/run_cycle.py` (automated 6-step cycle)
- **ADO Client**: `spm-prototype/src/clients/ado_client.py`
- **Config**: `spm-prototype/config/settings.yaml`

---

## Module 2 — Data, Signals & Analytical Thinking

> *Convert raw signals into actionable insights and prioritized workstreams.*

### Capabilities
1. Pattern and trend analysis across cases, telemetry, and support signals
2. Identify top support drivers (SAP movers) with evidence and ownership
3. Track key metrics: IPD, CSAT, DTC, SHS, custom KPIs
4. Author and version KQL queries for incident trends and case volumes
5. Detect anomalies: IPD spike > 2σ, MTTR increase > 20%, CSAT drops
6. Produce trend-analysis packs with week-over-week movement
7. Synthesize multi-source data into unified metric snapshots

### Key KQL Pattern
```kql
AllCloudsSupportIncidentWithReferenceModelVNext
| where CreatedDateTime >= ago(14d)
| where DerivedProductIDStr in ("15922", "16757")  // AppGW, Bastion
| summarize IPD = count() by bin(CreatedDateTime, 1d), ProductName
| order by CreatedDateTime desc
```

### Integration
- **Kusto Client**: `spm-prototype/src/clients/kusto_client.py`
- **Compute Movers**: `spm-prototype/src/compute_movers.py`
- **Compute Forecast**: `spm-prototype/src/compute_forecast.py`
- **Collect Signals**: `spm-prototype/src/collect_signals.py`

---

## Module 3 — Volume Tracking & Anomaly Detection

> *Automated support volume and ICM queue monitoring with trend and anomaly alerts.*

### Capabilities
1. Fetch CloudNet support volume from CX Observe API (weekly granularity)
2. Fetch ICM queue volume from Power BI ICMSlowDown report (CLOUDNET\EEECloudnet)
3. Trend detection using 4-week rolling window
4. Anomaly detection: spikes/dips beyond 2σ threshold
5. Week-over-week change analysis
6. Combined weekly report generation
7. Auto-post to Teams ("Networking Supportability Team" chat)
8. Scheduled execution via Windows Task Scheduler (Tuesdays 8:00 AM)

### Usage
```bash
# CX Observe volume
node skills/volume-tracker/fetch-volume.js
node skills/volume-tracker/analyze-volume.js

# ICM volume
node skills/icm-volume/fetch-icm.js
node skills/icm-volume/analyze-icm.js

# Combined weekly report + Teams post
node skills/weekly-volume-report/run-weekly-report.js

# Schedule weekly runs
node skills/weekly-volume-report/setup-scheduler.js
```

### Data Sources
- **CX Observe API**: `support-trafficmanager-wus3-prod.trafficmanager.net/api/insights`
- **Power BI**: ICMSlowDown report (aka.ms/icmslowdown)
- **Queue**: CLOUDNET\EEECloudnet

### Output
- `data/volume-weekly.csv`, `data/volume-analysis.md`
- `data/icm-volume-weekly.csv`, `data/icm-analysis.md`
- `data/weekly-combined-report.md`

---

## Module 4 — Case Clustering & Theme Analysis

> *Automated case theme clustering and spike detection from Kusto data.*

### Capabilities
1. Query Kusto for Azure Networking support cases (31 product IDs)
2. Volume distribution by product
3. Top support topics by product + SapPath breakdown
4. Daily spike detection (weekday baseline, 1.5σ threshold)
5. Title theme clustering via keyword frequency / n-gram analysis
6. Product deep dives for top 5 products

### Usage
```bash
# Previous month (default)
node skills/case-clustering/cluster-cases.js

# ICM incident clustering
node skills/case-clustering/cluster-icm.js

# Specific month
node skills/case-clustering/cluster-cases.js 2026-05
```

### Output
- `data/case-themes-report.md` — Full analysis report
- `data/case-themes-raw.csv` — Raw case data
- `data/icm-themes-report.md` — ICM incident theme analysis

---

## Module 5 — SAP Delta Analysis

> *Month-over-month SAP volume changes with Kusto drill-down and theme clustering.*

### Capabilities
1. Scrape Power BI "Networking - SAP Deltas" report for MoM changes
2. Query Kusto for case titles per notable SapPath
3. Multi-word n-gram theme clustering per SAP
4. Delta summary table with key takeaways
5. Per-SAP deep dive breakdowns

### Usage
```bash
# Previous month
node skills/sap-delta-analysis/analyze-sap-deltas.js

# Specific month
node skills/sap-delta-analysis/analyze-sap-deltas.js 2026-04
```

### Data Sources
- **Power BI**: Networking - SAP Deltas (ICMSlowDown)
- **Kusto**: `supportrptwus3prod.westus3.kusto.windows.net` / `KPISupportData`

### Output
- `data/sap-delta-report.md`, `data/sap-delta-raw.json`

---

## Module 6 — Forerunner Alerts

> *Monthly Forerunner alert report with ICM AI summaries.*

### Capabilities
1. Scan Outlook HighPriority folder for Forerunner alert emails (from Oscar Artavia)
2. Extract ICM incident links
3. Scrape ICM portal for AI-generated summaries (Azure OpenAI)
4. Produce monthly summary table with per-alert analysis

### Usage
```bash
# Automatic (Outlook + ICM scraping)
node skills/forerunner-alerts/fetch-alerts.js

# Manual ICM IDs
node skills/forerunner-alerts/fetch-alerts.js 2026-04 \
  --icm 772566295,779114522 \
  --products "Application Gateway,Application Gateway" \
  --dates "Apr 2,Apr 14"
```

### Output
- `data/forerunner-alerts.md`, `data/forerunner-alerts.csv`

---

## Module 7 — Customer Notifications

> *Customer-facing notification correlation with support case impact.*

### Capabilities
1. Scan Outlook for "New Customer facing notification" emails from Oscar
2. Extract product details and impacted subscriber counts
3. Query Kusto for related cases within ±5 days of each notification
4. Daily case volume distribution around notification time
5. Thematic analysis on correlated cases
6. Summary table + per-notification deep dives

### Usage
```bash
# Automatic
node skills/customer-notifications/fetch-notifications.js

# Manual notifications
node skills/customer-notifications/fetch-notifications.js 2026-05 \
  --notifications "Azure Firewall|16572|2026-05-01T14:30:00Z|150"
```

### Output
- `data/customer-notifications-report.md`, `data/customer-notifications-raw.json`

---

## Module 8 — Stakeholder Management & Influence

> *Bridge PG, CSS, and engineering — influence without authority through data and impact.*

### Capabilities
1. Map stakeholder landscape from PG-CSS Owners roster (22 products, 7 roles)
2. Build RACI matrices per initiative
3. Track commitments and flag overdue responses
4. Generate stakeholder-specific follow-ups and escalation briefs
5. Facilitate alignment meetings with pre-circulated agendas

### Stakeholder Roster
| Role | Description |
|------|-------------|
| CSS TA | Technical Advisor — product technical lead in support |
| Support Planner | Owns support readiness and planning |
| CSS SPM | Supportability Program Manager — drives portfolio outcomes |
| Beta Engineer (Beta EEE) | Manages beta/preview readiness and customer-zero validation |
| Release Manager | Coordinates release readiness across CSS |
| Delivery Manager | Owns service delivery and operational metrics |

### Product Clusters
| Cluster | Support Planner | Beta EEE |
|---------|-----------------|----------|
| Layer 7 (AppGW, AFD, ATM, WAF) | Deniz Ercoskun | Oscar Artavia |
| Hybrid (ExR, Firewall, NVA, vWAN, VPN GW) | Marcin Jaworski | Brian Martin |
| Mon/Conn (Bastion, DNS, LB, NW, PL, IP Svc, NAT, NSP) | Deniz Ercoskun | Oscar Artavia |
| Virtual Networks (VNet, Net Mgr) | Deniz Ercoskun | Oscar Artavia |

### Data Source
- `spm-prototype/config/pgcss_owners.yaml` — full role-to-person mapping

---

## Module 9 — Communication & Executive Storytelling

> *Exec-ready narratives that translate technical issues into business impact.*

### Capabilities
1. Executive summaries: 2 lines + 6 bullets
2. QBR/business review slide content with linked evidence
3. Escalation briefs: problem, impact, ask, timeline — one page
4. Follow-up emails with action, owner, due date, ADO link
5. Meeting recaps within 24 hours
6. Monthly newsletter headline + narrative from IPD Dashboard data

### Executive Summary Template
```
BOTTOM LINE: {{one-sentence summary}}
SO-WHAT: {{why this matters}}

• {{metric_1}}: {{value}} ({{↑↓→}}) — {{source}}
• {{metric_2}}: {{value}} ({{↑↓→}}) — {{source}}
• {{key_risk_or_highlight}}
• ACTION: {{action}} — {{owner}} by {{date}}
• ACTION: {{action}} — {{owner}} by {{date}}
• NEXT: {{next_milestone}}
```

### Newsletter Narrative
```bash
# Generate from IPD Dashboard Power BI data
node skills/newsletter-narrative/generate-narrative.js
```

### Integration
- **Report Generator**: `spm-prototype/src/generate_report.py`
- **Email Templates**: `AGENTS_PRACHANK/` (HTML email archive)
- **Newsletter Data**: `data/newsletter-draft.md`, `data/newsletter-ipd-data.csv`

---

## Module 10 — Customer Experience & Support Strategy

> *Understand the customer journey, drive proactive prevention over reactive support.*

### Capabilities
1. End-to-end customer journey mapping (pre-ticket → resolution → follow-up)
2. Top customer-impacting issues by volume × severity
3. Case deflection strategies based on GTS coverage gaps
4. Repeat-contact pattern detection
5. Customer segment analysis and targeting
6. COGS impact estimation from case reduction

### Deflection Strategy Matrix
| Gap Type | Strategy |
|----------|----------|
| No GTS exists | Create guided troubleshooter |
| GTS low usage | Improve discoverability |
| GTS low success | Update accuracy / steps |
| Bug-driven volume | Prioritize fix (correlate ADO) |
| Config-driven volume | Improve docs / onboarding |

### Key Metrics
| Metric | Direction |
|--------|-----------|
| IPD (Incidents Per Day) | ↓ Lower |
| CSAT | ↑ Higher |
| DTC (Days To Close) | ↓ Lower |
| SHS (Self-Help Success) | ↑ Higher |
| Repeat Contact Rate | ↓ Lower |
| GTS Coverage | ↑ Higher |

---

## Module 11 — AI, Automation & Scale Thinking

> *Leverage AI and automation to reduce support demand, lower cost, and scale outcomes.*

### Capabilities
1. Evaluate workflows for AI-augmentation opportunities
2. Agent-based automation for agenda building, action tracking, recap generation
3. AI governance: source traceability, hallucination prevention, human-in-the-loop
4. Copilot prompt libraries for support engineers
5. Track AI adoption metrics and realized value
6. Maintain automation candidate backlog (effort/impact prioritized)

### Current Automation Status
| Component | Status | Stack |
|-----------|--------|-------|
| SPM Cycle Pipeline | ✅ Live | Python — `run_cycle.py` |
| Kusto Signal Collection | ✅ Live | Python — `collect_signals.py` |
| SAP Mover Computation | ✅ Live | Python — `compute_movers.py` |
| HTML Report Generation | ✅ Live | Python — `generate_report.py` |
| ADO Reconciliation | ✅ Live | Python — `reconcile_ado.py` |
| CX Observe Volume Tracking | ✅ Live | Node.js — `fetch-volume.js` |
| ICM Volume Tracking | ✅ Live | Node.js — `fetch-icm.js` |
| Weekly Volume Report + Teams | ✅ Live | Node.js — `run-weekly-report.js` |
| Newsletter Narrative | ✅ Live | Node.js — `generate-narrative.js` |
| Forerunner Alerts | ✅ Live | Node.js — `fetch-alerts.js` |
| Case Clustering | ✅ Live | Node.js — `cluster-cases.js` |
| SAP Delta Analysis | ✅ Live | Node.js — `analyze-sap-deltas.js` |
| Customer Notifications | ✅ Live | Node.js — `fetch-notifications.js` |
| Meeting Transcript Parsing | 🔲 Planned | — |
| Self-Healing Diagnostics | 🔲 Planned | — |

### Governance Guardrails
- [ ] Every AI output cites data sources
- [ ] Confidence level flagged (High / Medium / Low)
- [ ] Human-in-the-loop before external distribution
- [ ] AI-generated content marked in metadata/footer
- [ ] No PII in outputs

---

## Quick Reference — All Commands

### Python (SPM Cycle)
```bash
cd spm-prototype
python src/run_cycle.py                    # Full 6-step cycle
```

### Node.js (Volume Analytics)
```bash
# Volume tracking
node skills/volume-tracker/fetch-volume.js && node skills/volume-tracker/analyze-volume.js

# ICM volume
node skills/icm-volume/fetch-icm.js && node skills/icm-volume/analyze-icm.js

# Weekly combined report + Teams
node skills/weekly-volume-report/run-weekly-report.js

# Newsletter narrative
node skills/newsletter-narrative/generate-narrative.js

# Forerunner alerts
node skills/forerunner-alerts/fetch-alerts.js

# Case clustering
node skills/case-clustering/cluster-cases.js

# SAP delta analysis
node skills/sap-delta-analysis/analyze-sap-deltas.js

# Customer notifications
node skills/customer-notifications/fetch-notifications.js
```

### Stakeholder Lookups
```
"Who is the SPM for AppGW?"        → Gitanjali Verma
"Who is the Beta EEE for Firewall?" → Brian Martin
"List products without an SPM"      → LB, NVA, VNet, NSP, Virtual Enclaves
```

---

## Data Sources

| Source | Endpoint | Auth |
|--------|----------|------|
| Kusto | `supportrptwus3prod.westus3.kusto.windows.net` / `KPISupportData` | Azure CLI |
| ADO | `dev.azure.com/msazure/One` / Area: `One\Networking` | PAT (auto-generated) |
| CX Observe | `support-trafficmanager-wus3-prod.trafficmanager.net/api/insights` | Edge SSO |
| Power BI | IPD Dashboard, ICMSlowDown, SAP Deltas | Edge SSO |
| Outlook | HighPriority folder (Forerunner alerts, customer notifications) | Edge SSO |
| SharePoint | PG-CSS Owners list | Graph API |
| Teams | Networking Supportability Team chat | Edge SSO |

---

## Repositories

| Repo | Contents |
|------|----------|
| [CloudNet-Supportability/SPM-Agent](https://github.com/CloudNet-Supportability/SPM-Agent) | Python pipeline + config + SPM skills |
| [CloudNet-Supportability/JRVolumeCheckersAndNewsletter](https://github.com/CloudNet-Supportability/JRVolumeCheckersAndNewsletter) | Node.js volume analytics + newsletter skills |
