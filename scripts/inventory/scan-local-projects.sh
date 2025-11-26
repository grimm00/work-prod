#!/bin/bash

# scan-local-projects.sh
# Scans local directories for Git repositories and projects
# Outputs to data/local-projects.json

set -e  # Exit on error

echo "========================================="
echo "Scanning Local Projects"
echo "========================================="
echo ""

# Create data directory if it doesn't exist
mkdir -p data

OUTPUT_FILE="data/local-projects.json"

# Directories to scan
SCAN_DIRS=(
    "$HOME/Projects"
    "$HOME/Learning"
)

echo "Scanning directories:"
for dir in "${SCAN_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ⚠ $dir (not found, skipping)"
    fi
done
echo ""

# Python script to generate JSON output
python3 << 'PYTHON_SCRIPT' > "$OUTPUT_FILE"
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def get_dir_size(path):
    """Get total size of directory in bytes"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat(follow_symlinks=False).st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return total

def count_files(path):
    """Count total files in directory"""
    count = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                count += 1
            elif entry.is_dir(follow_symlinks=False):
                count += count_files(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return count

def detect_languages(path):
    """Detect languages by file extensions"""
    ext_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.h': 'C/C++',
        '.hpp': 'C++',
        '.cs': 'C#',
        '.go': 'Go',
        '.rs': 'Rust',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.m': 'Objective-C',
        '.r': 'R',
        '.R': 'R',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.zsh': 'Zsh',
        '.ps1': 'PowerShell',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        '.vue': 'Vue',
        '.md': 'Markdown',
        '.json': 'JSON',
        '.xml': 'XML',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.toml': 'TOML',
    }
    
    lang_count = defaultdict(int)
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                ext = Path(entry.name).suffix.lower()
                if ext in ext_map:
                    lang_count[ext_map[ext]] += 1
            elif entry.is_dir(follow_symlinks=False) and not entry.name.startswith('.'):
                sub_langs = detect_languages(entry.path)
                for lang, count in sub_langs.items():
                    lang_count[lang] += count
    except (PermissionError, FileNotFoundError):
        pass
    
    return dict(lang_count)

def get_git_info(path):
    """Get Git repository information"""
    git_dir = os.path.join(path, '.git')
    if not os.path.isdir(git_dir):
        return None
    
    info = {'isGit': True}
    
    try:
        # Get remote URL
        result = subprocess.run(
            ['git', '-C', path, 'remote', 'get-url', 'origin'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['remoteUrl'] = result.stdout.strip()
        else:
            info['remoteUrl'] = None
            
        # Get last commit date
        result = subprocess.run(
            ['git', '-C', path, 'log', '-1', '--format=%aI'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['lastCommitDate'] = result.stdout.strip()
        else:
            info['lastCommitDate'] = None
            
        # Get current branch
        result = subprocess.run(
            ['git', '-C', path, 'branch', '--show-current'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            info['currentBranch'] = result.stdout.strip()
        else:
            info['currentBranch'] = None
            
    except Exception as e:
        print(f"Warning: Error getting git info for {path}: {e}", file=sys.stderr)
    
    return info

def scan_directory(base_dir):
    """Scan directory for projects"""
    projects = []
    
    if not os.path.isdir(base_dir):
        return projects
    
    try:
        for entry in os.scandir(base_dir):
            if entry.is_dir(follow_symlinks=False) and not entry.name.startswith('.'):
                project_path = entry.path
                project_name = entry.name
                
                print(f"Scanning: {project_path}", file=sys.stderr)
                
                # Get git info
                git_info = get_git_info(project_path)
                is_git = git_info is not None
                
                # Get directory size and file count
                dir_size = get_dir_size(project_path)
                file_count = count_files(project_path)
                
                # Detect languages
                languages = detect_languages(project_path)
                
                project = {
                    'name': project_name,
                    'path': project_path,
                    'baseDir': os.path.basename(base_dir),
                    'isGit': is_git,
                    'gitInfo': git_info if is_git else None,
                    'sizeBytes': dir_size,
                    'fileCount': file_count,
                    'languages': languages,
                    'scannedAt': datetime.now().isoformat()
                }
                
                projects.append(project)
    except (PermissionError, FileNotFoundError) as e:
        print(f"Warning: Cannot access {base_dir}: {e}", file=sys.stderr)
    
    return projects

# Scan all directories
all_projects = []
scan_dirs = [
    os.path.expanduser("~/Projects"),
    os.path.expanduser("~/Learning")
]

for scan_dir in scan_dirs:
    projects = scan_directory(scan_dir)
    all_projects.extend(projects)

# Output JSON
print(json.dumps(all_projects, indent=2))
PYTHON_SCRIPT

# Count projects
PROJECT_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")

echo ""
echo "✓ Successfully scanned $PROJECT_COUNT projects"
echo "✓ Saved to: $OUTPUT_FILE"
echo ""

# Show summary
echo "Summary:"
echo "--------"
echo "Total Projects: $PROJECT_COUNT"

# Count by location
PROJECTS_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; repos = json.load(sys.stdin); print(sum(1 for r in repos if r.get('baseDir') == 'Projects'))")
LEARNING_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; repos = json.load(sys.stdin); print(sum(1 for r in repos if r.get('baseDir') == 'Learning'))")

echo "  ~/Projects: $PROJECTS_COUNT"
echo "  ~/Learning: $LEARNING_COUNT"

# Count by Git status
GIT_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; repos = json.load(sys.stdin); print(sum(1 for r in repos if r.get('isGit', False)))")
NON_GIT_COUNT=$((PROJECT_COUNT - GIT_COUNT))

echo "  Git repos: $GIT_COUNT"
echo "  Non-Git: $NON_GIT_COUNT"

echo ""
echo "✓ Local project scan complete!"
echo ""
echo "Next step: Run python3 analyze-tech-stack.py to analyze technologies"

