### Step 9: Create Release

Only after user confirms:

**GitHub:**
```bash
gh release create "$new_version" \
    --title "Version ${new_version#v}" \
    --notes "$notes"
```

**GitLab:**
```bash
glab release create "$new_version" \
    --name "Version ${new_version#v}" \
    --notes "$notes"
```

**Gitea:**
```bash
tea release create \
    --tag "$new_version" \
    --title "Version ${new_version#v}" \
    --note "$notes"
```

### Step 10: Report Result

Show new version, release URL, and confirm it was published.

## Edge Cases

| Case | Handling |
|------|----------|
| No previous tags | Default version based on type |
| Pre-release tag (v1.2.3-rc1) | Strip suffix, use base version |
| No PRs/MRs found | Show commits only |
| Tag already exists | Error and abort |
| No CHANGELOG file | Skip changelog update |
| Unknown CHANGELOG format | Ask user or use simple `## vX.Y.Z` format |

## Notes

- Tag format: `vX.Y.Z`
- Title format: `Version X.Y.Z`
- Entry format: `- description #123 @author` (PRs) or `- description abc1234` (commits)
- Grouped by type: New Features (feat), Improvements (refactor/perf/chore/docs), Bug Fixes (fix), Other
- Conventional commit prefix stripped from description for cleaner output
- Always show preview and get confirmation before publishing
