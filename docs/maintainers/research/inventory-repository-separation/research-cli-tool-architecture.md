# Research: CLI Tool Architecture

**Research Topic:** Inventory Repository Separation  
**Question:** Should we create a unified CLI tool instead of just separating scripts?  
**Status:** ✅ Complete  
**Created:** 2025-12-16  
**Last Updated:** 2025-12-16

---

## 🎯 Research Question

Should we create a unified CLI tool with commands/flags instead of just separating the existing scripts? This is the **gating decision** that affects all other choices.

---

## 🔍 Research Goals

- [x] Goal 1: Evaluate effort difference between script separation vs CLI tool
- [x] Goal 2: Determine value add of CLI tool approach
- [x] Goal 3: Identify risks and tradeoffs
- [x] Goal 4: Make recommendation

---

## 📚 Research Methodology

**Sources:**
- [x] Web search: Python CLI best practices
- [x] Typer documentation (https://typer.tiangolo.com/)
- [x] Click documentation (https://click.palletsprojects.com/)
- [x] Existing work-prod CLI tool (scripts/project_cli/)

---

## 📊 Findings

### Finding 1: We Already Have CLI Experience

**Description:** The work-prod project already has a CLI tool (`scripts/project_cli/`) built with `argparse`. This demonstrates familiarity with CLI patterns and provides a template.

**Source:** Local codebase analysis

**Relevance:** Reduces learning curve - we've done this before.

---

### Finding 2: CLI Tool Effort is Moderate, Not High

**Description:** Creating a basic CLI tool with Typer or Click adds approximately 2-4 hours of work on top of script separation. The framework handles parsing, help text, and error handling.

**Estimated Effort Comparison:**

| Approach | Effort | Result |
|----------|--------|--------|
| Script separation only | 4-6 hours | Scripts in new repo, run individually |
| Basic CLI wrapper | 6-10 hours | Unified interface, better UX |
| Full-featured CLI | 12-16 hours | Commands, config, progress bars |

**Source:** Web research + existing project_cli analysis

**Relevance:** The delta is reasonable given the UX improvement.

---

### Finding 3: CLI Tool Provides Significant UX Benefits

**Description:** A unified CLI provides:
- Single entry point (`pinv` instead of 6 separate scripts)
- Consistent help system (`pinv --help`, `pinv scan --help`)
- Command completion (with shell integration)
- Progress bars and colored output (via `rich`)
- Configuration management baked in

**Source:** Web research on CLI best practices

**Relevance:** Makes the tool more professional and usable.

---

### Finding 4: Script Separation Is Minimum Viable

**Description:** Just moving scripts to a new repo works, but:
- Users must remember 6 different script names
- Each script has inconsistent argument handling
- No shared configuration
- Harder to add new functionality

**Source:** Analysis of current scripts

**Relevance:** This is the fallback option if time is constrained.

---

### Finding 5: Work-Prod Already Uses CLI Pattern

**Description:** The existing `proj` CLI tool (`scripts/project_cli/`) demonstrates the value:
- `proj list`, `proj get`, `proj create`, etc.
- Consistent interface for all operations
- Easy to add new commands
- Professional feel

**Source:** Local codebase

**Relevance:** Inventory tool should follow same pattern for consistency.

---

## 🔍 Analysis

### Option A: Script Separation Only

**Pros:**
- Fastest implementation (4-6 hours)
- No new dependencies
- Minimal changes to existing code

**Cons:**
- Poor UX (6 separate scripts)
- No shared configuration
- Inconsistent interfaces
- Harder to extend

**Best for:** Time-constrained situations

---

### Option B: Basic CLI Wrapper

**Pros:**
- Good UX (single entry point)
- Moderate effort (6-10 hours)
- Foundation for future features
- Consistent with work-prod patterns

**Cons:**
- Requires framework choice
- Slightly more initial work

**Best for:** Most situations (recommended)

---

### Option C: Full-Featured CLI

**Pros:**
- Professional tool
- All features from day one
- Best UX

**Cons:**
- Higher effort (12-16 hours)
- Scope creep risk
- May over-engineer for current needs

**Best for:** If tool will be shared widely

---

## 💡 Recommendations

### Primary Recommendation: Option B (Basic CLI Wrapper)

**Rationale:**
1. Consistent with work-prod's existing `proj` CLI pattern
2. Moderate effort with high UX payoff
3. Provides foundation for future features
4. Follows Python CLI best practices
5. Can evolve to Option C over time

### Proposed Minimum Viable Commands

```bash
pinv scan github       # Scan GitHub repos
pinv scan local        # Scan local projects
pinv analyze           # Analyze tech stack + classify
pinv dedupe            # Deduplicate results
pinv export json       # Export to JSON
pinv export api        # Push to work-prod API
```

### Implementation Approach

1. Create Python package structure with CLI entry point
2. Wrap existing scripts as subcommands
3. Add shared configuration
4. Iteratively improve each command

---

## 📋 Requirements Discovered

- [x] REQ-1: CLI tool should have single entry point command
- [x] REQ-2: Commands should mirror existing script functionality
- [x] REQ-3: Configuration should be externalized (not hardcoded)
- [x] REQ-4: Tool should be pip-installable
- [x] REQ-5: Should follow work-prod CLI patterns (argparse or modern framework)

---

## 🎯 Decision Recommendation

**Decision:** ✅ YES - Build a unified CLI tool (Option B)

**Rationale:**
1. Moderate additional effort (2-4 hours on top of separation)
2. Significant UX improvement
3. Consistent with work-prod patterns
4. Foundation for future enhancements
5. More professional tool for personal use

**Next Steps:**
1. Select CLI framework (see [research-cli-framework.md](research-cli-framework.md))
2. Define repository/package naming
3. Plan minimum viable command set
4. Begin implementation

---

**Last Updated:** 2025-12-16

