# R37QualityDraft — QUALITY.md Q26 / Q27 draft (kengaku round 37, wave 1)

Seat: `R37QualityDraft` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Deliverable: two paste-ready QUALITY.md rows for the L1 to integrate. I did not edit the lane.

## 1. Behaviour

Read, in this order: `plans/round-37-claims.md` (frozen, C1/C2, excluded branches, limits),
`corpus/QUALITY.md` (all 25 rows; Q22–Q25 and their Lesson lines in full),
`corpus/lessons/round-36-verifier-spotcheck.md` (lines 68–74, 86–96),
`plans/round37_c1_verify.py` (docstring + frozen `MUTANTS` table), the five
`.ufo/waves/round-37/claims/control-*.txt` receipts, `corpus/SOURCES.md` (103 registry rows),
`SCORECARD.md:564` (the `package-gate` capability row), `plans/pkg_gate.py` (docstring).

Then I wrote a reference implementation of the Q26 check
(`build/R37QualityDraft/anchor_digest_check.py`), measured the lane with it, and ran two
controls: a **broken** copy of `corpus/SOURCES.md` (mutation) and a **repaired** copy
(green-after). All three runs are recorded below. Nothing in the lane was modified; the
mutated and repaired trees are scratch copies under `/fast/scratch/hyaku/kengaku-r37/R37QualityDraft/`.
I did not run the C1 counter: its freeze receipt is the evidence, and the counter prints
`PREDICATE C1 n/a` outside the predicate mode.

## 2. Paste-ready markdown (append after Q25)

