#!/usr/bin/env python3
"""Gate prose facts: S-row mentions, admit/reject tokens, verdict tokens per lesson file."""
import re, pathlib

L = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons")

def gate_body(text):
    lines = text.splitlines()
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            on = ln[3:].strip().lower().startswith("gate")
            continue
        if on:
            out.append(ln)
    return "\n".join(out)

for n in (57, 58, 59, 60, 61, 62):
    t = (L / f"round-{n}.md").read_text(encoding="utf-8")
    g = gate_body(t)
    srows = sorted(set(re.findall(r"\bS(\d{3})\b", g)), key=int)
    print(f"##### round-{n}.md")
    print(f"  S-rows cited in Gate: {['S'+s for s in srows]}")
    for pat in (r"admit\w*", r"reject\w*", r"no rejections", r"rejections this round[^\n.]*",
                r"supersed\w*", r"no flips[^\n.]*", r"REJECT-equivalent[^\n.]*"):
        hits = re.findall(pat, g, re.I)
        if hits:
            uniq = []
            for h in hits:
                if h.lower() not in [u.lower() for u in uniq]:
                    uniq.append(h)
            print(f"  /{pat}/ -> {uniq}")
    print("  -- gate verdict-ish sentences --")
    for ln in g.splitlines():
        if re.search(r"\b(pass|fail|admit|reject|flip|PREDICATE)\b", ln, re.I):
            print(f"     {ln.strip()[:180]}")
    print()
