# R30FxNoHarm — no-harm audit of the whole round-30 diff

Seat: `L1Kengaku30.R30FxNoHarm-3` (falsify wave 2, leaf). Lane: `kengaku-shokunin`.
Snapshot instant of every inventory below: **2026-10-25T04:42:46-03:00**, re-checked at
**04:45:21** (identical: 11 tracked files, 574 +/8 −, 18 status paths, 0 file deletions); first pass
was 04:37:5x and the diff was still growing under concurrent peers — see F7.
Base = lane `HEAD` = `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db`, detached (`git rev-parse --abbrev-ref
HEAD` → `HEAD`). No round-30 commit exists yet, so the round diff is **worktree vs `363a4ebf`**
(tracked modifications + untracked additions), not commit vs commit.

Tooling installed or upgraded by this seat: **none**. No pacman invocation of any kind. Scratch:
`/tmp/r30fx-noharm/`. No lane byte was edited except this report.

## Method (every number below was produced here, not read from a build report)

```
git -C <lane> diff --stat|--numstat|--name-status|--summary 363a4ebf
git -C <lane> status --porcelain
git -C <lane> show 363a4ebf:...            # base blobs
git -C <lane> grep -li kappa <rev>         # 2ff4b6f, 363a4ebf, worktree
git -C <lane> ls-tree 1f3b0f1e plans/      # baseline has no adoption_check.py
python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census
python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census
python3 plans/sources_adopt.py --selftest            # 14 cases
python3 <363a4ebf:plans/sources_adopt.py> --selftest # 10 cases (control)
python3 <363a4ebf:plans/sources_adopt.py> --help  vs  current --help
python3 plans/round30_defects.py --lane .
<frozen 8c14a5d:plans/adoption_check.py> + <363a4ebf counter> on a `git archive 1f3b0f1e` tree
```

## 1. Per-path verdict table

Tracked changes (`git diff --numstat 363a4ebf`, 11 files, **574 +/8 −** as of 04:43:49 — recomputed
line by line: 4+22+36+64+33+24+4+6+7+34+340; untracked 7 roots, 68 files). `plans/adoption_check.py`
(+34 / −0) appeared **between** my 04:40:29 and 04:43:49 passes — see F7/F8; it is audited in the
same table:

| path | change | prior row edited? | deletion | within named scope | verdict |
|---|---|---|---|---|---|
| `SCORECARD.md` | +33 / −0, **1 hunk at EOF** (`@@ -1008,3 +1008,36 @@`) | no — pure append, the round-29 attempt-2 block is untouched context | 0 | yes | **PASS** — no axis lowered (§2) |
| `corpus/QUALITY.md` | +24 / −0, 1 hunk at EOF | no — Q1–Q19 untouched; Q20 follows Q19 (§Round30 criterion) | 0 | yes | **PASS** |
| `corpus/SOURCES.md` | +6 / −0, 1 hunk | no — all 82 base rows byte-identical; S081–S086 appended | 0 | yes | **PASS** — rows 82→88, no duplicate id, census exit 0 |
| `corpus/README.md` | +4 / −1, 3 hunks | no: knowledge index row appended, coverage row appended, one frontier bullet rewritten in place (F6) | 1 line (rewrite) | yes (index / coverage / frontier are named surfaces) | **PASS** with note F6 |
| `corpus/lessons/round-29.md` | +7 / −3, 2 hunks | no | 3 lines = the two named round-29 repairs (S078 count, kappa scope) | yes — named exception | **PASS** (F3 on the repaired number) |
| `LOG.md` | +64 / −0, 1 hunk at EOF | no | 0 | yes | **PASS** |
| `.ufo/waves/yield.tsv` | +36 / −0, 1 hunk at EOF | no — 40 prior rows untouched | 0 | yes | **PASS on harm**; one appended row dangles (F1) |
| `.ufo/waves/round-29/attempt2/adoption-expect.json` | +4 / −1 | no — `entries` array and both sources untouched | 1 line: `]` → `],` (needed for the new key) | yes — named exception (round-29 expect note) | **PASS** — counter output unchanged (`cited_rows=5`, exit 0, re-run) |
| `.ufo/waves/round-29/attempt2/build/R29a2CritEntry.md` | +22 / −0 (append only) | n/a | 0 | yes (D4) | **PASS** |
| `plans/sources_adopt.py` | +340 / −3, 9 hunks | n/a | 3 lines, docstring only (capability list item 4 + the 2-line `Scope:` paragraph, extended in place) | yes (C3) | **PASS** — see no-regression evidence §4 |
| `plans/adoption_check.py` | +34 / −0, 1 hunk (mid-file, before the pass predicate) | no — the seven printed fields are untouched; preceding 96 lines are context | 0 | **no** — the frozen prereg calls this counter "unchanged from round 29" (F8) | **PASS on harm, FAIL on claim consistency** — both prior greens survive the tightening (§4a) |
| `corpus/knowledge/contamination-transparency-card.md` | new (15 029 B) | n/a | n/a | yes | **PASS** — content review is not this seat's item; see note at end |
| `corpus/lessons/round-30.md` | new (11 236 B) | n/a | n/a | yes | **PASS** |
| `plans/round-30-claims.md`, `plans/round30_defects.py` | new | n/a | n/a | yes | **PASS** — the counter has no write path (only `subprocess` `git -C` reads, verified by grep) |
| `corpus/evidence/round30/` (5 files) | new receipts | n/a | n/a | yes | **PASS** — all five reproduce (§4) |
| `corpus/evidence/round29-attempt2/control-nothing.txt` | new file in a round-29 evidence dir | no — the 10 committed base files are untouched | 0 | yes (D1) | **PASS on harm**; provenance sentence imprecise (F4) |
| `.ufo/waves/round-30/` (79 files: 35 build reports for 36 build seats — F1 — plus spec/dispatch/claims/assimilation/falsify/registry) | new | n/a | n/a | yes | **PASS** — one ledger row dangles (F1) |

