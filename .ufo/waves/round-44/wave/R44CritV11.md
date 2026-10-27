# R44CritV11 — critic: falsify C2 V11 (held-out predictor)

Seat: R44CritV11 (leaf). Date: 2026-10-26. Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin (read-only for this seat; every run inside the round-44 envelope, home read-only, `~/.local/bin` content digest unchanged in every run).

## 1. Verdict in one line

`VERDICT: v11-bypasses-4-of-7` — four distinct predictor programs that never perform the substring reading pass `c2.v11()` with 0 disagreements on the 48 seeded states. V11 verifies agreement with the executed grader on a fixed, deterministic, memorizable sample; it cannot verify that agreement came from reading the file.

## 2. Method

- Mirror construction is byte-for-byte the freeze control's (`claims/c2_predictor_control.py`): a scratch directory holding the frozen spec `plans/pkg-spec-r44.json`, the pinned capture `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/test_outputs.py`, and an entry with one `## Predictor` fenced python block.
- `c2` imported from `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round44_c2_verify.py` (frozen digest, unedited); every candidate run through `c2.v11(mirror, work)`.
- Ground truth: the 48 states regenerated exactly as v11 does (`c2.states(c2.constants(lane))`, `random.Random(44)`), graded by running the captured grader's `test_attack` in the identical bwrap construction v11 uses (`c2.sandboxed` with `--bind <work>/app /app --ro-bind <work>/tests /tests`). Independent regrade: **24 PASS / 24 FAIL**, exactly matching the freeze control `claims/control-c2-predictor.txt` (`grader_pass=24 grader_fail=24`).

