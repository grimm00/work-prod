# Transition Plan Command

Creates transition planning documents from reflection artifacts or directly from reflection documents. Plans the next stage of the project (feature, release, infrastructure) based on reflection insights.

---

## Workflow Overview

**When to use:**

- After creating reflection artifacts with `/reflection-artifacts`
- To plan transition to next stage (feature, release, infrastructure)
- When ready to move from reflection to implementation planning

**Key principle:** Transform reflection artifacts into actionable transition plans ready for implementation, following established planning patterns.

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
- Organize into logical phases (if feature)
- Identify dependencies
- Estimate effort

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
- [ ] Implementation steps extracted
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

### Phase 1: [Phase Name]

- [ ] Task 1
- [ ] Task 2
- Estimated: [X] hours

### Phase 2: [Phase Name]

- [ ] Task 1
- [ ] Task 2
- Estimated: [X] hours

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

### 5. Update Planning Hubs

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

### 6. Summary Report

**Present to user:**

```markdown
## Transition Plan Complete

**Source:** [artifact-file or reflection-file]
**Type:** [Release/Feature/CI/CD/Infrastructure]

### Transition Planning Documents Created

- `transition-plan.md` - Detailed transition plan
- Updated artifact files with transition details

### Transition Steps

- [N] steps identified
- Estimated effort: [X] hours
- Estimated duration: [Y] days

### Next Steps

1. Review transition plan
2. Begin implementation when ready
3. Use `/phase-task` or `/pr` commands for implementation
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
- `/phase-task` - Implement individual tasks
- `/pr` - Create PRs for completed work

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use after `/reflection-artifacts` to create transition plans, or use `--from-reflection` to streamline workflow

--- End Command ---

