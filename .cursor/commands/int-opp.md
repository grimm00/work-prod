# Document Internal Opportunities

After completing a phase, use this command to capture learnings for improving dev-infra template.

## Instructions

1. Create phase learnings document in `docs/maintainers/planning/notes/opportunities/internal/`
2. Document actionable template improvements
3. Update the internal opportunities README

---

## Phase Learnings Template

**File:** `docs/maintainers/planning/notes/opportunities/internal/phase-N-learnings.md`

### Structure to include:

#### Header
- Phase name and number
- Completion date
- Duration (days/hours)
- Applied to dev-infra status
- Last updated date

#### Overview Section
- Phase summary (what was built)
- Timeline & effort table
- Key metrics (tests, coverage, PRs, LOC)
- Major achievements

#### What Worked Exceptionally Well
For each successful pattern:
- Why it worked
- What made it successful
- Template implications (directory structure, code patterns)
- Key code examples
- Benefits realized

Categories to consider:
- Development patterns (architecture, testing)
- Workflow processes (Git Flow, PR reviews)
- Documentation approaches (hub-spoke, ADRs)
- Tools and automation (CLI, testing tools)
- Code quality practices (TDD, coverage)

#### What Needs Improvement
For each pain point:
- What the problem was
- Why it occurred
- Impact on development
- How to prevent in future projects
- Specific template changes needed

Categories to consider:
- Setup friction
- Missing documentation
- Process gaps
- Tool limitations
- Configuration issues

#### Unexpected Discoveries
- Findings that surprised you
- Insights about tools/patterns
- Better approaches discovered mid-phase
- Things that worked differently than expected

#### Time Investment Analysis
- Breakdown of where time was spent
- What took longer than expected
- What was faster than expected
- Lessons for future estimation

#### Metrics & Impact
- Lines of code written
- Test coverage achieved
- Number of bugs found/fixed
- External review feedback (Sourcery)
- Developer experience improvements

---

## Dev-Infra Improvements Template

**File:** `docs/maintainers/planning/notes/opportunities/internal/dev-infra-improvements-phaseN.md`

### Structure to include:

#### Introduction
- Source (which phase)
- Target (dev-infra template)
- Status
- Why improvements matter
- How discovered
- What problem they solve

#### Improvement Sections

Organize by category (adjust as needed):

**Pre-Project Setup**
- Research templates to add/enhance
- Decision record templates needed
- Planning guides to improve

**Project Structure**
- Directories to pre-create
- .gitkeep files needed
- Structure comments/documentation

**Configuration**
- Config templates to add
- Environment variable patterns
- Security best practices to encode

**Testing Infrastructure**
- Test setup patterns
- Fixture templates
- Coverage configuration
- CI/CD improvements

**Documentation**
- README templates
- Hub-spoke patterns
- ADR templates
- Manual testing guides

**Development Workflow**
- Git Flow setup
- PR templates
- Review checklists
- Fix tracking systems

**CLI/Tooling**
- CLI patterns to template
- Script templates
- Automation opportunities

#### For Each Improvement:

- [ ] **Improvement Title**
  - **Location:** Specific file path in template
  - **Action:** What to do
  - **Prevents/Enables:** Problem solved or capability added
  - **Content/Example:** Code or content to add
  - **Expected Impact:** Benefit statement
  - **Priority:** CRITICAL/HIGH/MEDIUM/LOW
  - **Effort:** LOW/MEDIUM/HIGH

---

## Update Tracking

After creating documents:

1. Update `internal/README.md` completion tracking table
2. Add new phase row with status
3. Update "Last Updated" date
4. Link to new documents in Quick Links

Example update:

```markdown
| Phase | Learnings Doc | Status | Applied to dev-infra |
|-------|--------------|--------|---------------------|
| Phase N | phase-N-learnings.md | ✅ Complete | 🟡 Pending |
```

---

## Tips

### While Working
- Keep notes throughout phase (don't wait until end)
- Capture friction moments immediately
- Note "aha!" moments when they happen
- Track time spent on different activities

### During Documentation
- Be specific (exact file paths, line numbers)
- Include code examples
- Think "would this help me 6 months ago?"
- Focus on actionable items
- Estimate impact and effort

### Quality Checks
- Can someone follow your improvement checklist?
- Are your examples copy-pasteable?
- Did you explain WHY, not just WHAT?
- Are priorities and effort estimates realistic?

---

## Reference Examples

- **Comprehensive:** `phase-1-learnings.md` - 880 lines covering everything
- **Actionable:** `dev-infra-improvements.md` - Specific checklist with file locations

Follow these as models for structure and level of detail.

