# F42ReopenRows — live re-open of S125–S128 (kengaku r42 wave 2)

Scout, read-only. Scratch: /fast/scratch/hyaku/kengaku-r42/F42ReopenRows (files left for the trap-less shell; contains only the 3 raw files + i.json, <30 KB).
No bwrap envelope needed: seat ran no battery/counter/fixture builder, only `curl`, `gh api`, `cmp`, `sha256sum`, `sed`, `grep`, `python3 -c` (reads). Receipt times: `date +%T` 18:03:19 before, 18:03:50 after; `ls -A /home/vgpnk/.local/bin | sha256sum` before and after both `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` (unchanged). Live access instant (UTC): 2026-10-26T21:03:35Z = 18:03 -03.
Lane compared against: working tree at tip 445e81f (SOURCES.md lines 140-143).

## S125 / S126 / S127 — raw capture vs evidence dir
Command: `curl -sS -w "%{http_code}" -o <f> https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/<tests/test_outputs.py|instruction.md|tests/sim.c>` → HTTP 200 ×3.
`cmp <live> corpus/evidence/round42/tb2-circuit-fibsqrt/<f>` → byte-identical ×3 (`same test_outputs.py`, `same instruction.md`, `same sim.c`).
sha256 live (all match the SOURCES.md cell and evidence SHA256SUMS):
- test_outputs.py 6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438
- instruction.md a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea
- sim.c 700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173
Line counts `wc -l`: test_outputs.py 147, instruction.md 13, sim.c 353 — match the cited ranges 1-147 / 1-13 / 1-353.

Anchors located:
- S125 `:23`: `sed -n 23p` → `assert line_count < 32000, f"gates.txt has {line_count} lines…` — quote "assert line_count < 32000" (4 words) present at :23. grep finds it only at line 23. OK.
- S126 `:8`: `sed -n 8p` → `Initially, the first 32 lines are defined by the binary representation of stdin.` — quote (12 words) present at :8. OK.
- S127: `grep -n 'for (int step = 0; step < 32000; step++)' sim.c` → only `335:`. `sed -n 319p` → `    parse_gates("gates.txt");` (does NOT contain the quoted loop). The cell reads `:319, :335 "for (int step …)"` — two line numbers, one quote; the quote is at :335 only. Quote text itself (9 words) is exact.

State words: S125–S127 have no state column (pinned-commit raw files; immutable by commit hash). Rows say "accessed 2026-10-26" in the knowledge entry source lines; live fetch confirms still 200 and unchanged.

## S128 — OpenAgents issue #9645
Command: `gh api repos/OpenAgentsInc/openagents/issues/9645` → number 9645; title `Audit circuit grader coverage beyond its 48,401 input ceiling` (matches cell); state `closed`; state_reason `completed`; created_at `2026-09-25T09:01:50Z`; closed_at `2026-09-25T09:11:26Z`; updated_at `2026-09-25T09:11:26Z`; html_url https://github.com/OpenAgentsInc/openagents/issues/9645.
All of created_at, state closed, closed_at in the cell match live exactly. No edit since close (updated_at == closed_at), so the quote has not moved.
Body split on `\n`: line 1 `## Problem`, line 2 blank, line 3 the paragraph (body line 3 as cited — OK; "paragraph 1" is the first paragraph under the heading, consistent).
Quote check: `'The official grader exercises 28 values, none above 48,401.' in body` → True (9 words). The paragraph also states "All six submitted simulator sources match … SHA-256 700645ac…" — equals S127's sha256, an independent corroboration of the pinned sim.c.
Access-time cell `2026-10-26 17:35 -03` is the L1's earlier open (past, not wrong); live re-open 18:03 -03 agrees on every state word.

## Wrong cells: 0 factual; 1 locator ambiguity (cosmetic)
No cell is factually wrong (hashes, line counts, quotes, word counts, state, timestamps all verified live).
One imprecision: S127's anchor `:319, :335 "for (int step = 0; step < 32000; step++)"` reads as if the quote lives at both lines; it lives at :335 only, :319 is `parse_gates("gates.txt");` (the cwd-relative read the row's claim cell names). Not wrong enough to count as a wrong cell (the second line number supports a claim in the same row), but a reader checking :319 for the quote fails. Optional, CORPUS rule 2 / Q34 form (new row, never in place; next free id to be chosen by the L1 — S129 placeholder, check):

```
| S129 | Terminal-Bench 2.0 circuit-fibsqrt task simulator (tests/sim.c) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/sim.c | code | A | same capture as S127, locator sharpened | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, sim.c:1-353; :319 `parse_gates("gates.txt");` (cwd-relative read); :335 "for (int step = 0; step < 32000; step++)" (9 words); sha256 700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173 | supersedes S127 — the quoted loop is at :335 only; :319 is the parse_gates call; no change to bytes, hash or claims | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-circuit-fibsqrt-grader.md |
```
Recommendation: L1 may skip it (no reader-facing claim changes); if added, S127's own `supersedes` columns stay untouched.

Unattacked: SOURCES.md claim cells beyond the first 768 bytes were read in full (cut-line output) and not found to contradict the captures; semantic claims about the grader (cwd, parse rules, 28-value table) belong to other wave-2 seats.

VERDICT: rows-reopened-4-wrong-cells-0
