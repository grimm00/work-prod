# Project Inventory Scripts

**Purpose:** Automated discovery and cataloging of repositories and projects  
**Created:** 2025-11-26  
**Last Updated:** 2025-11-26

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

###3. `analyze-tech-stack.py`

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

### 5. `generate-report.py`

Generates filled inventory document from collected data.

**Usage:**
```bash
python3 generate-report.py
```

**Inputs:**
- `data/github-repos.json`
- `data/local-projects.json`
- `data/tech-stack.json`
- `data/classifications.json`

**Outputs:**
- `data/generated-inventory.md` - Filled inventory
- `../../docs/maintainers/exploration/discovered-skills.md` - Skills list

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

# 4. Classify projects (interactive)
python3 classify-projects.py

# 5. Generate reports
python3 generate-report.py
```

---

## Data Files (Gitignored)

All output files are saved to `data/` which is gitignored:

- `github-repos.json` - GitHub repository data
- `local-projects.json` - Local project data
- `tech-stack.json` - Language statistics
- `classifications.json` - User project classifications
- `generated-inventory.md` - Final inventory report

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

**Last Updated:** 2025-11-26  
**Status:** ✅ Scripts ready to use

