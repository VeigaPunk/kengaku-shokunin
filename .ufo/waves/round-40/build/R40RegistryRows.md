# R40RegistryRows — SKILL.md gate/probe rows for round-39 closure R1/R2 and the five round-40 instruments

Seat: scribe, kengaku round 40 wave 1. Lane clone measured: `/fast/scratch/hyaku/kengaku-r40/R40RegistryRows/lane`
(= `git clone --shared` of the lane, `rev-parse HEAD` = `3077adbc7145726519f60f01426a5d03381ad444`, which is the
round-40 wave-1 dispatch commit on top of freeze `bbb1095` and first recorded probe run `055748f`). Every command
below was run from that clone root with `--lane .`; the lane itself was never written.

Registry column shape copied verbatim from `SKILL.md:562` (8 columns): `| name | kind | entry | verdict map |
self-test | pinned values | write scope | owner |`. The table currently holds **26** rows
(`awk '/^## Gate\/probe registry/{f=1;next} /^## /{f=0} f&&/^\| `/' SKILL.md | wc -l` → `26`) and none of the five
tools below is registered (`grep -c <tool> SKILL.md` → `order_check 0`, `round39_c1_audit 0`,
`round40_c1_verify 0`, `round40_c2_verify 0`, `db_wal_probe 0`).

Nothing frozen was edited. No installs were needed (`python3` 3.14, `/usr/bin/bwrap`, `/usr/bin/git` already
present; no pacman transaction).

## 1. Drafted rows (drop into `SKILL.md` §Gate/probe registry after the `round39-c2` row)

Measured receipt lines for each row are in §2; `rc` values there are the exits this seat observed, not source
reading.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `order-check` | gate | `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt` (lane root; all three flags are required, `plans/order_check.py:143-145`) — Q30's order-of-operations gate | `0` order holds: `ORDER ok no claims file committed at or before the receipt shows the frozen probe executed`, then `ORDER RESULT PASS` (`plans/order_check.py:204-206`) · `1` order broken: one `ORDER FAIL <clause> …` line per broken clause (`freeze-contains-receipt`, `receipt-before-claims`), one `ORDER HIT <path>@<commit>:<n> kind=<kind> …` line per claims blob that shows the probe executed, then `ORDER FAIL <clauses> hits=<n>` and `ORDER RESULT FAIL` (`plans/order_check.py:184-202`) · `2` could-not-evaluate: `ORDER ERROR <reason>` on stderr then `ORDER RESULT ERROR` — not a git work tree, claims or receipt never committed in HEAD, claims file not named `round-NN-claims.md`, path outside the lane, mid-scan `git cat-file` failure, argparse (`plans/order_check.py:151-175`, handler `:207-210`) | no `--selftest` in the script; falsifiers are external — `plans/round40_c1_verify.py` mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), each witnessed pre-freeze (`.ufo/waves/round-40/claims/witness/`), and the measured controls `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `--claims plans/round-99-claims.md` → `ORDER ERROR claims not committed in HEAD`, exit 2 | reads committed history only and pins nothing itself; the population is the claims file and the receipt named per run; the round-40 pair is `freeze bbb1095`, `receipt_commit 055748f`, `claims_dir .ufo/waves/round-40/claims/` | none — `rev-parse`, `log`, `rev-list`, `ls-tree`, `cat-file`, `merge-base --is-ancestor` only; writes nothing, imports no probe/gate/counter, never runs the probe it polices | kengaku |
| `round39-c1-audit` | gate | `python3 plans/round39_c1_audit.py --lane .` (lane root; `--battery r38` the do-nothing control; `--battery-dir DIR` and `--only M01,M02` development selectors, which print `PREDICATE C1 n/a`; `--work DIR` scratch parent, must already exist — see limits) | `0` frozen predicate holds plus the audit's extra evidence: `PINS total=26 mismatched=0`, `BATTERY … wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PINS final … mismatched=0`, `AUDIT nondeterministic_kills=0`, `AUDIT C1 clean`, `PREDICATE C1 pass` (`plans/round39_c1_audit.py:418-428`) · `1` any survivor, invalid mutant, null detection, wrong/renamed/disagree/sidechannel count, a post-run pin mismatch (`PINS final`), a nondeterministic kill, `AUDIT C1 dirty`, `PREDICATE C1 fail` (`:420-428`); also a development subset whose killed set is not clean (`:423-425`) · `2` an unpinned `plans/battery37`/`battery38` module present (`AUDIT unpinned battery module present; refusing to import it`, `:286-287`), a child build/parse failure (`:303`, `:315`, `:328`, `:333`), or argparse — **`--work` absent is not `2`**: `tempfile.mkdtemp(dir=…)` raises `FileNotFoundError` at `:293` and the process exits 1, which reads as a verdict failure | no `--selftest`; the audit *is* the soundness self-test of the round-39 counter and its controls are external — `--only M01` (dev, `PREDICATE C1 n/a`) and `--battery r38` (do-nothing); measured full run at the lane tip is green (§2.5), 55 s | 26 digests in its own `PINS` (gate, round-36 and round-37 counters, round-35 spec, round-37 attribution audit, nine `battery37` modules, twelve `battery38` modules), re-hashed after the run as `PINS final`; the `battery37`/`battery38` directories must hold exactly the pinned module names | scratch under `--work`; gate copies and fixture dirs are counter-owned and removed on exit; writes no lane byte | kengaku |
| `round40-c1-mutants` | gate | `python3 plans/round40_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only A01,L05` development selectors print `PREDICATE C1 n/a`; `--work DIR` created if absent; `--jobs N` parallel tool runs, default 8) | `0` frozen predicate holds: `PINS total=3 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass` (`plans/round40_c1_verify.py:458,557-570`) · `1` any survivor (printed with `exhibits=<directions>`), invalid mutant, null detection, `wrong>0`, `tampered>0`, `sidechannel>0`, a pin mismatch before or after the run, or `PREDICATE C1 fail` (`:557-570`) · `2` setup/usage: `/usr/bin/bwrap` not executable (`:460-461`), lane clone failure (`:471`), a battery build that raises (`:478`), duplicate fixture id (`:482`), argparse | itself plus the freeze controls `.ufo/waves/round-40/claims/control-c1-nothing.txt` (no `plans/battery40`: `killed=0 survived=21`, exit 1), `control-c1-tool-edited.txt` (`PINS mismatched=1`, the 11 anchor mutants `invalid`), `control-c1-hostile-daemon.txt` (a detached child that rewrites its fixture is killed with the build pid namespace, nothing killed); dev selector `--only A01` prints `PREDICATE C1 n/a` | the three tool digests in `PINS` (anchor `11bb2cad…`, ledger `853bcb2a…`, order `948d5e1d…`, re-hashed as `PINS-AFTER`); the 21 frozen mutant ids and their `old -> new` strings live in the counter's `MUTANTS` | fixtures are counter-owned dirs under `--work`; battery modules are built in `bwrap --unshare-pid` children and every tool run is sandboxed with the variant bound read-only at one fixed path; writes no lane byte | kengaku |
| `round40-c2` | gate | `python3 plans/round40_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, **must already exist** — the counter does not create it) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` (`plans/round40_c2_verify.py:278-280`) · `1` any `Vn DEFECT <note>` — including a check that raises, which prints `error <Class>: …` and is a defect, never a pass (`:271-277`) · `2` argparse usage only: the script has no setup exit (`:262-284`), and an absent `--work` is a `FileNotFoundError` traceback under exit 1 (measured, §2.3) | itself; the freeze control `.ufo/waves/round-40/claims/control-c2-nothing.txt`; measured at lane HEAD `3077adbc` the row is **red** — `checks=7 defects=4` (V2, V3, V4, V7), exit 1 — because S119/S120 index rows, the entry and the requirement map are not landed yet (§2.3) | `plans/pkg-spec-r40.json` `4af78f4f…`, `plans/pkg_gate.py` `ea638822…`, `plans/db_wal_probe.py` `69af65df…`, dry table `corpus/evidence/round40/db-wal-dry-cases-freeze.txt` `688f3475…`, and the eight captures in `CAPTURES` (`test_outputs.py 88dc5c2a…`, `instruction.md 5a203751…`, `main.db 68cb288e…`, `main.db-wal.encrypted 68753bdc…`, `solve.sh ed8530c9…`, `task.toml 1cdc2c61…`, `test.sh 4770437e…`, `Dockerfile 63a26053…`) | scratch under `--work` only; the gate it dispatches writes nothing in the lane | kengaku |
| `db-wal-probe` | probe | `python3 plans/db_wal_probe.py --lane .` (`--dry` prints the 28 frozen cases, `violates=` tags and predictions with no sandbox; `--stage-check` builds each case's end state and prints only stage exit codes, the grader module is never imported; `--work DIR` scratch parent, created if absent) | `0` every case yielded seven test verdicts twice and both summary lines printed — **prediction mismatches are on the summary line, never in the exit code** (`cases=28 … mismatches=N` still exits 0, `plans/db_wal_probe.py:378-380`) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero (`stagecheck cases=<n> failed=<k>`, `:349`) · `2` setup: duplicate case id, unknown tag or malformed prediction (`:314-315`); a capture missing or not at its pinned digest (`:327-328`); `/usr/bin/bwrap`, `sqlite3`, `xxd` or `python3` not executable (`:331-332`); `--work` cannot be created (`:337-338`); a case that did not yield seven verdicts twice (`:362-364`) | `python3 plans/round40_c2_verify.py --lane .` V5 (probe at its freeze digest and `--dry` byte-equal to the frozen table) and V2's gate `P10` (a fresh run byte-compared to the receipt — measured `gate: P10 ok probe_rerun=byte-equal bytes=8257`, §2.3); the probe's own `--dry`/`--stage-check` modes are not a self-test of its verdicts | `PINS` in the probe: the eight captures (`test_outputs.py` `88dc5c2a…`, `solve.sh` `ed8530c9…` and six more, each checked before any case); the frozen dry table and the receipt digest are pinned by `plans/round40_c2_verify.py` (V4, V5) | scratch under `--work`/`$TMPDIR` only; per case a private `/app`, private network/pid/ipc namespaces, `/usr` and `/etc` read-only; writes no lane byte | kengaku |

Addendum text for the q30 scope and the two operability limits (proposed, one paragraph, in the style of the
round-37/38/39 addenda):

> Round-40 registry addendum: `order-check` (`plans/order_check.py`) is Q30's gate — it reads commits only and is
> **documentation, not enforcement**: nothing in the lane invokes it yet (round-39 routed `F39CritQ30`), so the row
> records a checkable rule, not a wired one; measured on the round-40 pair at `3077adbc` it prints `ORDER RESULT
> PASS` and exits 0. `round39-c1-audit` is a second counter over the same frozen battery as `round39-c1-mutants`,
> not a replacement: it adds `AUDIT C1 clean|dirty` on top of the frozen numbers. `round40-c1-mutants` and
> `db-wal-probe` are the round-40 pair; only the probe's receipt is green today (`cases=28 observed_pass=8
> observed_fail=20 mismatches=0`, `regrade differ=0`, reproduced byte-equal by this seat), while `round40-c2` is red
> (`defects=4`: V2 gate rejects the incomplete package, V3 the two unlanded registry rows, V4/V7 the missing entry).
> Two `--work` limits are declared rather than fixed: `round40-c2`, `round39-c2` and `round39-c1-audit` do not create
> `--work` and crash with `FileNotFoundError` under exit 1 when it is absent (the §Gate standard's undeclared code
> reads as could-not-evaluate; exit 1 reads as a verdict failure), and `round40-c1-mutants` treats a mistyped
> `--battery-dir` as zero fixtures (`BATTERY fixtures=0`) and exits 1 instead of 2.

## 2. Measured receipts (one run per command written above)

### 2.1 `order-check` — exit 0

```
$ cd <clone> && python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt
ORDER claims=plans/round-40-claims.md round=40 freeze=bbb109505670192035ef63d7c8b37733e99fa1a3
ORDER receipt=corpus/evidence/round40/db-wal-probe.txt receipt_commit=055748f78a3335434f2a4070bb3fb1cf8d0eba1f claims_dir=.ufo/waves/round-40/claims/
ORDER scanned commits=1 file_entries=12 distinct_blobs=12
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
rc=0
```

Exit 1 (control, round-39 receipt):

```
$ python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt
ORDER FAIL freeze-contains-receipt bbb1095… already has corpus/evidence/round39/git-leak-probe.txt
ORDER FAIL receipt-before-claims 6a1eb5e1… is an ancestor of bbb1095…
ORDER scanned commits=0 file_entries=0 distinct_blobs=0
ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0
ORDER RESULT FAIL
rc=1
```

Exit 2:

```
$ python3 plans/order_check.py --lane . --claims plans/round-99-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt
ORDER ERROR claims not committed in HEAD: plans/round-99-claims.md
ORDER RESULT ERROR
rc=2
```

### 2.2 `round40-c1-mutants` — exit 1 (do-nothing control; `plans/battery40` does not exist at this tip)

```
$ python3 plans/round40_c1_verify.py --lane . --work <scratch>/w1
PINS total=3 mismatched=0
… MUTANT A01…O14 … SURVIVED exhibits=none …
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=21 killed=0 survived=21 invalid=0 null_detected=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
rc=1
```
(21 `MUTANT … SURVIVED` lines; full text in `R40RegistryRows/c1-control.out`.)

Dev-selector and battery-dir limits, measured in the same clone:

```
$ python3 plans/round40_c1_verify.py --lane . --work … --only A01
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0   /   PREDICATE C1 n/a (non-default battery or mutant subset)   rc=1
$ python3 plans/round40_c1_verify.py --lane . --work … --battery-dir <absent>
MUTANTS total=21 killed=0 survived=21 …            PREDICATE C1 n/a   rc=1     # no SETUP line: absent dir == zero fixtures
```
So the `n/a` exit is 0 only when the subset is clean; the row must not read `n/a` as success.

### 2.3 `round40-c2` — red at the tip, and the `--work` crash

```
$ python3 plans/round40_c2_verify.py --lane . --work <existing dir>
V1 ok listed=8 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 DEFECT no '## Located quotes' section
    gate: P4 DEFECT no parsed quote
    gate: P5 ok manifest_entries=8 bad=0 first=0
    gate: P6 DEFECT rows=2 bad=2 first=S119: rows=0
    gate: P7 DEFECT entry unreadable
    gate: P8 DEFECT index_rows=46 knowledge_files=46 bad=2 first=index rows for knowledge/tb2-db-wal-recovery-grader.md=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8257
    gate: defects=5
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=2 bad=['S119:row', 'S120:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
checks=7 defects=4
PREDICATE C2 fail
rc=1
```

Absent `--work` (the counter never creates it, `plans/round40_c2_verify.py:266`):

```
$ python3 plans/round40_c2_verify.py --lane . --work <absent dir>
FileNotFoundError: [Errno 2] No such file or directory: '…/absent/k40-c2-724dstph'
rc=1        # traceback, no PREDICATE line — exit 1 is also the defect exit
```

Bad flag → `rc=2` (`round40_c2_verify.py: error: unrecognized arguments: --bogus`), the only `2` in this tool.

### 2.4 `db-wal-probe` — 0 / 0 / 0, and byte-equal to the committed receipt

```
$ python3 plans/db_wal_probe.py --lane . --work <absent dir>          # creates the dir
regrade cases=28 differ=0
cases=28 observed_pass=8 observed_fail=20 mismatches=0
rc=0
$ cmp <that output> corpus/evidence/round40/db-wal-probe.txt && echo BYTE-EQUAL
BYTE-EQUAL
$ python3 plans/db_wal_probe.py --lane . --dry
cases=28 predicted_pass=8 predicted_fail=20
rc=0
$ python3 plans/db_wal_probe.py --lane . --work … --stage-check
stagecheck cases=28 failed=0
rc=0        # 5.03 s
```

### 2.5 `round39-c1-audit` — exit 0, and the `--work` crash

```
$ python3 plans/round39_c1_audit.py --lane .
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=0
AUDIT nondeterministic_kills=0
AUDIT C1 clean
PREDICATE C1 pass
rc=0        # 55.18 s wall
$ python3 plans/round39_c1_audit.py --lane . --only M01 --work <existing dir>
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
AUDIT C1 clean
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0        # 32.58 s — the 90-fixture in-process build happens regardless of --only
$ python3 plans/round39_c1_audit.py --lane . --work <absent dir>
FileNotFoundError: [Errno 2] … /absent-audit/k39-c1a-mtikmvou
rc=1        # traceback before any verdict; not a declared code
```

## 3. R2 — `plans/git_leak_probe.py --work <absent dir>`: **PINNED**, not editable

Reproduced the defect (D3) on the unmodified clone: `--work` absent → `FileNotFoundError` from
`tempfile.mkdtemp` (`plans/git_leak_probe.py:232`, `:258`), **rc=1, no `SETUP` line** — an undeclared code for a
non-`--stage-check` run, since the row maps `1` to `--stage-check` only. Full stderr in
`R40RegistryRows/glp-absent.err`; with the dir created the same command is `rc=0`, `cases=25 predicted_pass=13
predicted_fail=12` (`--dry`, 3 s).

Then the pin claim, tested as instructed (fresh `git clone --shared`, one appended line
`# r40 registry-row draft: one-line edit to test the pin` at the end of `plans/git_leak_probe.py`,
digest `4961a50f… → 753a134c…`, nothing else changed):

| run | command | result |
|---|---|---|
| baseline, unmodified clone | `python3 plans/round39_c2_verify.py --lane . --work <existing>` | `V1..V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass`, **rc=0** (`R40RegistryRows/c2r39-clean.out`) |
| one-line edit | same | `V2 DEFECT spec=frozen gate=frozen gate_exit=1`, `V5 DEFECT probe or dry table not at freeze digest`, `checks=7 defects=2`, `PREDICATE C2 fail`, **rc=1** (`c2r39-edited.out`) |
| one-line edit, gate directly | `python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r39.json --rerun` | `P1 DEFECT pinned=2 mismatched=['plans/git_leak_probe.py']`, `P2 DEFECT receipt_sha256=d7f3a465…`, `defects=2`, **rc=1** (`gate-edited.out`) |

So the edit is caught twice over and reds the round-39 C2 counter: `plans/round39_c2_verify.py:62`
`PROBE_SHA256 = "4961a50f…"` and `plans/pkg-spec-r39.json` `frozen_instruments["plans/git_leak_probe.py"] =
"4961a50f…"` (the gate's P1 re-hashes it from the spec). Fixing the probe therefore requires re-freezing the
round-39 counter (V5 digest), the round-39 spec's `frozen_instruments`, and re-deriving the round-39 receipt; that is
not this round's work and the probe is not this round's surface. **Registry text, not code:**

> Corrected `git-leak-probe` row text — entry cell: `python3 plans/git_leak_probe.py --lane .` (`--dry` prints the 25
> frozen cases, `violates=` tags and predictions with no sandbox; `--stage-check` builds each case's repository state
> and prints only stage exit codes, the grader module never imported; `--work DIR` scratch parent, **which must
> already exist — the probe does not create it (`plans/git_leak_probe.py:258`); an absent `--work` is a
> `FileNotFoundError` traceback and exit 1, a code this row does not otherwise use**). Verdict-map cell: append
> `— exit 1 also covers an absent --work (traceback, no SETUP line): create the directory first`. Pinned-values
> cell: unchanged (`PROBE_SHA256 4961a50f…` in `plans/round39_c2_verify.py:62` + `plans/pkg-spec-r39.json
> frozen_instruments`), plus a note that the file is **not editable without re-reding the round-39 C2 counter
> (V2+V5) and the gate's P1**.

The same `--work` declaration is needed verbatim on the new `round40-c2` and `round39-c1-audit` rows (§1) and
already exists on `round39-c2` (`plans/round39_c2_verify.py:264`, `FileNotFoundError`, measured rc=1), which is
why this seat declares it per row instead of asking for one shared fix this round.

## 4. Findings, limits, out of scope

Findings (all measured, all outside my write scope — lane file edits belong to L1):

1. **The R2 class is now a pattern, not a one-off**: four tools take `--work` and only one creates it —
   `db_wal_probe` (`:335`, `:339`) and `round40_c1_verify` (`:463`) do; `git_leak_probe` (`:258`),
   `round39_c2_verify` (`:264`), `round40_c2_verify` (`:266`) and `round39_c1_audit` (`:293`) do not, and all four
   exit **1** with a traceback. Under the §Gate standard an undeclared nonzero reads as could-not-evaluate, so exit 1
   makes a missing scratch dir indistinguishable from a real defect verdict — for `round40_c2` that is exactly the
   C2 predicate's red.
2. **`round40_c1_verify --battery-dir <absent>`** prints `BATTERY fixtures=0` and exits 1, never `SETUP`/2: a typo'd
   battery path is indistinguishable from the do-nothing control. The row declares it; a wave-2 fix would be a
   `SETUP battery dir absent` → 2.
3. **`round40_c2` is red at `3077adbc`** (`defects=4`) and the reds are exactly the unlanded package parts (S119/S120
   rows, entry, requirement map) — the row must record a red state, not a green one, exactly as the `git-leak-probe`
   and `round37-c2` rows did at their freezes.
4. **`round40-c1-mutants` is at its do-nothing control** (`fixtures=0`, `killed=0 survived=21`, rc=1); its green
   (`fixtures>=21 killed=21`) is wave-1 executors' to earn. The row claims no green.
5. **`order-check` is green and unwired**: `ORDER RESULT PASS`, rc=0 over the round-40 pair; nothing in the lane runs
   it (round-39 `F39CritQ30`), so its row says "documentation, not enforcement".
6. **`db-wal-probe` is byte-reproducible here**: my scratch run of the entry command is `cmp`-equal to the committed
   `corpus/evidence/round40/db-wal-probe.txt` (8257 bytes), and V2's gate `P10` independently re-ran it
   `byte-equal bytes=8257`. The probe creates an absent `--work`, unlike its round-39 sibling — the asymmetry is now
   documented rather than fixed.
7. **No gate pins the gate/probe registry row set**: `plans/registry_check.py:55` reads `corpus/SOURCES.md` (the
   source registry, population `S038…S060` + 35 knowledge paths), and `plans/state_check.py` P3 anchors SKILL.md
   headings, not rows — so appending five rows changes no pinned population. L1 should still re-run
   `python3 plans/state_check.py --summary` and `python3 plans/registry_check.py --summary` after integrating.

Limits: the row verdict maps are read from source and each code is exercised where the current tip allows; the
`round40-c1-mutants` exit 0 path and the `round39-c1-audit` exit 2 path could not be exercised without a green
`plans/battery40` and without planting an unpinned battery module (both out of my write scope) and are marked as
source-only above. `git_leak_probe` full-run exit 0 was not re-run by this seat (only `--dry`, and the gate's P10
already re-runs it byte-equal); round-39's spot-check records the full run. Everything above ran unprivileged on this
host (python3 3.14, git 2.56, bubblewrap present); no pacman transaction was attempted or needed.

Out of scope / untouched: no lane file (`SKILL.md`, `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`,
`PROVINCE.md`, `SHONEN.md`), no jj state, no fleet root, no source repo. Scratch `/fast/scratch/hyaku/kengaku-r40/
R40RegistryRows` is removed at exit (`trap`); the receipts copied into this report dir are the only residue.

Artifacts (this report dir): `R40RegistryRows/c1-control.out`, `c2.out`, `c2r39-clean.out`, `c2r39-edited.out`,
`gate-edited.out`, `audit.out`, `dbw-full.out`, `glp-absent.err`.

VERDICT: registry-rows-6-r2-pinned
