# RemintChessEigenR80 independent receipt replay

Axes: coverage (R80-C1); calibration (historical divergence disclosure). No predicate, target, control or kill-rule changes.

Freeze: `af51132d8919cedd14d3d3407ae5abc966d5d427`.
Measured master: `6669fe72e59718acc1a0f32a92849a544b0b2f1c` (advanced from freeze).

```text
$ git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane
Cloning into '/fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane'...
done.
[exit 0]

$ git -C /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane
[exit 0]

$ git -C /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane checkout --detach 6669fe72e59718acc1a0f32a92849a544b0b2f1c
HEAD is now at 6669fe72 round-80: integration — six located replays minted and the ledger flipped (R80-C1), V1-V6 routed rows plus the V1 receipt and corrections (R80-C2), S258, lesson, index, wave spec/dispatch
[exit 0]

$ git -C /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane status --porcelain
[exit 0]

```
Clean shared clone pinned to measured tip; all work and instrument receipt paths are seat-owned scratch.

## chess-best-move
```text
$ /usr/bin/python3 plans/round55_c3_chess_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/chess-best-move.work --receipt /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/chess-best-move.out.txt
CASE both-lowercase-two-lines predicted=P observed=P rc=0
CASE both-space-separated predicted=P observed=P rc=0
CASE reversed-order predicted=P observed=P rc=0
CASE single-move-only predicted=F observed=F rc=1
CASE uppercase-white predicted=F observed=F rc=1
CASE extra-decoy-move predicted=F observed=F rc=1
CASE duplicate-move predicted=F observed=F rc=1
CASE whitespace-padded predicted=P observed=P rc=0
CASE empty-file predicted=F observed=F rc=1
CASE crlf-line-endings predicted=P observed=P rc=0
CASE instruction-example-h1h8 predicted=F observed=F rc=1
CASE fullwidth-unicode-digit predicted=F observed=F rc=1
cases=12 observed_pass=5 observed_fail=7 mismatches=0
PREDICATE R55-C3 pass
[exit 0]

RECEIPT corpus/evidence/round80/chess-best-move-probe.txt
SOURCE_SHA recomputed=de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca stamped=de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca
TOOL_SHA recomputed=7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60 stamped=7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60
LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235 ancestry_to=6669fe72e59718acc1a0f32a92849a544b0b2f1c merge-base_exit=0
MINTED_BY plans/round80_c1_remint.py
EXACTLY_ONE subject_members=['chess-best-move'] MEMBER_lines=['MEMBER chess-best-move']
OBSERVATIONS receipt=14 fresh=14 ordered_equal=True
HISTORICAL observation_lines=14 receipt_observation_lines=14 same=True
CHECK subject_shape=True
CHECK exactly_one_subject_member=True
CHECK exactly_one_MEMBER_stamp=True
CHECK SOURCE_RECEIPT=True
CHECK SOURCE_SHA=True
CHECK TOOL=True
CHECK TOOL_SHA=True
CHECK LANE_TIP_ancestor=True
CHECK WORKTREE_stamp=True
CHECK EXIT_stamp_matches_fresh=True
CHECK MINTED_BY=True
CHECK tracked_artifacts=True
CHECK fresh_stdout_ordered_equals_block=True
CHECK COMMAND_frozen_argv=True
```

