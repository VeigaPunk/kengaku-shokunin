# SentinelReceiptsR81 — receipt provenance & seat scope audit (kengaku round 81 w1)

Role sentinel, leaf, read-only. Frozen claims `plans/round-81-claims.md` @ freeze `4d896e0daf8831ef7a0016bf3c944d11ba465f70`; base `4e833e9fee8022d24559535178c6fe32b2cd62f1`. Audited: (1) receipt stamp provenance, (2) mint driver `plans/round81_c1_remint.py`, (3) wave write scope. **Tools installed: none** (no tooling authorization exercised).

## 0. Measurement pins (integration was live during this audit)

Master moved five times while I measured; every check below names the tip it ran against.

| time (2026-11-04) | master at measurement | note |
|---|---|---|
| ~05:33 | `ca9bfe79` | receipts not yet tracked; tools untracked in worktree |
| ~05:37 | `805a65c8` | receipts/tools committed (`2fe3d8e6` landed 05:32:14) |
| ~05:43 (final) | `a54753e9de9812edbff23ede11a4dee5a2536771` | all re-verification below |

`git -C kengaku-shokunin log --oneline 4e833e9f..4ac8471b` → `4ac8471b` (instruments+repairs) ← `ca9bfe79` (wave spec) ← `4d896e0d` (freeze). Linear; no merges.

## 1. Receipt verdicts — `corpus/evidence/round81/{log-summary-date-ranges,vulnerable-secret}-probe.txt`

Both receipts are tracked at final tip `a54753e9` (`git ls-tree -r --name-only a54753e9 -- corpus/evidence/round81/`), added by `2fe3d8e6` ("located receipts …; ledger rows executed", 05:32:14), whose **parent is exactly the pinned tree**: `git rev-parse 2fe3d8e6^` → `4ac8471b15a40cddc16e1c5cccbde2a087f12117`.

| check | log-summary-date-ranges | vulnerable-secret | method |
|---|---|---|---|
| first line shape | PASS | PASS | `# tb2 <m> grader probe (round 81)`; frozen counter regex `^# tb2 {m} grader probe\b` (plans/round81_c1_new_members.py:68) accepts the `(round 81)` suffix, which the counter's own green fixture also emits (:504) |
| SUBJECT_CAPTURE | PASS | PASS | `corpus/evidence/round52/graders/<m>/tests/test_outputs.py`, tracked at tip |
| SUBJECT_SHA | PASS | PASS | `git show 4ac8471b:<capture> \| sha256sum` → `2fc06a6c…cb2b4` / `f2b65f63…0c753` = receipt lines; identical at `a54753e9` |
| TOOL_SHA | PASS | PASS | tracked bytes at `4ac8471b` and `a54753e9`: `a983909a…9a046` (log_summary), `209b28bc…90dca` (vuln_secret) = receipt lines |
| HOST_PYTHON | PASS | PASS | receipt `Python 3.14.8` == live `python3 -V` (`/usr/bin/python3`) |
| HOST_OPENSSL | PASS | PASS | receipt `OpenSSL 3.6.5 29 Sep 2026 (Library: …)` == live `openssl version` |
| LANE_TIP reachable | PASS | PASS | `git merge-base --is-ancestor 4ac8471b… a54753e9` → exit 0 (REACHABLE). Caveat: at my first measurement (tip `ca9bfe79`, pre-integration) it was NOT reachable; it became reachable the moment the wave's own commits landed. Any future tip must remain a descendant. |
| WORKTREE clean | PASS (driver-gated, see §2) | PASS (driver-gated, see §2) | not independently observable post-hoc; corroborated by: driver's pre+post `git status --porcelain` gates, and receipts committed 60 s after mint on top of the pinned tree with nothing between (`2fe3d8e6^ == 4ac8471b`) |
| COMMAND / EXIT 0 | PASS | PASS | driver only mints on probe rc==0 (remint.py main loop); command string matches `render()` output shape (`/usr/bin/python3 plans/round81_<m>_probe.py --lane . --work … --receipt …`) |
| MINTED_BY_SHA | PASS | PASS | receipt `eb6297f6…b5715d` == `git show <tip>:plans/round81_c1_remint.py \| sha256sum` at `ca9bfe79`, `4ac8471b`, `805a65c8`, `a54753e9` (driver unchanged all round) |
| OBSERVATIONS == instrument stdout at measured tree | PASS | PASS | independent replay in my own `--shared` clone detached at `4ac8471b` (toplevel asserted == clone dir), `/usr/bin/python3 plans/round81_<m>_probe.py --lane . --work <scratch> --receipt <scratch>`: rc=0, `mismatches=0`, `PREDICATE R81-C1 pass`; block-vs-replay with `^REV ` dropped → **EQUAL=True, 14/14 lines, both members**. Also: the mint driver's own stdout captures (`/fast/scratch/hyaku/kengaku-r81/mintwork/<m>.stdout.txt`, mtime 05:31) minus `REV` lines byte-equal the committed blocks (`diff -q` clean) |
| ledger row | PASS | PASS | at `a54753e9`: `{"classes":["file-artifact"],"receipt":"corpus/evidence/round81/<m>-probe.txt","round":81,"status":"executed","subject":"tb2-header","verdict":"predicate"}` (read from `git show a54753e9:plans/grader-population-ledger.json`) |

