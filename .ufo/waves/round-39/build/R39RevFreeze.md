# R39RevFreeze — freeze-order audit (kengaku round 39, hyaku run 8, 2026-10-26)

Axes: (1) freeze integrity — nothing frozen changed and the receipt postdates the freeze; (2) reproducibility —
both do-nothing controls re-run on a clean clone of the freeze commit; (3) disclosure accuracy — the claims'
order-of-operations section checked against gate/counter/probe source and committed control contents.

All work in scratch `/fast/scratch/hyaku/kengaku-r39/R39RevFreeze` (removed at end; receipts copied to
`.ufo/waves/round-39/build/R39RevFreeze/`). Two `git clone -q --shared` copies of the lane, each
`git checkout -q --detach 088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8`, `git status --porcelain | wc -l` = 0.

## 1. Commit order

`git -C <lane> log --format='%H %cI %s' b2bdd425..master`:

```
750473847af9c7a461487ba3a589b5519fac5ed8 2026-10-26T03:44:10-03:00 round-39: wave-1 spec and validated dispatch (36 seats, policy v1)
6a1eb5e1da4a435940b821e28530c31f3411549c 2026-10-26T03:40:45-03:00 round-39: first recorded git-leak probe run (25 cases, mismatches=0, byte-equal second run)
088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8 2026-10-26T03:40:24-03:00 round-39: freeze claims, C1/C2 counters, git-leak probe, dry table, captures, controls
ef2fba062069de4f29aea45cb2a03d29a131054b 2026-10-26T03:37:53-03:00 round-38: wave-2 reports and results (34/34), outcome appended to lesson
```

Freeze 088f7c3 (03:40:24) precedes receipt commit 6a1eb5e (03:40:45) by 21 s; master is 7504738, which adds only
dispatch files. Order matches the claims header.

## 2. Freeze commit carries the right set — and no receipt

`git show --name-status 088f7c3` — exactly 21 files, all status `A` (nothing pre-existing modified):
`.ufo/waves/round-39/claims/` ×7 (census-before.txt, control-c1-gate-edited.txt,
control-c1-hostile-inproc-module.py, control-c1-hostile-inproc.txt, control-c1-nothing.txt,
control-c2-nothing.txt, frozen-digests.txt), `corpus/evidence/round39/git-leak-dry-cases-freeze.txt`,
`corpus/evidence/round39/tb2-git-leak-recovery/` ×8 (7 captures + SHA256SUMS), `plans/git_leak_probe.py`,
`plans/pkg-spec-r39.json`, `plans/round-39-claims.md`, `plans/round39_c1_verify.py`, `plans/round39_c2_verify.py`.

- Receipt absent at freeze: `git cat-file -e 088f7c3:corpus/evidence/round39/git-leak-probe.txt` →
  `fatal: path … exists on disk, but not in '088f7c36…'` (exit 1). Present at 6a1eb5e (exit 0). ✓
- No battery39 at freeze: `git cat-file -e 088f7c3:plans/battery39` → `fatal: path 'plans/battery39' does not
  exist …`. ✓ (claims: "Written and frozen before any `plans/battery39` fixture exists")
- 6a1eb5e diffstat: `corpus/evidence/round39/git-leak-probe.txt | 30 +++` and
  `.ufo/waves/round-39/first-run/first-run.txt | 7 +++` — 2 files, 37 insertions, zero modifications to frozen
  files. The receipt landed in exactly that commit. ✓

## 3. Digests

`for p in frozen-digests.txt: git show 088f7c3:<path> | sha256sum` — **9/9 OK**: pkg_gate.py
(`ea638822…`), round39_c1_verify.py, round39_c2_verify.py, git_leak_probe.py (`4961a50f…`), pkg-spec-r39.json,
git-leak-dry-cases-freeze.txt (`e92a5d6d…`), round37_c1_verify.py, round38_c1_verify.py, round38_c2_verify.py.
Full hashes in `.ufo/waves/round-39/claims/frozen-digests.txt`; every row matched its freeze blob.

Captures: `cd …/tb2-git-leak-recovery && sha256sum -c SHA256SUMS` on the freeze checkout → **7/7 OK** (Dockerfile,
challenge-setup.sh, instruction.md, solve.sh, task.toml, test.sh, test_outputs.py).

Receipt: `git show 6a1eb5e:corpus/evidence/round39/git-leak-probe.txt | sha256sum` →
`d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f`, equal to the run1 digest recorded in
`.ufo/waves/round-39/first-run/first-run.txt`. ✓

## 4. Control re-runs on a clean clone of 088f7c3

Method: `TMPDIR=$S/w1 python3 plans/round39_c1_verify.py --lane .` in the freeze clone (work dir via tempfile under
TMPDIR, counter docstring: `--work DIR  scratch parent (default: $TMPDIR via tempfile)`); same for C2 in the second
clone. Raw outputs + diffs archived: `build/R39RevFreeze/out-c1.txt`, `out-c2.txt`, `c1-rerun.diff`, `c2-rerun.diff`.

