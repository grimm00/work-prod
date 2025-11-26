# Planning Structure Guide

**Purpose:** Guide for creating feature plans, lesson outlines, and exercise plans based on ADRs  
**Status:** 📋 Handoff Documentation  
**Last Updated:** 2025-11-21

---

## 🎯 Overview

This guide explains how to create planning documents that translate Architecture Decision Records (ADRs) into actionable learning content. Planning follows a three-phase approach: **Planning → Content Creation → Review & Refinement**.

**Reference:** See `nodejs/docs/maintainers/planning/features/stage-0-fundamentals/` for complete examples

---

## 📊 Planning Workflow

### Process Flow

```
ADRs (Decisions)
    ↓
Feature Plan (High-level roadmap)
    ↓
Lesson Outline (Detailed lesson breakdown)
    ↓
Exercise Plan (Hands-on practice)
    ↓
Content Creation (Actual lessons and exercises)
```

### Phase Structure

**Phase 1: Planning**
- Feature plan
- Lesson template
- Lesson outline
- Exercise plan

**Phase 2: Content Creation**
- Create lessons based on outline
- Create exercises based on plan
- Create setup guides

**Phase 3: Review & Refinement**
- Review content
- Refine based on feedback
- Finalize materials

---

## 📋 Feature Plan Template

**Purpose:** High-level roadmap for a learning stage or feature

**Location:** `docs/maintainers/planning/features/[feature-name]/feature-plan.md`

**Template:**

```markdown
# [Feature Name] - Feature Plan

**Purpose:** [Brief description]  
**Status:** 🟡 Planned / 🟢 In Progress / ✅ Complete  
**Last Updated:** [Date]

---

## 🎯 Feature Description

[Overview of what this feature/stage covers]

**Reference:** 
- [Roadmap link] - Overall learning strategy
- [ADR link] - Decision that defines this feature

---

## 📚 Learning Goals

By the end of this feature, learners will:

- [Learning goal 1]
- [Learning goal 2]
- [Learning goal 3]

---

## ✅ Success Criteria

This feature is considered complete when:

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## 📋 Content Outline

**Reference:** [ADR that defines topics]

### 1. [Topic 1]

- [Sub-topic 1]
- [Sub-topic 2]

### 2. [Topic 2]

- [Sub-topic 1]
- [Sub-topic 2]

---

## 🔗 Dependencies

**Prerequisites:**
- [Prerequisite 1]
- [Prerequisite 2]

**Informs:**
- [What this feature enables]

---

## 📅 Implementation Plan

### Phase 1: Planning
- [ ] Create feature plan
- [ ] Create lesson outline
- [ ] Create exercise plan

### Phase 2: Content Creation
- [ ] Create lessons
- [ ] Create exercises
- [ ] Create setup guides

### Phase 3: Review & Refinement
- [ ] Review content
- [ ] Refine based on feedback
- [ ] Finalize materials

---

## 📖 Related Documents

- [Lesson Outline](lesson-outline.md)
- [Exercise Plan](exercise-plan.md)
- [Status and Next Steps](status-and-next-steps.md)
```

---

## 📚 Lesson Outline Template

**Purpose:** Detailed breakdown of lessons for a feature/stage

**Location:** `docs/maintainers/planning/features/[feature-name]/lesson-outline.md`

**Template:**

```markdown
# [Feature Name] - Detailed Lesson Outline

**Purpose:** Detailed breakdown of lessons  
**Status:** 📋 Planning / ✅ Complete  
**Last Updated:** [Date]

---

## 🎯 Overview

This document provides a detailed lesson breakdown based on ADR topics and lesson structure requirements.

**Reference Documents:**
- [ADR 0002: Stage Structure and Scope](../../../decisions/0002-stage-structure-and-scope.md) - Topics
- [ADR 0006: Content Delivery and Structure](../../../decisions/0006-content-delivery-and-structure.md) - Lesson structure
- [Lesson Template](lesson-template.md) - Standard format

---

## 📚 Lesson Organization

**Structure:** [Hub-and-spoke / Linear / Other]  
**Naming:** [Sequential numbering pattern]  
**Target Length:** [X-Y minutes per lesson]  
**Total Lessons:** [Number] lessons covering [number] topics

---

## 📋 Lesson Breakdown

### Lesson [XX]: [Lesson Title]

**Filename:** `[XX]-[kebab-case-title].md`  
**Topic:** [Topic from ADR]  
**Estimated Time:** [X-Y minutes] ([X min reading, Y min exercises])

**Learning Objectives:**
- [Objective 1]
- [Objective 2]
- [Objective 3]

**Prerequisites:**
- [Prerequisite 1]
- [Prerequisite 2]

**Key Concepts:**
- [Concept 1]
- [Concept 2]
- [Concept 3]

**Exercise Suggestions:**
- [Exercise idea 1]
- [Exercise idea 2]

**Dependencies:**
- [Lesson dependency 1]
- [Lesson dependency 2]

---

[Repeat for each lesson]

---

## 🔗 Lesson Dependencies

**Dependency Graph:**
- Lesson 01 → Lesson 02
- Lesson 02 → Lesson 03
- Lesson 03 → Lesson 04, Lesson 05

---

## 📊 Progress Tracking

- [ ] Lesson 01 planned
- [ ] Lesson 02 planned
- [ ] Lesson 03 planned
```

