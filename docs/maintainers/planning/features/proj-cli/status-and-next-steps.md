# proj-cli - Status and Next Steps

**Feature:** Unified CLI Tool  
**Status:** 🔴 Not Started  
**Last Updated:** 2025-12-16

---

## 📊 Current Status

| Phase | Focus | Effort | Status |
|-------|-------|--------|--------|
| 1 | Repository Setup | ~2-3 hrs | 🔴 Not Started |
| 2 | Migrate Project Commands | ~3-4 hrs | 🔴 Not Started |
| 3 | Add Inventory Commands | ~3-4 hrs | 🔴 Not Started |
| 4 | Polish & Cleanup | ~2-3 hrs | 🔴 Not Started |
| **Total** | | **~10-14 hrs** | |

---

## ✅ Completed

*Nothing completed yet.*

---

## 🟠 In Progress

*Nothing in progress yet.*

---

## 🔜 Next Steps

### Immediate (Pre-requisites)

1. **Create `proj-cli` repository:**
   ```bash
   cd ~/Projects/dev-infra
   ./new-project.sh proj-cli
   ```

2. **Begin Phase 1 implementation:**
   - Use `/task-phase --phase 1` in proj-cli project
   - Follow TDD workflow in `phase-1.md`

### Phase 1 Key Tasks

1. Create package structure with `src/proj/`
2. Add `pyproject.toml` with `proj` entry point
3. Create Pydantic config with XDG paths
4. Implement basic Typer app

---

## 📋 Requirements Checklist

### Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1 | Single entry point (`proj`) | 🔴 High | 🔴 Pending |
| FR-2 | Scan commands | 🔴 High | 🔴 Pending |
| FR-3 | Analysis commands | 🔴 High | 🔴 Pending |
| FR-4 | Processing commands | 🟡 Medium | 🔴 Pending |
| FR-5 | Export commands | 🔴 High | 🔴 Pending |
| FR-6 | Config file support | 🔴 High | 🔴 Pending |
| FR-7 | Environment overrides | 🔴 High | 🔴 Pending |
| FR-8 | Default config creation | 🟡 Medium | 🔴 Pending |

### Non-Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| NFR-1 | Typer framework | 🔴 High | 🔴 Pending |
| NFR-2 | Rich terminal output | 🟡 Medium | 🔴 Pending |
| NFR-3 | Pydantic validation | 🔴 High | 🔴 Pending |
| NFR-4 | XDG compliance | 🔴 High | 🔴 Pending |
| NFR-5 | Pip installable | 🔴 High | 🔴 Pending |
| NFR-6 | Error handling | 🔴 High | 🔴 Pending |

---

## 🎯 Success Criteria

- [ ] `proj` command installable via `pip install .`
- [ ] All existing `proj` commands work (list, get, create, update, delete, search, import)
- [ ] New `proj inv` subcommands functional
- [ ] Configuration via `~/.config/proj/config.yaml`
- [ ] XDG directory compliance
- [ ] work-prod `scripts/project_cli/` removed
- [ ] Basic tests passing

---

## 📚 References

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Transition Plan](transition-plan.md)
- [ADR-0007](../../../decisions/ADR-0007-inventory-system-cli-tool-architecture.md)

---

**Last Updated:** 2025-12-16

