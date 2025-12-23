# Command Adaptation: reflect for Dev-Infra

**Source Command:** `/reflect` from work-prod  
**Target:** Dev-infra template  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Overview

The `/reflect` command analyzes project state, recent work, and patterns to provide actionable suggestions. This adaptation makes it generic for any project using the dev-infra template.

**Key Adaptation:** Remove work-prod-specific paths and assumptions, make reflection scope configurable.

---

## 🎯 Original Command

**Command:** `/reflect`  
**Purpose:** Analyze project state and provide actionable suggestions  
**Location:** `.cursor/commands/reflect.md` (work-prod)

**Key Features:**
- Analyzes recent commits and PRs
- Reviews current phase status
- Identifies patterns and opportunities
- Provides actionable suggestions
- References phase learnings

---

## 🔄 Adaptations Needed

### 1. Generic Phase/Feature Paths

**Change:** Replace work-prod-specific phase paths with generic feature paths  
**Reason:** Dev-infra projects may have different feature structures  
**Impact:** Makes reflection work for any project structure

**Original:**
```markdown
- Read `docs/maintainers/planning/features/projects/status-and-next-steps.md`
- Check latest phase learnings document
```

**Adapted:**
```markdown
- Read `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
- Check latest phase learnings document (if exists)
- Support multiple feature structures
```

**Files to modify:**
- `.cursor/commands/reflect.md` - Update path references
- Make feature name configurable or auto-detect

---

### 2. Configurable Reflection Scope

**Change:** Support project-specific reflection scopes  
**Reason:** Different projects have different structures (features, releases, etc.)  
**Impact:** Reflection adapts to project structure

**Original:**
- Assumes `features/projects/` structure
- Assumes phase-based development
- Assumes specific learning document locations

**Adapted:**
- Support `features/[feature-name]/` or `releases/[version]/` structures
- Support phase-based or milestone-based development
- Auto-detect project structure

**Files to modify:**
- `.cursor/commands/reflect.md` - Add structure detection
- Support multiple project patterns

---

### 3. Generic Learnings References

**Change:** Make learnings document paths configurable  
**Reason:** Projects may organize learnings differently  
**Impact:** Reflection can reference learnings regardless of structure

**Original:**
```markdown
- Check latest phase learnings document
- Review dev-infra improvements
```

**Adapted:**
```markdown
- Check learnings documents (auto-detect location)
- Review improvement documents (if exists)
- Support optional learnings structure
```

**Files to modify:**
- `.cursor/commands/reflect.md` - Make learnings optional
- Auto-detect learnings location

---

### 4. Project-Agnostic Suggestions

**Change:** Remove work-prod-specific suggestion patterns  
**Reason:** Different projects have different needs  
**Impact:** Suggestions adapt to project context

**Original:**
- Assumes Projects feature
- Assumes specific workflow patterns
- Assumes fix management system

**Adapted:**
- Detect project features from structure
- Adapt suggestions to project context
- Support optional workflows (fix management, etc.)

**Files to modify:**
- `.cursor/commands/reflect.md` - Make suggestions contextual
- Detect available workflows

---

## 📝 Implementation Steps

### Step 1: Update Path References

- [ ] Replace hardcoded `features/projects/` with `features/[feature-name]/`
- [ ] Add feature detection logic
- [ ] Support multiple feature structures

### Step 2: Make Reflection Scope Configurable

- [ ] Add structure detection
- [ ] Support phase-based and milestone-based projects
- [ ] Auto-detect project patterns

### Step 3: Update Learnings References

- [ ] Make learnings optional
- [ ] Auto-detect learnings location
- [ ] Support projects without learnings structure

### Step 4: Contextualize Suggestions

- [ ] Detect project features from structure
- [ ] Adapt suggestions to project context
- [ ] Support optional workflows

---

## ✅ Definition of Done

- [ ] Command works for any dev-infra project
- [ ] Paths are configurable/generic
- [ ] Reflection scope adapts to project structure
- [ ] Learnings references are optional
- [ ] Suggestions are contextual
- [ ] Documentation updated
- [ ] Ready for use in dev-infra

---

**Last Updated:** 2025-12-07  
**Status:** 🔴 Not Started  
**Next:** Apply adaptations to dev-infra template

