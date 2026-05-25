# Prompt: Start My Day

**Trigger phrase:** "start my day"

---

## Instructions for AI

When Prachand says "start my day", do the following in order:

1. **Read context files**
   - Read `AGENTS.md`
   - Read `Prachand-Kumar-Profile.md`
   - Read `Meetings/Action-Tracker/Active-Actions.md`
   - Read `Meetings/Follow-Ups/Pending-Follow-Ups.md`

2. **Check today's calendar**
   - Ask: "What meetings do you have today?" (or read calendar context if provided)
   - Map meetings to known templates in `Meetings/Prompts/`

3. **Review overdue action items**
   - List all items from `Active-Actions.md` where Due < today and Status ≠ ✅
   - Flag them clearly as overdue

4. **List pending follow-ups**
   - List all open items from `Pending-Follow-Ups.md`
   - Highlight any that are overdue or marked 🔴

5. **Suggest top 3 priorities for today**
   - Based on overdue items, today's meetings, and open follow-ups
   - Frame as: "Here are your top 3 priorities for today:"

---

## Output Format

```
## Good Morning, Prachand 👋

### Today's Meetings
- [Time] [Meeting Name] — [1-line purpose]

### Overdue Action Items
- [Action] | Owner: [Owner] | Was due: [Date]

### Pending Follow-Ups
- [Item] | With: [Person] | Due: [Date]

### Your Top 3 Priorities Today
1. [Priority]
2. [Priority]
3. [Priority]
```
