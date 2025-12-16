# Requirements - Inventory Repository Separation

**Source:** Research on inventory-repository-separation  
**Status:** Draft  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 📋 Overview

This document captures requirements discovered during research on separating the inventory system into its own repository with a unified CLI tool.

**Research Source:** [research-summary.md](research-summary.md)

---

## ✅ Functional Requirements

### FR-1: Single Entry Point CLI Command

**Description:** The tool should provide a single CLI command (`pinv`) as the entry point for all operations.

**Source:** [research-cli-tool-architecture.md](research-cli-tool-architecture.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### FR-2: Scan Commands

**Description:** The CLI should provide scan commands to discover projects:
- `pinv scan github` - Scan GitHub repositories
- `pinv scan local` - Scan local project directories
- `pinv scan all` - Combined scan

**Source:** [research-cli-tool-architecture.md](research-cli-tool-architecture.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### FR-3: Analysis Commands

**Description:** The CLI should provide analysis commands:
- `pinv analyze` or `pinv analyze tech-stack` - Analyze technologies used
- `pinv classify` - Classify projects by type

**Source:** [research-cli-tool-architecture.md](research-cli-tool-architecture.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### FR-4: Processing Commands

**Description:** The CLI should provide processing commands:
- `pinv dedupe` - Deduplicate scanned projects
- `pinv report` - Generate reports

**Source:** [research-cli-tool-architecture.md](research-cli-tool-architecture.md)

**Priority:** 🟡 Medium

**Status:** 🔴 Pending

---

### FR-5: Export Commands

**Description:** The CLI should provide export commands:
- `pinv export json` - Export to JSON file
- `pinv export api` - Push to work-prod API

**Source:** [research-cli-tool-architecture.md](research-cli-tool-architecture.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### FR-6: Configuration File Support

**Description:** The tool should support a YAML configuration file at `~/.config/pinv/config.yaml` for:
- Scan directories
- GitHub settings
- Output preferences
- API integration settings

**Source:** [research-configuration.md](research-configuration.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### FR-7: Environment Variable Overrides

**Description:** All configuration should be overridable via environment variables with `PINV_` prefix.

**Source:** [research-configuration.md](research-configuration.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### FR-8: Default Config Creation

**Description:** On first run, if no config exists, create a default config file and notify the user.

**Source:** [research-configuration.md](research-configuration.md)

**Priority:** 🟡 Medium

**Status:** 🔴 Pending

---

## 🎯 Non-Functional Requirements

### NFR-1: Use Typer CLI Framework

**Description:** The CLI should be built using the Typer framework for:
- Type hint-based argument parsing
- Auto-generated help text
- Shell completion support

**Source:** [research-cli-framework.md](research-cli-framework.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### NFR-2: Rich Terminal Output

**Description:** The CLI should use Rich library for:
- Colored output
- Progress bars for long operations
- Tables for data display

**Source:** [research-cli-framework.md](research-cli-framework.md)

**Priority:** 🟡 Medium

**Status:** 🔴 Pending

---

### NFR-3: Pydantic Configuration Validation

**Description:** Configuration should be validated using Pydantic for type safety and clear error messages.

**Source:** [research-configuration.md](research-configuration.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### NFR-4: XDG Directory Compliance

**Description:** The tool should follow XDG Base Directory Specification:
- Config: `~/.config/pinv/`
- Data: `~/.local/share/pinv/`
- Cache: `~/.cache/pinv/` (if needed)

**Source:** [research-configuration.md](research-configuration.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### NFR-5: Pip Installable

**Description:** The tool should be installable via pip:
- `pip install .` from local
- `pip install git+https://github.com/...` from GitHub

**Source:** [research-cli-tool-architecture.md](research-cli-tool-architecture.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

### NFR-6: Error Handling

**Description:** The tool should handle errors gracefully:
- No silent failures
- Clear error messages
- Non-zero exit codes on failure

**Source:** [research-tech-debt.md](research-tech-debt.md)

**Priority:** 🔴 High

**Status:** 🔴 Pending

---

## ⚠️ Constraints

### C-1: Python 3.10+

**Description:** The tool requires Python 3.10 or higher for type hint syntax.

**Source:** Typer requirements

---

### C-2: Existing Script Compatibility

**Description:** The CLI should wrap existing scripts without major rewrites initially. Shell scripts can remain as-is for Phase 1.

**Source:** [research-tech-debt.md](research-tech-debt.md)

---

### C-3: No Backward Compatibility Required

**Description:** Since this is a new tool in a new repo, no backward compatibility with current scripts is required.

**Source:** Separation decision

---

## 💭 Assumptions

### A-1: Single User Tool

**Description:** The tool is designed for single-user use on a development machine. Multi-user/server deployment is not a requirement.

**Source:** Project context

---

### A-2: GitHub Token via Environment

**Description:** GitHub token will be provided via `GITHUB_TOKEN` or `PINV_GITHUB_TOKEN` environment variable.

**Source:** [research-configuration.md](research-configuration.md)

---

### A-3: Work-Prod API Available

**Description:** For `pinv export api`, the work-prod API must be running and accessible.

**Source:** Integration requirements

---

## 🔗 Related Documents

- [Research Summary](research-summary.md)
- [Research: CLI Tool Architecture](research-cli-tool-architecture.md)
- [Research: CLI Framework](research-cli-framework.md)
- [Research: Configuration](research-configuration.md)
- [Research: Technical Debt](research-tech-debt.md)

---

## 🚀 Next Steps

1. Review and refine requirements
2. Use `/decision inventory-repository-separation --from-research` to make decisions
3. Create ADR documenting these decisions
4. Update transition plan
5. Begin implementation

---

**Last Updated:** 2025-12-16