---

## 🎯 Exercise Plan Template

**Purpose:** Detailed exercise planning for hands-on practice

**Location:** `docs/maintainers/planning/features/[feature-name]/exercise-plan.md`

**Template:**

```markdown
# [Feature Name] - Exercise Plan

**Purpose:** Detailed exercise planning  
**Status:** 📋 Planning / ✅ Complete  
**Last Updated:** [Date]

---

## 🎯 Overview

This document provides a comprehensive exercise plan following ADR 0004 guidelines.

**Reference Documents:**
- [ADR 0004: Learning Materials and Exercises](../../../decisions/0004-learning-materials-and-exercises.md) - Exercise structure
- [Lesson Outline](lesson-outline.md) - Lesson breakdown
- [Lesson Template](lesson-template.md) - Standard format

---

## 📚 Exercise Organization

**Structure:** [Organization pattern]  
**Naming:** `exercise-[X.Y]-[descriptive-name].md`  
**Type:** [Guided / Self-directed / Mixed]  
**Focus:** [Concept introduction / Application / Integration]  
**Verification:** [Self-assessment / Automated tests / Manual checks]  
**Solutions:** [Provided / Not provided / Partial]

---

## 📋 Exercise Breakdown by Lesson

### Lesson [XX]: [Lesson Title]

**Exercises:** [Number] exercises

#### Exercise [X.Y]: [Exercise Name]

**Filename:** `exercise-[X.Y]-[kebab-case-name].md`  
**Objective:** [What learner will achieve]  
**Duration:** [X-Y minutes]  
**Difficulty:** [Beginner / Intermediate / Advanced]  
**Prerequisites:** [Prerequisites]

**Learning Objectives:**
- [Objective 1]
- [Objective 2]

**Instructions:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Requirements:**
- [Requirement 1]
- [Requirement 2]

**Verification:**
- **Self-Assessment:**
  - [ ] [Check 1]
  - [ ] [Check 2]
- **Automated Tests:**
  - [Test description]
- **Manual Check:**
  - [Check description]

**Hints:**
- [Hint 1]
- [Hint 2]

**Key Learnings:**
- [Learning 1]
- [Learning 2]

**Next Steps:**
[Link to next exercise or lesson]

---

[Repeat for each exercise]

---

## 📊 Exercise Statistics

**Total Exercises:** [Number]  
**By Difficulty:**
- Beginner: [Number]
- Intermediate: [Number]
- Advanced: [Number]

**By Type:**
- Concept Introduction: [Number]
- Application: [Number]
- Integration: [Number]

---

## 🔗 Exercise Dependencies

**Dependency Graph:**
- Exercise 0.1 → Exercise 0.2
- Exercise 0.2 → Exercise 0.3
```

---

## 📝 Lesson Template

**Purpose:** Standard format for all lessons

**Location:** `docs/maintainers/planning/features/[feature-name]/lesson-template.md`

**Key Sections:**

1. **Header** - Title, purpose, status
2. **Overview** - Brief introduction
3. **Learning Objectives** - What learners will achieve
4. **Prerequisites** - Required knowledge
5. **Key Concepts** - Main topics covered
6. **Content** - Detailed explanations
7. **Examples** - Code examples
8. **Exercises** - Links to exercises
9. **Summary** - Key takeaways
10. **Next Steps** - What comes next
11. **References** - Additional resources

**Reference:** See `nodejs/docs/maintainers/planning/features/stage-0-fundamentals/lesson-template.md` for complete template

---

## 🔄 Planning Process

### Step 1: Review ADRs

**Before Planning:**

1. **Review Relevant ADRs** - Understand what decisions were made
2. **Identify Topics** - Extract topics from ADR 0002 (or equivalent)
3. **Understand Structure** - Review ADR 0006 (or equivalent) for lesson structure
4. **Review Exercise Guidelines** - Understand ADR 0004 (or equivalent) for exercises

**Key ADRs to Review:**

- **ADR 0001:** Learning Vision and Competency - Target level
- **ADR 0002:** Stage Structure and Scope - Topics
- **ADR 0004:** Learning Materials and Exercises - Exercise structure
- **ADR 0006:** Content Delivery and Structure - Lesson structure

---

### Step 2: Create Feature Plan

**Feature Plan Should Include:**

1. **Learning Goals** - What learners will achieve
2. **Content Outline** - Topics from ADR
3. **Success Criteria** - How to measure completion
4. **Dependencies** - Prerequisites and what it enables
5. **Implementation Plan** - Phases and tasks

**Example:**

```markdown
## 📋 Content Outline (Per ADR 0002)

**Reference:** [ADR 0002: Stage Structure and Scope](../../../decisions/0002-stage-structure-and-scope.md)

### 1. Node.js Overview and Architecture

- V8 JavaScript engine
- Event loop and non-blocking I/O
- Node.js runtime model
- Architecture overview
```

