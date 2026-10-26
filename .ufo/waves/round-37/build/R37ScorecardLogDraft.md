# R37ScorecardLogDraft — round-37 SCORECARD section + LOG entry (drafts only)

Seat: `R37ScorecardLogDraft`, scribe, kengaku round 37 (hyaku run 8), wave 1, 2026-10-26.
Deliverable: draft text for `SCORECARD.md` `## Round 37` + two `## Capabilities` rows + the `LOG.md` round-37
entry. **Nothing in the lane was edited.** No clone, no scratch tree, no fixture was created by this seat
(there is nothing to delete); no tool was installed.

## 0. State measured at draft time (read-only)

| fact | command | output |
|---|---|---|
| lane HEAD | `git --no-pager log --oneline -1` | `44b7298 round-37: wave-1 spec and validated dispatch (40 seats, policy v1)` |
| history hop | `git --no-pager log --oneline -6` | `44b7298 round-37: wave-1 spec and validated dispatch (40 seats, policy v1)`, `5c7b34e round-37: first recorded probe run (22 cases, 0 mismatches; second run byte-equal)`, `ca79046 round-37: freeze claims C1 (gate mutants 55, before killed=5) and C2 (TB2 configure-git-webserver), counters, probe, captures, controls`, `3ea9a1d round-36 verifier spot-check (integrator, hyaku): non-author admit/reject`, `0fb87f8 round-36: final measurement receipt and census after`, `612458f round-36: close wave-1-only round, wording fixes, digest correction, errata, wave-1 results` |
| gate at freeze digest (unedited) | `sha256sum plans/pkg_gate.py` | `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` |
| probe at freeze digest (unedited) | `sha256sum plans/git_webserver_probe.py` | `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf` |
| battery37 not yet landed at first check | `ls plans/battery37` | `No such file or directory`; later in the same draft window six untracked modules appeared — `ls plans/battery37/*.py` → `d4.py d5.py p23.py p4.py p7.py p8.py`, `grep -c '"fid"'` per module → `3 7 6 4 6 5` (lines containing `"fid"`, not a fixture count); the battery is still partial and being written by wave-1 seats |
| C2 entry not yet landed | `ls corpus/knowledge/tb2-git-webserver-grader.md` | `No such file or directory` |
| registry rows before | `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` | `103` |
| knowledge files / index rows before | `ls corpus/knowledge/*.md \| wc -l`; `grep -c '^| \`knowledge/' corpus/README.md` | `43` / `43` |
| capability rows before | `sed -n '553,570p' SCORECARD.md \| grep -oE '^\| [a-z][a-z-]+' \| wc -l` | `11` |
| census before | `grep -c W04 .ufo/waves/round-37/claims/census-before.txt` | `15` (last line `kengaku ok …/corpus/SOURCES.md`, `exit=0`) |
| C1 freeze control | `cat .ufo/waves/round-37/claims/control-c1-nothing.txt` | `BATTERY fixtures=14 wrong=0 renamed_disagree=0`; `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`; `PREDICATE C1 fail`; `exit=1` |
| C2 freeze control | `cat .ufo/waves/round-37/claims/control-c2-nothing.txt` | `checks=7 defects=4` (V2, V3, V4, V7 red); `PREDICATE C2 fail`; `exit=1` |
| probe receipt summary | `grep -nE '^cases=\|match=NO' corpus/evidence/round37/git-webserver-probe.txt` | line 49 `cases=22 observed_pass=9 observed_fail=13 mismatches=0`; no `match=NO` line |
| dry table | `tail -1 corpus/evidence/round37/git-webserver-dry-cases-freeze.txt` | `cases=22 predicted_pass=9 predicted_fail=13` |
| capture sizes | `wc -l corpus/evidence/round37/tb2-git-webserver/{instruction.md,verify.sh,test_outputs.py}` | `10`, `91`, `13` |
| bubblewrap is the sandbox | `grep -n bwrap plans/git_webserver_probe.py` | `:49 BWRAP = "/usr/bin/bwrap"` |

