# Hub-and-Spoke Documentation Pattern

**Purpose:** Document the hub-and-spoke organization pattern used throughout work-prod  
**Status:** ✅ Active  
**Last Updated:** 2025-12-16

---

## Overview

The hub-and-spoke pattern organizes documentation into:
- **Hubs:** Central README.md files that provide navigation and overview
- **Spokes:** Detailed documents linked from hubs

This pattern scales well and reduces cognitive load by providing clear entry points.

---

## Pattern Structure

### Basic Structure

```
directory/
├── README.md           # HUB - Entry point with Quick Links
├── document-1.md       # SPOKE - Detailed content
├── document-2.md       # SPOKE - Detailed content
└── subdirectory/
    ├── README.md       # SUB-HUB - Entry point for subdirectory
    └── details.md      # SPOKE - Subdirectory details
```

### Hub Template

```markdown
# [Directory Name]

**Purpose:** [One-line description]  
**Status:** [Status indicator]  
**Last Updated:** [YYYY-MM-DD]

---

## 📋 Quick Links

### [Category 1]

- **[Document Name](document.md)** - Brief description (Status)
- **[Another Doc](another.md)** - Brief description (Status)

### [Category 2]

- **[More Docs](more.md)** - Description

---

## 📊 Overview

[Brief overview of what's in this directory]

---

## 🔗 Related

- **[Parent Hub](../README.md)** - Link back to parent
- **[Related Resource](path/to/resource.md)** - Related documentation

---

**Last Updated:** [YYYY-MM-DD]
```

---

## Examples from Work-Prod

### Example 1: Features Hub

**File:** `docs/maintainers/planning/features/README.md`

```markdown
# Features Planning

## 📋 Quick Links

### Active Features

- **[Projects](projects/README.md)** - Project management (✅ MVP Complete)

### Planned Features

- **[Daily Focus](daily-focus/README.md)** - Daily task management (🔴 Not Started)
```

### Example 2: Fix Tracking Hub

**File:** `docs/maintainers/planning/features/projects/fix/README.md`

```markdown
# Fix Tracking

## 📋 Quick Links

### Active PRs

- **[PR #2](pr02/README.md)** - Phase 1 fixes (🟡 Partial)
- **[PR #12](pr12/README.md)** - Phase 4 fixes (✅ Complete)

### Cross-PR Batches

- **[Cross-PR Batches](cross-pr/README.md)** - Batches across PRs

### Archived

- **[Archived](archived/README.md)** - Completed PRs
```

### Example 3: Reflections Hub

**File:** `docs/maintainers/planning/notes/reflections/README.md`

```markdown
# Reflections

## 📋 Quick Links

### Project-Wide

- **[MVP Complete](reflection-2025-12-07-mvp-complete.md)** - Full reflection
- **[Release Complete](reflection-2025-12-07-release-complete.md)** - Release reflection

### Phase-Specific

- **[Phase 6 CLI](reflection-phase6-cli-enhancement-2025-12-06.md)** - CLI phase
```

---

## Best Practices

### 1. Quick Links First

Always put the Quick Links section at the top after the header:

```markdown
## 📋 Quick Links

### [Category]

- **[Link](path)** - Description (Status)
```

### 2. Use Status Indicators

Include status in link descriptions:
- `(✅ Complete)` - Done
- `(🟠 In Progress)` - Active work
- `(🟡 Planned)` - Not started
- `(🔴 Not Started)` - Waiting

### 3. Bidirectional Links

Hubs link to spokes, spokes link back to hubs:

**In Hub:**
```markdown
- **[Document](document.md)** - Description
```

**In Spoke:**
```markdown
## 🔗 Related

- **[Back to Hub](README.md)** - Parent directory
```

### 4. Consistent Structure

Use the same structure across all hubs:
1. Title and metadata
2. Quick Links
3. Overview/Summary
4. Related links
5. Footer with date

### 5. Progressive Depth

- **Level 1:** Quick Links (navigate fast)
- **Level 2:** Overview (understand context)
- **Level 3:** Spoke documents (full details)

---

## When to Create Hubs

Create a hub when:
- Directory has 3+ documents
- Directory will grow over time
- Multiple people need to navigate the content
- Content has distinct categories

Don't create a hub when:
- Only 1-2 simple documents
- Content is temporary
- No navigation benefit

---

## Anti-Patterns

### 1. Deep Nesting Without Hubs

❌ Bad:
```
features/projects/phases/implementation/details/
```

✅ Good:
```
features/projects/
├── README.md        # Hub for projects
├── phases/
│   └── README.md    # Sub-hub for phases
```

### 2. Missing Quick Links

❌ Bad:
```markdown
# Directory

Here is some content about this directory...
[lots of text]
Links are buried at the bottom.
```

✅ Good:
```markdown
# Directory

## 📋 Quick Links

- **[Important](important.md)** - Key document

## Overview

Brief context...
```

### 3. Orphan Documents

❌ Bad: Document not linked from any hub  
✅ Good: Every document linked from at least one hub

---

## Scale Benefits

| Project Size | Without Pattern | With Pattern |
|--------------|----------------|--------------|
| Small (10 docs) | OK | Slight overhead |
| Medium (50 docs) | Hard to navigate | Easy navigation |
| Large (100+ docs) | Very difficult | Scales well |

Work-prod has 100+ documentation files and the pattern keeps everything navigable.

---

## Related

- **[Feature Planning Example](feature-planning-example.md)** - Real-world hub usage
- **[Examples Hub](README.md)** - Back to examples

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active