**C1** (`c1-rerun.diff`): substantive output byte-identical to `control-c1-nothing.txt` — `PINS total=26
mismatched=0`, `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=3
survived=4 invalid=0 null_detected=0`, `PREDICATE C1 fail`, observed rc=1. Sole delta: the committed file's
trailing `exit=1` line, which the counter does not print (seat annotation; observed rc matches it).

**C2** (`c2-rerun.diff`): all check verdicts identical (`V1 ok`, `V2 DEFECT gate_exit=1`, `V3 DEFECT
S117/S118`, `V4/V7 receipt or entry absent`, `V5 ok probe=frozen dry_byte_equal=True`, `V6 ok census_exit=0`,
`checks=7 defects=4`, `PREDICATE C2 fail`, rc=1). Two deltas beyond the same `exit=1` annotation, both expected:

| line | committed control | clean-clone rerun | why |
|---|---|---|---|
| P9 | `DEFECT untracked=19 first=.ufo/waves/round-39/claims/census-before.txt` | `ok untracked=0 first=0` | control captured 03:39:07 (file mtime) on the dirty pre-commit lane tree; the freeze clone has the claims committed |
| gate defects | `defects=8` | `defects=7` | arithmetic consequence of P9 becoming ok |

The evidentiary core — `P10 DEFECT receipt unreadable` — is present in both the committed control and the rerun.

## 5. Order of operations: did any committed control execute the probe?

No. Chain of evidence:

1. The gate's rerun path cannot: `c_rerun` reads the receipt first — `want = read(p.root / p.spec["receipt"])`,
   `if want is None: return False, "receipt unreadable"` (`plans/pkg_gate.py:268-270`) — and returns before the
   probe argv is built (`probe = list(p.spec["probe_cmd"])` comes after). With the r39 spec's receipt absent at
   freeze, P10 exits there. Both the committed control and my clean-clone rerun print `P10 DEFECT receipt
   unreadable`, so the C2 control's gate run never executed the probe.
2. The C2 control's only probe execution is V5's `--dry`: `subprocess.run([sys.executable, str(lane / PROBE_REL),
   "--lane", str(lane), "--dry"], …)` (`plans/round39_c2_verify.py:195`). `--dry` "print[s] the frozen case table
   only (no sandbox)" (probe docstring) and returns before any sandbox/grader code (`git_leak_probe.py:241-248`
   precedes `run_case`); the grader import sits behind `if mode == "stage": sys.exit(0)`
   (`git_leak_probe.py:171-173`). This is exactly the pre-freeze mode the claims disclose: "the probe ran only as
   `--dry` (no sandbox) and `--stage-check`" (`plans/round-39-claims.md`, Order of operations).
3. The C1 side cannot reach the r39 probe: every battery rerun fixture uses the r35 spec, whose `probe_cmd` is
   `["plans/tb2_grader_probe.py", "--lane", "."]` (`plans/pkg-spec-r35.json:7-10`) — a different probe.
4. The first full (sandboxed, grader-importing) execution is the one 6a1eb5e records: first-run.txt —
   "clone: git clone --no-local <lane>; checkout 088f7c36… (the freeze)", run twice from scratch work, rc1=0 rc2=0,
   byte-equal, sha256 `d7f3a465…` = the committed receipt blob. Freeze commit 088f7c3 predates it.

## Findings by severity

**Defects: none.**

Observations (informational, for L1):

- **O1 — control files embed a manual `exit=1` annotation.** Both committed controls end with `exit=1`, which
  neither counter prints; raw counter stdout ends at `PREDICATE … fail` and observed rc=1 matches. Cosmetic; the
  convention (appended rc line) is undocumented but unambiguous.
- **O2 — `control-c2-nothing.txt` froze the dirty-tree P9 state.** `P9 DEFECT untracked=19` reflects the
  pre-commit lane, so a landing-tip re-run of the do-nothing comparison will read `P9 ok untracked=0` /
  `defects=7`. Evidentiary value unaffected (P10 `receipt unreadable` is the operative line); archived diff shows
  the exact two-line delta to expect.
- **O3 — the promised post-run skip-control is not yet committed.** Claims: "No skip-control that would make P10
  execute the probe is run before the first recorded probe run; it is run, and committed, after that run"
  (round-39-claims.md, Order of operations). As of master 7504738 nothing after 6a1eb5e adds a control (7504738
  adds build-dispatch.json, build-spec.json, make_build_spec.py only). Forward-looking statement — admission must
  not forget to run and commit it.

## Residual risk / verification gaps

- I did not re-run the full probe (a second recorded run belongs to the first-run protocol, not to this audit);
  the byte-equal second-run claim rests on first-run.txt's `cmp run1 run2 -> byte-equal` statement.
- Commit order is the canonical timing evidence; wall-clock capture times (control mtimes 03:37:45 / 03:39:07,
  both pre-freeze) are consistent but not git-provable beyond it.
- LSP unavailable/unneeded: this audit's subject is git objects and control text, not symbol references; all
  evidence above is command output quoted verbatim.
- Capture-side integrity relies on the captures' own SHA256SUMS (self-referential at freeze); upstream-origin
  verification against terminal-bench-2 @ 2fd12b88 is C2's surface, not re-checked here.

VERDICT: freeze-audit-ok
