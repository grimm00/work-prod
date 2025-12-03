# Projects Feature - Phase 5: Projects API - Import from JSON

**Phase:** 5 - Projects API - Import from JSON (Backend + CLI)  
**Duration:** 1 day  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 4 complete

---

## 📋 Overview

Phase 5 implements bulk import functionality to load the 59 existing projects from the inventory POC data. This phase creates a POST /api/projects/import endpoint and a CLI command to import from JSON. By the end, all 59 projects are loaded into the database.

**Success Definition:** Can import all 59 projects from classifications.json with one command.

---

## 🎯 Goals

1. **POST /api/projects/import Endpoint** - Bulk import from JSON
2. **Data Mapping** - Map inventory POC format to Project model
3. **Duplicate Handling** - Skip or update existing projects
4. **CLI Import Command** - `proj import <file>`
5. **Import Success** - All 59 projects loaded correctly

---

## 📝 Tasks

### TDD Flow

#### 1. Write Import Tests (TDD - RED)
- [ ] Test import single project from JSON
- [ ] Test import multiple projects
- [ ] Test duplicate handling (skip existing)
- [ ] Test invalid JSON returns 400
- [ ] Test import statistics in response

#### 2. Implement Import Endpoint (TDD - GREEN)
- [ ] Add POST /api/projects/import route:
  ```python
  @projects_bp.route('/projects/import', methods=['POST'])
  def import_projects():
      data = request.get_json()
      
      imported = 0
      skipped = 0
      errors = []
      
      for project_data in data.get('projects', []):
          try:
              # Check if already exists
              existing = Project.query.filter_by(
                  remote_url=project_data.get('remote_url')
              ).first()
              
              if existing:
                  skipped += 1
                  continue
              
              # Create new project
              project = Project(
                  name=project_data['name'],
                  path=project_data.get('path'),
                  organization=project_data.get('organization'),
                  classification=project_data.get('classification'),
                  status=project_data.get('status', 'active'),
                  description=project_data.get('description'),
                  remote_url=project_data.get('remote_url')
              )
              db.session.add(project)
              imported += 1
          except Exception as e:
              errors.append({'project': project_data.get('name'), 'error': str(e)})
      
      db.session.commit()
      
      return jsonify({
          'imported': imported,
          'skipped': skipped,
          'errors': errors
      }), 201
  ```

#### 3. Create Data Mapping Script
- [ ] Create `scripts/map_inventory_to_projects.py`:
  - Read `scripts/inventory/data/classifications-merged.json`
  - Map to Project model format
  - Output projects.json for import

#### 4. Write Mapping Tests
- [ ] Test mapping inventory format to Project format
- [ ] Test all 59 projects map correctly
- [ ] Test special cases (missing fields, etc.)

#### 5. Implement CLI Import
- [ ] Add `proj import <file>` command:
  ```python
  def import_projects(filename):
      with open(filename, 'r') as f:
          data = json.load(f)
      
      resp = requests.post(f"{API_BASE}/projects/import", json=data)
      
      if resp.status_code == 201:
          stats = resp.json()
          print(f"✓ Imported: {stats['imported']}")
          print(f"⊘ Skipped: {stats['skipped']}")
          if stats['errors']:
              print(f"✗ Errors: {len(stats['errors'])}")
      else:
          print(f"✗ Import failed: {resp.json()}")
  ```

#### 6. Execute Full Import
- [ ] Run mapping script to generate projects.json
- [ ] Import via CLI: `./proj import projects.json`
- [ ] Verify all 59 projects in database
- [ ] Verify classifications match expectations

---

## ✅ Completion Criteria

- [ ] Import endpoint works for bulk data
- [ ] Duplicate detection prevents re-imports
- [ ] All 59 projects from inventory imported successfully
- [ ] Import statistics accurate
- [ ] Tests pass with coverage > 80%
- [ ] CLI import command works
- [ ] Can list all imported projects

---

## 📦 Deliverables

1. POST /api/projects/import endpoint
2. Data mapping script
3. CLI import command
4. Mapped projects.json file
5. Import tests
6. Documentation of import process

---

## 💡 Import Process

### Step 1: Map Data
```bash
cd scripts
python map_inventory_to_projects.py \
  inventory/data/classifications-merged.json \
  projects.json
```

### Step 2: Import via CLI
```bash
cd project_cli
./proj import ../projects.json
```

### Step 3: Verify
```bash
./proj list
# Should show all 59 projects
```

### curl Example
```bash
curl -X POST http://localhost:5000/api/projects/import \
  -H "Content-Type: application/json" \
  -d @projects.json | jq
```

---

## 📊 Expected Import Results

- **Total Projects:** 59
- **Work Projects:** ~25
- **Learning Projects:** ~17 (with learning_type classification)
- **Personal Projects:** ~17

---

**Last Updated:** 2025-12-02  
**Status:** 🔴 Not Started  
**Next:** Begin after Phase 4 complete
