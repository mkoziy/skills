#!/bin/bash
# create a feature branch from plan file name if on the default branch
# usage: create-branch.sh <plan-file-path>
# strips leading YYYYMMDD- date prefix from branch name

set -e

if [ -z "${1:-}" ]; then
    echo "error: plan file path required" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
vcs=$(bash "$SCRIPT_DIR/detect-vcs.sh")

derive_branch_name() {
    local name
    name=$(basename "$1" .md)
    name=$(echo "$name" | sed 's/^[0-9]\{4\}-\{0,1\}[0-9]\{2\}-\{0,1\}[0-9]\{2\}-//')
    echo "$name"
}

do_git() {
    local plan_file="$1"
    local current_branch
    current_branch=$(git branch --show-current)

    local default_branch
    default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
    if [ -z "$default_branch" ]; then
        for candidate in main master trunk develop; do
            if git show-ref --verify --quiet "refs/heads/$candidate" 2>/dev/null; then
                default_branch="$candidate"
                break
            fi
        done
    fi
    if [ -z "$default_branch" ]; then
        default_branch=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | sed 's/.*: //')
    fi

    if [ -n "$current_branch" ] && [ -n "$default_branch" ] && [ "$current_branch" != "$default_branch" ]; then
        echo "$current_branch"
        return 0
    elif [ -n "$current_branch" ] && [ -z "$default_branch" ] && [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
        echo "$current_branch"
        return 0
    fi

    local branch_name
    branch_name=$(derive_branch_name "$plan_file")

    if git show-ref --verify --quiet "refs/heads/$branch_name" 2>/dev/null; then
        git checkout "$branch_name"
    else
        git checkout -b "$branch_name"
    fi

    echo "$branch_name"
}

do_hg() {
    local plan_file="$1"
    local current
    current=$(hg log -r . --template '{activebookmark}\n')

    local default_branch
    default_branch=$(bash "$SCRIPT_DIR/detect-branch.sh" 2>/dev/null || true)
    default_branch=${default_branch#remote/}

    if [ -n "$current" ] && [ -n "$default_branch" ] && [ "$current" != "$default_branch" ]; then
        echo "$current"
        return 0
    elif [ -n "$current" ] && [ -z "$default_branch" ] && [ "$current" != "main" ] && [ "$current" != "master" ]; then
        echo "$current"
        return 0
    fi

    local branch_name
    branch_name=$(derive_branch_name "$plan_file")

    if hg book --template '{bookmark}\n' 2>/dev/null | grep -qxF "$branch_name"; then
        hg update "$branch_name" >/dev/null
    else
        hg book "$branch_name" >/dev/null
    fi

    echo "$branch_name"
}

case "$vcs" in
git) do_git "$@" ;;
hg) do_hg "$@" ;;
*)
    echo "error: unsupported VCS: $vcs" >&2
    exit 1
    ;;
esac
