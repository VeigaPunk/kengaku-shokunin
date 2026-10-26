# F37NoHarmSweep — no-harm sweep at integration tip `357deceb` (round 37, wave 2)

Seat: executor (leaf), measure-only. No lane file was edited; nothing was committed; the lane's Git index and
jj state were not touched. Every number below came from one clean clone of the assigned tip, executed with
`cwd` = clone root. Report dir: `.ufo/waves/round-37/falsify/F37NoHarmSweep/`.

## 0. Setup (reproducible)

- Scratch: `S=/fast/scratch/hyaku/kengaku-r37/F37NoHarmSweep`; `export TMPDIR="$S"`.
- Clone: `git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/fx/lane"` then
  `git -C "$D/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`.
  Verified before any run: `git rev-parse --show-toplevel` = `$S/fx/lane`, `HEAD` =
  `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`, tree `bc1532d0707153e7d568b5cad0b74c7b3690d134`,
  `git status --porcelain` = **0 lines**; and **0 lines** again after the whole sweep.
- Host: `python3 -V` → `Python 3.14.8`; `ls /usr/bin/bwrap` → present (service-class probe runnable).
- Freeze identity at the measured tree (`sha256sum plans/pkg_gate.py plans/git_webserver_probe.py
  plans/round37_c1_verify.py plans/round37_c2_verify.py`): `ea63882240e67e99…766edd41`,
  `63cb75cfcd1c224a…d3a5eedf`, `dbc9f7199381f5bb…9173413cc`, `b8cba11a369298f2…954b9168` — all four equal
  the digests named in `plans/round-37-claims.md` and in `.ufo/waves/round-37/integrate/measure-final.txt`.
- Runner: `receipts/run.sh` + `receipts/cmds.tsv` / `receipts/cmdsB.tsv`, 6-way parallel for the fast set,
  5-way for the slow set; per-command log, `receipts/summary.tsv` (label, exit, seconds, last line).
  Wall: fast set 3.89 s (24 commands), slow set 81.67 s (5 commands, bounded by C1 at 81.7 s).
- No tool was installed or upgraded (Python, bwrap, and the shell tools were already present); nothing
  touched pacman, and no host service was restarted.

## 1. Result

**29/30 entries green as declared at `357deceb`; 1 new red.**

- The wave-1 baseline (`build/R37TipSweep.md` §1, 25 green rows) is preserved **25/25**: every one of those
  commands reproduces its wave-1 exit code and its declared verdict line, with the expected growth deltas
  (§6.1).
- Of the five registry rows that postdate that baseline (`git-webserver-probe`, `round37-c1-mutants`,
  `round37-c2`, `anchor-digest-check`, `ledger-tip`), four are green and **`ledger-tip` is red** in the clone
  shape this fleet mandates (§3).
- The two wave-1 reds flip green exactly as the freeze required: C1 `killed=55 survived=0`, C2
  `checks=7 defects=0`.

## 2. Table (30 comparable entries; every path relative to the clone root)

