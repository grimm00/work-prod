# Transition Plan Command

Creates transition planning documents from reflection artifacts or directly from reflection documents. Plans the next stage of the project (feature, release, infrastructure) based on reflection insights.

---

## Workflow Overview

**When to use:**

- After creating reflection artifacts with `/reflection-artifacts`
- To plan transition to next stage (feature, release, infrastructure)
- When ready to move from reflection to implementation planning

**Key principle:** Transform reflection artifacts into actionable transition plans ready for implementation, following established planning patterns. For feature transitions, also create detailed phase documents (`phase-#.md`) following comprehensive phase structure with TDD workflow.

---

## Usage

**Command:** `/transition-plan [--from-artifacts|--from-reflection] [options]`

**Examples:**

- `/transition-plan --from-reflection reflection-2025-12-07-mvp-complete.md` - Create transition plan from reflection (auto-generates artifacts first)
- `/transition-plan --from-artifacts releases/v0.1.0/checklist.md` - Create transition plan from specific artifact
- `/transition-plan --type release` - Force release transition type
- `/transition-plan --type feature` - Force feature transition type
- `/transition-plan --dry-run` - Show transition plan without creating files

**Options:**

- `--from-reflection FILE` - Use reflection file (auto-generates artifacts first, then creates plans)
- `--from-artifacts PATH` - Use specific artifact file (e.g., `releases/v0.1.0/checklist.md`)
- `--type TYPE` - Force transition type (`feature`, `release`, `ci-cd`, `infrastructure`, `auto`)
- `--dry-run` - Show transition plan without creating files

---

## Step-by-Step Process

### Mode Selection

**Two modes of operation:**

1. **Artifact Mode (default):** Create plans from existing artifacts
   - Use: `/transition-plan --from-artifacts [path]`
   - Reads: Artifact files created by `/reflection-artifacts`
   - Creates: Transition planning documents

2. **Reflection Mode:** Create plans from reflection (auto-generates artifacts first)
   - Use: `/transition-plan --from-reflection [file]`
   - Reads: Reflection document
   - Internally calls `/reflection-artifacts` first
   - Then creates transition plans from artifacts

**If `--from-reflection` is specified, skip to "From Reflection Mode" section below.**

---

### 1. Identify Artifact File (Artifact Mode)

**Default behavior:**

- If no artifact specified, look for latest artifacts in planning directories
- Check `docs/maintainers/planning/releases/` for latest release
- Check `docs/maintainers/planning/features/` for latest feature
- Use most recent artifact

**Manual specification:**

- Use provided artifact path
- Verify artifact file exists and is readable

**Commands:**

```bash
# Find latest release artifact
ls -t docs/maintainers/planning/releases/v*/checklist.md | head -1

# Find latest feature artifact
ls -t docs/maintainers/planning/features/*/feature-plan.md | head -1

# Check if artifact exists
ls docs/maintainers/planning/releases/v0.1.0/checklist.md
```

**Checklist:**

- [ ] Artifact file identified (or using default)
- [ ] File exists and is readable
- [ ] Artifact type determined (release, feature, ci-cd, infrastructure)

---

### 2. Determine Transition Type

**Auto-detection logic:**

1. **Release Transition:**
   - Artifact path contains `releases/`
   - Artifact filename is `checklist.md` or `release-notes.md`
   - Artifact content mentions "release", "version", "tag"

2. **Feature Transition:**
   - Artifact path contains `features/`
   - Artifact filename is `feature-plan.md`
   - Artifact content mentions "feature", "implementation", "phases"

3. **CI/CD Transition:**
   - Artifact path contains `ci/`
   - Artifact filename is `improvement-plan.md`
   - Artifact content mentions "ci", "cd", "pipeline", "automation"

4. **Infrastructure Transition:**
   - Artifact path contains `infrastructure/`
   - Artifact filename is `improvement-plan.md`
   - Artifact content mentions "infrastructure", "monitoring", "logging"

**Manual override:**

- Use `--type` option to force specific type
- Useful when auto-detection is ambiguous

**Checklist:**

- [ ] Transition type determined (or forced with `--type`)
- [ ] Type is appropriate for artifact
- [ ] Type matches project needs

---

### 3. Parse Artifact Content

