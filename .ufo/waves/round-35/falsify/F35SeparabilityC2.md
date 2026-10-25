# F35SeparabilityC2 — Causal separability of C1 vs C2 (round 35 wave 2 falsify)

Seat: F35SeparabilityC2 (executor, leaf). Date: 2026-10-25.
Target: in a fixture clone at lane tip `dfee6fff631ebc5f623ba4506e5c7992a215401c` (master),
remove ONLY C1's surfaces, fixture-commit, re-run the C2 ledger; it must stay green. D1 in a
clone is trivially green — stated below.

## Fixture

Rules followed verbatim: `D=$(mktemp -d /tmp/k35f-XXXX); git clone -q --no-checkout --shared
<lane> "$D/lane"; git -C "$D/lane" sparse-checkout set --no-cone plans corpus SCORECARD.md .ufo/waves/round-34;
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c`.
Verified before any write: `git -C "$D/lane" rev-parse --show-toplevel` == `$D/lane`
(actual `/tmp/k35f-RPHR/lane`). Tip confirmed: `git rev-parse HEAD` == `dfee6fff...`.
All git calls named `-C "$D/lane"`; two fixture commits inside the clone with identity
`fixture <fixture@invalid>`; `rm -rf "$D"` at the end.

## What was removed (C1 surfaces only)

All four surfaces listed in the assignment; every change traces to commit `4fe72a9`
("C1 admit TB2 protein-assembly grader entry, S105-S107, probe receipt; ...") — the only commit
between freeze `58a19f3` and landing touching `corpus/README.md`/`corpus/SOURCES.md`:

1. Entry file: deleted `corpus/knowledge/tb2-protein-assembly-grader.md` (131 lines).
2. SOURCES rows: deleted rows S105/S106/S107 (3 table rows) from `corpus/SOURCES.md`.
3. README rows: deleted the 4 C1 additions in `corpus/README.md` — the "What's here" index row
   for the entry (line 68), the coverage-map bullet "Terminal-Bench 2.0 task grader (one task)"
   (line 257), the Frontier bullet "Partly discharged round 35" (line 282), and the trailing
   "### Round-35 evidence" section (lines 398–404, incl. the two bullets about
   `tb2-eval/` and `tb2-grader-probe.txt`).
4. Evidence dir: deleted `corpus/evidence/round35/` (11 files incl. `tb2-eval/` captures and
   the probe receipt).

Fixture commits: `d7abe076` (README+SOURCES) and `d7d7e48` (entry+evidence); parent of both is
`dfee6fff`. Post-commit `git status --porcelain` empty (clean).

## Evidence runs (all in the fixture clone unless noted)

Absence checks (post-commit, `git grep` at HEAD, exit 1 = no match):

```
$ git -C $D/lane grep -n -E '^\| S10[5-7] ' -- corpus/SOURCES.md
(no output; grep_exit=1)
$ git -C $D/lane grep -n -E 'tb2-protein-assembly-grader|Round-35 evidence|Terminal-Bench 2\.0 task grader \(one task\)' -- corpus/README.md
(no output; grep_exit=1)
$ [ -e corpus/knowledge/tb2-protein-assembly-grader.md ] → absent
$ [ -e corpus/evidence/round35 ] → absent
```

C2 ledger in the fixture (the acceptance run) — `cd $D/lane && python3 plans/defect_ledger.py --lane .`:

```
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
(ledger_exit=0)
```

This is the exact frozen predicate (`plans/round-35-claims.md` line 47–48). C2 is green with
every C1 surface removed.

C1 counter in the same fixture (proves the removal is real — it bites C1) — `python3 plans/round35_c1_verify.py --lane .`:

```
V1 DEFECT SHA256SUMS absent
V2 DEFECT S105 present 0 times
V3 DEFECT entry absent
V4 DEFECT index row absent or missing S105/S106/S107
V5 DEFECT probe receipt absent
V6 ok
checks=6 defects=5
PREDICATE C1 fail
(c1_exit=1)
```

Control: original lane at landing tip — `python3 plans/defect_ledger.py --lane .` (cwd
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`) prints the identical green block; `ledger_exit=0`.

## D1 note

`R34-D1` passed with `untracked=0`. This is the *designed* trivial pass in a fresh clone: D1
is a working-tree check (`git ls-files --others`) and a clone has no untracked files — the same
fact the claims file already calls out for the flip control ("D1 passes only because a fresh
clone has no untracked files — D1 is a working-tree check by design", `round-35-claims.md:54-55`);
The fixture run is therefore not evidence that D1's real-world state at the landing tip is clean
(that is the original-lane run's job, which is also in). D2's `committed_mirror_paths=0` and
D3's `listed=6` are real byte checks and are not trivial in a clone.

## Cross-dependency

None found. The C2 ledger's five checks read only C2/round-34/lesson/SCORECARD surfaces:

- D1: `git ls-files --others` on `plans/round34_c1_verify.py`, `plans/round34_defects.py`,
  `plans/round34_mutate.py`, `.ufo/waves/round-34/`
- D2: `git ls-tree -r refs/heads/master` on round-34 mirror roots
- D3: `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS` + capture bytes
- D4: `.ufo/waves/round-34/build/R34C2CounterDraft.md`, `R34MutC2Harness.md`, `SCORECARD.md`
- D5: `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html`, `corpus/lessons/round-34.md`,
  `corpus/lessons/round-35.md` (§Mistakes S091 row)

None overlaps C1's four surfaces (entry, SOURCES S105–S107, README C1 rows, evidence/round35).
One nuance worth recording: the README "### Round-35 evidence" section I removed contained a third
bullet naming `defects.jsonl` + `plans/defect_ledger.py` (C2's ledger). Removing it did not move
C2 because the ledger never reads `corpus/README.md`; the ledger's D4 reads `SCORECARD.md`, not
README. Empirically, the ledger stayed `rows=5 closed=5 observed_pass=5 mismatches=0` with the
whole section gone. The reverse direction is also verified: with C1 surfaces removed, C1's own
counter drops to 5 defects while C2 stays green — the two counters are causally independent.

## Risks / limitations

- The fixture ran with sparse checkout; the C2 ledger's reads were all materialized (plans,
  corpus, SCORECARD.md, .ufo/waves/round-34) and none resolved to absent paths (a missing read
  would have surfaced as a check error, not a pass — none occurred).
- Only C1's four surfaces were touched; no other lane file was written. Scratch cleaned.
- `git status` post-commit clean in both fixture commits; parent verified `dfee6fff`.

VERDICT: c2-separable-yes