Bounds check: the union of the 18 status paths is inside `corpus/`, `plans/`, `.ufo/`, `LOG.md`,
`SCORECARD.md`. No `PROVINCE.md` or `considerthese/` byte changed (allowed, unused). Nothing outside
the lane repo: `git diff --summary 363a4ebf` is empty (no mode change, no symlink, no tracked file
creation/deletion), and `/home/vgpnk/Projects/shokuknow` has **no** `lanes/kengaku` or `merge/kengaku`
file modified since 2026-10-25T04:00 (`find … -newermt '2026-10-25 04:00'` → empty; `lanes/kengaku`
dir mtime 2026-10-24T21:59), so LOG.md's "shokuknow read-only throughout" holds for this round's
window. That repo's 1 918 dirty entries belong to other lanes (newest 04:38:14
`lanes/tabi/round8/.work/ratelimit-series.tsv`).

## 2. Axis scores — none lowered

Last canonical statement before this round (`SCORECARD.md:722`, round-25 re-derivation) plus the
round-29 attempt-2 block (`:986-1010`):

| axis | recorded before | round-30 block says | lowered? |
|---|---|---|---|
| coverage | 7 (capped) | 7 → 7 held | no |
| novelty | 7 | 7 held | no |
| calibration | 8 | 8 → 8 held | no |
| depth | 9 | 9 held | no |
| operability | 8 | 8 → 8 held | no |
| freshness | 8 | 8 held | no |
| adjacency | 8 | 8 held | no |

Mechanically stronger than the table: the SCORECARD diff is **+33 / −0 in one EOF hunk**, so no prior
score cell can have been rewritten. The two operational numbers the block does assert re-derive:
ocean of rows 82 → 88, tier A 76 → 79, tier B 4 → 7, tier C 2 → 2 (82 = 76+4+2, 88 = 79+7+2),
knowledge files 38 → 39, knowledge index rows 38 → 39 — all recomputed from base and worktree here.

## 3. Deletion inventory (8 deleted lines, 4 files; zero file deletions)

