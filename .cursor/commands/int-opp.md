# Document Internal Opportunities

Capture learnings from work-prod (or any project) to improve dev-infra template and other projects.

---

## Workflow Overview

**When to use:**

- After completing a phase or significant work
- To capture learnings for improving dev-infra template
- To create project-specific opportunity directories
- To document command adaptations for dev-infra

**Key principle:** Capture learnings while fresh, organize by project, and create actionable improvement checklists.

---

## Usage

**Command:** `/int-opp [project-name] [options]`

**Examples:**

- `/int-opp` - Capture learnings for work-prod (default)
- `/int-opp work-prod` - Explicitly specify work-prod
- `/int-opp dev-infra` - Create opportunities directory for dev-infra
- `/int-opp inventory-tools --new-project` - Create new project directory and discover project info
- `/int-opp dev-infra --command-adaptation` - Document command adaptations for dev-infra
- `/int-opp [project] --phase N` - Capture phase-specific learnings

**Options:**

- `--new-project` - Create directory for new project and discover project information
- `--command-adaptation` - Document command adaptations for dev-infra (use with dev-infra project)
- `--phase N` - Capture learnings for specific phase
- `--type TYPE` - Type of opportunity (`learnings`, `improvements`, `command-adaptation`)
- `--dry-run` - Show what would be created without creating files

---

## Step-by-Step Process

### 1. Identify Project

**Default behavior:**

- If no project specified, use `work-prod` (current project)
- Check if project directory exists in `docs/maintainers/planning/notes/opportunities/internal/[project]/`

**New project discovery (`--new-project`):**

1. **Check if directory exists:**
   - Look for `docs/maintainers/planning/notes/opportunities/internal/[project]/`
   - If exists, project is known

2. **Search for project information:**
   - Check Projects API: `./proj list --search "[project-name]"`
   - Check GitHub: Search for repository with project name
   - Check local filesystem: Look for project directories in `~/Projects/` or `~/Learning/`
   - Check if project is mentioned in documentation

3. **Gather project context:**
   - Project type (application, tool, library, template)
   - Technology stack (if known)
   - Purpose/description
   - Current status

4. **Ask for clarification (if needed):**
   - If project info is ambiguous or missing
   - Request: project description, type, purpose
   - Confirm project name and directory structure

**Checklist:**

- [ ] Project identified (or using default)
- [ ] Project directory checked/created
- [ ] Project information gathered (if new project)
- [ ] Clarification obtained (if needed)

---

### 2. Create Project Directory Structure (if new project)

**If `--new-project` specified and directory doesn't exist:**

**Directory structure:**

```
docs/maintainers/planning/notes/opportunities/internal/[project-name]/
├── README.md                    # Project hub
├── learnings/                   # Learnings from this project
│   ├── README.md                # Learnings hub
│   └── [topic]-learnings.md    # Specific learnings documents
└── improvements/                # Improvements for dev-infra/other projects
    ├── README.md                # Improvements hub
    └── [topic]-improvements.md  # Specific improvement documents
```

**Create project hub:**

**File:** `docs/maintainers/planning/notes/opportunities/internal/[project-name]/README.md`

