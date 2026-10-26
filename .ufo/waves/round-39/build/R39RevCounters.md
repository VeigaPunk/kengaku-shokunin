# R39RevCounters — code review: round39_c1_verify.py, round39_c2_verify.py, git_leak_probe.py

Scope: the three frozen files as committed at freeze `088f7c3`. All three verified byte-identical to that
commit in the current lane (`git diff --quiet 088f7c3 -- <file>` → SAME-AS-FREEZE for all three; probe sha256
`4961a50f28ae85e8…` matches `PROBE_SHA256` at round39_c2_verify.py:62). Method: full read of all three plus
pkg_gate.py, round37_c1_verify.py (Ctx), pkg-spec-r39.json, the captured grader, the frozen controls; every
claim below reproduced in my scratch clone `/fast/scratch/hyaku/kengaku-r39/R39RevCounters/lane` (deleted
after; receipts preserved in `build/R39RevCounters/`). The real lane was never written.

## Reproduction baseline (all commands run in my scratch clone)

| Check | Command | Result |
|---|---|---|
| C1 do-nothing | `python3 plans/round39_c1_verify.py --lane $S/lane` | `PINS total=26 mismatched=0` / `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0` / `MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0` / `PREDICATE C1 fail`, rc=1 (24.2 s) — identical to `.ufo/waves/round-39/claims/control-c1-nothing.txt`, same kill names (M01←d5m-n21-manifest-row-2, M05←p23-p2-receipt-deleted, M06←r36-P0; M02/M03/M04/M07 survive). Receipt: `R39RevCounters/c1-repro.txt` |
| C2 mid-wave | `python3 plans/round39_c2_verify.py --lane $S/lane --work $S` | `V1 ok`, `V2 DEFECT gate_exit=1`, `V3 DEFECT`, `V4 DEFECT`, `V5 ok probe=frozen dry_byte_equal=True`, `V6 ok`, `V7 DEFECT` → `checks=7 defects=4`, the same four as `control-c2-nothing.txt`. Receipt: `c2-midwave-run.txt` |
| C2 P10 chain | same run, gate output | `P10 ok probe_rerun=byte-equal bytes=5867` — the gate's fresh probe rerun through V2 is byte-equal to the frozen receipt |
| Probe grade | `probe_iso.py` (copy + one added case) | all 25 frozen cases `match=yes`; added iso case FPPPP (my case writes no flag); `cases=26 observed_pass=13 observed_fail=13 mismatches=1` |
| Probe dry | `python3 plans/git_leak_probe.py --lane $S/lane --dry` | rc=0, byte-equal to `corpus/evidence/round39/git-leak-dry-cases-freeze.txt` |

## Findings by severity

### 1. MEDIUM (C1 counter integrity): pins and the effective reference spec are never re-verified after the battery children run

Children execute at round39_c1_verify.py:281-285 (`module_fixtures` for battery38/battery39; each child is a
full-privilege process that receives `ctx` with the lane path, round37_c1_verify.py:192-196). The PINS digest
check runs once, before them (:261), and is never repeated. The gate copies are safe — written from the
in-memory `gate_src` read at :264, before children, and digest-checked per mutant (:365-368) — but every
reference and mutant gate run appends `ctx.spec_path` (:313, :334, :341, :364), and `Ctx.spec_path` is
`lane / "plans/pkg-spec-r35.json"` on disk (round37_c1_verify.py:194). A battery39 module can therefore
rewrite a pinned lane input mid-run and the counter neither notices nor aborts.

Demonstrated (receipt `c1-hostile-spec-tamper-run.txt`): a `--battery-dir` module whose `build` appends one
byte to `plans/pkg-spec-r35.json` and returns an innocent fixture argv. The run printed
`PINS total=26 mismatched=0`, built and ran everything, and left the clone with
`M plans/pkg-spec-r35.json` (`git status --short` after the run) with no counter diagnostic.

Mitigants found while trying to weaponize it: the `ok` check compares the reference defect set to the
declared set (`res[1] == frozenset(declared)`, :321), so any tamper that changes reference DEFECT output on a
declared fixture trips `wrong>0`; exhibits require the declared set to contain the mutant's clause, so a
tamper that keeps all 86 expectations intact cannot manufacture a kill either. I could not construct a false
green this way. What remains: (a) the advertised invariant "a module hands back only JSON" is false at the
filesystem level; (b) a broken or hostile module can dirty pinned lane inputs during the landing measurement,
which the no-harm checks and C2 then read. Recommended for L1 (post-freeze errata or round-40): re-run the
PINS check after :285 and abort on change, or stage a copy of the r35 spec under `root` at :268 and pass the
copy. One line either way.

