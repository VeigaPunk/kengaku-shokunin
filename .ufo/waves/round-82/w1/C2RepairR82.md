# C2RepairR82 — round 82 w1 executor: repaired bytes for R82-C2 V1, V4, V5, V7

Seat `C2RepairR82` (executor, leaf). 2026-11-04. Lane `kengaku-shokunin`.
Freeze commit / measured tip `12f1029a45cf0097a3afd030d757bf93b87f8018` (`git -C <lane> rev-parse master`,
measured this session). Base revision `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`. Scope: V1, V4, V5, V7 —
V2/V3/V6 belong to C2ProseR82 and were not touched.

**Method.** The shared lane worktree is dirty with sibling in-flight edits
(`git status --porcelain`: `M SKILL.md`, `M corpus/README.md`, `M corpus/SOURCES.md`,
`M corpus/knowledge/tb2-file-artifact-replay-classes.md`, `M corpus/lessons/round-81.md`;
untracked `.ufo/waves/round-82/`, `corpus/evidence/round82/census-before.txt`,
`corpus/evidence/round82/fetch/`, `corpus/knowledge/tb2-replay-sweep-at-one-tip.md`), so nothing was
minted from it. Every measurement below runs inside one `git clone --shared` of the lane at
`/fast/scratch/hyaku/kengaku-r82/C2RepairR82/clone` (HEAD `12f1029a…`, `git status --porcelain`
empty). The shared lane worktree was never cleaned, stashed or written. Tools installed: none.

## V1 — `corpus/evidence/round81/c2-after.txt` re-minted from a clean tree

```
$ cd $S/clone && python3 plans/round81_c2_spotcheck_debt.py --lane .
rc=0
UNIVERSE spotcheck=corpus/lessons/round-80-verifier-spotcheck.md ids=6 R80-U1,R80-U2,R80-U3,R80-U4,R80-U5,R80-U6
DEBT R80-U1 … check=present          (all six rows)
DEBT-TOTAL ids=6 registered=6 closed=6 checks_passed=6
INDEX corpus/lessons/round-80-verifier-spotcheck.md indexed=yes
DEFECTS n=0
TARGET ids=6 closed=6 checks_passed=6 indexed=yes
PREDICATE R81-C2 pass
```
(stderr empty.) Receipt assembled in the round-81 line order — stamp block first, then the counter
stdout verbatim: `# R81-C2 after` / `LANE_TIP 12f1029a45cf0097a3afd030d757bf93b87f8018` /
`WORKTREE clean` / `COMMAND python3 plans/round81_c2_spotcheck_debt.py --lane .` / `EXIT 0` /
`--- stdout ---` / stdout. Proof on the delivered file:
`grep -c '^WORKTREE clean'` = **1**, `grep -c '^WORKTREE dirty'` = **0**. 18 lines.
sha256 `f392c1f903584cff99f4703344ef5bd09076ebaa66fdb96877e16a6cdb1d8f1c`.

## V4 — mutant-docstring count now equals the battery's printed number

Diagnosis: `plans/round81_c2_spotcheck_debt.py:384` (mutants docstring) says "Six attributed data
mutations" while `MUTANTS` held 4 entries and the committed `corpus/evidence/round81/c2-mutants.txt`
prints `MUTANTS real=4 killed=4 survived=0`. Preferred fix applied: **added the two missing mutants**
as new entries of the existing families (both already proven killed by the counter's own selftest
cases `check-fails`/`close-no-evidence`); no predicate, check or CASES byte changed. Full diff of the
delivered file against the tip bytes (the only change):

```
379a380,381
>     ("check-made-failing", "CHECK-FAIL"),
>     ("close-sans-evidence", "CLOSE-NOT-EVIDENCE"),
400a403,406
>         elif name == "check-made-failing":
>             rows[0]["check"] = "grep -q 'absent marker' corpus/lessons/round-81.md"
>         elif name == "close-sans-evidence":
>             repair = FIXTURE_REPAIR.replace("R80-U1 correction: counted.", "nothing here.")
```

Proof, run from the delivered file itself in scratch:

```
$ python3 .ufo/waves/round-82/w1/repaired/plans/round81_c2_spotcheck_debt.py --mutants --work $S/mutwork
MUTANT drop-one-row expect=DEBT-UNREGISTERED observed=DEBT-UNREGISTERED killed
MUTANT close-names-spotcheck expect=CLOSE-NOT-REPAIR observed=CLOSE-NOT-REPAIR killed
MUTANT check-made-trivial expect=CHECK-TRIVIAL observed=CHECK-TRIVIAL killed
MUTANT status-reopened expect=TARGET observed=- killed
MUTANT check-made-failing expect=CHECK-FAIL observed=CHECK-FAIL killed
MUTANT close-sans-evidence expect=CLOSE-NOT-EVIDENCE observed=CHECK-FAIL,CLOSE-NOT-EVIDENCE killed
MUTANTS real=6 killed=6 survived=0        (rc=0)
$ … --selftest --work $S/mutwork
SELFTEST cases=9 red=8 failures=0         (rc=0)
```

The docstring still says "Six" — now true. sha256 `680eb0d742e518df22270b579e83f6f34edcd41c40cfae82f2bfc71ff08da7b8`.

## V5 — stray `--lane/` confirmed empty + untracked; rmdir command delivered