| # | entry / registry row | command (abridged) | exit | key output line | vs wave 1 |
|---|---|---|---|---|---|
| 1 | hermetic-grader | `python3 grader.py` | 0 | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS` | same |
| 2 | hermetic-grader | `grader.py --selftest` | 0 | `[selftest] ALL PASS` (S0–S7) | same |
| 3 | coverage-census | `corpus/evidence/round13-coverage/coverage_census.py` | 0 | knowledge `indexed=44`, evidence `23`, lessons `33`; `dangling=0`, `duplicate_rows=0` | same (43→44 knowledge) |
| 4 | interval-reverdict | `plans/attrib_calibration.py --summary` | 0 | `TOTAL files=9 … scored_trials=92 correct=92 incorrect=0 … mismatches=0` | same |
| 5 | interval-reverdict | `attrib_calibration.py --selftest` | 0 | `selftest: 18 checks, 0 failed` | same |
| 6 | state-assertion-check | `plans/state_check.py --summary` | 0 | `assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`, `VERDICT: PASS` | same |
| 7 | state-assertion-check | `state_check.py --selftest` | 0 | `[selftest] ALL PASS` | same |
| 8 | grader-perturb | `plans/grader_perturb.py --summary` | 0 | `TOTAL population=1964 excluded=0 audited_verdicts=15168 policy_checks=909` | same |
| 9 | grader-perturb | `grader_perturb.py --selftest` | 0 | `SELFTEST TOTAL families=10 branch_cases=10 failed=0` | same |
| 10 | gate-timing | `--lesson corpus/lessons/round-26.md --commit b571944` | 0 | `admissions=1 passed=1 failed=0 second-seat-reports=53` | same |
| 11 | gate-timing | same, `--commit HEAD` | 0 | identical summary with `commit=HEAD` | same |
| 12 | gate-timing | `gate_timing_check.py --selftest` | 0 | `[selftest] ALL PASS` | same |
| 13 | benchmark-spec-audit | `plans/benchmark_spec_audit.py --summary` | 0 | `task_count=812 distinct_task_ids=812 … findings=0 exit=0` | same |
| 14 | benchmark-spec-audit | `--selftest` | 0 | `SELFTEST clean cases=67` | same |
| 15 | registry-reference-check | `plans/registry_check.py --summary` | 0 | `source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0` | same |
| 16 | registry-reference-check | `--selftest` | 0 | `SELFTEST clean cases=15` | same |
| 17 | config-projection | `plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0` | same |
| 18 | config-projection | `--selftest` | 0 | `SELFTEST clean cases=31` | same |
| 19 | sources-adopt | `plans/sources_adopt.py` (bare) | 2 | `error: --registry and --package are required unless --selftest` | same (documented usage) |
| 20 | sources-adopt | `--selftest` | 0 | `SELFTEST cases=17 failed=0` | same |
| 21 | package-gate | `plans/pkg_gate.py package --root . --spec plans/pkg-spec-r35.json --rerun --require-clean-tree` | 0 | `P1…P10 ok`, `P10 ok probe_rerun=byte-equal bytes=3399`, `P9 ok untracked=0`, `defects=0` | same |
| 22 | round36-c1-battery | `plans/round36_c1_verify.py --lane .` | 0 | `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`; `rows=4 closed=4 observed_pass=4 mismatches=0`; `PREDICATE C1 pass` | same |
| 23 | regex-log-probe self-test | `plans/round36_c2_verify.py --lane .` | 0 | `W1…W6 ok`, `checks=6 defects=0`, `PREDICATE C2 pass` | same |
| 24 | regex-log-probe | `plans/regex_log_probe.py --lane .` + `cmp` vs receipt | 0 | `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; `CMP byte-equal`, receipt sha256 `439101fa…a2be` | same |
| 25 | census (ticket) | `scripts/sources-census.sh validate --file corpus/SOURCES.md` | 0 | `file ok <clone>/corpus/SOURCES.md` after **15** `W04` duplicate-url warnings (S040…S100) | same 15 |
| 26 | **git-webserver-probe** | `plans/git_webserver_probe.py --lane . --work …` (52.8 s) | 0 | `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | new row, green |
| 27 | **round37-c1-mutants** | `plans/round37_c1_verify.py --lane . --work …` (81.7 s) | 0 | `GATE plans/pkg_gate.py sha256=frozen`; `BATTERY fixtures=64 wrong=0 renamed_disagree=0`; `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`; `PREDICATE C1 pass` | wave-1 red → green |
| 28 | **round37-c2** | `plans/round37_c2_verify.py --lane . --work …` (53.0 s) | 0 | `V1…V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass` | wave-1 red → green |
| 29 | **anchor-digest-check** | `plans/anchor_digest_check.py --lane .` | 0 | `rows=107 tokens=15 defects=0` | new row, green |
| 30 | **ledger-tip** | `plans/ledger_tip.py --source <clone of tip> --work …` | **1** | `rows=9 closed=9 observed_pass=7 mismatches=2` | **new red** (§3) |

C1/C2 predicates required by the ticket are satisfied verbatim at `357deceb` on a clean clone
(`BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0
null_detected=0`, `PREDICATE C1 pass`, exit 0; `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0).

