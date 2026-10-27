# R46ExecLogAppendOnly — wave 1 report

## Deliverable

Draft tool: `.ufo/waves/round-46/w1/R46ExecLogAppendOnly/plans/log_appendonly.py` (stdlib-only; L1 integrates it as `plans/log_appendonly.py`). It scans reachable history with `git log --full-history`, diffs every log-touching commit against its first parent, reports all deleted/changed lines and one violation per commit, and exits 1 iff any violation exists. Pure additions pass. `--since REV` checks `REV..HEAD`, requiring REV to be an ancestor; `--show-lines`, `--verbose`, and `--selftest` are included. The checker is read-only; subprocesses inherit `TMPDIR`, and selftest creates its temporary repos there.

## Evidence

All runs below used the required envelope. Each retained receipt contains the full `ENVELOPE` command/start/end lines and `local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.

- **Lane history:** `receipt-lane.txt`; command `python3 <draft> --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --show-lines --verbose`; output `LOG-APPENDONLY commits=77 violations=7`, exit 1. Every reported violation:
  - `f147a2706961`: deleted old line 9 (1 line).
  - `28a2fbfb3e53`: deleted old lines 22–28 (7 lines).
  - `2f00932ddb52`: deleted old line 29 (1 line).
  - `96c9d8fd7d23`: deleted old lines 641 and 680 (2 lines).
  - `66c734c0a1e1`: deleted old lines 935–937 (3 lines).
  - `f660ae04a1c5`: deleted old lines 1374 and 1388 (2 lines).
  - `3d9ea54a558b`: deleted old lines 1407–1408 (2 lines; **includes the requested 3d9ea54**).

  Attribution detail: the closure's `git diff -U0 fbad1c5 3d9ea54 -- LOG.md` exposes the `:1374`/`:1388` rewrites, but the per-commit walk attributes those changes to the earlier `f660ae04`; `3d9ea54` itself rewrites the separate `:1407`/`:1408` tally. The lane receipt retains the deleted text for all seven commits. `--verbose` reports `full-history=77 simplified=76 ... full_only=323b392113e7`; the extra first-parent merge is a pure append, so it adds no violation.
- **Requested-round bound:** `receipt-since-fbad1c5.txt`; command `--since fbad1c5`; output `commits=2 violations=2`, exit 1, listing `f660ae04a1c5` and `3d9ea54a558b`. `receipt-since-r45base.txt` binds from `64ba8385...` and reports 0 log-touching commits/0 violations, exit 0.
- **Two-commit fixtures under scratch:** `receipt-fixture-build.txt` confirms both fixture repositories had 2 commits and their verified toplevels were under `$S`. `receipt-fixture-green.txt`: append-only fixture, `commits=2 violations=0`, exit 0. `receipt-fixture-red.txt`: edited-line fixture, `commits=2 violations=1`, exit 1.
- **Selftest:** `receipt-selftest.txt` reports `SELFTEST pass`: green, edit, deletion, move/reorder, `--since` ranges, and non-ancestor rejection all matched expected exit codes/counts.
- **Independent history cross-check:** `receipt-crosscheck.txt`; across all 77 full-history commits, old/new blob line-multiset comparison found no missed deletion commits (`missed_multiset_deletions=0`). Direct per-commit diffs confirmed deleted-line counts 1, 7, 1, 2, 3, 2, 2 for the seven listed commits.

Receipt and draft hashes (SHA-256): draft `e7dbaf7b0915f6299151adb16d12500bd8754635afc24ad717d11367a0f91067`; lane `a679ec67922ad8781191488b69765d193652955a721067e55365c57e584e5da1`; selftest `f1bb37083dfcd24f1c95801f38c593f8cc3ead0d7a06330bcfdf462e6204cb84`; fixture-build `fe5de7ed6d53f43866322e4cc455aa647926cab1f549958e96172e74e9344695`; green `8acb263f2eeed624381fd68048b0f9fd63af1dbb8628b76a7bc775f7614b1e65`; red `a369325a777a9468a33ea2c607fa04ab8869f1b340dc99b60f9c7dba80d859ed`; cross-check `14f12b33ceb2b2dc663e16890609671669db997ff5eecdace8fd077e82abd577`; since-base `6ceb3b4c79b0c25ed1ca4baaa965b5936e4ca4aea9797a3175831baaf43a69e0`; since-salvage `a7411ccb9105002eba8694430ca34041c8797a4ea35307412fdbc4329cbd2f7b`.

Scratch was removed using the required `scratch_guard.py safe-rm` command (`DELETE ... bytes=80523 size=78.6KiB`). No tools were installed. No lane implementation files were edited; this is a draft for L1 integration.

## Risks / limits

The checker sees commits reachable from HEAD; abandoned/unreachable branches are outside its scan. `--since` deliberately trusts the caller that earlier history is clean. Merge diffs use the first parent, with full-history traversal to avoid history-simplification omissions. Moves/reorders count as rewrites by design. No blockers.

VERDICT: log-appendonly-lane-violations-7-fixture-red-green-ok
