---
name: explain-implementation
description: Use after you finish writing code, or when the user asks about code you just wrote in this conversation. (1) Footer mode — a coding task (feature, fix, refactor) is done and you used something a mid-level dev wouldn't reach for by default (obscure API or hook, deliberate non-idiomatic pattern, trade-off-laden algorithm, little-known documented behavior); append a short footer naming it with a source you actually verified. Also fires when the coding request itself asks you to teach afterwards ("...then explain anything non-obvious you used"), or when a Stop-hook reminder asks. (2) Deep mode — the user wants a walkthrough of your just-completed work (what you built, why, the tricky parts — often before a review or PR), especially when they want real, verified doc links; any language ("explain what you implemented", "walk me through what you did", "/explain-implementation"). Also fires when they push back on a footer concept ("I already know this", "explain it again") — update the knowledge memory accordingly. Not for pre-existing code you didn't write, general concept tutorials, changelogs, or docstrings.
---

# Explain Implementation

Help the user actually learn from the code you write for them. Two modes share
the same three pillars: **notability filtering** (only what's genuinely
non-obvious), **verified sources** (never cite a URL you did not check this
session), and **personal knowledge memory** (don't re-teach what the user has
already seen or knows).

## Why these rules exist

- A footer on every task becomes banner blindness: the user stops reading it,
  and the tokens are wasted. Rarity is what makes it valuable.
- URLs recalled from memory are the single most common hallucination in
  "cited" output: they look plausible and are wrong just often enough to
  destroy trust. A source you haven't verified this session is worse than no
  source — omit the citation (or the whole item) instead.
- Repeating explanations the user already has teaches nothing and erodes the
  signal of the footer. The memory file exists so novelty is real novelty.

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
- `shown` — a footer or deep dive already presented this concept. Skip it in
  future footers; deep mode may still cover it briefly.
- `known` — the user explicitly said they know it. Skip it everywhere unless
  they ask.
- `re-explain` — the user asked to see it again. Treat as unknown; after
  re-explaining, set it back to `shown`.

Maintenance: when the user says they already know a concept ("I know this",
"I already know that"), update its line to `known` (add the line if missing).
When they ask to have something re-explained, set it to `re-explain`. Create
the file and parent directory on first use. Keep slugs kebab-case and stable
so the same concept always matches.

## Source verification protocol

Applies to BOTH modes. Full details and edge cases:
[references/source-verification.md](references/source-verification.md).

The short version: before citing anything, resolve it against real
documentation **in this session** — Context7 first (library/framework APIs),
WebFetch/WebSearch as fallback (specs, RFCs, platform docs). Cite only URLs
that a tool call actually returned or confirmed. If verification fails or the
tools are unavailable, say what the concept is and name the authoritative
place to look ("the React docs page on useSyncExternalStore") WITHOUT a URL —
never fabricate one.

## Footer mode

Run this after completing an implementation, when either the description
triggered you or a Stop-hook reminder asked for it.

1. **Collect candidates.** Scan only the work from this task (the diff you
   produced, not pre-existing code) for techniques that pass the notability
   bar: would a mid-level developer in this stack write this by default? If
   yes, it is obvious — drop it. Notable examples: a rarely used API or hook,
   a non-idiomatic pattern chosen deliberately, an algorithmic choice with a
   real trade-off, documented-but-little-known behavior you relied on.
   Standard CRUD, common hooks, ordinary error handling, idiomatic loops are
   never notable.
2. **Filter against memory.** Read the knowledge memory. Drop candidates whose
   concept is `shown` or `known`.
3. **Cap at 2.** If more survive, keep the two the user is least likely to
   have met. Learning happens one or two concepts at a time.
4. **Verify sources** for the survivors (protocol above). A candidate whose
   source cannot be verified may still appear with the no-URL fallback if it
   is genuinely valuable; otherwise drop it.
5. **Nothing survived → no footer.** Do not write "nothing notable this time"
   — silence is the correct output, and most implementations should end in
   silence.
6. **Emit the footer** after your normal completion summary, in the language
   of the conversation:

   ```
   ---
   📚 During this implementation:
   - **useSyncExternalStore** — subscribing to an external store without
     tearing during concurrent rendering. ([React docs](https://react.dev/reference/react/useSyncExternalStore))
   ```

7. **Record exposure.** Append each footer item to the memory file as `shown`
   with today's date.

## Deep mode (/explain-implementation)

When invoked, produce a detailed explanation of the implementation just
completed in this conversation (if ambiguous, the most recent one; if the user
names a diff/commit, use that scope).

Structure the walkthrough around decisions, not files:

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
a deep dive, record newly explained concepts in the memory as `shown`.

## Scope guard

Both modes explain work done in this conversation by the agent. If asked to
explain pre-existing code the agent didn't write, deep mode still works, but
say explicitly that the rationale ("why") is inferred from the code, not
known from authorship.
