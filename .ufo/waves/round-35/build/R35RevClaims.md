# R35RevClaims — claims review (round 35, wave 1)

Seat: R35RevClaims (reviewer). Target: frozen claims `plans/round-35-claims.md` (freeze commit
`11d6453`) vs counters `plans/round35_c1_verify.py` (V1–V6) and `plans/defect_ledger.py` (D1–D5),
and the four committed controls `.ufo/waves/round-35/claims/control-*.txt`. All work read-only:
one `--shared --no-checkout` fixture clone at `/tmp/k35-UWR8` (toplevel verified, `rm -rf` after),
plus read-only counter runs against the live lane. The lane working tree was never written.

## 0. Verified as claimed (executed evidence)

- **Freeze tip == baseline claim.** `git log --oneline -1 master` → `11d6453 round-35: freeze
  claims, counters, probe, ledger, controls`; `git show --name-status 11d6453` adds exactly the
  12 claims/counter/probe/ledger/control files and touches no corpus/ or SCORECARD content.
  HEAD is detached at the same commit (`git rev-parse HEAD` = `git rev-parse master` = `11d6453…`).
- **Pins are honest upstream digests.** Fetched 2026-10-25:
  `curl -fsSL https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/protein-assembly/<f> | sha256sum`
  → test_outputs.py `44a05a24…96582`, test.sh `9ede4664…267b5`, instruction.md `1bb2af1d…3f7c5`
  — equal to the counter's frozen `FILES` constants (`round35_c1_verify.py:32-40`), to the live
  round-35 captures, and to the round-34 captures
  (`.ufo/waves/round-34/assimilation/captures/tb2-eval/`). The "byte-identical to the round-34
  captures" claim (round-35-claims.md:16-17) holds for the digests checked.
- **Probe receipt reproduces byte-for-byte.** `python3 plans/tb2_grader_probe.py --lane .` (uv
  biopython==1.85 path; no system Bio on this host) → exit 0, `cmp` vs
  `corpus/evidence/round35/tb2-grader-probe.txt` → identical, summary
  `cases=18 observed_pass=5 observed_fail=13 mismatches=0` — exactly the goal statement. The
  probe writes only to tempdirs; deterministic output (no timestamps; header pins
  `biopython=1.85`, tb2_grader_probe.py:150).
