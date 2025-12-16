# Inventory Repository Separation - Exploration Hub

**Purpose:** Deep exploration of inventory system separation into dedicated repository  
**Status:** 🟠 Exploration  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

- **[Exploration Document](exploration.md)** - Main exploration document
- **[Research Topics](research-topics.md)** - Research questions to investigate

### Related Documentation

- **[Infrastructure Plan](../../planning/infrastructure/inventory-repository-separation/README.md)** - High-level infrastructure plan
- **[Transition Plan](../../planning/infrastructure/inventory-repository-separation/transition-plan.md)** - Implementation phases
- **[Original Reflection](../../planning/notes/reflections/reflection-inventory-poc-repository-placement-2025-12-07.md)** - Decision rationale

---

## 🎯 Overview

This exploration goes deeper into the inventory repository separation to identify specific research questions, evaluate options, and prepare for implementation. The high-level decision has been made (separate repository recommended), but several questions remain about:

- **🆕 Unified CLI Tool** - Should we create a central CLI app instead of just separating scripts?
- Repository naming and structure
- Git history preservation strategies
- Script organization patterns
- Configuration management approaches
- Integration patterns with work-prod
- Technical debt prioritization

### Scope Consideration (2025-12-16)

**New idea:** Instead of just separating inventory scripts, create a **unified CLI tool** that serves as the central "project management" interface with commands like:

```bash
pinv scan github       # Scan GitHub repos
pinv scan local        # Scan local projects
pinv analyze tech      # Analyze tech stack
pinv export api        # Push to work-prod API
```

This changes the scope from "move scripts to new repo" to "create a professional CLI tool".

---

## 📊 Status

**Current Phase:** Exploration  
**Prior Work:** Phase 1 of transition plan complete (documentation)  
**Next Step:** Conduct research on topics identified in research-topics.md

---

## 🔗 Context

### What's Already Decided

| Decision | Status | Source |
|----------|--------|--------|
| Separate repository | ✅ Decided | Reflection document |
| Mapping script stays in work-prod | ✅ Decided | Transition plan |
| Historical artifacts preserved | ✅ Decided | Exploration README |

### What Needs Research

| Topic | Priority | Status |
|-------|----------|--------|
| **🆕 Unified CLI Tool (gating)** | 🔴 HIGH | 🔴 Not Started |
| Repository name | HIGH | 🔴 Not Started |
| **🆕 CLI Naming & Distribution** | MEDIUM | 🔴 Not Started |
| Git history preservation | MEDIUM | 🔴 Not Started |
| Script organization patterns | MEDIUM | 🔴 Not Started |
| Configuration management | HIGH | 🔴 Not Started |
| Technical debt prioritization | HIGH | 🔴 Not Started |
| Integration patterns | MEDIUM | 🔴 Not Started |

---

**Last Updated:** 2025-12-16

