# Reflection Artifacts Command

Extracts structured planning artifacts from reflection documents. Creates feature plans, release checklists, CI/CD improvement plans, and other actionable documents ready for implementation.

---

## Workflow Overview

**When to use:**

- After creating a reflection document with `/reflect`
- To extract actionable suggestions into structured planning artifacts
- Before planning next stage (feature, release, infrastructure)

**Key principle:** Transform reflection insights into structured, actionable planning artifacts following established templates.

---

## Usage

**Command:** `/reflection-artifacts [reflection-file] [options]`

**Examples:**

- `/reflection-artifacts` - Extract artifacts from latest reflection (default)
- `/reflection-artifacts reflection-2025-12-07-mvp-complete.md` - Use specific reflection file
- `/reflection-artifacts --type release` - Only generate release artifacts
- `/reflection-artifacts --type feature` - Only generate feature artifacts
- `/reflection-artifacts --type all` - Generate all artifact types (default)
- `/reflection-artifacts --output-dir releases/v0.1.0` - Custom output directory
- `/reflection-artifacts --dry-run` - Show what would be created without creating files

**Options:**

- `--from-reflection FILE` - Specify reflection file (default: latest in reflections/)
- `--type TYPE` - Artifact type to generate (`feature`, `release`, `ci-cd`, `infrastructure`, `all`)
- `--output-dir DIR` - Custom output directory (default: appropriate planning directory)
- `--dry-run` - Show artifact plan without creating files

---

## Step-by-Step Process

### 1. Identify Reflection File

**Default behavior:**

- Find latest reflection file in `docs/maintainers/planning/notes/reflections/`
- Sort by date (most recent first)
- Use latest reflection file

**Manual specification:**

- Use provided reflection file path
- Verify file exists and is readable

**Commands:**

```bash
# Find latest reflection
ls -t docs/maintainers/planning/notes/reflections/reflection-*.md | head -1

# Check if reflection file exists
ls docs/maintainers/planning/notes/reflections/reflection-2025-12-07-mvp-complete.md
```

**Checklist:**

- [ ] Reflection file identified (or using default)
- [ ] File exists and is readable
- [ ] File contains "Actionable Suggestions" section

---

### 2. Parse Reflection Document

**Extract from reflection file:**

- "Actionable Suggestions" section
- "Recommended Next Steps" section
- "Opportunities for Improvement" section
- "Potential Issues" section
- Current state information
- Key metrics

**Parse actionable suggestions:**

- Extract suggestions by priority (HIGH, MEDIUM, LOW)
- Categorize by type (feature, release, ci-cd, infrastructure)
- Extract effort estimates
- Extract benefits and next steps

**Example parsing:**

```markdown
### High Priority

#### 1. Create Release Management Structure

**Category:** Release Management  
**Priority:** 🔴 High  
**Effort:** MEDIUM (2-3 hours)

**Suggestion:**
Create release directory structure and templates...

**Next Steps:**
1. Create release directory structure
2. Create release checklist template
...
```

**Checklist:**

- [ ] Reflection document parsed
- [ ] Actionable suggestions extracted
- [ ] Suggestions categorized by type
- [ ] Priority and effort extracted

---

### 3. Categorize Suggestions by Type

**Categorization logic:**

1. **Release Management:**
   - Keywords: "release", "version", "tag", "changelog", "release notes"
   - Examples: "Create release checklist", "Prepare MVP release"

2. **Feature Planning:**
   - Keywords: "feature", "new feature", "implement", "add capability"
   - Examples: "Add new feature", "Implement feature X"

3. **CI/CD Improvements:**
   - Keywords: "ci", "cd", "pipeline", "automation", "deployment"
   - Examples: "Improve CI pipeline", "Add deployment automation"

4. **Infrastructure:**
   - Keywords: "infrastructure", "devops", "monitoring", "logging"
   - Examples: "Set up monitoring", "Improve logging"

**Checklist:**

- [ ] Suggestions categorized by type
- [ ] Each suggestion assigned to appropriate category
- [ ] Categories verified

---

### 4. Generate Artifacts by Type

**For each artifact type:**

#### Release Artifacts

**Location:** `docs/maintainers/planning/releases/vX.Y.Z/`