**Extract from artifact:**

- Overview/description
- Success criteria
- Implementation steps
- Next steps
- Priority and effort
- Benefits

**Parse implementation steps:**

- Extract actionable steps
- **Extract ALL phases** from artifact (Phase 1, Phase 2, Phase 3, etc.)
- Organize into logical phases (if feature)
- Preserve phase structure, goals, tasks, deliverables, and effort estimates
- Identify dependencies between phases
- Estimate effort per phase

**Example parsing:**

```markdown
## Implementation Steps

1. Create release directory structure
2. Create release checklist template
3. Create release notes template
4. Document version tagging process
5. Prepare MVP release (v0.1.0)
```

**Checklist:**

- [ ] Artifact content parsed
- [ ] **ALL phases extracted** (not just Phase 1 and Phase 2)
- [ ] Implementation steps extracted
- [ ] Phase structure preserved (goals, tasks, deliverables, effort)
- [ ] Dependencies identified
- [ ] Effort estimated

---

### 4. Create Transition Planning Documents

**For Release Transition:**

**Location:** `docs/maintainers/planning/releases/vX.Y.Z/`

**Documents created:**
- `transition-plan.md` - Detailed transition plan
- Update `checklist.md` - Add transition-specific checklist items

**Transition Plan Template:**

```markdown
# Release Transition Plan - vX.Y.Z

**Version:** vX.Y.Z  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Source:** [artifact-file]  
**Type:** Release

---

## Overview

[Extracted from artifact overview]

## Transition Goals

[Extracted from artifact success criteria]

## Pre-Transition Checklist

- [ ] All prerequisites met
- [ ] Release artifacts reviewed
- [ ] Release checklist complete
- [ ] Release notes prepared

## Transition Steps

[Extracted from artifact implementation steps, organized chronologically]

1. **Step 1: [Name]**
   - [ ] Task 1
   - [ ] Task 2
   - Estimated: [X] hours

2. **Step 2: [Name]**
   - [ ] Task 1
   - [ ] Task 2
   - Estimated: [X] hours

## Post-Transition

- [ ] Release tagged
- [ ] Release notes published
- [ ] Documentation updated
- [ ] Monitoring active

## Definition of Done

- [ ] All transition steps complete
- [ ] Release successful
- [ ] Post-transition tasks complete
- [ ] Ready for next stage
```

---

**For Feature Transition:**

**Location:** `docs/maintainers/planning/features/[feature-name]/`

**Documents created:**
- `transition-plan.md` - Detailed transition plan
- Update `feature-plan.md` - Add transition-specific details

**Transition Plan Template:**

```markdown
# Feature Transition Plan - [Feature Name]

**Feature:** [Feature Name]  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Source:** [artifact-file]  
**Type:** Feature

---

## Overview

[Extracted from artifact overview]

## Transition Goals

[Extracted from artifact success criteria]

## Pre-Transition Checklist

- [ ] Feature plan reviewed
- [ ] Prerequisites identified
- [ ] Dependencies resolved
- [ ] Resources allocated

## Transition Steps

[Extracted from artifact implementation steps, organized into phases]

**IMPORTANT:** Extract **ALL phases** from the artifact (Phase 1, Phase 2, Phase 3, Phase 4, etc.). Do not stop at Phase 2.

### Phase 1: [Phase Name]

**Goal:** [Extracted from artifact phase goal]

**Estimated Effort:** [X] hours/days

**Prerequisites:**

- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

**Tasks:**

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Deliverables:**

- [Deliverable 1]
- [Deliverable 2]

**Definition of Done:**

- [ ] All tasks complete
- [ ] Deliverables created
- [ ] Ready for Phase 2

---

### Phase 2: [Phase Name]

**Goal:** [Extracted from artifact phase goal]

**Estimated Effort:** [X] hours/days

**Prerequisites:**

- [ ] Phase 1 complete
- [ ] [Additional prerequisites]

**Tasks:**

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Deliverables:**

- [Deliverable 1]
- [Deliverable 2]

**Definition of Done:**

- [ ] All tasks complete
- [ ] Deliverables created
- [ ] Ready for Phase 3 (or post-transition if last phase)

---

### Phase 3: [Phase Name]

[Continue extracting ALL phases from artifact. Include Phase 3, Phase 4, Phase 5, etc. as they exist in the artifact.]

**Goal:** [Extracted from artifact phase goal]

**Estimated Effort:** [X] hours/days

**Prerequisites:**

- [ ] Phase 2 complete
- [ ] [Additional prerequisites]

**Tasks:**

- [ ] Task 1
- [ ] Task 2

**Deliverables:**

- [Deliverable 1]

**Definition of Done:**

- [ ] All tasks complete
- [ ] Deliverables created
- [ ] Ready for post-transition (if last phase)

## Post-Transition

- [ ] Feature complete
- [ ] Documentation updated
- [ ] Tests passing
- [ ] Ready for next feature

## Definition of Done

- [ ] All phases complete
- [ ] Feature implemented
- [ ] Tests passing
- [ ] Documentation updated
```

