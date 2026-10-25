# RevBaseReceipts — round-27 start receipts, read-only re-run

Receipt: corpus/evidence/round27-calibration/round-start.txt (sha256 b5438ead7c7a88eabf6bab69f68c7abdf401b8d13b8fe9afa552cc659cdb9062)
Scope: all 9 receipt commands re-run read-only; header timestamp excluded; untracked count 1 vs 1 (no drift).
Raw re-run text: /tmp/kengaku-r27-revb/rerun.txt. Lane at re-run: master 11a7fc8c64dc5d634331be24ccf5936f84a11f03 (receipt base b5719440e5eee46c1886fddbdf7bdc1624829454).

| # | receipt command | result |
|---|---|---|
| 1 | jj-lane.sh state | DIFF, HEAD only (D1) |
| 2 | git rev-parse master | DIFF, HEAD only (D1) |
| 3 | sources-census.sh validate --root … kengaku | identical; exit 0 |
| 4 | sh plans/round26_census.sh | DIFF, `head=` token only (D1); other 21 lines identical; exit 0 |
| 5 | git cat-file -e master:plans/parser_policy_compare.py | identical; exit 128 |
| 6 | state_check.py --summary \| head -1 | values identical; receipt exit/stderr not reproducible (D2) |
| 7 | python3 grader.py \| tail -1 | values identical; label mismatch (D3) |
| 8 | ls corpus/lessons/operator-* | identical; exit 2 |
| 9 | ls corpus/lessons/round-26-verifier-spotcheck.md | identical; exit 2 |

## Differences

D1 (blocks 1, 2, 4): receipt b5719440… / b571944 → now 11a7fc8c… / 11a7fc8.
- Cause (observed): lane advanced by 2 commits. `git --no-optional-locks rev-list --count b5719440..11a7fc8` = 2. Log: 11a7fc8 "round-27: pre-registration … + round-start receipts"; ec36f37 "considerthese: 2026-10-21 daily shokunin reflection".
- `git diff --stat b5719440 11a7fc8`: considerthese/2026-10-21.md +86; plans/round-27-claims.md +153; corpus/evidence/round27-calibration/round-start.txt +48.
- [INFERENCE] none of the three paths is an input of the census, state_check, or grader lines; consistent with all value lines being unchanged.

D2 (block 6, receipt lines 37–40): values identical. First line `assertions=278 match=270 mismatch=0 superseded=5 offline_unverifiable=3`; OUT_OF_POPULATION lines = 21 (prefix and substring counts agree).
- The receipt's `exit=0` is `head`'s status. Under this pipeline state_check raises BrokenPipeError: 11-line traceback (plans/state_check.py:2553 `sys.exit(main())`, :2545 `print_summary`, :1852 `print`) and exits 1. PIPESTATUS=1 in 5/5 runs.
- Standalone `python3 plans/state_check.py --summary >/dev/null 2>…`: exit 0, stderr 0 bytes.
- Receipt has no traceback. [INFERENCE] stderr was dropped at capture.

D3 (block 7, receipt lines 41–43): labeled `… | tail -1`, but the receipt lists two lines.
- The labeled command prints only `VERDICT: PASS — stored evidence fully re-derives offline`.
- `CHECKS n=733 mismatches=0 errata_pinned=1` is the penultimate line; `| tail -2` reproduces both.
- Full run `python3 grader.py`: exit 0 (not recorded in the receipt).

## Provenance notes (no value drift)
- Bare `jj-lane.sh` is not on PATH (exit 127). Re-run used scripts/hyaku/jj-lane.sh with `<lane-dir>`; bare `state` gives usage, exit 64. `sources-census.sh` run via /home/vgpnk/Projects/shokunin/scripts/.
- untracked=1 is directory-collapsed: `git --no-optional-locks status --porcelain` → `?? .ufo/waves/round-27/` (exit 0). This count cannot move as wave files accrete, so it is a weak drift detector. Use file-level listing (`git ls-files --others --exclude-standard`) for future receipts.
- scripts/hyaku/jj-lane.sh:179 runs plain `git status --porcelain` (no --no-optional-locks), so `state` can opportunistically refresh .git/index. Its header says "pure git, read-only" (:156). Ran once here; tracked=0 before and after.
- The write-grep hit grader.py:4265 `open(…,"w")` sits inside the `SYNTH_PROBE_SRC` fixture string (grader.py:4255–4335), not import-time code. No IMPORT-SIDE-EFFECT.txt exists in the lane.
- Every python invocation used PYTHONDONTWRITEBYTECODE=1. No new untracked entries after the re-run beyond the existing .ufo/waves/round-27/ directory.

## Installs
None.

## Writes
- This file only: .ufo/waves/round-27/build/RevBaseReceipts.md. Scratch only in /tmp/kengaku-r27-revb/.

VERDICT: 9 receipt blocks re-run: 4 identical; 3 differ only by HEAD (lane advanced to 11a7fc8c via 2 commits); 2 not reproducible verbatim (state_check pipe exit and traceback; grader tail label) with identical values. No value drift.