```markdown
# [Project Name] Opportunities

**Purpose:** [Project description]  
**Type:** [Application/Tool/Library/Template]  
**Status:** ✅ Active  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Learnings

- **[Learnings Hub](learnings/README.md)** - Learnings from [project name]

### Improvements

- **[Improvements Hub](improvements/README.md)** - Improvements for dev-infra/other projects

---

## 🎯 Overview

[Project description and purpose]

**Project Context:**

- **Type:** [Application/Tool/Library/Template]
- **Technology Stack:** [If known]
- **Purpose:** [What this project does]
- **Status:** [Current status]

---

## 📊 Summary

**Learnings Documents:** [N]  
**Improvement Documents:** [M]  
**Status:** ✅ Active

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Project directory created (if new project)
- [ ] Project hub README created
- [ ] Learnings directory and hub created
- [ ] Improvements directory and hub created
- [ ] Project information documented

---

### 3. Determine Opportunity Type

**Types:**

1. **Learnings** (default for work-prod):
   - What worked well
   - What needs improvement
   - Unexpected discoveries
   - Time investment analysis

2. **Improvements** (for dev-infra):
   - Actionable checklists
   - Template updates needed
   - Pattern documentation

3. **Command Adaptation** (for dev-infra):
   - How to adapt work-prod commands for dev-infra
   - Command modifications needed
   - Workflow adaptations

**Auto-detection:**

- If project is `dev-infra` and `--command-adaptation` → Command Adaptation
- If project is `dev-infra` → Improvements
- If project is `work-prod` → Learnings
- Otherwise → Ask user or default to Learnings

**Checklist:**

- [ ] Opportunity type determined
- [ ] Type is appropriate for project
- [ ] Type matches user intent

---

### 4. Create Opportunity Documents

#### For Learnings (Default)

**Location:** `docs/maintainers/planning/notes/opportunities/internal/[project]/learnings/`

**File naming:**

- Format: `[topic]-learnings.md` (e.g., `phase-N-learnings.md`, `fix-management-learnings.md`)
- Or: `[project]-learnings-[date].md` for general learnings

#### For Improvements (Dev-Infra)

**Location:** `docs/maintainers/planning/notes/opportunities/internal/[project]/improvements/`

**File naming:**

- Format: `[project]-improvements-[topic].md` (e.g., `dev-infra-improvements-phaseN.md`)

#### For Command Adaptation (Dev-Infra)

**Location:** `docs/maintainers/planning/notes/opportunities/internal/dev-infra/command-adaptations/`

**File naming:**

- Format: `[command-name]-adaptation.md` (e.g., `int-opp-adaptation.md`, `reflect-adaptation.md`)

---

### 5. Update Project Hubs

**Update project hub:**

- Add new document to Quick Links
- Update summary statistics
- Update "Last Updated" date

**Update learnings/improvements hub:**

- Add document link
- Update summary
- Update "Last Updated" date

**Checklist:**

- [ ] Project hub updated
- [ ] Learnings/improvements hub updated
- [ ] Quick links added
- [ ] Summary statistics updated

---

### 6. Update Main Internal Opportunities Hub

**File:** `docs/maintainers/planning/notes/opportunities/internal/README.md`

**Add project entry:**

```markdown
### [Project Name] Opportunities

- **[Project Hub]([project-name]/README.md)** - [Project description]
  - Learnings: [N] documents
  - Improvements: [M] documents
```

**Checklist:**

- [ ] Main hub updated with project entry
- [ ] Completion tracking updated
- [ ] Quick links updated
- [ ] "Last Updated" date updated

---

## Common Scenarios

### Scenario 1: Capture Phase Learnings (work-prod)

**Command:** `/int-opp work-prod --phase 8`

**Process:**

1. Identify work-prod project (default)
2. Create phase learnings document
3. Use phase learnings template
4. Update work-prod hub

---

### Scenario 2: Create New Project Directory

**Command:** `/int-opp inventory-tools --new-project`

**Process:**

1. Search for inventory-tools project
2. Gather project information
3. Ask for clarification if needed
4. Create project directory structure
5. Create project hub with information

---

### Scenario 3: Document Command Adaptation

**Command:** `/int-opp dev-infra --command-adaptation`

**Process:**

1. Identify commands to adapt
2. Analyze each command
3. Create adaptation documents
4. Update dev-infra hub

---

## Tips

### For New Projects

- Search thoroughly before asking user
- Gather as much information as possible automatically
- Only ask for clarification when information is ambiguous
- Document project context clearly in hub

### For Command Adaptations

- Focus on making commands generic/reusable
- Document project-specific assumptions
- Provide clear examples
- Think about how dev-infra will use the command

### For Learnings

- Capture while fresh (right after phase/work)
- Be specific with examples
- Focus on actionable items
- Think about template implications

---

## Reference

**Project Directories:**

- `docs/maintainers/planning/notes/opportunities/internal/[project-name]/`

**Command Files:**

- `.cursor/commands/[command-name].md`

**Related Commands:**

- `/reflect` - Create reflection documents
- `/transition-plan` - Create transition plans
- `/fix-plan` - Create fix plans
- `/cursor-rules` - Manage Cursor rules files

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active  
**Next:** Use to capture learnings, create project directories, or document command adaptations

--- End Command ---
