# Prompt: Post-Meeting Processor

**Trigger:** Prachand pastes raw meeting notes into the chat

---

## Instructions for AI

When Prachand pastes meeting notes, do the following in order:

1. **Read context files**
   - Read `AGENTS.md` and `Prachand-Kumar-Profile.md`
   - Read current `Meetings/Action-Tracker/Active-Actions.md`
   - Read current `Meetings/Follow-Ups/Pending-Follow-Ups.md`
   - Read current `Meetings/Decisions-Log/Decisions.md`

2. **Extract from the notes**

   **Attendees** — list everyone mentioned or present

   **Decisions** — any conclusion, agreement, or approved direction  
   → Add each to `Decisions-Log/Decisions.md` with date and meeting name

   **Action Items** — any task assigned to a person with or without a due date  
   → Add each to `Action-Tracker/Active-Actions.md` with owner, due date (if stated), and source meeting  
   → If no due date is mentioned, flag as "TBD"

   **Follow-Ups** — anything waiting on someone else or needing a response  
   → Add each to `Follow-Ups/Pending-Follow-Ups.md` with the person it's with and expected date

3. **Generate a structured meeting report**
   - Save as `Meetings/Meeting-Reports/YYYY-MM-DD-[Meeting-Name].md`
   - Use the output format below

4. **Confirm what was added**
   - Tell Prachand how many actions, decisions, and follow-ups were extracted

---

## Meeting Report Output Format

```markdown
# [Meeting Name] — [Date]

**Attendees:** [list]

## Summary
[2-3 sentence summary of what was discussed and decided]

## Decisions
- [Decision 1]
- [Decision 2]

## Action Items
| Action | Owner | Due |
|---|---|---|
| | | |

## Follow-Ups
| Item | With | Due |
|---|---|---|
| | | |

## Notes
[Any additional context worth preserving]
```
