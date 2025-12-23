# Inventory Repository Separation - Exploration Hub

**Purpose:** Deep exploration of inventory system separation into dedicated repository  
**Status:** ✅ Research Complete  
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

**Current Phase:** ✅ Research Complete  
**Prior Work:** Phase 1 of transition plan complete (documentation)  
**Research:** [Research Hub](../../research/inventory-repository-separation/README.md) - All topics researched  
**Next Step:** Use `/decision` to create ADR, then update transition plan

---

## 🔗 Context

### What's Already Decided

| Decision | Status | Source |
|----------|--------|--------|
| Separate repository | ✅ Decided | Reflection document |
| Mapping script stays in work-prod | ✅ Decided | Transition plan |
| Historical artifacts preserved | ✅ Decided | Exploration README |

### Research Complete ✅

| Topic | Priority | Status | Decision |
|-------|----------|--------|----------|
| **Unified CLI Tool** | 🔴 HIGH | ✅ Complete | YES - Build CLI |
| **CLI Framework** | 🔴 HIGH | ✅ Complete | Typer |
| **Configuration** | 🔴 HIGH | ✅ Complete | YAML + Pydantic |
| **Tech Debt Priority** | 🔴 HIGH | ✅ Complete | Fix P0 + P1 |
| Repository name | HIGH | 🟡 Addressed | `project-inventory` |
| CLI Naming | MEDIUM | 🟡 Addressed | `pinv` |
| Git history | MEDIUM | ⏳ Deferred | TBD |
| Script organization | MEDIUM | 🟡 Addressed | Package structure |
| Integration patterns | MEDIUM | 🟡 Addressed | API command |

**Full Research:** [Research Hub](../../research/inventory-repository-separation/README.md)

---

**Last Updated:** 2025-12-16