```markdown
## Round37 criterion — an anchor digest is 64 hex and a digest of committed bytes

- **Q26 — every `sha256` token in a `SOURCES.md` registry row's `anchor` cell is 64 lowercase
  hex and equals a digest in a committed manifest, unless the cell itself declares it an
  abbreviated prefix or a snapshot hash.** The anchor cell is the one place a row states "these
  are the bytes I read", and a digest that lost a character still parses as a cell: the round-36
  spot-check found S110's anchor carrying 63 hex while the manifest, the capture and the live
  bytes carried 64 (`corpus/lessons/round-36-verifier-spotcheck.md:71`), agreed the admission
  anyway, and routed the missing check instead of pretending the counter had one (`:88`: "Add a
  counter check that each row's anchor digest equals the capture manifest"). Measured at the
  criterion's creation (2026-10-26, lane tip `3ea9a1d9`): 103 registry rows, 7 committed
  manifests, 11 `sha256` tokens — `tokens_ok=7 bad_shape=1 declared_snapshot=1 unmarked=2`. The
  bad shape is S110's 63-hex token; the declared snapshot is S072 ("snapshot hash, not a manifest
  pin" in its own cell); S073 and S074 assert digests of live-fetched bytes with neither a
  manifest entry nor the declaration. Check (executable): `python3 plans/anchor_digest_check.py
  --lane .` scans each `| S### |` row's seventh cell for `sha256 ` + optional backtick + hex + an
  optional `…`, and counts a token as a pass when it is 64 hex present in a committed
  `corpus/evidence/**/SHA256SUMS*` or `plans/fixtures/**/manifest.*` digest set, when it is
  shorter and ends in `…` (a declared prefix, as S036's `afaae9dd…`), or when the same cell says
  "snapshot hash, not a manifest pin". The landing requires `bad_shape=0 unmarked=0`, exit 0; the
  three red rows are corrected by appended errata that name the superseded cells (R1), never by
  rewriting them. Shown able to fail (2026-10-26, scratch copies of the lane's own `SOURCES.md`
  and manifests): deleting one hex from S108's token and replacing S109's with 64 zeros gives
  `tokens_ok=5 bad_shape=2 declared_snapshot=1 unmarked=3`, prints `BAD_SHAPE S108 len=63` and
  `UNMARKED S109 0000…`, exit 1; the repaired control (S110 restored to
  `4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c`, S108/S109 restored,
  S073/S074 marked) gives `tokens_ok=8 bad_shape=0 declared_snapshot=3 unmarked=0`, exit 0. The
  repair's source is the manifest's own line: `corpus/evidence/round36/tb2-regex-log/SHA256SUMS:3`
  carries that digest for `instruction.md`.
  Limits: this is a shape-and-membership check, not a truth check — a 64-hex token that is a
  digest of the wrong file, or of nothing, passes whenever it appears in some manifest; four
  committed manifests share the basenames `test_outputs.py` (3), `instruction.md` (3),
  `test.sh` (3), `task.toml` (3) and `solve.sh` (2), so membership attributes a digest to a
  capture set, not to the revision a row claims, and the pin→capture binding stays with the
  counters that run the probe (`pkg_gate.py` P5, the round-37 C2 counter's W1); rows that cite a
  digest inside another file without a token (S037 "pinned by sha256 in the script", S061
  "sha256 in plans/fixtures/r28/webarena/manifest.json") pass vacuously, so the rule governs the
  token a reader can copy, not every digest a row mentions; a live-URL row with no committed
  capture can satisfy only the declaration leg; and the check reads the manifests, so a manifest
  edited to contain a bad digest would launder its rows — those digests are re-derived by the
  round's package-gate run (Q20, Q24), not by this criterion.
  Lesson: `corpus/lessons/round-37.md` §Mistakes (1) — the lesson this round mines the
  S110 truncated anchor into; the criterion's grounding is independent of that file's wording
  (`round-36-verifier-spotcheck.md:71,:88` and the receipts below). Supersedes: none. It is the
  check routed item 1 asked for; Q10's second-seat re-read found the typo, and Q24's gate checks
  manifest digests inside a package (P5) but never the registry's own anchor cells.

## Round37 criterion — an advertised defect class is held only when a fixture kills its silence mutant

- **Q27 — a gate's advertised defect class counts as held only when a single-defect fixture kills
  that class's silence mutant; a class whose mutant no fixture kills is advertised debt.** A
  battery that shows the gate accepts the genuine package and rejects a few junk packages proves
  the battery's reach, not the gate's: the round-36 battery was green at 14/14 while the gate's
  branch silences went untested, so the round-37 counter against the same 14 fixtures and 55
  frozen single-branch mutants prints `MUTANTS total=55 killed=5 survived=50 invalid=0
  null_detected=0` and `PREDICATE C1 fail`, exit 1
  (`.ufo/waves/round-37/claims/control-c1-nothing.txt`) — 50 of the classes the gate's docstring,
  Q24 and the `package-gate` capability row (`SCORECARD.md:564`) advertise changed nothing
  observable on any fixture. Check (executable, round-37 instance): `python3
  plans/round37_c1_verify.py --lane .` prints `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`,
  then `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1
  pass`, exit 0, on a clean clone of the landing tip with `plans/pkg_gate.py` at
  `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`. A class is demonstrated
  when its one frozen `old → new` replacement applies exactly once and compiles (`invalid=0`) and
  some fixture's observable result — the pair (exit code, set of clause ids printing `DEFECT`) —
  differs from the unmodified gate's (`killed`); an unmodified copy of the gate must change
  nothing (`null_detected=0`), each fixture must carry the reference's exact verdict and `DEFECT`
  set (`wrong=0`), and every fixture must give the same result under another directory name
  (`renamed_disagree=0`). Shown able to fail: the do-nothing control at the freeze reads
  `killed=5/55`; editing the gate so the mutants stop applying reads `invalid=55`
  (`control-c1-gate-edited.txt`); mislabelling the genuine package a reject reads `wrong=1`
  (`control-c1-mislabel.txt`); and the one-fixture API example kills exactly one further class,
  `killed=6/55` (`control-c1-example.txt`, M08) — which is why the standard is per class, not per
  battery.
  Limits: demonstration is observational — a killing fixture shows the branch is reached and its
  result is visible, never that the check is the right check; the branches excluded from the 55
  are named in `plans/round-37-claims.md` and stay unclaimed (the empty `frozen_instruments`
  branch of P1, every `spec not found` / `root not a directory` setup path, P10's
  `OSError`/`SubprocessError` branch, `run_checks`' clause-crash handler, `main`'s crash→exit-2
  handler, the `--require-clean-tree`/`--rerun` option gating), so a gate can hold this criterion
  and still be wrong on a setup path; the mutant list is the denominator, so a branch nobody wrote
  a mutant for is invisible, and an equivalent mutant found later is reported as a limit of the
  freeze, never removed; a kill records a result difference, not a reason — the result is the raw
  exit code, so a mutant killed by making the gate crash on a fixture counts the same as one
  killed by its clause firing, and single-defect fixtures reduce but do not remove co-occurrence
  (the round-36 all-junk fixture declares `P1,P3,P6,P9`); 55 fixtures is a budget, not a search
  for every reachable defect.
  Lesson: `corpus/lessons/round-37.md` §Mistakes (2); the freeze control is
  `.ufo/waves/round-37/claims/control-c1-nothing.txt`. Supersedes Q24's middle clause, "every
  single-property junk mutant must be rejected", as the proof standard: a property-level battery
  is satisfied by 14 fixtures while 50 branch silences go untested. Q24's ordering rule (battery
  before the first data receipt) and its `unevaluated` leg stand unamended.
```

## 3. Evidence (every number carries its command)

| # | command | output |
|---|---|---|
| E1 | `grep -oE 'sha256 [0-9a-fA-F]+' corpus/SOURCES.md \| wc -l` | `10` (undercounts: S070's token sits behind a backtick; the authoritative count is E3's 11) |
| E2 | `awk -F'\|' '$2 ~ /S110/ {print $7}' corpus/SOURCES.md` | `…; sha256 4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c` — 63 hex |
| E3 | `python3 build/R37QualityDraft/anchor_digest_check.py --lane .` | `BAD_SHAPE S110 len=63`, `UNMARKED S073 97b8671f…`, `UNMARKED S074 f996dfee…`, `rows=103 manifests=7 tokens_ok=7 bad_shape=1 declared_snapshot=1 unmarked=2`, `exit=1` |
| E4 | same, `--lane $S/ctl` (mutated copy: S108 one hex deleted, S109 → 64 zeros) | `rows=103 manifests=7 tokens_ok=5 bad_shape=2 declared_snapshot=1 unmarked=3`, `exit=1` |
| E5 | same, `--lane $S/green` (S110 corrected to the manifest digest, S108/S109 restored, S073/S074 marked) | `rows=103 manifests=7 tokens_ok=8 bad_shape=0 declared_snapshot=3 unmarked=0`, `exit=0` |
| E6 | `grep -n 'instruction.md' corpus/evidence/round36/tb2-regex-log/SHA256SUMS` | `3:4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c  instruction.md` |
| E7 | `cat` of the four TB2 `SHA256SUMS` → `awk 'NF>=2{print $2}' \| sort \| uniq -c \| awk '$1>1'` | `3 instruction.md`, `2 solve.sh`, `3 task.toml`, `3 test_outputs.py`, `3 test.sh` (basename collisions, the Q26 limit) |
| E8 | `grep -E 'MUTANTS\|PREDICATE\|exit=' .ufo/waves/round-37/claims/control-c1-nothing.txt` | `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`, `PREDICATE C1 fail`, `exit=1` |
| E9 | same, `control-c1-gate-edited.txt` | `MUTANTS total=55 killed=0 survived=0 invalid=55 null_detected=0`, `PREDICATE C1 fail`, `exit=1` |
| E10 | same, `control-c1-mislabel.txt` | `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`, `PREDICATE C1 fail`, `exit=1` |
| E11 | same, `control-c1-example.txt` | `MUTANTS total=55 killed=6 survived=49 invalid=0 null_detected=0`, `PREDICATE C1 fail`, `exit=1` |
| E12 | `grep -cE '^\| S11[1-9] ' corpus/SOURCES.md` | `0` — C2's S111–S113 rows are not in the registry at this moment, so Q26 is measured on the pre-C2 row set |
| E13 | `ls corpus/lessons/round-37.md` | `No such file or directory` — the Lesson path Q26/Q27 name is a dependency, not a landed file |

Mutation control notes: the mutated tree is `cp corpus/SOURCES.md → $S/ctl/corpus/SOURCES.md` plus
symlinks to the lane's real `corpus/evidence` and `plans`, so E4's `unmarked` growth (S109) is a
retargeted digest, not a missing manifest. The `S110` red in E3 and E4 is the lane's own defect, present
at tip; E5 shows the identical checker going green on the same 103 rows.

## 4. Gates

- No lane gate was run by me, and none of my numbers is a gate result: E3–E5 are my own reference
  implementation's output, E8–E11 are the frozen claim's committed control receipts, E12–E13 are `ls`/`grep`.
- `python3 plans/round37_c1_verify.py --lane .` was **not** executed (the battery is wave-1 work in
  flight; a `--only` development run prints `PREDICATE C1 n/a` and would prove nothing about the
  criterion). Q27's check line is the frozen predicate, quoted from
  `plans/round-37-claims.md` §C1 and `plans/round37_c1_verify.py:6-10`.
- The `--battery-dir` development mode was not used: no fixture of mine.

## 5. Findings for the L1 (integration obligations, in priority order)

1. **Q26 lands red on three rows unless the errata land with it.** At tip: S110 (63 hex), S073 and
   S074 (digests of live-fetched bytes, no manifest entry, no declaration). Two integration options,
   both admissible: (a) append the three errata in the same commit — S110's corrected cell is E6,
   S073/S074 gain "(snapshot hash, not a manifest pin)" or a committed capture — and the Check cell's
   `bad_shape=0 unmarked=0` is then true at the landing; or (b) land Q26 with an explicit `before`
   line citing E3 and keep the red visible. Do not rewrite the cells in place (R1).
2. **Q26's check has no landed tool yet.** The reference implementation is
   `build/R37QualityDraft/anchor_digest_check.py` (2.9 KB, stdlib only, `--lane` default `.`, exit 0/1,
   one summary line). Copy it to `plans/anchor_digest_check.py`; per Q20 the landing that adds a
   `plans/*.py` must carry an out-of-band gate run made in an extracted tree. If the L1 prefers a
   different path, change the Check cell and the docstring together.
3. **The Lesson path is unresolved.** `corpus/lessons/round-37.md` does not exist (E13), and the peer
   named `ScribeLesson` states it owns `corpus/lessons/round-33.md` only and must not be cited. Both
   rows name `corpus/lessons/round-37.md` §Mistakes (1)/(2) because that is the round's lesson by the
   lane's own convention (`round-36.md` §Mistakes (1)/(2) are the Q24/Q25 Lesson lines). If the round-37
   lesson lands at another path, re-point both Lesson cells; the criteria's grounding survives the
   repoint, since it rests on E3–E11 and `round-36-verifier-spotcheck.md:71,:88`.
   **Marked dependency: different-path.** A criterion whose Lesson line cites an absent file is a
   Q7-class defect at landing.
4. **Q27 supersedes Q24's middle clause, not Q24.** Q24's `unevaluated` leg stays the crash-vs-rejection
   guard; Q27's counter keeps non-0/1 exit codes as results, so a crash is a kill (named in Q27's
   Limits). If the L1 would rather delete Q24, the `unevaluated=14` control loses its home.
5. **Q27 does not restate the mutant table or the excluded branches** — both are named by reference.
   A battery37 change therefore never forces a QUALITY.md edit; a *mutant-list* change is a re-freeze
   under the claim's kill rule, not a criterion edit.
6. **No criterion was written for C2** in this seat. C2's cheap falsifier (a requirement map whose
   labels agree with the executed receipt, V7) is already a check inside its own counter; if the L1
   wants a corpus-level row, the honest one is "a requirement map's label is the observed verdict, not
   the instruction's claim" — that is a distinct draft, not smuggled into Q26/Q27.
7. **Census interaction:** Q26 adds no SOURCES row and edits no `teaches` cell, so the 15-W04 census
   (`census-before.txt`) is untouched. If the errata append rows (§5.1a), they are new rows and must
   carry 11 cells, a `supersedes S### —` opener and a `used-by` that the index resolves — that is the
   one path by which Q26 can move the census.

## 6. Out of scope (not done, deliberately)

- No edit to `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `plans/`, or any other
  lane file; no git or jj write in the lane; no commit, push or publish.
- No battery37 fixture, no `--battery-dir` run, no gate or counter re-run (wave-1 executors own those;
  a scribe that re-ran them would duplicate their receipts).
- No attempt to repair S110/S073/S074 in the lane — the errata are the L1's to append.
- The C2 probe and its receipt were read only as context; no probe case was executed.

## 7. Artifact paths

- This report: `.ufo/waves/round-37/build/R37QualityDraft.md`
- Reference check (copy to `plans/anchor_digest_check.py` to land Q26):
  `.ufo/waves/round-37/build/R37QualityDraft/anchor_digest_check.py`
- Scratch (deleted before this report was written, nothing copied from it except the numbers above):
  `/fast/scratch/hyaku/kengaku-r37/R37QualityDraft/` — `ctl/`, `green/`, `q26check.py`, `q26final.py`
- Read-only inputs: `plans/round-37-claims.md`, `corpus/QUALITY.md`, `plans/round37_c1_verify.py`,
  `corpus/SOURCES.md`, `SCORECARD.md:564`, `plans/pkg_gate.py`, `corpus/lessons/round-36-verifier-spotcheck.md`,
  `.ufo/waves/round-37/claims/{control-c1-*,census-before}.txt`,
  `corpus/evidence/{round35/tb2-eval,round36/tb2-regex-log,round37/tb2-git-webserver}/SHA256SUMS`.

VERDICT: quality-drafted-2-criteria
