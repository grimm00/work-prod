#!/usr/bin/env python3

"""
generate-report-deduplicated.py
Generates deduplicated inventory reports
Merges GitHub + Local projects when they reference the same repository
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse

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

def normalize_github_url(url):
    """Normalize GitHub URL for comparison"""
    if not url:
        return None
    
    url = url.rstrip('.git')
    if url.startswith('git@github.com:'):
        url = url.replace('git@github.com:', 'https://github.com/')
    url = url.lower()
    
    parsed = urlparse(url)
    if parsed.netloc == 'github.com':
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return f"{path_parts[0]}/{path_parts[1]}"
    return None

def format_size(bytes_count):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"

def format_language_list(languages, limit=5):
    """Format language list for display"""
    if not languages:
        return "N/A"
    
    if isinstance(languages, list):  # GitHub format
        names = [lang.get('name', 'Unknown') for lang in languages[:limit]]
    elif isinstance(languages, dict):  # Local format
        # Sort by count, take top N
        sorted_langs = sorted(languages.items(), key=lambda x: x[1].get('count', 0) if isinstance(x[1], dict) else x[1], reverse=True)
        names = [lang[0] for lang in sorted_langs[:limit]]
    else:
        return "N/A"
    
    return ", ".join(names)

def merge_projects(github_repos, local_projects, classifications):
    """Merge GitHub and local projects, eliminating duplicates"""
    
    # Build GitHub index
    github_index = {}
    for repo in github_repos:
        normalized_url = normalize_github_url(repo['url'])
        if normalized_url:
            github_index[normalized_url] = repo
    
    # Build merged projects list
    merged_projects = []
    used_github_urls = set()
    
    # Process local projects first (they have more detail like local paths)
    for local_proj in local_projects:
        if local_proj.get('isGit') and local_proj.get('gitInfo'):
            remote_url = local_proj['gitInfo'].get('remoteUrl', '')
            normalized_url = normalize_github_url(remote_url)
            
            if normalized_url and normalized_url in github_index:
                # This is a duplicate - merge
                github_repo = github_index[normalized_url]
                merged_id = f"merged:{github_repo['name']}"
                
                merged_project = {
                    'type': 'merged',
                    'name': github_repo['name'],
                    'github_url': github_repo['url'],
                    'local_path': local_proj['path'],
                    'description': github_repo.get('description', ''),
                    'is_private': github_repo.get('isPrivate', False),
                    'is_fork': github_repo.get('isFork', False),
                    'last_push': github_repo.get('pushedAt', '').split('T')[0],
                    'last_commit': local_proj['gitInfo'].get('lastCommitDate', '').split('T')[0],
                    'branch': local_proj['gitInfo'].get('currentBranch', 'N/A'),
                    'size': local_proj.get('sizeBytes', 0),
                    'file_count': local_proj.get('fileCount', 0),
                    'languages': local_proj.get('languages', {}),
                    'github_languages': github_repo.get('languages', []),
                    'classification': classifications.get(merged_id) or classifications.get(f"github:{github_repo['name']}") or classifications.get(f"local:{local_proj['path']}") or 'Unclassified'
                }
                
                merged_projects.append(merged_project)
                used_github_urls.add(normalized_url)
            else:
                # Local-only project
                local_id = f"local:{local_proj['path']}"
                merged_project = {
                    'type': 'local',
                    'name': local_proj['name'],
                    'local_path': local_proj['path'],
                    'is_git': local_proj.get('isGit', False),
                    'remote_url': remote_url if remote_url else None,
                    'last_commit': local_proj.get('gitInfo', {}).get('lastCommitDate', '').split('T')[0] if local_proj.get('gitInfo') else None,
                    'branch': local_proj.get('gitInfo', {}).get('currentBranch', 'N/A') if local_proj.get('gitInfo') else 'N/A',
                    'size': local_proj.get('sizeBytes', 0),
                    'file_count': local_proj.get('fileCount', 0),
                    'languages': local_proj.get('languages', {}),
                    'classification': classifications.get(local_id, 'Unclassified')
                }
                merged_projects.append(merged_project)
        else:
            # Non-Git local project
            local_id = f"local:{local_proj['path']}"
            merged_project = {
                'type': 'local',
                'name': local_proj['name'],
                'local_path': local_proj['path'],
                'is_git': False,
                'size': local_proj.get('sizeBytes', 0),
                'file_count': local_proj.get('fileCount', 0),
                'languages': local_proj.get('languages', {}),
                'classification': classifications.get(local_id, 'Unclassified')
            }
            merged_projects.append(merged_project)
    
    # Add GitHub-only projects
    for repo in github_repos:
        normalized_url = normalize_github_url(repo['url'])
        if normalized_url not in used_github_urls:
            github_id = f"github:{repo['name']}"
            merged_project = {
                'type': 'github',
                'name': repo['name'],
                'github_url': repo['url'],
                'description': repo.get('description', ''),
                'is_private': repo.get('isPrivate', False),
                'is_fork': repo.get('isFork', False),
                'last_push': repo.get('pushedAt', '').split('T')[0],
                'github_languages': repo.get('languages', []),
                'classification': classifications.get(github_id, 'Unclassified')
            }
            merged_projects.append(merged_project)
    
    return merged_projects

def generate_inventory_markdown(merged_projects, tech_stats):
    """Generate markdown inventory from merged projects"""
    
    lines = []
    
    # Header
    lines.append("# Current State Inventory")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Purpose:** Comprehensive catalog of all repositories and projects (deduplicated)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Summary
    lines.append("## 📊 Summary")
    lines.append("")
    
    total_unique = len(merged_projects)
    merged_count = sum(1 for p in merged_projects if p['type'] == 'merged')
    github_only = sum(1 for p in merged_projects if p['type'] == 'github')
    local_only = sum(1 for p in merged_projects if p['type'] == 'local')
    
    lines.append(f"- **Total Unique Projects:** {total_unique}")
    lines.append(f"- **GitHub + Local (Merged):** {merged_count}")
    lines.append(f"- **GitHub-Only:** {github_only}")
    lines.append(f"- **Local-Only:** {local_only}")
    
    git_tracked = sum(1 for p in merged_projects if p['type'] in ['merged', 'github'] or (p['type'] == 'local' and p.get('is_git')))
    non_git = total_unique - git_tracked
    lines.append(f"- **Git-tracked:** {git_tracked}")
    lines.append(f"- **Non-Git:** {non_git}")
    
    if tech_stats:
        summary = tech_stats.get('summary', {})
        total_langs = summary.get('totalLanguages', 0)
        lines.append(f"- **Languages Used:** {total_langs}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Group by classification
    by_category = defaultdict(list)
    for proj in merged_projects:
        category = proj.get('classification', 'Unclassified')
        by_category[category].append(proj)
    
    # All Projects section
    lines.append("## 📂 All Projects (Deduplicated)")
    lines.append("")
    lines.append(f"This section lists all {total_unique} unique projects, grouped by classification.")
    lines.append("")
    
    for category in sorted(by_category.keys()):
        projects = sorted(by_category[category], key=lambda p: p['name'].lower())
        lines.append(f"### {category} ({len(projects)})")
        lines.append("")
        
        for proj in projects:
            name = proj['name']
            proj_type = proj['type']
            
            if proj_type == 'merged':
                lines.append(f"#### {name} 🔗")
                if proj.get('description'):
                    lines.append(f"*{proj['description']}*")
                    lines.append("")
                lines.append(f"- **Type:** GitHub + Local (Merged)")
                lines.append(f"- **GitHub URL:** {proj['github_url']}")
                lines.append(f"- **Local Path:** `{proj['local_path']}`")
                lines.append(f"- **Visibility:** {'Private' if proj['is_private'] else 'Public'}")
                if proj['is_fork']:
                    lines.append(f"- **Fork:** Yes")
                lines.append(f"- **Last GitHub Push:** {proj['last_push']}")
                lines.append(f"- **Last Local Commit:** {proj['last_commit']}")
                lines.append(f"- **Current Branch:** {proj['branch']}")
                lines.append(f"- **Local Size:** {format_size(proj['size'])} ({proj['file_count']:,} files)")
                
                lang_display = format_language_list(proj['languages'])
                if lang_display != "N/A":
                    lines.append(f"- **Languages:** {lang_display}")
                
            elif proj_type == 'github':
                lines.append(f"#### {name} ☁️")
                if proj.get('description'):
                    lines.append(f"*{proj['description']}*")
                    lines.append("")
                lines.append(f"- **Type:** GitHub-Only (not on local machine)")
                lines.append(f"- **GitHub URL:** {proj['github_url']}")
                lines.append(f"- **Visibility:** {'Private' if proj['is_private'] else 'Public'}")
                if proj['is_fork']:
                    lines.append(f"- **Fork:** Yes")
                lines.append(f"- **Last Push:** {proj['last_push']}")
                
                lang_display = format_language_list(proj['github_languages'])
                if lang_display != "N/A":
                    lines.append(f"- **Languages:** {lang_display}")
            
            else:  # local
                lines.append(f"#### {name} 💻")
                lines.append(f"- **Type:** Local-Only")
                lines.append(f"- **Path:** `{proj['local_path']}`")
                lines.append(f"- **Git Repository:** {'Yes' if proj.get('is_git') else 'No'}")
                
                if proj.get('is_git'):
                    if proj.get('remote_url'):
                        lines.append(f"- **Remote URL:** {proj['remote_url']}")
                    if proj.get('last_commit'):
                        lines.append(f"- **Last Commit:** {proj['last_commit']}")
                    lines.append(f"- **Branch:** {proj['branch']}")
                
                lines.append(f"- **Size:** {format_size(proj['size'])} ({proj['file_count']:,} files)")
                
                lang_display = format_language_list(proj['languages'])
                if lang_display != "N/A":
                    lines.append(f"- **Languages:** {lang_display}")
            
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Tech Stack Summary
    if tech_stats and 'summary' in tech_stats:
        lines.append("## 🛠️ Tech Stack Summary")
        lines.append("")
        
        summary = tech_stats['summary']
        lang_by_project = summary.get('languagesByProjectCount', [])
        
        if lang_by_project:
            lines.append("### Top Languages by Project Count")
            lines.append("")
            lines.append("| Rank | Language | Projects | % of Total |")
            lines.append("|------|----------|----------|------------|")
            
            for i, lang_data in enumerate(lang_by_project[:15]):
                lang_name = lang_data.get('language', 'Unknown')
                project_count = lang_data.get('projectCount', 0)
                percentage = lang_data.get('percentage', 0)
                lines.append(f"| {i+1} | {lang_name} | {project_count} | {percentage:.1f}% |")
            
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Workflow observations section
    lines.append("## 🧠 Workflow Observations & Challenges")
    lines.append("")
    lines.append("**Instructions:** Reflect on the inventory above. What patterns do you notice? What are your biggest pain points?")
    lines.append("")
    lines.append("### Project Management & Organization")
    lines.append("- [Your observations here]")
    lines.append("")
    lines.append("### Context Switching")
    lines.append("- [Your observations here]")
    lines.append("")
    lines.append("### Forgotten/Inactive Projects")
    lines.append("- [Your observations here]")
    lines.append("")
    lines.append("### Learning & Skill Development")
    lines.append("- [Your observations here]")
    lines.append("")
    lines.append("### Opportunities for Automation")
    lines.append("- [Your observations here]")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Integration opportunities
    lines.append("## 💡 Integration Opportunities")
    lines.append("")
    lines.append("**Instructions:** Based on your tools and project inventory, what are the most promising integrations?")
    lines.append("")
    lines.append("### GitHub Integration")
    lines.append("- [Ideas here]")
    lines.append("")
    lines.append("### Local Filesystem Integration")
    lines.append("- [Ideas here]")
    lines.append("")
    lines.append("### Other Tools (Miro, Slack, Outlook)")
    lines.append("- [Ideas here]")
    lines.append("")
    
    return "\n".join(lines)

def generate_skills_markdown(tech_stats, merged_projects):
    """Generate discovered skills document"""
    
    lines = []
    
    lines.append("# Discovered Skills from Project Inventory")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Purpose:** List of technologies identified across all projects to seed the Skills Matrix feature.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    if not tech_stats or 'summary' not in tech_stats:
        lines.append("No tech stack data available.")
        return "\n".join(lines)
    
    summary = tech_stats['summary']
    total_langs = summary.get('totalLanguages', 0)
    total_projects = len(merged_projects)
    
    lines.append("## 📊 Summary")
    lines.append("")
    lines.append(f"- **Total Unique Languages/Technologies:** {total_langs}")
    lines.append(f"- **Projects Analyzed:** {total_projects}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## 🧠 Discovered Skills")
    lines.append("")
    lines.append("This section lists all identified languages and technologies, grouped by suggested confidence level based on project count.")
    lines.append("")
    
    lang_by_project = summary.get('languagesByProjectCount', [])
    
    if not lang_by_project:
        lines.append("No language data available.")
        return "\n".join(lines)
    
    # Group by confidence
    high_confidence = []
    medium_confidence = []
    low_confidence = []
    
    for lang_data in lang_by_project:
        lang_name = lang_data.get('language', 'Unknown')
        project_count = lang_data.get('projectCount', 0)
        percentage = lang_data.get('percentage', 0)
        
        entry = f"- **{lang_name}** (Used in {project_count} projects, {percentage:.1f}% of total)"
        
        if project_count >= 10:
            high_confidence.append(entry)
        elif project_count >= 5:
            medium_confidence.append(entry)
        else:
            low_confidence.append(entry)
    
    lines.append("### High Confidence (Used in 10+ projects)")
    lines.append("")
    if high_confidence:
        lines.extend(high_confidence)
    else:
        lines.append("No languages found in 10+ projects.")
    lines.append("")
    
    lines.append("### Medium Confidence (Used in 5-9 projects)")
    lines.append("")
    if medium_confidence:
        lines.extend(medium_confidence)
    else:
        lines.append("No languages found in 5-9 projects.")
    lines.append("")
    
    lines.append("### Low Confidence (Used in <5 projects)")
    lines.append("")
    if low_confidence:
        lines.extend(low_confidence)
    else:
        lines.append("No languages found in <5 projects.")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## 🚀 Next Steps")
    lines.append("")
    lines.append("1. Review this list and refine suggested confidence levels")
    lines.append("2. Add any missing skills or technologies")
    lines.append("3. Use this document as a foundation for the 'Skills Matrix & Development Tracker' feature")
    lines.append("")
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("Generating Deduplicated Inventory Reports")
    print("=" * 60)
    
    # Load data
    print("\nLoading data files...")
    github_repos = load_json('data/github-repos.json')
    local_projects = load_json('data/local-projects.json')
    tech_stats = load_json('data/tech-stack.json')
    classifications = load_json('data/classifications.json') or {}
    
    if not github_repos or not local_projects:
        print("Error: Required data files not found")
        return 1
    
    print(f"  ✓ {len(github_repos)} GitHub repositories")
    print(f"  ✓ {len(local_projects)} local projects")
    print(f"  ✓ {len(classifications)} classifications")
    
    # Merge projects
    print("\nMerging duplicate projects...")
    merged_projects = merge_projects(github_repos, local_projects, classifications)
    
    total_original = len(github_repos) + len(local_projects)
    total_unique = len(merged_projects)
    duplicates_removed = total_original - total_unique
    
    print(f"  ✓ Original count: {total_original} projects")
    print(f"  ✓ Deduplicated: {total_unique} unique projects")
    print(f"  ✓ Removed {duplicates_removed} duplicates")
    
    # Generate inventory report
    print("\nGenerating inventory report...")
    inventory_md = generate_inventory_markdown(merged_projects, tech_stats)
    
    with open('data/generated-inventory-dedup.md', 'w') as f:
        f.write(inventory_md)
    print(f"  ✓ Saved to: data/generated-inventory-dedup.md")
    
    inventory_path = Path('../../docs/maintainers/exploration/current-state-inventory.md')
    with open(inventory_path, 'w') as f:
        f.write(inventory_md)
    print(f"  ✓ Updated: {inventory_path}")
    
    # Generate skills report
    print("\nGenerating discovered skills report...")
    skills_md = generate_skills_markdown(tech_stats, merged_projects)
    
    skills_path = Path('../../docs/maintainers/exploration/discovered-skills.md')
    with open(skills_path, 'w') as f:
        f.write(skills_md)
    print(f"  ✓ Saved to: {skills_path}")
    
    print("\n" + "=" * 60)
    print("✓ Deduplicated Report Generation Complete!")
    print("=" * 60)
    print(f"\nGenerated Files:")
    print(f"  1. data/generated-inventory-dedup.md (working copy)")
    print(f"  2. {inventory_path} (documentation)")
    print(f"  3. {skills_path} (skills matrix seed)")
    print(f"\nKey Stats:")
    print(f"  • {total_unique} unique projects")
    print(f"  • {duplicates_removed} duplicates eliminated")
    print(f"  • Projects with both GitHub + Local: {sum(1 for p in merged_projects if p['type'] == 'merged')}")
    print("")

if __name__ == '__main__':
    sys.exit(main() or 0)





