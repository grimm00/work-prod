# Maintainers Hub

**Purpose:** Central hub for maintainer-facing documentation and project management  
**Status:** ✅ Active  
**Version:** v0.1.0 MVP Released (2025-12-07)  
**Last Updated:** 2025-12-07

---

## 📋 Quick Links

### Core Management

- **[Exploration Hub](exploration/README.md)** - Requirements gathering and discovery (✅ Complete)
- **[Research Hub](research/README.md)** - Technical research and analysis (✅ Week 1 Complete)
- **[Planning Hub](planning/README.md)** - Feature planning, releases, and project phases (🟡 Planned)
- **[Decisions Hub](decisions/README.md)** - Architecture Decision Records / ADRs (✅ 4 ADRs)
- **[Feedback](feedback/)** - External code reviews and feedback (🔴 Not Started)
- **[Archived](archived/)** - Historical documentation (🔴 Empty)

---

## 🎯 Overview

The maintainers directory serves as the central coordination point for project maintainers, providing documentation for planning, decisions, and project management throughout the project lifecycle.

### Key Functions

1. **Exploration** - Requirements gathering and user needs discovery
2. **Research** - Technical analysis and evaluation (organized by category)
3. **Planning Management** - Feature planning, releases, and project phases
4. **Decision Tracking** - Architecture Decision Records (ADRs) with rationale
5. **Feedback Integration** - External code reviews and feedback
6. **Historical Preservation** - Archived documentation and superseded documents

---

## 📁 Directory Structure

```
docs/maintainers/
├── README.md          # 📍 HUB - This file
├── exploration/       # 📡 SPOKE - Requirements and discovery
├── research/          # 📡 SPOKE - Technical research (organized by category)
│   ├── tech-stack/    # Technology & framework decisions
│   ├── microsoft/     # Microsoft integrations
│   ├── miro/          # Miro platform
│   ├── data-models/   # Database & data structures
│   ├── ui-ux/         # UI/UX patterns
│   ├── security/      # Security & privacy
│   └── features/      # Feature-specific research
├── planning/          # 📡 SPOKE - Project planning hub
│   ├── features/      # Feature-based planning
│   ├── releases/      # Release management
│   └── notes/         # Planning notes and opportunities
├── decisions/         # 📡 SPOKE - Architecture Decision Records (ADRs)
├── feedback/          # 📡 SPOKE - External code reviews
└── archived/          # 📡 SPOKE - Historical documentation
```

---

## 🎨 Design Patterns

### Hub-and-Spoke Documentation

- Each subdirectory has its own README.md hub
- Hub files provide quick links to spoke documents
- Spoke documents focus on single topics
- Progressive disclosure: Overview → Details → Analysis

### Feature-Based Planning

- Features organized under `planning/features/`
- Each feature has hub-and-spoke documentation
- Includes fix directories for troubleshooting
- Status tracking with consistent indicators

### Decision Documentation

- Architecture Decision Records (ADRs) in `decisions/`
- Options analysis and rationale
- Historical context preservation
- Lessons learned documentation

---

## 🚀 Quick Start

### For Exploration & Research

1. Create exploration document: `exploration/[topic].md`
2. Document requirements, research findings, or analysis
3. Link to relevant planning or decision documents
4. Update exploration hub with new document

### For New Features

1. Create feature directory: `planning/features/[feature-name]/`
2. Add README.md hub with quick links
3. Create feature-plan.md with overview
4. Add phase documents as needed

### For Releases

1. Create release directory: `planning/releases/vX.Y.Z/`
2. Add checklist.md and release-notes.md
3. Update release history

### For Decisions

1. Create ADR: `decisions/0001-[decision-name].md`
2. Document context, decision, and consequences
3. Link to related planning documents

---

## 📚 Related Documentation

### Exploration

- [Exploration Hub](exploration/README.md) - Requirements gathering and research

### Planning

- [Planning Hub](planning/README.md) - Project planning overview
- [Feature Planning](planning/features/README.md) - Feature development process
- [Release Process](planning/releases/README.md) - Release management

### Decisions

- [Architecture Decisions](decisions/) - ADR index

### Feedback

- [External Reviews](feedback/) - Code review feedback

---

**Last Updated:** 2025-11-26  
**Status:** ✅ Active  
**Next:** Complete exploration phase requirements gathering