## largest-eigenval
```text
$ /usr/bin/python3 plans/round57_c2_eigen_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/largest-eigenval.work --receipt /fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/largest-eigenval.out.txt
CASE eig-sleep-pair-s2 predicted=P observed=P rc=0
CASE eig-bare-pair-s2 predicted=P observed=P rc=0
CASE zero-e1-pair-s2 predicted=F observed=F rc=1
CASE eig-sleep-pair-s5 predicted=P observed=P rc=0
CASE eig-bare-pair-s5 predicted=P observed=P rc=0
CASE zero-e1-pair-s5 predicted=F observed=F rc=1
CASE eig-sleep-pair-s10 predicted=P observed=P rc=0
CASE eig-bare-pair-s10 predicted=P observed=P rc=0
CASE zero-e1-pair-s10 predicted=F observed=F rc=1
CASE eig-sleep-dom-s2 predicted=P observed=P rc=0
CASE eig-bare-dom-s2 predicted=P observed=P rc=0
CASE zero-e1-dom-s2 predicted=F observed=F rc=1
CASE eig-sleep-dom-s5 predicted=P observed=P rc=0
CASE eig-bare-dom-s5 predicted=P observed=P rc=0
CASE zero-e1-dom-s5 predicted=F observed=F rc=1
CASE eig-sleep-dom-s10 predicted=P observed=P rc=0
CASE eig-bare-dom-s10 predicted=P observed=P rc=0
CASE zero-e1-dom-s10 predicted=F observed=F rc=1
CASE eig-sleep-speed-s2 predicted=F observed=F rc=1
CASE eig-bare-speed-s2 predicted=U observed=F rc=1 (observed-only)
CASE zero-e1-speed-s2 predicted=P observed=P rc=0
CASE eig-sleep-speed-s10 predicted=F observed=F rc=1
CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
CASE zero-e1-speed-s10 predicted=P observed=P rc=0
cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
PREDICATE R57-C2 pass
[exit 0]

RECEIPT corpus/evidence/round80/largest-eigenval-probe.txt
SOURCE_SHA recomputed=463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784 stamped=463877700639fcf7a522b207cbf88a3a6eebd2aa40d6afd5e1c258087ce8c784
TOOL_SHA recomputed=4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105 stamped=4f2b8bebb451c5f67d26dc06c76dbd99f3a459f41d9e8a8d555af12d15e0f105
LANE_TIP 6250e94b2adaff8cd22d32f7ab45024f092e3235 ancestry_to=6669fe72e59718acc1a0f32a92849a544b0b2f1c merge-base_exit=0
MINTED_BY plans/round80_c1_remint.py
EXACTLY_ONE subject_members=['largest-eigenval'] MEMBER_lines=['MEMBER largest-eigenval']
OBSERVATIONS receipt=27 fresh=27 ordered_equal=False
HISTORICAL observation_lines=27 receipt_observation_lines=27 same=False
HISTORICAL-DIFF observation_line=23
 historical: CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
 receipt:    CASE eig-bare-speed-s10 predicted=U observed=F rc=1 (observed-only)
HISTORICAL-DIFF observation_line=25
 historical: cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
 receipt:    cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0
HISTORICAL-DIFF observation_line=26
 historical: OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
 receipt:    OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F
REPLAY-MISMATCH block_line=23
 receipt: CASE eig-bare-speed-s10 predicted=U observed=F rc=1 (observed-only)
 fresh:   CASE eig-bare-speed-s10 predicted=U observed=P rc=0 (observed-only)
REPLAY-MISMATCH block_line=25
 receipt: cases=24 observed_pass=14 observed_fail=10 mismatches=0 setup=0
 fresh:   cases=24 observed_pass=15 observed_fail=9 mismatches=0 setup=0
REPLAY-MISMATCH block_line=26
 receipt: OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=F
 fresh:   OBSERVED-U eig-bare-speed-s2=F eig-bare-speed-s10=P
CHECK subject_shape=True
CHECK exactly_one_subject_member=True
CHECK exactly_one_MEMBER_stamp=True
CHECK SOURCE_RECEIPT=True
CHECK SOURCE_SHA=True
CHECK TOOL=True
CHECK TOOL_SHA=True
CHECK LANE_TIP_ancestor=True
CHECK WORKTREE_stamp=True
CHECK EXIT_stamp_matches_fresh=True
CHECK MINTED_BY=True
CHECK tracked_artifacts=True
CHECK fresh_stdout_ordered_equals_block=False
CHECK COMMAND_frozen_argv=True
HISTORICAL-DIVERGENCE 6 the tip's instrument produces 27 observation lines where the historical receipt has 27; historical receipt kept, sha stamped
```

## Scope and limits
Both independent replay/stamp checks pass: False. Historical comparison is separate from replay comparison; differences above are not silently treated as historical equality.
WORKTREE clean is the committed mint-time assertion; this measurement establishes clone cleanliness and matching stamped bytes/ancestry, not an independently recoverable historical porcelain listing. MINTED_BY identifies the tracked driver and its rendered stamp logic; the stamp alone cannot authenticate which process originally wrote the file.
No LSP tool is exposed in this seat; source inspection used file reads. No code refactor was required. No tools installed or upgraded. No global gates, build, lint, formatters, selftests or mutations run. Only explicitly assigned instruments executed.
Files changed: this advisory report only. Scratch clone and measurement script removed by EXIT trap after report creation.

## Finding and retained evidence
FAIL: largest-eigenval violates the frozen ordered stdout equality requirement at measured tip `6669fe72e59718acc1a0f32a92849a544b0b2f1c`. Its instrument exits 0 and prints its own predicate pass, but receipt block lines 23, 25 and 26 differ from the independently observed stdout above. The U timing case at size 10 flips F→P, changing both aggregates. The instrument explicitly describes U as host-noise-dependent; this is a reproducibility risk, not grounds to weaken the frozen predicate. No retries were used to seek matching output.

PASS: chess-best-move independently reproduces all 14 block lines, and matches all 14 historical observation lines. Both members pass stamp/hash/ancestry/member-uniqueness checks. Eigen's historical divergence is disclosed; three differing historical positions correspond to the receipt's symmetric-difference count of six.

Exact retained evidence is the complete stdout, exit codes, differing ordered positions, recomputed sha256 values and measured revisions in this report. Comparison implementation used `hashlib.sha256(path.read_bytes()).hexdigest()`, `git -C <clone> merge-base --is-ancestor <LANE_TIP> <measured-tip>`, `git -C <clone> ls-files --error-unmatch <receipt> <historical> <tool> <MINTED_BY>`, and ordered Python list equality after excluding only `^REV [0-9a-f]{7,40}\s*$`. Historical lists independently selected the frozen observation prefixes. Clone cwd for both printed instrument commands was `/fast/scratch/hyaku/kengaku-r80/RemintChessEigenR80/lane`.

Parent action: integrate this measured failure without reopening the frozen requirement; parent owns any full counter/gate execution. No implementation change is authorized for this seat. No blocker prevented measurement.