---

**For CI/CD Transition:**

**Location:** `docs/maintainers/planning/ci/[improvement-name]/`

**Documents created:**
- `transition-plan.md` - Detailed transition plan

**Transition Plan Template:**

```markdown
# CI/CD Transition Plan - [Improvement Name]

**Improvement:** [Improvement Name]  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Source:** [artifact-file]  
**Type:** CI/CD

---

## Overview

[Extracted from artifact overview]

## Transition Goals

[Extracted from artifact benefits]

## Pre-Transition Checklist

- [ ] Improvement plan reviewed
- [ ] CI/CD infrastructure ready
- [ ] Dependencies identified
- [ ] Rollback plan prepared

## Transition Steps

[Extracted from artifact implementation steps]

1. **Step 1: [Name]**
   - [ ] Task 1
   - [ ] Task 2
   - Estimated: [X] hours

2. **Step 2: [Name]**
   - [ ] Task 1
   - [ ] Task 2
   - Estimated: [X] hours

## Post-Transition

- [ ] Improvement deployed
- [ ] CI/CD pipeline verified
- [ ] Documentation updated
- [ ] Monitoring active

## Definition of Done

- [ ] All steps complete
- [ ] CI/CD improvement active
- [ ] Tests passing
- [ ] Documentation updated
```

---

### 5. Create Phase Documents (For Feature Transitions)

**When this applies:** Only for Feature transitions. Release and CI/CD transitions use transition plans directly.

**Process:**

1. **Extract phases from transition plan:**
   - Read `transition-plan.md` created in Step 4
   - Extract phase/step number, name, goal, tasks, deliverables, prerequisites, effort
   - Identify all phases/steps (Phase/Step 1, Phase/Step 2, Phase/Step 3, etc.)

2. **For each phase/step, create `phase-#.md` file:**
   - Use phase document template (see `docs/PHASE-DOCUMENT-TEMPLATE.md` if exists)
   - Populate with extracted phase/step information
   - **For Feature Transitions:** Expand tasks with TDD flow structure (RED → GREEN → REFACTOR)
   - Add project-specific implementation notes

3. **Phase document structure:**
   - Header: Phase number, name, duration, status, prerequisites
   - Overview: What phase delivers, success definition
   - Goals: Numbered list of phase goals
   - Tasks: Detailed TDD flow with proper ordering
   - Completion Criteria: Checklist of completion requirements
   - Deliverables: What gets created/delivered
   - Dependencies: Prerequisites, external dependencies, blocks
   - Risks: Risk assessment with mitigation (if applicable)
   - Progress Tracking: Status tracking by category
   - Implementation Notes: TDD workflow, patterns, examples
   - Related Documents: Links to related docs

