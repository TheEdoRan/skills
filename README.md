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
<summary><b>analyze</b> — five-dimension implementation review with test-first hardening</summary>

Invoke with `/analyze` (Claude Code) or `$analyze` (Codex), optionally followed by the feature, paths, or diff to analyze; with no arguments it targets the implementation just completed in the conversation.

Reviews an implementation across five dimensions — security (highest priority), performance, maintainability, edge cases, and test coverage — then hardens it test-first. Each dimension is explored by a read-only subagent, all running in parallel; they report findings back to the main agent, which merges and verifies them and applies every change itself.

- **Security first**: trust boundaries, injection, authn/authz, secrets, and crypto misuse are always checked, and library usage is verified against current documentation via Context7 rather than recalled from memory.
- **TDD hardening**: every confirmed defect and unhandled edge case gets a failing test before the fix; findings that would need design decisions, API changes, or new dependencies are reported as recommendations instead of auto-applied.
- **Actionable report**: findings ordered by severity with `file:line` references, split into fixed, recommended-but-not-applied, and checked-with-no-issues.

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
