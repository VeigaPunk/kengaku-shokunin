"""FEntryQuality-2: can a '"'-bearing value yield VALID but restructured JSON under the S070 text order?"""
import json
from collections import Counter

ROOT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/"
raw = open(ROOT + "plans/fixtures/r28/webarena/config_files/test.raw.json", encoding="utf-8").read()
tasks = json.loads(raw)
ORDER = ["GITLAB", "REDDIT", "SHOPPING", "SHOPPING_ADMIN", "WIKIPEDIA", "MAP"]


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for v in obj:
            yield from leaves(v, path + "[]")
    elif isinstance(obj, str):
        yield path, obj


ctx = {n: Counter() for n in ORDER}
for t in tasks:
    for p, s in leaves(t):
        for n in ORDER:
            if f"__{n}__" in s:
                ctx[n]["array" if p.endswith("[]") else "member"] += 1
print("leaf_context_by_token", {n: dict(c) for n, c in ctx.items()})

for victim in [n for n in ORDER if ctx[n] and not ctx[n]["array"]]:
    values = {n: f"http://{n.lower()}.invalid" for n in ORDER}
    values[victim] = f'http://{victim.lower()}.invalid","zz_injected_key":"x'
    text = raw
    for n in ORDER:
        text = text.replace(f"__{n}__", values[n])
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print("victim", victim, "json_valid False", e.msg)
        continue
    inj = [t for t in data if "zz_injected_key" in t]
    dup_start = [t for t in data if t["start_url"].endswith(".invalid")]
    print("victim", victim, "json_valid True parsed", len(data),
          "tasks_with_injected_top_key", len(inj),
          "start_url_truncated_to_value", len(dup_start),
          "example", inj[0]["task_id"] if inj else None,
          repr(inj[0]["start_url"]) if inj else None,
          repr(inj[0]["zz_injected_key"][:30]) if inj else None)
