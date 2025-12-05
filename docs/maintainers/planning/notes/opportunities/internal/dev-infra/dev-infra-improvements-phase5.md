# Dev-Infra Improvements - Phase 5

**Source:** Phase 5 (Import Projects from JSON)  
**Target:** ~/Projects/dev-infra template  
**Status:** 🟡 Pending  
**Why:** Bulk import patterns, data mapping scripts, and validation improvements  
**How Discovered:** Phase 5 implementation and fix batches  
**Problem Solved:** Missing patterns for bulk operations, data transformation, and strict validation

---

## Introduction

Phase 5 introduced bulk import functionality with data mapping, which revealed several patterns that should be included in the dev-infra template. Additionally, fix batches (PR #17, #18, #19) identified improvements to validation, CLI UX, and test quality that should be templated.

---

## Pre-Project Setup

### Bulk Import Endpoint Template

- [ ] **Bulk Import Endpoint Pattern**
  - **Location:** `backend/app/api/[resource]_import.py` template
  - **Action:** Create template for bulk import endpoints with statistics
  - **Prevents/Enables:** Consistent bulk import patterns, clear statistics format
  - **Content/Example:**
    ```python
    @[resource]_bp.route('/[resource]/import', methods=['POST'])
    def import_[resource](s):
        """Bulk import [resource]s from JSON.
        
        Request body:
        {
            "[resource]s": [
                {"field1": "value1", ...},
                ...
            ]
        }
        
        Returns:
            201: Import completed with statistics
            400: Invalid JSON or request body shape
        """
        # Validate Content-Type
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        # Validate JSON
        try:
            data = request.get_json()
        except Exception:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        # Validate request body shape
        if not isinstance(data, dict):
            return jsonify({'error': 'Request body must be a JSON object'}), 400
        
        if '[resource]s' not in data:
            return jsonify({'error': f"Missing '[resource]s' field"}), 400
        
        [resource]_data = data['[resource]s']
        if not isinstance([resource]_data, list):
            return jsonify({'error': f"'[resource]s' field must be a list"}), 400
        
        # Import with statistics
        imported = 0
        skipped = 0
        errors = []
        
        for item_data in [resource]_data:
            try:
                # Check for duplicates (customize duplicate detection)
                existing = [Resource].query.filter_by(
                    unique_field=item_data.get('unique_field')
                ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Create item
                item = [Resource](**item_data)
                db.session.add(item)
                imported += 1
            except Exception as e:
                errors.append({
                    'item': item_data.get('name', 'Unknown'),
                    'error': str(e)
                })
        
        db.session.commit()
        
        return jsonify({
            'imported': imported,
            'skipped': skipped,
            'errors': errors
        }), 201
    ```
  - **Expected Impact:** Consistent bulk import patterns across projects
  - **Priority:** 🟡 MEDIUM
  - **Effort:** 🟢 LOW

---

## Project Structure

### Data Mapping Script Template

- [ ] **Data Mapping Script Template**
  - **Location:** `scripts/map_[source]_to_[target].py` template
  - **Action:** Create template for data mapping scripts
  - **Prevents/Enables:** Consistent data transformation patterns, reusable mapping logic
  - **Content/Example:**
    ```python
    #!/usr/bin/env python3
    """Map [source] data format to [target] model format.
    
    Usage:
        python map_[source]_to_[target].py input.json output.json
    """
    import json
    import sys
    from collections import defaultdict
    
    def map_[source]_to_[target](source_data):
        """Map [source] format to [target] format."""
        [target]_items = []
        seen = set()  # For deduplication
        
        for item in source_data:
            # Deduplication logic
            unique_key = item.get('unique_field')
            if unique_key in seen:
                continue
            seen.add(unique_key)
            
            # Mapping logic
            [target]_item = {
                'field1': item.get('source_field1'),
                'field2': item.get('source_field2', 'default'),
                # ... more mappings
            }
            
            [target]_items.append([target]_item)
        
        return [target]_items
    
    if __name__ == '__main__':
        if len(sys.argv) != 3:
            print("Usage: python map_[source]_to_[target].py input.json output.json")
            sys.exit(1)
        
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        
        with open(input_file, 'r') as f:
            source_data = json.load(f)
        
        [target]_items = map_[source]_to_[target](source_data)
        
        output = {'[target]s': [target]_items}
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Mapped {len([target]_items)} items")
    ```
  - **Expected Impact:** Consistent data mapping patterns, easier data migration
  - **Priority:** 🟡 MEDIUM
  - **Effort:** 🟢 LOW

---

## Configuration

### Enum Validation Pattern

- [ ] **Enum Validation Before Database Operations**
  - **Location:** `backend/app/api/[resource].py` validation section
  - **Action:** Add enum validation pattern before database operations
  - **Prevents/Enables:** Prevents invalid enum values from reaching database
  - **Content/Example:**
    ```python
    # Define valid enum values
    VALID_STATUSES = ['active', 'paused', 'completed', 'cancelled']
    VALID_CLASSIFICATIONS = ['primary', 'secondary', 'archive', 'maintenance']
    
    # Validate before database operations
    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return jsonify({'error': f"Invalid status: {data['status']}"}), 400
    
    if 'classification' in data:
        if data['classification'] not in VALID_CLASSIFICATIONS:
            return jsonify({'error': f"Invalid classification: {data['classification']}"}), 400
    ```
  - **Expected Impact:** Prevents database enum errors, clearer error messages
  - **Priority:** 🟠 HIGH
  - **Effort:** 🟢 LOW

---

## Testing Infrastructure

### Bulk Import Test Template

- [ ] **Bulk Import Test Patterns**
  - **Location:** `backend/tests/integration/api/test_[resource]_import.py` template
  - **Action:** Create test template for bulk import endpoints
  - **Prevents/Enables:** Consistent test coverage for bulk operations
  - **Content/Example:**
    ```python
    @pytest.mark.integration
    def test_import_single_item(client, app):
        """Test importing a single item."""
        response = client.post(
            '/api/[resource]/import',
            json={'[resource]s': [{'name': 'Test', 'field': 'value'}]},
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['imported'] == 1
        assert data['skipped'] == 0
        assert len(data['errors']) == 0
    
    @pytest.mark.integration
    def test_import_duplicate_skipped(client, app):
        """Test that duplicates are skipped."""
        # Create existing item
        with app.app_context():
            existing = [Resource](name='Test', unique_field='test')
            db.session.add(existing)
            db.session.commit()
        
        # Try to import duplicate
        response = client.post(
            '/api/[resource]/import',
            json={'[resource]s': [{'name': 'Test', 'unique_field': 'test'}]},
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['imported'] == 0
        assert data['skipped'] == 1
    
    @pytest.mark.integration
    def test_import_invalid_request_body_shape(client):
        """Test that non-dict request body returns 400."""
        response = client.post(
            '/api/[resource]/import',
            json=["not a dict"],
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json['error'] == 'Request body must be a JSON object'
    
    @pytest.mark.integration
    def test_import_missing_field(client):
        """Test that missing '[resource]s' field returns 400."""
        response = client.post(
            '/api/[resource]/import',
            json={'data': 'no [resource]s'},
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json['error'] == f"Missing '[resource]s' field"
    
    @pytest.mark.integration
    def test_import_non_list_field(client):
        """Test that non-list '[resource]s' field returns 400."""
        response = client.post(
            '/api/[resource]/import',
            json={'[resource]s': 'not a list'},
            content_type='application/json'
        )
        assert response.status_code == 400
        assert response.json['error'] == f"'[resource]s' field must be a list"
    ```
  - **Expected Impact:** Consistent test coverage for bulk imports
  - **Priority:** 🟡 MEDIUM
  - **Effort:** 🟢 LOW

### Data Mapping Script Test Template

- [ ] **Data Mapping Script Test Template**
  - **Location:** `backend/tests/unit/test_map_[source]_to_[target].py` template
  - **Action:** Create test template for data mapping scripts
  - **Prevents/Enables:** Testable data transformation logic
  - **Content/Example:**
    ```python
    import sys
    import importlib.util
    from pathlib import Path
    
    # Load mapping script as module
    script_path = Path(__file__).parent.parent.parent / 'scripts' / 'map_[source]_to_[target].py'
    spec = importlib.util.spec_from_file_location("map_[source]_to_[target]", script_path)
    map_module = importlib.util.module_from_spec(spec)
    sys.modules["map_[source]_to_[target]"] = map_module
    spec.loader.exec_module(map_module)
    
    def test_map_basic_item():
        """Test basic item mapping."""
        source_data = [{'source_field1': 'value1', 'source_field2': 'value2'}]
        result = map_module.map_[source]_to_[target](source_data)
        assert len(result) == 1
        assert result[0]['field1'] == 'value1'
        assert result[0]['field2'] == 'value2'
    
    def test_map_deduplication():
        """Test that duplicates are removed."""
        source_data = [
            {'unique_field': 'test', 'name': 'Test 1'},
            {'unique_field': 'test', 'name': 'Test 2'},  # Duplicate
        ]
        result = map_module.map_[source]_to_[target](source_data)
        assert len(result) == 1  # Only one after deduplication
    ```
  - **Expected Impact:** Testable data mapping logic
  - **Priority:** 🟡 MEDIUM
  - **Effort:** 🟢 LOW

---

## Documentation

### Manual Testing Guide Template Updates

- [ ] **Mandatory Manual Testing Updates in PR Validation**
  - **Location:** `.cursor/commands/pr-validation.md` template
  - **Action:** Make manual testing guide updates mandatory
  - **Prevents/Enables:** Documentation stays in sync with code
  - **Content/Example:**
    ```markdown
    ### 2. Update Manual Testing Guide (MANDATORY)
    
    **IMPORTANT:** This step is MANDATORY for all PRs. Always check and update the manual testing guide.
    
    **Process:**
    1. Review PR changes to identify new features
    2. Check if scenarios exist for new functionality
    3. Add missing scenarios using template
    4. Update header with PR number
    5. Update acceptance criteria
    
    **After updating:**
    - [ ] Scenarios added for all new functionality
    - [ ] Header updated with PR number
    - [ ] Acceptance criteria updated
    - [ ] Scenarios committed to PR branch
    ```
  - **Expected Impact:** Documentation always up-to-date
  - **Priority:** 🟠 HIGH
  - **Effort:** 🟢 LOW

---

## Development Workflow

### CLI Import Command Template

- [ ] **CLI Import Command Pattern**
  - **Location:** `scripts/[cli]/commands/import_cmd.py` template
  - **Action:** Create template for CLI import commands
  - **Prevents/Enables:** Consistent CLI import patterns
  - **Content/Example:**
    ```python
    @click.command()
    @click.argument('filename', type=click.Path(exists=True))
    def import_[resource](s(filename):
        """Import [resource]s from JSON file."""
        console = Console()
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            client = APIClient()
            response = client.import_[resource](s(data)
            
            if response.status_code == 201:
                stats = response.json()
                console.print(f"[green]✓ Imported: {stats['imported']}[/green]")
                console.print(f"[yellow]⊘ Skipped: {stats['skipped']}[/yellow]")
                if stats['errors']:
                    console.print(f"[red]✗ Errors: {len(stats['errors'])}[/red]")
                    for error in stats['errors']:
                        console.print(f"  - {error['item']}: {error['error']}")
            else:
                console.print(f"[red]✗ Import failed: {response.json()['error']}[/red]")
                raise click.Abort()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise click.Abort() from e
    ```
  - **Expected Impact:** Consistent CLI import patterns
  - **Priority:** 🟡 MEDIUM
  - **Effort:** 🟢 LOW

---

## Summary

### Priority Breakdown

- 🔴 **CRITICAL:** 0
- 🟠 **HIGH:** 2 (Enum validation, Manual testing updates)
- 🟡 **MEDIUM:** 4 (Bulk import endpoint, Data mapping script, Test templates, CLI import)
- 🟢 **LOW:** 0

### Effort Breakdown

- 🟢 **LOW:** 6 items
- 🟡 **MEDIUM:** 0 items
- 🟠 **HIGH:** 0 items

### Expected Impact

- Consistent bulk import patterns across projects
- Better data transformation patterns
- Improved validation preventing database errors
- Documentation staying in sync with code
- Better test coverage for bulk operations

---

**Last Updated:** 2025-12-05

