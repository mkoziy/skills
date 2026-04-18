#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO"

deploy() {
  local tool="$1"    # claude or codex
  local kind="$2"    # skills or agents
  local dest="$3"    # destination directory

  local src_dir="$SRC/.$tool/$kind"
  [[ -d "$src_dir" ]] || return 0

  mkdir -p "$dest"

  for item in "$src_dir"/*/; do
    [[ -d "$item" ]] || continue
    name="$(basename "$item")"
    mkdir -p "$dest/$name"
    cp -r "$item"* "$dest/$name/"
    echo "  .$tool/$kind/$name -> $dest/$name"
  done
}

echo "Deploying Claude skills..."
deploy claude skills "$HOME/.claude/skills"

echo "Deploying Claude agents..."
deploy claude agents "$HOME/.claude/agents"

echo "Deploying Codex skills..."
deploy codex skills "$HOME/.codex/skills"

echo "Deploying Codex agents..."
deploy codex agents "$HOME/.codex/agents"

echo "Done."
