# Command Adaptation: transition-plan for Dev-Infra

**Source Command:** `/transition-plan` from work-prod  
**Target:** Dev-infra template  
**Status:** 🔴 Not Started  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Overview

The `/transition-plan` command creates transition planning documents from reflection artifacts. This adaptation makes it generic for any project using the dev-infra template.

**Key Adaptation:** Support different transition types and project structures.

---

## 🎯 Original Command

**Command:** `/transition-plan`  
**Purpose:** Create transition plans from reflection artifacts  
**Location:** `.cursor/commands/transition-plan.md` (work-prod)

**Key Features:**
- Creates plans from reflection artifacts
- Supports multiple transition types (feature, release, infrastructure)
- Generates transition planning documents
- Follows established planning patterns

---

## 🔄 Adaptations Needed

### 1. Generic Planning Paths

**Change:** Replace work-prod-specific planning paths with configurable paths  
**Reason:** Projects may organize planning differently  
**Impact:** Transition planning works for any project structure

**Original:**
```markdown
- `docs/maintainers/planning/releases/v*/checklist.md`
- `docs/maintainers/planning/features/*/feature-plan.md`
```

**Adapted:**
```markdown
- `docs/maintainers/planning/releases/[version]/checklist.md`
- `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
- Support custom planning structures
```

**Files to modify:**
- `.cursor/commands/transition-plan.md` - Update path references
- Add structure detection

---

### 2. Configurable Transition Types

**Change:** Support project-specific transition types  
**Reason:** Different projects have different transition needs  
**Impact:** Transition planning adapts to project context

**Original:**
- Assumes specific transition types (feature, release, infrastructure)
- Hardcoded transition patterns

**Adapted:**
- Support custom transition types
- Auto-detect transition type from context
- Configurable transition patterns

**Files to modify:**
- `.cursor/commands/transition-plan.md` - Add transition type detection
- Support custom types

---

### 3. Generic Artifact Detection

**Change:** Make artifact detection configurable  
**Reason:** Projects may organize artifacts differently  
**Impact:** Transition planning finds artifacts regardless of structure

**Original:**
- Assumes specific artifact locations
- Hardcoded artifact patterns

**Adapted:**
- Auto-detect artifact locations
- Support custom artifact structures
- Configurable artifact patterns

**Files to modify:**
- `.cursor/commands/transition-plan.md` - Add artifact detection
- Support custom structures

---

### 4. Project-Agnostic Templates

**Change:** Make transition plan templates generic  
**Reason:** Different projects need different plan structures  
**Impact:** Transition plans adapt to project needs

**Original:**
- Work-prod specific plan templates
- Assumes specific planning patterns

**Adapted:**
- Generic plan templates
- Configurable plan structure
- Support custom templates

**Files to modify:**
- `.cursor/commands/transition-plan.md` - Update templates
- Add template configuration

---

## 📝 Implementation Steps

### Step 1: Update Path References

- [ ] Replace hardcoded planning paths with configurable paths
- [ ] Add structure detection
- [ ] Support custom planning structures

### Step 2: Add Transition Type Detection

- [ ] Auto-detect transition type from context
- [ ] Support custom transition types
- [ ] Make transition patterns configurable

### Step 3: Improve Artifact Detection

- [ ] Auto-detect artifact locations
- [ ] Support custom artifact structures
- [ ] Add artifact pattern configuration

### Step 4: Genericize Templates

- [ ] Update plan templates to be generic
- [ ] Add template configuration
- [ ] Support custom templates

---

## ✅ Definition of Done

- [ ] Command works for any dev-infra project
- [ ] Paths are configurable/generic
- [ ] Transition types are auto-detected or configurable
- [ ] Artifact detection is flexible
- [ ] Templates are generic/configurable
- [ ] Documentation updated
- [ ] Ready for use in dev-infra

---

**Last Updated:** 2025-12-07  
**Status:** 🔴 Not Started  
**Next:** Apply adaptations to dev-infra template