Because both after-values require the landing tip (battery37 present, entry/index/registry rows present), every
after-cell below is the literal placeholder `<pending: integration>`. No after-value is estimated, inferred or
extrapolated.

## 1. Draft A — `SCORECARD.md` section (append at end of file, after the round-36 close/errata block)

````markdown
## Round 37 (hyaku run 8, 2026-10-26): gate mutant harness, one TB2 service grader executed

Baseline `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd`; frozen prereg `plans/round-37-claims.md` (freeze
`ca790460e9b74d4dc5870c878affd13cc9c4437a`; first recorded probe run
`5c7b34e9223f460a440596e3a76bdae8bfdd37d8`). Lowest non-retired axis: coverage 7, tied with novelty 7; coverage
chosen by the frozen tie-break (a pinned local source and an offline sandbox exist, and the round-36 planning
seat priced the novelty candidate — a requirement-class census — as covered by published work,
`.ufo/waves/round-36/build/R36PlanNext.md` §1.4). Coverage stays capped by the open L0 question
(`.ufo/l0-questions.md`, `kengaku | round-33`); C2 is judged on its counter, not on a score move. Calibration is
the round-36 `### Planned (round 37)` row. No stagnation waiver.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 gate mutant harness: 55 frozen one-branch mutants against `plans/pkg_gate.py` (freeze digest `ea63882240e6…`) over the round-36 battery (14 fixtures) plus `plans/battery37/*.py` | **calibration** | `python3 plans/round37_c1_verify.py --lane .` on a clean clone: before `BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-37/claims/control-c1-nothing.txt`; the five demonstrated classes are M01 P1, M05 P3, M40 P9, M47 D4, M54 D5) → after `<pending: integration>` | **8 → `<pending: integration>`**; at freeze the mismatch count is 50 advertised-but-undemonstrated clauses |
| C2 pinned TB2 `configure-git-webserver` grader admitted with an executed 22-case sandbox probe (S111-S113) | **coverage** (lowest, tied) | `python3 plans/round37_c2_verify.py --lane .`: before `checks=7 defects=4` exit 1 (`.ufo/waves/round-37/claims/control-c2-nothing.txt`; V2, V3, V4, V7 red) → after `<pending: integration>`; probe `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (`corpus/evidence/round37/git-webserver-probe.txt`) | **7 → 7 held** (L0 cap); frozen predicate `<pending: integration>` |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Capabilities entered (table
above, first-working round 37): `gate-mutation-harness`, `service-grader-sandbox-probe` —
`<pending: integration>`; both rows are drafted with their demonstration commands (Draft C), and a row enters
only with its after measurement. Registry 103 → `<pending: integration>` (the frozen spec names S111, S112,
S113); knowledge files / index rows 43/43 → `<pending: integration>`; census exit 0 with 15 W04 before
(`.ufo/waves/round-37/claims/census-before.txt`), `<pending: integration>` after. Assimilation:
`considerthese/2026-10-25.md` proposal 2(a) (re-run every closed defect's check at the tip) —
`<pending: integration>`. Frontier: census before exit 0, 15 W04; sourced claim C2 (S111-S113 opened this
round 2026-10-26); mistake to mine: the S110 anchor digest that lost one hex digit (round-36 spot-check §5
item 1), whose fix (C2 counter V3) must be shown able to fail.

### Limits named at freeze

- C1's demonstration is observational: a fixture shows the branch is reached and its result is visible, not that
  each check is the right check. Excluded branches, never counted in the 55 and never claimed demonstrated: the
  empty `frozen_instruments` branch of P1; every `spec not found` / `root not a directory` setup path; the
  `OSError`/`SubprocessError` branch of P10; the `run_checks` clause-crash handler and `main`'s crash → exit 2;
  the `--require-clean-tree`/`--rerun` option gating.
- C2's probe shows what the grader's verdict depends on with `apt-get` and `expect` absent; it never runs the
  oracle or a real git push, so it does not show that the intended path passes. Predictions were written before
  the first run (`cases=22 predicted_pass=9 predicted_fail=13`); a prediction/observation mismatch is reported,
  never re-predicted.

### Planned (round 38) — proposed; the L1 decides

- Calibration: land the persistent ledger checker over the round-37 mutant list so every advertised clause
  re-runs at each tip (the assimilation proposal 2(a) debt), or price the excluded branches and name them
  permanent non-claims.
- Coverage/novelty (tied 7): the remaining unenforced faces of the service grader's requirement map, or the
  prior-art-gated requirement-class census across the three admitted graders; keep the frozen predicate and
  control in the same sentence.
````

## 2. Draft C — two rows to append to the `## Capabilities` table (main table, line 553)

