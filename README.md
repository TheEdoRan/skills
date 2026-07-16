# skills

Personal plugins and skills for Claude Code and Codex. The repo doubles as a plugin marketplace (`theedoran-skills`, defined in `.claude-plugin/marketplace.json`).

## Installation

### Claude Code

Add the marketplace once, then install the plugin from it:

```
/plugin marketplace add theedoran/skills
/plugin install explain-implementation@theedoran-skills
```

You can also run `/plugin` to browse the marketplace interactively. To update later, run `/plugin marketplace update theedoran-skills`.

### Codex

Codex (CLI >= 0.144) uses the same slash commands:

```
/plugin marketplace add theedoran/skills
/plugin install explain-implementation@theedoran-skills
```

Run `/plugins` to open the plugin browser, and `/reload-plugins` after installing. Each plugin ships a `.codex-plugin/plugin.json` manifest, so Codex picks up the skills and the Stop hook natively.

### Manual (either tool)

Clone the repo and copy the plugin directory into your plugins folder:

```
git clone https://github.com/theedoran/skills
cp -r skills/explain-implementation ~/.claude/plugins/   # Claude Code
cp -r skills/explain-implementation ~/.codex/plugins/    # Codex
```

## explain-implementation

A plugin that helps you actually learn from the code the agent writes for you, without drowning you in explanations. Three pillars:

- **Notability filtering**: only what a mid-level developer would not write by default gets explained (obscure APIs, deliberately non-idiomatic patterns, algorithmic trade-offs). Standard CRUD and idiomatic code stay silent.
- **Verified sources**: every cited link is resolved in the current session (Context7 first, then WebFetch/WebSearch). No URLs recalled from memory: if verification fails, the source is named without a link instead of fabricating one.
- **Personal knowledge memory**: `~/.claude/explain-implementation/known-concepts.md` tracks concepts already shown or declared known, so the same things are never re-explained. Shared across projects and across agents.

### Two modes

1. **Footer**: at the end of an implementation, if (and only if) something genuinely non-obvious was used, the agent appends a short footer with at most 2 concepts, each with a verified source. Nothing notable means no footer at all.
2. **Deep dive** (`/explain-implementation`): a detailed walkthrough of the work just completed, organized around decisions rather than files: what was built, how it works (with `file:line` references), why each non-trivial choice was made, with verified sources for every technical claim.

Saying "I already know this" marks the concept as known (it will not be shown again); "explain it again" puts it back in the queue.

### Layout

```
explain-implementation/
├── .claude-plugin/plugin.json   # Claude Code manifest
├── .codex-plugin/plugin.json    # Codex manifest
├── skills/explain-implementation/
│   ├── SKILL.md                 # the skill itself
│   ├── references/source-verification.md
│   └── evals/evals.json
└── hooks/
    ├── hooks.json               # Stop hook
    └── stop-footer.py           # reminds about the footer after file-modifying turns
```

The Stop hook only fires after turns that modified files, reminding the agent to consider the footer.

## License

MIT
