# R49C1MutNames — Q39 name-mutation probe

Axes: primary **calibration**; probe dimension **Q39 name independence** (fixture/module/build names and directory shape).

## Freeze and measured revision

Stage-1 freeze verified before measurement: `9d2900af41e4d1fc6022eff99010436fde6dbd93`, commit time `2026-10-28T09:14:40-03:00`; `git merge-base --is-ancestor ... master` returned success. It commits `plans/round-49-claims.md`. Probe timestamp: `2026-10-28T09:28:31-03:00`.

`REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` — clean scratch clone at frozen base. The stage-2 v3 counter/populations are not in that tree, so this is a bounded detector probe of the frozen fence with the committed round-48 v2 harness/round-46 contract; it is **not** a v3 scoring run or claim admission.

Source locations opened (local URLs), accessed 2026-10-28:
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-49-claims.md` — quote: “name-hiding (Q39) retained: per-run random tokens, padded parents, shuffled jobs” (12 words).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` — quote: “C1 kill-battery gap” (3 words).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-48.md` — quote: “A frozen requirement-tag set with no violating case makes a counter leg unsatisfiable” (13 words).

## Commands and detector

Exact setup/measurement commands:
```sh
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %cI %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 master
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r49/R49C1MutNames/clone
git -C /fast/scratch/hyaku/kengaku-r49/R49C1MutNames/clone checkout --detach 9d2900af41e4d1fc6022eff99010436fde6dbd93
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C1MutNames
python3 /fast/scratch/hyaku/kengaku-r49/R49C1MutNames/probe.py
```
The runner reused `round46_c1_verify.py`'s fixture builder and harness contract, invoked the fence under the same `strace` syscall trace set and read-only sandbox, and applied the same `k46.analyse` outside-touch classifier. It compared pristine, renamed, and restored copies with fixed RNG seed. Mutations: module file basenames changed to opaque names; fixture parents renamed to `shape_*`; repository child dirs renamed to `repo_*`; corresponding `--lane` arguments updated to preserve semantics. Sampled modules: honest `n13_remote_origin.py`, six honest fixtures from `battery42/a_class.py`, hostile `refusals46/f1_gitfile.py`.

## Paired outputs (verbatim detector lines)

```text
PAIR pristine 0 0 n13_remote_origin.py fid=n13-remote-origin tool=anchor verdict=BREACH touches=0 calls=446 reason=BREACH repo/.git/config section header b'[remote "origin"]' is not plain argv=["--lane", "repo"]
PAIR renamed 0 0 n13_remote_origin.py fid=n13-remote-origin tool=anchor verdict=BREACH touches=0 calls=446 reason=BREACH repo_0_0/.git/config section header b'[remote "origin"]' is not plain argv=["--lane", "repo_0_0"]
PAIR restored 0 0 n13_remote_origin.py fid=n13-remote-origin tool=anchor verdict=BREACH touches=0 calls=446 reason=BREACH repo/.git/config section header b'[remote "origin"]' is not plain argv=["--lane", "repo"]
PAIR pristine 1 0 a_class.py fid=a_class-x6-sibling-digest tool=anchor verdict=ADMIT touches=0 calls=538 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-pristine-1/fx/f59846171bd10ebc/f000/repo"]
PAIR renamed 1 0 a_class.py fid=a_class-x6-sibling-digest tool=anchor verdict=ADMIT touches=0 calls=538 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-renamed-1/fx/83d0be2c22338be0/shape_1_0/repo_1_0"]
PAIR restored 1 0 a_class.py fid=a_class-x6-sibling-digest tool=anchor verdict=ADMIT touches=0 calls=538 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-restored-1/fx/99ae244d64c0df4f/f000/repo"]
PAIR pristine 1 1 a_class.py fid=a_class-x6-stale-manifest tool=anchor verdict=ADMIT touches=0 calls=565 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-pristine-1/fx/f59846171bd10ebc/f001/repo"]
PAIR renamed 1 1 a_class.py fid=a_class-x6-stale-manifest tool=anchor verdict=ADMIT touches=0 calls=565 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-renamed-1/fx/83d0be2c22338be0/shape_1_1/repo_1_1"]
PAIR restored 1 1 a_class.py fid=a_class-x6-stale-manifest tool=anchor verdict=ADMIT touches=0 calls=565 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-restored-1/fx/99ae244d64c0df4f/f001/repo"]
PAIR pristine 1 2 a_class.py fid=a_class-x7-fabricated-token tool=anchor verdict=ADMIT touches=0 calls=527 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-pristine-1/fx/f59846171bd10ebc/f002/repo"]
PAIR renamed 1 2 a_class.py fid=a_class-x7-fabricated-token tool=anchor verdict=ADMIT touches=0 calls=527 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-renamed-1/fx/83d0be2c22338be0/shape_1_2/repo_1_2"]
PAIR restored 1 2 a_class.py fid=a_class-x7-fabricated-token tool=anchor verdict=ADMIT touches=0 calls=527 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-restored-1/fx/99ae244d64c0df4f/f002/repo"]
PAIR pristine 1 3 a_class.py fid=a_class-x7-provenance-row tool=anchor verdict=ADMIT touches=0 calls=544 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-pristine-1/fx/f59846171bd10ebc/f003/repo"]
PAIR renamed 1 3 a_class.py fid=a_class-x7-provenance-row tool=anchor verdict=ADMIT touches=0 calls=544 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-renamed-1/fx/83d0be2c22338be0/shape_1_3/repo_1_3"]
PAIR restored 1 3 a_class.py fid=a_class-x7-provenance-row tool=anchor verdict=ADMIT touches=0 calls=544 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-restored-1/fx/99ae244d64c0df4f/f003/repo"]
PAIR pristine 1 4 a_class.py fid=a_class-x14-uppercase-token tool=anchor verdict=ADMIT touches=0 calls=538 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-pristine-1/fx/f59846171bd10ebc/f004/repo"]
PAIR renamed 1 4 a_class.py fid=a_class-x14-uppercase-token tool=anchor verdict=ADMIT touches=0 calls=538 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-renamed-1/fx/83d0be2c22338be0/shape_1_4/repo_1_4"]
PAIR restored 1 4 a_class.py fid=a_class-x14-uppercase-token tool=anchor verdict=ADMIT touches=0 calls=538 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-restored-1/fx/99ae244d64c0df4f/f004/repo"]
PAIR pristine 1 5 a_class.py fid=a_class-x14-two-errata tool=anchor verdict=ADMIT touches=0 calls=566 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-pristine-1/fx/f59846171bd10ebc/f005/repo"]
PAIR renamed 1 5 a_class.py fid=a_class-x14-two-errata tool=anchor verdict=ADMIT touches=0 calls=566 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-renamed-1/fx/83d0be2c22338be0/shape_1_5/repo_1_5"]
PAIR restored 1 5 a_class.py fid=a_class-x14-two-errata tool=anchor verdict=ADMIT touches=0 calls=566 reason=ADMIT argv=["--lane", "/fast/scratch/hyaku/kengaku-r49/R49C1MutNames/work/run-restored-1/fx/99ae244d64c0df4f/f005/repo"]
PAIR pristine 2 0 f1_gitfile.py fid=f1-gitdir-outside tool=order verdict=BREACH touches=0 calls=430 reason=BREACH .git is a file (gitdir redirect), not a directory argv=["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md", "--receipt", "corpus/evidence/round42/receipt.txt"]
PAIR renamed 2 0 f1_gitfile.py fid=f1-gitdir-outside tool=order verdict=BREACH touches=0 calls=430 reason=BREACH .git is a file (gitdir redirect), not a directory argv=["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md", "--receipt", "corpus/evidence/round42/receipt.txt"]
PAIR restored 2 0 f1_gitfile.py fid=f1-gitdir-outside tool=order verdict=BREACH touches=0 calls=430 reason=BREACH .git is a file (gitdir redirect), not a directory argv=["--lane", ".", "--claims", ".ufo/waves/round-42/claims/round-42-claims.md", "--receipt", "corpus/evidence/round42/receipt.txt"]
```
Summary: six honest `a_class.py` fixtures are admitted with zero traced touches in all three legs; the hostile `.git`-file fixture is refused with zero touches in all legs. The honest remote-origin fixture is refused with zero touches in all legs (the base fence's known over-refusal, not a name-induced flip). No paired verdict changed. Mutant classifications: 7 name mutants survived (same outcome pristine/mutated/restored); `n13_remote_origin` is **inconclusive** for honest-admission validity because its pristine baseline already refuses, but its refusal also did not change under rename.

## Hashes and restoration

Measured clone files:
```text
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
 ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508  plans/round46_c1_verify.py
eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb  plans/battery42/a_class.py
34b2ca158cf3ce4d82484db06a065d88458064ae29fb4321e039d8a54e835d9d  round-48 honest n13_remote_origin.py
bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d  plans/refusals46/f1_gitfile.py
```
Restored-copy hashes exactly match their originals: n13 `34b2ca158cf3ce4d82484db06a065d88458064ae29fb4321e039d8a54e835d9d`; a_class `eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb`; f1 `bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d`. Renamed module copies were byte-identical; mutation was by path/shape only. Clone `git status --porcelain` count was `0`; HEAD remained the measured REV.

## Limits and verdict

Bounded sample only: one module per category, with six generated honest subfixtures; no full 120-fixture v3 population, no stage-2 v3 counter (absent at frozen base), no new stage-2 pins, and no claim scoring. Probe exercises counter builder + fence sandbox, not the v3 full counter CLI. The n13 baseline refusal remains a fence behavior defect already recorded for C1; this probe does not repair or attribute it to names.

**VERDICT: Q39 name-dependence not observed in this bounded probe; 7 surviving name mutations, n13 paired comparison inconclusive for admission because pristine baseline refuses. No claim admission asserted.**
