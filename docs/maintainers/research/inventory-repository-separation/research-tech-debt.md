# Research: Technical Debt Prioritization

**Research Topic:** Inventory Repository Separation  
**Question:** Which technical debt items should be addressed during separation vs. after?  
**Status:** ✅ Complete  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 🎯 Research Question

Which of the 7 known technical debt items should be fixed during the separation, and which can be deferred?

---

## 🔍 Research Goals

- [x] Goal 1: Categorize debt as blocking vs. non-blocking
- [x] Goal 2: Estimate effort for each item
- [x] Goal 3: Create phased plan
- [x] Goal 4: Define minimum viable state

---

## 📚 Research Methodology

**Sources:**
- [x] POC Analysis document
- [x] Current script analysis
- [x] Exploration document
- [x] CLI tool decision (affects prioritization)

---

## 📊 Findings

### Finding 1: Technical Debt Inventory

From the exploration document and POC analysis:

| # | Issue | Current State |
|---|-------|---------------|
| 1 | Hardcoded paths | `/Users/cdwilson/...` hardcoded |
| 2 | No error handling | Scripts crash on errors |
| 3 | Missing dependencies | No requirements.txt |
| 4 | Inconsistent output | Different JSON structures |
| 5 | No master orchestrator | 6 separate scripts |
| 6 | Shell script limitations | bash scripts hard to extend |
| 7 | No incremental mode | Full scan every time |

**Source:** Exploration document

**Relevance:** Complete list for prioritization.

---

### Finding 2: Blocking vs. Non-Blocking Analysis

**Blocking (Must fix for separation):**

| Issue | Why Blocking | Effort |
|-------|--------------|--------|
| #1 Hardcoded paths | Won't work anywhere else | LOW |
| #3 Missing dependencies | Can't install | LOW |

**Important (Should fix for usability):**

| Issue | Why Important | Effort |
|-------|---------------|--------|
| #2 No error handling | Poor reliability | MEDIUM |
| #4 Inconsistent output | Integration issues | MEDIUM |
| #5 No master orchestrator | CLI tool solves this | HIGH → LOW (via CLI) |

**Nice to Have (Can defer):**

| Issue | Why Deferrable | Effort |
|-------|----------------|--------|
| #6 Shell script limits | Works for now | HIGH |
| #7 No incremental mode | Optimization | HIGH |

**Source:** Analysis based on CLI tool decision

**Relevance:** Prioritization for phased approach.

---

### Finding 3: CLI Tool Addresses Some Debt

**Description:** Building a CLI tool automatically addresses:
- **#5 No master orchestrator** → CLI is the orchestrator
- **#4 Inconsistent output** → CLI can standardize output
- **#2 Error handling** → Typer/Click handle errors gracefully

**Source:** CLI tool architecture decision

**Relevance:** CLI approach reduces debt, not adds to it.

---

### Finding 4: Effort Estimates

| Item | Effort | Time | Notes |
|------|--------|------|-------|
| #1 Hardcoded paths | LOW | 1-2 hours | Config file |
| #2 Error handling | MEDIUM | 2-3 hours | Try/except, logging |
| #3 Dependencies file | LOW | 30 min | requirements.txt |
| #4 Output consistency | MEDIUM | 2-3 hours | Define schema |
| #5 Master orchestrator | LOW (via CLI) | 0 hours | CLI provides this |
| #6 Shell rewrites | HIGH | 4-6 hours | Python conversion |
| #7 Incremental mode | HIGH | 4-6 hours | State management |

**Source:** Estimation based on script complexity

**Relevance:** Informs phased approach.

---

## 🔍 Analysis

### Minimum Viable State for Separation

**Must Have (P0):**
1. ✅ Remove hardcoded paths (config file)
2. ✅ Create requirements.txt

**Should Have (P1):**
3. ✅ Basic error handling
4. ✅ CLI wrapper (solves orchestrator + output)

**Nice to Have (P2) - Post-separation:**
5. ⏳ Shell script to Python conversion
6. ⏳ Incremental mode

---

### Phased Implementation Plan

**Phase 1: Separation Foundation (Day 1)**
- Remove hardcoded paths → config file
- Create requirements.txt
- Create package structure

**Phase 2: CLI Wrapper (Day 1-2)**
- Add Typer CLI entry point
- Wrap existing scripts as commands
- Add basic error handling

**Phase 3: Refinement (Week after separation)**
- Standardize output formats
- Add progress bars
- Improve error messages

**Phase 4: Future Enhancements (Later)**
- Convert shell scripts to Python
- Add incremental scanning
- Add caching

---

## 💡 Recommendations

### Primary Recommendation: Fix P0 + P1 During Separation

**Scope for initial separation:**

| Item | Status | Effort |
|------|--------|--------|
| #1 Config file | ✅ Include | 1-2 hours |
| #3 requirements.txt | ✅ Include | 30 min |
| #2 Basic error handling | ✅ Include | 2-3 hours |
| #5 CLI wrapper | ✅ Include | 4-6 hours |
| **Total** | | **8-12 hours** |

### Defer to Post-Separation

| Item | Reason |
|------|--------|
| #4 Output consistency | Can iterate after CLI works |
| #6 Shell rewrites | Works for now, optimize later |
| #7 Incremental mode | Optimization, not blocking |

---

## 📋 Requirements Discovered

- [x] REQ-16: Config file must support all current hardcoded paths
- [x] REQ-17: Requirements.txt with all dependencies
- [x] REQ-18: Basic error handling (no silent failures)
- [x] REQ-19: CLI wrapper for all scripts
- [x] REQ-20: Document known limitations (shell scripts, no incremental)

---

## 🎯 Decision Recommendation

**Decision:** ✅ Fix P0 + P1 during separation (8-12 hours total)

**Scope:**
1. Config file for paths → 1-2 hours
2. requirements.txt → 30 minutes
3. Basic error handling → 2-3 hours
4. CLI wrapper → 4-6 hours

**Defer:**
- Output standardization (iterate later)
- Shell script conversion (works for now)
- Incremental mode (optimization)

**Timeline:**
- Day 1: Package structure + config + requirements
- Day 2: CLI wrapper + basic error handling
- Day 3: Testing + documentation
- Week 2+: Refinements and enhancements

---

**Last Updated:** 2025-12-16

