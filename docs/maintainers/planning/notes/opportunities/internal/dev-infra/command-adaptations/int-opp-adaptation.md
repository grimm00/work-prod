# Command Adaptation: int-opp for Dev-Infra

**Source Command:** `/int-opp` from work-prod  
**Target:** Dev-infra template  
**Status:** ✅ Complete  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Overview

The `/int-opp` command captures learnings from projects to improve dev-infra template and other projects. This adaptation makes it generic and reusable for any project, not just work-prod.

**Key Adaptation:** Support project-specific opportunities with automatic project discovery and command adaptation workflow.

---

## 🎯 Original Command

**Command:** `/int-opp`  
**Purpose:** Capture learnings from work-prod for dev-infra template  
**Location:** `.cursor/commands/int-opp.md` (work-prod)

**Key Features:**
- Phase learnings capture
- Dev-infra improvements documentation
- Work-prod specific paths and assumptions

---

## 🔄 Adaptations Needed

### 1. Project-Specific Support

**Change:** Support any project, not just work-prod  
**Reason:** Dev-infra should work with any project  
**Impact:** Makes command reusable across projects

**Original:**
- Hardcoded `work-prod` paths
- Assumes work-prod project structure
- Only supports work-prod → dev-infra flow

**Adapted:**
- Configurable project name parameter
- Project discovery (`--new-project` flag)
- Support for multiple projects

**Files to modify:**
- `.cursor/commands/int-opp.md` - Update command documentation
- Add project discovery logic
- Support project-specific directory structure

---

### 2. Project Discovery

**Change:** Add `--new-project` flag with automatic discovery  
**Reason:** Enable creating opportunities for new projects automatically  
**Impact:** Reduces manual setup for new projects

**Original:**
- No project discovery
- Manual directory creation
- No project information gathering

**Adapted:**
- Search Projects API for project info
- Search GitHub for repository info
- Search local filesystem for project paths
- Ask for clarification if ambiguous

**Implementation:**
```bash
# Search Projects API
./proj list --search "[project-name]"

# Search GitHub
gh repo list --search "[project-name]"

# Search local filesystem
find ~/Projects ~/Learning -type d -name "*[project-name]*"
```

**Files to modify:**
- `.cursor/commands/int-opp.md` - Add discovery workflow
- Document discovery process
- Add clarification prompts

---

### 3. Command Adaptation Workflow

**Change:** Add `--command-adaptation` flag for dev-infra  
**Reason:** Document how to adapt work-prod commands for dev-infra  
**Impact:** Enables systematic command porting

**Original:**
- No command adaptation workflow
- No documentation for adapting commands
- Commands assumed to be work-prod specific

**Adapted:**
- `--command-adaptation` flag for dev-infra
- Command adaptation template
- Adaptation documentation structure

**Implementation:**
```bash
/int-opp dev-infra --command-adaptation
```

**Files to modify:**
- `.cursor/commands/int-opp.md` - Add command adaptation workflow
- Create `command-adaptations/` directory structure
- Document adaptation process

---

### 4. Directory Structure Changes

**Change:** Support project-specific directory structure  
**Reason:** Enable opportunities for any project  
**Impact:** Makes command truly generic

**Original Structure:**
```
internal/
├── work-prod/
│   ├── phase-*-learnings.md
└── dev-infra/
    └── dev-infra-improvements*.md
```

**Adapted Structure:**
```
internal/
├── [project-name]/
│   ├── README.md                    # Project hub
│   ├── learnings/                   # Learnings from project
│   │   ├── README.md
│   │   └── [topic]-learnings.md
│   └── improvements/                # Improvements for dev-infra/others
│       ├── README.md
│       └── [topic]-improvements.md
├── dev-infra/
│   ├── command-adaptations/         # NEW: Command adaptations
│   │   ├── README.md
│   │   └── [command]-adaptation.md
│   └── dev-infra-improvements*.md
└── work-prod/
    └── phase-*-learnings.md
```

**Files to modify:**
- `.cursor/commands/int-opp.md` - Update directory structure documentation
- Update templates to support project-specific paths
- Add project hub creation logic

---

## 📝 Implementation Steps

### Step 1: Update Command Documentation

- [ ] Add `--new-project` flag documentation
- [ ] Add `--command-adaptation` flag documentation
- [ ] Update usage examples
- [ ] Add project discovery workflow

### Step 2: Add Project Discovery Logic

- [ ] Implement Projects API search
- [ ] Implement GitHub search
- [ ] Implement filesystem search
- [ ] Add clarification prompts

### Step 3: Create Project Directory Structure

- [ ] Create project hub template
- [ ] Create learnings directory template
- [ ] Create improvements directory template
- [ ] Update main internal hub

### Step 4: Add Command Adaptation Workflow

- [ ] Create command-adaptations directory structure
- [ ] Create command adaptation template
- [ ] Document adaptation process
- [ ] Update dev-infra hub

---

## ✅ Definition of Done

- [ ] Command supports project-specific opportunities
- [ ] `--new-project` flag works with discovery
- [ ] `--command-adaptation` flag works for dev-infra
- [ ] Directory structure supports multiple projects
- [ ] Project discovery implemented
- [ ] Command adaptation workflow documented
- [ ] Ready for use in dev-infra

---

## 📚 Examples

### Example 1: Create New Project Directory

```bash
/int-opp inventory-tools --new-project
```

**Process:**
1. Search for inventory-tools project
2. Discover project information
3. Create project directory structure
4. Create project hub with information

### Example 2: Document Command Adaptation

```bash
/int-opp dev-infra --command-adaptation
```

**Process:**
1. Identify commands to adapt
2. Create adaptation documents
3. Document changes needed
4. Update dev-infra hub

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Complete  
**Next:** Apply adaptations to dev-infra template

