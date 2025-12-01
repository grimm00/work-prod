#!/usr/bin/env python3

"""
analyze-tech-stack.py
Analyzes languages and technologies across all repositories
Combines GitHub and local project data to generate statistics
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def load_json(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        print("Run fetch-github-repos.sh and scan-local-projects.sh first")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)

def analyze_github_repos(repos):
    """Analyze language usage from GitHub repos"""
    lang_stats = defaultdict(lambda: {
        'totalBytes': 0,
        'projectCount': 0,
        'projects': []
    })
    
    for repo in repos:
        repo_name = repo.get('name', 'Unknown')
        languages = repo.get('languages', [])
        
        # GitHub provides languages as list of dicts with name and size
        for lang_info in languages:
            lang_name = lang_info.get('node', {}).get('name')
            if lang_name:
                lang_stats[lang_name]['totalBytes'] += 0  # Size not in basic query
                lang_stats[lang_name]['projectCount'] += 1
                lang_stats[lang_name]['projects'].append({
                    'name': repo_name,
                    'url': repo.get('url'),
                    'source': 'github'
                })
        
        # Use primary language if languages list is empty
        if not languages:
            primary = repo.get('primaryLanguage', {})
            if primary:
                lang_name = primary.get('name')
                if lang_name:
                    lang_stats[lang_name]['projectCount'] += 1
                    lang_stats[lang_name]['projects'].append({
                        'name': repo_name,
                        'url': repo.get('url'),
                        'source': 'github'
                    })
    
    return dict(lang_stats)

def analyze_local_projects(projects):
    """Analyze language usage from local projects"""
    lang_stats = defaultdict(lambda: {
        'fileCount': 0,
        'projectCount': 0,
        'projects': []
    })
    
    for project in projects:
        project_name = project.get('name', 'Unknown')
        project_path = project.get('path', '')
        languages = project.get('languages', {})
        
        for lang_name, file_count in languages.items():
            lang_stats[lang_name]['fileCount'] += file_count
            lang_stats[lang_name]['projectCount'] += 1
            lang_stats[lang_name]['projects'].append({
                'name': project_name,
                'path': project_path,
                'fileCount': file_count,
                'source': 'local'
            })
    
    return dict(lang_stats)

def merge_language_stats(github_stats, local_stats):
    """Merge GitHub and local language statistics"""
    all_langs = set(github_stats.keys()) | set(local_stats.keys())
    merged = {}
    
    for lang in all_langs:
        gh_data = github_stats.get(lang, {})
        local_data = local_stats.get(lang, {})
        
        # Combine project lists
        all_projects = []
        if 'projects' in gh_data:
            all_projects.extend(gh_data['projects'])
        if 'projects' in local_data:
            all_projects.extend(local_data['projects'])
        
        # Remove duplicates (same project name from both sources)
        unique_projects = {}
        for proj in all_projects:
            key = proj['name']
            if key not in unique_projects:
                unique_projects[key] = proj
        
        merged[lang] = {
            'totalProjects': len(unique_projects),
            'githubProjects': gh_data.get('projectCount', 0),
            'localProjects': local_data.get('projectCount', 0),
            'localFileCount': local_data.get('fileCount', 0),
            'projects': list(unique_projects.values())
        }
    
    return merged

def calculate_percentages(merged_stats):
    """Calculate percentage breakdown of languages"""
    total_projects = sum(stats['totalProjects'] for stats in merged_stats.values())
    
    for lang, stats in merged_stats.items():
        stats['percentage'] = round((stats['totalProjects'] / total_projects * 100), 2) if total_projects > 0 else 0
    
    return merged_stats

def get_top_languages(merged_stats, limit=10):
    """Get top N languages by project count"""
    sorted_langs = sorted(
        merged_stats.items(),
        key=lambda x: x[1]['totalProjects'],
        reverse=True
    )
    return sorted_langs[:limit]

def print_summary(merged_stats):
    """Print summary to console"""
    print("\n" + "="*50)
    print("Tech Stack Analysis Summary")
    print("="*50 + "\n")
    
    total_langs = len(merged_stats)
    total_projects = sum(stats['totalProjects'] for stats in merged_stats.values())
    
    print(f"Total Languages Found: {total_langs}")
    print(f"Total Projects Analyzed: {total_projects}")
    print("\n" + "-"*50)
    print("Top 10 Languages by Project Count:")
    print("-"*50 + "\n")
    
    top_langs = get_top_languages(merged_stats, 10)
    
    for i, (lang, stats) in enumerate(top_langs, 1):
        proj_count = stats['totalProjects']
        percentage = stats['percentage']
        gh_count = stats['githubProjects']
        local_count = stats['localProjects']
        
        print(f"{i:2d}. {lang:20s} - {proj_count:3d} projects ({percentage:5.1f}%)")
        print(f"     GitHub: {gh_count:2d}  |  Local: {local_count:2d}")
        print()

def generate_output(merged_stats, github_repos, local_projects):
    """Generate output JSON with full analysis"""
    output = {
        'analyzedAt': datetime.now().isoformat(),
        'summary': {
            'totalLanguages': len(merged_stats),
            'totalProjects': sum(stats['totalProjects'] for stats in merged_stats.values()),
            'githubRepoCount': len(github_repos),
            'localProjectCount': len(local_projects)
        },
        'topLanguages': [
            {
                'name': lang,
                'totalProjects': stats['totalProjects'],
                'percentage': stats['percentage'],
                'githubProjects': stats['githubProjects'],
                'localProjects': stats['localProjects']
            }
            for lang, stats in get_top_languages(merged_stats, 20)
        ],
        'allLanguages': {
            lang: {
                'totalProjects': stats['totalProjects'],
                'percentage': stats['percentage'],
                'githubProjects': stats['githubProjects'],
                'localProjects': stats['localProjects'],
                'localFileCount': stats['localFileCount'],
                'projects': stats['projects']
            }
            for lang, stats in merged_stats.items()
        }
    }
    
    return output

def main():
    print("="*50)
    print("Analyzing Tech Stack")
    print("="*50 + "\n")
    
    # Ensure data directory exists
    data_dir = Path('data')
    if not data_dir.exists():
        print("Error: data/ directory not found")
        sys.exit(1)
    
    # Load GitHub repos
    print("Loading GitHub repositories...")
    github_repos = load_json('data/github-repos.json')
    print(f"  ✓ Loaded {len(github_repos)} GitHub repositories\n")
    
    # Load local projects
    print("Loading local projects...")
    local_projects = load_json('data/local-projects.json')
    print(f"  ✓ Loaded {len(local_projects)} local projects\n")
    
    # Analyze GitHub repos
    print("Analyzing GitHub repositories...")
    github_stats = analyze_github_repos(github_repos)
    print(f"  ✓ Found {len(github_stats)} languages in GitHub repos\n")
    
    # Analyze local projects
    print("Analyzing local projects...")
    local_stats = analyze_local_projects(local_projects)
    print(f"  ✓ Found {len(local_stats)} languages in local projects\n")
    
    # Merge statistics
    print("Merging language statistics...")
    merged_stats = merge_language_stats(github_stats, local_stats)
    merged_stats = calculate_percentages(merged_stats)
    print(f"  ✓ Combined data for {len(merged_stats)} unique languages\n")
    
    # Generate output
    output = generate_output(merged_stats, github_repos, local_projects)
    
    # Save to file
    output_file = 'data/tech-stack.json'
    with open(output_file, 'w') as f:
        json.dump(output, indent=2, fp=f)
    
    print(f"✓ Saved analysis to: {output_file}\n")
    
    # Print summary
    print_summary(merged_stats)
    
    print("="*50)
    print("✓ Tech stack analysis complete!")
    print("="*50 + "\n")
    print("Next step: Run python3 classify-projects.py to classify projects\n")

if __name__ == '__main__':
    main()


