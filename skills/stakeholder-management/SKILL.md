---
name: stakeholder-management
description: >
  Stakeholder Management & Influence skill for the SPM AI Agent.
  Use this skill when the user needs to map stakeholders, build RACI matrices,
  track commitments, prepare alignment meetings, or drive cross-org influence.
  Triggers: "stakeholder", "RACI", "who owns", "PG-CSS owners", "vTeam",
  "alignment", "escalation", "follow-up", "accountability".
---

# Stakeholder Management & Influence

> *The SPM acts as a bridge across PG, CSS, and engineering — influencing without authority through data and impact.*

## Overview

This skill enables the agent to map stakeholder landscapes, maintain RACI matrices, track commitments, and drive cross-functional alignment. It leverages the PG-CSS Owners roster to answer "who owns what" instantly and ensures no stakeholder commitment goes untracked.

## Capabilities

1. Define and map the stakeholder landscape: leadership team, sponsors, developers, customers, VIPs, and partners.
2. Map RACI responsibilities per initiative and maintain a stakeholder contact map (role, area, preferred channel).
3. Act as the bridge between Product Group (PG), CSS, and engineering — driving alignment across organizational boundaries.
4. Hold teams accountable for supportability outcomes using data-backed progress tracking.
5. Drive alignment across cross-functional vTeams; mediate priority conflicts with trade-off analysis.
6. Influence without authority: use data and business impact narratives to move decisions.
7. Create and maintain partnerships and integrations across organizations for shared outcomes.
8. Inform stakeholders proactively: update leadership on strategic plans, successes, and opportunities.
9. Track stakeholder commitments and flag overdue responses before escalation windows close.
10. Facilitate alignment meetings with pre-circulated agendas and post-meeting recaps.

## Workflow

### Step 1 — Identify the Stakeholder Question
Determine what the user needs:
- **Lookup**: "Who is the SPM for AppGW?" → query `pgcss_owners.yaml`
- **RACI Build**: Map roles to a specific initiative
- **Commitment Tracking**: Check overdue follow-ups in ADO
- **Alignment Prep**: Generate pre-meeting agenda for a stakeholder group

### Step 2 — Query the Roster
Use `spm-prototype/config/pgcss_owners.yaml` for Azure Networking stakeholders:

| Role | Description |
|------|-------------|
| CSS TA | CSS Technical Advisor — the product's technical lead in support |
| Support Planner | Owns support readiness and planning for the product |
| CSS SPM | Supportability Program Manager — drives portfolio outcomes |
| Beta Engineer (Beta EEE) | Manages beta/preview readiness and customer-zero validation |
| Release Manager | Coordinates release readiness across CSS |
| Delivery Manager | Owns service delivery and operational metrics |

### Step 3 — Build the RACI
For any initiative, map stakeholders from the roster to RACI roles:

| Activity | Responsible | Accountable | Consulted | Informed |
|----------|-------------|-------------|-----------|----------|
| {{activity}} | {{who does the work}} | {{who approves}} | {{who provides input}} | {{who is kept updated}} |

### Step 4 — Track Commitments
Query ADO for action items assigned to stakeholders. Flag:
- Items past due date with no update
- Items approaching due date without progress
- Items carried forward > 2 cycles

### Step 5 — Generate Communications
Produce stakeholder-specific follow-ups:
- Owner-specific action reminders
- Pre-meeting agendas with stakeholder-relevant items highlighted
- Escalation briefs for blocked items

## Data Sources

- **PG-CSS Owners**: `spm-prototype/config/pgcss_owners.yaml` — 22 Azure Networking products with all role assignments
- **Repo Memory**: `/memories/repo/networking-pgcss-owners.md` — quick-reference copy
- **SharePoint Source**: `https://microsoft.sharepoint.com/teams/SupportabilityChecklist579/Lists/PGCSS%20Owners`
- **ADO**: Work items with owner assignments and due dates

## Quick Reference — Product Cluster Mapping

| Cluster (PCY) | Products | Support Planner | Beta EEE |
|---------------|----------|-----------------|----------|
| Azure NET Layer 7 | AppGW, AFD, ATM, WAF | Deniz Ercoskun | Oscar Artavia |
| Azure NET Hybrid | ExR, Firewall, Firewall Mgr, NVA, vWAN, VPN GW, Virtual Enclaves | Marcin Jaworski | Brian Martin |
| Azure NET Monitoring_Connectivity | Bastion, DNS, LB, NW, Private Link, IP Services, VNet NAT, NSP | Deniz Ercoskun | Oscar Artavia |
| Azure NET Virtual Networks | VNet, Network Manager | Deniz Ercoskun | Oscar Artavia |

## Quality Criteria

- Stakeholder lookups return correct role assignments (validated against SharePoint source)
- RACI matrices cover all initiative activities with no empty Accountable cells
- Commitment tracker flags overdue items before escalation windows close
- Follow-up communications sent within 24 hours of action assignment
