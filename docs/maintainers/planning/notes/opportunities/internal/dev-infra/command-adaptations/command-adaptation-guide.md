# Command Adaptation Guide

**Purpose:** General guide for adapting work-prod commands for dev-infra template  
**Status:** ✅ Active  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📋 Overview

This guide provides a systematic approach for adapting work-prod Cursor commands to work in the dev-infra template context. The goal is to make commands generic and reusable while preserving proven workflows.

---

## 🎯 Adaptation Principles

### 1. Make Generic

**Remove Project-Specific Assumptions:**
- Replace hardcoded project names with parameters
- Use configurable paths instead of fixed paths
- Support multiple project types

**Example:**
```markdown
# Before (work-prod specific)
Location: `docs/maintainers/planning/features/projects/`

# After (generic)
Location: `docs/maintainers/planning/features/[feature-name]/`
```

---

### 2. Preserve Patterns

**Keep Proven Workflows:**
- Maintain command structure and flow
- Preserve best practices
- Keep successful patterns

**Example:**
- TDD workflow (RED → GREEN → REFACTOR)
- Hub-and-spoke documentation pattern
- Phase-based development approach

---

### 3. Document Changes

**Clear Before/After:**
- Show original pattern
- Show adapted pattern
- Explain rationale

**Example:**
```markdown
**Original:**
[work-prod specific code]

**Adapted:**
[generic code]

**Reason:**
[Why this change is needed]
```

---

## 📝 Adaptation Checklist

### For Each Command:

- [ ] **Identify Project-Specific Elements**
  - [ ] Hardcoded project names
  - [ ] Fixed file paths
  - [ ] Project-specific assumptions
  - [ ] Work-prod specific workflows

- [ ] **Make Generic**
  - [ ] Replace hardcoded names with parameters
  - [ ] Use configurable paths
  - [ ] Support multiple project types
  - [ ] Remove work-prod assumptions

- [ ] **Preserve Patterns**
  - [ ] Keep proven workflows
  - [ ] Maintain command structure
  - [ ] Preserve best practices

- [ ] **Document Adaptations**
  - [ ] Create adaptation document
  - [ ] Show before/after examples
  - [ ] Explain rationale
  - [ ] Provide implementation steps

- [ ] **Update Templates**
  - [ ] Update command documentation
  - [ ] Update file templates
  - [ ] Update directory structures

---

## 🔄 Common Adaptations

### Path Adaptations

**Pattern:** Replace work-prod specific paths with generic patterns

**Examples:**

| Original (work-prod) | Adapted (generic) |
|---------------------|-------------------|
| `docs/maintainers/planning/features/projects/` | `docs/maintainers/planning/features/[feature-name]/` |
| `scripts/project_cli/` | `scripts/[cli-name]/` |
| `backend/app/models/project.py` | `backend/app/models/[model-name].py` |

---

### Project Name Adaptations

**Pattern:** Replace hardcoded "work-prod" with configurable project name

**Examples:**

| Original | Adapted |
|---------|---------|
| `work-prod` | `[project-name]` or `PROJECT_NAME` |
| `work-prod learnings` | `[project-name] learnings` |
| `work-prod improvements` | `[project-name] improvements` |

---

### Command Flag Adaptations

**Pattern:** Add flags for project-specific behavior

**Examples:**

| Original | Adapted |
|---------|---------|
| Assumes work-prod | `--project [name]` flag |
| Hardcoded paths | `--base-dir [path]` flag |
| Single project | `--new-project` flag for discovery |

---

## 📚 Command-Specific Adaptations

### `/int-opp` Command

**Key Adaptations:**
- ✅ Project-specific support (`--new-project`)
- ✅ Command adaptation workflow (`--command-adaptation`)
- ✅ Generic directory structure

**See:** [int-opp-adaptation.md](int-opp-adaptation.md)

---

### `/reflect` Command (Planned)

**Key Adaptations Needed:**
- Support any project scope
- Generic reflection templates
- Project-specific reflection paths

**Status:** 🟡 Planned

---

### `/fix-plan` Command (Planned)

**Key Adaptations Needed:**
- Generic fix tracking paths
- Project-agnostic PR structure
- Configurable batch naming

**Status:** 🟡 Planned

---

### `/transition-plan` Command (Planned)

**Key Adaptations Needed:**
- Generic transition types
- Project-agnostic planning paths
- Configurable artifact types

**Status:** 🟡 Planned

---

### `/task-phase` Command (Planned)

**Key Adaptations Needed:**
- Generic phase structure
- Project-agnostic task patterns
- Configurable TDD workflow

**Status:** 🟡 Planned

---

## 🚀 Implementation Workflow

### 1. Analyze Command

- Read command documentation
- Identify project-specific elements
- List adaptations needed

### 2. Create Adaptation Document

- Use command adaptation template
- Document all adaptations
- Provide before/after examples

### 3. Update Command

- Apply adaptations to command
- Update documentation
- Test with dev-infra context

### 4. Document in Dev-Infra

- Add adapted command to dev-infra
- Update dev-infra documentation
- Create usage examples

---

## 📝 Template: Command Adaptation Document

**File:** `[command-name]-adaptation.md`

```markdown
# Command Adaptation: [Command Name] for Dev-Infra

**Source Command:** `/[command-name]` from work-prod  
**Target:** Dev-infra template  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD

---

## 📋 Overview

[Description of command and adaptations needed]

---

## 🎯 Original Command

**Command:** `/[command-name]`  
**Purpose:** [Original purpose]  
**Location:** `.cursor/commands/[command-name].md`

**Key Features:**
- Feature 1
- Feature 2

---

## 🔄 Adaptations Needed

### [Adaptation Category]

**Change:** [What needs to change]  
**Reason:** [Why this change is needed]  
**Impact:** [How this affects dev-infra usage]

**Original:**
[Original code/pattern]

**Adapted:**
[Adapted code/pattern]

**Files to modify:**
- `[file1]` - [reason]
- `[file2]` - [reason]

---

## 📝 Implementation Steps

1. **Step 1: [Name]**
   - [ ] Task 1
   - [ ] Task 2

---

## ✅ Definition of Done

- [ ] Command adapted for dev-infra
- [ ] Documentation updated
- [ ] Ready for use in dev-infra

---

**Last Updated:** YYYY-MM-DD
```

---

## 💡 Tips

### Before Adapting

- Understand original command thoroughly
- Identify all project-specific assumptions
- Think about how dev-infra will use it

### During Adaptation

- Make minimal changes (preserve what works)
- Document rationale for each change
- Provide clear examples

### After Adaptation

- Test adapted command in dev-infra context
- Update dev-infra documentation
- Create usage examples

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Continue adapting commands for dev-infra

