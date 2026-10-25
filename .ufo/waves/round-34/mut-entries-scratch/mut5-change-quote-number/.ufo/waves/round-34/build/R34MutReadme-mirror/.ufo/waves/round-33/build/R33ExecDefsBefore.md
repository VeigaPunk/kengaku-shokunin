# R33ExecDefsBefore — independent reproduction of the C2 freeze control

Seat: leaf executor, round 33 (hyaku run 7), 2026-10-25.
Claim: C2 (calibration), frozen predicate at `plans/round-33-claims.md` §C2.
Scope: reproduce the freeze control for `python3 plans/round33_defects.py --lane .` from
committed bytes only. No production edit anywhere.

**VERDICT: defects-reproduced** — the committed control is byte-exactly reproducible
against the joint pre-repair state, and the repaired tip re-derives green.

## 1. Files written (the only writes)

- `.ufo/waves/round-33/build/receipts/defs-repro.txt` — full run log, verbatim outputs,
  hashes, table, delta analysis (this seat's receipt; acceptance artifact).
- `.ufo/waves/round-33/build/R33ExecDefsBefore.md` — this report.
- Scratch only: `/tmp/r33-defsbefore/` (1.7 MB), see §7.

Nothing under `corpus/`, `plans/`, `SCORECARD.md`, lessons, the fleet repo, or shokuknow
was modified. No pacman transaction; no tool installed or upgraded.

## 2. Runs

| run | lane state | fleet state | result | exit |
|---|---|---|---|---|
| A | live repaired lane (HEAD `7895588`) | live repaired | `checks=6 defects=0` | 0 |
| B | `git archive f0b20aea` (no index) | live repaired | `checks=6 defects=4` | 1 |
| C | archive `--selftest` | fixtures | `SELFTEST checks=14 failed=0` | 0 |
| D | reconstructed pre-repair lane (real index) | pre-erratum | `checks=6 defects=6` | 1 |
| E | archive (no index) | pre-erratum | `checks=6 defects=6` | 1 |
| G | live repaired lane | pre-erratum | `checks=6 defects=2` | 1 |
| H | `git archive c227e486` (no index) | live repaired | `checks=6 defects=4` | 1 |

RUN A is the frozen predicate's repaired-tree clause, exactly as written.
RUN D reproduces the committed control `defects-before.txt` **byte-for-byte**: the seven
`DEFECT`/`checks=` lines hash `c6c732e7…c31e2` in both files (`diff` empty).
RUN C passes 14/14 on the archive copy of the counter, i.e. on the frozen program bytes.

Integrity fact that makes RUN A meaningful: the counter's sha256 is
`6ef17abc…64d5b6` in BOTH the `f0b20aea` archive and the live lane. The predicate program
was not edited between freeze and the live run — the green result is a re-derivation, not a
moved goalpost. RUN A also read committed bytes: `git status --porcelain` is empty for all
five inputs (SCORECARD, both lessons, the wave-32 tree, the counter).

## 3. The live-vs-archive delta, precisely

Archive (B) shows 4 where the control shows 6. Three distinct causes, none a repair inside
the archive:

1. **N3/N4 are fleet-coupled by construction.** `plans/round33_defects.py:40` hardcodes
   `FLEET = Path("/home/vgpnk/Projects/shokunin")`; `check_n3`/`check_n4` default to reports
   under it, and `--lane` does not redirect them. The fleet repo already carries the L1's
   erratum commit `3d3ca566`, so on *any* lane tree — including the freeze archive — N3/N4
   read repaired report bytes and go green. RUN G isolates this exactly: repaired lane +
   pre-erratum fleet reddens exactly N3 and N4 (2 defects), leaving N1/N2/N5/N6 green.
   The counter's own selftest docstring names the hazard ("N3/N4 read absolute fleet paths by
   default, which would couple the selftest to the live repair state") but the mitigation was
   applied to the selftest only, not to the `--lane` path.
2. **N1's archive redness is an artifact, not evidence.** `git archive` exports no index, so
   `git ls-files` fails and `check_n1` reports the git error instead of an untracked set.
   The control's actual N1 finding — 84 untracked paths — reproduces only with an index:
   RUN D's N1 message equals the control's character-for-character, sorted example filenames
   included. The reconstruction is justified, not assumed: `git diff --stat c227e48 HEAD --
   .ufo/waves/round-32` is empty (tree byte-identical since the repair), tracked counts are
   5 at `f0b20aea` and 89 at `c227e48`, and 89 files sit on disk → 84 untracked.
3. **N2/N5/N6 are pure lane-content checks** and behave exactly as claimed: red on
   `f0b20aea` (B, D, E), green on the repaired tip (A, G).

So the frozen control is a valid record, but reproducible only as a **joint state**:
lane@`f0b20aea` + fleet@pre-`3d3ca566`. Conditional on that state both directions of the
predicate hold: `defects=6 exit 1` before, `defects=0 exit 0` after (RUN A).

N1 green at `c227e486` (the claim's stated landing): **[INFERENCE]** from the empty diff
above plus live tracked=89/untracked=0. The lane repo was not reconstructed at that commit
(no `git clone` permitted), so this is inference, not a measured run.

## 4. New calibration defect found (reported, not fixed — production file)

`corpus/evidence/round33/defects-after.txt` (sha256 `c807bc7d…6d79ea`) states
`checks=6 defects=0 / exit=0` and then `# revision: c227e486a622ff…`. That file was added
by `7895588` and does **not** exist at `c227e486`; running the counter on the `c227e486`
tree prints `checks=6 defects=4` (RUN H). Token counts agree: `^## Round 32` in SCORECARD,
`:39-40` in round-31 lesson, `:72` in round-30 lesson are all absent at `c227e486`, present
at HEAD.

The numbers are true of `7895588` (RUN A). The revision label is not. Even read charitably
as "c227e486 is the N1 repair", the receipt then omits the tip that makes it re-runnable —
which is exactly what QUALITY Q22, added in the same commit, demands. This is the round-32
`landing` class recurring in round 33.

**Draft repair bytes for the L1** (append-only, safest form; `corpus/evidence/round33/defects-after.txt`):

```
# revision-correction (round 33, R33ExecDefsBefore): the run tree is 7895588, which added this
# receipt; the file does not exist at c227e486 and that revision prints checks=6 defects=4 exit=1.
# Evidence: .ufo/waves/round-33/build/receipts/defs-repro.txt §5b (RUN H).
```

If the receipt is instead meant to be regenerated in place, the label line should become
`# revision: 78955888542258ba369f5aa72c200c913b4c3c90`.

## 5. Draft lesson rows for `corpus/lessons/round-33.md` §Mistakes (L1 integrates)

```
| instrument-coupling | `plans/round33_defects.py` N3/N4 read the absolute `FLEET` root, so the C2 freeze control re-derives only as a joint state (lane@f0b20aea + fleet@pre-3d3ca566); `--lane <archive>` prints `defects=4` against a recorded 6 | R33ExecDefsBefore RUN B/G, `build/receipts/defs-repro.txt` §6 | control cited from its committed bytes; any `--lane` re-run must name both trees |
| receipt-binding | `corpus/evidence/round33/defects-after.txt` names `revision: c227e486`, a commit that lacks the file and prints `defects=4` — Q22's first catch on a same-commit receipt | R33ExecDefsBefore RUN H, `build/receipts/defs-repro.txt` §5b | revision line names the run tip (`7895588`); append a correction line |
```

## 6. How C2's receipt should cite this

- Repaired-tree clause: cite RUN A (`checks=6 defects=0`, exit 0) at `7895588`.
- Pre-repair clause: cite the committed `defects-before.txt` (sha256 `0e8cabd7…7af78`) and
  RUN D as its reproduction; state the joint-state precondition, otherwise a reviewer
  re-running the archive will see 4 and misread it as a regression or a failed reproduction.

## 7. Evidence retained

- Receipt: `.ufo/waves/round-33/build/receipts/defs-repro.txt` — verbatim stdout of A–H,
  exit codes, sha256s of counter/control/variant/fleet fixtures, delta table.
- Control: `.ufo/waves/round-33/claims/defects-before.txt`, sha256 `0e8cabd7…7af78`.
- Counter: sha256 `6ef17abc…64d5b6` (archive == live).
- Reproduction variant: `/tmp/r33-defsbefore/variant/round33_defects_fleetpre.py`,
  sha256 `c4079547…9dbd0`, one line changed (`FLEET`), everything else frozen bytes.
- Pre-erratum fleet fixtures: round-31 `cf141d2c…0d71`, round-32 `75ed1719…60cf`, taken from
  `git show '3d3ca566^:…'`.
- Bounded archive: 194,560 bytes (full `f0b20aea` archive is 492,144,640 bytes and was NOT
  extracted — 60 MB scratch bound; only the five paths the counter reads were materialised,
  so every consumed byte is the committed byte).

## 8. Risks / blockers

- **Blocker:** none.
- **Risk (for the L1):** if C2's receipt quotes `defects-after.txt` without the §4
  correction, the claim inherits a non-self-binding receipt — the precise class round 32
  routed. Fix is one appended line.
- **Risk (design):** the fleet coupling means C2 cannot be re-verified from a lane archive
  alone; a future round wanting an independently re-runnable control needs N3/N4 to accept a
  fleet root (e.g. a `--fleet` flag). Not fixed here: out of my write scope and not asked.
- **Not run:** the C1/C3 counters (out of scope); the full archive extraction (disk bound);
  no lane reconstruction at `c227e486` (§3, no clone).
