# R48C2Rerun — independent C2 v4 counter rerun

Axes named: **coverage** (R48-C2).

## Freeze and revision gate

- Stage-1 freeze exists in committed revision `a543d92083557dd9b33ee674e9b99b03411f80af`; it contains `plans/round-48-claims.md`. The measured candidate `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` descends from stage 1, and the claims file has no diff from stage 1 to candidate. Thus stage-1 claims predate the bounded checks below.
- Candidate revision: `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` (w1 handoff marker). Claimed baseline: `0f77f9b27931b3c76b3d095fc0fa70edb79556d9`.
- **Stage 2 is absent.** `git log --all -- plans/round48_c2_verify.py` returned no commits; `git ls-tree` found no `plans/round48_c2_verify.py` at either stage 1 or candidate; the frozen claims still contain `<V>` and `<N>`. Therefore there is no committed, pinned R48-C2 v4 counter to rerun. I made **no scored counter or full-probe run** and report no R48-C2 predicate/exit result.

## Bounded checks (dry/stage-check only)

Scratch: `/fast/scratch/hyaku/kengaku-r48/R48C2Rerun`; one shared clone at candidate plus a detached worktree at baseline. Before fixture use, `git rev-parse --show-toplevel` printed the exact scratch paths for both trees.

Exact commands and observed outputs:

```text
cd /fast/scratch/hyaku/kengaku-r48/R48C2Rerun/lane
python3 plans/polyglot_c_py_probe.py --lane . --dry > "$TMPDIR/dry_candidate.txt"
diff -q "$TMPDIR/dry_candidate.txt" corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
```
Observed: `exit=0`; `CANDIDATE DRY == FROZEN DRY TABLE`.

```text
cd /fast/scratch/hyaku/kengaku-r48/R48C2Rerun/base
python3 plans/polyglot_c_py_probe.py --lane . --dry > "$TMPDIR/dry_base.txt"
diff -q "$TMPDIR/dry_base.txt" /fast/scratch/hyaku/kengaku-r48/R48C2Rerun/lane/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt
```
Observed: `exit=0`; `BASE DRY == FROZEN DRY TABLE`.

```text
cd /fast/scratch/hyaku/kengaku-r48/R48C2Rerun/lane
python3 plans/polyglot_c_py_probe.py --lane . --stage-check --work "$TMPDIR/stage-check"
```
Observed exact summary: `stagecheck cases=18 failed=0`; exit `0`. The probe documentation says stage-check parses end states and “does not import `test_outputs.py`, does not call `test_fibonacci_polyglot`, and does not compile-and-run the candidate file.” This is the explicitly permitted pre-stage-2 mode.

```text
cd /fast/scratch/hyaku/kengaku-r48/R48C2Rerun/lane/corpus/evidence/round46/tb2-polyglot-c-py
sha256sum -c SHA256SUMS
```
Observed: all eight files `gitignore`, `README.md`, `Dockerfile`, `instruction.md`, `solve.sh`, `task.toml`, `test.sh`, and `test_outputs.py` reported `OK`; exit `0`.

At candidate, observed pins: probe SHA-256 `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`; dry-table SHA-256 `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`; spec SHA-256 after masking `receipt_sha256` to `PENDING-STAGE-2` was `560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e`, matching the imported round-46 counter's pin values.

## Concrete defects and predicate implications

1. **Counter rerun blocked:** there is no stage-2 commit/counter/pinned `<V>` or `<N>`. The requested frozen-counter checks, defects, predicate, and exit cannot be observed yet. The stage-1 predicate remains frozen; this is not evidence that it passes or fails.
2. **V7 is still defective in the current committed package inputs:** the frozen receipt has violating cases for `single-file`, `python-run`, `c-build`, `fib-kth`, and `stdout-only`, but none for frozen tags `both-print` and `toolchain`. The committed entry itself says those two tags “are violated by no frozen case.” The stage-1 contract requires stage-2 case amendments to supply violating cases for all seven tags; until then the expected V7 defect remains, not a passing result.
3. **Frozen surface digest mismatch:** stage-1 claims describe the hardened probe as SHA-256 `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d` and say it was integrated verbatim. That digest is the round-46 wave artifact's digest. The candidate committed `plans/polyglot_c_py_probe.py` instead hashes to `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26` (the value in `plans/round46_c3_verify.py`). These bytes differ, so the frozen surface description and committed probe do not agree. Stage 2 may pin inputs but cannot change the stage-1 claim; this needs explicit handling by the integration owner, not a silent re-freeze.
4. **Control wording conflicts with the declared baseline:** stage-1 calls the C2 do-nothing control “the base tree (no `plans/polyglot_c_py_probe.py`)”. But the declared baseline `0f77f9b` already contains that path (blob `f38471151a1117c2fd18fd0ecc8240905b427c77`). The no-probe control therefore is not literally that baseline; its derivation must be unambiguous before a control receipt is treated as the frozen base control.

## Source record

Access date for all local sources below: 2026-10-27. Quotes are located, verbatim, and each is ≤25 words.

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — §C2 control: “the base tree (no `plans/polyglot_c_py_probe.py`)”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — C3 row: “V7 lacks violating cases for `both-print` and `toolchain`”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/polyglot_c_py_probe.py` — lines 10–12: “Before the stage-2 freeze only `--dry` and `--stage-check` are run”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c3_verify.py` — line 121: `PROBE_SHA256 = "67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26"`.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` — first line: `TAG single-file instruction.md:1`.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round46/polyglot-c-py-probe.txt` — summary: `cases=18 observed_pass=7 observed_fail=11 mismatches=0` (round-46 committed receipt; not rerun here).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/knowledge/tb2-polyglot-c-py-grader.md` — §Requirement map: “two of them (`both-print`, `toolchain`) are violated by no frozen case”.
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/order_check.py` — module docstring: “a frozen probe must not run before its receipt is committed.” (Read only; not run.)
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2SourceReject.md` — line 9: “The page does not list gcc or Python versions.”
- `file:///home/vgpnk/.omp/agent/RULES.md` — tooling directive: “Record every install or update — tool, version, channel, reason — in your report or handoff.”

Verification gap: no LSP device/server is exposed in this session, so caller/definition/diagnostic queries could not be performed. This is not semantic proof of absence; the stage-2 counter absence was checked from committed Git tree/history.

No tools installed or updated.

## Limits and verdict

Only dry/stage-check and hash/tree checks were run. No scored v4 counter, no full probe, and no graded case was executed. No C2 admission is claimed. Scratch cleanup is performed before yield.

VERDICT: **BLOCKED — no stage-2 frozen C2 v4 counter exists in the committed lane tree; no predicate/exit available.** Current package evidence also retains the V7 gap and the two freeze/control inconsistencies above.
