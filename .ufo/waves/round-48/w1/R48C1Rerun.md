# R48C1Rerun — independent C1 rerun

**Axis:** calibration (R48-C1).  
**VERDICT:** BLOCKED — no scored counter execution performed. The stage-1 contract is committed, but the required stage-2 freeze artifacts are absent. Running the round-46 counter or an improvised v3 counter would not be the frozen v3 measurement this item requires.

## Freeze and measured revision

The exact frozen base is `a543d92083557dd9b33ee674e9b99b03411f80af` (`2026-10-27T06:53:29-03:00`). It contains the C1 stage-1 contract, but not `plans/round48_c1_verify.py`; the claims receipt directory has only `README.txt` and `freshness-r48.txt`. Thus there is no committed v3 counter, stage-2 input pins/population/literals, or before-control receipt to establish that a measurement would be governed by the complete freeze. No candidate fence was scored. No `REV` measurement receipt exists because no counter ran.

Observed prerequisite check (verbatim):

```text
REV=a543d92083557dd9b33ee674e9b99b03411f80af
STAGE1_COMMIT=2026-10-27T06:53:29-03:00 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
MISSING plans/round48_c1_verify.py
EXISTS .ufo/waves/round-48/claims
.ufo/waves/round-48/claims/README.txt
.ufo/waves/round-48/claims/freshness-r48.txt
BASE_FENCE=a2b128ae007bf47d3aefdeda6321ae118c7e5958
BASE_COUNTER=415b40705749b5d3bada6929b34970acf0693d1c
C1_STAGE2_ARTIFACTS=
```

The stage-1 contract says stage 2 freezes counter files, input pins, fixture populations, literals, and before-control receipts; it explicitly places the base-fence control measurement at stage 2. Consequently, there are no honest fields, exit code, or predicate line to report. I did not substitute `plans/round46_c1_verify.py` or construct an unpinned counter, and did not score any candidate fence variant.

## Commands run

- `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1Rerun && export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1Rerun && echo "TMPDIR=$TMPDIR" && df -h /fast/scratch | tail -1`
  - Output: `TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1Rerun`; `/dev/nvme1n1p2 804G 372G 432G 47% /fast`.
- `cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git log --oneline -8 && git status --porcelain && git rev-parse HEAD`
  - Tip observed: `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; pre-existing untracked paths included `.ufo/waves/round-48/claims/`, `.ufo/waves/round-48/w1.ready.partial`, `.ufo/waves/round-48/w1/`, and `corpus/lessons/round-48.md`.
- `git cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af` and `git show --stat --oneline a543d92083557dd9b33ee674e9b99b03411f80af`
  - Output: `commit`; only `plans/round-48-claims.md` added.
- `git diff --stat 0f77f9b a543d920 -- plans/fixture_fence.py plans/round46_c1_verify.py`
  - Output: `(empty diff = fence unchanged at freeze)`.
- `wc -l plans/round46_c1_verify.py plans/fixture_fence.py && sha256sum plans/round46_c1_verify.py plans/fixture_fence.py && git log -1 --format='%H' -- plans/round46_c1_verify.py`
  - Output: 635 and 575 lines; SHA-256 values `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508` and `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`; round-46 counter commit `cf7de6af112e5d491ebd47318682b05fe864c125`.
- The prerequisite check shown above, against `a543d920`, confirmed the stage-2 C1 counter and artifacts are not present.

No counter/probe command was run; therefore there are no output fields, exit status, or predicate line. No tool was installed or updated.

## Sources opened

Access date: 2026-10-27. These are local committed sources (file URLs); no external source was opened.

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — quote: “Stage 2 (one amendment commit, after wave 1 returns and BEFORE any claimed work is scored)” (C1 freeze prerequisite and C1 counter/predicate sections, lines 20–68; stage-1 revision `a543d92083557dd9b33ee674e9b99b03411f80af`).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — quote: “9/9 novel honest controls refused” (round-46 routed C1 defect evidence; opened for the required assignment context).

## Limits

This is a freeze-prerequisite review, not a counter rerun: the v3 executable and stage-2 pins/population/literals are absent at the committed frozen base. Candidate variants were not scored, and no admission judgment is made. Required next prerequisite is the committed stage-2 freeze; after it exists, rerun the pinned counter on the specified base/control and candidate variants under the frozen contract.