| # | file | old | new | justification |
|---|---|---|---|---|
| 1 | `corpus/lessons/round-29.md` | `"The verifier never runs in the agent's sandbox." — 9 words, line 75` | `… — 8 words, line 75` | **named repair** (D3). `wc -w` on the quoted sentence = 8; `corpus/SOURCES.md:^| S078` already said 8. Count corrected upward in accuracy, quote text unchanged. |
| 2 | `corpus/lessons/round-29.md` | `point duplicates …:7-13. Only per-variable kappa and a test–retest ceiling are new (`grep kappa` → 0 hits in the lane).` | five lines that keep both new items and scope the grep to `corpus/knowledge/*.md`, then report the lane-wide `git grep -li kappa` count with both commits named | **named repair** (D2). The deleted clause is the over-broad claim; nothing true was dropped. `grep -rn kappa corpus/knowledge/*.md` → 0 hits confirmed; 65 at `2ff4b6f`, 66 at `363a4ebf`, added file exactly `corpus/lessons/round-29-verifier-spotcheck.md` — confirmed. |
| 3 | `corpus/lessons/round-29.md` | (second line of the same sentence: `  test–retest ceiling are new …`) | folded into the rewritten sentence | same repair |
| 4 | `.ufo/waves/round-29/attempt2/adoption-expect.json` | `  ]` | `  ],` + a `usedby_notes` object documenting the S091 asymmetry | **named exception** (the round-29 expect note). Note is inert: re-ran the round-29 counter on the note-bearing file → `entries=1 … cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0, and on a scratch copy without the key → identical line. The frozen `8c14a5d` counter also accepts the extra key (exit 1, `entries=0`, same fields + `verified_at=0`). |
| 5 | `corpus/README.md` | frontier bullet `- **Contamination transparency cards**: … gate a knowledge entry on Q1–Q8.` | same sentence + appended parenthetical naming **CG1–CG8** and one new sub-bullet | in-place rewrite (F6). Token-level check: all 54 old tokens survive in order; the only token not literally re-emitted is the terminal `Q1–Q8.`, which reappears inside the parenthetical. No claim, lead or caveat removed. |
| 6-8 | `plans/sources_adopt.py` docstring | capability item 4 ended `… or a nonempty collision set.`; `Scope: registry row mechanics only. Source truth, tier judgement and the census itself stay where they are …` | item 4 gains `;` + item 5 (quote mode); `Scope:` now says "registry row mechanics and quote presence only" | docstring only; no executable line deleted. `--help` diff is purely additive (only `--quote-file`/`--artifact` appear). |

Nothing else was deleted: `--diff-filter=D` is empty, `--summary` is empty, and the untracked set
contains only additions (no path that existed at `363a4ebf`).

## 4. No-regression evidence for the only executable change (`plans/sources_adopt.py`)

- Selftest case **names**: base 10 / current 14; removed = **none**; added = `quote-overlong-refused`,
  `quote-absent-refused`, `quote-located-accepted`, `quote-boundary-25-accepted`.
- Base control run (`363a4ebf:plans/sources_adopt.py`): `SELFTEST cases=10 failed=0`, exit 0;
  `--quote-file/--artifact` → `error: unrecognized arguments`, so the control cannot reach the target.
- `--help` diff: no option removed; two added.
- `corpus/evidence/round30/` receipts re-produced by this seat:
  `adoption-after.txt` line exactly as printed by the counter; `gate-selftest-after.txt`
  (`SELFTEST cases=14 failed=0`); `r29-counter-unchanged.txt` (`entries=1 … cited_rows=5 …`,
  exit 0); `census-before.txt`/`census-after.txt` both 14 `W04` + 1 `ok` line, exit 0, against 82 and
  88 registry rows (base row count 82 confirmed from the base blob).
- Both D1 control forms reproduced on a `git archive 1f3b0f1e` tree: frozen counter (`8c14a5d`) →
  `… usedby_ok=0 verified_at=0 census=skipped` exit 1; shipped counter → `… usedby_ok=0
  census=skipped` exit 1. The receipt's two lines are therefore true.

## 4a. No-regression evidence for `plans/adoption_check.py` (+34, landed 04:43:29, mid-audit)

The patch implements four clauses the frozen C1 sentence names but the old plumbing never read —
`exactly the six ids`, `distinct`, `opened=<access date>`, `one index row` — as `ids_ok`,
`duplicates_ok`, `opened_ok`, `index_shape_ok`, each `and`-ed into the pass predicate. It is a
**tightening only** (no clause removed, no field added to the printed seven). Re-ran under the
patched code:

| invocation | printed | exit |
|---|---|---|
| round-29 expect `--census` | `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` | 0 |
| round-29 expect (no `--census`) | same seven fields, `census=skipped` | 1 |
| round-30 expect `--census` | `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` | 0 |

Both previously-green states stay green and the previously-red no-census state stays red, so the
round-29/30 receipts (`r29-counter-unchanged.txt`, `adoption-after.txt`) still describe the shipped
tool. The tightening is therefore harmless to prior state — but it contradicts the frozen prereg
(F8).

## 5. Findings

**F1 — MED — `.ufo/waves/yield.tsv` appends a row whose report path does not exist.**
`30 / R30DraftEntry / scribe / .ufo/waves/round-30/build/R30DraftEntry.md / no / pending` — the file
is absent at 04:42:46 (35 `.md` files in `build/`, ledger has 36 round-30 rows, `swarm-registry.json`
still lists the seat as `spawn`/running). Classifying all 76 ledger rows by existence: 3 unresolve —
this row, plus **two pre-existing** round-29 rows (`.ufo/waves/round-29/attempt2/residual/
R29a2rGateAttack.md`, `…/R29a2rEntryVerify.md`) whose files carry the `L1Kengaku29.` prefix; those two
are base bytes and outside this diff (worth a separate repair). If the ledger is committed as-is, 1 of
36 round-30 rows is a dangling path in a durability ledger (QUALITY Q19's own subject). `commit=pending`
marks it as not-yet-landed, which is honest, but the path column still resolves to nothing.

**F2 — MED — SCORECARD's C2 "after" state does not reproduce on the working tree.**
`SCORECARD.md` C2 prints `after: python3 plans/round30_defects.py --lane .` → `defects=0`, exit 0.
Run at 04:42:46 on the landed bytes: `defects=2`, exit 1 —
`DEFECT D1 receipt exists only in the worktree … not committed at HEAD` and
`DEFECT D4 HEAD:…R29a2CritEntry.md omits the addendum`. The counter is designed to judge `HEAD`
(its docstring says so, and the C2 cell says "D1 judged on the committed blob"), so the printed
"after" is only true post-commit. As *landed bytes* a reader running the SCORECARD's literal command
gets 2. `[INFERENCE]` after a commit that includes both files it becomes 0 — the worktree conditions
the counter tests both hold (receipt present; `### D. Addendum` in the worktree file), but I cannot
verify post-commit without a commit, and no commit exists. The row should read "after the landing
commit".

