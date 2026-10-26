# F38CritNoHarmDiff — did round 38 remove a line, move a score without its claim, or touch a frozen file?

Seat: critic, wave 2 (falsify). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, window
`21e6251b` (round-37 L1 landing, 2026-10-26 02:25:17 -0300) → `8c7422d7` (landed tip), freeze
`e0a37853`. Every command below is read-only (`git diff/show/log/ls-tree/cat-file`, `sha256sum`,
`grep`, `sed` on committed bytes). No clone was needed, nothing was written outside
`.ufo/waves/round-38/falsify/F38CritNoHarmDiff/`; no scratch dir was created; no tool installed
(nothing was needed — pacman is paused, so nothing was filed).

Receipts: `falsify/F38CritNoHarmDiff/diff-numstat.txt`, `frozen-and-scope.txt`,
`counts-and-hunks.txt`, `score-and-citations.txt`.

## 0. Ancestry (so the window is the right window)

```
$ git rev-parse 21e6251b 8c7422d7 e0a37853 fc1174f5
21e6251bfebf87ecf09f7b0a6df98b5c6179d0e9
8c7422d7a646515d80af44844e8ecc8a1fc1d30a
e0a378539a45cc9388c66cfba22f44275131de23
fc1174f52b150999bef91f2e81da78732ca0eb9f
$ git merge-base --is-ancestor 21e6251b 8c7422d7 && ... e0a37853 8c7422d7 && ... fc1174f5 21e6251b
21e6251b ISA ancestor of landing
freeze e0a37853 ISA ancestor of landing
baseline fc1174f5 ISA ancestor of 21e6251b
```