**Artifacts created:**
- `checklist.md` - Release preparation checklist
- `release-notes.md` - Release notes draft

**Template structure:**

**Release Checklist:**
```markdown
# Release Checklist - vX.Y.Z

**Version:** vX.Y.Z  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Source:** reflection-YYYY-MM-DD.md

---

## Pre-Release

- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] Documentation reviewed
- [ ] Production configuration verified
- [ ] Deployment guide reviewed
- [ ] Critical bugs fixed
- [ ] HIGH priority issues addressed

## Release

- [ ] Version tagged
- [ ] Release notes prepared
- [ ] Changelog updated
- [ ] Documentation updated

## Post-Release

- [ ] Release notes published
- [ ] Deployment verified
- [ ] Monitoring active
```

**Release Notes:**
```markdown
# Release Notes - vX.Y.Z

**Release Date:** YYYY-MM-DD  
**Status:** Stable  
**Source:** reflection-YYYY-MM-DD.md

---

## What's New

[Extracted from reflection suggestions]

## Improvements

[Extracted from reflection suggestions]

## Bug Fixes

[Extracted from reflection suggestions]

## Breaking Changes

- None (or list breaking changes)

## Migration Guide

[If migration needed]
```

---

#### Feature Artifacts

**Location:** `docs/maintainers/planning/features/[feature-name]/`

**Artifacts created:**
- `feature-plan.md` - Feature plan draft
- `status-and-next-steps.md` - Status tracking document

**Template structure:**

**Feature Plan:**
```markdown
# [Feature Name] - Feature Plan

**Feature:** [Feature Name]  
**Priority:** [Priority Level]  
**Status:** 🟡 Planned  
**Created:** YYYY-MM-DD  
**Source:** reflection-YYYY-MM-DD.md

---

## 📋 Overview

[Extracted from reflection suggestion description]

## 🎯 Success Criteria

[Extracted from reflection suggestion benefits]

## 📅 Implementation Phases

[Extracted from reflection next steps, organized into phases]

## 🚀 Next Steps

[Extracted from reflection next steps]
```

---

#### CI/CD Artifacts

**Location:** `docs/maintainers/planning/ci/[improvement-name]/`

**Artifacts created:**
- `improvement-plan.md` - CI/CD improvement plan

**Template structure:**

```markdown
# CI/CD Improvement Plan - [Improvement Name]

**Improvement:** [Improvement Name]  
**Priority:** [Priority Level]  
**Effort:** [Effort Level]  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Source:** reflection-YYYY-MM-DD.md

---

## Overview

[Extracted from reflection suggestion]

## Benefits

[Extracted from reflection benefits]

## Implementation Steps

[Extracted from reflection next steps]

## Definition of Done

- [ ] Improvement implemented
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Ready for deployment
```

---

### 5. Create Directory Structure

**For each artifact type:**

1. **Release Artifacts:**
   - Create `docs/maintainers/planning/releases/` if needed
   - Create version directory: `docs/maintainers/planning/releases/vX.Y.Z/`
   - Create artifacts in version directory

2. **Feature Artifacts:**
   - Create `docs/maintainers/planning/features/[feature-name]/` if needed
   - Create artifacts in feature directory

3. **CI/CD Artifacts:**
   - Create `docs/maintainers/planning/ci/[improvement-name]/` if needed
   - Create artifacts in improvement directory

**Checklist:**

- [ ] Directory structure created
- [ ] Artifacts placed in appropriate directories
- [ ] Directory structure follows conventions

---

### 6. Update Planning Hubs

**Update relevant hub files:**

1. **Release Hub:**
   - File: `docs/maintainers/planning/releases/README.md`
   - Add new release entry
   - Update release timeline

2. **Feature Hub:**
   - File: `docs/maintainers/planning/features/README.md` (if exists)
   - Add new feature entry

3. **CI/CD Hub:**
   - File: `docs/maintainers/planning/ci/README.md` (if exists)
   - Add new improvement entry

**Checklist:**

- [ ] Release hub updated (if release artifacts created)
- [ ] Feature hub updated (if feature artifacts created)
- [ ] CI/CD hub updated (if CI/CD artifacts created)
- [ ] Hub links verified

---

### 7. Summary Report

**Present to user:**

