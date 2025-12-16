# Documentation Examples

**Purpose:** Best practices and patterns for project documentation  
**Status:** ✅ Active  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

### Patterns

- **[Hub-and-Spoke Pattern](hub-and-spoke-pattern.md)** - Core documentation organization pattern
- **[Feature Planning Example](feature-planning-example.md)** - Example from Projects feature

---

## 📊 Overview

This directory contains documentation examples and best practices extracted from the work-prod project. Use these as reference when:

- Creating new feature documentation
- Organizing planning documents
- Setting up hub-and-spoke structures
- Onboarding new contributors

---

## 🎯 Key Patterns

### 1. Hub-and-Spoke Organization

Every directory has a **hub** (`README.md`) that links to **spokes** (detailed documents):

```
feature/
├── README.md           # Hub: Overview and quick links
├── feature-plan.md     # Spoke: Detailed plan
├── status.md           # Spoke: Current status
└── phase-1.md          # Spoke: Phase details
```

### 2. Progressive Disclosure

Start with overview, link to details:
- **Level 1:** Quick Links section (immediate navigation)
- **Level 2:** Summary/Overview (context)
- **Level 3:** Linked documents (full details)

### 3. Status Indicators

Use consistent status markers:
- 🔴 **Not Started** - Planning stage only
- 🟡 **Planned** - Approved but not begun
- 🟠 **In Progress** - Active development
- ✅ **Complete/Active** - Finished or operational
- ⏸️ **Deferred** - Intentionally postponed

### 4. Document Header

Every document should have:
- **Purpose:** One-line description
- **Status:** Current status indicator
- **Last Updated:** Date (YYYY-MM-DD format)

---

## 📁 Directory Structure

```
examples/
├── README.md                      # This file (hub)
├── hub-and-spoke-pattern.md       # Pattern documentation
└── feature-planning-example.md    # Real-world example
```

---

## 🔗 Related

- **[Planning Hub](../../README.md)** - Main planning directory
- **[Reflections](../reflections/README.md)** - Project reflections

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active

