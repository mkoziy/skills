#!/bin/bash
# resolve custom rules file from project-level override
# usage: resolve-rules.sh <filename>
# e.g.: resolve-rules.sh planning-rules.md
#
# checks in order (first-found-wins):
#   1. .codex/<filename> (project override)
#
# outputs file content to stdout if found, empty output if not
# always exits 0

filename="$1"
if [ -z "$filename" ]; then
    exit 0
fi

if [ -f ".codex/$filename" ] && [ -s ".codex/$filename" ]; then
    cat ".codex/$filename"
fi

exit 0