**F8 — MED — the frozen prereg says the counter is unchanged; the worktree changes it.**
`plans/round-30-claims.md:36` (frozen 04:16:36, untouched since): "**Counting command:** the last
clause above (`adoption_check.py`, *unchanged from round 29*)." The worktree patches
`plans/adoption_check.py` +34 / −0 at 04:43:29 (mid-audit), adding four gating clauses. The patch's
own comment records that "a falsify critic bought the old pass line for 159 bytes" — i.e. a falsify
seat already forced it. Harm to prior greens: none (§4a, all three invocations re-run). Claim
integrity: broken — either the prereg text must be amended with the disclosed delta (consistent with
how C2/C3 disclose their counter tightening) or the patch reverted. As it stands, a round that scores
itself on "the counter is unchanged" ships a diff in which the counter changed.

**F3 — LOW — the D2 repair's own count is already falsified by the round's later bytes.**
`corpus/lessons/round-29.md` now states `git grep -li kappa …` "finds 65 files at the round-29 tip
`2ff4b6f` and 66 at round 30". Verified: 65 at `2ff4b6f` ✔, 66 at `363a4ebf` ✔, and the one added file
is exactly `corpus/lessons/round-29-verifier-spotcheck.md` ✔. But the **worktree now yields 67**: the
extra file is `LOG.md`, whose appended round-30 entry says "kappa" twice (`LOG.md:801`, `:827`) and was
written after that lesson line. "at round 30" is therefore a moving target inside the round itself;
pin it to `363a4ebf` the way the other end is pinned to `2ff4b6f`.

**F4 — LOW — the D1 receipt's provenance sentence omits the counter version it swapped in.**
`corpus/evidence/round29-attempt2/control-nothing.txt`: "Both forms were reproduced on 2026-10-25 from
a scratch `git archive` of the round-29 baseline 1f3b0f1e." The eight-field form is unreachable from
that tree — `git ls-tree 1f3b0f1e plans/` contains no `adoption_check.py` (the counter first lands at
`8c14a5d`), and the shipped counter prints seven fields (`plans/adoption_check.py:116-117`). The
eight-field line requires `8c14a5d:plans/adoption_check.py:107` (`verified_at={verified_at_ok}`).
Sentence is true for the *tree* and silent about the *counter*; name the counter commit, since the
whole point of the receipt is provenance.

