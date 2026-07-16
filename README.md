# skills

Personal skills for Claude Code and Codex.

## Installation

Clone the repo and copy the skill directory into your skills folder:

```
git clone https://github.com/TheEdoRan/skills
cp -r skills/explain-implementation ~/.claude/skills/   # Claude Code
cp -r skills/explain-implementation ~/.codex/skills/    # Codex
```

## explain-implementation

An `/explain-implementation` command: a detailed walkthrough of the work the agent just completed in the conversation, organized around decisions rather than files — what was built, how it works (with `file:line` references), why each non-trivial choice was made. It only runs when you ask for it; nothing is appended automatically.

- **Verified sources**: every cited link is resolved in the current session (Context7 first, then WebFetch/WebSearch). No URLs recalled from memory: if verification fails, the source is named without a link instead of fabricating one.
- **Personal knowledge memory**: `~/.claude/explain-implementation/known-concepts.md` tracks concepts already shown or declared known, so the same things are never re-explained. Shared across projects and across agents. Saying "I already know this" marks a concept as known; "explain it again" puts it back in the queue.

### Layout

```
explain-implementation/
├── SKILL.md                          # the skill itself
├── references/source-verification.md
└── evals/evals.json
```

## License

MIT