**File locations:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`

**Key sections to populate:**

- **Header:** Extract from transition plan phase header
- **Overview:** Expand phase goal into detailed overview with success definition
- **Goals:** Extract and expand phase goals
- **Tasks:** Expand transition plan tasks into detailed TDD flow with proper ordering:
  - **TDD Task Ordering (IMPORTANT):** Order tasks following RED → GREEN → REFACTOR:
    1. **Tests first (RED):** Write tests before implementation code
    2. **Implementation second (GREEN):** Write minimum code to pass tests
    3. **Refactor/documentation last:** Clean up and document
  - Group tasks into RED/GREEN pairs where applicable
  - Add detailed sub-tasks with checkboxes
  - Include code examples where applicable
  - Add testing commands and manual testing steps
  - **Example TDD Task Order:**
    - Task 1: Write tests for feature X (RED)
    - Task 2: Implement feature X (GREEN)
    - Task 3: Write tests for feature Y (RED)
    - Task 4: Implement feature Y (GREEN)
    - Task 5: Documentation and cleanup
- **Completion Criteria:** Extract from transition plan "Definition of Done"
- **Deliverables:** Extract from transition plan deliverables
- **Dependencies:** Extract prerequisites, add external dependencies if known
- **Risks:** Add risk assessment if applicable
- **Progress Tracking:** Add status tracking sections
- **Implementation Notes:** Add TDD workflow guidance, patterns, examples
- **Related Documents:** Link to previous/next phases, feature plan, hub

**Task Ordering Patterns:**

Depending on the phase type, use the appropriate task ordering pattern:

| Phase Type | Task Order | Example |
|------------|------------|---------|
| **Code + Tests (TDD)** | Tests → Implementation → Docs | Write tests, implement code, document |
| **Scripts (TDD)** | Tests → Script → Integration | Write bats tests, create script, integrate |
| **Documentation Only** | Create → Link → Verify | Create docs, add links, verify links work |
| **Configuration** | Plan → Implement → Validate | Define config, apply changes, verify |

**When ordering tasks, ask:** "What needs to exist first for TDD to work?"

- **If tests can be written:** Put test tasks BEFORE implementation tasks
- **If no tests apply:** Put validation/verification tasks LAST
- **If documentation phase:** Put doc creation before linking/integration

**Checklist:**

- [ ] All phases/steps extracted from transition plan
- [ ] Phase documents created (`phase-1.md`, `phase-2.md`, etc.)
- [ ] Phase documents follow template structure
- [ ] Tasks expanded with TDD workflow
- [ ] Tasks ordered correctly (tests before implementation)
- [ ] Implementation notes added
- [ ] Related documents linked
- [ ] Phase documents are detailed (~200-300+ lines)

---

### 6. Update Planning Hubs

**Update relevant hub files:**

1. **Release Hub:**
   - File: `docs/maintainers/planning/releases/README.md`
   - Update release status
   - Add transition plan link

2. **Feature Hub:**
   - File: `docs/maintainers/planning/features/README.md` (if exists)
   - Update feature status
   - Add transition plan link

3. **CI/CD Hub:**
   - File: `docs/maintainers/planning/ci/README.md` (if exists)
   - Update improvement status
   - Add transition plan link

**Checklist:**

- [ ] Release hub updated (if release transition)
- [ ] Feature hub updated (if feature transition)
- [ ] CI/CD hub updated (if CI/CD transition)
- [ ] Hub links verified

---

### 7. Summary Report

**Present to user:**

```markdown
## Transition Plan Complete

**Source:** [artifact-file or reflection-file]
**Type:** [Release/Feature/CI/CD/Infrastructure]

### Transition Planning Documents Created

- `transition-plan.md` - Detailed transition plan
- `phase-1.md`, `phase-2.md`, `phase-3.md`, etc. - Detailed phase documents (for feature transitions)
- Updated artifact files with transition details

### Transition Steps

- [N] steps/phases identified
- Estimated effort: [X] hours
- Estimated duration: [Y] days

### Phase Documents (Feature Transitions)

- [N] phase documents created
- Each phase document includes: Overview, Goals, Tasks (TDD flow), Completion Criteria, Deliverables, Dependencies, Implementation Notes
- Phase documents are detailed (~200-300+ lines each)

### Next Steps

