# Project Inventory System - POC Analysis

**Status:** 🟡 POC Complete - Research Scheduled Week 4  
**Date:** 2025-12-01  
**Category:** Automation / Tooling  
**Related Research:** Scheduled for Week 4 (MEDIUM priority)

---

## 📋 Overview

This document analyzes the proof-of-concept (POC) implementation of the automated project inventory system. The POC was implemented rapidly to gather data for the Skills Matrix feature and to validate whether "Projects" should be a core feature. While functional and valuable, it has technical debt that should be addressed through proper research and architectural design in Week 4.

---

## ✅ What the POC Accomplished

### Data Collection Success

**59 Unique Projects Cataloged:**

- 12 projects with both GitHub + Local presence (merged)
- 14 GitHub-only repositories
- 33 Local-only projects
- 40 Git-tracked projects total
- 19 non-Git directories

**24 Languages/Technologies Identified:**

- Provided seed data for Skills Matrix feature
- Language usage statistics across all projects
- Project-to-technology mapping for skill validation

### Generated Documentation

1. **`current-state-inventory.md`** (18KB)

   - Comprehensive catalog of all projects
   - Grouped by user classification (Work/Personal/Learning/Inactive)
   - Shows merged GitHub + Local projects clearly (🔗 emoji)
   - Includes tech stack summary

2. **`discovered-skills.md`**
   - 24 unique languages discovered
   - Suggested confidence levels based on project count
   - Direct input for Skills Matrix feature planning

### User Value Delivered

- **Validated Skills Matrix data source** - Real technology usage vs. guessing
- **Validated "Projects" as potential 8th feature** - 59 projects shows significant need
- **Eliminated manual inventory work** - Automated discovery saved hours of manual cataloging
- **Classification system** - User can track Work vs. Personal vs. Learning projects
- **Deduplication intelligence** - Correctly identified 11 duplicate entries (GitHub repos with local clones)

---

## 🏗️ Current POC Architecture

### Script Pipeline (7 Scripts)

1. **`fetch-github-repos.sh`** (Bash)

   - Uses `gh` CLI to fetch all repos for grimm00 user
   - Outputs: `data/github-repos.json` (13KB)
   - Collects: name, description, URL, languages, dates, visibility

2. **`scan-local-projects.sh`** (Bash)

   - Scans `~/Projects` and `~/Learning` directories
   - Detects Git repos, remote URLs, commit dates
   - Analyzes file extensions for language detection
   - Outputs: `data/local-projects.json` (21KB)

3. **`analyze-tech-stack.py`** (Python)

   - Combines GitHub + Local language data
   - Generates usage statistics and percentages
   - Outputs: `data/tech-stack.json` (51KB)

4. **`deduplicate-projects.py`** (Python)

   - Matches local Git repos to GitHub repos by remote URL
   - Resolves classification conflicts (prefers local classification)
   - Outputs: `data/classifications-merged.json` (backup)
   - Updates: `data/classifications.json` with merged IDs

5. **`classify-projects.py`** (Python - Interactive)

   - User-driven classification into categories
   - Shows project context (languages, dates, paths)
   - Supports bulk operations
   - Saves progress incrementally
   - Outputs: `data/classifications.json` (3.8KB)

6. **`generate-report.py`** (Python - Legacy)

   - Original report generator (with duplicates)
   - No longer used, kept for reference

7. **`generate-report-deduplicated.py`** (Python)
   - Merges GitHub + Local data for unified view
   - Generates both inventory and skills documents
   - Uses emoji indicators (🔗 merged, ☁️ GitHub-only, 💻 Local-only)
   - Outputs final documentation files

### Data Flow

```
fetch-github-repos.sh → data/github-repos.json ─┐
                                                  ├→ analyze-tech-stack.py → data/tech-stack.json
scan-local-projects.sh → data/local-projects.json ┘                                ↓
                                ↓                                                   ↓
                    deduplicate-projects.py                                         ↓
                                ↓                                                   ↓
                    classify-projects.py → data/classifications.json               ↓
                                ↓                                                   ↓
                    generate-report-deduplicated.py ←───────────────────────────────┘
                                ↓
                    ┌───────────┴──────────────┐
                    ↓                          ↓
    current-state-inventory.md    discovered-skills.md
```

### Data Files (Gitignored)

- `data/github-repos.json` - Raw GitHub repository data
- `data/local-projects.json` - Raw local project scan data
- `data/tech-stack.json` - Combined language statistics
- `data/classifications.json` - User project classifications (deduplicated)
- `data/classifications-merged.json` - Backup of merged classifications
- `data/generated-inventory.md` - Legacy output (with duplicates)
- `data/generated-inventory-dedup.md` - Working copy of deduplicated report

---

## ⚠️ Known Technical Debt

### 1. Classification Data Stored Separately

**Current State:**

- Classification stored in `data/classifications.json` separate from project data
- Keys use format: `github:repo-name`, `local:/path/to/project`, `merged:repo-name`
- Requires joining data across files during report generation

**Issues:**

- Not normalized data model
- Repeated project information across files
- Classification changes require re-running generator
- No single source of truth for project metadata

**Better Approach (To Research):**

- Integrate classification as field within project JSON
- Unified project schema with source, classification, and metadata
- Versioned data model

### 2. Two Report Generators (Redundancy)

**Current State:**

- `generate-report.py` - Legacy, shows duplicates
- `generate-report-deduplicated.py` - Current, merges duplicates

**Issues:**

- Confusing which to use
- Code duplication
- Both maintained in codebase

**Better Approach:**

- Single generator with deduplication built-in
- Remove legacy script post-refactor

### 3. Late Deduplication

**Current State:**

