---
name: explain-fix
description: Analyzes the implementation of a feature (or the work just completed in the conversation) across security, performance, maintainability, and edge cases, then hardens it test-first — same analysis as the `explain` skill, but the fixes are applied instead of left to the user. Invoke only when the user explicitly requests `/explain-fix` or `$explain-fix`, optionally naming the feature, paths, or diff to analyze.
disable-model-invocation: true
argument-hint: "[optional: feature, paths, or diff to analyze]"
---

# Explain and Fix Implementation

Two phases: analyze, then fix.

## Phase 1: Explain

Read `../explain/SKILL.md` (relative to this skill's directory) and follow it
end to end — same scope resolution, same parallel subagent exploration, same
four dimensions with security first, same `explain-report.md` written to the
repo root. Its read-only rule applies to this phase only: once the report is
written, continue below instead of stopping.

## Phase 2: TDD hardening

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

Update `explain-report.md` so each finding is marked **fixed** (with the test
that now guards it) or **recommended, not applied** (with why). Then end with
a short summary in the conversation:

1. **Fixed** — each finding fixed, with severity, `file:line`, and the test
   that now guards it.
2. **Recommended, not applied** — findings needing a user decision, with the
   suggested approach.
3. Path to the updated `explain-report.md`.

$ARGUMENTS