### 2. LOW (probe error path): a sandbox timeout crashes with a traceback and exit 1, not the documented error taxonomy

`run_case` passes `timeout=300` (git_leak_probe.py:216) and `TimeoutExpired` is caught nowhere — not in
`run_case` (:206-219) nor in main's case loop (:276-283). A hung bwrap case yields a Python traceback, exit
code 1, and a truncated receipt, while the docstring promises "A setup or recipe that exits non-zero is a
probe error (exit 2), never a verdict" (git_leak_probe.py:15-16). Downstream damage is bounded — the gate's
P10 and V5 would see a non-zero/short output and defect honestly, so no false green — but a mid-receipt crash
also discards the cases already graded. Fix: wrap the `run_case` call in `except subprocess.TimeoutExpired`
→ print `SETUP case … timed out`, return 2.

### 3. LOW (carried from round 38, not a regression): C2 V6 depends on an unpinned, host-absolute script outside the lane

`CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` (round39_c2_verify.py:65). It is (a)
unrunnable from a clean clone on any other host, so the frozen predicate "measured on a clean clone of the
landing tip" silently assumes this host; (b) not digest-pinned, so the census grammar can drift between
freeze and landing without any counter noticing. Verified carried verbatim from round38_c2_verify.py:63, so
round-38 precedent — but the round-39 docstring's "Every input this counter reads that exists at the freeze
is pinned here by digest" (round39_c2_verify.py:9-10) overclaims: the census script is read and not pinned.
Fix: pin its digest in a comment at minimum, or copy it into the lane; otherwise name the host-bound limit in
the entry.

## Notes (operability, no defect claimed)

- N1 — `environ` is a substring token (:100, scan at :193): a battery39 comment saying "environment" flips
  `sidechannel>0` and fails the predicate. Wave-1 executors must avoid the bare letters `environ`, `ppid`,
  `cmdline`, `psutil`, `/proc` anywhere in module source. Conservative direction; just a trip hazard.
- N2 — argv confinement covers only `--spec` (:293-297); `--root`, `--file`, `--capture-dir` returned by a
  module may point anywhere. Expectation legs (`wrong`, declared sets) bound the damage, but confining all
  path-like argv to the fixture dir would close it cheaply.
- N3 — duplicate fixture ids are a hard stop across all batteries (:300-304). battery38 uses bare ids
  (`p10b-rerun-byte-equal-accept`); battery39 modules should namespace (e.g. `b39-…`) or a collision reds the
  run with `SETUP duplicate fixture id`.
- N4 — in grade mode only harness stdout is printed on failure (:282); bwrap/recipe stderr is swallowed.
  Determinism-protecting, but the SETUP path would benefit from a stderr tail.
- N5 — V3's anchor regex (:147) and the census script are two different grammars for the same registry row:
  my synthetic 11-cell row passed V3 (`V3 ok rows=2 bad=0`) and failed census (`V6 DEFECT census_exit=1`).
  Wave-1 must satisfy both; test against `sources-census.sh validate`, not V3 alone.
- N6 — when the gate's P10 reruns the probe (V2), the gate passes no `--work`, so the probe's scratch follows
  the caller's TMPDIR. Export `TMPDIR` when running the landing predicate, per the seat directive.
- N7 — verified non-issue: C1's in-process imports drop `__pycache__/` into `plans/`, but the lane `.gitignore`
  covers it and gate P9 counts untracked via `ls-files --others --exclude-standard` (pkg_gate.py:254-259), so
  running C1 before C2 on one landing clone does not false-red V2/P9.

## Asked questions, answered with evidence

**C1 child-process contract — what a module still controls.** Cannot: patch the parent's `run_gate`
(separate process; the round-38 lesson holds), swap gate/mutant bytes (written from pre-child `gate_src`
after all children exit, :264/:318/:347, digest-checked per mutant :365-368), or smuggle a second result
line (parent takes exactly one `BUILT ` line, :176-179; extra lines or rc≠0 → SETUP rc 2). Can: print junk
(filtered), return a spec inside a *sibling* fixture dir (rejected, :296-297), read/write any user-writable
file including pinned lane inputs (Finding 1), spawn processes that outlive it (named limit in the claims),
and point `--root`/`--file`/`--capture-dir` anywhere (N2). Source scan is static, top-level `*.py` only
(:191-194); dynamically written helpers are neither scanned nor imported by the parent.

