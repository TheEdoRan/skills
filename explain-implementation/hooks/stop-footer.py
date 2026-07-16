#!/usr/bin/env python3
"""Stop hook: if this turn modified files and no footer was emitted yet,
remind the agent to apply the explain-implementation skill in footer mode.

Exit 0 with no output = let the turn end silently (the common case)."""
import json
import sys

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
FOOTER_MARKER = "\U0001F4DA"  # 📚

REMINDER = (
    "This turn modified files. If that completed an implementation that used "
    "any genuinely non-obvious technique (rare API/hook, non-idiomatic "
    "pattern, algorithmic trade-off, little-known documented behavior), apply "
    "the explain-implementation skill in footer mode: max 2 items, filtered "
    "against ~/.claude/explain-implementation/known-concepts.md, every URL "
    "verified via Context7/WebFetch before citing (omit unverifiable URLs). "
    "If nothing notable was used, or the implementation is not finished, end "
    "your turn now with no added text — do not announce that there is nothing "
    "to explain."
)


def turn_state(transcript_path):
    """Return (edits_in_turn, footer_already_emitted) for the current turn."""
    last_user = -1
    entries = []
    with open(transcript_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            entries.append(entry)

    for i, entry in enumerate(entries):
        if entry.get("type") != "user" or entry.get("isMeta"):
            continue
        content = entry.get("message", {}).get("content")
        # A genuine prompt is a string, or a list with a text block and no
        # tool_result blocks (tool results also arrive as "user" entries).
        if isinstance(content, str):
            last_user = i
        elif isinstance(content, list):
            kinds = {c.get("type") for c in content if isinstance(c, dict)}
            if "tool_result" not in kinds and "text" in kinds:
                last_user = i

    edits = False
    footer = False
    for entry in entries[last_user + 1:]:
        if entry.get("type") != "assistant":
            continue
        for block in entry.get("message", {}).get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") in EDIT_TOOLS:
                edits = True
            if block.get("type") == "text" and FOOTER_MARKER in block.get("text", ""):
                footer = True
    return edits, footer


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    if payload.get("stop_hook_active"):
        return  # a Stop hook already extended this turn once; never loop

    transcript = payload.get("transcript_path")
    if not transcript:
        return  # unknown host (e.g. different Codex payload) — stay silent

    try:
        edits, footer = turn_state(transcript)
    except OSError:
        return

    if edits and not footer:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": REMINDER,
            }
        }))


if __name__ == "__main__":
    main()