## 3. Finding N1 (new red) — `ledger-tip` reports a *mismatch* for an environment it never refuses

**Named harm:** registry row `ledger-tip` (`SKILL.md:581`) is red at the assigned tip in the clone shape every
fleet seat is *required* to use, and it reports the red as a ledger mismatch (`exit 1`, `agree=NO`) rather than
the setup refusal its verdict map reserves for clone problems (`2 usage/clone refusal`).

Observed (`receipts/33-ledger-tip.log`), source = my detached-HEAD clone of `357deceb`:

```
R34-D2 status=closed observed=fail agree=NO error CalledProcessError: Command '['git', '-C', '…/work/lt/lane', 'ls-tree', '-r', '--name-only', 'refs/heads/master', …]' returned non-zero exit status 128. ledger=corpus/defects.jsonl kind=pin
R35-D3 status=closed observed=fail agree=NO error CalledProcessError: Command '['git', '-C', '…/work/lt/lane', 'ls-tree', '-r', '--name-only', 'refs/heads/master']' returned non-zero exit status 128. ledger=corpus/defects-round35.jsonl kind=pin
rows=9 closed=9 observed_pass=7 mismatches=2
```

Root cause (two hops, both verifiable in the tree):

1. The two pin-kind check bodies hardcode a branch ref: `plans/defect_ledger.py:29` and
   `plans/round36_c1_verify.py:38` both read `BRANCH = "refs/heads/master"`. These are the `kind=pin` rows
   R34-D2 and R35-D3 that failed.
2. `plans/ledger_tip.py:69` clones with `git clone -q --shared <source> <dest>`. A `git clone` of a
   **detached-HEAD** source produces a detached clone with **no local `master` ref**, so
   `git ls-tree … refs/heads/master` exits 128. `ledger_tip.py` then folds an infrastructure exception into
   `observed=fail agree=NO` (exit 1) instead of exiting 2.

Controls that isolate the cause to the ref, not to the bytes (`receipts/controls.tsv`):

| control | setup | result |
|---|---|---|
| same tree, master ref present | clone of the same commit + `git update-ref refs/heads/master 357deceb…`; both trees resolve to `bc1532d0…` | `rows=9 closed=9 observed_pass=9 mismatches=0`, rc **0** (`35-ledger-master.log`) |
| same clone, control mode | `--lane <detached clone>` | `dirty=0`, `rows=9 … mismatches=0`, rc **0** (`36-ledger-lanectl.log`) |
| lane on master, current head | `--source /home/vgpnk/Projects/shokunin/kengaku-shokunin` (TIP `dc90676`) | `rows=9 … mismatches=0`, rc **0** (`43-ledger-lane-master.log`) |

