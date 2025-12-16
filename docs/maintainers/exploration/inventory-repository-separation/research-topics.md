# Research Topics - Inventory Repository Separation

**Purpose:** List of research topics/questions to investigate  
**Status:** 🔴 Pending Research  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 📋 Research Topics

This document lists research topics and questions that need investigation before implementing the repository separation.

---

### Research Topic 1: Repository Naming & Structure

**Question:** What should the new repository be named and how should it be structured?

**Why:** The name sets expectations for the project's purpose and scope. Structure decisions affect maintainability.

**Sub-questions:**
- What naming conventions exist for similar tools?
- Should it be specific (project-inventory) or generic (inventory-tools)?
- What's the long-term vision for this tool?
- Should it be a Python package or standalone scripts?

**Priority:** 🔴 HIGH

**Status:** 🔴 Not Started

**Approach:**
- Review similar tools on GitHub
- Consider future expansion possibilities
- Evaluate Python package vs. scripts tradeoffs

---

### Research Topic 2: Git History Preservation

**Question:** Should we preserve git history during separation, and if so, how?

**Why:** History provides context for decisions, but adds complexity to the migration.

**Sub-questions:**
- What's the real value of preserving history for these scripts?
- How complex is git subtree split vs. filter-repo?
- What do we lose with a fresh start?
- Can we document decisions without preserving commits?

**Options to research:**
- `git subtree split` - Split subdirectory with history
- `git filter-repo` - More powerful, preserves everything
- Fresh start with reference commit - Link to original repo

**Priority:** 🟡 MEDIUM

**Status:** 🔴 Not Started

**Approach:**
- Estimate complexity of each approach
- Evaluate actual history value (how many commits?)
- Decide based on effort/value ratio

---

### Research Topic 3: Script Organization Patterns

**Question:** What's the best way to organize inventory scripts for maintainability?

**Why:** Current flat structure works but may not scale. Reorganization during migration is efficient.

**Sub-questions:**
- What patterns do similar Python CLI tools use?
- Should we add a `src/` directory structure?
- How do we balance simplicity with organization?
- Should shell scripts be converted to Python?

**Priority:** 🟡 MEDIUM

**Status:** 🔴 Not Started

**Approach:**
- Review Python project layout best practices
- Evaluate complexity of current scripts
- Decide on minimal viable structure

---

### Research Topic 4: Configuration Management

**Question:** How should configuration be managed in the new repository?

**Why:** Current hardcoded paths are the biggest technical debt item. Configuration is essential for portability.

**Sub-questions:**
- YAML vs. JSON vs. Python config?
- Config file location patterns?
- Environment variable overrides?
- How to handle sensitive paths?

**Options to research:**
- `~/.config/project-inventory/config.yaml` - XDG standard
- `config.yaml` in repo with gitignore - Simple
- Environment variables only - 12-factor style
- Python `configparser` or `pydantic` - Type-safe

**Priority:** 🔴 HIGH

**Status:** 🔴 Not Started

**Approach:**
- Review Python configuration best practices
- Evaluate portability requirements
- Design minimal config schema

---

### Research Topic 5: Technical Debt Prioritization

**Question:** Which technical debt items should be addressed during separation vs. after?

**Why:** Limited time and scope creep risk. Need to prioritize effectively.

**Known technical debt:**
1. Hardcoded paths (blocking portability)
2. No error handling (reliability)
3. Missing dependencies file (reproducibility)
4. Inconsistent output formats (integration)
5. No master orchestrator (usability)
6. Shell script limitations (maintainability)
7. No incremental mode (efficiency)

**Sub-questions:**
- Which items block separation?
- Which items add the most value?
- What's the minimum viable state?
- What can be deferred to post-separation?

**Priority:** 🔴 HIGH

**Status:** 🔴 Not Started

**Approach:**
- Categorize by blocking/non-blocking
- Estimate effort for each
- Create phased plan

---

### Research Topic 6: Integration Patterns

**Question:** How should the new inventory repo integrate with work-prod?

**Why:** Need to maintain workflow for importing projects into Projects API.

**Sub-questions:**
- Manual file copy vs. export command vs. API client?
- How does mapping script fit in?
- Should new repo have API client for work-prod?
- Future: automated sync?

**Current workflow:**
```
inventory scripts → inventory-data.json → map_inventory.py → API import
```

**Options:**
- A: Manual workflow (copy files between repos)
- B: Export command (new repo outputs work-prod format)
- C: Direct API (new repo has API client)

**Priority:** 🟡 MEDIUM

**Status:** 🔴 Not Started

**Approach:**
- Document current workflow in detail
- Evaluate automation opportunities
- Recommend phased approach

---

## 🎯 Research Workflow

1. **Conduct research** using `/research inventory-repository-separation --from-explore`
2. Research will create documents in `docs/maintainers/research/inventory-repository-separation/`
3. After research complete, update transition plan with decisions
4. Begin Phase 2 implementation

---

## 📊 Research Prioritization

| Topic | Priority | Blocking? | Effort | Order |
|-------|----------|-----------|--------|-------|
| Repository Naming | HIGH | Yes | LOW | 1st |
| Configuration Management | HIGH | Yes | MEDIUM | 2nd |
| Technical Debt Prioritization | HIGH | Yes | LOW | 3rd |
| Git History | MEDIUM | No | MEDIUM | 4th |
| Script Organization | MEDIUM | No | MEDIUM | 5th |
| Integration Patterns | MEDIUM | No | LOW | 6th |

**Recommended approach:** Research topics 1, 4, 5 first (blocking decisions), then 2, 3, 6 (implementation details).

---

**Last Updated:** 2025-12-16

