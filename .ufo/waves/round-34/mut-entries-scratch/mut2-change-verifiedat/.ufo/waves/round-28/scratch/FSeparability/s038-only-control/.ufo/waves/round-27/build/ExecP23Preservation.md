# ExecP23Preservation - round 27 P2/P3 preservation comparer (WRITER)

Base: lane observed at 11a7fc8c64dc5d634331be24ccf5936f84a11f03 (b5719440 is its ancestor).
Clone: /tmp/kengaku-r27-ExecP23Preservation, branch r27-ExecP23Preservation, commit 05bb9e4a88d86c781a84969a07565ffcf9b97f38, tree clean.

## Files written in clone
- plans/fixtures/r27/p23_preservation.py (189 lines) sha256 b41db4403f3aec0be5c1456b8a2f700de0c99a719fcf6dc19a177e8e58c971a7
- Scratch outside the clone only: /tmp/kengaku-r27-ExecP23Preservation-scratch/ (b5719440 export, mutN1..mutN3, v3-base.json).

## Pinned inputs
- v3 plans/state_check.py sha256 32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089: identical at b5719440:plans/state_check.py, 11a7fc8c and the lane working tree (sha256sum).
- Export: `git -C /tmp/kengaku-r27-ExecP23Preservation archive b5719440e5eee46c1886fddbdf7bdc1624829454 | tar -x -C /tmp/kengaku-r27-ExecP23Preservation-scratch/base-b5719440`, exit 0. Seed plans/fixtures/r25/shonen-seed.txt sha256 3962e6b8...0927 equals state_check SEED_FIXTURE_SHA256.

## Comparer contract (p23_preservation.py)
- Runs `state_check.py --json --root ROOT` for --old and --new (child env PYTHONDONTWRITEBYTECODE=1, cwd=ROOT, 900 s timeout).
- Keeps ids starting P2 or P3. Compares each record in full (id, source_line, check, observed, verdict) as canonical JSON with sorted keys. Keyed by id, duplicates by occurrence; the P2/P3 sequence order is compared too.
- Exit 0 IDENTICAL; 1 DIFFERENT (DIFF / ADDED / REMOVED / COUNT / ORDER lines plus unified diff); 2 NOT COMPARABLE (usage error, child exit not 0 or 1, no JSON, zero P2/P3 records on a side).
- Child exit 1 (mismatches found) is comparable: state_check still prints its full JSON.
- Deviation to note: non-comparable runs exit 2, not 1, following the lane's state_check exit convention, so a broken run never reads as IDENTICAL or DIFFERENT.

## Control (assigned): v3 vs v3 on b5719440 export
$ PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-ExecP23Preservation/plans/fixtures/r27/p23_preservation.py --old /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py --new /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/state_check.py --root /tmp/kengaku-r27-ExecP23Preservation-scratch/base-b5719440
  old and new: exit=0, P2=255 P3=43, summary assertions=278 match=270 mismatch=0 offline_unverifiable=3 out_of_population=20 superseded=5
  compared: ids=298 record_pairs=298 differences=0 order=same
  VERDICT: IDENTICAL - 298 old and 298 new P2/P3 records match on every field, in the same order
  exit=0
- Pinned variant (old = export copy, new = clone copy, same bytes, different paths): exit=0, IDENTICAL, 298 records. No record embeds the script location.
- Base inventory (v3): 298 P2/P3 records; verdicts MATCH 270, OFFLINE_UNVERIFIABLE 3, OUT_OF_POPULATION 20, SUPERSEDED 5, MISMATCH 0; no duplicate ids.

## Negative controls (scratch mutants of v3, root = export; all exit 1 as required)
- N1: check-text edit on P3e.row-to-file.lessons/round-25.md plus id rename P3d.axis-table.round24. Output: REMOVED, ADDED, DIFF on `check` with verdict MATCH unchanged, ORDER. differences=4, exit=1.
- N2: check_p3 moved before check_readme_index (state_check.py:1815/1819). Output: ORDER only, keyed content identical. differences=1, exit=1.
- N3: P3d.axis-table.round25 appended twice. Output: COUNT old=1 new=2 plus ORDER. differences=2, exit=1.
- U1: --root pointing at a missing directory: exit=2 (USAGE).
- U2: --new pointing at a JSON file: exit=2 (no JSON document).
- Not exercised: DIFF with duplicate ids on both sides (#occurrence label; same DIFF branch), and the zero-P2/P3 guard (unreachable with v3, whose every record is P2 or P3).

## Reuse with v4 (round 27)
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/kengaku-r27-ExecP23Preservation/plans/fixtures/r27/p23_preservation.py --old /tmp/kengaku-r27-ExecP23Preservation-scratch/base-b5719440/plans/state_check.py --new <v4 plans/state_check.py> --root /tmp/kengaku-r27-ExecP23Preservation-scratch/base-b5719440
Expect exit 0 IDENTICAL, P2=255 P3=43, compared ids=298, provided v4 adds only P4* ids. Pin --old to the export copy: the lane file changes once v4 lands. If /tmp was cleared, recreate the export with the git archive command above.

## Notes for integrator
- The base P2/P3 population is 298 records. v4 must keep these ids and field values unchanged (no re-scoping).
- Key order inside a record is not compared; the field set and values are.

Installs: none. Python 3.14.8, git, tar, awk and sha256sum were already present; no pacman transactions.
Sources: none.
VERDICT: comparer committed at 05bb9e4 reproduces IDENTICAL on the b5719440 control (298 records); negative and usage controls exit as specified; v4 reuse command recorded.
