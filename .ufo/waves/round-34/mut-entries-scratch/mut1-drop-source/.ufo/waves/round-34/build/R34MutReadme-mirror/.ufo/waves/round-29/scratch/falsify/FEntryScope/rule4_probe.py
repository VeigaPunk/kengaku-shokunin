"""Probe decision-rule step (4) and line 30-32 failure-mode claim with generator lines 11-20 semantics
re-typed from the pinned generator bytes. Synthetic *.invalid values only."""
import json
import re

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", encoding="utf-8").read()
base = json.load(open(ROOT + "plans/fixtures/r29/profiles.json"))["distinct_origins"]["values"]
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]
data = json.loads(raw)
print("task0_key_order", list(data[0].keys()))


def run(label, override):
    vals = dict(base, **override)
    text = raw
    for n in ORDER:
        text = text.replace(f"__{n}__", vals[n])
    try:
        proj = json.loads(text)
    except json.JSONDecodeError as e:
        print(label, "JSONDecodeError", e.msg)
        return
    remaining = sum(text.count(f"__{n}__") for n in ORDER)
    idx_mismatch = sum(1 for i, t in enumerate(proj) if t.get("task_id") != i)
    extra_keys = sum(1 for t0, t1 in zip(data, proj) if set(t1) - set(t0))
    print(label, "parsed", len(proj), "remaining_tokens", remaining,
          "index_ne_task_id", idx_mismatch, "tasks_with_extra_keys", extra_keys,
          "task0_start_url", repr(proj[0]["start_url"]), "task0_task_id", proj[0]["task_id"])


run("quote_injection", {"GITLAB": 'http://g.invalid", "injected": "x'})
run("quote_injection_dupkey", {"MAP": 'http://m.invalid", "task_id": 9999, "z": "'})
run("control_char_newline", {"GITLAB": "http://g.invalid\n"})
run("control_char_tab", {"GITLAB": "http://g\t.invalid"})
run("backslash_n", {"GITLAB": "http://g.invalid\\n"})
run("trailing_backslash", {"GITLAB": "http://g.invalid\\"})
