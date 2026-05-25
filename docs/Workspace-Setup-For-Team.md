# Workspace Setup For Team

## Personal Productivity Workspace — Prachand Kumar
**Role:** Sr Supportability Manager | **Team:** Azure Networking – Supportability PM

### Quick Links

| File | Purpose |
|---|---|
| [me.md](./me.md) | Personal AI profile — context for all AI-assisted tasks |
| [daily-planner-template.md](./daily-planner-template.md) | Daily planning and EOD wrap-up |
| [repair-tracker.md](./repair-tracker.md) | Live repair status, ownership, and impact |
| [weekly-status-template.md](./weekly-status-template.md) | Weekly status report template |
| [meeting-notes/aaa-weekly-standup-template.md](./meeting-notes/aaa-weekly-standup-template.md) | AAA Weekly Standup (Thu) |
| [meeting-notes/pace-exr-vpn-ta-sync-template.md](./meeting-notes/pace-exr-vpn-ta-sync-template.md) | PACE \|\| ExR + VPN TA Sync (Bi-weekly) |
| [meeting-notes/appgw-pace-sync-template.md](./meeting-notes/appgw-pace-sync-template.md) | AppGW PACE Sync (Bi-weekly) |
| [meeting-notes/project-pace-connect-template.md](./meeting-notes/project-pace-connect-template.md) | Project PACE Connect (Mon & Wed) |
| [meeting-notes/sme-agent-office-hours-template.md](./meeting-notes/sme-agent-office-hours-template.md) | SME Agent Office Hours |
| [meeting-notes/stakeholder-vteam-checkin-template.md](./meeting-notes/stakeholder-vteam-checkin-template.md) | Stakeholder / vTeam Check-Ins |

---

## Purpose

This document standardizes how the team sets up and uses the `skills-main` workspace for reviewing, creating, and maintaining skills in this repository.

## What This Repository Contains

- `skills/`: individual skill implementations, each with its own `SKILL.md` and supporting assets.
- `spec/`: the Agent Skills specification used as the source of truth for format and behavior expectations.
- `template/`: a minimal starter template for creating new skills.
- `README.md`: the primary onboarding and usage guide for the repository.

## Recommended Local Setup

1. Clone the repository into a shared workspace location.
2. Open `skills-main` as the folder root in VS Code.
3. Read `README.md` before making changes.
4. Read `spec/agent-skills-spec.md` if you are adding or reviewing skill behavior.
5. Use `template/SKILL.md` as the starting point for any new skill.

## Expected Team Workflow

### 1. Review the repository-level guidance

Start with these files:

- `README.md`
- `spec/agent-skills-spec.md`
- `template/SKILL.md`

These three files establish the format, structure, and examples used across the repo.

### 2. Work inside the appropriate skill folder

Each skill is self-contained. When updating a skill:

- keep changes local to that skill's folder where possible
- update `SKILL.md` first when behavior or instructions change
- keep supporting assets near the skill that uses them

### 3. Preserve repository conventions

- Prefer small, focused edits.
- Do not introduce top-level tooling unless there is a clear team decision to do so.
- Keep markdown readable and structured.
- Match the style already used in neighboring skills.

## Tooling Notes

There is no top-level package manifest or build pipeline in the current workspace root. Treat this repository as documentation-first unless a specific skill folder includes its own scripts or language-specific setup.

Before running anything inside a skill folder:

1. Inspect that folder for local instructions.
2. Check for language-specific files such as `requirements.txt`, scripts, or reference docs.
3. Avoid assuming one global install or validation command applies to the whole repo.

## Team Onboarding Checklist

- Confirm access to the repository.
- Open the repo in VS Code.
- Read `README.md`.
- Review `spec/agent-skills-spec.md`.
- Inspect at least one existing skill under `skills/` before authoring a new one.
- Use `template/SKILL.md` for the first draft of any new skill.

## Creating a New Skill

1. Copy the structure implied by `template/SKILL.md`.
2. Create a new folder under `skills/` using a clear, lowercase, hyphenated name.
3. Add `SKILL.md` with valid frontmatter and task-specific instructions.
4. Add only the assets or scripts required by that skill.
5. Compare the new skill against nearby examples for consistency.

## Review Expectations

When reviewing changes, check for:

- clear skill name and description
- valid markdown structure
- instructions that are specific and actionable
- consistency with repository layout
- licensing or notice files where required by the skill contents

## Notes For Team Leads

- Use this document as the default onboarding path for new contributors.
- If the team adopts shared validation scripts later, add them here instead of relying on tribal knowledge.
- If contribution rules expand, this document should point to a dedicated contributing guide.