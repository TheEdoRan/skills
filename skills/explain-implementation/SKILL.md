---
name: explain-implementation
description: Explains a completed implementation as a decision-oriented walkthrough of what changed, how it works with file:line references, and why key choices were made. Uses session-verified documentation and a persistent knowledge memory to avoid repeating known concepts. Invoke only when the user explicitly requests `/explain-implementation` or asks to explain or walk through an implementation; do not use for unsolicited post-task summaries, general concept tutorials, changelogs, or docstrings.
---

# Explain Implementation

On explicit request, help the user actually learn from the code you wrote for
them. Two pillars: **verified sources** (never cite a URL you did not check
this session) and a **personal knowledge memory** (don't re-teach what the
user has already seen or knows).

## Why these rules exist

- URLs recalled from memory are the single most common hallucination in
  "cited" output: they look plausible and are wrong just often enough to
  destroy trust. A source you haven't verified this session is worse than no
  source — omit the citation (or the whole item) instead.
- Repeating explanations the user already has teaches nothing. The memory
  file exists so novelty is real novelty.

## The knowledge memory

Path: `~/.claude/explain-implementation/known-concepts.md` (shared across
projects and across agents — Codex uses the same file).

Format — one line per concept:

```
react-use-sync-external-store | 2026-07-16 | shown
postgres-advisory-locks | 2026-07-02 | known
css-anchor-positioning | 2026-06-20 | re-explain
```

States:
- `shown` — a previous walkthrough already presented this concept. Cover it
  briefly, don't re-teach from scratch.
- `known` — the user explicitly said they know it. Skip it unless they ask.
- `re-explain` — the user asked to see it again. Treat as unknown; after
  re-explaining, set it back to `shown`.

Maintenance: when the user says they already know a concept ("I know this",
"I already know that"), update its line to `known` (add the line if missing).
When they ask to have something re-explained, set it to `re-explain`. Create
the file and parent directory on first use. Keep slugs kebab-case and stable
so the same concept always matches.

## Source verification protocol

Full details and edge cases:
[references/source-verification.md](references/source-verification.md).

The short version: before citing anything, resolve it against real
documentation **in this session** — Context7 first (library/framework APIs),
WebFetch/WebSearch as fallback (specs, RFCs, platform docs). Cite only URLs
that a tool call actually returned or confirmed. If verification fails or the
tools are unavailable, say what the concept is and name the authoritative
place to look ("the React docs page on useSyncExternalStore") WITHOUT a URL —
never fabricate one.

## The walkthrough

Explain the implementation just completed in this conversation (if ambiguous,
the most recent one; if the user names a diff/commit, use that scope).

Structure it around decisions, not files:

1. **What was built** — two or three sentences of outcome.
2. **How it works** — the key flow, referencing real files as `path:line`.
3. **Decisions and techniques** — for each non-trivial choice: what it is, why
   this over the alternative, and a verified source for every technical claim
   about an API, language feature, or documented behavior. Repo-specific
   rationale ("this matched the existing pattern in X") needs no external
   source — point to the code instead. Cover `shown` concepts briefly;
   respect `known` ones unless asked.
4. **Sources** — a final list of every verified link used above.

Ground every claim in either the actual diff/code (cite the location) or a
verified document (cite the URL). A claim you cannot ground gets labeled
"(not verified — check before relying on this)". Never silently guess. After
the walkthrough, record newly explained concepts in the memory as `shown`
with today's date.

## Browser view

After delivering the walkthrough in chat, produce a browser-viewable copy:

1. Write the same walkthrough as a **single self-contained HTML file** — all
   CSS inline, no external scripts, fonts, or images — so it renders offline
   and can be moved or shared as one file. Author the HTML directly from the
   walkthrough you just wrote (no pandoc or other converter). Use readable
   typography: a max-width text column, styled headings and links, monospace
   code blocks.
2. Save it to `~/.claude/explain-implementation/walkthroughs/YYYY-MM-DD-<topic-slug>.html`
   (create the directory on first use). The file persists there, so the user
   can re-open, copy, or share it later.
3. Open it in the default browser: `open <file>` on macOS,
   `xdg-open <file>` on Linux, `start "" <file>` on Windows.
4. End the chat message with the saved file path so the user knows where the
   file lives.

Sources in the HTML are the same verified links from the walkthrough — the
verification protocol applies unchanged.

## Scope guard

This skill explains work done in this conversation by the agent, on explicit
request only. If asked to explain pre-existing code the agent didn't write,
the walkthrough still works, but say explicitly that the rationale ("why") is
inferred from the code, not known from authorship.
