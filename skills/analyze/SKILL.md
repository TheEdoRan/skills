---
name: analyze
description: Read-only analysis of a feature's implementation (or the work just completed in the conversation) across security, performance, maintainability, and edge cases. Writes findings to a markdown report file for the user to act on; changes no code. Verifies security and library best practices against current documentation via Context7. Invoke only when the user explicitly requests `/analyze` or `$analyze`, optionally naming the feature, paths, or diff to analyze.
disable-model-invocation: true
argument-hint: "[optional: feature, paths, or diff to analyze]"
---

# Analyze Implementation

Review an implementation across four dimensions — security, performance,
maintainability, edge cases — and report the findings. Security is the
highest-priority dimension: never skip it, never shorten it.

**This skill is strictly read-only.** It never edits, creates, or deletes any
project file. The only file it writes is the report described at the end. The
user decides what to do with the findings — do not fix anything, do not offer
to fix anything mid-analysis. (The `analyze-fix` skill exists for when the
user wants the fixes applied.)

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
each surviving finding against the source before including it in the report.

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
symlinks). For each real gap, state what the correct behavior should be —
that goes in the report as the suggested fix.

## Report

Write the full report to `analyze-report.md` at the root of the analyzed
repository (overwriting any previous run). Structure it so the user can hand
it straight back to an agent as a plan or fix prompt:

1. **Scope** — what was analyzed (feature, paths, commit) and when.
2. **Findings** — ordered by severity, security first. Each finding:
   severity, `file:line`, what is wrong, why it matters, and a concrete
   suggested fix (including the test that should guard it, where applicable).
   Flag findings that need a design decision, public API change, schema
   migration, or new dependency as such.
3. **Checked, no issues** — one line per dimension confirming what was
   examined and found sound, including which library docs were verified via
   Context7.

Every claim points at real code (`file:line`) or a doc verified this session
— no unverified assertions.

In the conversation, give the user only a short summary: finding count per
severity, the single most important finding, and the path to
`analyze-report.md`. Then stop — apply nothing.

$ARGUMENTS