**Verdict: both receipts PROVENANCE-PASS.** No fabricated pin found; every digest re-derives from committed bytes; the observation blocks are genuine instrument output reproduced by an independent replay.

## 2. Mint driver audit — `plans/round81_c1_remint.py` (committed bytes, sha256 `eb6297f6…`)

**Q1 Can it write a receipt while the worktree is dirty? NO — with two residual edges.**
`main()` runs `git status --porcelain` *before* any mint (`SETUP worktree not clean …; run in a fresh clone`, rc 2) and *again after all probes, before any write* (`…nothing written`, rc 2). Receipts/ledger are written only after the second clean check. Edges: (a) `work.mkdir(parents=True)` runs **before** the first clean check — a refused run still creates its scratch dir (harmless, outside the lane); (b) TOCTOU: a concurrent writer between the post-check and the `write_text` calls is not re-checked (inherent; window is milliseconds).

**Q2 Does `LANE_TIP` come from the executed checkout or the branch? The executed checkout.**
`head = git(lane, "rev-parse", "HEAD")` — HEAD of whatever checkout `--lane` names, never `master`/branch refs. A detached clone pins the clone's HEAD. This is why the receipts pin `4ac8471b` and not today's later tip: faithful to the measured tree.

**Q3 Can a probe's failure still mint? The failed member cannot; the run is not all-or-nothing; and the mismatch guard is an OR-hole.**
- A member whose probe times out, exits non-zero, prints no observations, or fails the guard is `continue`d — never staged, never written. Its ledger row is untouched.
- **[Medium] Partial-failure runs still write.** If member A succeeds and B fails, A's receipt *and* the ledger update are written to the lane, then the driver exits 3 (`MINT minted=1 failed=1`). Nothing rolls back. The claims' kill rule ("two or honest stop") is enforced only by the counter/gate, not by the driver. An operator who ignores rc 3 is left with a half-minted lane. Smallest remediation: stage all writes until after the per-member loop reports `failed == 0` (buffer, then write).
- **[Medium] The mismatch guard mints a lying probe.** remint.py: `if "mismatches=0" not in proc.stdout and "PREDICATE" not in proc.stdout: MINT-FAIL`. The two signals are OR'd, so a probe that exits 0 and prints a `PREDICATE R81-C1 pass` line while reporting `mismatches=12` and/or `MISMATCH` case lines **still mints**. Exploit path: an instrument bug (or a tampered tool committed by a future round) that exits 0 while the grader disagrees → driver mints → the frozen counter's reproduction check compares the receipt block against the *same* deterministic stdout → equal → `REPRODUCED` passes → ledger `verdict=predicate` (the pass line is present) → the claims sentence is satisfied with a receipt that honestly records its own grader disagreement. The frozen OBS projection keeps `MISMATCH` lines and the frozen counter has no `mismatches=0` requirement, so nothing downstream catches it. Smallest remediation (driver-side; the counter is frozen): require `"mismatches=0" in proc.stdout` **and** no `^MISMATCH ` line in stdout before staging. Note this does not affect the two receipts minted this round — both replay to `mismatches=0` independently (§1).

## 3. Wave write-scope audit

### 3a. `.ufo/waves/round-81/` (lane) — final listing vs declared paths (w1-spec.json)