First-working round is marked `37` with the pending qualifier; the L1 drops the qualifier only after the C1/C2
after-measurement exists.

````markdown
| gate-mutation-harness | Decide which of a gate's advertised defect clauses its own battery actually demonstrates: one frozen byte-level mutant per branch, killed iff the observable result — exit code plus the set of clause ids printing `DEFECT` — changes on some fixture, with a null mutant for non-determinism and a renamed run so no fixture can be recognised by its directory name. Survivors are advertised-but-undemonstrated clauses. Not proof that any check is the right check. | `python3 plans/round37_c1_verify.py --lane .` on a clean clone → `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` (after value `<pending: integration>`; freeze control `killed=5 survived=50`, `.ufo/waves/round-37/claims/control-c1-nothing.txt`) | 37 (pending integration) |
| service-grader-sandbox-probe | The pinned-grader-probe instrument on a grader whose graded artefact is a live HTTP service rather than a data string or an agent-authored file: 22 frozen cases (curl and wget branches), each served its own body inside a bubblewrap sandbox with a private network namespace, HOME and /tmp in scratch and `/tests` bound read-only to the captures, one prediction per case written from a static read before the first run. Not task validity; never runs the oracle or a real git push. | `python3 plans/git_webserver_probe.py --lane .` → `cases=22 observed_pass=9 observed_fail=13 mismatches=0`; receipt `corpus/evidence/round37/git-webserver-probe.txt`, second run byte-equal at `5c7b34e9`; `plans/round37_c2_verify.py` V4/V5 pin the receipt and the `--dry` table and V2's `P10` re-runs the probe and byte-compares it | 37 (pending integration) |
````

## 3. Draft B — `LOG.md` entry (append at end, after the round-36 close block)

````markdown
## Round 37 — 2026-10-26 (hyaku run 8)

Declared C1 calibration (8): attack the round-36 gate itself — 55 frozen one-branch mutants
(`plans/round37_c1_verify.py`) against `plans/pkg_gate.py` at its freeze digest, a null mutant and a
renamed-fixture run included, until every advertised defect class has a single-defect fixture in
`plans/battery37/`; survivors are advertised-but-undemonstrated clauses. Declared C2 coverage (lowest, tied 7):
admit the pinned Terminal-Bench 2.0 `configure-git-webserver` grader (S111 `tests/test_outputs.py`, S112
`tests/verify.sh`, S113 `instruction.md` @ `2fd12b88`) as `corpus/knowledge/tb2-git-webserver-grader.md` with an
executed 22-case sandbox probe. Baseline `3ea9a1d9`; freeze `ca790460` (claims, both counters, the probe case
table with predictions, six captures, six red controls); first recorded probe run `5c7b34e9`.

- Probe: `python3 plans/git_webserver_probe.py --lane .` → `cases=22 observed_pass=9 observed_fail=13
  mismatches=0`; a second run byte-equal (`5c7b34e9`). Each case runs the captured grader in a bubblewrap sandbox
  (`/usr/bin/bwrap`, `plans/git_webserver_probe.py:49`): private network namespace, HOME and /tmp in scratch,
  `/tests` bound read-only to `corpus/evidence/round37/tb2-git-webserver/` (six files, `SHA256SUMS`).
