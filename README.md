# skills

Personal skills for Claude Code and Codex.

Every skill in this repo works in both agents. The only difference is how you invoke it: Claude Code uses slash commands (`/gcp`), Codex uses dollar commands (`$gcp`).

## Installation

### As a plugin (recommended)

This repo is a plugin marketplace for both agents. Add it once, install the `skills` plugin, and updates flow through the plugin system.

Claude Code:

```
/plugin marketplace add TheEdoRan/skills
/plugin install skills@theedoran-skills
```

Codex:

```
codex plugin marketplace add TheEdoRan/skills
codex plugin add skills@theedoran-skills
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

## explain-implementation

Invoke with `/explain-implementation` (Claude Code) or `$explain-implementation` (Codex).

A detailed walkthrough of the work the agent just completed in the conversation, organized around decisions rather than files — what was built, how it works (with `file:line` references), why each non-trivial choice was made. It only runs when you ask for it; nothing is appended automatically.

- **Verified sources**: every cited link is resolved in the current session (Context7 first, then WebFetch/WebSearch). No URLs recalled from memory: if verification fails, the source is named without a link instead of fabricating one.
- **Personal knowledge memory**: `~/.claude/explain-implementation/known-concepts.md` tracks concepts already shown or declared known, so the same things are never re-explained. Shared across projects and across agents. Saying "I already know this" marks a concept as known; "explain it again" puts it back in the queue.

### Layout

```
skills/explain-implementation/
├── SKILL.md                          # the skill itself
├── references/source-verification.md
└── evals/evals.json
```

## gcp

Invoke with `/gcp` (Claude Code) or `$gcp` (Codex), optionally followed by text used as guidance for commit messages or grouping.

Stages the current changes, creates logical commits — splitting unrelated concerns into separate commits — pushes the current branch, and verifies the result. Commit messages follow the style of recent commits in the repo. It never amends, force-pushes, resets, or changes branches.

### Layout

```
skills/gcp/
├── SKILL.md
└── agents/openai.yaml   # Codex interface metadata
```

## License

MIT
