---
name: gcp
description: Stage changed files, create logical commits (splitting into multiple commits when changes span different concerns), and push to the remote branch.
disable-model-invocation: true
argument-hint: "[optional: guidance for commit messages]"
---

# Git Workflow: Stage, Commit, and Push

## Current state

```!
git status
```

## Changed files

```!
git diff --stat
```

## Recent commit style

```!
git log --oneline -5
```

## Current branch

```!
git branch --show-current
```

## Instructions

1. **Review the changes** shown above carefully.
2. **Stage and commit logically**:
   - If all changes are cohesive (one feature, one fix), create a single commit.
   - If changes span multiple features, fixes, or concerns, split them into separate focused commits. Stage related files together with `git add <files>` before each commit.
3. **Commit message style**: Follow the style of recent commits shown above. If no clear style exists, use imperative mood (e.g. "Fix bug" not "Fixed bug").
4. **Push**: After all commits are created, push to the remote with `git push origin $(git branch --show-current)`.
5. **Verify**: Confirm the push succeeded and show the final `git log --oneline -5`.

$ARGUMENTS
