#!/usr/bin/env python3

"""
deduplicate-projects.py
Merges local and GitHub projects when they reference the same repository
Updates classifications to reflect merged projects
"""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

def normalize_github_url(url):
    """Normalize GitHub URL for comparison"""
    if not url:
        return None
    
    # Remove .git suffix
    url = url.rstrip('.git')
    
    # Convert SSH to HTTPS for comparison
    if url.startswith('git@github.com:'):
        url = url.replace('git@github.com:', 'https://github.com/')
    
    # Normalize to lowercase
    url = url.lower()
    
    # Extract owner/repo
    parsed = urlparse(url)
    if parsed.netloc == 'github.com':
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return f"{path_parts[0]}/{path_parts[1]}"
    
    return None

def main():
    print("=" * 60)
    print("Deduplicating Projects")
    print("=" * 60)
    
    # Load data
    print("\nLoading data files...")
    with open('data/github-repos.json', 'r') as f:
        github_repos = json.load(f)
    
    with open('data/local-projects.json', 'r') as f:
        local_projects = json.load(f)
    
    with open('data/classifications.json', 'r') as f:
        classifications = json.load(f)
    
    print(f"  ✓ {len(github_repos)} GitHub repositories")
    print(f"  ✓ {len(local_projects)} local projects")
    print(f"  ✓ {len(classifications)} classifications")
    
    # Build GitHub URL index
    print("\nBuilding GitHub repository index...")
    github_index = {}
    for repo in github_repos:
        normalized_url = normalize_github_url(repo['url'])
        if normalized_url:
            github_index[normalized_url] = repo
    print(f"  ✓ Indexed {len(github_index)} GitHub repos")
    
    # Find duplicates
    print("\nFinding duplicates...")
    duplicates = []
    local_only = []
    
    for local_proj in local_projects:
        if local_proj.get('isGit') and local_proj.get('gitInfo'):
            remote_url = local_proj['gitInfo'].get('remoteUrl', '')
            normalized_url = normalize_github_url(remote_url)
            
            if normalized_url and normalized_url in github_index:
                github_repo = github_index[normalized_url]
                duplicates.append({
                    'github': github_repo,
                    'local': local_proj,
                    'github_id': f"github:{github_repo['name']}",
                    'local_id': f"local:{local_proj['path']}",
                    'normalized_url': normalized_url
                })
            else:
                local_only.append(local_proj)
        else:
            local_only.append(local_proj)
    
    # GitHub-only projects (not in duplicates)
    github_only = [repo for repo in github_repos 
                   if normalize_github_url(repo['url']) not in 
                   [dup['normalized_url'] for dup in duplicates]]
    
    print(f"  ✓ Found {len(duplicates)} duplicates")
    print(f"  ✓ {len(github_only)} GitHub-only repos")
    print(f"  ✓ {len(local_only)} local-only projects")
    
    # Show duplicates
    if duplicates:
        print("\nDuplicate projects found:")
        for dup in duplicates:
            print(f"  • {dup['github']['name']}")
            print(f"    - GitHub: {dup['github_id']}")
            print(f"    - Local:  {dup['local_id']}")
            
            # Check if classifications differ
            github_class = classifications.get(dup['github_id'])
            local_class = classifications.get(dup['local_id'])
            
            if github_class and local_class and github_class != local_class:
                print(f"    ⚠ Different classifications: GitHub={github_class}, Local={local_class}")
    
    # Merge classifications
    print("\nMerging classifications...")
    merged_classifications = {}
    conflicts = []
    
    # Handle duplicates - prefer local classification (more context)
    for dup in duplicates:
        github_id = dup['github_id']
        local_id = dup['local_id']
        
        github_class = classifications.get(github_id)
        local_class = classifications.get(local_id)
        
        # Use merged ID format
        merged_id = f"merged:{dup['github']['name']}"
        
        if local_class:
            merged_classifications[merged_id] = local_class
            if github_class and github_class != local_class:
                conflicts.append({
                    'name': dup['github']['name'],
                    'github': github_class,
                    'local': local_class,
                    'kept': local_class
                })
        elif github_class:
            merged_classifications[merged_id] = github_class
        
        # Also keep original IDs pointing to merged classification
        if local_class or github_class:
            merged_classifications[github_id] = merged_classifications[merged_id]
            merged_classifications[local_id] = merged_classifications[merged_id]
    
    # Add GitHub-only projects
    for repo in github_only:
        github_id = f"github:{repo['name']}"
        if github_id in classifications:
            merged_classifications[github_id] = classifications[github_id]
    
    # Add local-only projects
    for proj in local_only:
        local_id = f"local:{proj['path']}"
        if local_id in classifications:
            merged_classifications[local_id] = classifications[local_id]
    
    if conflicts:
        print("\n⚠ Classification conflicts resolved (kept local classification):")
        for conflict in conflicts:
            print(f"  • {conflict['name']}: Local={conflict['local']} (kept), GitHub={conflict['github']} (discarded)")
    
    # Save merged classifications
    with open('data/classifications-merged.json', 'w') as f:
        json.dump(merged_classifications, f, indent=2)
    
    # Replace original classifications
    with open('data/classifications.json', 'w') as f:
        json.dump(merged_classifications, f, indent=2)
    
    print(f"\n✓ Merged classifications: {len(merged_classifications)} total")
    print(f"  ✓ Saved to: data/classifications.json")
    print(f"  ✓ Backup:   data/classifications-merged.json")
    
    # Generate deduplicated summary
    total_unique_projects = len(duplicates) + len(github_only) + len(local_only)
    
    print("\n" + "=" * 60)
    print("Deduplication Summary")
    print("=" * 60)
    print(f"\nOriginal counts:")
    print(f"  • GitHub repos: {len(github_repos)}")
    print(f"  • Local projects: {len(local_projects)}")
    print(f"  • Total: {len(github_repos) + len(local_projects)}")
    print(f"\nAfter deduplication:")
    print(f"  • Merged (GitHub + Local): {len(duplicates)}")
    print(f"  • GitHub-only: {len(github_only)}")
    print(f"  • Local-only: {len(local_only)}")
    print(f"  • Total unique projects: {total_unique_projects}")
    print(f"\nReduced from {len(github_repos) + len(local_projects)} to {total_unique_projects} projects")
    print(f"({len(duplicates)} duplicates removed)")
    
    print("\n✓ Deduplication complete!")
    print("\nNext step: Run python3 generate-report.py to regenerate docs with deduplicated data")

if __name__ == '__main__':
    main()