Commands:
```
python3 /fast/scratch/hyaku/kengaku-r44/R44CritV11/harness.py  /fast/scratch/hyaku/kengaku-r44/R44CritV11
python3 /fast/scratch/hyaku/kengaku-r44/R44CritV11/harness2.py /fast/scratch/hyaku/kengaku-r44/R44CritV11
python3 /fast/scratch/hyaku/kengaku-r44/R44CritV11/probe_extra.py /fast/scratch/hyaku/kengaku-r44/R44CritV11
python3 /fast/scratch/hyaku/kengaku-r44/R44CritV11/probe_memorizer.py /fast/scratch/hyaku/kengaku-r44/R44CritV11
```
All run with cwd=/home/vgpnk/Projects/shokunin (fleet root) under:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r44/R44CritV11/env /fast/scratch/hyaku/kengaku-r44/R44CritV11/env --bind /fast/scratch/hyaku/kengaku-r44/R44CritV11/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 <script> /fast/scratch/hyaku/kengaku-r44/R44CritV11
ENVELOPE start 20:33:34 cwd=/home/vgpnk/Projects/shokunin   (run 1; end 20:33:36 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged — first run aborted on a table-building bug, see §7)
ENVELOPE start 20:33:44 cwd=/home/vgpnk/Projects/shokunin   (run 2; end 20:43:46 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged)
ENVELOPE start 20:43:57 cwd=/home/vgpnk/Projects/shokunin   (run 3; end 20:43:58 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged)
ENVELOPE start 20:44:17 cwd=/home/vgpnk/Projects/shokunin   (run 4; end 20:44:18 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged)
ENVELOPE start 20:44:29 cwd=/home/vgpnk/Projects/shokunin   (run 5; end 20:44:30 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged)
```

## 3. Ground truth (the 48 states, seed 44)

```
GROUNDTRUTH pass=24 fail=24
STATE  0 exact        PASS len=2047     STATE 16 exact        PASS len=2047     STATE 32 exact        PASS len=2047
STATE  1 shuffled     PASS len=2047     STATE 17 shuffled     PASS len=2047     STATE 33 shuffled     PASS len=2047
STATE  2 drop-one     FAIL len=2026     STATE 18 drop-one     FAIL len=2026     STATE 34 drop-one     FAIL len=2027
STATE  3 drop-three   FAIL len=1985     STATE 19 drop-three   FAIL len=1986     STATE 35 drop-three   FAIL len=1986
STATE  4 concat       PASS len=1947     STATE 20 concat       PASS len=1947     STATE 36 concat       PASS len=1947
STATE  5 zero-pad     PASS len=2300     STATE 21 zero-pad     PASS len=2300     STATE 37 zero-pad     PASS len=2300
STATE  6 hex          FAIL len=1895     STATE 22 hex          FAIL len=1895     STATE 38 hex          FAIL len=1895
STATE  7 decoys       PASS len=2760     STATE 23 decoys       PASS len=2619     STATE 39 decoys       PASS len=2354
STATE  8 bump-one     FAIL len=2047     STATE 24 bump-one     FAIL len=2047     STATE 40 bump-one     FAIL len=2047
STATE  9 absent       FAIL len=None     STATE 25 absent       FAIL len=None     STATE 41 absent       FAIL len=None
STATE 10 empty        FAIL len=0       STATE 26 empty        FAIL len=0       STATE 42 empty        FAIL len=0
STATE 11 comma        PASS len=2145     STATE 27 comma        PASS len=2145     STATE 43 comma        PASS len=2145
STATE 12 split-one    FAIL len=2048     STATE 28 split-one    FAIL len=2048     STATE 44 split-one    FAIL len=2048
STATE 13 duplicated   PASS len=2151     STATE 29 duplicated   PASS len=2172     STATE 45 duplicated   PASS len=2377
STATE 14 half         FAIL len=1022     STATE 30 half         FAIL len=1022     STATE 46 half         FAIL len=1022
STATE 15 prefixed-digit PASS len=2147   STATE 31 prefixed-digit PASS len=2147   STATE 47 prefixed-digit PASS len=2147
```

## 4. Bypass candidates through c2.v11() (results)

| # | predictor | kind | V11 result | note |
|---|-----------|------|------------|------|
| P0 | substring reading (control) | reads | `ok states=48 grader_pass=24 grader_fail=24 disagree=0` | required ok |
| P1 | raw-lookup | memorized | **`ok ... disagree=0`** | exact-content dict, no parsing |
| P2 | hash-lookup-fixed | memorized | **`ok ... disagree=0`** | sha256(text)→verdict dict |
| P3 | noisy-lookup-fixed | memorized | **`ok ... disagree=0`** | same table + extra stdout/stderr prints |
| P4 | js-lookup | memorized | **`ok ... disagree=0`** | reads `/states.json` inside sandbox, verdict table indexed by state position |
| P5 | len-heuristic (>700) | structural | `DEFECT ... disagree=18 at=drop-one#2,drop-three#3,hex#6,bump-one#8,split-one#12,half#14` | no |
| P6 | sandbox-read probe | structural | `DEFECT ... disagree=24 at=exact#0,shuffled#1,concat#4,zero-pad#5,decoys#7,comma#11` | no |
| P7 | timeout (sleep 610s) | structural | `DEFECT predictor failed: ... timed out after 600 seconds` | blocked, no |
| P8 | always-true (freeze control) | control | `DEFECT ... disagree=24 at=drop-one#2,drop-three#3,hex#6,bump-one#8,absent#9,empty#10` | required DEFECT |

`SUMMARY {"hash-lookup": false, "raw-lookup": true, "noisy-lookup": false, "sandbox-read": false, "len-heuristic": false, "timeout": false, "always-true": false}` (run 2); `SUMMARY2 {"hash-lookup-fixed": true, "noisy-lookup-fixed": true, "js-lookup": true}` (run 3). `CONTROL substring ok=True` (run 2).

**Four bypasses pass: P1, P2, P3, P4.** None of them reads the file content to decide: P1/P2/P3 are pure dictionary lookups keyed on the exact text (or its sha256); P4 additionally demonstrates a file read inside the sandbox (`/states.json`) but only to locate the memorized verdict. The predictor blocks contain no constants, no `in` test, no parsing.

## 5. Why a memorizer can be built (the design gap)

- The 48 states are deterministic: `random.Random(44)` over the 100 public constants of the pinned capture. One execution of the grader yields all 48 verdicts; the result is reproducible, so the table is stable.
- The claims doc says the verdicts exist "only by executing the grader, so a filler cannot copy them from the counter" (`plans/round-44-claims.md` §C2). True textually, but false operationally: **(a)** an author may legitimately execute the grader once (the counter itself does, on every run) and harvest the table; **(b)** the counter's own diagnostic leaks verdicts differentially — on any disagreement, `v11` prints up to six mismatching state labels: e.g. P8 → `at=drop-one#2,drop-three#3,hex#6,bump-one#8,absent#9,empty#10`, P5 → `at=drop-one#2,drop-three#3,hex#6,bump-one#8,split-one#12,half#14`. Fixing revealed states and re-running converges a table to `disagree=0` in ≈8 runs of the counter. Either path ends with a passer that never reads the file.

