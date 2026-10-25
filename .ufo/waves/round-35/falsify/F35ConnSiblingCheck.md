# F35ConnSiblingCheck — Cross-lane sibling-overlap falsification, kengaku round 35 wave 2

**Seat:** F35ConnSiblingCheck (connector, leaf — no subagents)
**Round:** kengaku round 35 (hyaku run 7, 2026-10-25), WAVE 2 of 2 (falsify)
**Axis:** adjacency
**Landed tip checked:** dfee6fff631ebc5f623ba4506e5c7992a215401c (branch master); freeze 11d64530
**Report target:** `.ufo/waves/round-35/falsify/F35ConnSiblingCheck.md`
**Access date for every sibling file read:** 2026-10-25
**Read-only:** no sibling or lane file was edited; no git/jj mutation; no tools installed or upgraded (grep/read/head/find only).

## 1. What this seat falsifies

Wave-1 report `R35ConnSibling.md` (build) concluded: **0 contested / 7 adjacent**, and asserted
the only persistent ledger files fleet-wide are kengaku's `corpus/defects.jsonl`, kagi's
`corpus/claim-ledger.sh`, tameshi's `knowledge/fleet-kill-rate-ledger.md`, and kumitate's receipt-ledger
evidence set. This wave re-runs the sweep **by full-tree scan**, not by `README.md`/`PROVINCE.md`
rows alone, precisely to catch artifacts a README-driven scan cannot see, and asks: does any sibling
hold (a) a TB2 task-grader reading, or (b) a routed-defect ledger the lane should cite?

## 2. S1 — TB2 task-grader reading: still zero siblings (confirmed, not falsified)

Command (all 20 sibling lanes, whole trees, excluding kengaku, node_modules, `.git`, `.jj`):

```
cd /home/vgpnk/Projects/shokunin
grep -rniE 'protein[- ]assembly|terminal[- ]bench' --include='*.md' --include='*.py' \
  --include='*.sh' --include='*.jsonl' --include='*.txt' --include='*.json' . \
  | grep -v '^./kengaku-shokunin/' | grep -v node_modules | grep -v '/\.git/' \
  | grep -v '/\.jj/' | wc -l
16
```

All 16 hits are non-readings: fleet reports for kengaku itself (`.ufo/reports/*/kengaku.md`),
kumitate round-61/62 **wave-scratch audit quotes** of arXiv 2512.08296v3 (the *paper's authors*
enumerate Terminal-Bench among six benchmarks they ran — no grader code, no reading),
HTML/string noise (`listingblock`, `bindingBlocker`, `GBlock`, `LGBLOCK`). Corpus-surface scan
(`PROVINCE.md` + `corpus/README.md` + `corpus/SOURCES.md` + `corpus/knowledge/`) is **0 hits in
all 20 lanes**. kaidoku's `probe-HarborLib-runtime-hex-6.4.0.json` is an EVM bytecode interface
inspection of a Solidity library (`HarborLib`), unrelated to harbor-framework/terminal-bench.
kasegi's `authorization-safe-harbor-and-scope.md` is the legal "safe harbor" phrase.

**Verdict S1: 0 contested.** Wave-1 S1 negative holds; nothing to cite.

## 3. S2 — routed-defect ledgers: wave-1 inventory was incomplete; three artifacts surfaced

Wave-1's "only persistent ledger files" claim **is falsified as an inventory**. A whole-tree scan
for `*defect*`, `*routed*defect*`, `*disposition*`, and `*.jsonl` finds three sibling artifacts the
wave-1 README-driven scan did not report:

### 3.1 chousa — `corpus/evidence/round40/routed-defect-dispositions.json` (NEW)

