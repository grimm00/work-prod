#!/bin/bash

# fetch-github-repos.sh
# Fetches all repositories for grimm00 user from GitHub via gh CLI
# Outputs to data/github-repos.json

set -e  # Exit on error

echo "========================================="
echo "Fetching GitHub Repositories for grimm00"
echo "========================================="
echo ""

# Check if gh CLI is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "Error: gh CLI is not installed"
    echo "Install with: brew install gh"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "Error: gh CLI is not authenticated"
    echo "Run: gh auth login"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data

OUTPUT_FILE="data/github-repos.json"

echo "Fetching repositories from github.com for grimm00..."
echo ""

# Fetch all repos for grimm00
# Using --json to get structured data
gh repo list grimm00 \
    --limit 1000 \
    --json name,description,url,sshUrl,createdAt,updatedAt,pushedAt,isPrivate,isFork,isArchived,primaryLanguage,languages,stargazerCount,forkCount,diskUsage \
    > "$OUTPUT_FILE"

# Count repos
REPO_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")

echo "✓ Successfully fetched $REPO_COUNT repositories"
echo "✓ Saved to: $OUTPUT_FILE"
echo ""

# Show summary
echo "Summary:"
echo "--------"
echo "Total Repositories: $REPO_COUNT"

# Count by visibility
PRIVATE_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; repos = json.load(sys.stdin); print(sum(1 for r in repos if r.get('isPrivate', False)))")
PUBLIC_COUNT=$((REPO_COUNT - PRIVATE_COUNT))

echo "  Private: $PRIVATE_COUNT"
echo "  Public: $PUBLIC_COUNT"

# Count forks
FORK_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; repos = json.load(sys.stdin); print(sum(1 for r in repos if r.get('isFork', False)))")
ORIGINAL_COUNT=$((REPO_COUNT - FORK_COUNT))

echo "  Original: $ORIGINAL_COUNT"
echo "  Forks: $FORK_COUNT"

# Count archived
ARCHIVED_COUNT=$(cat "$OUTPUT_FILE" | python3 -c "import sys, json; repos = json.load(sys.stdin); print(sum(1 for r in repos if r.get('isArchived', False)))")
ACTIVE_COUNT=$((REPO_COUNT - ARCHIVED_COUNT))

echo "  Active: $ACTIVE_COUNT"
echo "  Archived: $ARCHIVED_COUNT"

echo ""
echo "✓ GitHub repository fetch complete!"
echo ""
echo "Next step: Run ./scan-local-projects.sh to scan local directories"