## 6. Sandbox characterization (what a predictor can observe)

- `sandbox-read` probe: `os.path.exists('/states.json')` is True inside the predict sandbox; `open('/app/plaintexts.txt')` raises FileNotFoundError. The predict sandbox binds only `/usr`, `/etc`, `/proc`, `/dev`, tmpfs `/tmp`, `/states.json`, `/predictor.py` — the grader's `/app` and `/tests` are not mounted, and work-dir state from the grading sandbox is not shared. No runtime exfiltration channel was found; the only viable non-reading pass is memorization (§4/§5).
- Timeout: a predictor hanging >600 s fails V11 cleanly (`predictor failed: ... timed out after 600 seconds`) — hangs are rejected, not exploited.
- Noise: extra stdout/stderr lines are tolerated (P3 passes; the counter parses only the last stdout line of the runner).

## 7. Honest notes

- First harness run aborted at table-building (`AttributeError: 'NoneType' object has no attribute 'encode'` on the absent states) — a harness bug, not a counter result; fixed, all reported runs are green envelope (exit 0, digest unchanged).
- Initial `hash-lookup` (None→True bug) produced `disagree=3 at=absent#9,absent#25,absent#41`; the fixed `hash-lookup-fixed` (None→False) passes. Both shown for completeness.

## 8. Is 48 states with seed 44 enough? No — coverage of grader behaviours

The 48 states are 3 repeats of exactly 16 hand-picked kinds (KINDS in the counter). Behaviours probed that **never appear among the 48** (all measured by executing the captured grader in the same sandbox):

| end state | grader result | probe |
|-----------|---------------|-------|
| all 100 constants sign-flipped (`-c`) | **PASS** (`c in "-c"` is a substring) | `probe_extra.py` → `["negated", true]` |
| whitespace-only file | FAIL (`AssertionError`) | → `["whitespace-only", false, "AssertionError"]` |
| unreadable file (chmod 000) | FAIL (`PermissionError`) | → `["unreadable", false, "PermissionError"]` |
| directory at `/app/plaintexts.txt` | FAIL (`IsADirectoryError`) | → `["dir-as-file", false, "IsADirectoryError"]` |

By inspection also untested: non-UTF8/bytes, huge files, FIFOs/dangling symlinks, exponent formats, constants with boundary separators other than newline (split-one only splits on `\n`), name-flip class, etc. Consequence: the sample is biased toward the 16 kinds; it cannot distinguish a memorizer from a reader, and a memorizer is silently wrong (crashes) outside the sample — demonstrated: `probe_memorizer.py` feeds the negated state to both predictors; raw-lookup → `RuntimeError` (KeyError), substring → `ok [True, False, False]`, matching the grader's own verdicts (§8 table). The honest reading generalizes; the memorizer doesn't — yet both pass V11 on the fixed 48.

## 9. Smallest safe correction (for the L1 / next counter version)

V11 should (1) hold out the 48 states' verdicts as a *non-deterministic* oracle (randomized/rotating seed per run, or multiple seeds), so a table cannot be stable across runs; (2) reject predictor blocks whose source contains a mapping keyed on state content/hash without any constant-substring check (a token/source lint — e.g. flag `TABLE =`/`dict` literals ≥48 entries keyed by long strings, or `hashlib.sha256(text...)`); (3) draw states from a wider behaviour space (sign-flip, whitespace-only, unreadable, dir-as-file, huge, binary) and (4) hide the `at=` disagreement labels behind a debug flag so the diagnostic stops being a tuning oracle. Any one of (1)+(4) removes the demonstrated bypass; (2)+(3) close the generalization gap.

## 10. Files

- Report: `.ufo/waves/round-44/wave/R44CritV11.md` (this file).
- Scratch `/fast/scratch/hyaku/kengaku-r44/R44CritV11` removed at finish via `scratch_guard.py safe-rm` (see cleanup below).
- No lane file was written or modified; no corpus/plans tree was copied into the wave dir; no receipt file is retained.

Cleanup: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44CritV11 /fast/scratch/hyaku/kengaku-r44/R44CritV11`

VERDICT: v11-bypasses-4-of-7
