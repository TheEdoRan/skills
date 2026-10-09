---
name: use-subagents
description: Splits the current task (or the tasks named in the arguments) into units of work and runs them through as many subagents as the work warrants, choosing the model and reasoning effort for each subagent independently to cut wall-clock time and cost while improving the quality of the final result. Invoke only when the user explicitly requests `/use-subagents` or `$use-subagents`, optionally naming the task or tasks to run.
disable-model-invocation: true
argument-hint: "[optional: the task or tasks to run with subagents]"
---

# Use Subagents

Spawn as many subagents as the task needs and the work suggests. Choose the
right model and reasoning effort for every subagent independently, based on
what that specific unit of work demands. Run as many of them in parallel as is
useful, to reduce wall-clock time and complexity, save cost, and improve both
the final output and the thinking behind it.

The user invoking this skill is the explicit opt-in to delegate, to set
per-subagent model and effort, and to fan out. Do not ask for permission to
do any of that.

## Scope

- Arguments name one or more tasks → those are the work.
- No arguments → the task currently in progress in this conversation, or the
  one the user just described.
- Neither exists → ask what to run; do not guess.

## 1. Decompose

Before spawning anything, understand the task well enough to split it. Read
what you need to read; a subagent cannot fix a bad decomposition.

Break the work into units and classify each one:

- **Independent**: no shared state, no ordering. Runs in parallel.
- **Dependent**: needs another unit's output. Runs in a later wave, or in a
  pipeline so it starts as soon as its own input is ready.
- **Keep on the main thread**: anything faster to do yourself than to brief
  (a one-file edit, a single known lookup), decisions that need the full
  conversation context, and the final integration.

Size units so each has one clear goal and one clear deliverable. Too coarse
loses parallelism; too fine wastes tokens on briefing and merging. Two
subagents must never edit the same file in parallel: give each writer a
disjoint set of files, run conflicting edits sequentially, or isolate
parallel writers in separate worktrees when the harness supports it.

Spawning has a fixed cost. Use exactly as many subagents as the work
justifies, not as many as possible: a three-minute task does not need five
agents.

## 2. Pick model and effort per subagent

Decide independently for every unit. Use the cheapest combination that will
do that unit well; spend on the units where a wrong answer is expensive.

| Unit of work | Model tier | Effort |
|---|---|---|
| File and keyword search, inventories, mechanical extraction, format conversion, summarizing known content | small and fast (e.g. `haiku`) | low |
| Well-specified implementation, writing tests or docs, a focused review of one dimension, research synthesis, routine refactors | balanced (e.g. `sonnet`) | medium |
| Architecture and planning, hard debugging, security review, concurrency, ambiguous specs, adversarial verification of other agents' output | strongest available (e.g. `opus`, or a stronger one if the harness lists it) | high |
| A single hard reasoning problem where a mistake is costly and no cheaper check exists | strongest available | xhigh or max |

Adjustments:

- Large but shallow input (many files, little judgment) → small model. Small
  input that needs deep judgment → strong model.
- If a cheap subagent's output is weak, re-run that unit one tier up. Do not
  escalate everything preemptively.
- A unit whose output will be verified by a stronger agent can run cheaper.

How to apply it per harness:

- **Claude Code**: pass `model` and `effort` on each Agent tool call. Use a
  specialized agent type when one fits (for example `Explore` for read-only
  sweeps, `Plan` for design), still setting model and effort per call.
- **Codex**: set the model and reasoning effort for each spawned agent with
  whatever the multi-agent tools expose (per-spawn overrides, or agent roles
  whose configuration sets `model` and `model_reasoning_effort`).
- If the harness cannot set model or effort per subagent, still delegate,
  and tell the user in one line which control was unavailable.

## 3. Dispatch

Before dispatching, show the user a short plan, one line per subagent:
unit, model, effort, and which wave it runs in. Then dispatch immediately
without waiting for approval.

- Send all independent units of a wave in a single message with multiple
  tool calls, so they run concurrently.
- Start each dependent unit as soon as its inputs are ready, rather than
  waiting for the whole previous wave.
- If the harness offers a workflow or orchestration tool and the plan has
  many units or stages, use it; this skill counts as the user's opt-in.

Every subagent starts with no memory of this conversation. Each prompt must
be self-contained:

1. **Goal**: what this unit must achieve and why it matters to the overall
   task.
2. **Scope**: the exact files, paths, symbols, or questions in scope, and
   what is out of scope.
3. **Constraints**: read-only or allowed to edit (and which files), project
   conventions to follow, commands it may run, and anything it must not
   touch.
4. **Deliverable**: the exact shape of what to return (findings with
   `file:line`, a diff summary, a decision with reasons) and a length limit.
   Ask for conclusions, not file dumps.
5. **Verification**: how it should check its own work before returning
   (run the tests, re-read the changed code, cite sources).

## 4. Integrate and verify

The main agent owns the result. When subagents return:

- Merge and dedupe. Resolve contradictions by checking the real code or
  docs, not by majority vote.
- Verify every claim that the final answer depends on. Treat subagent
  output as a lead, not a fact; spot-check output from small-model agents
  more strictly.
- For changes to code, run the relevant tests and linters yourself after all
  writers finish.
- If a unit failed or came back thin, re-run it with a sharper prompt or a
  stronger tier. Do not paper over the gap.
- Make sure every process a subagent started (servers, watchers, browsers)
  is stopped before you report completion.

## Report

End with a short summary for the user: what was done, the subagents used
(unit, model, effort, outcome), what was verified and how, and anything left
open. Keep subagent transcripts out of it; report conclusions.

$ARGUMENTS
