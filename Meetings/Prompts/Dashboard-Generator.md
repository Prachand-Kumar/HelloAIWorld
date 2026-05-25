# Prompt: Dashboard Generator

**Trigger phrase:** "update my dashboard"

---

## Instructions for AI

When Prachand says "update my dashboard", do the following:

1. **Read all tracker files**
   - `Meetings/Action-Tracker/Active-Actions.md`
   - `Meetings/Follow-Ups/Pending-Follow-Ups.md`
   - `Meetings/Decisions-Log/Decisions.md`
   - List of files in `Meetings/Meeting-Reports/`

2. **Count and categorize**
   - Action Items: count total, open (⬜), in progress (🔄), overdue (🔴), done (✅), blocked (⏸)
   - Follow-Ups: count total, pending (⬜), sent/waiting (📨), overdue (🔴), resolved (✅)
   - Decisions: count total entries
   - Meeting Reports: list the most recent 5

3. **Identify overdue or at-risk items**
   - Any action or follow-up where Due < today and Status ≠ ✅

4. **Overwrite `Meetings/Dashboard.md`** with the refreshed content

5. **Confirm to Prachand**
   - "Dashboard updated. Here's your snapshot:" then show the Status at a Glance table

---

## Dashboard.md Output Format

```markdown
# Meetings Dashboard

**Last Updated:** [Today's date]

## Status at a Glance

| Tracker | Total | Open | Overdue | Done |
|---|---|---|---|---|
| Action Items | N | N | N | N |
| Follow-Ups | N | N | N | N |
| Decisions | N | — | — | — |

## Overdue / At Risk
| Item | Type | Owner | Due | Status |
|---|---|---|---|---|

## Open Action Items (Summary)
| Action | Owner | Due |
|---|---|---|

## Pending Follow-Ups (Summary)
| Item | With | Due |
|---|---|---|

## Recent Decisions
| Decision | Date | Made By |
|---|---|---|

## This Week's Meeting Reports
| Report | Meeting | Date |
|---|---|---|
```
