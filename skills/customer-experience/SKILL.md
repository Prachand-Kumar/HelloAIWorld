---
name: customer-experience
description: >
  Customer Experience & Support Strategy skill for the SPM AI Agent.
  Use this skill when the user needs to analyze customer journeys, case data,
  deflection strategies, repeat-contact patterns, or support planning.
  Triggers: "customer experience", "CX", "case deflection", "self-help",
  "CSAT", "SHS", "customer journey", "top issues", "repeat contacts",
  "support strategy", "GTS coverage", "COGS impact".
---

# Customer Experience & Support Strategy

> *The SPM deeply understands the end-to-end customer journey and drives proactive prevention over reactive support.*

## Overview

This skill focuses on understanding the customer's support experience from pre-ticket self-help through case resolution, identifying the highest-impact issues, and driving strategies that shift support left — reducing case volume through better self-help, diagnostics, and proactive prevention.

## Capabilities

1. Maintain deep understanding of the end-to-end customer journey from pre-ticket through resolution.
2. Focus on improving case resolution speed, customer satisfaction, and the pre-ticket self-help experience.
3. Drive proactive issue prevention over reactive support — shift left at every opportunity.
4. Analyze case/ticket data to identify top customer-impacting issues by volume and severity.
5. Correlate support case drivers with product bug backlogs to quantify fix-impact on customer experience.
6. Recommend case-deflection strategies based on top-driver analysis and GTS coverage gaps.
7. Surface repeat-contact patterns indicating unresolved customer pain.
8. Define customer segments and targeting: which segments are most impacted, which offer the highest leverage.
9. Design the support plan: what support channels, tools, costs, and processes are needed.
10. Develop sales and distribution strategies for supportability tools and self-help solutions.
11. Define pricing and bundling strategies for supportability offerings when applicable.
12. Create marketing strategy for supportability: events, visibility, customer outreach, and promotion.
13. Flag COGS-impact opportunities from case-reduction or efficiency initiatives.

## Workflow

### Step 1 — Assess Current State
Pull baseline metrics from Kusto and dashboards:
- **IPD** (Incidents Per Day) by product — current and trend
- **CSAT** — customer satisfaction scores
- **DTC** (Days To Close) — case resolution speed
- **SHS** (Self-Help Success) — % of customers resolving via self-help
- **Repeat Contact Rate** — customers reopening or filing duplicate cases

### Step 2 — Identify Top Customer Issues
Use the SAP movers data from the cycle output:
- Cross-reference `ipd_movers.csv` with GTS coverage status
- Identify drivers with high volume but no guided troubleshooter
- Rank by `volume × severity × (1 - GTS_coverage)` for deflection opportunity

### Step 3 — Map the Customer Journey
For each top issue, trace the customer path:
```
Pre-ticket:  Did self-help exist? → Was it findable? → Was it accurate?
Ticket:      What severity? → What product? → What resolution path?
Post-ticket: Was it resolved? → Did customer return? → CSAT score?
```

### Step 4 — Define Deflection Strategies
For each gap identified:

| Gap Type | Strategy | Example |
|----------|----------|---------|
| No GTS exists | Create guided troubleshooter | SSL cert expiry → step-by-step renewal guide |
| GTS exists but low usage | Improve discoverability | Add to portal, link from error messages |
| GTS exists but low success | Improve accuracy | Update steps, add screenshots, test with real cases |
| Bug-driven volume | Prioritize fix | Correlate with ADO bug, quantify case reduction |
| Config-driven volume | Improve docs | Create best-practices guide, onboarding checklist |

### Step 5 — Quantify COGS Impact
Estimate cost savings from deflection:
```
Cases_deflected = Current_volume × Expected_deflection_rate
Cost_savings = Cases_deflected × Avg_cost_per_case
```

### Step 6 — Report and Track
Produce outputs:
- Deflection opportunity matrix
- Customer segment analysis
- COGS impact estimates
- Recommendations with owners and timelines

## Integration Points

- **Kusto Client**: `spm-prototype/src/clients/kusto_client.py` — case data queries
- **IPD Movers**: `spm-prototype/src/compute_movers.py` — top driver identification
- **Forecast**: `spm-prototype/src/compute_forecast.py` — volume projections
- **Product Catalog**: `spm-prototype/config/settings.yaml` — PESIDs for product filtering
- **Known Issues Registry**: Cross-reference with GTS coverage status

## Key Metrics

| Metric | Definition | Good Direction |
|--------|-----------|----------------|
| IPD | Incidents per day per product | ↓ Lower |
| CSAT | Customer satisfaction (1–5 scale) | ↑ Higher |
| DTC | Days from case open to close | ↓ Lower |
| SHS | Self-Help Success rate | ↑ Higher |
| Repeat Contact Rate | % of customers with >1 case in 30 days | ↓ Lower |
| GTS Coverage | % of top drivers with guided troubleshooter | ↑ Higher |
| Case Deflection Rate | % of potential cases resolved via self-help | ↑ Higher |

## Quality Criteria

- Top customer issues identified with volume + severity data
- Deflection strategies mapped to specific gaps with owners
- COGS impact estimated with source assumptions documented
- SHS and deflection metrics tracked with trend visibility
- Customer segments defined with leverage analysis
