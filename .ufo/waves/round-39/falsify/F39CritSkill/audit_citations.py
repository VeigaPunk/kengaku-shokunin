#!/usr/bin/env python3
"""F39CritSkill audit: SKILL.md round-39 decision-table citations vs the round-39 receipt.
Run from anywhere: python3 audit_citations.py /home/vgpnk/Projects/shokunin/kengaku-shokunin
"""
import pathlib
import re
import sys

lane = pathlib.Path(sys.argv[1])
lines = (lane / "SKILL.md").read_text().splitlines()
s0 = next(i for i, l in enumerate(lines) if l.startswith("## Repository-history TB2 grader"))
i0 = next(j for j in range(s0, s0 + 40) if lines[j].startswith("### Decision table"))
i0 = next(j for j in range(i0, i0 + 10) if lines[j].startswith("|"))
rows, j = [], i0
while j < len(lines) and lines[j].startswith("|"):
    rows.append(lines[j])
    j += 1
data = rows[2:]
print(f"table rows={len(data)} (SKILL.md:{i0 + 1}-{j})")

receipt = (lane / "corpus/evidence/round39/git-leak-probe.txt").read_text().splitlines()
byline = {i: m.group(1) for i, l in enumerate(receipt, 1) if (m := re.match(r"^CASE (\S+) ", l))}
rt = {m.group(1): re.search(r"tests=([PF]{5})", l).group(1)
      for l in receipt if (m := re.match(r"^CASE (\S+) ", l))}

pairs = []
for r in data:
    cite = r.rstrip().split("|")[-2]
    pairs += [(n, int(i)) for n, i in re.findall(r"`([a-z0-9-]+)` \(receipt:(\d+)\)", cite)]
bad = [(n, i, byline.get(i)) for n, i in pairs if byline.get(i) != n]
print(f"citations={len(pairs)} resolved={len(pairs) - len(bad)} bad={bad}")

claims = [("echo-only", "PPPPP"), ("echo-gc-only", "PPPPP"), ("flag-padded-crlf", "PPPPP"),
          ("flag-extra-text", "FPPPP"), ("flag-is-directory", "FPPPP"), ("flag-in-repo-only", "FPPPF"),
          ("blob-ref-keeps-secret", "PPPPP"), ("tag-message-secret", "PPPPP"), ("config-secret", "PPPPP"),
          ("branch-keeps-leak", "PFPPP"), ("commit-message-secret", "PFPPP"), ("notes-secret", "PFPPP"),
          ("echo-reflog-expire", "PPPPP"), ("stash-secret", "PPPPP"), ("dangling-secret-blob", "PPPFP"),
          ("dangling-secret-commit", "PPPFP"), ("message-rewritten", "PPPPP"), ("history-rebuilt", "PPPPP"),
          ("dotfile-in-worktree", "PPPPP"), ("readme-edited", "PPPPF"), ("untracked-file-secret", "PPPPF"),
          ("empty-app", "FFFFF"), ("untouched", "FPPPP"), ("oracle-solve-sh", "PPPPP")]
body = "\n".join(data)
wrong = [(n, l, rt.get(n)) for n, l in claims if rt.get(n) != l]
absent = [(n, l) for n, l in claims if not (f"`{n}`" in body and l in body)]
print(f"letter claims={len(claims)} receipt_mismatch={wrong} absent_from_table={absent}")
