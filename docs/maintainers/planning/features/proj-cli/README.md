# proj-cli Feature Hub

**Feature:** Unified CLI Tool  
**Status:** 🔴 Not Started  
**Created:** 2025-12-16  
**ADR:** [ADR-0007](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)

---

## 📋 Quick Links

### Planning Documents

- **[Feature Plan](feature-plan.md)** - Overview and success criteria
- **[Transition Plan](transition-plan.md)** - Detailed implementation approach
- **[Status & Next Steps](status-and-next-steps.md)** - Current progress tracking

### Phase Documents

- **[Phase 1: Repository Setup](phase-1.md)** - Create proj-cli repository (~2-3 hours) 🔴
- **[Phase 2: Migrate Project Commands](phase-2.md)** - Move proj commands (~3-4 hours) 🔴
- **[Phase 3: Add Inventory Commands](phase-3.md)** - Add proj inv subcommands (~3-4 hours) 🔴
- **[Phase 4: Polish & Cleanup](phase-4.md)** - Testing, docs, work-prod cleanup (~2-3 hours) 🔴

### Supporting Documents

- **[Fix Tracking](fix/README.md)** - Issue tracking and fixes
- **[Deliverables](deliverables/README.md)** - Planning outputs

### Research & Decisions

- **[ADR-0007: Unified CLI Architecture](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)** - Architecture decision
- **[Research Hub](../../../research/inventory-repository-separation/README.md)** - Supporting research
- **[Requirements](../../../research/inventory-repository-separation/requirements.md)** - Functional and non-functional requirements

---

## 🎯 Overview

Build a unified CLI tool (`proj`) that consolidates project management commands and inventory scanning into a single, professional tool. The CLI will live in its own repository (`proj-cli`), making work-prod API-only.

### Command Structure

```bash
# Project Management (migrated from work-prod)
proj list              # List all projects
proj get <id>          # Get project details
proj create "Name"     # Create project
proj update <id>       # Update project
proj delete <id>       # Delete project
proj search "query"    # Search projects
proj import file.json  # Import from JSON

# Inventory Management (new subcommands)
proj inv scan github   # Scan GitHub repos
proj inv scan local    # Scan local directories
proj inv analyze       # Analyze tech stack
proj inv dedupe        # Deduplicate results
proj inv export json   # Export to JSON
proj inv export api    # Push to work-prod API
```

---

## 📊 Progress Summary

| Phase | Focus | Effort | Status |
|-------|-------|--------|--------|
| 1 | Repository Setup | ~2-3 hrs | 🔴 Not Started |
| 2 | Migrate Project Commands | ~3-4 hrs | 🔴 Not Started |
| 3 | Add Inventory Commands | ~3-4 hrs | 🔴 Not Started |
| 4 | Polish & Cleanup | ~2-3 hrs | 🔴 Not Started |
| **Total** | | **~10-14 hrs** | |

---

## 🚀 Next Steps

1. Create `proj-cli` repository using `dev-infra/new-project.sh`
2. Begin Phase 1: Repository Setup
3. Use `/task-phase --phase 1` to implement

---

**Last Updated:** 2025-12-16