---

### Step 3: Create Lesson Outline

**Lesson Outline Should Include:**

1. **Lesson Organization** - Structure, naming, length
2. **Lesson Breakdown** - Each lesson with:
   - Filename
   - Topic
   - Learning objectives
   - Prerequisites
   - Key concepts
   - Exercise suggestions
   - Dependencies

**Example:**

```markdown
### Lesson 01: Introduction to Node.js

**Filename:** `01-introduction-to-nodejs.md`  
**Topic:** Node.js overview and architecture  
**Estimated Time:** 20-25 minutes (10 min reading, 10-15 min exercises)

**Learning Objectives:**
- Understand what Node.js is and its role
- Learn about Node.js architecture
- Understand Node.js vs. browser JavaScript

**Prerequisites:**
- Basic JavaScript knowledge
- Development environment set up

**Key Concepts:**
- Node.js as a JavaScript runtime
- V8 JavaScript engine
- Event loop and non-blocking I/O

**Exercise Suggestions:**
- Verify Node.js installation
- Run a simple "Hello, Node.js!" script
```

---

### Step 4: Create Exercise Plan

**Exercise Plan Should Include:**

1. **Exercise Organization** - Structure, naming, type
2. **Exercise Breakdown** - Each exercise with:
   - Filename
   - Objective
   - Duration
   - Difficulty
   - Prerequisites
   - Instructions
   - Requirements
   - Verification methods
   - Hints
   - Key learnings

**Example:**

```markdown
#### Exercise 0.1: Verify Node.js Installation

**Filename:** `exercise-0.1-verify-nodejs-installation.md`  
**Objective:** Verify Node.js installation and understand basic CLI usage  
**Duration:** 5-7 minutes  
**Difficulty:** Beginner

**Learning Objectives:**
- Verify Node.js is installed correctly
- Check Node.js and npm versions
- Understand basic Node.js CLI commands

**Instructions:**
1. Open your terminal
2. Run `node --version` to check Node.js version
3. Run `npm --version` to check npm version
4. Run `node -e "console.log('Node.js is working!')"`

**Verification:**
- **Self-Assessment:**
  - [ ] Node.js version command works
  - [ ] npm version command works
  - [ ] Inline code execution works
```

---

## 📊 Planning Best Practices

### 1. Reference ADRs

- Always reference ADRs in planning documents
- Link to specific ADRs that inform decisions
- Show how planning implements ADR decisions

### 2. Be Specific

- Use clear, actionable language
- Break down complex topics
- Provide concrete examples

### 3. Consider Dependencies

- Map lesson dependencies
- Map exercise dependencies
- Ensure logical progression

### 4. Estimate Time

- Provide time estimates for lessons
- Provide time estimates for exercises
- Consider reading vs. practice time

### 5. Plan for Verification

- Define verification methods
- Consider self-assessment
- Consider automated tests
- Consider manual checks

### 6. Provide Hints

- Include hints for exercises
- Don't give away solutions
- Guide learners to discover answers

---

## 🔗 From Planning to Content

**Process:**

1. **Complete Planning** - Feature plan, lesson outline, exercise plan
2. **Review Planning** - Ensure completeness and consistency
3. **Create Content** - Write lessons and exercises based on plans
4. **Reference Plans** - Link content back to planning documents

**Example Flow:**

```
Feature Plan: "Stage 0: Fundamentals"
    ↓
Lesson Outline: "8 lessons covering 7 topics"
    ↓
Exercise Plan: "17 exercises across 8 lessons"
    ↓
Content Creation: "Write lessons and exercises"
```

---

## 📖 Example Planning Documents

**Reference:** See `nodejs/docs/maintainers/planning/features/stage-0-fundamentals/` for complete examples:

- `feature-plan.md` - Complete feature plan
- `lesson-outline.md` - Complete lesson outline
- `exercise-plan.md` - Complete exercise plan
- `lesson-template.md` - Lesson template
- `status-and-next-steps.md` - Progress tracking

---

## ✅ Planning Checklist

Before moving to content creation, ensure:

- [ ] Feature plan is complete
- [ ] Lesson outline is complete
- [ ] Exercise plan is complete
- [ ] All ADRs are referenced
- [ ] Dependencies are mapped
- [ ] Time estimates are provided
- [ ] Verification methods are defined
- [ ] Planning documents are reviewed

---

## 📚 Related Documentation

- [Main Handoff Document](javascript-learning-project-handoff.md) - Overall process
- [Research Template Guide](research-template-guide.md) - How to create research
- [ADR Template Guide](adr-template-guide.md) - How to create ADRs
- [Node.js Planning Examples](../../planning/features/stage-0-fundamentals/) - Complete examples

---

**Last Updated:** 2025-11-21  
**Status:** 📋 Handoff Documentation  
**Next:** Read JavaScript-Specific Adaptations to learn how to adapt this process for JavaScript learning

