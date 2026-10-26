# R38PlanNext — `### Planned (round 39)` data walk (kengaku r38, wave 1, scout)

Seat: R38PlanNext (scout, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`,
read-only; nothing in the lane was edited, staged or committed. Scratch `/fast/scratch/hyaku/kengaku-r38/R38PlanNext/`
(removed at the end, §9). Receipts copied first: `.ufo/waves/round-38/build/R38PlanNext/receipts/`.

Axes named before work (Godspeed): **A1** class distance from the four graders read (data string, agent regex, live
service, build provenance); **A2** offline executability and recomputable expected verdicts; **A3** quote supply
(>= 8 distinct located 3-25-word lines); **A4** prior-art clearance; **A5** reachability of a calibration gap by a
frozen counter; **A6** a do-nothing control that can be run now. A2/A3/A6 ran first; A4 only on survivors.

## 0. Headline

Two candidates priced, each with a control executed this seat. A third (novelty) was priced and **not filed**.

1. **Coverage/novelty 7 (lowest, capped):** TB2 `git-leak-recovery` @ `2fd12b88` — a **repository-history-state** grader
   class. Measured: the task's own `challenge-setup.sh` reproduces the graded initial state offline, the expected
   checksum is recomputed (`test_repository_contents_checksum` PASSES on the rebuilt repo), the oracle passes 5/5,
   the **untouched** repo passes 4/5, a one-line `echo` passes 5/5 while the secret stays in the repo, and an empty
   tree fails 5/5.
2. **Calibration 8:** the instruments rounds 36-38 added to *check the lane* (anchor-digest tool, attribution audit,
   `ledger_tip`) are tripwires with no frozen mutant list. Measured: the standing detector pair kills **1 of 5**
   anchor-tool mutants, the landed-battery audit run changes on **0 of 4** attribution-audit mutants, and
   `ledger_tip` prints `rows=9 closed=9 observed_pass=7 mismatches=2` (exit 1) from a source clone with no `master` ref.

## 1. Inputs read (state at read time, 2026-10-26)

`plans/round-38-claims.md` (full); `SCORECARD.md:1266-1332` (round 37, `### Planned (round 38)`, wave-2 outcome);
`corpus/lessons/round-37-verifier-spotcheck.md` §5 (D1-D7); `.ufo/waves/round-37/build/R37PlanNext.md` (full);
`.ufo/waves/round-37/falsify/` headlines of `F37MutAnchorTool`, `F37MutAttribution`, `F37NoHarmSweep`,
`F37AnchorRerun`, `F37MutC2Counter`, `F37MutProbeCases`, `F37CritOverfit`, `F37CritRenamed`, `F37ScoutMisroot`;
`plans/pkg-spec-r38.json`. TB2 at the pin: blobless clone of `harbor-framework/terminal-bench-2`, all 89
`tests/test_outputs.py` + `environment/` read at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`.

Axis state carried (SCORECARD round 37; round 38 not yet landed): calibration 8, coverage 7, novelty 7, depth 9,
operability 8, freshness 8, adjacency 8. Coverage is capped at 7 by the open L0 question (`kengaku | round-33`,
`plans/round-38-claims.md:18-22`), so candidate A is judged on its counter, not a score move. No stagnation waiver.

Round 38 already took the R37PlanNext coverage candidate (build-pmars) and the C1 mutant list N01-N22 (which carries
B1/B6/B8 and the 13 wave-2 gate survivors). Round 39's debts are therefore different: the **tool** mutants and one
new grader class.

## 2. Candidate A — coverage/novelty 7: TB2 `git-leak-recovery` (repository-history class)

### 2.1 Source (opened this seat, pin = upstream main, `git rev-parse` of each blob at both refs)

| file | git blob (pin = origin/HEAD `2fd12b88`) | sha256 | role |
|---|---|---|---|
| `tests/test_outputs.py` | `30ee951bcfac8ba577d7b83ad0d43f89cdf32c11` | `dc7b01c1b9dbb0c123def54b146dc1dd399a600edee5970d043a5db5eac4c775` | registry row (next free id; S115/S116 are round 38's, so S117 — re-derive at freeze) |
| `instruction.md` | `c1fe9cb6c43c4046281a83e89e1dfc94e10d2c86` | `54ac693fd26a4c003f610d62c4b2671f1d1d04ac5b1286f780605e385a9a5861` | registry row (S118) |
| `environment/challenge-setup.sh` | `a3d6ab23a5712451e921a00a928ec92cdcf5585a` | `a0a19652fc595b0bd06b6970e1d6a455bd4c50991c2ffdcc37fe5b66452b23e2` | capture only (builds the graded state) |
| `solution/solve.sh` | `2e744693a5846f07c7d8f05cae82856624f22307` | `791a7eb23019ee7c93307b35cc77ea334469c4d3688e1171fe1e5ba6fd9a14dd` | capture only (oracle) |
| `tests/test.sh` | `cb4a41a45e4b23f4d1f1392fd68f6e47c5dbbf57` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` | capture only (runner; same digest as build-pmars `test.sh`) |

Command: `git show 2fd12b88:git-leak-recovery/<f> | sha256sum`; `git rev-parse <pin>:… / origin/HEAD:…` equal for all five.
`task.toml` (docker_image `alexgshaw/git-leak-recovery:20251031`, difficulty medium) is metadata.

Quote supply (3-25-word lines, measured): `test_outputs.py` 52 of 113; `instruction.md` 7 of 9. Ample (gate needs 8 distinct).

### 2.2 What the grader asks (static read; locations `tests/test_outputs.py`)

Five pytest functions over `/app/secret.txt` and `/app/repo`: `secret.txt` stripped text equals the literal
`secret[lost_and_found_in_git]` (`:13-16`); `git log --all --grep 'secret\['` and `git log --all -p -S 'secret['` are
empty (`:21-48`); `git log --oneline --all` contains the init message (`:53-63`); `git fsck --lost-found` lines
containing `dangling` are `cat-file -p`'d and must lack `secret[` (`:66-92`); a `find … sha256sum | sort | sha256sum`
over non-dot files equals a pinned hash (`:97-113`). The instruction asks to recover the secret, clean it so it
"cannot be found anywhere in that repo" and keep other files and commit messages (`instruction.md`). The answer is a
literal in the grader (`:16`), so "recover" is not checked by provenance.

### 2.3 Measured controls (executed; bubblewrap `--unshare-net`, `/app` and `/tests` bound, grader `test_*` called after import — pytest not needed; git 2.56.0)

Rebuild: `challenge-setup.sh` run inside the sandbox (`rc=0`); the grader's pinned checksum
`2c3d6389133b6f9fffae5d3428ec1250c3b1cab5573c716d580dc1d4fa2f4adb` (`tests/test_outputs.py:110`) is reproduced
(test 5 PASS, with `/app/repo` paths as in the grader), so **A2 holds: every expected verdict is recomputable offline** (unlike round 37's service).

```
control                                              flag  init  commits  unreachable  checksum   fails
D  empty /app (no repo)                              FAIL  FAIL  FAIL     FAIL         FAIL       5   # do-nothing on an empty tree
A  untouched initial repo (nop state)                FAIL  PASS  PASS     PASS         PASS       1   # 4 of 5 pass without any action
B  oracle solution/solve.sh                          PASS  PASS  PASS     PASS         PASS       0
C  echo "secret[lost_and_found_in_git]" > secret.txt PASS  PASS  PASS     PASS         PASS       0   # secret still in dangling commit 58c55465…:secret.txt (git grep -c → 1)
E  C + secret blob pinned by refs/blobs/keep, reflog expired, gc --prune=now
                                                     PASS  PASS  PASS     PASS         PASS       0
F  C + annotated tag whose message is the secret, reflog expired, gc --prune=now
                                                     PASS  PASS  PASS     PASS         PASS       0
G  C + reflog expire only (no gc)                    PASS  PASS  PASS     PASS         PASS       0
H  C + .git removed, fresh `git init`, one "chore: init …" commit
                                                     PASS  PASS  PASS     PASS         PASS       0
```

Reproduce: `.ufo/waves/round-38/build/R38PlanNext/receipts/git-leak-setup.sh` + `git-leak-run.py` (the runner), commands in §7.
E and F retain the secret by construction (a ref to the blob; the tag message). C's retention is observed
(`git cat-file -p 58c55465…`; `git grep -c 'secret\[' 58c55465…:secret.txt` → `…:secret.txt:1`). `git log --all -S` finds 0
because the commit is unreferenced, not because the secret is gone.

Statements an entry could make (each with a grader location): the instruction's second bullet is **unenforced** — only
`dangling` objects are inspected and `cat-file -p` of a dangling *commit* prints a tree id, not blob content
(`:77-91`); the checksum guards only non-dot files (`:101-102`); `--grep`/`-S` over `--all` cannot see unreferenced
commits (`:26-30,41`). A `pass`-at-nop is the shape TB2's own validation names — see §2.5 — so the entry claims a
**probed instance**, never a class, and **no novelty is filed**.

### 2.4 Predicate sketch, counter sketch, controls

- **Package:** `corpus/knowledge/tb2-git-leak-recovery-grader.md`, rows S117 (`tests/test_outputs.py`) + S118
  (`instruction.md`), captures under `corpus/evidence/round39/tb2-git-leak-recovery/` + `SHA256SUMS`, probe
  `plans/git_leak_probe.py`, spec `plans/pkg-spec-r39.json`, counter `plans/round39_c2_verify.py` (a copy of
  `round38_c2_verify.py` with its pin table; V1-V7 unchanged, so the round-38 rule is reused, not re-invented).
- **Probe:** ~22 cases = the table above as recipes (D, A, B, C, E, F, G, H) plus per-test mutants of the secret file
  (trailing newline, CRLF, extra text, wrong literal), reflog-only, stash-only, `refs/notes`, `refs/stash`, deleted
  README, a changed commit message, a packed-refs variant. Each case's predicted per-test verdict is written to a
  `--dry` table **before** the first run; observed verdicts come from the grader; `mismatches=0` or each `match=NO` is
  named (the round-38 V4 rule). The probe never runs the oracle image; host git/bash stand in for the task image.
- **Frozen predicate (to freeze):** `python3 plans/round39_c2_verify.py --lane .` prints `checks=7 defects=0`, then
  `PREDICATE C2 pass`, exit 0 on a clean clone of the landing tip; the receipt prints `cases=<n> observed_pass=<p>
  observed_fail=<f> mismatches=0`, second run byte-equal.
- **Do-nothing control (measured now, grader level):** untouched initial state → `fails=1` of 5 (`A` above); empty
  tree → `fails=5` (`D`). Counter-level do-nothing: the round-38 mechanism (entry, rows, captures, probe absent → red,
  exit 1) — `control-c2-nothing.txt`-style, produced at freeze, not measured here.
- **Cheapest skip-control:** the round-38 `control-c2-skip.txt` scaffold (junk entry + rows with correct anchors + a
  hand-typed receipt copied from `--dry`, `observed=predicted`) — it must stay red at V2/P10; wall ~1 minute. Add one
  probe-level skip: an all-permitting case table (`fails=0` everywhere) must print `mismatches>0` against a table
  containing the D/A rejecting cases.
- **Order-of-operations (mined from r37 and r38):** record the first probe run on a clean clone **before** any control
  runs the gate with `--rerun` (the gate's P10 executes the probe; round 38 disclosed this, `round-38-claims.md:8-15`).

### 2.5 Prior art (searched, not exhaustively)

`web_search` (this seat, two queries; snippets, not opened as primary sources): a `git-leak-recovery`-specific
blind-spot write-up exists as search-engine prose only; TB's own task-validation text says a nop agent "must score
exactly 0.0" and a per-test nop pass is flagged (cited by the search as `harbor-framework/terminal-bench`
`checks/test-tasks/fail-validate-nop` and `docs/TASK_REVIEW_AUTOMATION.md`); a third-party repair repo reports
"1 of 5 passing" at no-op and calls the do-not-modify guard correct. [INFERENCE: these URLs were not opened; a
prior-art seat must open them before the entry's wording is frozen.] Conclusion: the nop-pass class is **published**;
the git-history instance is a probe claim; coverage is the right axis, novelty is not claimed. Also not done: a check
of upstream TB2 issues for `git-leak-recovery` (round-38 C2's issue #59 re-open item names the method: `gh api`).

### 2.6 Alternates priced (measured stats from the 89-task table; `tests/test_outputs.py` / `instruction.md` quote-eligible lines)

| alternate | measured | verdict |
|---|---|---|
| `db-wal-recovery` | grader 107 lines, 7 tests, 69/12 eligible; env ships `main.db` + `main.db-wal.encrypted` (24704 B) | good offline state; tests are data-equality on `recovered.json` (class = data string again, near protein-assembly); fallback |
| `openssl-selfsigned-cert` | 160 lines, 6 tests, 90/22 | richest instruction; a certificate-attribute class; no environment files (host openssl) — second fallback |
| `fix-git` | 39 lines, 2 tests, 16 / **0** instruction eligible | instruction row has no quote supply (as R37PlanNext found; re-measured 0 of 1) |
| `sanitize-git-repo` | 71 lines, 3 tests, 36/9; env 252 B | pins an upstream commit (`d6987af0…`), offline fixture cannot reproduce — same refusal as round 36 |
| `winning-avg-corewars` | 108 lines, 43/11 | adjacent to build-pmars (same `pmars` surface); thin new class; not chosen |

## 3. Candidate B — calibration 8: mutants of the lane's own tripwire tools

### 3.1 Gap, with sources

Round 37 wave 2 found the tools added to police the lane have no standing mutant list:
`F37MutAnchorTool` (`anchor-tool-mutants-1/5`), `F37MutAttribution` (`attribution-mutants-1/4-residual-1`),
`F37NoHarmSweep` N1 (`ledger_tip` false-red), `F37AnchorRerun` M4b/M5 (row pointed at another row's real digest). Round 38
C1 addresses the **gate** (22 mutants) only; routed D3/D4 (anchor binding, `ledger-tip` detached clones) are open at
`2c5f4e0`. This is also the unfinished half of the "no instrument is mutation-tested" pattern R36 and R37 recorded.

### 3.2 Do-nothing control (executed this seat, tip `2c5f4e0`, copies of the tool, lane unedited)

(a) **Anchor tool, standing detector = the frozen before/after pair** (`3ea9a1d9` must flag S110, tip must exit 0):

```
mutant (single replacement of one source line)                 before @3ea9a1d9           tip
M0 pristine                                                    defects=5 rc=1             defects=0 rc=0
M1 drop the 64-length check (HEX64.fullmatch -> [0-9a-f]+)     defects=5 rc=1             defects=0 rc=0   SURVIVES
M2 accept uppercase hex (HEX64 -> [0-9a-fA-F]{64})             defects=5 rc=1             defects=0 rc=0   SURVIVES
M3 skip indented census rows (ROW drops ^ {0,3})               defects=5 rc=1             defects=0 rc=0   SURVIVES
M4 erratum accepted w/o committed-evidence check (drop `and t in allowed`)
                                                               defects=5 rc=1             defects=0 rc=0   SURVIVES
M5 evidence root narrowed to corpus/evidence/round36           defects=9 rc=1             defects=12 rc=1  KILLED (after-half)
```
→ **killed=1 of 5**, reproducing `F37MutAnchorTool` on the current tip (`receipts/M*_*.out`; commands §7). M1 changes
the S110 diagnostic (`class=digest-short` becomes `digest-unknown`) without changing the verdict — the pair is
verdict-shaped, so "the gate flags S110" stays true while "flags it **as** a 63-hex abbreviation" is lost.

(b) **Attribution audit** (`plans/round37_c1_attribution.py`; mutants from `F37MutAttribution/mutants/attr_m1..m4`),
run on the landed battery: all four print `ATTRIBUTED 55/55 UNATTRIBUTED=0`, rc 0 (`receipts/attr_m*_*.out`) — so
the landed-battery receipt moves on **0 of 4**; the only detector that moves is the hostile-battery receipt
(`6/55`), where `F37MutAttribution` found 1 of 4 changes. The hostile modules were not rebuilt this seat.

(c) **`ledger_tip` D4** (`F37NoHarmSweep` N1): a no-`master` source clone, `python3 plans/ledger_tip.py --source
$S/det --work $S/lt` → `R35-D3 … observed=fail agree=NO error CalledProcessError … ls-tree -r --name-only refs/heads/master
… exit status 128`, final `rows=9 closed=9 observed_pass=7 mismatches=2`, rc=1. In control mode (`--lane .`) the same
tree gives `rows=9 closed=9 observed_pass=9 mismatches=0`, rc 0. Round 38 may fix D4 (routed); if it does, this row
drops from the plan and the count below shrinks by its mutants.

### 3.3 Counter sketch

`plans/round39_c1_verify.py` (clone of `round38_c1_verify.py`'s structure): pins the three tools and the round-38
counter by digest; a frozen `MUTANTS` table `Tnn | tool | old -> new | direction | attributed signal` (old string must
occur once); detectors are **fixtures the counter owns** — anchor lane-trees (uppercase token row, indented row,
fabricated erratum, row pointed at another row's digest, S110-shaped 63-hex row asserted by `class=` not exit code),
an attribution-audit hostile battery of three minimal modules, a detached/no-`master` source clone for `ledger_tip`.
Kill = attributed (the mutant's own class line changes), silence and mirror both. Starting list: anchor M1-M4 (4) +
audit m1-m3 surviving (3) + `ledger_tip` N1 (1) + the D3 row-binding hole (1) = **9**; freeze may add mirrors
(a false-defect mutant per tool). Predicate (to freeze): `PINS total=<k> mismatched=0`, `FIXTURES n=<n> wrong=0`,
`MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`. The tools are not edited, except
that D3/D4 repairs, if the planner wants them landed, must be a separately frozen tool change *before* the counter
freezes (otherwise the mutant "old" strings would target unfixed code); otherwise the repairs stay routed.

- **Do-nothing control (measured):** §3.2 — 1/5, 0/4 on the landed side, and `observed_pass=7 mismatches=2`.
- **Cheapest skip-control:** run the new counter with an empty `battery39`/fixture dir → must print `killed=0
  survived=9`; and the round-38 hostile pattern — a counter whose detector only compares exit codes (the present pair)
  must print `survived>=4`; minutes each, and no gate run is needed (no `--rerun`).
- **Limits:** a token-heuristic side-channel scan (r38) still leaves non-author code review in admission; the
  attribution-audit mutants kill only on the hostile battery, which round 39 would have to rebuild from
  `.ufo/waves/round-37/build/R37CritC1Battery/`.

## 4. Candidate C — novelty 7 (priced, not filed)

"Initial-state pass census": per-test pass counts of every TB2 grader on the untouched initial state.
Pilot (executed): **89 graders, 210 tests** in a sandbox with an **empty** `/app`: `PASSED=6 FAILED/ERROR=204`
(four tasks have a passing test: `mcmc-sampling-stan` 2, `rstan-to-pystan` 1, `schemelike-metacircular-eval` 1,
`sqlite-with-gcov` 2; `receipts/empty-app-census-summary.txt`). With a **COPY-lines-only** reconstruction of `/app`
(Dockerfile `RUN` steps skipped, so an under-approximation of the real state): `18` passes across `10` of 89 tasks
(`receipts/initial-state-pilot-summary.txt`). The rough static screen (Dockerfiles with no non-apt/pip download) says 55
tasks ship environment files, but the passes are partly host leakage (`sqlite3` on the host `PATH`, `test_sqlite_in_path`) and by-design guards
(`test_protected_files_not_modified`). **Why not filed:** TB2's validation contract already requires nop = 0.0
(§2.5, prior art published) and the reconstruction needs the task images to be valid; no novelty claim survives. As a
coverage source it is a rider on candidate A (the `git-leak-recovery` `A` row is the pilot's only fully-rebuilt case).

## 5. DRAFT — `### Planned (round 39)` (paste-ready for `SCORECARD.md`)

```markdown
### Planned (round 39)

- **Coverage/novelty (7, tied lowest; coverage still capped by the open L0 question `kengaku | round-33`, so judged
  on its counter, no score move claimed; novelty not filed — nop-pass is published TB validation text, prior-art seat
  must open the cited pages):** a fifth Terminal-Bench 2.0 grader of a class the lane has not read, **repository history
  state**: `git-leak-recovery` @ `2fd12b88` (rows S117 `tests/test_outputs.py`, S118 `instruction.md`, ids re-derived at
  freeze; `challenge-setup.sh`, `solve.sh`, `test.sh` captured, not rows). Measured before writing the entry, offline in
  a `--unshare-net` sandbox with the task's own setup script rebuilding the graded repo (expected checksum
  recomputed): the untouched repo passes 4 of 5 tests, an empty tree fails 5, the oracle passes 5, and a single
  `echo "secret[lost_and_found_in_git]" > /app/secret.txt` passes 5 while the secret is still in a dangling commit;
  a ref-pinned blob, an annotated tag carrying the secret, a reflog-only cleanup and a history rebuilt from scratch all
  pass 5/5. Package: entry `corpus/knowledge/tb2-git-leak-recovery-grader.md`, captures
  `corpus/evidence/round39/tb2-git-leak-recovery/` + `SHA256SUMS`, probe `plans/git_leak_probe.py` with a case table
  frozen before its first recorded run (first run recorded before any `--rerun` control), counter
  `plans/round39_c2_verify.py` = the round-38 V1-V7 over `plans/pkg-spec-r39.json` with its inputs pinned. Frozen predicate:
  `python3 plans/round39_c2_verify.py --lane .` prints `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0; receipt
  `cases=<n> observed_pass=<p> observed_fail=<f> mismatches=0`, byte-equal on a second run. Before / do-nothing: grader
  level `fails=1` of 5 on the untouched repo and `fails=5` on an empty tree (measured round 38 wave 1,
  `.ufo/waves/round-38/build/R38PlanNext.md` §2.3); counter level entry/rows/captures/probe absent → red, exit 1.
  Skip-control: junk entry with correct anchors plus a hand-typed `--dry` receipt stays red (V2/P10); an
  all-permitting case table must print `mismatches>0`. Fallbacks: `db-wal-recovery`, `openssl-selfsigned-cert`;
  `fix-git` loses (zero quote-eligible instruction lines), `sanitize-git-repo` refused (pinned upstream commit).
- **Calibration (8):** mutation-test the lane's own tripwire tools, which round 37 wave 2 found unguarded and round 38
  C1 (gate only) does not touch. Measured at `2c5f4e0`: the standing before/after pair kills 1 of 5 anchor-tool mutants
  (uppercase hex, indented rows, unverified erratum evidence and a dropped 64-length check all survive), the
  landed-battery audit run is unchanged by 4 of 4 attribution-audit mutants, and `plans/ledger_tip.py` from a
  source clone without `refs/heads/master` prints `rows=9 closed=9 observed_pass=7 mismatches=2` (exit 1). Plan:
  `plans/round39_c1_verify.py` owns its fixtures (anchor lane-trees, a three-module hostile audit battery, a
  detached source clone) and a frozen mutant table, attributed kills, silence and mirror. Predicate (to freeze):
  `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`; the tools are not edited
  unless a separately frozen repair precedes the counter. Before / do-nothing: the measured 1/5, 0/4 and `mismatches=2`;
  skip-control: an empty fixture dir must print `killed=0 survived=9` and an exit-code-only detector `survived>=4`.
  Kill rule as round 38: a survivor, invalid mutant or null detection means not admitted; an equivalent mutant is a
  limit, never removed.
```

## 6. Limits

- A's per-test grid is a pilot: eight recipes were run once; the 22-case probe, its dry table and the second-run
  byte-equality are freeze work. Host git 2.56.0 and host bash stand in for the task image's git/dash.
- The E and F rows are constructed retention (a ref to the blob; a tag message), not an independent scan of `.git` for
  the literal; C's retention is observed. The entry must state which.
- The empty-`/app` census ran with a host-bound `/usr` (host `sqlite3`, `python3`); counts are leakage-exposed, not an
  image measurement. The initial-state pilot skips every Dockerfile `RUN` step.
- B's count (9) is the starting list from §3.3, not a freeze; the attribution mutants kill only on a hostile battery
  that this seat did not rebuild. D4 may be repaired by round 38, which removes the `ledger_tip` row.
- Prior art was searched through `web_search` snippets only; no page was opened as a primary source.
- `ledger_tip.py --source` ran on a no-`master` clone I made (`git branch -D master` in a scratch clone), the lane's own
  detached state was not used; the lane was never written.

## 7. Evidence ledger

| claim | command | output |
|---|---|---|
| tip and clean baseline | `git -C $S/lane rev-parse HEAD`; lane `git status --short` | `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e`; untracked `.ufo/waves/round-38/*` only |
| TB2 pin = origin/HEAD, task blobs equal | `git rev-parse origin/HEAD`; `git rev-parse <pin>:git-leak-recovery/<f>` vs `origin/HEAD:…` | `2fd12b88…`; five equal pairs (§2.1) |
| sha256 of the five task files | `git show <pin>:git-leak-recovery/<f> \| sha256sum` | §2.1 table |
| quote supply | python line scan 3-25 words | `52 of 113`; `7 of 9` |
| rebuilt repo, oracle, controls A-D | `bwrap … bash /dev/stdin < setup.sh`, `… python3 /tests/run.py`, `… < solve.sh` | §2.3 (`fails=1`, `0`, `0`, `5`) |
| controls E-H | same, extra recipe each | `fails=0` x4 (§2.3); H leaves `bd0d475 chore: init e665d1a2-…` |
| secret still in repo after C | `git cat-file -p 58c55465…`; `git grep -c 'secret\[' 58c55465…` | commit shows `tree aa7dfd0c…`, `…:secret.txt:1` |
| empty-/app census, 89 graders | `bwrap … python -m pytest /tests/test_outputs.py -rA` (venv pytest 8.4.1) | `PASSED=6 FAILED/ERROR=204` |
| COPY-only initial-state pilot | same, `/app` from Dockerfile `COPY` lines | `passed 18 failed 202`, 10 tasks with a pass |
| anchor mutants | `cp mut/Mk.py $S/<lane|lane36>/plans/_mut.py; python3 plans/_mut.py --lane .` | §3.2 (a) table; `receipts/M*_*.out` |
| attribution mutants | `python3 <mutant> --lane . --work $S/awN` x4 | `ATTRIBUTED 55/55 UNATTRIBUTED=0` x4 |
| ledger_tip no-`master` | `python3 plans/ledger_tip.py --source $S/det --work $S/lt` | `rows=9 closed=9 observed_pass=7 mismatches=2`, rc=1; `--lane .` → `observed_pass=9 mismatches=0` |
| next free source id | `grep -o '^| S[0-9]* ' corpus/SOURCES.md \| tail -2` | `S113 S114` (S115/S116 land with round 38) |

Tools: `uv venv` + `uv pip install pytest==8.4.1` into the scratch venv (official PyPI via `uv`, for the grader census only;
nothing installed on the host). No pacman use. `jq`/`gh` not needed.

## 8. Out of scope

No lane file, claim, counter, probe, spec, capture or corpus path written; no `git add/commit` in the lane; no subagent;
no scratch outside `/fast/scratch/hyaku/kengaku-r38/R38PlanNext/`; the source repo `shokuknow` untouched.

## 9. Scratch

Receipts copied to `.ufo/waves/round-38/build/R38PlanNext/receipts/`, then `rm -rf /fast/scratch/hyaku/kengaku-r38/R38PlanNext`.

VERDICT: plan39-drafted