- **Freeze controls reproduce at the freeze tip.** Re-ran `round35_c1_verify.py --lane <clone>`
  at master: V1 `SHA256SUMS absent`, V2 `S105 present 0 times`, V3 `entry absent`, V4
  `index row absent or missing S105/S106/S107`, V5 `probe receipt absent`, V6 ok,
  `checks=6 defects=5` → same defect lines as `control-c1-nothing.txt`. Tip counts:
  `git ls-files 'corpus/knowledge/*.md' | wc -l` = 41, README `| `knowledge/` rows = 41.
- **Both checks demonstrably fail and pass.** C2 live (mid-build, read-only):
  D1 `untracked=5` fail, D3 `listed=6 evaluator_listed=True bad=0` pass, D4
  `correction_lines=1` pass, D5 `erratum_lines=1 r35_mistake_row=False` fail, rows still open →
  `mismatches=2`, `PREDICATE C2 fail`. C1 live: V1,V2,V3,V5,V6 ok, only V4 red
  (`knowledge files=41 index rows=42 (want 42/42)` — entry uncommitted mid-build).

## 1. Predicate-sentence consistency (plan vs code vs receipt)

| Claim | plans/round-35-claims.md | Counter code | Receipt label |
|---|---|---|---|
| C1 | :26-27 “C1 passes iff … `checks=6 defects=0` and `PREDICATE C1 pass`, exit 0” | `round35_c1_verify.py:5-6` — verbatim identical | controls carry `PREDICATE C1 fail` + `exit=1` (`control-c1-nothing.txt:8-9`); counter prints the label at :212 |
| C2 | :47-48 “C2 passes iff … `rows=5 closed=5 observed_pass=5 mismatches=0` and `PREDICATE C2 pass`, exit 0” | `defect_ledger.py:12-13` — verbatim identical, with an honest caveat at :14-15 | `control-c2-nothing.txt:6-8`; counter prints the label at :139 |

Sentences match verbatim in both pairs. One asymmetry, finding FG2: the C2 *code* enforces a
weaker condition than the sentence (row count unenforced); only a verifier who string-matches the
full `rows=5 closed=5 observed_pass=5 mismatches=0` line applies the frozen sentence. The C1 probe
receipt (`tb2-grader-probe.txt`) itself carries no predicate line — the "receipt label" convention
(house style since round-30-claims.md:26) refers to the counter-run receipts, which do carry it.

## 2. False-green findings (check can pass without delivering the claimed surface)

- **FG1 (medium) — D1 is vacuously green in any fresh clone, and the frozen predicate does not
  pin the run location.** `r34_d1` (`defect_ledger.py:37-44`) reads `git ls-files --others` — a
  clone always has `untracked=0`, so `R34-D1 observed=pass` with zero evidence about the lane's
  actual working tree. Executed: ledger on my fixture clone at the same tip printed
  `R34-D1 status=open observed=pass agree=NO untracked=0` while the live lane at the identical
  commit prints `R34-D1 … untracked=5`. The claims acknowledge this for the skip-control
  (round-35-claims.md:54-55, `control-c2-flip.txt:1`), and both C2 controls were run in clones
  (`control-c2-flip.sh:8-19`), so a verifier who follows the control's own pattern gets a green
  D1 that delivers none of D1's surface (round-34 tree hygiene; spotcheck
  round-34-verifier-spotcheck.md:75). At the true landing live and clone agree only after the
  repair commits/deletes the untracked files. **Ask:** the L1's C2 verification receipt must
  record cwd = the live lane root (`git rev-parse --show-toplevel` = the lane) and the D1
  `untracked=` note.
- **FG2 (low-medium) — the code's `PREDICATE C2 pass` is ledger-generic; `rows=5` is enforced
  only by the plan's string match.** `good = bool(rows) and closed == len(rows) and passed ==
  len(rows) and mism == 0` (`defect_ledger.py:138`): a 4-row or 6-row all-green ledger prints
  `PREDICATE C2 pass`, exit 0. The docstring admits it (:14-15). A verifier keying on the
  PREDICATE line / exit code alone (the natural shortcut, since for C1 those two are equivalent)
  admits a ledger that is not the claimed five-defect closure. Known-check-name guard is sound:
  an unknown check name yields `ok=False`, so a padded row cannot be silently green (:125-127).
- **FG3 (low) — V3's located-quote table skips unparsable rows and counts duplicates; spans are
  unbounded.** The row regex (`round35_c1_verify.py:124-126`) `continue`s on non-matching rows,
  so junk rows (straight quotes, missing backticks) are never validated; nothing requires quote
  uniqueness; and any `a-b` span width is accepted (:127-136), so `file:1-200` "locates"
  trivially. The hardening seat has already exhibited this mutant
  (`plans/round35_hardening.py:5-6`, R35MutC1Quotes "unparsed quote rows are skipped"). Bounded:
  ≥8 parsable verbatim-on-capture quotes are still required, and the live entry's head triad and
  falsifier pass V3.
- **FG4 (low) — D3 checks manifest self-consistency, not upstream identity.**
  `r34_d3` (`defect_ledger.py:55-66`) requires `have and not bad` — a fabricated digest whose
  file was edited to match would pass. Bounded in practice: the same two files' true upstream
  digests are pinned by C1's V1 and verified equal today (§0), and the round-34 captures are
  byte-identical to them — but D3 itself cannot detect the fabrication.
- **FG5 (low) — D4/D5 validate the existence and substrings of self-assessment lines, not their
  truth.** D4's correction line needs 4 substrings (`defect_ledger.py:77-83`) after an
  observation pre-check (:72-76); D5's erratum needs `nec-s091-reopen.html` + `present`
  (:96-101). A labelled-but-false line passes — already demonstrated by the hardening seat
  (`plans/round35_hardening.py:5`, R35CritC2). The observations themselves (draft line 8, quote
  in capture) are byte-checked, so the *observations* are honest; the prose about them is only
  shape-checked.

## 3. False-red / environment-gating findings (truthful landing scored red)

- **FR1 (medium-low) — D2 reads `refs/heads/master`, not the tree under test.**
  `BRANCH = "refs/heads/master"` (`defect_ledger.py:29`) + `ls-tree -r … BRANCH` (:47-53). The
  lane is a jj-colocated repo with detached HEAD at the freeze commit; the build (mirror
  deletion) is uncommitted, so today a truthful repaired tree still reads
  `committed_mirror_paths=109413` and D2 stays red until the landing commit is actually ON
  master. D1 is the mirror image (working-tree only). The two checks have opposite environment
  requirements: D1 wants the live working tree, D2 wants master == landing tip. Both are
  satisfied simultaneously only by: commit the landing, move master, then run
  `defect_ledger.py --lane .` in the live lane. The claims say "at the landing tip"
  (round-35-claims.md:52) but no receipt exists yet proving that order was followed.
- **FR2 (low) — V5's fresh-run reproduction prefers a system Bio over the pinned uv path.**
  `round35_c1_verify.py:165-168` uses the counter's own interpreter if `import Bio` succeeds;
  the probe header prints the actual version (`tb2_grader_probe.py:150`), and the committed
  receipt says `biopython=1.85`. On a host with system biopython ≠ 1.85 the fresh run differs
  from the receipt byte-for-byte → V5 red on a truthful landing (honest red, wrong reason).
  On this host system Bio is absent, the uv path ran, and the receipt reproduced exactly
  (`RECEIPT_BYTE_IDENTICAL=yes`), so the landing is verifiable here; uv+cache/network is a
  dependency of that.
- **FR3 (low) — V4's `42/42` is reachable but lane-global.** Tip is 41 files / 41 index rows
  (measured at both `58a19f3` and `11d6453`), so the landing's one entry + one row lands exactly
  on 42/42 (`round35_c1_verify.py:154`); the skip control demonstrates V4 ok once the entry is
  index-visible (`control-c1-skip.sh:37` stages it). Not a false red on a committed landing —
  but V4 reds (i) a landing judged in a fresh clone while the entry was left unstaged in the
  live lane (the live mid-build state: `files=41 index rows=42` → red), and (ii) any *other*
  seat's knowledge-tree drift. C1's verdict is coupled to lane-wide index hygiene, not just its
  own surface.

## 4. Separability

Verified by enumerating both counters' read sets. C1 reads: `corpus/evidence/round35/tb2-eval/*`,
`corpus/SOURCES.md`, `corpus/knowledge/tb2-protein-assembly-grader.md`, `corpus/README.md`,
`plans/tb2_grader_probe.py`, `scripts/sources-census.sh` (+ fleet registry). C2 reads:
`corpus/defects.jsonl`, `.ufo/waves/round-34/{plan tools, assimilation captures, build drafts}`,
`SCORECARD.md`, `corpus/lessons/round-34.md`, `corpus/lessons/round-35.md`. The read sets are
disjoint — round-35-claims.md:59-62 is accurate. Two couplings the paragraph omits: (a) the
global guards V4 (42/42) and V6 (whole-registry census, :182-187) make C1 red-able by drift C1
did not cause; (b) `corpus/lessons/round-35.md` is written by both claims' landings (C1's
admission row and C2's D5 Mistakes row share the file), though no check of either counter reads
the other's section. Causally separable as stated: no C2 edit can green C1 and vice versa.

## 5. Residual risk and verification gaps

- The landing does not exist yet, so the frozen predicates were executed only on (a) the freeze
  tip (all red, controls reproduced) and (b) the live mid-build tree. Whether the landing
  achieves `checks=6 defects=0` / `rows=5 closed=5 …` is for the L1's verification run — which,
  per FG1/FR1, must be executed in the live lane after master moves to the landing commit.
- The 18 probe predictions' "written from static reading before the first run" provenance
  (round-35-claims.md:20-21) is unfalsifiable post-hoc; the committed receipt now anchors them
  (byte-equal re-run, mismatches=0), and re-prediction would break V5's byte-compare.
- V1's manifest parser ignores malformed lines and last-valid-wins per name (:57-64); extra
  untracked files inside `tb2-eval/` are not flagged. Cosmetic against pinned-digest delivery.
- I did not independently re-verify the entry's 22 quote rows beyond V3's executed verdict, nor
  re-run `census-before.txt`; V6's live `ok` covers the current registry.

VERDICT: claims-review-5-false-green-3-false-red
