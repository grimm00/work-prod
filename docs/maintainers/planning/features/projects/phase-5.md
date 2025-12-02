# Projects Feature - Phase 5: Search and Filtering

**Phase:** 5 - Search and Filtering  
**Duration:** 2 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 4 complete

---

## 📋 Overview

Phase 5 adds search and filtering capabilities to quickly find projects in a large list. With 59+ projects, users need efficient ways to locate specific projects by name, organization, classification, or learning type.

**Success Definition:** Can search and filter 100+ projects in under 1 second.

---

## 🎯 Goals

1. **Full-Text Search** - SQLite FTS5 for fast search
2. **Multi-Faceted Filtering** - By organization, classification, status, learning_type
3. **Sort Options** - By name, updated_at, status
4. **Search UI** - Debounced search bar with results highlighting
5. **Filter UI** - Filter chips with clear/reset

---

## 📝 TDD Tasks

### Backend Search

- [ ] Set up SQLite FTS5 virtual table
- [ ] Write search endpoint tests
  - Test full-text search
  - Test filtering by organization
  - Test filtering by classification
  - Test filtering by status
  - Test filtering by learning_type
  - Test combined filters
  - Test sorting options
- [ ] Implement GET /api/projects/search
  - Query params: `q`, `organization`, `classification`, `status`, `learning_type`, `sort`
  - Return filtered and sorted results
  - Performance: < 100ms for 100+ projects

### Frontend Search UI

- [ ] Write search UI tests
- [ ] Create SearchBar component with debounced input
- [ ] Create FilterChips component
- [ ] Add learning project badges
- [ ] Add sort dropdown
- [ ] Integrate with ProjectList

### Manual Testing

- [ ] Search for project by name
- [ ] Filter by organization
- [ ] Filter by learning type
- [ ] Combine multiple filters
- [ ] Test with 100+ projects (seed data)
- [ ] Verify performance (< 1 second)

---

## ✅ Completion Criteria

- [ ] FTS5 search configured
- [ ] Search endpoint returns results in < 100ms
- [ ] Search UI with debounce working
- [ ] Filters working (org, classification, status, learning_type)
- [ ] Sort options working
- [ ] Learning project badges visible
- [ ] All tests passing

---

## 📦 Deliverables

- SQLite FTS5 configuration
- GET /api/projects/search endpoint
- SearchBar component
- FilterChips component
- Learning project badges
- Backend and frontend tests

---

## 🔗 Dependencies

**Prerequisites:** Phase 4 complete  
**Blocks:** Phase 6

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started


