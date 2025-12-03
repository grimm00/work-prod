# Projects Feature - Phase 4: Projects API - Search & Filter

**Phase:** 4 - Projects API - Search & Filter (Backend + CLI)  
**Duration:** 1.5 days  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 3 complete

---

## 📋 Overview

Phase 4 adds search and filtering capabilities to the Projects API. This phase implements query parameters for filtering by organization, classification, status, and text search. By the end, you can find specific projects quickly via API and CLI.

**Success Definition:** Can search and filter projects by multiple criteria via curl/CLI.

---

## 🎯 Goals

1. **Query Parameters** - GET /api/projects?status=active&org=work
2. **Text Search** - Search project names and descriptions
3. **Multiple Filters** - Combine filters (AND logic)
4. **CLI Search/Filter** - `proj list --status active --org work`
5. **Performance** - Fast queries with proper indexing

---

## 📝 Tasks

### TDD Flow

#### 1. Write Filter Tests (TDD - RED)
- [ ] Test filter by status: GET /api/projects?status=active
- [ ] Test filter by organization: GET /api/projects?organization=work
- [ ] Test filter by classification: GET /api/projects?classification=primary
- [ ] Test multiple filters: GET /api/projects?status=active&organization=work
- [ ] Test invalid filter values return all projects (or 400)

#### 2. Implement Filtering (TDD - GREEN)
- [ ] Update GET /api/projects to accept query parameters
- [ ] Build dynamic query with filters:
  ```python
  @projects_bp.route('/projects', methods=['GET'])
  def get_projects():
      query = Project.query
      
      # Apply filters
      if 'status' in request.args:
          query = query.filter_by(status=request.args['status'])
      if 'organization' in request.args:
          query = query.filter_by(organization=request.args['organization'])
      if 'classification' in request.args:
          query = query.filter_by(classification=request.args['classification'])
      
      projects = query.all()
      return jsonify({
          'projects': [p.to_dict() for p in projects],
          'total': len(projects)
      }), 200
  ```

#### 3. Write Search Tests (TDD - RED)
- [ ] Test search by name: GET /api/projects?search=work
- [ ] Test search is case-insensitive
- [ ] Test search matches partial names
- [ ] Test search in description field

#### 4. Implement Text Search (TDD - GREEN)
- [ ] Add search parameter:
  ```python
  if 'search' in request.args:
      search_term = f"%{request.args['search']}%"
      query = query.filter(
          (Project.name.ilike(search_term)) |
          (Project.description.ilike(search_term))
      )
  ```
- [ ] Add index on name field for performance

#### 5. Enhance CLI
- [ ] Add filter options to `proj list`:
  ```python
  ./proj list --status active
  ./proj list --org work
  ./proj list --search "productivity"
  ./proj list --status active --org work  # Multiple filters
  ```

---

## ✅ Completion Criteria

- [ ] Filtering by status, organization, classification works
- [ ] Text search works (case-insensitive, partial match)
- [ ] Multiple filters combine correctly (AND logic)
- [ ] Tests pass with coverage > 80%
- [ ] CLI supports filter flags
- [ ] Performance acceptable (< 100ms for 100 projects)

---

## 📦 Deliverables

1. Enhanced GET /api/projects with query parameters
2. Search functionality
3. CLI with filter flags
4. Performance optimization (indexes)
5. Filter tests

---

## 💡 curl Examples

```bash
# Filter by status
curl "http://localhost:5000/api/projects?status=active" | jq

# Filter by organization
curl "http://localhost:5000/api/projects?organization=work" | jq

# Multiple filters
curl "http://localhost:5000/api/projects?status=active&organization=work" | jq

# Text search
curl "http://localhost:5000/api/projects?search=productivity" | jq

# Complex query
curl "http://localhost:5000/api/projects?status=active&classification=primary&search=work" | jq
```

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Next:** Begin after Phase 3 complete
