# LEARNING LOG - QUICK REFERENCE

**File:** `memory-bank/tracking/learning-log.md`  
**Purpose:** Record what works so you can duplicate success

---

## ⚡ QUICK ENTRY TEMPLATE

```markdown
### [DATE] - [TASK NAME]
**Worked:** [What worked]
**Why:** [Root cause]
**Pattern:** [How to reuse]
**Code:** [Snippet if applicable]
**Saved:** [Time saved]
```

---

## 📝 WHEN TO LOG

### ✅ Always Log:
- After completing any task
- When you solve a tricky bug
- When you discover an API quirk
- When you find a performance optimization
- When you create a reusable pattern
- When you avoid a mistake

### ⏰ Timing:
- **Best:** Immediately after discovery
- **Good:** End of work session
- **Acceptable:** End of day
- **Too Late:** Next week (you'll forget details)

---

## 🎯 WHAT TO CAPTURE

### 1. Technical Wins
```markdown
**Example:**
### 2026-01-28 - DashMap Performance
**Worked:** Replaced RwLock with DashMap
**Why:** Lock-free concurrent access
**Pattern:** Use DashMap for concurrent state
**Code:** `let state = DashMap::new();`
**Saved:** 100x performance improvement
```

### 2. Process Improvements
```markdown
**Example:**
### 2026-01-28 - Incremental Validation
**Worked:** Validate after each method
**Why:** Catches bugs before they compound
**Pattern:** Run tests after each change
**Code:** `pytest tests/unit/test_method.py -v`
**Saved:** 8h debugging time
```

### 3. API Discoveries
```markdown
**Example:**
### 2026-01-28 - Timestamp Format
**Worked:** Convert ns to ms for Paradex
**Why:** Paradex uses milliseconds
**Pattern:** Always check timestamp format
**Code:** `ts_ms = ts_ns // 1_000_000`
**Saved:** 2h debugging
```

### 4. Debugging Breakthroughs
```markdown
**Example:**
### 2026-01-28 - Duplicate Fills
**Worked:** Deduplicate using trade_id
**Why:** WebSocket sends duplicates
**Pattern:** Track emitted events in set
**Code:** `if trade_id not in self._emitted_fills:`
**Saved:** Prevented production bug
```

---

## 🚫 ANTI-PATTERNS TO LOG

```markdown
**Example:**
### 2026-01-28 - ANTI-PATTERN: Skip Validation
**What Happened:** Implemented 10 methods, validated at end
**Result:** 5 bugs, hard to isolate
**Lesson:** Validate after EACH method
**Fix:** Incremental validation
```

---

## 📊 METRICS TO TRACK

```markdown
### Time Savings
| Improvement | Time Saved |
|-------------|------------|
| Dependency analysis | 5h |
| Mock infrastructure | 10h |
| Incremental validation | 8h |

### Bugs Prevented
| Practice | Bugs | Severity |
|----------|------|----------|
| Reconciliation-first | 3 | HIGH |
| Mock testing | 2 | LOW |
```

---

## 🔄 DAILY WORKFLOW

### Morning:
```bash
# Review yesterday's learnings
tail -20 memory-bank/tracking/learning-log.md
```

### After Each Task:
```bash
# Log immediately
vim memory-bank/tracking/learning-log.md
# Add entry using template
```

### End of Day:
```bash
# Review and summarize
# What were top 3 wins today?
# What patterns emerged?
```

---

## 📚 USING THE LOG

### Before Starting Similar Task:
```bash
# Search for relevant patterns
grep "Pattern:" memory-bank/tracking/learning-log.md | grep "validation"
```

### When Stuck:
```bash
# Check if similar problem was solved
grep "Worked:" memory-bank/tracking/learning-log.md | grep "WebSocket"
```

### For New Projects:
```bash
# Extract all reusable patterns
grep "Reusable Pattern:" memory-bank/tracking/learning-log.md > patterns-library.md
```

---

## 💡 PRO TIPS

1. **Log immediately** - Don't wait, you'll forget details
2. **Be specific** - "Used DashMap" not "Made it faster"
3. **Include code** - Exact snippet that worked
4. **Quantify savings** - "Saved 5h" not "Saved time"
5. **Link references** - Commit hash, file path, line number
6. **Update metrics** - Track cumulative time saved
7. **Review weekly** - Identify patterns and trends

---

## 🎯 SUCCESS CRITERIA

### Good Entry:
```markdown
### 2026-01-28 - Reconciliation Deduplication
**Worked:** Track emitted fills in set
**Why:** WebSocket sends duplicate fill messages
**Pattern:** Use set to deduplicate events by ID
**Code:** 
```python
self._emitted_fills: set[TradeId] = set()
if trade_id not in self._emitted_fills:
    self._send_fill_report(report)
    self._emitted_fills.add(trade_id)
```
**Saved:** Prevented duplicate fill bug (HIGH severity)
**Reference:** execution.py:245, commit abc123
```

### Bad Entry:
```markdown
### 2026-01-28 - Fixed bug
**Worked:** Made it work
**Why:** It was broken
```
❌ Too vague, not reusable

---

## 📁 FILE LOCATION

```bash
# Main log
memory-bank/tracking/learning-log.md

# Quick reference (this file)
memory-bank/tracking/learning-log-quick-ref.md

# Related files
memory-bank/tracking/bug-fixes-record.md
memory-bank/tracking/improvements-log.md
memory-bank/tracking/progress.md
```

---

## 🚀 START LOGGING NOW

```bash
# Open the log
vim memory-bank/tracking/learning-log.md

# Add your first entry
### 2026-01-28 - Started Learning Log
**Worked:** Created learning log system
**Why:** Capture knowledge for future projects
**Pattern:** Log after each task completion
**Saved:** Will save hours in future projects
```

---

**Remember:** Every minute spent logging saves 10 minutes in the future!