Full contents: a JSON ledger of **four routed defects, R2–R5** (the r39→r40 non-author spot-check
routed to chousa), each with `status` (`corrected` ×3, `not-reproduced` ×1), an `evidence` path
list, and a `decision` string. It is the sibling object **closest to kengaku's C2 surface** — the
same two-word phrase as C2's name. It is counter-backed: `corpus/evidence/round40/c2-count.py:11`
(`DISPOSITIONS = ROOT / "corpus/evidence/round40/routed-defect-dispositions.json"`) and
`corpus/evidence/round40/claims.md:23` (the counter "must re-derive these states from the committed
evidence, not count prose labels alone"). Referenced from `corpus/lessons/round-40.md:27,29`.

Boundary: every row is a **chousa-owned** defect about **chousa's** committed r39 report/spec/
receipts (e.g. R4: role-count mismatch reviewer 6/2 vs spot-check 8/0 — "preserve the conflict and
do not invent a spec correction"). None touches kengaku's D1–D5, and chousa `PROVINCE.md:11`
explicitly refuses evaluation claims (→ kengaku). So it is **adjacent on the identical object
class**, not contested. kengaku's C2 claim ("one persistent ledger instead of a new
`plans/roundNN_defects.py` per round", `plans/round-35-claims.md:41-42`) is a parallel design
choice, not a uniqueness claim over chousa's file; the lane should nonetheless cite chousa's
disposition/status/evidence schema when describing its own ledger shape.

### 3.2 audio — `corpus/live/r67-author/ledger-r67-run1-defect.tsv`, `ledger-r67-run2-defect.tsv` (NEW)

Both exist (wc: 113 and 112 lines), alongside `ledger-r67.tsv`, `run_ledger.py`,
`probe_transports.py`. Format: `run-index<TAB>defect-flag<TAB>path<TAB>note` — e.g. `02 1 …-transport-preempt-act-r67/measurements.json transport_preempt_act_r67_probe: transport: detection+decode verdict forks …`. These are **audio's own probe-run defect ledgers** (live research-run experiments), not routed (no routing fields, no opened/closed tracking). They are *undocumented*: `audio-shokunin/corpus/README.md` has 0 mentions of `defect` or `ledger-r67` (grep → 0 lines). Different object, different domain → adjacent at most; cannot collide with kengaku C2.

### 3.3 kaidoku — `.ufo/waves/round-18/tools/routed-defects.py` (NEW, wave-scratch)

A 1,288-line routed-defect **counting tool** (Python 3 stdlib, git-object reads only) counting the
six routed round-17 defects still open at a rev, with `named`/`substance` check sets
(`routed-defects.py:187-196`), receipt at `.ufo/waves/round-18/final-recheck/routed-defects.receipt.json`, plus
`w1/RoutedDefectsTool.md` and `w1/ConnDefectCriteria.md`. It is wave-scratch history (round 18),
not persistent corpus, so not a "ledger" in kengaku's sense; but it is a sibling instrument of the
same vocabulary and of the same *counter* shape as kengaku's `defect_ledger.py` → adjacent.

### 3.4 kagi — `corpus/closure-dispositions.json` / `.py` (reconfirmed, different object)

Schema `kagi-closure-dispositions-v1`, source `corpus/lessons/round-22-verifier-spotcheck.md`;
entries `SPOT-01…` are claim-tier spot-decision dispositions (`no-action`, pointers into
`corpus/SOURCES.md`) — a claim-ledger closure record, not a defect ledger. Wave-1's ruling stands.

**Verdict S2: 0 contested.** No sibling holds a persistent routed-defect ledger covering any ground
kengaku's C2 claims; three led-adjacent artifacts were missed by wave-1 and are now on the record.

## 4. Wave-1 comparison

| Wave-1 claim | Status today |
|---|---|
| 0 contested on S1 (TB2 grader) | **Holds** (full-tree scan, 0 corpus hits) |
| 7 adjacent lanes | **Extends**: audio (3.2) and kaidoku (3.3) are newly-adjacent on defect-ledger/routed-defects instrument vocabulary; chousa already counted adjacent |
| "only persistent ledger files found: defects.jsonl, claim-ledger.sh, fleet-kill-rate-ledger.md, receipt-ledger evidence set" | **Falsified as inventory**: chousa `routed-defect-dispositions.json` (same object class, corpus), audio `ledger-r67-*-defect.tsv` ×2, kaidoku round-18 `routed-defects.py` + receipt were not in the inventory |

No wave-1 verdict flips to contested.

## 5. Citation recommendations (adjacency, not contention)

1. **chousa `corpus/evidence/round40/routed-defect-dispositions.json`** — cite in C2's claim prose
   (`plans/round-35-claims.md`) as the sibling's routed-defect disposition pattern (per-defect
   `status`/`evidence`/`decision`, counter re-derives states) whose shape kengaku's
   `defects.jsonl` rows parallel (opened/closed/source/check) with the routing difference noted.
2. **kaidoku `routed-defects.py`** — note as the sibling's routed-defect *counter* precedent
   (git-object reads; named/substance check duality ≈ kengaku's kill rules).
3. **audio `ledger-r67-*-defect.tsv`** — note as same-word/different-object ("ledger …
   defect": own-probe run logs), no citation obligation.
4. Wave-1 §4 items (kumitate receipt-canonicalization, tameshi verification-patterns-fleet,
   chousa receipt-binding) remain valid; all seven cited files verified present
   (`verification-patterns-fleet.md`, `receipt-identity-canonicalization.md`,
   `receipt-binding-r38.md`, `receipt-verifier-subject-r39.md`,
   `receipt-expectation-digests-r40.md`, `claim-ledger.sh`, `fleet-kill-rate-ledger.md` — all EXISTS).

## 6. Verification commands (this seat, all read-only)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` → 21 lane repos; all 20 siblings have
  `PROVINCE.md` + `corpus/` + `corpus/README.md`.
- Full-tree TB2 grep → 16 hits, all non-readings (§2; corpus-surface count 0/20).
- `find . -iname '*routed*defect*' -o -iname '*defect*routed*' -o -iname '*disposition*'` →
  chousa `round40/routed-defect-dispositions.json` (+ adjacent `audit-dispositions.md`,
  `w04-dispositions.tsv`, `round44/disposition.tsv`), kagi `closure-dispositions.json/.py`,
  audio `sigdisposition.json`, plus a test scratch.
- `find . -name '*.jsonl'` → no defect-named jsonl ledger in any sibling (audio live receipt/spot
  jsonl files are receipt/spot logs; chousa `expectations.jsonl` are expectations).
- `cat chousa-shokunin/corpus/evidence/round40/routed-defect-dispositions.json` → R2–R5 rows (§3.1).
- `head`/`wc -l` on audio `ledger-r67-run{1,2}-defect.tsv` → 113/112 lines (§3.2).
- `head kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py` / `RoutedDefectsTool.md`
  → tool contract (§3.3).
- `grep -n 'defect'` in every sibling `corpus/README.md` → audio 0 (documents nothing), chousa 19,
  kotoba 37, kumitate 30, kagi 9, kaidoku 8, tameshi 10 (README rows are lessons/knowledge rows,
  no second persistent defect ledger).
- `grep -n -A25 'C2' kengaku-shokunin/plans/round-35-claims.md` → C2 predicate, kill rule,
  separability; no fleet-uniqueness overclaim.
- `grep -n 'S105\|S106\|S107' kengaku-shokunin/corpus/SOURCES.md` → rows 120–122 present, pinned
  commit `2fd12b88`, sha256s present.

Tool installs/upgrades: **none**.

## 7. Counts

- Contested sibling lanes: **0** (S1: zero TB2 readings; S2: zero overlapping/duplicate routed-defect ledgers).
- Adjacent sibling lanes: **9** — chousa (routed-defect dispositions ledger + receipt binding),
  kasegi, kama, kotoba, kumitate, tameshi, kagi (wave-1's 7) **plus audio** (defect-ledger
  artifacts) **and kaidoku** (routed-defects counter tool).
- None: the other 11 lanes.

VERDICT: sibling-0-contested-9-adjacent
