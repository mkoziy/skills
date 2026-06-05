#!/bin/bash
# run codex review and return output
# usage: run-codex.sh "<prompt>"

set -e

prompt="$1"
if [ -z "$prompt" ]; then
    echo "error: usage: run-codex.sh '<prompt>'" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
vcs=$(bash "$SCRIPT_DIR/detect-vcs.sh")

args=("exec")
[ "$vcs" = "hg" ] && args+=("--skip-git-repo-check")
args+=("--sandbox" "read-only")

if [ "${CODEX_NO_OVERRIDES:-}" != 1 ]; then
    args+=(
        "-c" "model=${CODEX_MODEL:-gpt-5.5}"
        "-c" "model_reasoning_effort=xhigh"
        "-c" "stream_idle_timeout_ms=3600000"
        "-c" "project_doc=$HOME/.claude/CLAUDE.md"
        "-c" "project_doc=./CLAUDE.md"
    )
fi

codex "${args[@]}" "$prompt" < /dev/null
