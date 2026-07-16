---
name: gcp
description: Stage changed files, create logical commits, split unrelated concerns into separate commits, push the current branch, and verify the result. Use only when the user explicitly invokes $gcp or asks to run the GCP git workflow; accept any accompanying text as optional commit-message guidance.
---

# Git Workflow: Stage, Commit, and Push

Run the following workflow in the current repository.

1. Inspect the repository before changing anything:
   - Run `git status --short --branch`.
   - Run `git diff --stat` and review the full relevant diffs.
   - Run `git diff --cached --stat` and review any already-staged changes.
   - Run `git log --oneline -5` to learn the repository's commit-message style.
   - Run `git branch --show-current` and confirm it returns a branch name.
2. Treat any text supplied with the invocation as guidance for commit messages or grouping. Do not let it override the requirement to inspect and logically separate changes.
3. Group changes by concern:
   - Create one commit when all changes form one cohesive feature or fix.
   - Create separate focused commits when changes span unrelated features, fixes, refactors, tests, or documentation.
   - Preserve pre-existing staged changes. Do not unstage or rewrite them unless required to make the requested logical commits, and explain the reason if so.
   - Do not include unrelated untracked files or secrets.
4. Stage each group explicitly with `git add -- <paths>`, inspect the staged diff with `git diff --cached`, then commit it.
5. Match the recent commit-message style. If no clear style exists, use a concise imperative subject.
6. After all intended changes are committed, push with `git push origin "$(git branch --show-current)"`.
7. Verify the push succeeded. Report the created commit or commits and show the final `git status --short --branch` and `git log --oneline -5`.

Never amend, force-push, reset, discard changes, bypass hooks, or change branches unless the user explicitly asks.
