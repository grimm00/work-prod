# Command Adaptations for Dev-Infra

**Purpose:** Document how to adapt work-prod commands for dev-infra template  
**Status:** ✅ Active  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Quick Links

### Command Adaptation Documents

- **[int-opp Adaptation](int-opp-adaptation.md)** - How to adapt `/int-opp` command for dev-infra (✅ Documented)
- **[reflect Adaptation](reflect-adaptation.md)** - How to adapt `/reflect` command for dev-infra (✅ Documented)
- **[fix-plan Adaptation](fix-plan-adaptation.md)** - How to adapt `/fix-plan` command for dev-infra (✅ Documented)
- **[transition-plan Adaptation](transition-plan-adaptation.md)** - How to adapt `/transition-plan` command for dev-infra (✅ Documented)
- **[task-phase Adaptation](task-phase-adaptation.md)** - How to adapt `/task-phase` command for dev-infra (✅ Documented)
- **[Command Adaptation Guide](command-adaptation-guide.md)** - General guide for adapting commands
- **[Command Coverage](command-coverage.md)** - Track which commands have adaptation documentation

---

## 🎯 Overview

This directory contains documentation on how to adapt work-prod Cursor commands for use in the dev-infra template. These adaptations make commands generic and reusable across projects.

**Goal:** Enable dev-infra to use work-prod's proven command workflows with appropriate adaptations for template context.

---

## 📊 Summary

**Total Adaptation Documents:** 6  
**Status:** ✅ Active

**Commands to Adapt:**
- `/int-opp` - Internal opportunities command (✅ Documented)
- `/reflect` - Reflection workflow (✅ Documented)
- `/fix-plan` - Fix planning workflow (✅ Documented)
- `/transition-plan` - Transition planning (✅ Documented)
- `/task-phase` - Phase implementation workflow (✅ Documented)
- `/pr` - PR creation workflow (🔴 HIGH Priority - Not Documented)
- `/fix-implement` - Fix implementation workflow (🔴 HIGH Priority - Not Documented)
- `/fix-review` - Fix review workflow (🔴 HIGH Priority - Not Documented)
- `/post-pr` - Post-merge documentation (🔴 HIGH Priority - Not Documented)
- `/reflection-artifacts` - Artifact extraction (🔴 HIGH Priority - Not Documented)

**See:** [Command Coverage](command-coverage.md) for complete status

---

## 🔄 Adaptation Process

1. **Identify Command** - Select command to adapt
2. **Analyze Dependencies** - Identify project-specific assumptions
3. **Document Adaptations** - Create adaptation document
4. **Provide Examples** - Show before/after patterns
5. **Update Dev-Infra** - Apply adaptations to template

---

## 📝 Adaptation Principles

**Make Generic:**
- Remove work-prod-specific paths
- Use configurable project names
- Support multiple project types

**Preserve Patterns:**
- Keep proven workflows
- Maintain command structure
- Preserve best practices

**Document Changes:**
- Clear before/after examples
- Rationale for each change
- Implementation steps

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Continue documenting command adaptations