The freeze is a child of `21e6251b` (SCORECARD.md:1337 says "a child of the round-37 L1's
`21e6251b`, which landed 3 s earlier"), so `21e6251b..8c7422d` is exactly round 38 and the
`--numstat` in my ticket is a net window, not a superset.

## 1. The assigned command — 0 removed lines

```
$ git -C <lane> diff --numstat 21e6251b 8c7422d -- SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/
35   0  LOG.md
82   0  PROVINCE.md
41   0  SCORECARD.md
56   0  SKILL.md
67   0  corpus/QUALITY.md
23   0  corpus/README.md
2    0  corpus/SOURCES.md
30   0  corpus/evidence/round38/build-pmars-dry-cases-freeze.txt
26   0  corpus/evidence/round38/build-pmars-probe.txt
5    0  corpus/evidence/round38/tb2-build-pmars/SHA256SUMS
9    0  corpus/evidence/round38/tb2-build-pmars/instruction.md
29   0  corpus/evidence/round38/tb2-build-pmars/solve.sh
41   0  corpus/evidence/round38/tb2-build-pmars/task.toml
29   0  corpus/evidence/round38/tb2-build-pmars/test.sh
85   0  corpus/evidence/round38/tb2-build-pmars/test_outputs.py
342  0  corpus/knowledge/tb2-build-pmars-grader.md
155  0  corpus/knowledge/tb2-git-webserver-grader.md
77   0  corpus/lessons/round-38.md
```

18 files, **1134 added, 0 removed**. Second, independent count of the same property from the patch
text rather than numstat:

```
$ git diff 21e6251b 8c7422d -- <same set> | grep -c '^-[^-]'
0
```

`SHONEN.md` does not appear: `git diff --name-only … -- SHONEN.md` prints nothing, i.e. unchanged,
not rewritten.

**The net window has a blind spot** — a file created *inside* the window and then rewritten would
still show `N 0`. I closed it per commit (`git log --numstat --format='COMMIT %h %s'
e0a37853..8c7422d -- <same set>`): only four commits touch these paths and every one is `+n 0`:

```
COMMIT a022ae6 …        35 0 LOG.md      41 0 SCORECARD.md   77 0 corpus/lessons/round-38.md
COMMIT d93b7d6 …        82 0 PROVINCE.md 56 0 SKILL.md       67 0 corpus/QUALITY.md
                        20 0 corpus/knowledge/tb2-build-pmars-grader.md
                       155 0 corpus/knowledge/tb2-git-webserver-grader.md
COMMIT dc0cdb5 …        23 0 corpus/README.md  2 0 corpus/SOURCES.md
                       322 0 corpus/knowledge/tb2-build-pmars-grader.md
COMMIT e95cf55 …        26 0 corpus/evidence/round38/build-pmars-probe.txt
```

So the new entry (342 lines) is 322 + 20 appended in two separate commits, and the round-37 entry
is one 155-line append. No intra-round removal anywhere in the set.

## 2. Tree-wide: 65 removed lines exist, all outside the assigned set, all in the named D3/D4 rewrites

```
$ git diff --numstat 21e6251b 8c7422d | awk '$2>0'
272  46  plans/anchor_digest_check.py
105  19  plans/ledger_tip.py
```

`65 = 46 + 19`. Nothing in `SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/` and nothing
in `plans/battery*`, the round-36/37 counters, `plans/pkg_gate.py`, `.ufo/waves/round-37/` or
`corpus/evidence/round3[67]/` is touched — all four `git diff --name-only` probes over those paths
print empty (`frozen-and-scope.txt`).

The two deletions are the frontier repairs the claims name (`plans/round-38-claims.md`
§Frontier step: "`plans/anchor_digest_check.py` binds each token to its own row's capture (D3)",
"`plans/ledger_tip.py` binds an absent branch ref"). I checked the cheap regression question — did a
defect class disappear? No:

```
before classes:  abbrev-unresolved digest-unknown erratum-digest-unresolved erratum-incomplete
                 row-malformed token-outside-anchor                       (6 distinct)
landing classes: abbrev-unresolved anchor-unbound digest-unknown digest-wrong-capture
                 erratum-digest-unresolved erratum-incomplete row-malformed token-outside-anchor
                                                                          (8 distinct)
```

Two classes added, none dropped, for `anchor_digest_check.py`; `ledger_tip.py` keeps its
`exec_module` path (grep count 1 before, 1 at landing). Re-running those tools is another seat's
assignment (D3/D4), not mine; I only establish that the 65 deletions are not silent doc loss.

## 3. Any score moved without its claim? No — every axis row says *held*, and says why

```
$ git show 8c7422d:SCORECARD.md | grep -n '^| C1 \|^| C2 ' | awk -F'|' '{print $1, $(NF-1)}'
1344: **8 → 8 held; NOT ADMITTED (honest stop).** The survivor N21 is frozen as `silence` but can only
      be killed as a mirror … Not relabelled after scoring. Also: 3 of 22 `adv` cells name no
      advertising sentence (`R38CritClaims` §1) and the counter's predicate is reachable by an
      in-process monkeypatch (`R38CritClaims` §2)
1345: **7 → 7 held** (L0 cap). Frozen predicate met; admission also rests on non-author re-reads
      (`R38CritPytest` 22/22, `R38CritIndep` 22/22 + 3/3) because the counter admits an informed
      filler (`R38CritC2Counter` §1)
```

The held-axes line is byte-identical to round 37's, which is what "held" requires:

```
21e6251b SCORECARD.md:1279  Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8.
8c7422d  SCORECARD.md:1347  Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. No-harm …
```

`calibration 8` is the previous value (round-37 rows 1223/1276 read `8 → 8 held`), and the round-38
C1 row keeps it at 8 while marking the predicate unmet — the honest-stop form the ticket asks about.
The frozen claims require exactly this ("C2 is judged on its counter, not on a score move"; "a
predicate not met at landing → not admitted"), so the prose and the frozen rule agree. The
`Planned (round 39)` bullet also re-opens `Calibration (8)`, not `9`.

The counts the appended rows cite are the counts the file trees have, and the counter measured them
at landing (`measures-and-hunks.txt`; `measure-final.txt:126` `index_rows=45 knowledge_files=45`,
`:397` `registry_rows=109`):

| claim (SCORECARD:1341, README round-38 bullet) | 21e6251b | 8c7422d | command |
|---|---|---|---|
| SOURCES rows / tier A | 107 / 91 | 109 / 93 | `grep -c '^| S[0-9]'`, awk on field 5 |
| knowledge files / index rows (parity) | 44 / 44 | 45 / 45 | `ls-tree corpus/knowledge/`, `grep -c '^| \`knowledge/'` |

So "knowledge 44/44 → 45/45", "SOURCES 107→109", "Registry 107→109 (tier A +2)" all check out, and
the parity the counter enforces (P8) is 45/45 both in the tree and in the receipt.

## 4. Any frozen file changed after `e0a37853`? No — 8/8 digests identical at freeze and tip

```
$ for each line of .ufo/waves/round-38/claims/frozen-digests.txt:
    sha256(git show e0a37853:$f) vs sha256(git show 8c7422d:$f) vs want
OK plans/pkg_gate.py                        freeze=ea63882240e6 landing=ea63882240e6 want=ea63882240e6
OK plans/round38_c1_verify.py               freeze=8069739990c7 landing=8069739990c7 want=8069739990c7
OK plans/round38_c2_verify.py               freeze=d906d55f2656 landing=d906d55f2656 want=d906d55f2656
OK plans/build_pmars_probe.py               freeze=32f0771cd5c4 landing=32f0771cd5c4 want=32f0771cd5c4
OK plans/pkg-spec-r38.json                  freeze=bd9bfe71c1c9 landing=bd9bfe71c1c9 want=bd9bfe71c1c9
OK corpus/evidence/round38/build-pmars-dry-cases-freeze.txt freeze=93b4b60cfe13 … want=93b4b60cfe13
OK plans/round37_c1_verify.py               freeze=dbc9f7199381 landing=dbc9f7199381 want=dbc9f7199381
OK plans/round37_c2_verify.py               freeze=b8cba11a3692 landing=b8cba11a3692 want=b8cba11a3692
```

Also empty: `git diff --name-status e0a37853 8c7422d -- .ufo/waves/round-38/claims
plans/round-38-claims.md plans/pkg_gate.py plans/round38_c1_verify.py plans/round38_c2_verify.py
plans/build_pmars_probe.py plans/pkg-spec-r38.json
corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` — the frozen claims file and all five
red controls are byte-unchanged, so the "frozen before the first recorded run" property cannot have
been retrofitted after `e95cf55`. And the freeze commit itself is additive:

```
$ git diff --numstat e0a37853^ e0a37853 | awk '{a+=$1;d+=$2;n++} END {print "files="n" added="a" removed="d}'
files=18 added=1588 removed=0
```

## 5. The strongest counterexample I could build: two assigned files are *not* append-only

`git diff -U0` shows four of the five top-level docs are pure EOF appends, but SKILL.md and
corpus/README.md are edited *mid-file*:

```
SKILL.md             @@ -581,0 +582,5 @@     (insertion after 581 of 806)
                     @@ -806,0 +812,51 @@   (EOF append)
corpus/README.md     @@ -70,0  +71 @@        @@ -261,0 +263 @@
                     @@ -288,0 +291,15 @@   @@ -429,0 +447,6 @@
SCORECARD.md/LOG.md/PROVINCE.md/QUALITY.md/SOURCES.md/git-webserver entry: single `@@ -<eof>,0` append each
```

Insertion is not removal (numstat 0), but it renumbers every later line, so it can silently break
line-number citations. I tested the citations that could cross an insertion point:

- `plans/ledger_tip.py:23` cites `SKILL.md:581`. Line 581 is *unchanged* — verified identical at
  both revisions (the `ledger-tip` registry row) — because the insertion starts at 582.
- `corpus/lessons/round-36-verifier-spotcheck.md` cites `SKILL.md:574-576,576`; `round-37-…` cites
  `SKILL.md:577-581`. All are ≤ 581, so unchanged.
- The only lane citation at `README.md:70` (`round-37-verifier-spotcheck.md:78`, "README index row
  at `corpus/README.md:70`") is at the boundary; the insertion is after 70, so it still resolves —
  landing line 70 is still `| \`knowledge/tb2-git-webserver-grader.md\` | A third Terminal-Bench 2.0
  task grader read and executed …` while old 74–78 → new 74–79 shows only the single +1 shift from
  the row inserted after 70.

So: two files are structural registries where insertion is the correct edit (an index row belongs
in the index, an instrument row in the registry), and round 38 placed both insertion points *after*
the highest line any lane doc cites. No citation was invalidated by this round.

## 6. Residuals (not defects of the diff; smallest safe corrections named)

R1 — **the round-37 false label still lives in the map; only prose corrects it.** Append-only makes
a local fix illegal, so `corpus/knowledge/tb2-git-webserver-grader.md:107` still reads

```
| `instruction.md:9` | enforced | `capitalised`, `leading-space` |
```

while the correction sits in `## Errata (round 38)` at line 293 of 446 (186 lines below). Any reader
or tool that parses the map row alone re-derives the round-37 D2 defect; Q28 at `QUALITY.md:455`
now says labels must be derived "from every executed case that violates the requirement", so the
stale row contradicts a rule added in the same round. Smallest safe correction: nothing inside the
append-only rule — this is the correct-by-constraint form. If a future round permits a rewrite, that
one row should carry an inline pointer to the erratum. Impact: none on this round's axes; it is the
price of the lane's append-only norm, and it should be stated as such rather than as "fixed".

R2 — **"No-harm at the landing tip" is measured three commits before the tip.** SCORECARD.md:1338
already discloses the clone (`of d93b7d68`), but :1346 labels the numbers "at the landing tip". I
verified the label transfers: `git diff --numstat d93b7d68 8c7422d` removes 0 lines and adds only
`.ufo/waves/round-38/{build,assimilation,integrate}/*` plus `LOG.md`, `SCORECARD.md`,
`corpus/lessons/round-38.md` — and every no-harm instrument reads `plans/pkg_gate.py`,
`plans/battery3[67]`, `corpus/SOURCES.md`, `corpus/evidence/**`, `corpus/defects*.jsonl`, none of
which those three commits touch. So the claim is true but is an inference, not a re-measurement.
Smallest safe correction: one clause — "measured at `d93b7d68`; the three later commits append docs
and wave reports only, so the instruments see identical inputs" — or a re-run at `8c7422d`.

R3 — the C1 claim's own source arithmetic (`13+1+6 = 20 ≠ 22`) is wrong in the frozen file and is
now self-reported (`corpus/lessons/round-38.md:38`, LOG.md round-38 "Mistakes mined"). The frozen
file is correctly left frozen; the list N01–N22 the counter scores is unchanged. Not a no-harm
defect, but the SCORECARD C1 row does not restate it, so a reader of SCORECARD alone never learns
the derivation is short by two.

## 7. Provenance spot-checks of the appended prose (6/6 resolve)

The 82-line PROVINCE append cites sibling instruments by line; each resolves to the claimed
instrument: `tameshi-shokunin/tools/env-diff.py:57-70` (bwrap envelope, `BWRAP_UNAVAILABLE`),
`tameshi-shokunin/SKILL.md:1929` (`defect-probes.py` registry row), `kumitate-shokunin/scripts/
cap-run.mjs:30-38` (`systemd-run` + `bwrap --clearenv` argv), `mado-shokunin/quality/counters/
c1-r40-live-v2.py:19-23` (`bwrap --unshare-all --cap-drop ALL`, "No bwrap -> SETUP, exit 2"),
`kaidoku-shokunin/SKILL.md:606` (`carrier-guard` row), `kotodama-shokunin/SKILL.md:254`
("Determinism is not isolation"). The PROVINCE arithmetic "89 carry `tests/test.sh`; 4 are read"
(→ "remaining 85") is self-consistent and README's frontier bullet says "4 of the 89".

## What would have changed the verdict

A single `-` line in `SCORECARD.md LOG.md SKILL.md PROVINCE.md SHONEN.md corpus/`; a frozen digest
that differed between `e0a37853` and `8c7422d`; a `8 → 9` (or `7 → 8`) score field on a row whose
predicate is unmet; a pre-round artifact inside the window. None occurred: removed lines in the
assigned set = **0**; frozen digests mismatched = **0**; score moves without a claim = **0**;
pre-round artifacts touched = **0**. The gaps that remain are labelled residuals R1–R3 above, and
none of them is a deletion, a silent score move, or a post-freeze edit.

VERDICT: no-harm-removed-lines-0
