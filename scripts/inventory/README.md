# Project Inventory Scripts

**Purpose:** Automated discovery and cataloging of repositories and projects  
**Created:** 2025-11-26  
**Last Updated:** 2025-12-07  
**Status:** 🟡 POC Complete - Repository Separation Planned (Week 4)

---

## Overview

These scripts automate the collection of project inventory data to inform the work productivity app design.

### What It Does:

1. **Fetches GitHub repos** for grimm00 user (personal)
2. **Scans local projects** in ~/Projects and ~/Learning  
3. **Analyzes tech stack** across all repos
4. **Interactive classification** to categorize projects
5. **Generates reports** for documentation

---

## Prerequisites

- `gh` CLI (GitHub CLI) - authenticated
- `git` - for local repo information
- Python 3.x - for analysis and classification scripts
- Access to ~/Projects and ~/Learning directories

---

## Scripts

### 1. `fetch-github-repos.sh`

Fetches all repositories for grimm00 user from GitHub.

**Usage:**
```bash
./fetch-github-repos.sh
```

**Output:** `data/github-repos.json`

**What it collects:**
- Repository name, description, URL
- Created/updated/last pushed dates
- Private/public status, fork status
- Primary language and full language breakdown
- Stars, forks count

---

### 2. `scan-local-projects.sh`

Scans local directories for Git repositories and projects.

**Usage:**
```bash
./scan-local-projects.sh
```

**Output:** `data/local-projects.json`

**What it collects:**
- Project path and name
- Git repository status (yes/no)
- Remote URL (if exists)
- Last commit date
- Directory size, file count
- Languages detected (by file extension)

---

### 3. `analyze-tech-stack.py`

Analyzes languages and technologies across all repositories.

**Usage:**
```bash
python3 analyze-tech-stack.py
```

**Inputs:**
- `data/github-repos.json`
- `data/local-projects.json`

**Output:** `data/tech-stack.json`

**Generates:**
- Language usage statistics
- Most used languages
- Languages per project
- Percentage breakdown

---

### 4. `classify-projects.py`

Interactive script to classify projects by category.

**Usage:**
```bash
python3 classify-projects.py
```

**Inputs:**
- `data/github-repos.json`
- `data/local-projects.json`
- `data/tech-stack.json`

**Output:** `data/classifications.json`

**Categories:**
- Work (DRW)
- Apprenti
- Personal
- Learning
- Inactive/Archived

**Features:**
- Shows context for each project
- Bulk operations (e.g., mark all in ~/Learning as "Learning")
- Save progress and resume later

---

### 5. `deduplicate-projects.py`

Merges GitHub and local projects when they reference the same repository.

**Usage:**
```bash
python3 deduplicate-projects.py
```

**Inputs:**
- `data/github-repos.json`
- `data/local-projects.json`
- `data/classifications.json`

**Output:**
- `data/classifications-merged.json` - Deduplicated classifications
- Updates `data/classifications.json` with merged entries

**What it does:**
- Matches local Git repos to GitHub repos by remote URL
- Resolves classification conflicts (prefers local classifications)
- Reduces project count by eliminating duplicates
- Creates merged project IDs for unified tracking

---

### 6. `generate-report-deduplicated.py` ⭐

Generates final deduplicated inventory and skills documents.

**Usage:**
```bash
python3 generate-report-deduplicated.py
```

**Inputs:**
- `data/github-repos.json`
- `data/local-projects.json`
- `data/tech-stack.json`
- `data/classifications.json`

**Outputs:**
- `data/generated-inventory-dedup.md` - Working copy
- `../../docs/maintainers/exploration/current-state-inventory.md` - Final inventory
- `../../docs/maintainers/exploration/discovered-skills.md` - Skills list

**Features:**
- Merges GitHub + Local projects into single entries (marked with 🔗)
- Shows GitHub-only projects (marked with ☁️)
- Shows local-only projects (marked with 💻)
- Displays both GitHub push dates and local commit dates
- Groups projects by classification
- Generates comprehensive tech stack summary

---

### 7. `generate-report.py` (Legacy)

Original report generator (does NOT deduplicate).

**Note:** Use `generate-report-deduplicated.py` instead for cleaner reports without duplicates.

---

## Quick Start

Run all scripts in order:

