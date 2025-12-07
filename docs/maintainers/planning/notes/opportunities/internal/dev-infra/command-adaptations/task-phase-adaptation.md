# Command Adaptation: task-phase for Dev-Infra

**Source Command:** `/task-phase` from work-prod  
**Target:** Dev-infra template  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Overview

The `/task-phase` command implements phase tasks following TDD workflow. This adaptation makes it generic for any project using the dev-infra template.

**Key Adaptation:** Support different phase structures and task organization patterns.

---

## 🎯 Original Command

**Command:** `/task-phase`  
**Purpose:** Implement phase tasks step-by-step following TDD workflow  
**Location:** `.cursor/commands/task-phase.md` (work-prod)

**Key Features:**
- Reads phase documents
- Implements tasks following TDD (RED → GREEN → REFACTOR)
- Groups related tasks
- Creates feature branches
- Commits work incrementally

---

## 🔄 Adaptations Needed

### 1. Generic Phase Paths

**Change:** Replace work-prod-specific phase paths with configurable paths  
**Reason:** Projects may organize phases differently  
**Impact:** Task implementation works for any project structure

**Original:**
```markdown
Read: `docs/maintainers/planning/features/projects/phase-N.md`
```

**Adapted:**
```markdown
Read: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
Support: Auto-detect feature name or use default
Support: Alternative phase structures (milestones, sprints, etc.)
```

**Files to modify:**
- `.cursor/commands/task-phase.md` - Update path references
- Add feature detection or configuration

---

### 2. Flexible Phase Structures

**Change:** Support different phase organization patterns  
**Reason:** Projects may use milestones, sprints, or other structures  
**Impact:** Task implementation adapts to project organization

**Original:**
- Assumes phase-based structure
- Assumes numbered phases

**Adapted:**
- Support phase-based, milestone-based, sprint-based structures
- Support named phases or numbered phases
- Auto-detect phase structure

**Files to modify:**
- `.cursor/commands/task-phase.md` - Add structure detection
- Support multiple phase patterns

---

### 3. Configurable Task Grouping

**Change:** Make task grouping rules configurable  
**Reason:** Different projects may group tasks differently  
**Impact:** Task grouping adapts to project preferences

**Original:**
- Hardcoded grouping rules (RED+GREEN together)
- Assumes specific task types

**Adapted:**
- Configurable grouping rules
- Support custom task types
- Auto-detect task relationships

**Files to modify:**
- `.cursor/commands/task-phase.md` - Make grouping configurable
- Add task type detection

---

### 4. Generic Branch Naming

**Change:** Make branch naming configurable  
**Reason:** Projects may prefer different branch naming conventions  
**Impact:** Branch names adapt to project preferences

**Original:**
```markdown
Format: `feat/phase-N-[description]`
```

**Adapted:**
```markdown
Format: Configurable (default: `feat/phase-N-[description]`)
Support: Custom naming patterns via config
Support: Feature-based branches: `feat/[feature]/phase-N-[description]`
```

**Files to modify:**
- `.cursor/commands/task-phase.md` - Make naming configurable
- Add configuration support

---

## 📝 Implementation Steps

### Step 1: Update Path References

- [ ] Replace hardcoded `features/projects/` with configurable path
- [ ] Add feature detection or configuration
- [ ] Support alternative phase structures

### Step 2: Add Structure Detection

- [ ] Detect phase structure (phases, milestones, sprints)
- [ ] Support multiple phase patterns
- [ ] Auto-detect phase organization

### Step 3: Make Task Grouping Configurable

- [ ] Add configuration for task grouping
- [ ] Support custom task types
- [ ] Auto-detect task relationships

### Step 4: Make Branch Naming Configurable

- [ ] Add configuration for branch naming
- [ ] Support custom naming patterns
- [ ] Default to work-prod pattern

---

## ✅ Definition of Done

- [ ] Command works for any dev-infra project
- [ ] Paths are configurable/generic
- [ ] Phase structures are flexible
- [ ] Task grouping is configurable
- [ ] Branch naming is configurable
- [ ] Documentation updated
- [ ] Ready for use in dev-infra

---

**Last Updated:** 2025-12-07  
**Status:** 🔴 Not Started  
**Next:** Apply adaptations to dev-infra template

