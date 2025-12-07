#!/usr/bin/env python3

"""
classify-projects.py
Interactive script for classifying projects by category
Allows user to categorize projects as Work/Apprenti/Personal/Learning/Archived
"""

import json
import sys
from pathlib import Path

# Classification categories
CATEGORIES = {
    '1': 'Work (DRW)',
    '2': 'Apprenti',
    '3': 'Personal',
    '4': 'Learning',
    '5': 'Inactive/Archived',
    '6': 'Skip'
}

def load_json(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return None

def load_existing_classifications():
    """Load existing classifications if any"""
    try:
        with open('data/classifications.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_classifications(classifications):
    """Save classifications to file"""
    with open('data/classifications.json', 'w') as f:
        json.dump(classifications, indent=2, fp=f)

def format_size(bytes):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

def display_project_info(project, tech_stats):
    """Display project information for user"""
    name = project.get('name', 'Unknown')
    path = project.get('path', project.get('url', 'Unknown'))
    
    print("\n" + "="*60)
    print(f"Project: {name}")
    print("="*60)
    
    # Location/URL
    if 'path' in project:
        print(f"Path: {path}")
        base_dir = project.get('baseDir', '')
        if base_dir:
            print(f"Location: ~/{base_dir}")
    else:
        print(f"URL: {project.get('url', 'Unknown')}")
    
    # Git info
    is_git = project.get('isGit', False)
    print(f"Git Repository: {'Yes' if is_git else 'No'}")
    
    if is_git and 'gitInfo' in project and project['gitInfo']:
        git_info = project['gitInfo']
        if git_info.get('remoteUrl'):
            print(f"Remote: {git_info['remoteUrl']}")
        if git_info.get('lastCommitDate'):
            print(f"Last Commit: {git_info['lastCommitDate'][:10]}")
        if git_info.get('currentBranch'):
            print(f"Branch: {git_info['currentBranch']}")
    
    # GitHub-specific info
    if 'pushedAt' in project:
        pushed_at = project.get('pushedAt', '')[:10]
        print(f"Last Push: {pushed_at}")
    if 'isPrivate' in project:
        visibility = "Private" if project.get('isPrivate') else "Public"
        print(f"Visibility: {visibility}")
    if project.get('isFork'):
        print("Type: Fork")
    if project.get('isArchived'):
        print("Status: Archived")
    
    # Description
    if 'description' in project and project['description']:
        print(f"Description: {project['description']}")
    
    # Size/files for local projects
    if 'sizeBytes' in project:
        size = format_size(project['sizeBytes'])
        file_count = project.get('fileCount', 0)
        print(f"Size: {size} ({file_count} files)")
    
    # Languages
    languages = project.get('languages', {})
    if languages:
        if isinstance(languages, list):
            # GitHub format
            lang_names = [lang.get('node', {}).get('name', 'Unknown') for lang in languages]
            print(f"Languages: {', '.join(lang_names)}")
        elif isinstance(languages, dict):
            # Local format with counts
            sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            top_langs = sorted_langs[:5]  # Top 5
            lang_str = ', '.join(f"{lang} ({count})" for lang, count in top_langs)
            print(f"Languages: {lang_str}")
    elif 'primaryLanguage' in project and project['primaryLanguage']:
        primary = project['primaryLanguage'].get('name', 'Unknown')
        print(f"Primary Language: {primary}")
    
    print("-"*60)

def classify_project(project, tech_stats):
    """Prompt user to classify a project"""
    display_project_info(project, tech_stats)
    
    print("\nClassify as:")
    for key, category in CATEGORIES.items():
        print(f"  [{key}] {category}")
    
    while True:
        choice = input("\nYour choice: ").strip()
        
        if choice in CATEGORIES:
            if choice == '6':
                return None  # Skip
            return CATEGORIES[choice]
        else:
            print("Invalid choice. Please enter 1-6.")

def bulk_classify():
    """Ask if user wants bulk classification"""
    print("\n" + "="*60)
    print("Bulk Classification Options")
    print("="*60)
    print("\nWould you like to:")
    print("  [1] Classify all ~/Learning projects as 'Learning'")
    print("  [2] Classify all ~/Projects as 'Personal' (can override individually)")
    print("  [3] No bulk operations, classify individually")
    
    while True:
        choice = input("\nYour choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1-3.")

def main():
    print("\n" + "="*60)
    print("Project Classification Tool")
    print("="*60)
    print("\nThis tool helps you categorize your projects.")
    print("You can classify each project or use bulk operations.\n")
    
    # Load data
    print("Loading project data...")
    github_repos = load_json('data/github-repos.json')
    local_projects = load_json('data/local-projects.json')
    tech_stats = load_json('data/tech-stack.json')
    
    if github_repos is None or local_projects is None:
        print("\nError: Required data files not found.")
        print("Please run:")
        print("  1. ./fetch-github-repos.sh")
        print("  2. ./scan-local-projects.sh")
        print("  3. python3 analyze-tech-stack.py")
        sys.exit(1)
    
    print(f"  ✓ {len(github_repos)} GitHub repositories")
    print(f"  ✓ {len(local_projects)} local projects")
    
    # Load existing classifications
    classifications = load_existing_classifications()
    
    # Combine all projects
    all_projects = []
    
    # Add GitHub repos
    for repo in github_repos:
        repo['source'] = 'github'
        repo['id'] = f"github:{repo['name']}"
        all_projects.append(repo)
    
    # Add local projects
    for project in local_projects:
        project['source'] = 'local'
        project['id'] = f"local:{project['path']}"
        all_projects.append(project)
    
    print(f"\nTotal projects to classify: {len(all_projects)}")
    
    # Check for bulk classification
    bulk_choice = bulk_classify()
    
    if bulk_choice == '1':
        # Classify all ~/Learning as Learning
        for project in all_projects:
            if project.get('source') == 'local' and project.get('baseDir') == 'Learning':
                classifications[project['id']] = 'Learning'
        print(f"\n✓ Bulk classified {sum(1 for p in all_projects if p.get('baseDir') == 'Learning')} Learning projects")
    
    elif bulk_choice == '2':
        # Classify all ~/Projects as Personal (can be overridden)
        for project in all_projects:
            if project.get('source') == 'local' and project.get('baseDir') == 'Projects':
                if project['id'] not in classifications:
                    classifications[project['id']] = 'Personal'
        print(f"\n✓ Bulk classified {sum(1 for p in all_projects if p.get('baseDir') == 'Projects')} Projects as Personal")
    
    # Classify remaining projects
    unclassified = [p for p in all_projects if p['id'] not in classifications]
    
    if not unclassified:
        print("\n✓ All projects already classified!")
    else:
        print(f"\n{len(unclassified)} projects need classification")
        print("(Press Ctrl+C to save and exit at any time)\n")
        
        try:
            for i, project in enumerate(unclassified, 1):
                print(f"\n[{i}/{len(unclassified)}]")
                
                category = classify_project(project, tech_stats)
                if category:
                    classifications[project['id']] = category
                    print(f"\n✓ Classified as: {category}")
                else:
                    print("\n⊘ Skipped")
                
                # Save progress every 5 projects
                if i % 5 == 0:
                    save_classifications(classifications)
                    print(f"\n💾 Progress saved ({i}/{len(unclassified)} classified)")
        
        except KeyboardInterrupt:
            print("\n\n⚠ Classification interrupted by user")
            print("Saving progress...")
    
    # Save final classifications
    save_classifications(classifications)
    
    # Summary
    print("\n" + "="*60)
    print("Classification Summary")
    print("="*60 + "\n")
    
    # Count by category
    category_counts = {}
    for project_id, category in classifications.items():
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print(f"Total Classified: {len(classifications)}/{len(all_projects)}")
    print("\nBy Category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")
    
    print(f"\n✓ Classifications saved to: data/classifications.json")
    print("\nNext step: Run python3 generate-report.py to create inventory report\n")

if __name__ == '__main__':
    main()