```bash
cd scripts/inventory

# 1. Fetch GitHub repos
./fetch-github-repos.sh

# 2. Scan local projects
./scan-local-projects.sh

# 3. Analyze tech stack
python3 analyze-tech-stack.py

# 4. Deduplicate projects
python3 deduplicate-projects.py

# 5. Classify projects (interactive - run in your terminal)
python3 classify-projects.py

# 6. Generate final deduplicated reports
python3 generate-report-deduplicated.py
```

**Note:** Steps 1-4 can be run through automation tools, but step 5 (classification) must be run interactively in your terminal since it requires user input.

---

## Data Files (Gitignored)

All output files are saved to `data/` which is gitignored:

- `github-repos.json` - GitHub repository data
- `local-projects.json` - Local project data
- `tech-stack.json` - Language statistics
- `classifications.json` - User project classifications (deduplicated)
- `classifications-merged.json` - Backup of merged classifications
- `generated-inventory.md` - Legacy inventory (with duplicates)
- `generated-inventory-dedup.md` - Deduplicated inventory (recommended)

---

## Integration with App

### Skills Matrix Feature

The discovered technologies can seed the Skills Matrix:
- Languages extracted from all projects
- Usage frequency suggests confidence level
- Last used date tracked per language
- Projects using each skill documented

### Projects Feature (Potential 8th Feature)

Data informs whether "Projects" should be a core feature:
- Number of active/inactive projects
- Context switching frequency
- Organization challenges
- GitHub integration opportunities

---

## Future Enhancements

- **Track changes over time** - Run monthly to see trends
- **GitHub activity metrics** - Commits, PRs, issues
- **Contribution graphs** - Visualize activity
- **Project health scores** - Identify abandoned projects
- **Technology learning paths** - Suggest skills to learn next

---

## Troubleshooting

### `gh: command not found`
Install GitHub CLI: `brew install gh` (macOS)

### `gh` not authenticated
Run: `gh auth login`

### Permission denied on local directories
Check that ~/Projects and ~/Learning exist and are accessible

### Python module not found
Install required modules: `pip3 install [module-name]`

---

## 🔄 Repository Separation Plan

**Decision:** ✅ Separate Repository Recommended  
**Timeline:** Week 4 (December 2025)  
**Rationale:** See [Inventory POC Repository Placement Reflection](../../docs/maintainers/planning/notes/reflections/reflection-inventory-poc-repository-placement-2025-12-07.md)

### Why Separate?

**Initial Context:**
- Inventory was one-time POC during exploration phase (Dec 1, 2025)
- Generated seed data for Projects API (59 projects, 24 languages)
- Projects API + CLI solved immediate need for project management

**Future Need:**
- **Project explosion anticipated** - Significant growth in project count expected
- **Periodic refresh required** - Ongoing discovery and sync will be necessary
- **Automation needed** - Manual discovery won't scale with project growth
- **Integration opportunity** - Inventory can sync discovered projects to Projects API

**Separation Benefits:**
- Clear separation of concerns (discovery tool vs production app)
- Independent evolution without affecting main repo
- Reusability for others
- Cleaner main repo focused on production code
- Technical debt isolation

### Mapping Script Placement

**Current:** `scripts/map_inventory_to_projects.py` (in main repo)  
**Decision:** Keep in main repo initially (used for import into Projects API)  
**Future:** Revisit after Week 4 research and repository separation

### Timeline

**Phase 1 (Now):**
- ✅ Document separation plan (this document)
- ✅ Update main repo documentation
- ✅ Add to Week 4 research plan

**Phase 2 (Week 4):**
- Create separate repository
- Move inventory scripts to new repo
- Update references and documentation
- Address technical debt (7 known issues)

**Phase 3 (Week 4+):**
- Enhance inventory system with periodic refresh
- Add Projects API integration for automatic import
- Implement continuous sync capability

### Related Documentation

- **[Reflection Document](../../docs/maintainers/planning/notes/reflections/reflection-inventory-poc-repository-placement-2025-12-07.md)** - Complete analysis and decision rationale
- **[POC Analysis](../../docs/maintainers/research/automation/inventory-system-poc-analysis.md)** - Technical debt and research questions
- **[Research Register](../../docs/maintainers/research/research-register.md)** - Week 4 research topic entry

---

**Last Updated:** 2025-12-07  
**Status:** 🟡 POC Complete - Repository Separation Planned (Week 4)


