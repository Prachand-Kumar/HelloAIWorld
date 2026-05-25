# AGENTS.md — AI Brain File

> This file teaches the AI assistant about this workspace. Read this file before responding to any request in this workspace. Always personalize responses to the person and context described here.

---

## Who I Am

My name is **Prachand Kumar**. I am a **Sr Supportability Manager (Supportability PM)** on the **Azure Networking – Supportability PM** team within Azure CSS.

Full profile: [Prachand-Kumar-Profile.md](./Prachand-Kumar-Profile.md)

**Always read my profile file before personalizing any response.**

---

## What This Workspace Is For

This workspace is my personal AI productivity hub. It is used to:

- Plan and track daily work across multiple stakeholders and meeting streams
- Capture and process meeting notes into structured actions, decisions, and follow-ups
- Maintain a single view of repair status, ownership, and customer impact
- Generate status reports, stakeholder summaries, and weekly reviews
- Reduce manual administrative overhead so I can focus on strategic work

---

## How I Work

### Meeting Rhythm

I attend six recurring meetings across my week:

| Meeting | Cadence |
|---|---|
| AAA Weekly Standup | Thu |
| SME Agent Office Hours | Recurring |
| PACE \|\| ExR + VPN TA Sync | Bi-weekly |
| AppGW PACE Sync | Bi-weekly |
| Project PACE Connect | Mon & Wed |
| Stakeholder / vTeam Check-ins | Ongoing |

Each meeting generates action items, follow-ups, and decisions. These feed into the `Meetings/` folder structure.

### Tracking Patterns

- Action items go into `Meetings/Action-Tracker/Active-Actions.md`
- Follow-ups go into `Meetings/Follow-Ups/Pending-Follow-Ups.md`
- Decisions go into `Meetings/Decisions-Log/Decisions.md`
- Meeting reports go into `Meetings/Meeting-Reports/`
- Dashboard status lives in `Meetings/Dashboard.md`

### Working Style

- Prachand prefers **concise, action-oriented outputs**
- Use **PACE / repair tracking language** for Azure Networking context
- Format work items to be **ADO-compatible** where relevant
- Use **ICM / KQL framing** when analyzing customer impact
- Default to tables for status, lists for actions

---

## Tools and Data Sources Available

| Tool | Context |
|---|---|
| Azure DevOps (ADO) | Backlog, repair items, sprint tracking |
| ICM + Kusto (KQL) | Customer issue trends, impact analysis |
| Outlook + Teams | Calendar, email, stakeholder comms |
| OneNote + Excel | Notes and ad hoc reporting |
| Power BI / CXObserve | Metrics dashboards |
| GitHub | Repos, issues, projects |

---

## Prompt Templates Available

The following AI prompt templates live in `Meetings/Prompts/`:

| Prompt | Trigger | What It Does |
|---|---|---|
| [Start-My-Day.md](./Meetings/Prompts/Start-My-Day.md) | "start my day" | Reviews calendar, overdue items, top 3 priorities |
| [Post-Meeting-Processor.md](./Meetings/Prompts/Post-Meeting-Processor.md) | Paste meeting notes | Extracts actions, decisions, follow-ups, generates report |
| [Dashboard-Generator.md](./Meetings/Prompts/Dashboard-Generator.md) | "update my dashboard" | Scans trackers, updates Dashboard.md |
| [Weekly-Review-Processor.md](./Meetings/Prompts/Weekly-Review-Processor.md) | "run my weekly review" | Summarizes week, sets next week priorities, archives done items |
| [Nebula-Review.md](./Meetings/Prompts/Nebula-Review.md) | "run nebula review" | Produces Nebula FQR risk/actions/KPI snapshot and stakeholder update draft |

---

## Rules for the AI

1. **Always read `Prachand-Kumar-Profile.md` before personalizing any response.**
2. Default responses to Prachand's role, team, and tools — do not respond generically.
3. When processing meeting notes, always extract actions, decisions, and follow-ups into the correct tracker files.
4. Keep outputs concise and action-oriented. Avoid unnecessary prose.
5. When asked for a status summary, read `Meetings/Dashboard.md` and the three tracker files first.
6. Use repair / PACE language for Azure Networking topics.
7. When uncertain about context, ask one clarifying question — do not assume.

### Nebula Program Rules (Updated Understanding)

**Critical distinction to apply in every Nebula response:**
- **Nebula** = CSS early in profession workforce program (people, roles, talent pipeline)
- **SME Agent / FQR** = AI tool that empowers the Nebula workforce and broader CSS engineers
- Prachand owns the SME Agent FQR program, which is the AI layer enabling the Nebula workforce

1. Never conflate Nebula (workforce program) with the SME Agent (AI tool). Use correct terminology in all outputs.
2. For Nebula program topics (hiring, training, workforce, case complexity), frame around people, roles, capacity, and talent pipeline.
3. For SME Agent / FQR topics (AI quality, FQR authoring, autonomous resolution), frame around technical delivery, PACE execution, and production metrics.
4. Read `Prachand-Kumar-Profile.md` "Nebula Program Understanding" section before any Nebula or SME Agent response.
5. Structure every SME Agent / FQR review with: Executive Snapshot, Top Risks, Recommended Actions, KPI Signal, Escalations.
6. Prioritize actions by customer impact, risk, and dependency; always include `Action | Owner | Due | Impact`.
7. Use PACE loop framing for improvements: Plan, Analyze, Construct, Execute.
8. When creating stakeholder updates, include both operational outcomes (SLA/quality) and business outcomes (cost/productivity/CSAT).
9. If required telemetry is missing, ask one focused question and provide a provisional recommendation with assumptions.

---

## Workspace Upgrade: Microsoft 365 Access (Outlook + Teams)

### Goal

Enable this workspace to use real Outlook email, Teams messages, and calendar context via an approved Microsoft 365 integration path.

### Preferred Path

Use a Microsoft 365 / Microsoft Graph MCP server in VS Code so the assistant can access approved M365 data sources through enterprise authentication.

### Setup Checklist

1. Confirm licensing and policy with tenant admin:
	- Microsoft 365 Copilot and/or Graph MCP usage approval
	- App consent policy for Graph-backed tools
2. Install and configure the approved Microsoft 365 MCP server in VS Code.
3. Sign in with corporate account and complete tenant consent prompts.
4. Validate access with sample queries:
	- "Summarize my unread emails from the last 7 days"
	- "List my meetings today"
	- "Summarize my recent chat with JR Mayberry"
5. If access fails, capture error text and verify app permissions with admin.

### Operating Rule After Enablement

When M365 access is available, the assistant should prefer live Outlook/Teams/calendar data over manual pasted context for daily planning and summaries.

### Security and Compliance Notes

- Use least-privilege permissions.
- Follow tenant data-handling and retention policies.
- Do not persist sensitive email/chat content outside approved locations.
