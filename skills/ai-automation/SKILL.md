---
name: ai-automation
description: >
  AI, Automation & Scale Thinking skill for the SPM AI Agent.
  Use this skill when the user needs to identify automation opportunities,
  build agent workflows, implement AI governance, or scale supportability
  outcomes beyond linear staffing.
  Triggers: "automate", "AI agent", "copilot", "self-healing", "scale",
  "automation candidate", "prompt library", "AI governance", "agent workflow".
---

# AI, Automation & Scale Thinking

> *The SPM leverages AI and automation to reduce support demand, lower cost, and scale outcomes.*

## Overview

This skill covers identifying, building, and governing AI-augmented workflows for supportability — from automated agenda generation and action tracking (already implemented in `spm-prototype`) to future copilot enablement, self-healing systems, and prompt libraries for support engineers.

## Capabilities

1. Leverage AI and automation to reduce support demand and cost at scale.
2. Build self-healing and self-help ecosystems that resolve issues without human intervention.
3. Apply product + data thinking to scale supportability outcomes beyond linear staffing.
4. Drive innovation in diagnostics, copilots, and support tooling.
5. Evaluate supportability workflows for AI-augmentation opportunities (classification, summarization, routing).
6. Develop and maintain agent-based automation for agenda building, action tracking, and recap generation.
7. Implement AI governance guardrails: source traceability, hallucination prevention, human-in-the-loop checkpoints.
8. Operationalize Copilot-for-Service-style enablement for support engineers (prompt libraries, scenario playbooks).
9. Track AI-initiative adoption metrics and report on realized vs. projected value.
10. Maintain a backlog of automation candidates prioritized by effort/impact ratio.
11. Ensure all AI-generated outputs are flagged as such and validated before external distribution.

## Workflow

### Step 1 — Identify Automation Candidates
Evaluate SPM workflows against the automation matrix:

| Workflow | Current State | Automation Opportunity | Effort | Impact |
|----------|--------------|----------------------|--------|--------|
| Signal collection | Automated (`collect_signals.py`) | ✅ Done | — | High |
| SAP mover computation | Automated (`compute_movers.py`) | ✅ Done | — | High |
| Agenda drafting | Automated (`draft_agenda.py`) | ✅ Done | — | Medium |
| ADO reconciliation | Automated (`reconcile_ado.py`) | ✅ Done | — | High |
| HTML report generation | Automated (`generate_report.py`) | ✅ Done | — | High |
| Meeting transcript parsing | Manual | AI summarization | Medium | High |
| Follow-up email drafting | Manual | Template + AI | Low | Medium |
| Escalation brief creation | Manual | Template + AI | Low | Medium |
| Case classification | Manual | AI classification | High | High |
| GTS gap detection | Manual | Kusto + rules engine | Medium | High |

### Step 2 — Build the Automation
For each candidate, follow the pattern established in `spm-prototype`:

1. **Define inputs/outputs** — What data goes in, what artifact comes out
2. **Write the module** — Python script in `src/` with clear function boundaries
3. **Integrate into pipeline** — Add as a step in `run_cycle.py`
4. **Add config** — Product-specific settings in `config/settings.yaml`
5. **Test end-to-end** — Run full cycle and validate output

### Step 3 — Implement Governance Guardrails
Every AI-generated output must:
- [ ] Cite data sources (Kusto query, ADO item, case ID)
- [ ] Flag confidence level (High / Medium / Low)
- [ ] Include human-in-the-loop checkpoint before external distribution
- [ ] Be marked as AI-generated in metadata or footer
- [ ] Not contain PII or customer-identifying information

### Step 4 — Build Prompt Libraries
For support engineer enablement, maintain scenario-specific prompts:

| Scenario | Prompt Pattern | Output |
|----------|---------------|--------|
| Case triage | "Classify this case by product, severity, and likely root cause: {{case_description}}" | Product + severity + RCA hypothesis |
| RCA analysis | "Given these symptoms: {{symptoms}}, what are the top 3 most likely root causes for {{product}}?" | Ranked RCA list |
| Customer response | "Draft a customer response for: {{issue_summary}}. Resolution: {{resolution_steps}}" | Email draft |
| Knowledge article | "Create a troubleshooting guide for: {{issue_pattern}}. Include: symptoms, cause, resolution, prevention." | GTS draft |

### Step 5 — Track Adoption & Value
Measure AI initiative outcomes:

| Metric | Definition | Target |
|--------|-----------|--------|
| Automation coverage | % of SPM workflows automated | Track over time |
| Time saved per cycle | Hours saved vs. manual process | Measure and report |
| Accuracy | % of AI outputs requiring no human correction | > 90% |
| Adoption rate | % of team using AI tools regularly | Track over time |
| Value realized | Cost/time savings from automation | Report quarterly |

## Current Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| SPM Cycle Pipeline | ✅ Live | `spm-prototype/src/run_cycle.py` |
| Kusto Signal Collection | ✅ Live | `spm-prototype/src/collect_signals.py` |
| SAP Mover Computation | ✅ Live | `spm-prototype/src/compute_movers.py` |
| IPD Forecasting | ✅ Live | `spm-prototype/src/compute_forecast.py` |
| Carry-Forward Tracking | ✅ Live | `spm-prototype/src/carry_forward.py` |
| Agenda Drafting | ✅ Live | `spm-prototype/src/draft_agenda.py` |
| ADO Reconciliation | ✅ Live | `spm-prototype/src/reconcile_ado.py` |
| HTML Report Generation | ✅ Live | `spm-prototype/src/generate_report.py` |
| Auto-Auth (Azure CLI + PAT) | ✅ Live | `spm-prototype/src/run_cycle.py` |
| GitHub Repo | ✅ Live | `CloudNet-Supportability/SPM-Agent` |
| Meeting Transcript Parsing | 🔲 Planned | — |
| Copilot Prompt Library | 🔲 Planned | — |
| Self-Healing Diagnostics | 🔲 Planned | — |

## Integration Points

- **SPM Prototype**: `spm-prototype/` — the living implementation of this skill
- **GitHub**: `https://github.com/CloudNet-Supportability/SPM-Agent`
- **Agent Skills Framework**: `Work/skills-main/skills/` — skill definitions
- **MCP Builder**: `Work/skills-main/skills/mcp-builder/` — for building new integrations

## Quality Criteria

- All AI outputs cite data sources
- Human-in-the-loop checkpoint before external distribution
- AI-generated content flagged in metadata
- Automation backlog maintained with effort/impact prioritization
- Adoption metrics tracked and reported quarterly
- No PII in AI-generated outputs
