# Prompt: Nebula Review

Trigger phrase: "run nebula review"

## Purpose

Run a charter-aligned PM review covering both the **Nebula workforce program** and the **SME Agent FQR program** — the AI layer that empowers Nebula engineers — using the latest workspace context. Produce action-oriented output for execution and stakeholder communication.

**Key distinction:** Nebula = early in profession workforce program (people). SME Agent / FQR = AI tool that empowers them. Review both lenses.

## Inputs to Read First

1. `AGENTS.md`
2. `Prachand-Kumar-Profile.md` (especially "Nebula Program Understanding")
3. `Meetings/Action-Tracker/Active-Actions.md`
4. `Meetings/Follow-Ups/Pending-Follow-Ups.md`
5. `Meetings/Decisions-Log/Decisions.md`
6. Relevant files in `Meetings/Meeting-Reports/` from this week

## Processing Steps

1. Identify current signals — split by lens:

   **Nebula Workforce lens:**
   - Workforce readiness, onboarding progress, capacity vs. case volume
   - Early in profession engineer feedback on tooling (SME Agent quality)
   - Case complexity model adherence and transfer patterns

   **SME Agent / FQR lens:**
   - Quality signals (FQR accuracy issues, defects, regressions)
   - Operational signals (SLA risk, escalation load, blocked actions)
   - Business signals (support cost/productivity/CSAT implications)

2. Apply PACE loop:
- Plan: what objective is at risk
- Analyze: what telemetry/feedback indicates
- Construct: what change or mitigation is needed
- Execute: what should happen this week

3. Prioritize next actions:
- Rank by customer impact, risk severity, and dependency chain
- Include explicit owner and due date
- Flag items requiring PG or leadership escalation

4. Produce stakeholder-ready narrative:
- What changed since last review
- What is on-track vs at-risk
- What decision/support is required

## Output Format

## Nebula PM Review — [DATE]

### Executive Snapshot
- Overall status: [On Track | At Risk | Off Track]
- One-line summary:

### Top Risks
| Risk | Signal | Impact | Owner |
|---|---|---|---|
|  |  |  |  |

### Recommended Actions
| Action | Owner | Due | Impact |
|---|---|---|---|
|  |  |  |  |

### KPI Signal
| KPI | Current | Target | Trend | Notes |
|---|---|---|---|---|
| FQR Accuracy |  | 90%+ |  |  |
| Autonomous Resolution Rate |  | 60-70% |  |  |
| First Response Time Reduction |  | 85% |  |  |
| Availability |  | 99.5% |  |  |
| CSAT |  | 95%+ |  |  |
| NPS Improvement |  | +10 |  |  |
| Support Cost Reduction |  | 30% |  |  |
| Productivity Gain |  | 40% |  |  |

### Escalations
| Escalation Needed | To (PG/Leadership/Ops) | Why | Needed By |
|---|---|---|---|
|  |  |  |  |

### Stakeholder Update Draft
Provide a concise 6-8 line update suitable for PG + Support leadership.

## Rules

- If key telemetry is missing, ask one focused question and proceed with explicit assumptions.
- Keep the output concise, decision-oriented, and owner-driven.
- Use Azure Networking and PACE terminology consistently.