Measured at the lane (read-only):

```
$ ls -ld -- '<lane>/--lane'
drwxr-xr-x 1 vgpnk vgpnk 0 Nov  4 01:58 /home/vgpnk/Projects/shokunin/kengaku-shokunin/--lane
$ find '<lane>/--lane' -mindepth 1 | wc -l
0
$ git -C '<lane>' ls-files -- '--lane'
(no output → untracked; `git status --porcelain` never lists it because it is empty)
```

Matches the round-81 spot-check C-D6 (mtime 01:58). Directory is **empty**, so removal is safe; this
seat did not delete it — `repaired/rmdir-command.txt` carries the exact L1 command
`rmdir -- '/home/vgpnk/Projects/shokunin/kengaku-shokunin/--lane'` plus the BEFORE listing above and
the AFTER listing clearly labeled *expected* (the L1 executes the removal).
sha256 `46ee14d555daaf93c557913f36203f4e1bf582ae040636018251976f7922e81f`.

## V7 — determinism.txt now carries producing COMMAND + REV, re-derived

The committed receipt (313 bytes, 3 lines) recorded `sha256=43a8c27622db358d` /
`sha256=8d3471f9f6238c63` with no command or revision. Two-stage hunt, both instruments run for real
at every candidate rev in a clean clone (bwrap sandbox, rc=0 each run):

1. REV-line substitution over all 570 ancestors of `f70fe5fa` against the final probe body: **no
   match** (the probes' bytes changed mid-round, so that model was invalid — reported as a negative
   result, not smoothed).
2. Real runs at each of the 12 revs from the probes' introduction (`4ac8471b`) to the determinism
   commit (`4fe5ebea`): **both legacy hashes reproduce exactly at
   `f6d5b8649bbc5ecd71d52f463d52eb1b103a183d`** ("real-tree control … process slip", 05:39:29 — the
   tip when the determinism receipt was written, one commit before it landed):

```
$ git checkout -q --detach f6d5b8649bbc5ecd71d52f463d52eb1b103a183d
$ python3 plans/round81_log_summary_probe.py --lane . --work work/ls        # rc=0
  sha256 stdout = 43a8c27622db358dea5d807f14ee33f2c57585788b3426217e6326c9d544e87d
$ python3 plans/round81_vulnerable_secret_probe.py --lane . --work work/vs  # rc=0
  sha256 stdout = 8d3471f9f6238c6355c0005599edea9d7d3b4d5d1e46b87d5cdb15e6314c6454
```
   (prefixes = the legacy 16-hex values; `--work` does not affect stdout.)

Delivered `corpus/evidence/round81/determinism.txt`: the original 313 bytes **untouched**
(`cmp` of the 313-byte prefix against `git show master:…` → identical), then appended: the two
producing `COMMAND` lines, `REV f6d5b8649bbc5ecd71d52f463d52eb1b103a183d`, a derivation note
(sha256 = first 16 hex of stdout), and the fresh tip re-run:

```
plans/round81_log_summary_probe.py run1 rc=0 sha256=46c7acf5df80dc8a run2 rc=0 sha256=46c7acf5df80dc8a identical
plans/round81_vulnerable_secret_probe.py run1 rc=0 sha256=fbf05e246592558c run2 rc=0 sha256=fbf05e246592558c identical
```
(both probes run twice at master `12f1029a…`, rc=0, byte-identical pairs). sha256
`ea7c2c04482b27ce2902bfb4bb3eb6976ee4ddfd5fd21bbed8582299e26761d1`.

## Deliverables (`.ufo/waves/round-82/w1/repaired/`, same relative paths as in-lane)

Listed in `MANIFEST` (`<sha256>  <path>`, repo-relative):

- `f392c1f9…` `corpus/evidence/round81/c2-after.txt` (V1)
- `ea7c2c04…` `corpus/evidence/round81/determinism.txt` (V7)
- `680eb0d7…` `plans/round81_c2_spotcheck_debt.py` (V4)
- `46ee14d5…` `rmdir-command.txt` (V5)

## Notes and risks for the L1

- The V1 receipt's `LANE_TIP` is `12f1029a…`, the lane tip at measurement. If master moves before
  integration, either re-mint (one counter run in a clean clone) or accept per the claim wording
  ("current lane tip").
- The committed `corpus/evidence/round81/c2-mutants.txt` still prints `real=4`; the delivered counter
  prints `real=6`. The L1 should re-mint that receipt alongside the counter (not a seat deliverable).
- The legacy determinism hashes are reproducible **only at `f6d5b864…`** — the probes' bytes changed
  between that rev and `4fe5ebea` (ls stdout hashes `43a8c276…` vs `8d3136bc…` at those revs, both
  measured). The appended REV line encodes this; the round's u7 check should run the COMMANDs at that
  REV, not at the tip, for the legacy pair, and at the tip for the R82 pair.
- V2 (SOURCES/lesson miscounts), V3 (provenance trio), V6 (wave composition) not touched — other seat.
- A ConnectorR82 finding about V2/S260-S261 was acknowledged and redirected (not this seat's item);
  its V1 warning (dirty shared worktree) was heeded — everything minted from the clean shared clone.
- Scratch `/fast/scratch/hyaku/kengaku-r82/C2RepairR82/` deleted before this report's yield. No
  fixture repos were needed (no commits made anywhere).
