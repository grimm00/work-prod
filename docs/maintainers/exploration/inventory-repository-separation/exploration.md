# Inventory Repository Separation - Exploration

**Status:** 🟠 Exploration  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 🎯 What Are We Exploring?

Deep dive into the inventory system separation to:
1. Finalize repository structure and naming
2. Evaluate git history preservation strategies
3. Define script organization patterns
4. Design configuration management approach
5. Plan integration patterns with work-prod
6. Prioritize technical debt items for resolution

---

## 🤔 Why Explore This?

**Context from Transition Plan:**

The inventory system (scripts in `scripts/inventory/`) is being separated into its own repository. Phase 1 (documentation) is complete, but several implementation questions remain before beginning Phase 2 (create repository).

**Key Drivers:**
- Periodic refresh requirement (different cadence than main app)
- Different purpose (data gathering vs. productivity tracking)
- Technical debt isolation
- Independent evolution
- Potential reusability for others

**Reference:** [Transition Plan](../../planning/infrastructure/inventory-repository-separation/transition-plan.md)

---

## 💡 Initial Thoughts

### Repository Naming Options

| Option | Pros | Cons |
|--------|------|------|
| `project-inventory` | Clear, descriptive | May conflict with generic naming |
| `inventory-tools` | Emphasizes tooling nature | Less specific |
| `project-scanner` | Describes functionality | Doesn't cover all features |
| `repo-inventory` | Specific to repos | Limits future expansion |
| `project-discovery` | Forward-looking | Vague |

**Leaning toward:** `project-inventory` or `inventory-tools`

### Script Organization

**Current state:** Flat structure in `scripts/inventory/`
```
inventory/
├── analyze-tech-stack.py
├── classify-projects.py
├── deduplicate-projects.py
├── fetch-github-repos.sh
├── generate-report.py
├── scan-local-projects.sh
└── README.md
```

**Possible improvements:**
```
inventory/
├── scanners/
│   ├── github_scanner.py
│   ├── local_scanner.sh
│   └── __init__.py
├── analyzers/
│   ├── tech_stack.py
│   ├── classifier.py
│   └── __init__.py
├── processors/
│   ├── deduplicator.py
│   └── reporter.py
├── config/
│   └── default.yaml
├── orchestrate.py         # Master script
├── requirements.txt
└── README.md
```

### Git History Options

| Strategy | Complexity | History Preserved |
|----------|------------|-------------------|
| Copy files | Low | No |
| git subtree split | Medium | Yes |
| git filter-repo | High | Yes, complete |
| Fresh start + reference | Low | Reference only |

**Consideration:** Is history preservation important enough to warrant complexity?

---

## 🔍 Key Questions

- [ ] **Q1:** What should the new repository be named? What's the long-term vision?
- [ ] **Q2:** Is preserving git history worth the complexity? What's the real value?
- [ ] **Q3:** Should scripts be reorganized in the new repo or after migration?
- [ ] **Q4:** What configuration management pattern works best for portable scripts?
- [ ] **Q5:** How should the new repo integrate with work-prod's Projects API?
- [ ] **Q6:** Which technical debt items are critical vs. nice-to-have?
- [ ] **Q7:** Should we add CLI tooling (argparse/click) to scripts?

---

## 📊 Technical Debt Inventory

From [POC Analysis](../../research/automation/inventory-system-poc-analysis.md):

| Issue | Priority | Effort | Notes |
|-------|----------|--------|-------|
| Hardcoded paths | HIGH | LOW | Config file needed |
| No error handling | HIGH | MEDIUM | Add try/catch, logging |
| Missing dependencies | MEDIUM | LOW | requirements.txt |
| Inconsistent output | MEDIUM | MEDIUM | Standardize JSON format |
| No master orchestrator | MEDIUM | MEDIUM | Single entrypoint |
| Shell script limitations | LOW | HIGH | Consider Python rewrite |
| No incremental mode | LOW | HIGH | Future enhancement |

**Critical for separation:** Hardcoded paths, Error handling  
**Nice for separation:** Master orchestrator, Dependencies file  
**Post-separation:** Shell rewrites, Incremental mode

---

## 🔄 Integration Patterns

### Current Integration

```
scripts/inventory/ --> data/inventory-*.json
                   --> docs/exploration/current-state-inventory.md
                   
scripts/map_inventory_to_projects.py --> projects.json
                                     --> POST /api/projects/import
```

### Post-Separation Options

**Option A: Manual Workflow**
```
project-inventory repo --> inventory-*.json (manual copy)
work-prod repo --> map_inventory_to_projects.py --> API
```

**Option B: Export to work-prod format**
```
project-inventory repo --> export command --> projects.json
work-prod repo --> POST /api/projects/import
```

**Option C: Direct API integration**
```
project-inventory repo --> API client --> POST /api/projects/import
```

**Recommended:** Start with Option A, build toward Option C

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research inventory-repository-separation --from-explore` to conduct research
3. Make decisions and update transition plan
4. After research complete, begin Phase 2 implementation

---

## 📝 Notes

### Existing Assets to Leverage

- `scripts/inventory/README.md` - Already documents scripts well
- `scripts/projects.json` - Output format already defined
- `scripts/map_inventory_to_projects.py` - Integration pattern established
- Exploration docs - Historical context preserved

### Potential Risks

1. **Breaking local workflows** - Need to update any scripts that reference inventory
2. **Losing context** - Ensure documentation links remain valid
3. **Scope creep** - Technical debt items could delay separation
4. **Testing gaps** - No automated tests for inventory scripts currently

### Success Metrics

- [ ] New repo created and functional
- [ ] All scripts work in new location
- [ ] Main repo cleaned up
- [ ] Documentation updated in both repos
- [ ] At least 3 technical debt items addressed
- [ ] Integration pattern documented

---

**Last Updated:** 2025-12-16

