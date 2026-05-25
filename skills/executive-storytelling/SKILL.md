---
name: executive-storytelling
description: >
  Communication & Executive Storytelling skill for the SPM AI Agent.
  Use this skill when the user needs exec-ready summaries, QBR content, business
  narratives, escalation briefs, branding, or stakeholder communications.
  Triggers: "exec summary", "QBR", "business review", "escalation brief",
  "walking deck", "status report", "email draft", "recap", "newsletter".
---

# Communication & Executive Storytelling

> *The SPM creates exec-ready narratives that translate technical issues into business impact with clear calls to action.*

## Overview

This skill transforms raw data and meeting outcomes into polished, audience-appropriate communications — from two-line executive summaries to full QBR slide content. Every output answers the "so-what" and includes explicit calls to action.

## Capabilities

1. Create exec-ready summaries, QBRs, and business updates tailored to audience level.
2. Translate technical issues into customer and financial impact narratives (the "so-what").
3. Drive clear calls-to-action (CTAs) with explicit ownership and timelines.
4. Communicate risks, mitigation plans, and progress effectively at every stakeholder tier.
5. Develop branding for projects, workstreams, and initiatives: names, logos, repeating themes.
6. Create a walking deck that captures the value proposition, differentiation, and strategic direction.
7. Communicate with customers: inform them of new features, build community, and create pull.
8. Generate excitement around supportability initiatives to drive engagement and adoption.
9. Prepare QBR/business-review slide content with linked evidence for every claim.
10. Author escalation briefs: problem statement, impact, ask, and timeline — all on one page.
11. Maintain a library of reusable executive communication templates.

## Workflow

### Step 1 — Determine the Communication Type
| Type | Audience | Length | Tone |
|------|----------|--------|------|
| Executive Summary | Directors / GMs | 2 lines + 6 bullets | Crisp, impact-focused |
| Meeting Recap | Working team | 1 page | Action-oriented |
| QBR Slide Content | VP / CVP | Slide-ready bullets | Strategic, data-backed |
| Escalation Brief | Leadership | 1 page max | Urgent, clear ask |
| Follow-up Email | Action owners | 3–5 sentences | Direct, specific |
| Status Report | Team + leadership | HTML report | Comprehensive, visual |
| Newsletter / Update | Broad audience | 1–2 pages | Engaging, accessible |

### Step 2 — Gather Source Material
Pull from the latest cycle output:
- `spm-prototype/output/Cycle-*/signal_pack.json` — raw metrics
- `spm-prototype/output/Cycle-*/agenda.md` — meeting agenda
- `spm-prototype/output/Cycle-*/spm_report.html` — generated HTML report
- ADO work items — action status
- Meeting transcripts — decisions and actions

### Step 3 — Draft the Communication
Apply the appropriate template and rules:

**Executive Summary Rules:**
- Line 1: Bottom-line statement (what happened)
- Line 2: So-what (why it matters)
- Bullets 1–3: Key data points with directional indicators (↑↓→)
- Bullets 4–5: Actions in flight with owners
- Bullet 6: Next milestone or ask

**Escalation Brief Rules:**
- Problem: One sentence
- Impact: Customer count, revenue exposure, or severity
- Ask: What you need from the reader
- Timeline: When you need it by

### Step 4 — Review & Distribute
Validate against quality criteria, then distribute via appropriate channel.

## Integration Points

- **Report Generator**: `spm-prototype/src/generate_report.py` — HTML report with charts
- **Email Templates**: `AGENTS_PRACHANK/` — existing HTML email templates
- **Status Reports**: `AGENTS_PRACHANK/status_report_EMAIL_*.html`
- **Meeting Templates**: `Work/skills-main/docs/meeting-notes/` — structured templates

## Templates

### Executive Summary (Template E)

```
BOTTOM LINE: {{one-sentence summary of the cycle outcome}}
SO-WHAT: {{why this matters to leadership}}

• {{metric_1}}: {{value}} ({{direction}} from {{previous}}) — {{source_link}}
• {{metric_2}}: {{value}} ({{direction}}) — {{source_link}}
• {{key_risk_or_highlight}}
• ACTION: {{action_1}} — {{owner}} by {{date}}
• ACTION: {{action_2}} — {{owner}} by {{date}}
• NEXT: {{next_milestone_or_meeting_date}}
```

### Follow-up Email (Template F)

```
Subject: [ACTION] {{topic}} — {{owner}} by {{due_date}}

Hi {{owner}},

During {{meeting_name}} on {{date}}, the following action was assigned to you:

ACTION: {{action_description}}
DUE: {{due_date}}
CONTEXT: {{brief context or decision that led to this action}}
ADO: {{work_item_url}}

Please update the work item with progress by {{date}}. Flag any blockers to {{facilitator}}.

Thanks,
{{sender}}
```

## Quality Criteria

- Every claim linked to evidence (Kusto query, ADO item, or dashboard)
- CTAs have explicit owner + due date
- Executive summaries ≤ 2 lines + 6 bullets
- Escalation briefs fit on one page
- Recap distributed within 24 hours of meeting
- No jargon without definition for cross-org audiences
