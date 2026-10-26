# R43ScoutMisroot — host-safety and hygiene watch (kengaku r43 wave 1)

Read-only watch. Written nothing except this report. My only side effect: I created the empty scratch dir
`/fast/scratch/hyaku/kengaku-r43/R43ScoutMisroot-2` (assigned S) and removed it with `rmdir` at the end.
Start snapshot 2026-10-26 19:10:57 -0300; end snapshot 19:11:42 -0300. The watch covers ~45 s only, so it cannot
speak to events before 19:10:57 except through mtimes.

## 1. ~/.local/bin (start vs end)

| item | start 19:10:57 | end 19:11:42 |
|---|---|---|
| dir mtime | `2026-10-26 18:10:45.207143322 -0300` | `2026-10-26 18:10:45.207143322 -0300` (same) |
| entry count (`ls -A | wc -l`) | 102 | 102 |
| digest `find ~/.local/bin -maxdepth 1 -printf '%p %y %s %T@\n' \| sort \| sha256sum` (name/type/size/mtime, not content) | `6845b3d515dcb20c21fdcf777961da8599c5996373e8a17e9fc539730b2a1053` | `6845b3d5…a1053` (same) |

- Entries newer than 2026-10-26 12:00 at start: `firefox` (symlink, 17:48:46), `omp` (file, 275970224 B, 18:10:45.199).
  Both predate the round-root sentinel (18:49:21) by 38 min or more. `omp` mtime = dir mtime, so it is the
  self-update that last changed the dir. No git/python/shim file is newer than 10:50 other than those.
- Also from today, not from round 43: `sasquatch`, `sasquatch-v4be` (01:22), `pypy3.11` (02:16), `meson` (04:19), `ruff` (09:46), `OpenBot…AppImage`/`openbot` (10:49-10:50).
- Verdict: no kengaku round-43 write to ~/.local/bin observed (digest unchanged, dir mtime unchanged over the window,
  nothing newer than 18:10:45 after round start 18:49). Caveat: name/size/mtime digest, not a content hash; the
  envelope's content digest is the stronger check.

## 2. Fleet root `/home/vgpnk/Projects/shokunin`

- `git status --porcelain --untracked-files=all`: 0 lines at start, 0 lines at end (clean tracked + untracked).
- Ignored paths seen with `--ignored`: only `.jj/…` internals (and `.ufo/watchdog.log` via .gitignore:10).
- Files in the fleet root (outside lane dirs, `.git`, `.jj`) modified after 18:40: `.ufo/prompts/kasegi-round-40.md`,
  `.ufo/prompts/kama-round-48.md`, `.ufo/state/{disk-guard,inline-dispatcher}.log`, `.ufo/state/{kasegi,kama}.report-baseline`,
  `.ufo/watchdog.log`, `.scratch/goal-20261026-hyaku-run9.md` (19:08:06), `MANIFEST.json` (18:57:35). All are
  orchestrator/hyaku-driver artefacts for other lanes (kasegi/kama); the run-9 ledger commits are the driver's.
  None is a kengaku r43 seat output. `grep -il 'round-43|round 43|kengaku-r43'` hits only `MANIFEST.json`, whose
  round-43 lines are other lanes (kotodama r43, kumitate r43, tsukuroi r43), from commits by the driver.
- Fleet-root commits since 18:00 touching kengaku/round-43 paths: `.ufo/prompts/kengaku-round-43.md` and
  `.ufo/prompts/closure/kengaku-round-42.md`, `.ufo/reports/round-42/kengaku.md` — driver dispatch/closure commits
  (006480bd 18:37:18 "round-43: kengaku dispatch evidence"), not seat writes.
- Count of kengaku r43 seat-written files in fleet root: **0**.
- Kengaku lane files newer than 18:49 outside `build/` (informational, lane not host): the frozen claims set
  (`plans/round43_c1_verify.py` 18:49:33, `plans/round-43-claims.md` 18:54:08, `corpus/evidence/round43/feal-probe.txt` 18:56:01,
  `.ufo/waves/round-43/claims/*`) — freeze-time writes by L1 before wave 1; no later writes seen.

## 3. Scratch `/fast/scratch/hyaku/kengaku-r43`

- `.ROUND-ROOT-SENTINEL`: PRESENT at start and at end, 74 B, mtime 18:49:21.037, content
  `kengaku r43 round root (L1 KengakuR43, created 2026-10-26 18:49:21 -0300)`.
