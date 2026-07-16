#!/usr/bin/env python3
"""Self-check for stop-footer.py — run: python3 test_stop_footer.py"""
import json
import os
import subprocess
import tempfile

SCRIPT = os.path.join(os.path.dirname(__file__), "stop-footer.py")


def run(entries, stop_active=False, transcript=True):
    path = None
    if transcript:
        f = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
        for e in entries:
            f.write(json.dumps(e) + "\n")
        f.close()
        path = f.name
    payload = {"stop_hook_active": stop_active}
    if path:
        payload["transcript_path"] = path
    out = subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                         capture_output=True, text=True)
    if path:
        os.unlink(path)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


user = {"type": "user", "message": {"content": "add a feature"}}
edit = {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Edit", "input": {}}]}}
text = {"type": "assistant", "message": {"content": [{"type": "text", "text": "done"}]}}
footer = {"type": "assistant", "message": {"content": [{"type": "text", "text": "---\n\U0001F4DA During this implementation: ..."}]}}
toolres = {"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}}

assert "additionalContext" in run([user, edit, text])          # edits -> reminder
assert run([user, text]) == ""                                  # no edits -> silent
assert run([user, edit, footer]) == ""                          # footer present -> silent
assert run([user, edit, text], stop_active=True) == ""          # already extended -> silent
assert run([{"type": "user", "message": {"content": "old"}}, edit, user, text]) == ""  # edits in prev turn
assert "additionalContext" in run([user, edit, toolres, text])  # tool_result doesn't reset turn
assert run([], transcript=False) == ""                          # unknown payload -> silent

f = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
f.write("not json\n" + json.dumps(user) + "\n" + json.dumps(edit) + "\n")
f.close()
out = subprocess.run(["python3", SCRIPT], input=json.dumps({"transcript_path": f.name}),
                     capture_output=True, text=True)
assert "additionalContext" in out.stdout                        # malformed line tolerated
os.unlink(f.name)

print("all 8 checks passed")
