# Command Coverage for Dev-Infra Handoff

**Purpose:** Track which commands have adaptation documentation for dev-infra  
**Status:** 🟡 In Progress  
**Created:** 2025-12-07  
**Last Updated:** 2025-12-07

---

## 📊 Command Coverage Status

**Total Commands:** 14  
**Adaptation Documents:** 5  
**Coverage:** 36% (5/14)

---

## ✅ Commands with Adaptation Documents

| Command | Adaptation Doc | Status | Priority |
|---------|--------------|--------|----------|
| `/int-opp` | [int-opp-adaptation.md](int-opp-adaptation.md) | ✅ Complete | HIGH |
| `/reflect` | [reflect-adaptation.md](reflect-adaptation.md) | ✅ Documented | HIGH |
| `/fix-plan` | [fix-plan-adaptation.md](fix-plan-adaptation.md) | ✅ Documented | HIGH |
| `/transition-plan` | [transition-plan-adaptation.md](transition-plan-adaptation.md) | ✅ Documented | HIGH |
| `/task-phase` | [task-phase-adaptation.md](task-phase-adaptation.md) | ✅ Documented | HIGH |

---

## 🟡 Commands Needing Adaptation Documents

### High Priority (Core Workflow)

| Command | Purpose | Priority | Notes |
|---------|---------|----------|-------|
| `/pr` | PR creation workflow | 🔴 HIGH | Central PR creation command - critical for workflow |
| `/fix-implement` | Implement fix batches | 🔴 HIGH | Core fix management workflow |
| `/fix-review` | Review deferred issues | 🔴 HIGH | Cross-PR fix management |
| `/post-pr` | Post-merge documentation | 🔴 HIGH | Documentation workflow |
| `/reflection-artifacts` | Extract planning artifacts | 🔴 HIGH | Reflection workflow completion |

### Medium Priority (Supporting Workflow)

| Command | Purpose | Priority | Notes |
|---------|---------|----------|-------|
| `/pr-validation` | PR validation and review | 🟡 MEDIUM | Sourcery review integration |
| `/pre-phase-review` | Pre-phase planning | 🟡 MEDIUM | Phase planning workflow |
| `/task-release` | Release task implementation | 🟡 MEDIUM | Release workflow |

### Low Priority (Optional/Project-Specific)

| Command | Purpose | Priority | Notes |
|---------|---------|----------|-------|
| `/cursor-rules` | Cursor rules management | 🟢 LOW | Project-specific tooling |

---

## 🎯 Recommended Adaptation Order

### Phase 1: Core Workflow (HIGH Priority)

1. **`/pr`** - PR creation workflow
   - Most frequently used command
   - Central to all workflows
   - Needs generic templates and paths

2. **`/fix-implement`** - Fix implementation
   - Core fix management workflow
   - Depends on `/fix-plan` (already documented)
   - Needs generic fix paths

3. **`/fix-review`** - Fix review
   - Cross-PR fix management
   - Complements `/fix-plan` and `/fix-implement`
   - Needs generic fix tracking paths

4. **`/post-pr`** - Post-merge documentation
   - Documentation workflow completion
   - Depends on PR structure
   - Needs generic documentation paths

5. **`/reflection-artifacts`** - Artifact extraction
   - Reflection workflow completion
   - Depends on `/reflect` (already documented)
   - Needs generic artifact paths

### Phase 2: Supporting Workflow (MEDIUM Priority)

6. **`/pr-validation`** - PR validation
   - Sourcery review integration
   - Supports PR workflow
   - Needs generic review paths

7. **`/pre-phase-review`** - Pre-phase planning
   - Phase planning workflow
   - Supports phase-based development
   - Needs generic phase paths

8. **`/task-release`** - Release tasks
   - Release workflow
   - Supports release management
   - Needs generic release paths

### Phase 3: Optional (LOW Priority)

9. **`/cursor-rules`** - Rules management
   - Project-specific tooling
   - May not be needed in dev-infra
   - Evaluate if needed

---

## 📝 Adaptation Checklist

### For Each Command:

- [ ] **Analyze Command**
  - [ ] Read command documentation
  - [ ] Identify project-specific assumptions
  - [ ] List hardcoded paths
  - [ ] Identify dependencies

- [ ] **Create Adaptation Document**
  - [ ] Use adaptation template
  - [ ] Document original command
  - [ ] List adaptations needed
  - [ ] Provide before/after examples
  - [ ] Add implementation steps

- [ ] **Update Coverage**
  - [ ] Add to coverage table
  - [ ] Update README
  - [ ] Mark as documented

---

## 🎯 Completion Goals

**Phase 1 (Core Workflow):** 5 commands  
**Target:** Complete by end of Week 1

**Phase 2 (Supporting Workflow):** 3 commands  
**Target:** Complete by end of Week 2

**Phase 3 (Optional):** 1 command  
**Target:** Evaluate need, document if required

**Overall Target:** 80%+ coverage (11/14 commands)

---

**Last Updated:** 2025-12-07  
**Status:** 🟡 In Progress  
**Next:** Create adaptation documents for Phase 1 commands

