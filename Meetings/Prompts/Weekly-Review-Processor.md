# Prompt: Weekly Review Processor

**Trigger phrase:** "run my weekly review"

---

## Instructions for AI

When Prachand says "run my weekly review", do the following:

1. **Read all workspace files**
   - `AGENTS.md` and `Prachand-Kumar-Profile.md`
   - `Meetings/Action-Tracker/Active-Actions.md`
   - `Meetings/Follow-Ups/Pending-Follow-Ups.md`
   - `Meetings/Decisions-Log/Decisions.md`
   - All files in `Meetings/Meeting-Reports/` from this week

2. **Summarize this week**
   - What got done: list completed actions (✅) and resolved follow-ups (✅)
   - What carried over: list open/overdue items still pending
   - Key decisions made this week

3. **Set next week's priorities**
   - Based on: carried-over actions, open follow-ups, and known upcoming meetings
   - Suggest top 5 priorities for next week

4. **Archive completed items**
   - Move all ✅ items from `Active-Actions.md` to `Action-Tracker/Completed-Actions.md`
   - Move all ✅ items from `Pending-Follow-Ups.md` to `Follow-Ups/Resolved-Follow-Ups.md`
   - Confirm what was archived

5. **Update Dashboard.md**
   - Run the same logic as Dashboard-Generator after archiving

---

## Output Format

```
## Weekly Review — Week of [DATE]

### ✅ What Got Done This Week
- [Item] — [Date completed]

### 🔄 Carried Over to Next Week
| Item | Type | Owner | Original Due |
|---|---|---|---|

### 📋 Key Decisions This Week
- [Decision] — [Meeting, Date]

### 🎯 Top 5 Priorities for Next Week
1. [Priority]
2. [Priority]
3. [Priority]
4. [Priority]
5. [Priority]

### 📁 Archived
- [N] action items moved to Completed-Actions.md
- [N] follow-ups moved to Resolved-Follow-Ups.md
```
