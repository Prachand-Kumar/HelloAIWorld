---
name: business-ownership
description: >
  Business Ownership & Operational Cadence skill for the SPM AI Agent.
  Use this skill when the user needs to run the business rhythm, drive prioritization,
  ensure closed-loop execution, manage backlogs, track risk, or produce operational
  reports. Triggers: "run cycle", "agenda", "carry-forward", "reconcile ADO",
  "action tracker", "business review", "MBR", "QBR", "cadence".
---

# Business Ownership & Operational Cadence

> *The SPM runs the business rhythm, drives prioritization, and ensures closed-loop execution.*

## Overview

This skill covers the end-to-end operational cadence of an SPM — from running weekly/bi-weekly syncs and MBR/QBR reviews, to tracking every action item through assignment → completion, and ensuring nothing is dropped. It integrates with ADO for work-item persistence and with the SPM cycle pipeline for automated data collection.

## Capabilities

1. Run the end-to-end business rhythm: weekly syncs, bi-weekly supportability reviews, MBR/QBR cadences, and leadership reviews.
2. Drive prioritization and decision-making using data-backed trade-off analysis across competing workstreams.
3. Ensure closed-loop execution: every action flows from assignment → owner → tracked completion, with no dropped items.
4. Maintain strong governance over the backlog, risk register, and deliverable pipeline.
5. Define and track key success metrics that measure health, growth, and impact of the supportability portfolio.
6. Create and distribute reports aligned to success metrics at the cadence expected by each stakeholder tier.
7. Review metric trends, judge what the data signals, and take corrective actions — accelerate, pivot, or escalate.
8. Manage risk proactively: identify problems customers will have, anticipate criticism, and define mitigation plans.
9. Persist every action item as an ADO work item with owner, due date, tags, and parent linkage.
10. Reconcile planned vs. actual delivery each cycle and produce variance commentary.

## Workflow

### Step 1 — Collect Signals
Pull data from ADO (open work items, carry-forwards), Kusto (IPD trends, case volumes), email threads, and meeting notes. Use `spm-prototype/src/collect_signals.py` or the full `run_cycle.py` pipeline.

### Step 2 — Build the Agenda
Instantiate the bi-weekly agenda template with collected data:
- Roll Call & Logistics
- Previous Actions Review (carry-forward table)
- SAP Movers (top support drivers)
- Operational Readiness & Change Updates
- Metrics & Trends Snapshot
- AI / Automation Updates
- New Business & Open Floor
- Decisions & Actions Recap

### Step 3 — Run the Meeting
Track time-boxed sections, capture decisions and actions in real time, flag carry-forward items, alert when sections exceed allotted time.

### Step 4 — Persist to ADO
Create or update ADO work items for every action, decision, and carry-forward. Tag items with `SAP-mover`, `carry-forward`, severity. Link parent items.

### Step 5 — Distribute Recap
Generate executive summary (Template E), follow-up emails (Template F), and distribute within 24 hours.

### Step 6 — Carry-Forward
Increment carry-forward counts, flag items exceeding 3 cycles, archive completed items, generate variance report.

## Integration Points

- **SPM Prototype Pipeline**: `spm-prototype/src/run_cycle.py` — automated cycle execution
- **ADO Client**: `spm-prototype/src/clients/ado_client.py` — WIQL queries, work item CRUD
- **Kusto Client**: `spm-prototype/src/clients/kusto_client.py` — KQL execution
- **Config**: `spm-prototype/config/settings.yaml` — product catalog, thresholds
- **Stakeholders**: `spm-prototype/config/pgcss_owners.yaml` — role-to-person mapping

## Quality Criteria

- 100% of actions have Owner + Due Date in ADO
- Every carry-forward item accounted for (Done, Carried, or Cancelled with rationale)
- Agenda distributed ≥ 24 hours before scheduled meeting
- Recap distributed within 24 hours of meeting close
- Zero dropped actions (reconciliation delta = 0)

## Templates

### Agenda Template
See `spm-prototype/src/draft_agenda.py` and SPM-AI-Agent-Spec.md Template A.

### Carry-Forward Tracker
| # | Action | Owner | Original Due | Cycle Count | Status | Blocker |
|---|--------|-------|-------------|-------------|--------|---------|
| 1 | {{action}} | {{owner}} | {{date}} | {{n}} | {{Open/Done/Blocked}} | {{blocker or "—"}} |

### Decision Log
| # | Decision | Date | Owner | Rationale | Follow-ups |
|---|----------|------|-------|-----------|------------|
| 1 | {{decision}} | {{date}} | {{owner}} | {{why}} | {{actions}} |
