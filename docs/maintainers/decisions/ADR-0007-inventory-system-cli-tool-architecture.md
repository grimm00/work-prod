# ADR-0007: Inventory System CLI Tool Architecture

**Status:** Accepted  
**Date:** 2025-12-16  
**Supersedes:** None  
**Superseded By:** N/A

---

## Context

The inventory system (`scripts/inventory/`) is being separated from work-prod into its own repository. This decision was made in a prior reflection to enable:
- Independent evolution without affecting main repo
- Different development cadence (periodic refresh vs. continuous)
- Technical debt isolation
- Potential reusability for others

**Key Question:** How should the inventory system be restructured during separation?

**Research Conducted:**
- [Exploration: Inventory Repository Separation](../exploration/inventory-repository-separation/README.md)
- [Research: CLI Tool Architecture](../research/inventory-repository-separation/research-cli-tool-architecture.md)
- [Research: CLI Framework Selection](../research/inventory-repository-separation/research-cli-framework.md)
- [Research: Configuration Management](../research/inventory-repository-separation/research-configuration.md)
- [Research: Technical Debt Prioritization](../research/inventory-repository-separation/research-tech-debt.md)

**Current State:**
- 6 separate scripts (Python + Shell)
- Hardcoded paths (non-portable)
- No unified interface
- No configuration management
- 7 known technical debt items

**Constraints:**
- Limited time (target: ~10 hours)
- Should be usable quickly
- Must integrate with work-prod API

---

## Decision

Build a **unified CLI tool** (named `pinv`) as a proper Python package, rather than simply moving scripts to a new repository.

### Key Decisions

| Decision Point | Choice | Rationale |
|----------------|--------|-----------|
| **Approach** | Unified CLI tool | Better UX, foundation for future |
| **Framework** | Typer | Modern, type hints, minimal boilerplate |
| **Configuration** | YAML + Pydantic + XDG | Standard locations, type-safe |
| **Technical Debt** | Fix P0 + P1 during separation | Necessary for portability |

### Repository & Package Structure

```
project-inventory/           # Repository name
├── pyproject.toml           # Modern Python packaging
├── requirements.txt
├── README.md
├── pinv/                    # Package name
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── cli.py               # Typer app
│   ├── config.py            # Pydantic config
│   ├── commands/            # Subcommands
│   ├── scanners/            # GitHub + local scanning
│   └── utils/               # Helpers
└── tests/
```

### CLI Command Structure

```bash
pinv scan github       # Scan GitHub repos
pinv scan local        # Scan local projects
pinv analyze           # Analyze tech stack + classify
pinv dedupe            # Deduplicate results
pinv export json       # Export to JSON
pinv export api        # Push to work-prod API
```

### Configuration

| Setting | Value |
|---------|-------|
| Config File | `~/.config/pinv/config.yaml` |
| Data Directory | `~/.local/share/pinv/` |
| Environment Prefix | `PINV_` |
| Validation | Pydantic |

---

## Consequences

### Positive

- **Better UX:** Single entry point (`pinv`) instead of 6 separate scripts
- **Professional Tool:** Typer + Rich provides beautiful output, help text, progress bars
- **Portable:** XDG config removes hardcoded paths
- **Foundation:** CLI wrapper enables future enhancements
- **Consistent:** Follows same patterns as work-prod's `proj` CLI
- **Reduces Debt:** CLI tool addresses #5 (orchestrator) and #4 (output consistency)

### Negative

- **More Initial Work:** ~6-10 hours vs ~4-6 hours for simple separation
- **New Dependency:** Adds Typer, Pydantic, PyYAML
- **Learning Curve:** Typer is new (though similar to existing argparse patterns)

### Deferred

- Shell script conversion to Python (works as-is)
- Incremental scanning mode
- Output format standardization (iterate after CLI works)

---

## Alternatives Considered

### Alternative 1: Simple Script Separation

**Description:** Move scripts to new repo as-is, add requirements.txt

**Pros:**
- Fastest implementation (4-6 hours)
- No new dependencies
- Minimal changes

**Cons:**
- Poor UX (6 separate scripts)
- No shared configuration
- Inconsistent interfaces
- Harder to extend

**Why Not Chosen:** The UX improvement from CLI justifies the moderate additional effort.

### Alternative 2: Full-Featured CLI (Option C)

**Description:** Build complete CLI with all bells and whistles from day one

**Pros:**
- Professional tool
- All features immediately

**Cons:**
- Higher effort (12-16 hours)
- Scope creep risk
- May over-engineer

**Why Not Chosen:** Option B provides foundation; can evolve to C over time.

### Alternative 3: Keep in work-prod Repository

**Description:** Don't separate; keep inventory scripts in work-prod

**Pros:**
- No separation effort
- Single repo

**Cons:**
- Different cadences conflict
- Clutters main repo
- Technical debt stays

**Why Not Chosen:** Decided against in prior reflection; separation enables better organization.

---

## Implementation Notes

### Phase 1: Foundation (Day 1, ~2-3 hours)
- Create package structure
- Add pyproject.toml with entry point
- Create basic Pydantic config
- Add requirements.txt

### Phase 2: CLI Wrapper (Day 2, ~4-5 hours)
- Create Typer app with subcommands
- Wrap existing scripts as commands
- Add basic error handling
- Test basic workflows

### Phase 3: Polish (Day 3, ~2-3 hours)
- Testing and documentation
- First-run config creation
- Progress bars and colors

### Dependencies

```
typer[all]>=0.9.0
pyyaml>=6.0
pydantic-settings>=2.0
```

### Requirements Impact

This decision implements or enables:
- FR-1: Single entry point CLI command ✅
- FR-2-5: Scan/Analyze/Process/Export commands ✅
- FR-6-8: Configuration support ✅
- NFR-1: Typer framework ✅
- NFR-2: Rich terminal output ✅
- NFR-3: Pydantic validation ✅
- NFR-4: XDG compliance ✅

---

## References

- [Exploration: Inventory Repository Separation](../exploration/inventory-repository-separation/README.md)
- [Research Hub](../research/inventory-repository-separation/README.md)
- [Research Summary](../research/inventory-repository-separation/research-summary.md)
- [Requirements Document](../research/inventory-repository-separation/requirements.md)
- [Existing Transition Plan](../planning/infrastructure/inventory-repository-separation/transition-plan.md)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

**Last Updated:** 2025-12-16

