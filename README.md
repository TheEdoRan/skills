# skills

Personal skills for Claude Code and Codex.

Every skill in this repo works in both agents. The only difference is how you invoke it: Claude Code uses slash commands (`/gcp`), Codex uses dollar commands (`$gcp`).

## Installation

### As a plugin (recommended)

This repo is a plugin marketplace for both agents — each one reads its own native manifest (`.claude-plugin/` for Claude Code, `.agents/plugins/` + `.codex-plugin/` for Codex). Add it once, install the `theedoran` plugin, and updates flow through the plugin system.

Claude Code:

```
/plugin marketplace add TheEdoRan/skills
/plugin install theedoran@theedoran-skills
```

Codex:

```
codex plugin marketplace add TheEdoRan/skills
codex plugin add theedoran@theedoran-skills
```

Start a new session after installing so the bundled skills are picked up.

### As standalone skills

With the [skills CLI](https://github.com/vercel-labs/skills):

```
npx skills add TheEdoRan/skills                              # pick interactively
npx skills add TheEdoRan/skills --skill gcp                  # or a specific skill
npx skills add TheEdoRan/skills --skill explain-implementation
```

Or manually — clone the repo and copy a skill directory into your agent's skills folder:

```
git clone https://github.com/TheEdoRan/skills
cp -r skills/skills/<skill-name> ~/.claude/skills/   # Claude Code
cp -r skills/skills/<skill-name> ~/.agents/skills/   # Codex
```

## Skills

<details>
<summary><b>explain</b> — read-only implementation review reported to a markdown file</summary>

Invoke with `/explain` (Claude Code) or `$explain` (Codex), optionally followed by the feature, paths, or diff to analyze; with no arguments it targets the implementation just completed in the conversation.

Reviews an implementation across four dimensions — security (highest priority), performance, maintainability, and edge cases — and changes no code. Each dimension is explored by a read-only subagent, all running in parallel; the main agent merges and verifies the findings and writes them to `explain-report.md` at the repo root. You then reference that file to write a plan or a fix prompt yourself — or run `explain-fix` to have the fixes applied.

- **Security first**: trust boundaries, injection, authn/authz, secrets, and crypto misuse are always checked, and library usage is verified against current documentation via Context7 rather than recalled from memory.
- **Actionable report**: findings ordered by severity with `file:line` references and a concrete suggested fix each, plus a checked-with-no-issues section per dimension.

</details>

<details>
<summary><b>explain-fix</b> — the explain review plus test-first hardening</summary>

Invoke with `/explain-fix` (Claude Code) or `$explain-fix` (Codex), with the same optional arguments as `explain`.

Runs the full `explain` review (including the `explain-report.md` report), then hardens the code test-first: every confirmed defect and unhandled edge case gets a failing test before the minimal fix, and the affected test suite is re-run afterwards. Findings that would need design decisions, API changes, schema migrations, or new dependencies are reported as recommendations instead of auto-applied, and the report is updated to mark each finding fixed or recommended.

</details>

<details>
<summary><b>explain-implementation</b> — decision-oriented walkthrough of the work just completed</summary>

Invoke with `/explain-implementation` (Claude Code) or `$explain-implementation` (Codex).

A detailed walkthrough of the work the agent just completed in the conversation, organized around decisions rather than files — what was built, how it works (with `file:line` references), why each non-trivial choice was made. It only runs when you ask for it; nothing is appended automatically.

- **Verified sources**: every cited link is resolved in the current session (Context7 first, then WebFetch/WebSearch) and cited inline with numbered footnotes. No URLs recalled from memory: if verification fails, the source is named without a link instead of fabricating one.
- **Personal knowledge memory**: `~/.claude/explain-implementation/known-concepts.md` tracks concepts already shown or declared known, so the same things are never re-explained. Shared across projects and across agents. Saying "I already know this" marks a concept as known; "explain it again" puts it back in the queue.
- **Browser view**: each walkthrough is also saved as a self-contained HTML page and opened in the browser, with copy/download buttons for the markdown source.

</details>

<details>
<summary><b>gcp</b> — stage, logically commit, and push</summary>

Invoke with `/gcp` (Claude Code) or `$gcp` (Codex), optionally followed by text used as guidance for commit messages or grouping.

Stages the current changes, creates logical commits — splitting unrelated concerns into separate commits — pushes the current branch, and verifies the result. Commit messages follow the style of recent commits in the repo. It never amends, force-pushes, resets, or changes branches.

</details>

## License

MIT
