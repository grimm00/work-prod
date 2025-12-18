# Command Usage Tracker

**Purpose:** Track command usage in work-prod for graduation feedback  
**Related:** Dev-infra ADR-004 (Graduation Process)  
**Status:** ✅ Active  
**Last Updated:** 2025-12-16

---

## 📋 Overview

This document tracks command usage in work-prod to:

1. **Validate commands** - Prove they work in real projects
2. **Provide feedback** - Help dev-infra graduation decisions
3. **Track issues** - Log problems for improvements

**Note:** Work-prod is a consumer of dev-infra commands. Usage here provides external validation for graduation.

---

## 📊 Usage Summary

### Core Commands (Tier 1)

| Command | Uses | Last Use | Success Rate | Notes |
|---------|------|----------|--------------|-------|
| `/pr` | 30+ | 2025-12-07 | ~95% | Heavy use |
| `/task-phase` | 20+ | 2025-12-07 | ~95% | Heavy use |
| `/fix-plan` | 10+ | 2025-12-07 | 100% | Heavy use |
| `/fix-implement` | 10+ | 2025-12-07 | 100% | Heavy use |
| `/reflect` | 10+ | 2025-12-07 | 100% | Heavy use |

### Valuable Commands (Tier 2)

| Command | Uses | Last Use | Success Rate | Notes |
|---------|------|----------|--------------|-------|
| `/explore` | 1 | 2025-12-02 | 100% | Initial exploration |
| `/research` | 3+ | 2025-12-03 | 100% | Tech stack research |
| `/decision` | 6 | 2025-12-03 | 100% | All ADRs |
| `/pre-phase-review` | 3+ | 2025-12-06 | 100% | Phase 7 review |
| `/pr-validation` | 20+ | 2025-12-07 | ~90% | Heavy use |
| `/post-pr` | 15+ | 2025-12-07 | 100% | Heavy use |

### Advanced Commands (Tier 3)

| Command | Uses | Last Use | Success Rate | Notes |
|---------|------|----------|--------------|-------|
| `/transition-plan` | 2 | 2025-12-07 | 100% | Release planning |
| `/reflection-artifacts` | 1 | 2025-12-07 | 100% | Minimal use |
| `/int-opp` | 2 | 2025-12-07 | 100% | Learnings capture |
| `/address-review` | 2 | 2025-12-06 | 100% | Phase 7 |
| `/task-release` | 1 | 2025-12-07 | 100% | v0.1.0 release |
| `/cursor-rules` | 0 | - | - | Not yet used |
| `/fix-review` | 3+ | 2025-12-07 | 100% | Fix management |

### Recently Added Commands (from dev-infra sync)

| Command | Uses | Last Use | Success Rate | Notes |
|---------|------|----------|--------------|-------|
| `/explore` | 0 (new) | - | - | Just synced |
| `/research` | 0 (new) | - | - | Just synced |
| `/decision` | 0 (new) | - | - | Just synced |
| `/task-improvement` | 0 (new) | - | - | Just synced |

---

## 📝 Detailed Usage Log

### Recent Usage (Last 7 Days)

| Date | Command | Context | Result | Evidence |
|------|---------|---------|--------|----------|
| 2025-12-16 | (sync) | Commands synced from dev-infra | ✅ Success | commit f0a09ee |

---

## 🔴 Commands Needing Testing

Commands just synced from dev-infra that haven't been used yet:

| Command | Status | Priority |
|---------|--------|----------|
| `/explore` | 🔴 Not tested | Use when new exploration needed |
| `/research` | 🔴 Not tested | Use when research needed |
| `/decision` | 🔴 Not tested | Use when new ADR needed |
| `/task-improvement` | 🔴 Not tested | Use for infrastructure work |
| `/cursor-rules` | 🔴 Not tested | Use when rules need update |

**Note:** Testing these in work-prod provides external validation for dev-infra graduation.

---

## 📋 How to Update This Tracker

**After successful command use:**

1. **Update Usage Summary table:**
   - Increment "Uses" count
   - Update "Last Use" date
   - Update "Success Rate" if failure occurred

2. **Add to Detailed Usage Log:**
   ```markdown
   | YYYY-MM-DD | `/command` | Context description | ✅ Success | Evidence link |
   ```

3. **Report issues to dev-infra:**
   - If command fails or has UX issues
   - Create entry in `docs/maintainers/planning/notes/opportunities/internal/dev-infra/`

**Commit message:**
```
docs(commands): update usage tracker - /[command-name]
```

---

## 🔗 Related

- [Dev-Infra Command Strategy](https://github.com/user/dev-infra/admin/decisions/dev-infra-identity-and-focus/adr-003-command-strategy.md)
- [Dev-Infra Graduation Process](https://github.com/user/dev-infra/admin/decisions/dev-infra-identity-and-focus/adr-004-graduation-process.md)

---

**Last Updated:** 2025-12-16