| file | mtime | author | declared? |
|---|---|---|---|
| `build_spec.py`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/w1-dispatch.json`, `w1/swarm-registry.json`, `w1/w1-run.err` | 05:24–05:25 | wave scaffolding (committed at tip) | orchestrator-owned; `w1-run.err` is 0 bytes |
| `w1/ScoutHostR81.md` | 05:28 | ScoutHostR81 | PASS — its declared report |
| `w1/host-state.txt` | 05:39 | EnvPinR81 | PASS — its declared "ONE deliverable" |
| `w1/EnvPinR81.md` | 05:41 | EnvPinR81 | PASS — report per reportDir convention |
| `w1/ConnectorR81.md` | 05:42 | ConnectorR81 | PASS — report |
| `w1/SentinelReceiptsR81.md` | (this file) | me | PASS — my declared report |

**[Flag, process] Declared executor deliverables bypassed the wave dir.** w1-spec.json names `w1/ProbeLogSummaryR81.py`, `w1/ProbeVulnSecretR81.py`, `w1/C2ChecksR81.py` as each seat's "ONE deliverable path … outside scratch". **None exists**; the same-purpose bytes live instead as lane files `plans/round81_log_summary_probe.py`, `plans/round81_vulnerable_secret_probe.py`, `plans/round81_c2_checks.py` (all tracked at `a54753e9`). `w1/r80-u1-anchors.txt` (U1AnchorR81's declared deliverable) was also absent at audit close (seat possibly still running). Either seats wrote into lane `plans/` directly (a write-scope breach — seats deliver bytes to the L1, who integrates) or the L1 relocated the deliverables (allowed). Attribution is not recoverable from bytes alone; the pattern repeats across three seats, so it looks deliberate (L1 relocation) rather than accidental — but the spec text and the outcome disagree, and that is worth an orchestrator ruling for the next wave. Seats whose only lane-facing obligation was a report complied.

### 3b. `/home/vgpnk/Projects/shokunin/.ufo/reports/round-81/` (fleet)

`kotoba.md` (26036 B, 2026-10-28 02:23), `kotodama.md` (14132 B, 11-03 14:50), `revenger.md` (16009 B, 11-03 14:50), `mori.md` (19071 B, 11-04 04:13). All tracked at fleet HEAD (absent from `status --porcelain`). All predate wave dispatch (05:24) — **no kengaku w1 seat wrote here**; these are fleet-level seats' round-81 reports. Oddity, noted not judged: `kotoba.md` is dated a week before this round's run began.

### 3c. Fleet-root porcelain — misroots carrying round-81 content

`git -C /home/vgpnk/Projects/shokunin status --porcelain=v1` (final): ` M .scratch/goal-20261103-hyaku-run15.md`, ` M .scratch/run15-state.json`, `?? .scratch/closure-*` (r73/r74/r75 closures), `?? .scratch/run13-state.json`, `?? .scratch/run15-kernel.py`, `?? after`.
- `after`: 24 bytes, content `== SCORECARD diff base-`, **zero** matches for `round-81|R81|kengaku` — stray debris, not a round-81 misroot.
- `.scratch/goal-20261103-hyaku-run15.md` and `run15-state.json` do mention kengaku round 81 but are the **orchestrator's own run-state** (legitimate).
- No fleet-root file written by a wave seat. PASS.

### 3d. Scratch hygiene — `$HYAKU_SCRATCH/kengaku-r81/`

Seat-named dirs exist (C2ChecksR81, MutationGateR81, ConnectorR81, ReviewerC1R81, U4RedBeforeR81, EnvPinR81, SentinelReceiptsR81, …) **alongside 25+ anonymous entries created this round** (mtimes 05:21–05:41): dirs `ct, gate, gate-work, mu, st, st2, st3, st4, dbg, rec, u4, c2c, c2c2, ls, mint, mintclone, mintwork, vs, clean, clean2, clean3, ctl, det, c2` and stray files `census-before.txt, index-before.txt, c1-after.txt`. **[Flag, Low]** The binding rule is scratch = `$HYAKU_SCRATCH/kengaku-r81/<your-seat-name>/`; anonymous siblings violate it. Notably the receipts' own `COMMAND` lines point at `kengaku-r81/mintwork/…` — the mint ran outside any seat-named dir (the driver's default is `…/kengaku-r81/mint`). No lane impact (scratch is disposable), but it breaks per-seat attribution and cleanup accounting.

## 4. What I attacked and could not break

- **Stamp forgery**: recomputed every digest in both stamp blocks from committed bytes at three tips — none fabricable without changing the pinned commits (all shas stable `4ac8471b`→`a54753e9`).
- **Observation fabrication**: replayed both instruments myself in a private clone detached at the pinned commit; both blocks reproduce line-for-line (14/14 EQUAL). A receipt could not have been written by hand and still match an independent replay.
- **Mint-time dirtiness**: the driver's two porcelain gates + the `2fe3d8e6^ == 4ac8471b` adjacency hold; I could not construct a dirty-worktree mint short of racing the TOCTOU window.
- What I could *not* verify: the literal worktree state at mint instant (post-hoc, unobservable) — I report it as driver-gated, corroborated by commit adjacency.

Scratch `$(HYAKU_SCRATCH)/kengaku-r81/SentinelReceiptsR81/` (incl. the one `--shared` clone) deleted before yield. No lane file was written by me except this report.
