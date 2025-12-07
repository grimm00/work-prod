#!/usr/bin/env python3
"""
Map inventory classifications to Project model format.

Reads classifications-merged.json and maps to the format expected by
POST /api/projects/import endpoint.

**Repository Placement Decision:**
This script remains in the main work-prod repository (not moved to inventory repo)
because it's used to import inventory data into the Projects API, which belongs
to the main project. The inventory system will be separated into its own repository
during Week 4, but this mapping script stays here as it's part of the Projects API
import workflow.

See: docs/maintainers/planning/infrastructure/inventory-repository-separation/transition-plan.md
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


# Map inventory classifications to Project model classification enum
CLASSIFICATION_MAP = {
    'Personal': 'primary',
    'Work (DRW)': 'primary',
    'Apprenti': 'primary',
    'Learning': 'secondary',
    'Inactive/Archived': 'archive',
    'Skip': None  # Skip these projects
}

# Map inventory classifications to Project model status enum
STATUS_MAP = {
    'Personal': 'active',
    'Work (DRW)': 'active',
    'Apprenti': 'active',
    'Learning': 'active',
    'Inactive/Archived': 'cancelled',
    'Skip': None
}

# Extract organization from classification
def extract_organization(classification):
    """Extract organization name from classification."""
    if classification == 'Work (DRW)':
        return 'DRW'
    elif classification == 'Apprenti':
        return 'Apprenti'
    return None


def parse_project_key(key):
    """
    Parse project key to extract name, type, and path/url.
    
    Keys are in format:
    - "merged:project-name" - merged project
    - "github:project-name" - GitHub-only
    - "local:/path/to/project" - local-only
    
    Returns dict with:
    - 'name': canonical project name (from merged/github, or extracted from path)
    - 'type': 'merged', 'github', 'local', or 'unknown'
    - 'path': local path (if type is 'local')
    - 'canonical_name': canonical name for deduplication (from merged/github if available)
    """
    if key.startswith('merged:'):
        name = key[7:]  # Remove "merged:" prefix
        return {'name': name, 'type': 'merged', 'canonical_name': name}
    elif key.startswith('github:'):
        name = key[7:]  # Remove "github:" prefix
        return {'name': name, 'type': 'github', 'canonical_name': name}
    elif key.startswith('local:'):
        path = key[6:]  # Remove "local:" prefix
        # Extract name from path (last directory)
        name = Path(path).name
        # Try to infer canonical name from path
        # For paths like /Users/cdwilson/Projects/music-app-drw, 
        # canonical might be "music-app" if there's a merged entry
        return {'name': name, 'type': 'local', 'path': path, 'canonical_name': None}
    else:
        # Unknown format, use key as name
        return {'name': key, 'type': 'unknown', 'canonical_name': None}


def build_github_url(project_name):
    """Build GitHub URL from project name."""
    return f"https://github.com/grimm00/{project_name}"


def map_classification_to_project(inventory_data):
    """
    Map inventory classifications to Project model format.
    
    Args:
        inventory_data: Dictionary from classifications-merged.json
        
    Returns:
        List of project dictionaries in format expected by import endpoint
    """
    projects = []
    seen_projects = set()  # Track by name to avoid duplicates
    
    # Group entries by canonical project name
    # First pass: collect all entries and identify canonical names
    all_entries = []
    canonical_names = {}  # Map from any key to canonical name
    
    for key, classification in inventory_data.items():
        if classification == 'Skip':
            continue
            
        parsed = parse_project_key(key)
        entry = {
            'key': key,
            'type': parsed['type'],
            'path': parsed.get('path'),
            'name': parsed['name'],
            'classification': classification
        }
        all_entries.append(entry)
        
        # Canonical name is from merged/github entries
        if parsed['type'] in ('merged', 'github'):
            canonical_names[key] = parsed['name']
            # Also map local entries that might match
            # If we see a merged:project-name, look for local entries with similar names
            canonical_names[parsed['name']] = parsed['name']
    
    # Second pass: group entries by canonical name
    # For merged/github entries, use their name as canonical
    # For local entries, try to match to merged/github entries with same classification
    project_groups = defaultdict(list)
    local_entries_by_classification = defaultdict(list)
    
    for entry in all_entries:
        if entry['type'] in ('merged', 'github'):
            canonical_name = entry['name']
            project_groups[canonical_name].append(entry)
        else:
            # Local entry - try to match to existing group
            local_entries_by_classification[entry['classification']].append(entry)
    
    # Match local entries to canonical names
    for classification, local_entries in local_entries_by_classification.items():
        for local_entry in local_entries:
            # Try to find matching merged/github entry
            matched = False
            for canonical_name, group_entries in project_groups.items():
                # Check if any entry in group matches (same classification and name similarity)
                for group_entry in group_entries:
                    if (group_entry['classification'] == classification and
                        (group_entry['name'] in local_entry['name'] or 
                         local_entry['name'] in group_entry['name'])):
                        project_groups[canonical_name].append(local_entry)
                        matched = True
                        break
                if matched:
                    break
            
            # If no match found, create new group for local-only entry
            if not matched:
                project_groups[local_entry['name']].append(local_entry)
    
    # Process each project group
    for project_name, entries in project_groups.items():
        # Skip if already processed (avoid duplicates)
        if project_name in seen_projects:
            continue
        
        # Prefer merged entry, then local, then github
        merged_entry = next((e for e in entries if e['type'] == 'merged'), None)
        local_entry = next((e for e in entries if e['type'] == 'local'), None)
        github_entry = next((e for e in entries if e['type'] == 'github'), None)
        
        # Use merged entry if available, otherwise prefer local
        entry = merged_entry or local_entry or github_entry
        if not entry:
            continue
        
        # Determine canonical name: prefer merged/github name, fallback to local name
        canonical_name = project_name
        if merged_entry:
            canonical_name = merged_entry['key'].replace('merged:', '')
        elif github_entry:
            canonical_name = github_entry['key'].replace('github:', '')
        
        # Skip if canonical name already processed (handles name mismatches)
        if canonical_name in seen_projects:
            continue
        
        classification_value = entry['classification']
        
        # Map classification
        project_classification = CLASSIFICATION_MAP.get(classification_value)
        if project_classification is None:
            continue  # Skip projects with None classification
        
        # Map status
        project_status = STATUS_MAP.get(classification_value, 'active')
        
        # Extract organization
        organization = extract_organization(classification_value)
        
        # Build project data using canonical name
        project_data = {
            'name': canonical_name,
            'status': project_status,
            'classification': project_classification,
        }
        
        # Add path if available (from local entry)
        if local_entry and local_entry.get('path'):
            project_data['path'] = local_entry['path']
        
        # Add remote_url if GitHub entry exists
        if merged_entry or github_entry:
            project_data['remote_url'] = build_github_url(canonical_name)
        
        # Add organization if available
        if organization:
            project_data['organization'] = organization
        
        projects.append(project_data)
        seen_projects.add(canonical_name)
        seen_projects.add(project_name)  # Also mark original name as seen
    
    return projects


def main():
    """Main function to map inventory data and generate projects.json."""
    script_dir = Path(__file__).parent
    inventory_file = script_dir / 'inventory' / 'data' / 'classifications-merged.json'
    output_file = script_dir / 'projects.json'
    
    # Load inventory data
    print(f"Loading inventory data from {inventory_file}...")
    try:
        with open(inventory_file, 'r') as f:
            inventory_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {inventory_file} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {inventory_file}: {e}")
        sys.exit(1)
    
    print(f"  ✓ Loaded {len(inventory_data)} inventory entries")
    
    # Map to project format
    print("\nMapping to Project model format...")
    projects = map_classification_to_project(inventory_data)
    print(f"  ✓ Mapped {len(projects)} unique projects")
    
    # Generate output format expected by import endpoint
    output_data = {
        'projects': projects
    }
    
    # Save to projects.json
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"  ✓ Saved {len(projects)} projects to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("Mapping Summary")
    print("="*60)
    
    by_classification = defaultdict(int)
    by_status = defaultdict(int)
    by_org = defaultdict(int)
    
    for project in projects:
        by_classification[project.get('classification', 'None')] += 1
        by_status[project.get('status', 'None')] += 1
        if project.get('organization'):
            by_org[project['organization']] += 1
    
    print("\nBy Classification:")
    for cls, count in sorted(by_classification.items()):
        print(f"  {cls}: {count}")
    
    print("\nBy Status:")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")
    
    print("\nBy Organization:")
    for org, count in sorted(by_org.items()):
        print(f"  {org}: {count}")
    
    print(f"\nTotal Projects: {len(projects)}")
    print("="*60)


if __name__ == '__main__':
    main()

