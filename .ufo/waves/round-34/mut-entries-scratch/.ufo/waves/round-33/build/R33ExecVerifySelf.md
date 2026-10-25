# R33ExecVerifySelf — selftest battery receipts (round 33, hyaku run 7)

Seat: selftest/receipts leaf. Writes: `.ufo/waves/round-33/build/receipts/selftests.txt` and this report only.
No production edits, no corpus/SOURCES.md / README / SCORECARD / lesson / fleet-report bytes drafted.
No tool installs (nothing was missing: `bash`, `git`, `sha256sum`, `python3` 3.14.8 already on host).
Access date: 2026-10-25. Scratch: `/tmp/r33-R33ExecVerifySelf/` (two copies of a lane script, no clone).

Tree observed: lane HEAD `7895588` (`78955888542258ba369f5aa72c200c913b4c3c90`, "round-33: C2 routed-defect
repairs …"), i.e. one commit past the assignment's stated freeze tip `c227e486` — the L1 landed the C2 repair
commit mid-wave. Five tracked files were modified and the round-33 wave tree untracked when the battery ran
(sibling seats in flight). Battery window: 14:24:22–14:24:26 -0300.

## Deliverable

`.ufo/waves/round-33/build/receipts/selftests.txt` — 218 lines, sha256
`cd65a639bd862bf1401f9c3e46be2dcaea45b9d55c0ec69f84f63f51bae761e7`, last line `VERDICT: selftests-run`.
It holds, per command: the command line, sha256 of the script **before** and **after** the run, the raw
combined stdout+stderr, and the exit code captured by the wrapper shell.

| # | command (lane cwd) | exit | observed |
|---|---|---|---|
| 1 | `python3 plans/round33_defects.py --selftest` | **0** | `SELFTEST checks=14 failed=0` |
| 2 | `python3 plans/round33_c1_verify.py --selftest` | **0** | `SELFTEST checks=8 failed=0` |
| 3 | `python3 plans/catalog_probe.py --selftest` | **0** | `SELFTEST checks=13 failed=0` |
| 4 | `python3 plans/adoption_check.py --help` | **0** | argparse usage + 3 options (see below) |
| 5 | `python3 plans/round32_c1_verify.py --selftest` | **0** | `SELFTEST checks=6 failed=0` |
| 6 | `python3 plans/round31_c1_verify.py --selftest` | **0** | `SELFTEST checks=6 failed=0` |
| 7 | `python3 plans/round32_defects.py --selftest` | **0** | `SELFTEST checks=7 failed=0` |
| 8 | `python3 plans/round31_defects.py --selftest` | **0** | `SELFTEST checks=10 failed=0` |

8/8 exit 0; 64 selftest cases, 0 failed; no script byte changed during any run
(`sha256(pre) == sha256(post)` in all eight blocks).

`adoption_check.py` carries **no** `--selftest` (`grep -c -- '--selftest' plans/adoption_check.py` → `0`), which
is why the task prescribed `--help`; the argparse surface is present and complete (verbatim from the receipt):

```
usage: adoption_check.py [-h] [--lane LANE] --expect EXPECT [--census]

Re-derive an adoption round's landed state from committed bytes.

options:
  -h, --help       show this help message and exit
  --lane LANE
  --expect EXPECT
  --census
```

## Script identity binding (per-block digests)

| script | sha256 at run time | vs HEAD `7895588` |
|---|---|---|
| `plans/round33_defects.py` | `6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6` | identical |
| `plans/round33_c1_verify.py` | `b04716c4571206366d606774547af90f9e793658e089ddd495d0843d579543ca` | **differs** (HEAD `f38b9d0f504a…`) |
| `plans/catalog_probe.py` | `8cdd2436452de8301ae1cf451eb81cd94d059b2b7a8f19e65434a7a2662ab360` | identical |
| `plans/adoption_check.py` | `f9f8188efb3612c1a1a9d7a3e2272255096b76bd3100d3dacdded63dd7d69926` | identical |
| `plans/round32_c1_verify.py` | `b348dc967a815e21734122dc968a64dcc93e74ea711382a9f04dd3242dfc225f` | identical |
| `plans/round31_c1_verify.py` | `5ca535d3a51fd58d508c097715604558cd6bde116ba6ee50f2a201e4813b40ba` | identical |
| `plans/round32_defects.py` | `064289153d4b49431e135a2f8275affab2e845e25cde91ae45365f98ebdcdf06` | identical |
| `plans/round31_defects.py` | `13813eae9b67db9fcd836811e64cf857e5371427815acaa0c887f7f361053026` | identical |

The battery therefore covers the committed bytes for seven of eight commands.

### The one committed-vs-worktree delta (r33 C1 verifier)

`git diff --numstat -- plans/round33_c1_verify.py` → `6 3` (2 hunks) is a sibling C1-seat edit:
`check_v2` now falls back to registry column 1 when column 0 carries no URL, and `check_v8` reads
`supersedes <id>` from the **source** cell plus requires a refusal word in the teaches cell. Because the exit
code above belongs to worktree bytes, I ran the committed bytes beside them:

```
$ git show HEAD:plans/round33_c1_verify.py > /tmp/r33-R33ExecVerifySelf/r33_c1_verify.HEAD.py   # sha256 f38b9d0f504a4977…
$ python3 /tmp/r33-R33ExecVerifySelf/r33_c1_verify.HEAD.py --selftest
CASE registry-complete PASS
CASE V1-red-on-empty PASS … CASE V8-red-on-empty PASS
SELFTEST checks=8 failed=0
exit: 0
```

Both variants pass. The delta changes live check semantics, not selftest outcome.

## Drift after the battery

`plans/catalog_probe.py` was rewritten by a sibling seat **after** block [3/8] (mtime 14:25:11, worktree
`8ff9ec059e5d…`, HEAD still `8cdd2436…`). To keep the receipt usable I checked the drifted bytes without
touching the lane: `compile(...)` → `compiles=ok`; `--selftest` → `SELFTEST checks=13 failed=0`, exit 0.
Repeated runs changed nothing on disk. This is recorded in the receipt's `POST-RUN DRIFT` block.

## What these receipts prove — and what they do not

- **Proved now:** each counter's selftest machinery is present, importable, hermetic and green on this host at
  lane HEAD `7895588`; every case discriminates as labelled (red-on-empty cases redden, fixture-green cases
  green — e.g. `N3-red-unsuperseded` / `N3-green-superseded`, `N1-green-tracked` / `N1-red-untracked`,
  `verify-digest-tamper-red`). `plans/round33_defects.py` builds its green fixtures in a temp git repo, so a
  pass says nothing about the live `.ufo/waves/round-32/` tree, `SCORECARD.md`, or the fleet reports.
- **Not proved, by design:** selftest green ≠ closure. `round33_defects.py --selftest` prints
  `checks=14` (its **case** count, `len(cases)`), not the frozen six checks; the C2 counting command
  `--lane .` prints `checks=6 defects=N`. A reader who treats the selftest line as the C2 receipt would
  misread the claim. Same shape for `round33_c1_verify.py` (`checks=8` in the selftest is the V1–V8 case
  list; the live run prints `checks=8 defects=N` against the lane).
- **Q22 (`corpus/QUALITY.md:257`) binding:** these exit codes are claims about bytes at revision `7895588`
  plus the two uncommitted worktrees digested above. If the L1 commits different bytes for any of the eight
  scripts, the post-integration gate must re-run all eight at the final tip; a later edit that reddens a
  selftest is not covered here.

## Handoff / risks

1. Re-run this exact battery once the L1 commits the in-flight `plans/round33_c1_verify.py` and
   `plans/catalog_probe.py` edits, and commit the new output beside this file (Q22). The commands are the
   eight table rows above, in this lane cwd.
2. `catalog_probe.py --selftest` and `round33_defects.py --selftest` are offline/hermetic — no endpoint or
   network dependency, so a green here is not evidence that the C3 live probe succeeded.
3. `round33_defects.py --selftest` mutates only a `tempfile.TemporaryDirectory` repository
   (`git init`/`git add` inside it); it requires `git` on PATH. Verified present on this host.
4. No blockers. Nothing outside `.ufo/waves/round-33/build/` was written by this seat; `/home/vgpnk/Projects/shokuknow`
   and the fleet repo were not read for this item and not touched.
