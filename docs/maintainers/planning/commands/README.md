# Commands Planning

**Purpose:** Track command usage and status for work-prod  
**Status:** ✅ Active  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

### Status & Tracking

- **[Usage Tracker](usage-tracker.md)** - Command usage tracking for graduation feedback

---

## 🎯 Overview

This directory tracks command usage in work-prod. Work-prod uses commands from the dev-infra template, and usage tracking here helps:

1. **Validate commands work** - Track successful uses in a real project
2. **Provide feedback** - Inform dev-infra about command effectiveness
3. **Identify issues** - Log problems for dev-infra improvements

---

## 🔄 Relationship to Dev-Infra

```
Dev-Infra (Template Factory)
        │
        ├── Develops commands
        ├── Graduates to templates
        │
        ▼
Work-Prod (Uses Templates)
        │
        ├── Uses commands
        ├── Tracks usage
        └── Provides feedback → Dev-Infra
```

**Current Commands:** 18 (from dev-infra template)

---

## 📁 Directory Structure

```
planning/commands/
├── README.md           # 📍 HUB - This file
└── usage-tracker.md    # Usage tracking for feedback
```

---

**Last Updated:** 2025-12-16