**rc legs vs docstring.** `exhibits` (:230-249) implements exactly the docstring's five legs: `rc-silence` =
expect reject + non-empty declared + ref rc 1 + mut rc 0; `rc-mirror` = expect accept + ref 0 + mut 1;
silence/mirror require both rcs in {0,1} and exclude RUN/MAIN; `error` (unused) = expect error + ref 2 +
mut ∈ {0,1}. `family_ok` (:224-227) matches the kill-rule family table incl. MAIN:any, applied before
exhibits (:342). Survivor lines print other exhibited directions (:355-357) — observed live as
`exhibits=none` for M02/M03/M04/M07. No deviation found. The M05/M06 `old` strings match the gate's actual
rc legs (`defects += not ok` in `run_checks`; `return 0 if cmd_package(args, spec) == 0 else 1` in `main`),
all seven `old` strings unique (invalid=0 in the control run).

**TMPDIR/--work honoured, no /tmp.** C1 root `mkdtemp(dir=a.work)` (:268); C2 `TemporaryDirectory(dir=a.work)`
(:264); probe `mkdtemp(dir=a.work)` (:258) — all fall back to $TMPDIR; the literal `/tmp` appears only as the
sandbox's private tmpfs mount target (git_leak_probe.py:197). Child/fixture temp dirs are created under the
counter root throughout.

**Probe sandbox.** Verified empirically on a copy with one instrumented case (recipe asserted each property;
rc=0 proves all passed): `GIT_CONFIG_GLOBAL=/dev/null` + `GIT_CONFIG_NOSYSTEM=1` (:213) → `git config
--global --list` empty and `git config user.name` empty inside; `/app` a fresh writable bind (:197-198,
per-case `mkdtemp` :207); `HOME=/tmp` (:211-213). Recipe failure leg: a copy with `exit 7` recipe → probe
rc=2, stderr `SETUP case recipe-fails did not yield five test verdicts (rc=3)` + `STAGE recipe rc=7`
(harness exits 3 at :168-170; main maps rc≠0 → 2 at :280-283). Nothing host-specific printed: the frozen
receipt is 30 lines = header with pinned digests + 25 CASE lines + summary; grep for `/home`, `/fast`,
`/tmp`, `vgpnk`, git version strings → no match. Residual: `/etc` is ro-bound read-only into the sandbox
(:197) — host /etc *content* is visible to cases (git config neutralized by NOSYSTEM; grader reads only
`/app` — verified in the captured test file); declared in the docstring (:13).

**Pins complete.** C1: 26 = gate + r37 + r36 + r35 spec + attribution audit + 9 battery37 + 12 battery38;
`plans/battery37` and `plans/battery38` contain exactly those 9 and 12 `.py` files (plus gitignored
`__pycache__`), and the predicate asserts `len(PINS) == 26` (:386). C2: seven captures pinned in the counter
and in the capture dir's own SHA256SUMS (V1 ok live); the probe pins the three files it executes. Witness
files named by the four surviving mutants all exist on the freeze commit. Gap: Finding 1 (post-child
re-verification) and Finding 3 (census script unpinned).

## Residual risk and verification gaps

1. V2's pass path has never executed in round 39 (it is red in both controls; the code is diff-verified
   unchanged from round 38's counter, which did pass at its landing). My positive control exercised V3/V4/V7:
   with synthetic S117/S118 rows and an entry whose map rows I derived by hand from the receipt, the counter
   printed `V3 ok rows=2 bad=0`, `V4 ok cases=25 mismatches_named=0/0`, `V7 ok rows=4 tags=4 bad=0` — and my
   hand derivation matches `derive()` exactly: recover-secret=enforced, secret-gone=partly,
   files-untouched=enforced, messages-untouched=partly. V2 remains exercisable only against a complete package.
2. Cross-host portability of the grader mapping is untested (host git 2.56/bash stand in for the image; the
   checksum test pins a digest of `find /app/repo -type f -not -path '*/\.*' | sha256sum`). 25/25 predictions
   reproduced twice more on this host; a different git/README byte layout would shift whole columns. Declared
   limit in the probe docstring; keep it in the entry.
3. The counters never verify the lane is a clean clone — that is procedural (P9 checks it only inside V2's
   gate run). Landing checklist should keep "fresh clone" literal for both counters.
4. `test_no_secrets_in_unreachable_objects` runs `git fsck --lost-found`, which writes `.git/lost-found/`
   before test 5's checksum; the dot-path filter excludes it — benign here, but any future test reordering in
   upstream would interact with it.

Receipts: `.ufo/waves/round-39/build/R39RevCounters/` (c1-repro.txt, c2-midwave-run.txt,
c2-positive-control.txt, c1-hostile-spec-tamper-run.txt, probe-recipe-fail-stderr.txt, probe-dry-repro.txt).

VERDICT: review-3-defects