```markdown
## Reflection Artifacts Complete

**Reflection:** reflection-YYYY-MM-DD.md

### Artifacts Created

- [N] artifacts created
- Breakdown:
  - Release: [X] artifacts
  - Feature: [Y] artifacts
  - CI/CD: [Z] artifacts
  - Infrastructure: [W] artifacts

### Artifact Locations

**Release Artifacts:**
- `docs/maintainers/planning/releases/vX.Y.Z/checklist.md`
- `docs/maintainers/planning/releases/vX.Y.Z/release-notes.md`

**Feature Artifacts:**
- `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
- `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`

**CI/CD Artifacts:**
- `docs/maintainers/planning/ci/[improvement-name]/improvement-plan.md`

### Next Steps

1. Review artifacts in planning directories
2. Use `/transition-plan` command to create transition plans from artifacts
3. Begin implementation when ready
```

---

## Artifact Type Details

### Release Artifacts

**When created:**
- Reflection contains release-related suggestions
- "Release Management Structure" mentioned
- "Prepare MVP Release" suggested
- Version tagging mentioned

**Artifacts:**
- Release checklist (pre-release, release, post-release)
- Release notes draft (what's new, improvements, bug fixes)

**Location:**
- `docs/maintainers/planning/releases/vX.Y.Z/`

---

### Feature Artifacts

**When created:**
- Reflection contains feature suggestions
- "New feature" mentioned
- "Implement feature X" suggested
- Feature capabilities described

**Artifacts:**
- Feature plan draft (overview, success criteria, phases)
- Status tracking document

**Location:**
- `docs/maintainers/planning/features/[feature-name]/`

---

### CI/CD Artifacts

**When created:**
- Reflection contains CI/CD improvement suggestions
- "CI pipeline" mentioned
- "Deployment automation" suggested
- "Automation" improvements mentioned

**Artifacts:**
- CI/CD improvement plan (overview, benefits, implementation steps)

**Location:**
- `docs/maintainers/planning/ci/[improvement-name]/`

---

### Infrastructure Artifacts

**When created:**
- Reflection contains infrastructure suggestions
- "Monitoring" mentioned
- "Logging" improvements suggested
- "DevOps" improvements mentioned

**Artifacts:**
- Infrastructure improvement plan

**Location:**
- `docs/maintainers/planning/infrastructure/[improvement-name]/`

---

## Common Issues

### Issue: No Reflection File Found

**Solution:**

- Check if reflection file exists
- Verify file path is correct
- May need to run `/reflect` first

### Issue: No Actionable Suggestions

**Solution:**

- Check if reflection contains "Actionable Suggestions" section
- Reflection may need to be updated with suggestions
- May need to run `/reflect` with different options

### Issue: Artifact Type Ambiguous

**Solution:**

- Review suggestion keywords
- Manually categorize if needed
- Use `--type` option to force specific type

### Issue: Directory Already Exists

**Solution:**

- Check if artifacts already exist
- Update existing artifacts if needed
- Use `--output-dir` to specify different location

---

## Tips

### Before Running

- Ensure reflection document is complete
- Verify "Actionable Suggestions" section exists
- Review reflection for clear suggestions

### During Artifact Creation

- Review extracted suggestions for accuracy
- Verify artifact types are correct
- Check that all relevant suggestions are included

### After Artifact Creation

- Review artifacts for completeness
- Update artifacts with additional context if needed
- Use `/transition-plan` to create transition plans from artifacts

---

## Reference

**Reflection Files:**

- `docs/maintainers/planning/notes/reflections/reflection-*.md`

**Artifact Locations:**

- Releases: `docs/maintainers/planning/releases/vX.Y.Z/`
- Features: `docs/maintainers/planning/features/[feature-name]/`
- CI/CD: `docs/maintainers/planning/ci/[improvement-name]/`
- Infrastructure: `docs/maintainers/planning/infrastructure/[improvement-name]/`

**Related Commands:**

- `/reflect` - Create reflection documents
- `/transition-plan` - Create transition plans from artifacts (or from reflection)
- `/fix-plan` - Create fix plans from reviews (similar pattern)

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use `/transition-plan` to create transition plans from artifacts, or use artifacts directly for planning

--- End Command ---

