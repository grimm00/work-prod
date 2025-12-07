#!/usr/bin/env python3

"""
generate-report.py
Generates filled inventory document from collected data
Creates current-state-inventory.md and discovered-skills.md
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

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

def format_size(bytes):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

def generate_inventory_report(github_repos, local_projects, tech_stats, classifications):
    """Generate markdown inventory report"""
    
    lines = []
    
    # Header
    lines.append("# Current State Inventory")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Purpose:** Comprehensive catalog of all repositories and projects")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Summary
    lines.append("## 📊 Summary")
    lines.append("")
    
    total_projects = len(github_repos) + len(local_projects)
    lines.append(f"- **Total Projects:** {total_projects}")
    lines.append(f"- **GitHub Repositories:** {len(github_repos)}")
    lines.append(f"- **Local Projects:** {len(local_projects)}")
    
    # Git status
    git_local = sum(1 for p in local_projects if p.get('isGit', False))
    non_git_local = len(local_projects) - git_local
    lines.append(f"- **Git-tracked Local:** {git_local}")
    lines.append(f"- **Non-Git Local:** {non_git_local}")
    
    # Tech stack summary
    if tech_stats:
        summary = tech_stats.get('summary', {})
        total_langs = summary.get('totalLanguages', 0)
        lines.append(f"- **Languages Used:** {total_langs}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # GitHub Repositories
    lines.append("## 🐙 Remote Repositories (GitHub - grimm00)")
    lines.append("")
    lines.append(f"Total: **{len(github_repos)}** repositories")
    lines.append("")
    
    # Group by classification
    github_by_category = defaultdict(list)
    for repo in github_repos:
        repo_id = f"github:{repo['name']}"
        category = classifications.get(repo_id, 'Unclassified')
        github_by_category[category].append(repo)
    
    for category in sorted(github_by_category.keys()):
        repos = github_by_category[category]
        lines.append(f"### {category} ({len(repos)})")
        lines.append("")
        
        for repo in sorted(repos, key=lambda r: r['name'].lower()):
            name = repo['name']
            lines.append(f"#### {name}")
            
            if repo.get('description'):
                lines.append(f"*{repo['description']}*")
                lines.append("")
            
            lines.append(f"- **URL:** {repo.get('url', 'N/A')}")
            
            # Visibility
            visibility = "Private" if repo.get('isPrivate') else "Public"
            lines.append(f"- **Visibility:** {visibility}")
            
            # Fork status
            if repo.get('isFork'):
                lines.append(f"- **Type:** Fork")
            
            # Archive status
            if repo.get('isArchived'):
                lines.append(f"- **Status:** Archived")
            
            # Last activity
            pushed_at = repo.get('pushedAt', '')[:10] if repo.get('pushedAt') else 'Unknown'
            lines.append(f"- **Last Push:** {pushed_at}")
            
            # Languages
            languages = repo.get('languages', [])
            if languages:
                lang_names = [lang.get('node', {}).get('name', 'Unknown') for lang in languages]
                lines.append(f"- **Languages:** {', '.join(lang_names)}")
            elif repo.get('primaryLanguage'):
                primary = repo['primaryLanguage'].get('name', 'Unknown')
                lines.append(f"- **Primary Language:** {primary}")
            
            # Stats
            stars = repo.get('stargazerCount', 0)
            forks = repo.get('forkCount', 0)
            if stars > 0 or forks > 0:
                lines.append(f"- **Stats:** ⭐ {stars} | 🍴 {forks}")
            
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Local Projects
    lines.append("## 💻 Local Projects")
    lines.append("")
    lines.append(f"Total: **{len(local_projects)}** projects")
    lines.append("")
    
    # Group by location
    for base_dir in ['Projects', 'Learning']:
        projects_in_dir = [p for p in local_projects if p.get('baseDir') == base_dir]
        
        if not projects_in_dir:
            continue
        
        lines.append(f"### ~/{base_dir} ({len(projects_in_dir)})")
        lines.append("")
        
        # Group by classification
        projects_by_category = defaultdict(list)
        for project in projects_in_dir:
            project_id = f"local:{project['path']}"
            category = classifications.get(project_id, 'Unclassified')
            projects_by_category[category].append(project)
        
        for category in sorted(projects_by_category.keys()):
            projects = projects_by_category[category]
            
            if len(projects_by_category) > 1:
                lines.append(f"#### {category} ({len(projects)})")
                lines.append("")
            
            for project in sorted(projects, key=lambda p: p['name'].lower()):
                name = project['name']
                lines.append(f"**{name}**")
                
                lines.append(f"- **Path:** `{project['path']}`")
                
                # Git status
                is_git = project.get('isGit', False)
                git_status = "Yes" if is_git else "No"
                lines.append(f"- **Git Repository:** {git_status}")
                
                if is_git and project.get('gitInfo'):
                    git_info = project['gitInfo']
                    if git_info.get('remoteUrl'):
                        lines.append(f"- **Remote:** {git_info['remoteUrl']}")
                    if git_info.get('lastCommitDate'):
                        last_commit = git_info['lastCommitDate'][:10]
                        lines.append(f"- **Last Commit:** {last_commit}")
                    if git_info.get('currentBranch'):
                        lines.append(f"- **Branch:** {git_info['currentBranch']}")
                
                # Size and files
                if 'sizeBytes' in project:
                    size = format_size(project['sizeBytes'])
                    file_count = project.get('fileCount', 0)
                    lines.append(f"- **Size:** {size} ({file_count} files)")
                
                # Languages
                languages = project.get('languages', {})
                if languages:
                    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
                    top_langs = sorted_langs[:5]
                    lang_str = ', '.join(f"{lang} ({count})" for lang, count in top_langs)
                    lines.append(f"- **Languages:** {lang_str}")
                
                lines.append("")
        
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Tech Stack Summary
    lines.append("## 🛠️ Tech Stack Summary")
    lines.append("")
    
    if tech_stats and 'topLanguages' in tech_stats:
        lines.append("### Top Languages by Project Count")
        lines.append("")
        
        top_langs = tech_stats['topLanguages'][:15]
        
        lines.append("| Rank | Language | Projects | Percentage | GitHub | Local |")
        lines.append("|------|----------|----------|------------|--------|-------|")
        
        for i, lang in enumerate(top_langs, 1):
            name = lang['name']
            total = lang['totalProjects']
            pct = lang['percentage']
            gh = lang['githubProjects']
            local = lang['localProjects']
            lines.append(f"| {i} | {name} | {total} | {pct:.1f}% | {gh} | {local} |")
        
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Categorization Summary
    lines.append("## 🗂️ Project Categories")
    lines.append("")
    
    category_counts = defaultdict(int)
    for proj_id, category in classifications.items():
        category_counts[category] += 1
    
    if category_counts:
        lines.append("| Category | Count |")
        lines.append("|----------|-------|")
        for category in sorted(category_counts.keys()):
            count = category_counts[category]
            lines.append(f"| {category} | {count} |")
        lines.append("")
    else:
        lines.append("*No classifications yet. Run `classify-projects.py` to categorize projects.*")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Current Workflow & Challenges (placeholder)
    lines.append("## 🔍 Current Workflow & Challenges")
    lines.append("")
    lines.append("*This section should be filled in manually based on actual workflow observations.*")
    lines.append("")
    lines.append("### Workflow Observations")
    lines.append("- [Add workflow observations here]")
    lines.append("")
    lines.append("### Challenges")
    lines.append("- [Add challenges here]")
    lines.append("")
    lines.append("### Pain Points")
    lines.append("- [Add pain points here]")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Integration Opportunities
    lines.append("## 💡 Integration Opportunities")
    lines.append("")
    lines.append("Based on the inventory:")
    lines.append("")
    
    # GitHub integration
    lines.append(f"### GitHub Integration")
    lines.append(f"- {len(github_repos)} repositories available for integration")
    lines.append(f"- Could track commits, PRs, issues for activity metrics")
    lines.append(f"- Potential for automated progress tracking")
    lines.append("")
    
    # Local project management
    non_git = sum(1 for p in local_projects if not p.get('isGit', False))
    if non_git > 0:
        lines.append(f"### Version Control")
        lines.append(f"- {non_git} local projects not Git-tracked")
        lines.append(f"- Consider version control setup workflow")
        lines.append("")
    
    # Skills tracking
    if tech_stats:
        total_langs = tech_stats.get('summary', {}).get('totalLanguages', 0)
        lines.append(f"### Skills Tracking")
        lines.append(f"- {total_langs} technologies identified")
        lines.append(f"- Can populate Skills Matrix automatically")
        lines.append(f"- See `discovered-skills.md` for full list")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Footer
    lines.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Data Sources:**")
    lines.append(f"- GitHub API (gh CLI)")
    lines.append(f"- Local filesystem scan")
    lines.append(f"- Manual classification")
    
    return '\n'.join(lines)

def generate_skills_report(tech_stats):
    """Generate discovered skills markdown"""
    
    lines = []
    
    # Header
    lines.append("# Discovered Skills")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Purpose:** Technologies discovered from project inventory")
    lines.append(f"**Use Case:** Seed data for Skills Matrix feature")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Summary
    if tech_stats and 'summary' in tech_stats:
        summary = tech_stats['summary']
        total_langs = summary.get('totalLanguages', 0)
        total_projects = summary.get('totalProjects', 0)
        
        lines.append("## 📊 Summary")
        lines.append("")
        lines.append(f"- **Total Technologies:** {total_langs}")
        lines.append(f"- **Total Projects:** {total_projects}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Skills by usage
    lines.append("## 🎯 Skills by Usage")
    lines.append("")
    lines.append("Suggested confidence levels based on project usage:")
    lines.append("- **High (4-5):** Used in 10+ projects")
    lines.append("- **Medium (3):** Used in 5-9 projects")
    lines.append("- **Low (1-2):** Used in 1-4 projects")
    lines.append("")
    
    if tech_stats and 'allLanguages' in tech_stats:
        all_langs = tech_stats['allLanguages']
        
        # Group by suggested confidence
        high_conf = []
        med_conf = []
        low_conf = []
        
        for lang_name, lang_data in all_langs.items():
            project_count = lang_data['totalProjects']
            if project_count >= 10:
                high_conf.append((lang_name, lang_data))
            elif project_count >= 5:
                med_conf.append((lang_name, lang_data))
            else:
                low_conf.append((lang_name, lang_data))
        
        # Sort each group by project count
        high_conf.sort(key=lambda x: x[1]['totalProjects'], reverse=True)
        med_conf.sort(key=lambda x: x[1]['totalProjects'], reverse=True)
        low_conf.sort(key=lambda x: x[1]['totalProjects'], reverse=True)
        
        # High confidence skills
        if high_conf:
            lines.append("### High Confidence Skills (10+ projects)")
            lines.append("")
            for lang_name, lang_data in high_conf:
                proj_count = lang_data['totalProjects']
                pct = lang_data['percentage']
                lines.append(f"#### {lang_name}")
                lines.append(f"- **Projects:** {proj_count} ({pct:.1f}%)")
                lines.append(f"- **Suggested Confidence:** 4-5")
                lines.append(f"- **Category:** Technical")
                
                # Show some projects
                projects = lang_data.get('projects', [])[:3]
                if projects:
                    proj_names = [p['name'] for p in projects]
                    lines.append(f"- **Example Projects:** {', '.join(proj_names)}")
                    if len(lang_data['projects']) > 3:
                        lines.append(f"  *(and {len(lang_data['projects']) - 3} more)*")
                
                lines.append("")
        
        # Medium confidence skills
        if med_conf:
            lines.append("### Medium Confidence Skills (5-9 projects)")
            lines.append("")
            for lang_name, lang_data in med_conf:
                proj_count = lang_data['totalProjects']
                pct = lang_data['percentage']
                lines.append(f"#### {lang_name}")
                lines.append(f"- **Projects:** {proj_count} ({pct:.1f}%)")
                lines.append(f"- **Suggested Confidence:** 3")
                lines.append(f"- **Category:** Technical")
                
                # Show projects
                projects = lang_data.get('projects', [])[:3]
                if projects:
                    proj_names = [p['name'] for p in projects]
                    lines.append(f"- **Example Projects:** {', '.join(proj_names)}")
                
                lines.append("")
        
        # Low confidence skills
        if low_conf:
            lines.append("### Developing Skills (1-4 projects)")
            lines.append("")
            lines.append("Technologies you've worked with but may need more practice:")
            lines.append("")
            
            for lang_name, lang_data in low_conf[:20]:  # Top 20
                proj_count = lang_data['totalProjects']
                lines.append(f"- **{lang_name}:** {proj_count} projects (Suggested confidence: 1-2)")
            
            if len(low_conf) > 20:
                lines.append(f"\n*...and {len(low_conf) - 20} more*")
            
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Integration with Skills Matrix
    lines.append("## 🔗 Integration with Skills Matrix Feature")
    lines.append("")
    lines.append("This data can be used to:")
    lines.append("")
    lines.append("1. **Pre-populate Skills Matrix** with real usage data")
    lines.append("2. **Set baseline confidence levels** based on project experience")
    lines.append("3. **Track skill usage over time** by re-running inventory")
    lines.append("4. **Identify gaps** in technology exposure")
    lines.append("5. **Plan learning paths** for underutilized technologies")
    lines.append("")
    lines.append("### Suggested Skills Matrix Fields")
    lines.append("")
    lines.append("For each skill above:")
    lines.append("- **Name:** Technology name")
    lines.append("- **Category:** Technical")
    lines.append("- **Confidence:** Based on project count")
    lines.append("- **Evidence:** \"Used in [N] projects\"")
    lines.append("- **Last Used:** Date from most recent project")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    
    lines.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Next Step:** Review and adjust confidence levels based on actual proficiency")
    
    return '\n'.join(lines)

def main():
    print("\n" + "="*60)
    print("Generating Inventory Reports")
    print("="*60 + "\n")
    
    # Load data
    print("Loading data files...")
    github_repos = load_json('data/github-repos.json')
    local_projects = load_json('data/local-projects.json')
    tech_stats = load_json('data/tech-stack.json')
    classifications = load_json('data/classifications.json')
    
    if github_repos is None or local_projects is None:
        print("\nError: Required data files not found.")
        print("Please run the data collection scripts first:")
        print("  1. ./fetch-github-repos.sh")
        print("  2. ./scan-local-projects.sh")
        print("  3. python3 analyze-tech-stack.py")
        print("  4. python3 classify-projects.py")
        sys.exit(1)
    
    if classifications is None:
        print("⚠ Warning: No classifications found. Projects will be listed as 'Unclassified'")
        classifications = {}
    
    print(f"  ✓ {len(github_repos)} GitHub repositories")
    print(f"  ✓ {len(local_projects)} local projects")
    print(f"  ✓ {len(classifications)} classifications")
    print("")
    
    # Generate inventory report
    print("Generating inventory report...")
    inventory_md = generate_inventory_report(github_repos, local_projects, tech_stats, classifications)
    
    # Save inventory to data directory
    inventory_file = 'data/generated-inventory.md'
    with open(inventory_file, 'w') as f:
        f.write(inventory_md)
    print(f"  ✓ Saved to: {inventory_file}")
    
    # Also copy to docs/maintainers/exploration
    docs_inventory_file = '../../docs/maintainers/exploration/current-state-inventory.md'
    with open(docs_inventory_file, 'w') as f:
        f.write(inventory_md)
    print(f"  ✓ Updated: {docs_inventory_file}")
    print("")
    
    # Generate skills report
    print("Generating discovered skills report...")
    skills_md = generate_skills_report(tech_stats)
    
    # Save skills report
    skills_file = '../../docs/maintainers/exploration/discovered-skills.md'
    with open(skills_file, 'w') as f:
        f.write(skills_md)
    print(f"  ✓ Saved to: {skills_file}")
    print("")
    
    # Summary
    print("="*60)
    print("✓ Report Generation Complete!")
    print("="*60 + "\n")
    
    print("Generated Files:")
    print(f"  1. {inventory_file} (working copy)")
    print(f"  2. {docs_inventory_file} (documentation)")
    print(f"  3. {skills_file} (skills matrix seed)")
    print("")
    
    print("Next Steps:")
    print("  1. Review the generated inventory document")
    print("  2. Fill in workflow observations and challenges")
    print("  3. Review discovered skills for Skills Matrix feature")
    print("  4. Consider whether 'Projects' should be an 8th core feature")
    print("")

if __name__ == '__main__':
    main()