**F5 — LOW — `LOG.md` §3 "the five pre-existing invocations are stdout/exit identical" is at best
unnamed and at worst self-inconsistent.** `--selftest` stdout necessarily changed (`cases=10` → 14,
four new `CASE` lines). The paired clause ("the ten original cases keep their names and verdicts")
does reproduce exactly. If `--selftest` is one of the five, the sentence is false as written; if not,
the five are named nowhere in the round's bytes. I checked base vs current on `--selftest`, `--help`
and the two counters; I could not reconstruct the five invocations' argv from the round-29 receipts
(they record output only — see gaps).

**F6 — INFO — `corpus/README.md` frontier bullet is a 1-line in-place rewrite**, which the no-harm
clause's strict exception list ("the round-29 lesson sentence/count repairs and the round-29 expect
note") does not name, though `corpus/README.md` frontier rows are a named landed surface. Content
check clears it (all old tokens survive in order; only a parenthetical and a sub-bullet are added), so
this is a wording-of-the-clause issue, not a content loss.

**F7 — INFO — the diff is moving under concurrent peers.** 14 status paths at 04:37:5x → 17 at
04:40:29 (`LOG.md`, `.ufo/waves/yield.tsv` landed) → 17 at 04:42:46 → **18 at 04:43:49**
(`plans/adoption_check.py` landed mid-audit, F8; `plans/sources_adopt.py` grew 336→340 additions).
This verdict is pinned to 04:43:49; a later append inside the allowed paths would not change the
no-harm conclusion, but a later *deletion* or another patched prior-round tool would, so the verdict
must be re-taken at commit time.

## 6. Residual risk and verification gaps

- **Uncommitted.** Every "after" state in the round's prose is a worktree state. `defects=0` (C2) and
  the D1/D4 clauses become verifiable only at the landing commit; I did not create one.
- I did not review the **content** of `corpus/knowledge/contamination-transparency-card.md` (claim
  C1's substance, the six anchor quotes vs this round's fetches). That is the source-re-read and
  complete-set seats' item, so this report deliberately emits **no** `VERDICT:` line for
  `corpus/knowledge/contamination-transparency-card.md`; the candidate path is recorded here only as
  the artifact whose existence, index row and six cited rows I did verify
  (`entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0;
  six distinct `source: S081…S086` lines; `verified-at: 2026-10-25`; all six rows `status=mined`,
  `opened=2026-10-25`).
- The five pre-existing gate invocations of F5 cannot be re-run verbatim: the round-29 receipts store
  outputs (`registry=76 staged=173 collisions=0 …`, `registry=82 staged=173 collisions=6 …`) without
  their argv, and the round-29 staged package is not committed at a path I could resolve. My
  no-regression evidence therefore rests on case-name identity, `--help` additivity and the two
  counters, not on byte-identical stdout for those five.
- Docs/claims text I could not falsify without network: the six source fetches behind S081–S086
  (this seat is not a source re-read).
- The `census=ok` component of the round-30 **freeze control** was not reproduced by me: the counter
  hard-codes `CENSUS = /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` and passes
  `lane.parent` as `--root` with the lane name, so a `/tmp` replay censuses an unregistered root and
  cannot print `census=ok`. What I did verify about the control is its shape and its exit code — both
  counter versions print seven/eight fields with `entries=0 …` and exit 1 on a
  `git archive 1f3b0f1e` tree.
- 2 pre-existing dangling `yield.tsv` rows (F1) are base bytes; they are reported, not attributed to
  this round.
- F8 is a snapshot finding: if a later seat amends `plans/round-30-claims.md:36` to disclose the
  counter delta, F8 closes; if the patch is reverted, F8 closes the other way. I re-checked the
  claims file at 04:44 and it still read "unchanged from round 29".

## 7. Verdict

**NO-HARM VERDICT: PASS — the round-30 diff at 04:43:49 adds only inside `corpus/ plans/ .ufo/
LOG.md SCORECARD.md`, lowers no axis score, edits no prior SCORECARD cell, deletes 8 lines with zero
file deletions (all 8 justified by the two named round-29 repairs, the round-29 expect note, an
additive README parenthetical, or a docstring extension), and touches no other lane's path; prior
greens survive the round's two gate edits (`sources_adopt.py` case set 10→14 with none removed,
`adoption_check.py` tightening with round-29 and round-30 both still exit 0); the eight findings
(F1–F8) are claim/ledger precision and one prereg inconsistency inside the round's own new bytes,
not harm to prior state.**
