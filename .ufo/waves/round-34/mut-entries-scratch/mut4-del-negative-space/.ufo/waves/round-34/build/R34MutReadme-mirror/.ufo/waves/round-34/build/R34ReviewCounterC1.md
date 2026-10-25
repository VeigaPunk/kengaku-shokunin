# R34ReviewCounterC1 — C1 counter gameability review

Seat: R34ReviewCounterC1 (leaf; no subagents). Scope: `.ufo/waves/round-34/build/R34C1CounterDraft/round34_c1_verify.py`
(142 lines, read in full) vs frozen predicate in `plans/round-34-claims.md` (freeze adaf25d, verified
`git log -1 adaf25d` = "round-34: frozen prereg + controls"). All commands run from lane root
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Evidence runs

1. Real-lane counter:
   `python3 .ufo/waves/round-34/build/R34C1CounterDraft/round34_c1_verify.py --lane .`
   → `DEFECT V1 … DEFECT V7` then `checks=8 defects=7`, `exit=1` (V8 green).
2. Selftest: `python3 … --selftest` → `SELFTEST FAIL: red V5 fixture passed`, `exit=1`.
3. Attack trees under `build/R34ReviewCounterC1Attacks/` (base = green fixture, digests recomputed:
   test.sh = e91090b0…, README = d1342e15…). Counter run per tree:

   | tree | mutated content | counter result |
   |---|---|---|
   | base | (green fixture) | checks=8 defects=0, exit 0 |
   | a3 | SOURCES.md = only HTML comments carrying the row tokens | checks=8 defects=0, exit 0 |
   | a4 | README index row removed; prose mention of filename | checks=8 defects=0, exit 0 |
   | a5 | README discharge tokens scattered across §2/§3/§9/frontier | checks=8 defects=0, exit 0 |
   | a6 | frontier bullets negated ("not present/unknown/not retained/no … seen") | checks=8 defects=0, exit 0 |
   | a7 | control receipt forged: literals inside comments, probes never run | checks=8 defects=0, exit 0 |
   | a8 | captures contain only SHA256SUMS referencing `../../../../../../corpus/README.md` | checks=8 defects=0, exit 0 |

## Check-by-check audit (labels vs frozen counting command)

**V1 entry cites exactly S105/S106/S107 — SURVIVED.** Lines anchored `^\s*source:` only; ids via
`\bS\d{3}\b`; requires exactly 3 tokens total, set == {S105,S106,S107}, all distinct; entry file must
exist. Word boundary rejects substring false-green (S1050, xS105, S105abc). Missing/extra id ⇒ red.

**V2 verified-at 2026-10-25 — SURVIVED.** Anchored `^verified-at:\s*2026-10-25\s*$`, multiline;
trailing whitespace tolerated; "2026-10-25T…" does not match. Missing line ⇒ red.

**V3 source rows mined/opened/used-by — FAILED (a3).** Per-sid: exactly one line containing
word-boundary sid, and that line must contain substrings `status=mined`, `opened=2026-10-25`,
`terminal-bench-task-grader.md`. Attack a3 puts exactly those substrings in HTML comments; no real row
exists, counter still reports `checks=8 defects=0 exit=0`. Additional gaps: one line can serve multiple
sids (count==1 per sid still passes); ENTRY test is substring (e.g. `used-by=notes-terminal-bench-task-grader.md`
passes); attribute tokens need not be a valid row line.

**V4 exactly one README index row — FAILED (a4).** Counts *any* README line containing the entry
filename substring. Attack a4 removes the index row and leaves prose "Discussion of
terminal-bench-task-grader.md appears in appendix B." → count=1 → `defects=0`. No index row exists.

**V5 coverage discharge names task and pin — FAILED (a5).** Regex `(?is)Benchmark grader
semantics.*?Terminal-Bench.*?protein-assembly.*?<PIN>` over the whole README: order-only, arbitrary
distance, no sentence/bullet/section constraint. Attack a5 spreads the four tokens across separate
paragraphs and the frontier bullet — no discharge sentence anywhere — full green.

**V6 frontier bullet :279 keeps other clauses verbatim — FAILED (a6).** Only substring inclusion
inside the first `## Frontier` section; no locality to bullet :279, no verbatim check. Attack a6
negates every clause ("beyond round-31 not present", "unknown", "are not retained", "no contamination
seen") — all four substrings still present → full green while the open clauses are actually removed.

**V7 freeze control receipt — FAILED (two independent defects).**
- D1 red-on-truth: committed `claims/control-c1.txt` (verified tracked via `git ls-files`) reads
  `## registry rows count (expect 97)` / `97` / `## rows S105+ (expect 0, empty)` / `0`. The check
  requires literal `registry rows\s*=\s*97` and `rows S105+\s*=\s*0` per line — no match. Real-lane
  run confirms `DEFECT V7`: the counter can never print `checks=8 defects=0` on the landed tree, so
  the frozen C1 predicate is unsatisfiable by this draft.
- D2 forgery: attack a7 swaps the receipt for `# registry rows = 97 (stale comment…)` + `# rows
  S105+ = 0` + `probes were never run` → full green. Literals-in-comments pass.

**V8 captured evaluator SHA256SUMS — FAILED (a8; real-tree observation).** `_sums_valid` resolves
manifest names via `directory / name`; relative `../../…` or absolute names escape the capture dir,
any one existing matching file suffices (`found > 0`), and the evaluator pair (test.sh,
test_outputs.py) is never required. Attack a8: capture dir contains only SHA256SUMS whose sole entry is
`d1342e15…  ../../../../../../corpus/README.md` → `defects=0` with zero evaluator bytes present.
Real-tree observation: current `captures/tb2-eval/SHA256SUMS` lists only antibody.fasta, pdb_ids.txt,
task.toml, instruction.md — **not** test.sh/test_outputs.py — and V8 was green in the real-lane run,
i.e. the two files the claim opens are absent from the manifest the check validates.

## Selftest
`--selftest` exits 1: `SELFTEST FAIL: red V5 fixture passed`. The red-V5 fixture replaces only the
first PIN occurrence; the PIN persists later in the README frontier bullet, so V5 stays green. Red
cases for V1–V4 and V6–V8 exist and fire; V5 has no working red case. The green fixture uses the
literal `registry rows = 97` control text, masking the V7 mismatch against the committed receipt.

## Anti-pattern scan
No check reads or greps the claims markdown for its value; V7 reads only the committed control receipt,
V1–V6 read corpus files, V8 reads captures. The "greps the claims file" failure mode is not present.

## Survival
Survived: V1, V2 (2/8). Falsified with concrete counterexample/failure: V3, V4, V5, V6, V7, V8
(6/8) — each shown green (`checks=8 defects=0`, exit 0) on a tree violating the corresponding frozen
clause, except V7 which is additionally red on the truthful tree.

## Residual risk / verification gaps
- Line is pre-integration; V1–V6/V8 on the final tree inferred from sandbox equivalents (same files,
  same counter). Only V7's red-on-truth is deterministic against the committed receipt.
- V3/V4 fail closed on duplicates, so residual risk concentrates in the green-direction forgery
  demonstrated (comments/prose/fake receipt/external manifest paths).
- Draft captures at `assimilation/captures/tb2-eval/` predate admission; their manifest omitting both
  evaluator scripts is a content gap the check does not catch.

VERDICT: review-c1-counter (survived 2/8)