So the gate is green on the normal operator path and on the same bytes whenever a local `master` exists; it is
red only when the source clone is detached, which is exactly the state the fixture rule ("`git checkout -q
<tip>`") imposes on every wave-2 seat. The red is a **false red** — no ledger row regressed — but it is a real
defect of the landed gate: a seat replaying the registry entry per the rules gets `exit 1` and must now
distinguish "two ledger rows fail" from "my clone has no master ref", a distinction the row's verdict map does
not offer.

The row is also *not* reproducible from the receipt as filed: `measure-final.txt` records
`TIP 5c7d5d75c2f36eb3477594432afe186b8b220086` (line 1) and `rows=9 … mismatches=0`, i.e. it was measured on a
source clone that carried `master`, two commits before the assigned tip.

## 4. Finding N2 (operability; not counted as a predicate failure) — `--work` must pre-exist, and its absence exits 1

Three of the five new rows hand an optional `--work` directory straight to `tempfile` without creating it:
`plans/round37_c1_verify.py:299` (`mkdtemp(prefix="k37-c1-", dir=a.work)`),
`plans/round37_c2_verify.py:214` (`TemporaryDirectory(prefix="k37-c2-", dir=a.work)`),
`plans/git_webserver_probe.py:271` (`mkdtemp(prefix="k37-cgw-", dir=a.work)`). `ledger_tip.py:101-102` is the
only one that does `work.mkdir(parents=True, exist_ok=True)`.

Measured, each with a fresh, absent `--work` path (all three receipts in `controls.tsv`):

```
round37_c1_verify.py --battery r36 --work <absent>  -> FileNotFoundError … k37-c1-1www4ozd   rc=1
round37_c2_verify.py --lane . --work <absent>       -> FileNotFoundError … k37-c2-kkorkmpl   rc=1
git_webserver_probe.py --lane . --work <absent>     -> FileNotFoundError … k37-cgw-mb87d_o2 rc=1
```

The registry rows map `1` to predicate failure and `2` to usage/setup, so an operator typo in a scratch path is
indistinguishable from "a mutant survived" or "a capture moved". With the directory pre-created, all three run
their declared predicate (§2). The documented selectors are also fine when `--work` exists:
`--battery r36` → `BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS … killed=5 survived=50`,
`PREDICATE C1 n/a (non-default battery or mutant subset)`; `--only M01,M02` → `killed=2 survived=0`, same
`n/a` predicate; `--battery nope` → argparse `error: … invalid choice`, rc 2.

## 5. Red-direction controls (does anything still bite?)

| control | command | observed |
|---|---|---|
| C1 refuses a gate off its freeze digest | comment appended to `plans/pkg_gate.py` in a scratch copy | `GATE plans/pkg_gate.py sha256=NOT-AT-FREEZE-DIGEST`, `MUTANTS total=55 killed=0 survived=0 invalid=55`, `PREDICATE C1 fail`, rc 1 |
| anchor check sees a wrong digest | one hex digit changed in S111's anchor | `DEFECT S111 anchor token=526aee3d…53346b38 class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS loc=corpus/SOURCES.md:126`, `rows=107 tokens=15 defects=1`, rc 1 |
| anchor check refuses bad args | `--evidence-ref bogus` | argparse `invalid choice: 'bogus'`, rc 2 |
| probe refuses a moved capture | byte appended to `corpus/evidence/round37/tb2-git-webserver/test_outputs.py` | `SETUP capture test_outputs.py missing or not at its pinned digest`, rc 2 |
| gate-timing still has a red direction | `--lesson corpus/lessons/round-25.md --commit 8ea41f9` | `passed=0 failed=1`, `reasons: no cited, existing, returned second-seat report`, rc 1 |

The S110 erratum exemption is row-scoped, not blanket: `corpus/SOURCES.md:125` still carries the 63-hex token
`4f7ac05e…e96f9c`, `corpus/lessons/round-37.md:32` corrects it, and the check accepts it (`defects=0`) while my
S111 mutant (a 64-hex token one digit off) is still a defect.

## 6. Observations (freshness / operability; no action taken here)

1. **Growth-only deltas vs the wave-1 baseline.** census knowledge `indexed` 43 → 44 and `P8 index_rows=44
   knowledge_files=44` (the new `corpus/knowledge/tb2-git-webserver-grader.md`); everything else the baseline
   printed is byte-identical, including `P10 … bytes=3399`, `population=1964`, `assertions=329 match=318`,
   `task_count=812`, the 15 `W04` warnings, and the regex receipt digest `439101fa…`.
2. **`measure-final.txt` names a stale TIP.** Its line 1 is `TIP 5c7d5d75…` while the assigned integration tip
   is `357deceb…`: `git log --oneline 5c7d5d7..357dece` returns `aa3d6ea`, `188a265`, `357dece` (three
   commits), and the lane's current master `dc90676` is a further three. I re-ran every predicate of that
   receipt at `357deceb` and they all still hold (§2), so the receipt is *semantically* current but its `TIP`
   field is not.
3. **`anchor-digest-check`'s provenance path is absent at the tip.** The row (`SKILL.md:580`) cites
   `.ufo/waves/round-37/build/R37AnchorSweep.md` and external falsifiers `fixture_matrix.py` /
   `fixture-receipt.txt`; at `357deceb` `find .ufo/waves/round-37 -maxdepth 2` lists no `build/` at all — the
   wave-1 reports (and those falsifier files) land only in `67cbe7a`, after this tip. A reader at the tip
   cannot open the cited falsifiers; the check itself is green and its red direction is reachable (§5).
4. **No registry row for the newly landed audit.** `plans/round37_c1_attribution.py` (added by `357dece`) has
   no `SKILL.md` row (`grep -c "round37_c1_attribution\|c1-attribution" SKILL.md` → `0`). It runs clean:
   `ATTRIBUTED 55/55 UNATTRIBUTED=0`, rc 0, 21.3 s.
5. **The frozen C1 "nothing" control is battery-bound, not gate-bound.** `claims/control-c1-nothing.txt` reads
   `MUTANTS total=55 killed=5 survived=50 … PREDICATE C1 fail`, and at the tip **with the edited gate**,
   `--battery r36` reproduces those exact numbers (§4) because the 50 kill-attributing fixtures are outside
   that battery. The pre-landing state is therefore not recoverable from those numbers alone; the evidence that
   the 55 kills are real is the full battery plus the attribution audit (item 4), not the control text.
6. **Carried forward from wave 1, unchanged:** the `coverage-census` paragraph after the registry table still
   says the script "lands with the census seat's artifact in this wave" although it is present and exits 0;
   `grader-perturb` exit 0 means "audit completed, including family FAIL findings"; `sources-adopt` bare exits
   2 by design and carries no verdict.
7. **`package-gate` numbers differ from the receipt's gate block for a legitimate reason.** `measure-final.txt`
   shows the gate via `plans/pkg-spec-r37.json` (`P1 pinned=2`, `P3 rows=32`, `P7 source_lines=4`); the registry
   command uses `plans/pkg-spec-r35.json` (`P1 pinned=3`, `P3 rows=22`, `P7 source_lines=3`). Both end
   `defects=0` / `P10 byte-equal bytes=3399`. Not a regression — different spec.

## 7. No-harm invariants

1. **Tree unchanged:** `git -C $D/lane status --porcelain` = 0 lines before the sweep, after the fast set,
   after the slow set, and after all controls. `--ignored` adds only `__pycache__/` directories created by the
   runs (`plans/`, `plans/battery37/`, `corpus/evidence/round35/tb2-eval/`,
   `corpus/evidence/round36/tb2-regex-log/`, repo root) — no tracked, untracked or ignored *file* besides those
   caches, and no gate wrote into the tree.
2. **Lane untouched:** no `git add/commit/stash/checkout/reset/push/pull` and no jj command in the lane; no
   lane file edited; the only writes are under this seat's report dir and `S`.
3. **Source repo untouched:** `/home/vgpnk/Projects/shokuknow` was never read or written by this seat; no
   campaign tool was run.
4. **All reads by the gates are of committed bytes:** `P9 ok untracked=0` and the anchor check's
   `--evidence-ref head` default held at a clean tree.
5. Scratch `S` deleted before this report was finalised; receipts copied into
   `falsify/F37NoHarmSweep/receipts/` first.

## 8. Evidence inventory (all under `falsify/F37NoHarmSweep/receipts/`)

- `summary.tsv` — label, exit, seconds, last line for the 29 batch commands.
- `controls.tsv` — the 11 control/extra runs (r36 counters, both ledger-tip controls, lane-master run, C1
  digest refusal, anchor defect and usage, both `--work` crashes, tampered-capture setup refusal).
- `*.log` — full stdout/stderr per command, including the whole C1 battery/mutant listing, all seven C2 `Vn`
  blocks, the 22 probe cases, and the failing ledger-tip rows.
- `regexprobe-fresh.txt` + `CMP byte-equal` against `corpus/evidence/round36/regex-log-probe.txt`
  (`sha256 439101fa2eac0e79ebec088ab47d9fc4481df0ec12d0ebc6c3475319d426a2be`).
- `cmds.tsv`, `cmdsB.tsv`, `run.sh` — the exact command set and runner, replayable verbatim;
  `SHA256SUMS` covers every receipt file.

VERDICT: no-harm-29/30-new-red-1