1. Review transition plan
2. Review phase documents (if created)
3. Begin implementation when ready
4. Use `/task-phase` to implement phases (reads `phase-#.md` files)
5. Use `/task-release` or `/pr` commands for releases
```

---

## From Reflection Mode

**When to use:**

- When reflection exists but artifacts haven't been created yet
- To streamline workflow (one command instead of two)
- When starting fresh from reflection

**Key principle:** Internally calls `/reflection-artifacts` first, then creates transition plans from generated artifacts.

---

### 1. Load Reflection File

**File location:**

- Default: Latest reflection in `docs/maintainers/planning/notes/reflections/`
- Manual: `--from-reflection reflection-2025-12-07-mvp-complete.md`

**Extract from reflection:**

- "Actionable Suggestions" section
- "Recommended Next Steps" section
- Current state information

**Checklist:**

- [ ] Reflection file found
- [ ] File is readable and well-formatted
- [ ] Actionable suggestions identified

---

### 2. Generate Artifacts (Internal Call)

**Process:**

1. Internally call `/reflection-artifacts` workflow
2. Generate artifacts from reflection
3. Store artifacts in appropriate directories
4. Continue with transition plan creation

**Artifacts generated:**

- Release artifacts (if release suggestions found)
- Feature artifacts (if feature suggestions found)
- CI/CD artifacts (if CI/CD suggestions found)

**Checklist:**

- [ ] Artifacts generated successfully
- [ ] Artifacts placed in correct directories
- [ ] Artifact types determined

---

### 3. Create Transition Plans from Artifacts

**Process:**

- Use generated artifacts as input
- Follow "Artifact Mode" workflow (steps 2-6 above)
- Create transition plans from artifacts

**Checklist:**

- [ ] Transition plans created from artifacts
- [ ] Plans follow appropriate templates
- [ ] Plans are actionable

---

## Transition Type Details

### Release Transition

**When triggered:**
- Release artifacts exist
- Release checklist needs completion
- MVP release preparation needed

**Planning focus:**
- Release preparation steps
- Version tagging process
- Release notes preparation
- Post-release tasks

**Output:**
- Release transition plan
- Updated release checklist
- Release preparation timeline

---

### Feature Transition

**When triggered:**
- Feature artifacts exist
- New feature planning needed
- Feature implementation ready to begin

**Planning focus:**
- Feature implementation phases
- Dependencies and prerequisites
- Resource allocation
- Success criteria

**Output:**
- Feature transition plan
- Updated feature plan
- Implementation timeline

---

### CI/CD Transition

**When triggered:**
- CI/CD artifacts exist
- CI/CD improvements needed
- Pipeline enhancements planned

**Planning focus:**
- CI/CD improvement steps
- Pipeline configuration
- Deployment automation
- Monitoring setup

**Output:**
- CI/CD transition plan
- Improvement implementation timeline

---

## Common Issues

### Issue: No Artifacts Found

**Solution:**

- Run `/reflection-artifacts` first to generate artifacts
- Or use `--from-reflection` to auto-generate artifacts
- Check artifact directory paths

### Issue: Transition Type Ambiguous

**Solution:**

- Use `--type` option to force specific type
- Review artifact content to determine type
- Check artifact file path for type hints

### Issue: Artifact Content Incomplete

**Solution:**

- Review artifact file for completeness
- Update artifact with additional context
- Re-run `/reflection-artifacts` if needed

---

## Tips

### Before Running

- Ensure artifacts exist (or use `--from-reflection`)
- Review artifact content for completeness
- Determine desired transition type

### During Planning

- Review extracted steps for accuracy
- Organize steps chronologically
- Identify dependencies between steps

### After Planning

- Review transition plan for completeness
- Update plan with additional context if needed
- Begin implementation when ready

---

## Reference

**Artifact Files:**

- Releases: `docs/maintainers/planning/releases/vX.Y.Z/checklist.md`
- Features: `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
- CI/CD: `docs/maintainers/planning/ci/[improvement-name]/improvement-plan.md`

**Reflection Files:**

- `docs/maintainers/planning/notes/reflections/reflection-*.md`

**Transition Plans:**

- `docs/maintainers/planning/releases/vX.Y.Z/transition-plan.md`
- `docs/maintainers/planning/features/[feature-name]/transition-plan.md`
- `docs/maintainers/planning/ci/[improvement-name]/transition-plan.md`

**Related Commands:**

- `/reflection-artifacts` - Generate artifacts from reflection (run first, or auto-called)
- `/reflect` - Create reflection documents
- `/task-phase` - Implement phase tasks
- `/task-release` - Implement release transition tasks
- `/pr` - Create PRs for completed work

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active  
**Next:** Use after `/reflection-artifacts` to create transition plans, or use `--from-reflection` to streamline workflow (enforces TDD task ordering for feature transitions)

--- End Command ---

