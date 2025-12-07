# Command Adaptation: fix-plan for Dev-Infra

**Source Command:** `/fix-plan` from work-prod  
**Target:** Dev-infra template  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Overview

The `/fix-plan` command analyzes Sourcery reviews and creates fix batches. This adaptation makes it generic for any project using the dev-infra template.

**Key Adaptation:** Make fix tracking paths configurable and support different project structures.

---

## 🎯 Original Command

**Command:** `/fix-plan`  
**Purpose:** Batch deferred issues from PR reviews into implementable fix plans  
**Location:** `.cursor/commands/fix-plan.md` (work-prod)

**Key Features:**
- Parses Sourcery review files
- Batches issues by priority and effort
- Creates fix plan documents
- Supports cross-PR batches
- Updates fix tracking hubs

---

## 🔄 Adaptations Needed

### 1. Generic Fix Tracking Paths

**Change:** Replace work-prod-specific fix paths with configurable paths  
**Reason:** Projects may organize fixes differently  
**Impact:** Fix planning works for any project structure

**Original:**
```markdown
Location: `docs/maintainers/planning/features/projects/fix/pr##/`
Review file: `docs/maintainers/feedback/sourcery/pr##.md`
```

**Adapted:**
```markdown
Location: `docs/maintainers/planning/features/[feature-name]/fix/pr##/`
Review file: `docs/maintainers/feedback/sourcery/pr##.md`
Support: Auto-detect feature name or use default
```

**Files to modify:**
- `.cursor/commands/fix-plan.md` - Update path references
- Add feature detection or configuration

---

### 2. Configurable Feature Context

**Change:** Support fix planning for any feature or project-wide  
**Reason:** Projects may have multiple features or no feature structure  
**Impact:** Fix planning adapts to project organization

**Original:**
- Assumes `features/projects/` structure
- Fixes are feature-specific

**Adapted:**
- Support `features/[feature-name]/fix/` structure
- Support project-wide fixes: `docs/maintainers/planning/fix/`
- Auto-detect or allow configuration

**Files to modify:**
- `.cursor/commands/fix-plan.md` - Add structure detection
- Support multiple fix organization patterns

---

### 3. Generic Batch Naming

**Change:** Make batch naming configurable  
**Reason:** Projects may prefer different naming conventions  
**Impact:** Batch names adapt to project preferences

**Original:**
```markdown
Format: `pr##-batch-[priority]-[effort]-[batch-number]`
```

**Adapted:**
```markdown
Format: Configurable (default: `pr##-batch-[priority]-[effort]-[batch-number]`)
Support: Custom naming patterns via config
```

**Files to modify:**
- `.cursor/commands/fix-plan.md` - Make naming configurable
- Add configuration support

---

### 4. Optional Fix Management

**Change:** Make fix management optional  
**Reason:** Not all projects use fix management workflow  
**Impact:** Command works even without fix structure

**Original:**
- Assumes fix tracking exists
- Assumes fix hubs exist

**Adapted:**
- Create fix structure if needed
- Support projects without fix management
- Make fix tracking optional

**Files to modify:**
- `.cursor/commands/fix-plan.md` - Add structure creation
- Support optional fix management

---

## 📝 Implementation Steps

### Step 1: Update Path References

- [ ] Replace hardcoded `features/projects/fix/` with configurable path
- [ ] Add feature detection or configuration
- [ ] Support project-wide fixes

### Step 2: Add Structure Detection

- [ ] Detect feature structure
- [ ] Support multiple fix organization patterns
- [ ] Auto-create fix structure if needed

### Step 3: Make Batch Naming Configurable

- [ ] Add configuration for batch naming
- [ ] Support custom naming patterns
- [ ] Default to work-prod pattern

### Step 4: Support Optional Fix Management

- [ ] Make fix tracking optional
- [ ] Create structure if needed
- [ ] Support projects without fix management

---

## ✅ Definition of Done

- [ ] Command works for any dev-infra project
- [ ] Paths are configurable/generic
- [ ] Feature context is auto-detected or configurable
- [ ] Batch naming is configurable
- [ ] Fix management is optional
- [ ] Documentation updated
- [ ] Ready for use in dev-infra

---

**Last Updated:** 2025-12-07  
**Status:** 🔴 Not Started  
**Next:** Apply adaptations to dev-infra template