- Findings: a file served on :8080 with no git repository, hook or push passes, because `verify.sh:49` never reads
  the expect step's status (`static-file-no-git`); a body that merely contains the text `TEST PASSED` passes even
  though `verify.sh` prints `TEST FAILED`, because `test_outputs.py:13` checks a substring of stdout that echoes
  the body (`token-in-body`, and on the wget branch `wget-token-in-body`); status and content are read by two
  separate requests (`verify.sh:57`, `verify.sh:60`; `status-then-content-split`); curl runs without `-L` and
  without a timeout; command substitution at `verify.sh:60` strips trailing newlines only, so a trailing space, a
  CR, a BOM and any case change fail while extra newlines pass.
- C1: at freeze `BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=5 survived=50
  invalid=0 null_detected=0` — only M01 (P1 instrument pin), M05 (P3 unparsed row), M40 (P9 untracked), M47 (D4
  pattern) and M54 (D5 manifest digest) are demonstrated, so 50 advertised clauses had no fixture. `plans/battery37/`
  was written clause by clause; measurement after `<pending: integration>`.
- C2 counter: before `checks=7 defects=4` (V2, V3, V4, V7 red, `control-c2-nothing.txt`); after
  `<pending: integration>`. V3 is the round-36 routed item 1 fix (an anchor cell must carry a full 64-hex pin and
  no other sha256 token); V2 brings the gate's quote-support clauses to C2 (round-36 routed item 3, a counter that
  admitted a junk package).
- Controls red at freeze: `control-c1-nothing.txt` (`killed=5 survived=50`), `control-c1-gate-edited.txt`
  (`invalid=55`), `control-c1-mislabel.txt` (`wrong=1`), `control-c1-example.txt` (a single-defect example kills
  one further mutant only), `control-c2-nothing.txt` (`checks=7 defects=4`), `control-c2-skip.txt` (junk rows whose
  anchors carry the right digests and eight one-word quotes → V2 red).
- Frozen predicates, the mutant list and the batteries are not edited after freeze; an equivalent mutant found
  later is reported as a limit of this freeze, never removed.
- Wave-1 falsifiers: `<pending: integration>`.
- Scope wording (PROVINCE): the round-37 grader is the lane's first service/state grader — a stdout substring over
  a helper shell script that probes a live HTTP service — and the probe runs offline in a sandbox, without the task
  image, apt or expect.
- Tool use: the frozen probe runs host `bwrap`, `curl` and `wget`; no package was installed or upgraded this round
  (no uv/PyPI dependency added).
````

## 4. Integration constraints the L1 must respect when filling the after-cells

1. **C1's after value is a clean-clone measurement of the landing tip**, with `plans/pkg_gate.py` at
   `ea638822…`. The predicate needs `BATTERY fixtures=<n> wrong=0 renamed_disagree=0` and
   `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` and `PREDICATE C1 pass`, exit 0.
   `<n>` is 14 plus the number of `FIXTURES` entries in `plans/battery37/*.py`; it is not known at draft time.
2. **C2 must be whole when C1 is measured.** `plans/round-37-claims.md` (Separability) requires the knowledge
   entry, its `corpus/README.md` index row and the S111-S113 registry rows to be either all present or all absent
   during the C1 run: the genuine fixture copies `corpus/knowledge/*.md` and the README, and P8 compares knowledge
   files with index rows. A half-landed C2 shows up as a C1 `wrong` declaration, not as a kill.
3. **S111-S113 land together with the row count.** `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` is 103 now; the
   three frozen pins make 106 if each gets one row — count it at integration rather than copying this line.
4. **C2's row is `7 → 7 held`** regardless of the green counter (L0 cap on file, `.ufo/l0-questions.md`), and the
   C2 verdict sentence must not claim a score move.
5. **Do not upgrade a freeze control into an after-value.** The `killed=5` / `checks=7 defects=4` numbers in this
   draft are before-values only, each with its control file path.

## 5. Out of scope for this seat

- No edit to `SCORECARD.md`, `LOG.md`, `corpus/`, `plans/`, the Git index or jj state; drafts only.
- No re-run of either counter, the probe or any fixture; no clone, no scratch tree, no fixture (nothing to clean).
- No capability-table row entered; rows are drafts with the after-value still pending.
- No assessment of whether C1/C2 pass; that is the wave-1 falsifiers' and the integration measurement's job.

VERDICT: scorecard-log-drafted
