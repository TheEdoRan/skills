---
name: analyze
description: Analyzes the implementation of a feature (or the work just completed in the conversation) across security, performance, maintainability, edge cases, and test coverage, then hardens it test-first. Verifies security and library best practices against current documentation via Context7. Invoke only when the user explicitly requests `/analyze` or `$analyze`, optionally naming the feature, paths, or diff to analyze.
disable-model-invocation: true
argument-hint: "[optional: feature, paths, or diff to analyze]"
---

# Analyze Implementation

Review an implementation across five dimensions — security, performance,
maintainability, edge cases, tests — and harden it test-first. Security is the
highest-priority dimension: never skip it, never shorten it.

## Scope

- Arguments name a feature, paths, commit, or diff → analyze exactly that.
- No arguments → analyze the implementation most recently completed in this
  conversation.
- Neither exists → ask the user what to analyze; do not guess.

First resolve the scope to a concrete file list yourself, then delegate the
exploration.

## Parallel exploration via subagents

Dispatch one read-only subagent per dimension below — security, performance,
maintainability, edge cases — all in parallel, in a single batch. Each
subagent's prompt contains the resolved file list, the relevant dimension
section from this skill as its brief, and this instruction: read every file in
scope fully, trace the real flow end to end (entry points, callers, data
paths), and return only findings — each with severity, `file:line`, what is
wrong, and the suggested change — or an explicit "no issues" with what was
checked. Subagents must not edit anything; they explore and report back.

When all subagents return, the main agent merges the reports: dedupe
overlapping findings, drop anything not grounded in real code, and verify
each surviving finding against the source before acting on it. The merged
list of things to change drives the TDD hardening step; the main agent — not
the subagents — applies every change.

If the environment cannot run subagents, do the same exploration inline,
dimension by dimension, security first.

## 1. Security (highest priority)

Check every trust boundary in scope:

- Input validation on everything that crosses a boundary (user input, HTTP
  params, file contents, env vars, IPC).
- Injection: SQL, command, path traversal, template, header, XSS.
- Authentication and authorization: missing checks, confused-deputy paths,
  IDOR, privilege escalation between the analyzed endpoints.
- Secrets: hardcoded credentials, keys or tokens in logs, secrets committed
  to the repo.
- Crypto misuse, unsafe deserialization, SSRF, open redirects — whichever
  apply to the code at hand.

For each library or framework the scope depends on (auth, ORM, HTTP client,
crypto, session handling, …), verify current best practices with Context7
(`resolve-library-id` → `query-docs`), falling back to web search if Context7
lacks the library. Do not rely on memory for security guidance: check how the
code uses the library against what the current docs recommend, and flag any
deviation.

## 2. Performance

- Algorithmic complexity on hot paths; accidental O(n²) over unbounded input.
- N+1 queries, queries or network calls inside loops, missing batching.
- Blocking I/O on async paths; redundant recomputation of stable values.
- Unbounded growth: caches without eviction, accumulating listeners, leaks.

Flag only what plausibly matters at real data sizes. Micro-optimizations that
save nanoseconds are noise — say they were considered and skipped.

## 3. Maintainability

- Duplication — both within the scope and against helpers that already exist
  elsewhere in the repo (search before concluding something is unique).
- Dead code, unused parameters, speculative abstractions with one caller.
- Functions or files doing too much; misleading names; drift from the
  surrounding codebase's established patterns.

Prefer deletion and reuse over new structure.

## 4. Edge cases

Enumerate what the code does NOT handle, picking from whichever apply:
empty/null/missing input, boundary values (0, -1, max, off-by-one), malformed
or hostile input, unicode and encoding, concurrent access and re-entrancy,
partial failure of external calls (timeout, 5xx, disconnect mid-write),
clock/timezone issues, filesystem oddities (missing dirs, permissions,
symlinks). For each real gap, decide the correct behavior — that decision
becomes a test in the next step.

## 5. TDD hardening

For every confirmed defect and every unhandled edge case with local, clearly
correct behavior:

1. Write a test in the repo's existing test framework and style that captures
   the correct behavior. Run it and confirm it FAILS against the current code.
2. Apply the minimal fix. Confirm the test passes.
3. Run the full test suite for the affected area and confirm nothing broke.

Never write the fix before the failing test. A finding without a failing test
is a hypothesis, not a defect — verify it before fixing it.

Do NOT auto-fix findings that require design decisions, public API changes,
schema migrations, or new dependencies. Report those as recommendations with
a suggested approach and leave the code untouched.

## Report

End with a report the user can act on:

1. **Fixed** — each finding fixed, with severity, `file:line`, and the test
   that now guards it.
2. **Recommended, not applied** — findings needing a user decision, with the
   suggested approach and why it wasn't auto-applied.
3. **Checked, no issues** — one line per dimension confirming what was
   examined and found sound, including which library docs were verified via
   Context7.

Order findings by severity (security first). Every claim points at real code
(`file:line`) or a doc verified this session — no unverified assertions.

$ARGUMENTS