- Deduplication happens after classification
- User may classify same project twice (GitHub + Local)
- Deduplication script resolves conflicts retroactively

**Issues:**

- User classified 70 projects instead of 59 unique
- 11 duplicates had to be reconciled
- 2 classification conflicts found after the fact

**Better Approach:**

- Deduplicate early (before classification)
- Present only unique projects for classification
- Avoid duplicate work

### 4. No Configuration Management

**Current State:**

- Hardcoded values scattered across scripts:
  - GitHub username: `grimm00`
  - Scan directories: `~/Projects`, `~/Learning`
  - Output paths: `data/`, `../../docs/maintainers/exploration/`
  - Limits: repo fetch limit (1000), etc.

**Issues:**

- Not reusable for others
- Changing config requires editing multiple scripts
- No central configuration file

**Better Approach (To Research):**

- External config file (`config.json` or `.env`)
- Config loader shared utility
- Document what can be configured

### 5. No Master Orchestration

**Current State:**

- Scripts run individually in sequence
- User must remember order
- No error handling between stages
- No "run full pipeline" command

**Issues:**

- Manual workflow is error-prone
- Difficult to re-run specific stages
- No progress reporting for full pipeline

**Better Approach:**

- Master `run-pipeline.sh` or `inventory.py` script
- Handles errors and dependencies
- Optional: skip stages if data exists
- Progress reporting

### 6. Inconsistent Error Handling

**Current State:**

- Some scripts exit on error (`set -e` in Bash)
- Python scripts use various error handling patterns
- No consistent logging format

**Issues:**

- Difficult to debug failures
- Inconsistent user experience
- No structured logging

**Better Approach:**

- Shared error handling utilities
- Consistent logging format across all scripts
- Graceful degradation where possible

### 7. Script Organization (Flat Structure)

**Current State:**

- All 7 scripts in single `scripts/inventory/` directory
- No subdirectories for organization
- No shared utilities library

**Issues:**

- Difficult to find scripts as system grows
- Code duplication (JSON loading, formatting, etc.)
- No clear separation of concerns

**Better Approach (To Research):**

- Possible structure:
  ```
  scripts/inventory/
  ├── collectors/     (fetch-github-repos.sh, scan-local-projects.sh)
  ├── processors/     (deduplicate, analyze, classify)
  ├── generators/     (generate-reports)
  ├── lib/            (shared utilities)
  └── config.json
  ```

---

## 💡 Value Delivered vs. Technical Debt

### High-Value Outcomes

✅ **Skills Matrix Seed Data** - 24 languages identified  
✅ **Projects Feature Validation** - 59 projects shows need  
✅ **Automation Proof** - Can programmatically discover projects  
✅ **Deduplication Works** - Successfully merged 11 duplicates  
✅ **User Classification System** - Categorization provides value

### Manageable Technical Debt

⚠️ POC remains functional for current needs  
⚠️ No breaking issues requiring immediate fix  
⚠️ Refactoring can wait for proper research phase  
⚠️ Week 2-4 priorities remain on user-facing features

---

## 🎯 Decision: Defer to Week 4

### Rationale

**Why Not Now:**

1. POC successfully delivered required data
2. Weeks 2-4 packed with HIGH priority user-facing feature research (15 topics)
3. Refactoring is technical improvement, not blocking MVP
4. Proper research and ADR should precede refactoring

**Why Week 4:**

1. Fits with other MEDIUM priority polish topics (UI, security, etc.)
2. Allows time to focus on core features first
3. Can learn from other automation needs that emerge
4. Natural point before implementation phase

**Deferred Items:**

- Full research document on data model options
- ADR-0005 for inventory system architecture
- Script refactoring and reorganization
- Configuration extraction
- Master orchestration script
- Shared utilities library

---

## 📝 Week 4 Research Questions (Preview)

When Week 4 arrives, research should address:

**Data Model:**

- Should classification be embedded in project JSON or separate?
- Unified schema vs source-specific schemas?
- How to version data model?
- Metadata to include (timestamps, sync status, etc.)?

**Pipeline Architecture:**

- What stages are needed? (Collect → Normalize → Deduplicate → Classify → Generate)
- Early vs late deduplication timing?
- Incremental updates vs full refresh?
- Error handling and rollback strategies?

**Configuration Management:**

- Config file format (JSON, YAML, .env)?
- What should be configurable?
- Where should config live?
- Environment-specific configs?

**Script Organization:**

- Flat vs subdirectories?
- Naming conventions?
- Shared utilities approach?
- Language choice (Python vs Bash vs mix)?

**Integration with Features:**

- How does inventory feed Skills Matrix?
- Should "Projects" become 8th core feature?
- Link to Daily Focus (project context)?
- GitHub activity integration?

---

## 🔗 Related Documents

- [Research Register](../research-register.md) - Week 4 research topic entry
- [Current State Inventory](../../exploration/current-state-inventory.md) - Generated output
- [Discovered Skills](../../exploration/discovered-skills.md) - Generated output
- [Scripts README](../../../scripts/inventory/README.md) - POC implementation docs

---

## 📊 POC Statistics

- **Total Execution Time:** ~5 minutes for full pipeline (excluding classification)
- **Interactive Classification Time:** ~15 minutes for 70 projects (user dependent)
- **Data Generated:** 110KB across 7 JSON/markdown files
- **Scripts Created:** 7 scripts (632 lines total across shell + Python)
- **Documentation Generated:** 2 markdown files (current-state-inventory, discovered-skills)

---

**Last Updated:** 2025-12-01  
**Status:** 🟡 POC Complete - Research Scheduled Week 4  
**Next:** Proceed with Week 2-3 HIGH priority research, return to this in Week 4





