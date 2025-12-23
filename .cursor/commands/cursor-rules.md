# Cursor Rules Management Command

Manage and organize Cursor rules files. Helps split large main.mdc files, create domain-specific rules (backend/frontend), and keep rules organized based on project learnings.

---

## Workflow Overview

**When to use:**

- After capturing learnings with `/int-opp`
- When main.mdc file becomes too long (>500 lines)
- When adding domain-specific rules (backend/frontend)
- To organize rules based on project evolution

**Key principle:** Keep rules organized, maintainable, and easy to navigate. Split when files get too large, reference split files from main.

---

## Usage

**Command:** `/cursor-rules [action] [options]`

**Examples:**

- `/cursor-rules check` - Check if main.mdc needs splitting
- `/cursor-rules split` - Split main.mdc into organized sections
- `/cursor-rules add-backend` - Create backend-specific rules file
- `/cursor-rules add-frontend` - Create frontend-specific rules file
- `/cursor-rules update-from-learnings` - Update rules based on phase learnings
- `/cursor-rules list` - List all rules files and their purposes

**Options:**

- `--check-size` - Check file size and suggest splitting (default: 500 lines)
- `--max-lines N` - Custom maximum lines before suggesting split (default: 500)
- `--dry-run` - Show what would be done without making changes
- `--from-learnings` - Update rules based on latest phase learnings

---

## Step-by-Step Process

### 1. Check Current Rules Structure

**Check main.mdc:**

```bash
# Check file size
wc -l .cursor/rules/main.mdc

# Check if alwaysApply is set
grep "alwaysApply" .cursor/rules/main.mdc
```

**List existing rules files:**

```bash
ls -la .cursor/rules/
```

**Checklist:**

- [ ] Main file size checked
- [ ] Existing rules files identified
- [ ] Current structure understood

---

### 2. Analyze Main File

**Identify logical sections:**

- Project overview and structure
- Documentation standards
- Git Flow and workflow
- Code standards (general)
- Backend-specific patterns
- Frontend-specific patterns
- Testing standards
- CI/CD configuration
- AI assistant guidelines

**Check for:**

- Sections that could be split out
- Domain-specific content (backend/frontend)
- Repeated patterns
- Outdated information

**Checklist:**

- [ ] Logical sections identified
- [ ] Split candidates identified
- [ ] Domain-specific content found

---

### 3. Split Main File (If Needed)

**When to split:**

- Main file > 500 lines (or custom threshold)
- Multiple distinct domains (backend/frontend)
- Sections becoming hard to navigate
- Want domain-specific rules

**Split strategy:**

1. **Keep in main.mdc:**
   - Project overview
   - Documentation standards
   - Git Flow workflow
   - General code standards
   - AI assistant guidelines
   - References to split files

2. **Split to backend.mdc:**
   - Backend-specific patterns
   - Flask/SQLAlchemy conventions
   - API design patterns
   - Backend testing standards

3. **Split to frontend.mdc:**
   - Frontend-specific patterns
   - React/Vite conventions
   - Component patterns
   - Frontend testing standards

4. **Split to workflow.mdc:**
   - Command workflows
   - PR processes
   - Fix tracking processes
   - Documentation processes

**Checklist:**

- [ ] Split files created
- [ ] Sections moved to appropriate files
- [ ] Main file updated with references
- [ ] All files have proper headers
- [ ] References work correctly

---

### 4. Update Rules from Learnings

**After `/int-opp` command:**

1. **Read phase learnings:**
   - Latest phase learnings document
   - Dev-infra improvements document

2. **Identify rule updates:**
   - New patterns to document
   - Process improvements
   - Code standards updates
   - Workflow changes

3. **Update appropriate rules file:**
   - General patterns → main.mdc
   - Backend patterns → backend.mdc
   - Frontend patterns → frontend.mdc
   - Workflow changes → workflow.mdc

**Checklist:**

- [ ] Learnings reviewed
- [ ] Rule updates identified
- [ ] Appropriate files updated
- [ ] References maintained

---

### 5. Verify Rules Structure

**Check all files:**

```bash
# Verify all rules files exist
ls -la .cursor/rules/

# Check file sizes
wc -l .cursor/rules/*.mdc

# Verify references work
grep -r "\.mdc" .cursor/rules/
```

**Checklist:**

- [ ] All files exist and are readable
- [ ] File sizes reasonable (<500 lines each)
- [ ] References work correctly
- [ ] No broken links

---

### 6. Commit Changes

**Commit message format:**

```
docs(cursor-rules): [action description]

[Detailed description of changes]

Examples:
- Split main.mdc into backend/frontend/workflow
- Add backend-specific patterns from Phase 4 learnings
- Update workflow rules with fix batch system
```

**Checklist:**

- [ ] Changes committed
- [ ] Commit message follows format
- [ ] Changes tested (Cursor can read rules)

---

## Common Scenarios

### Scenario 1: Main File Too Long

**Situation:** main.mdc is 700+ lines, hard to navigate

**Action:**

1. Run `/cursor-rules check` to confirm
2. Run `/cursor-rules split` to split into sections
3. Update main.mdc with references
4. Verify all files work

**Result:** Organized rules, easier to maintain

---

### Scenario 2: Adding Backend Rules

**Situation:** Starting backend development, need backend-specific rules

**Action:**

1. Run `/cursor-rules add-backend`
2. Extract backend sections from main.mdc
3. Add backend-specific patterns
4. Update main.mdc to reference backend.mdc

**Result:** Backend rules file created, main file cleaner

---

### Scenario 3: Update from Learnings

**Situation:** Phase 4 complete, new patterns discovered

**Action:**

1. Run `/int-opp` to capture learnings
2. Run `/cursor-rules update-from-learnings`
3. Review suggested updates
4. Apply updates to appropriate files

**Result:** Rules reflect latest project patterns

---

## Tips

### File Size Guidelines

- **Main file:** Keep < 500 lines (core project rules)
- **Domain files:** Keep < 300 lines each (backend/frontend)
- **Workflow file:** Keep < 400 lines (processes)

### When to Split

- File > 500 lines
- Multiple distinct domains
- Hard to navigate
- Want domain-specific rules

### Reference Strategy

- Main file references split files
- Split files are self-contained
- Use clear section headers
- Link back to main when needed

### Maintenance

- Update rules after each phase
- Review file sizes periodically
- Consolidate if files get too small
- Keep references up-to-date

---

## Reference

**Rules Files:**

- `.cursor/rules/main.mdc` - Core project rules
- `.cursor/rules/backend.mdc` - Backend-specific rules
- `.cursor/rules/frontend.mdc` - Frontend-specific rules
- `.cursor/rules/workflow.mdc` - Workflow processes

**Related Commands:**

- `/int-opp` - Capture phase learnings (run before updating rules)
- `/pr --phase [N]` - Phase completion and PR workflow
- `/post-pr` - Post-merge documentation

**Documentation:**

- Phase learnings: `docs/maintainers/planning/notes/opportunities/internal/work-prod/`
- Dev-infra improvements: `docs/maintainers/planning/notes/opportunities/internal/dev-infra/dev-infra-improvements-*.md`

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active  
**Next:** Use after `/int-opp` to keep rules current with project evolution

--- End Command ---