- Total 7.8 G (`du -sh`) on /fast (804G, 25% used). Dirs at start (`du -sh`, then 21 entries at end incl. mine removed → 20):

| dir | size |
|---|---|
| L1 | 1.3G |
| R43PkgEntry | 684M |
| R43PytestParity | 557M |
| R43SentinelCounter | 546M |
| R43PkgRows | 545M |
| R43CritEquiv | 543M |
| R43CritC1Counter, R43BatAncErr, R43BatAncAlt | 542M each |
| R43RevMutRows, R43GateRowsR2, R43BatOrdScan, R43BatOrdAlt | 541M each |
| R43CritValueLeg | 13M |
| R43ConsiderThese | 576K |
| R43CritIndep | 224K |
| R43ScoutPriorArt, R43R42Defects, R43ExecNoHarm | 0 |

  The ~540 MB per seat is a shared-clone `lane` each (note only; within `/fast`, no pressure at 604G free).
  Growth seen between two `du` runs about 1 min apart: R43PkgEntry 554 MB→684 MB (active).
- All dirs are under the round root and named for round-43 seats; no stray directory beside the sentinel; sibling
  `/fast/scratch/hyaku/` entries belong to other lanes (kaidoku-r38..42, kama-r48, kasegi-r40, mado-r47, tameshi-r48/50, tsukuroi-r43) plus loose `_d.txt`, `base-census.sh`, `line137.txt`, `unblob-tree.json`.

## 4. /tmp

- /tmp has 811 entries; files created after round-root creation (18:49) at start of watch: 18:50–19:11 batch listed by `find /tmp -maxdepth 1 -newermt '2026-10-26 18:40'`.
- Name/content search for kengaku/r43/round-43/feal/battery43 (`find -iname`, `grep -Il kengaku|round-43|r43|R43` on files <3 MB, depth 2):
  - names: only `/tmp/r43-tool.py` (14:38, mado-geometry tool, pre-round, other lane) and its `__pycache__`.
  - content: only `/tmp/self-assessment-census-3q1dofx8/{LOG,SCORECARD}.md` (19:11 — a different lane's self-assessment census).
- Post-18:49 /tmp files attributable by content to other lanes: kaidoku (`readme.txt`, `unblob-tree.json`, `e7z`, `7zx`, `xcheck`, `s/u/sb/si/l/sd.3438`, `brcm_sasq.*`, `bh*.out/err`, `var_*.sqfs`, `msg_sentinel.txt`), kasegi (`kas-r40-st`, `kas-selftest-full.txt`, `kasegi-r40-draft`), tabi/other web (`build.log`, `test.log`, `now.txt`, `gd.html`, `cl35`, `src_*.md`).
- Kengaku-adjacent but NOT round 43: `/tmp/r41-c1-counter.py` (18:50, kaidoku r41 counter text) and `/tmp/r42items_flat.tsv` (18:51; header ids `R42C1ImgDdwrt…` — kengaku round-42 closure seats), plus `/tmp/ecc-*`/`claude-tool-count-*` harness state.
- Unattributed: `/tmp/crk-h6-limb.txt` (19:09:34, 1216 B): a shell function `check_h6() { # TREE REF` using `SCRATCH_ROOT`; no kengaku/r43 string in it. `h6` matches the round-43 hostile fixture name `h6_receipt_dir.py`, so it may be a round-43 seat scratch note, but I cannot confirm. Single small file, harmless; flagged for the L1 to ask (candidates: R43CritC1Counter / R43CritIndep).
- Count of /tmp paths confidently created by a kengaku round-43 seat: **0 confirmed, 1 possible** (`/tmp/crk-h6-limb.txt`). Not evidence per rule; delete is the L1's call (I touched nothing).

## 5. Other observations (not requested)

- HOME writes since 18:49 outside .omp/.cache/Projects/.local/share/.config: `.cargo` registry cache (19:05), `.local/opt` dir mtime (19:05:20), `.npm/_logs`, `.grokbot/*`, `.zcode/v2`, `.gateguard/state-*` — harness/tooling noise; nothing indicating a seat install into PATH.
- The `.local/opt` mtime (19:05:20) is a dir under ~/.local, not ~/.local/bin; I did not inspect its contents.

## Summary

misroot = 0 (kengaku r43 seat files in fleet root: none; `git status` empty start and end); host writes = 0 observed
(~/.local/bin unchanged); sentinel present start and end; 1 possibly-r43 /tmp file (`/tmp/crk-h6-limb.txt`, flagged).

VERDICT: misroot-0-host-writes-0-sentinel-present
