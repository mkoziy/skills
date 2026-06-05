#!/bin/bash
# resolve a file through the three-layer override chain
# usage: resolve-file.sh <relative-path> [data-dir]
#
# checks in order (first-found-wins):
#   1. .codex/exec-plan/<path> (project override)
#   2. <data-dir>/<path> (user override, default: ~/.codex)
#   3. bundled default at <skill-root>/references/<path>

set -e

path="$1"
if [ -z "$path" ]; then
    echo "error: usage: resolve-file.sh <relative-path> [data-dir]" >&2
    exit 1
fi

data_dir="${2:-$HOME/.codex}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -f ".codex/exec-plan/$path" ]; then
    cat ".codex/exec-plan/$path"
elif [ -n "$data_dir" ] && [ -f "$data_dir/$path" ]; then
    cat "$data_dir/$path"
elif [ -f "$SKILL_ROOT/references/$path" ]; then
    cat "$SKILL_ROOT/references/$path"
else
    echo "error: file not found in override chain: $path" >&2
    exit 1
fi
