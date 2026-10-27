# R48SentHygiene — wave-wide boundary audit (R48-C1 + R48-C2)

Seat `R48SentHygiene` (sentinel, route `@m_flash` as captured at spawn; no model passed). Item: audit the whole
round-48 wave for boundary violations — outside writes, secrets, `/tmp` citation, fleet-repo touches, shared
writer paths — one report with per-seat disposition.

**Axes named:** calibration (R48-C1) and coverage (R48-C2) are the axes the wave serves. This seat scores neither
and claims neither admission; it audits write scope, provenance, freeze ordering and containment only.

**Snapshot:** `2026-10-27T09:02:08-03:00` (results below are that instant; 57 of 64 seats had landed a report,
7 had not — 1 still writing, 1 quiet, 5 stalled after cloning — and 1 landed report still had scratch on disk).
Scratch root `/fast/scratch/hyaku/kengaku-r48/R48SentHygiene` (created, `TMPDIR` exported, removed before yield).
No fixture, counter, probe, gate or fence was executed by this seat; no tool was installed or updated.

**Revision measured.** `REV a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze) and
`REV bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` (lane tip read). No receipt here is a scored measurement; the only
revisions measured are tree identities.

## Freeze gate (checked before anything else — no scored run is permitted without it)

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
$ git hash-object plans/round-48-claims.md ; git rev-parse a543d920:plans/round-48-claims.md
3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5
3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5
$ git diff --stat a543d920 -- plans/round-48-claims.md      # (no output: worktree bytes == frozen bytes)
$ ls plans/round48_c1_verify.py plans/round48_c2_verify.py
ls: cannot access 'plans/round48_c1_verify.py': No such file or directory
ls: cannot access 'plans/round48_c2_verify.py': No such file or directory
$ ls -la .ufo/waves/round-48/claims
README.txt  freshness-r48.txt          # prepared_by=L1 KengakuR48 2026-10-27T11:30:40Z; no receipts
```

Stage-1 is committed and predates all wave activity: freeze `06:53:29`, dispatch commit `453ddfdb` `08:29:18`,
handoff marker `bf783c1e` `08:29:33`, first seat artifact `08:31:07`. Stage 2 (counter files, pins, literals
`<P><H><S><B><M>` / `<V><N>`, before-control receipts) is **absent** from the committed tree and from the claims
receipts dir. Consequence, stated as the blocker it is: **no scored R48 counter or probe run is permitted and no
round-48 receipt exists on disk; this seat made none.** Every execution I observed in the wave measured the base
tree, a control tree or inherited round-46 instruments — never a frozen R48 counter (none exists) and never
claimed work.

## Findings

| # | severity | finding | evidence (observed) | smallest remediation |
|---|---|---|---|---|
| F1 | medium — ordering/provenance | Seats executed **non-dry** gates/controls before the stage-2 amendment, and one left the resulting receipts in the wave dir. `R48C1ExecControls` ran the six frozen C1 controls plus a second pass (`s1-*`) and diagnostics on scratch trees 08:39–08:46 with the **candidate** counter (v1, `sha256 f395e085…`) and landed all 18 receipt files under `w1/R48C1ExecControls/receipts/` — six of them named `control-c1-*.txt`, the names the claims reserve for the stage-2 receipts. `R48C2ExecControls` ran the C2 candidate gate on `base`/`filler`/`echo` trees with `p10=disabled` at 08:37 (`REV 787691a9…`, `4ffb15d0…`, `ecf768d0…`, scratch-only). `R48C1ExecCounter` ran its candidate counter against a scratch base-fence tree at 08:35:55 (`PINS total=75 mismatched=0`, `HONEST fixtures=113 admitted=109 refused=4`, then `KeyError: 'refusal'` in `BENIGN-MODULES`). The letter of §Ordering is not broken (no package probe ran; P10 disabled), but **none of these outputs may be promoted to the stage-2 before-control receipts**, and the `control-c1-*` names in `w1/` would collide with the frozen receipt path `.ufo/waves/round-48/claims/`. Instrument identity also moved during the wave: the C1 counter was v1 `f395e085…` when the controls ran; a later v2 (25,177 bytes) arrived in the controls seat's inbox. | `w1/R48C1ExecControls/receipts/*.txt` (18 files) and `summary.txt`; `w1/R48C2ExecControls.md:291-370`; `/fast/scratch/hyaku/kengaku-r48/R48C1ExecCounter/out/base-fence.{txt,err}`; `R48C1ExecControls/env/*` | L1 runs every control after the stage-2 commit, with the stage-2-pinned counter, into `.ufo/waves/round-48/claims/`; pre-stage-2 outputs stay labelled selftest and never enter `claims/`. |
| F2 | medium — unpreserved provenance | `R48C2ExecControls` cites a **sibling seat's scratch** artifact as the instrument it measured: `file:///fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py`. Its own report gives three different digests for that path: `2c574c84…` (instrument table line 45), `3de23da…` (three embedded receipts), while the file hashed `44a90c9e…` at 08:40:44, `0a2789e2…` at 08:42:38, and `7611883b…` at 08:46:29 — the final candidate its own seat reports (`sha256 7611883b…`, 652 lines). Every digest the control receipts measure is therefore superseded, and the receipt's subject lives only in another seat's scratch. | `R48C2ExecControls.md:45,285-295,438`; `sha256sum /fast/scratch/hyaku/kengaku-r48/R48C2ExecCounter/candidate/round48_c2_verify.py` → `0a2789e2…` (08:42:38) then `7611883b7004c4b5fabb728ff3448a2d1eedf3b49151dbcde67d0f29dfead227` (08:46:29, matches its own report) | Pin one digest of a copy the reporting seat owns (report/wave dir) and never cite a live sibling scratch path; the stage-2 counter is a different file anyway. |
| F3 | info — cross-seat instrument copy (not a writer-path breach) | `R48C1ExecControls` copied the sibling's candidate into **its own** scratch (`cp …/R48C1ExecCounter/cand/round48_c1_verify.py …/R48C1ExecControls/inbox/…`, mode read-only, `sha256 f395e085…`) and its runner aborts unless that digest matches. The producer's own report carries the same digest and embeds the full text as Appendix A, so the bytes survive the scratch cleanup. No shared writer path: each seat wrote only inside its own scratch. | `R48C1ExecControls.md:49-60,402`; `R48C1ExecCounter.md:39-47`; `sha256sum …/R48C1ExecControls/inbox/round48_c1_verify.py` → `f395e085ce8380c5fc0f65c978ada64b18dc89860b3881f07066009659a0b30c` | Keep the digest guard; the stage-2 pin must name this exact digest or its successor explicitly. |
| F4 | low — false cleanup claim | `R48C1ConnPattern` states “scratch was removed on command completion”, but `/fast/scratch/hyaku/kengaku-r48/R48C1ConnPattern/lane` (568 MB shared clone) was still on disk at 08:44:39 and at 08:50:00. This is the seat's own defect to report; it did not. | `R48C1ConnPattern.md` scratch-cleanup line; `du -sh` → `568M`; dir mtime `08:31` | Remove the tree or correct the report; the report is the evidence of record. |
| F5 | low — wave-dir artifacts outside the named report path | Three seats wrote directories beside their reports instead of only the named report file: `w1/R48C1ExecHonest/` (159 files, 796 KB: `modules/*`, `receipts/*`, `population.txt`, `identity.jsonl`), `w1/R48C1ExecControls/` (23 files, 488 KB: six `control-c1-*.txt` receipts, `s1-*` re-runs, `fences/*.py`, `run_controls.py`), `w1/R48C2ExecMutBattery/` (21 files, 108 KB: `M00…M14.json`, `battery.json`, `mutants.py`). Round-46 precedent exists (`w1/R46ExecC3Probe/`). Content scan: no `/tmp` hardcode, no secrets, no symlinks; the landed control-fence digests match the digests printed in the receipts (`name_keyed_variant.py` `560b746e…`). | `find w1 -maxdepth 1 -type d`; `du -sh` → `796K`, `488K`, `108K`; `sha256sum w1/R48C1ExecControls/fences/*` | L1 accepts or relocates these at stage 2; they are untracked lane material, not production edits — but `receipts/control-c1-*.txt` must not be mistaken for the `claims/` receipts (F1). |
| F6 | low — production-tree write during the wave | `corpus/lessons/round-48.md` is untracked and was written **while the wave ran**: 607 B at 08:31:40, 3,878 B at 08:35:32 (“Mistakes”, “Gate”, “Claim evidence and verdicts … after WAVE-DONE”). Content self-identifies the L1 (`KengakuR48`) and asserts no admission. In-role for the integrator, but it is a production edit mid-wave; two seats read earlier byte states. | `stat -c '%y %s' corpus/lessons/round-48.md`; `git status --porcelain` → `?? corpus/lessons/round-48.md`; `sed -n '1,25p'` | L1 confirms authorship; no seat action needed. Attribution is by content only — no process trail. |
| F7 | low — scratch paths cited as sources | Reports cite clone paths as source URLs instead of lane paths: `R48C1PredCounter` (round-45 committed bytes), `R48C2PosControl` (6 lane files), `R48C2PreReceipt` (8), `R48C2Sandbox` (probe), `R48C2ExecControls` (sibling counter, F2). The 18 receipt files landed at `w1/R48C1ExecControls/receipts/` likewise name only scratch paths for the counter, the clone and the fence in their command lines (mitigated: each receipt prints the measured `REV`, the tree was a `--shared` clone of that `REV`, and the fence digests match the copies landed under `w1/R48C1ExecControls/fences/`). Wave rule: anything a report cites lands in the wave dir or the lane tree. | `grep -lE 'file:///fast/scratch' w1/*.md`; `grep -l '/fast/scratch' w1/R48C1ExecControls/receipts/*.txt \| wc -l` → `18` | Cite `file:///home/…/kengaku-shokunin/…` for committed bytes; F2 is the material case. |
| F8 | info — host-level lane `.git` rewrite | At `08:36:07`, 5,148 files under the lane `.git` (loose objects and both packs) received new mtime/ctime with inode birth preserved (sample `b63fab84…`: birth `2026-10-26 13:21:59`, mtime/ctime `08:36:07.314`). Simultaneously `mado-shokunin/.git` 354 files, `kaidoku-shokunin/.git` 6,674 files (+3 new packs at `08:36:22`), `chousa-shokunin/.git` 1, fleet-root `.git` 26. No refs/HEAD/index change in the lane (`HEAD bf783c1e`, refs 08:29, index 08:29:35); `git fsck --no-dangling` silent; `git verify-pack -s` OK; tracked worktree clean. Not attributable to any kengaku seat — a host maintenance/backup job. | `find kengaku-shokunin/.git -newermt '…08:36:00' ! -newermt '…08:37:00' -type f \| wc -l` → `5148`; same window: kaidoku 6674, mado 354, chousa 1, fleet 26 | L1 should not attribute `.git` mtimes in that second to seats; confirm the host job outside this lane. Traced fixture runs in that second could have seen a moving object store (no seat reported a git error). |
| F9 | info — frozen-claim provenance mismatch | Claims §C2 says the probe (`sha256 22b7779e…`, the wave artifact) was “integrated verbatim to `plans/polyglot_c_py_probe.py`”. Committed `plans/polyglot_c_py_probe.py` at `a543d920` hashes `67a8f4a6…` and `cmp` differs at line 20 (`prlimit`/timeout/capped-output differences per `R48C2PosControl`). Stage-2 pinning must resolve this without editing a predicate line. | `sha256sum plans/polyglot_c_py_probe.py .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` → `67a8f4a6…`, `22b7779e…`; `plans/round-48-claims.md:85` | L1 records a Freeze-amendment note or pins the actual committed digest; do not silently pin the artifact hash. |
| F10 | info — no secrets | Pattern scan (`sk-…`, `AKIA…`, `ghp_…`, `xox[bap]-`, PEM `BEGIN … PRIVATE KEY`, JWT, `password=`, `token=`, SSH keys) over `.ufo/waves/round-48/`, all 57 reports at final snapshot and all wave scratch outside clones: **zero hits**. The only scratch hits are the committed lane file `.ufo/waves/round-34/build/R34SentSecrets.md` inside every clone (pre-existing lane content). | `grep -rInE '…' .ufo/waves/round-48/` → no output | none |
| F11 | info — `/tmp` use is small and not citable evidence | No report cites a `/tmp` path **as evidence**. One seat shows a `/tmp` path in its command transcript: `R48C2ExecMutBattery` fetched the pinned S166 to `/tmp/tb2_test_outputs.py` (1,564 B, 08:34) and printed `curl`/`sha256sum` there; the evidence is the printed digest `b94a7a98…`, which matches the committed capture, not the path. That file is still on disk (well under the 50 MB allowance); two other unreferenced 27,966-byte probe-shaped files (`/tmp/p_head.py` 08:31, `/tmp/probe_tip.py` 08:35) belong to no report. Reports otherwise mention `/tmp` only to say it was unused/private (`R48C1ExecHonest` deleted three <1 MB copies; `R48C2Sandbox` private tmpfs). No `/tmp` file is required to reproduce any claim. | `find /tmp -maxdepth 1 -newermt '…08:00'`; `R48C2ExecMutBattery.md:237-239`; `grep -n '/tmp' w1/*.md` | none required; `/tmp` is transient state, and every cited byte is committed in the lane. |
| F12 | info — no PATH / tool installs | `~/.local/bin` mtime `2026-10-27 05:26:51` (before the wave); no entry under `~/.local/share/uv/tools` has an mtime after `08:00`; no report records an install, so there is nothing to record. | `stat -c '%y' ~/.local/bin`; `find ~/.local/share/uv/tools -maxdepth 1 -newermt '2026-10-27 08:00'` → no output; `uv tool list` | none |
| F13 | info — no fleet-repo touches | Fleet `git status --porcelain` has only two pre-wave untracked files (`06:14:55`, `06:38:17`); fleet log tip is round-57 `08:19:19`; no round-48 artifact references a fleet write. Concurrent sibling-lane activity (`kasegi`, `mado`, `chousa`, `kaidoku` writing their own files 08:29–08:38) is their rounds, not this wave. | `git -C /home/vgpnk/Projects/shokunin status --porcelain`; `git log -3` | none |
| F14 | info — no shared writer paths | The spec has 64 seats and **64 unique report paths**, all under `.ufo/waves/round-48/w1/`, no duplicates; no seat wrote another seat's report path, and no two seats wrote one file. The cross-seat case (F3) is a read-only copy made inside the copying seat's own scratch. | `python3` over `w1-spec.json`: `unique report paths 64`, `dup paths: {}` | none |
| F15 | info — lane production files untouched by seats | `git status --porcelain` shows exactly four entries: `?? .ufo/waves/round-48/claims/`, `?? .ufo/waves/round-48/w1.ready.dispatched`, `?? .ufo/waves/round-48/w1/`, `?? corpus/lessons/round-48.md`. No tracked modification; no commit after `bf783c1e`; `.ufo/state` untouched by seats. | `git status --porcelain`; `git log --format='%H %ci %s' -5` | none |
| F16 | info — freeze-ordering compliance | Every landed report that executed something states the stage-1 check and refuses to score. The instruments actually run are inherited round-46 counters/gates (`round46_c1_verify.py`, `round46_c3_verify.py`, `pkg_gate.py` with P10 off, `order_check.py`, `polyglot_c_py_probe.py --dry`) or wave-1 candidates — never a stage-2 R48 counter, never claimed work. | `grep -cE 'no scored\|No scored' w1/*.md`; reports at `R48C1CritBase.md:9`, `R48C2MutTags.md:7`, `R48C2MutVerdict.md`, `R48RevClosure.md:11` | none |
| F17 | medium — operability (not a boundary breach) | Five seats stalled immediately after cloning and left no report: `R48C1HoMount`, `R48C1MutExit`, `R48C1MutGit`, `R48C1RevClaim`, `R48C1ScoutPop`. Each scratch holds exactly one `--shared` clone (568 MB) and nothing else; the newest file in each is 08:32:05–08:34:19, i.e. no activity for ~28 minutes at `09:02:08`. Their items are unattacked and their 2.8 GB of clones will not self-clean. Two seats are late rather than stalled: `R48C1ExecFenceB` was still writing at `09:01:59`; `R48C2ExecCases` wrote at 08:55:11 and has been quiet since (`09:02:08`). | Per-seat newest-file mtime, e.g. `R48C2ExecCases` → `08:55:11.191`, `R48C1ScoutPop` → `08:32:05.299`; `du -sh` → `568M` each | L1 re-dispatches or declares the five items unexecuted; their scratch is the harness's to reclaim, not a sibling's. |

## Per-seat disposition (64 seats; table at the 08:50:00 snapshot, late deltas in the totals block)

`RPT` = report file present at `.ufo/waves/round-48/w1/<seat>.md`; `SCR` = seat scratch dir still present under
`/fast/scratch/hyaku/kengaku-r48/`.

| seat | RPT | SCR | disposition |
|---|---|---|---|
| `R48C1ExecCounter` | Y | Y | report landed; scratch 2.8 GB still on disk at 08:50 (report says removal at seat end — mid-run); candidate `f395e085…` (552 lines, Appendix A), v2 copy arrived in the controls seat's inbox (F1/F3); non-dry base-fence selftest pre-stage-2 |
| `R48C1ExecFenceA` | Y | - | report landed; scratch removed |
| `R48C1ExecFenceB` | - | Y | **active at 08:57:23** (files still being written), report not yet landed; no violation observed; clone is `--shared` |
| `R48C1ExecHonest` | Y | - | artifact dir `w1/R48C1ExecHonest/` (159 files, 796 KB, F5); scratch and `/tmp` copies cleaned |
| `R48C1ExecControls` | Y | Y | report + artifact dir `w1/R48C1ExecControls/` (23 files, F5); 6/6 `PREDICATE R48-C1 fail` on candidate counter v1; 18 receipts landed under `w1/` pre-stage-2 (F1); ~48 KB scratch residue despite “removed” claim |
| `R48C1ScribeSynth` | Y | - | within write scope; scratch removed |
| `R48C1ScribeLimit` | Y | - | within write scope; scratch removed |
| `R48C1ConnOverlap` | Y | - | within write scope; created no scratch (consistent) |
| `R48C1ConnPattern` | Y | Y | **defect:** scratch 568 MB still on disk while the report claims removal (F4) |
| `R48C1ScoutPop` | - | Y | **stalled:** clone only (568 MB `--shared`), no write since 08:32:05, no report — item unattacked at snapshot |
| `R48C1Rerun` | Y | - | within write scope; scratch removed |
| `R48C1HonestInv` | Y | - | within write scope; scratch removed |
| `R48C1Overrefusal` | Y | - | within write scope; scratch removed |
| `R48C1HoArgv` | Y | - | within write scope; scratch removed |
| `R48C1HoPaths` | Y | - | within write scope; direct fence runs on own fixtures, no counter/probe; scratch removed |
| `R48C1HoStore` | Y | - | within write scope; scratch removed (rmdir) |
| `R48C1HoConfig` | Y | - | within write scope; scratch removed |
| `R48C1HoMount` | - | Y | **stalled:** clone only (568 MB `--shared`), no write since 08:34:19, no report — item unattacked at snapshot |
| `R48C1MutNames` | Y | - | within write scope; scratch removed |
| `R48C1MutOrder` | Y | - | ran inherited round-46 C1 detector on base fence; scratch removed |
| `R48C1MutBoundary` | Y | - | blocked honestly at stage 2; scratch removed |
| `R48C1MutGit` | - | Y | **stalled:** clone only (568 MB `--shared`), no write since 08:32:50, no report — item unattacked at snapshot |
| `R48C1MutPending` | Y | - | within write scope; scratch removed |
| `R48C1MutCounterPins` | Y | - | 8/8 mutants killed on inherited detector; restored clone, scratch removed |
| `R48C1MutExit` | - | Y | **stalled:** clone only (568 MB `--shared`), no write since 08:33:34, no report — item unattacked at snapshot |
| `R48C1PredCounter` | Y | - | cites scratch clone paths for committed bytes (F7); scratch removed |
| `R48C1CritBase` | Y | - | refused to run an older counter (correct); scratch removed |
| `R48C1CritPop` | Y | - | within write scope; scratch removed |
| `R48C1RevNoHarm` | Y | - | cites clone paths (F7); scratch removed |
| `R48C1RevClaim` | - | Y | **stalled:** clone only (568 MB `--shared`), no write since 08:33:49, no report — item unattacked at snapshot |
| `R48C2ExecCounter` | Y | - | report landed; final candidate `sha256 7611883b…` (652 lines) embedded in Appendix A; scratch removed; `--dry`/`--control` runs only (V2/probe excluded); its intermediate digests are what F2 measures |
| `R48C2ExecProbe` | Y | - | report landed; `--dry`/`--stage-check` and P10-disabled gate only, **no full probe**; clone restored, scratch removed |
| `R48C2ExecCases` | - | Y | late, not stalled: wrote at 08:55:11, quiet through `09:02:08`; no report yet; no violation observed |
| `R48C2ExecControls` | Y | - | **defect:** cites a live sibling scratch artifact with three inconsistent digests (F2); pre-stage-2 P10-disabled gate runs (F1); scratch cleaned as claimed |
| `R48C2ExecMutBattery` | Y | - | report landed; artifact dir `w1/R48C2ExecMutBattery/` (21 files, 108 KB, F5); ran committed base legs minus V2/V11 (V11 run separately on synthetic states); scratch removed; one `/tmp` fetch residue (F11) |
| `R48C2ScribeGate` | Y | - | fetched S166/Docker Hub to scratch only, transcribed, removed; no scored run |
| `R48C2ScribeEntry` | Y | - | within write scope; scratch removed |
| `R48C2ConnPrior` | Y | - | within write scope; no scored run |
| `R48C2ConnCross` | Y | - | within write scope; scratch removed after report |
| `R48C2ScoutEntry` | Y | - | within write scope; scratch removed |
| `R48C2Rerun` | Y | - | `--dry` stage-check only; scratch removed |
| `R48C2TagInv` | Y | - | within write scope; no execution |
| `R48C2PreReceipt` | Y | - | `--dry` only (allowed); cites clone paths (F7); scratch removed |
| `R48C2PosControl` | Y | - | `--dry` only; found the F9 digest mismatch; scratch removed |
| `R48C2Filler` | Y | - | within write scope; no scratch clone |
| `R48C2Echo` | Y | - | within write scope; scratch removed |
| `R48C2MutTags` | Y | - | blocked honestly at stage 2; no mutation executed; scratch removed |
| `R48C2MutOrder` | Y | - | detector (order gate) run on own committed-history fixture; sibling read of a scratch clone only; scratch removed |
| `R48C2MutPins` | Y | - | within write scope; scratch removed |
| `R48C2MutVerdict` | Y | - | blocked honestly at stage 2; scratch removed |
| `R48C2MutReceipt` | Y | - | ran inherited pure parse legs between V2/P10; no probe; scratch removed |
| `R48C2MutNames` | Y | - | ran inherited leg set sans V2; restored clone (`status` empty); scratch removed |
| `R48C2MutDup` | Y | - | blocked honestly; self-reported trap miss then explicit removal — verified removed |
| `R48C2SourceReopen` | Y | - | one HTTP fetch of the pinned S166 URL; scratch removed |
| `R48C2SourceReject` | Y | - | within write scope; scratch removed |
| `R48C2Scope` | Y | - | one shared clone; scratch removed after report (mid-report snapshot saw it) |
| `R48C2CritDoNothing` | Y | - | within write scope; scratch removed |
| `R48C2RevNoHarm` | Y | - | read-only no-harm review; scratch removed |
| `R48C2RevAdmission` | Y | - | within write scope; scratch removed |
| `R48C2Sandbox` | Y | - | bwrap host-path control only, private `/tmp`; no install; scratch removed |
| `R48SentHygiene` | Y | - | this seat (audit only; no fixture, counter or probe); scratch removed |
| `R48RevReport` | Y | - | read-only checklist; scratch removed |
| `R48RevengerOverlap` | Y | - | read-only overlap analysis; no execution admitted; scratch removed |
| `R48RevClosure` | Y | - | read-only closure review; no scored run; scratch removed |

Final tallies (`09:02:08`): 57 reports; 7 seats without one — `R48C1ExecFenceB` still writing, `R48C2ExecCases` quiet
since 08:55:11, and `R48C1HoMount`, `R48C1MutExit`, `R48C1MutGit`, `R48C1RevClaim`, `R48C1ScoutPop` stalled after
cloning (F17). One landed report still leaves scratch on disk (`R48C1ConnPattern`, 568 MB — false cleanup claim,
F4); the two seats that had scratch residue at 08:50 (`R48C1ExecCounter`, `R48C1ExecControls`) have since cleaned
it. Three artifact dirs live under `w1/` (F5). Zero secret hits, zero `/tmp` paths cited as evidence, zero
fleet-repo writes, zero duplicate writer paths. `.ufo/waves/round-48/claims/` still holds only the L1's
`README.txt` + `freshness-r48.txt` — no stage-2 receipt exists, so the pre-stage-2 receipts in
`w1/R48C1ExecControls/receipts/` remain only a promotion hazard (F1). `git hash-object plans/round-48-claims.md`
still equals `git rev-parse a543d920:plans/round-48-claims.md` (`3a9c71f3…`): no post-freeze edit of the claims.

## Exact commands run (read-only; representative, with observed output)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kengaku-shokunin
git log --format='%H %ci %s' -5
bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767 2026-10-27 08:29:33 -0300 round-48: w1 ready handoff marker
453ddfdb4e8f69068aaf25084756188012cfcb10 2026-10-27 08:29:18 -0300 round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
0f77f9b27931b3c76b3d095fc0fa70edb79556d9 2026-10-27 04:44:36 -0300
ce6d90e2eab7231d6460544cce090335eb7ec09f 2026-10-27 04:38:52 -0300 protocol-shokunin
git status --porcelain
?? .ufo/waves/round-48/claims/
?? .ufo/waves/round-48/w1.ready.dispatched
?? .ufo/waves/round-48/w1/
?? corpus/lessons/round-48.md
find /fast/scratch/hyaku/kengaku-r48 -maxdepth 1 -type d | wc -l        # 48 at 08:33, 52 at 08:40, 37 at 08:44
du -sh /fast/scratch/hyaku/kengaku-r48                                  # 25G (08:40); /fast 239G/804G (30%)
for d in /fast/scratch/hyaku/kengaku-r48/*/; do cat "$d/lane/.git/objects/info/alternates"; done
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/objects   # every clone sampled is --shared
find kengaku-shokunin/.git -newermt '2026-10-27 08:36:00' ! -newermt '2026-10-27 08:37:00' -type f | wc -l
5148
sha256sum plans/polyglot_c_py_probe.py .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py
67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26  plans/polyglot_c_py_probe.py
22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d  .ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py
grep -rInE 'sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|BEGIN [A-Z ]*PRIVATE KEY|xox[bap]-' .ufo/waves/round-48/
(no output)
```

## Sources opened (access date 2026-10-27; no external URL opened by this seat)

| source | URL | quote (≤25 words) |
|---|---|---|
| frozen claims | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` | “Pre-receipt controls run the C2 gate with its P10 (fresh probe re-run) leg disabled” |
| routed defects | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` | “9/9 novel honest fixtures refused and fence mutants 2/13 caught” |
| scorecard | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/SCORECARD.md` (§Round 46 wave-2 verdicts) | “C1 \| calibration \| not admitted — frozen predicate met, frozen kill rule fires” |
| operator rules | `file:///home/vgpnk/.omp/agent/RULES.md` | “Any agent … installs or updates any tool that helps its task” |
| lane report | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2ExecControls.md` | “each receipt is embedded verbatim above with its digest” |
| lane report | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ConnPattern.md` | “scratch was removed on command completion” |
| lane report | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2PosControl.md` | “That is the wave artifact hash, not the frozen `plans/polyglot_c_py_probe.py` hash.” |
| lane report | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest.md` | “All paths are under the lane wave dir (untracked; the L1 integrates).” |
| lane report | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecCounter.md` | “a read-only copy was also dropped at … for the controls seat, which asked for the instrument verbatim” |
| lane report | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C2Scope.md` | “One live clone at the freeze commit under my scratch” |

## Limits

- **Snapshot, not closure.** 7 seats had no report at `09:02:08`; five of them stalled after cloning (F17), one was
  still writing, one had gone quiet. Their boundary behaviour is unobserved beyond their scratch state. Their
  scratch footprints are shared clones (verified `--shared` on every sampled tree) and nothing they wrote is
  visible outside scratch. A late seat can still create a defect this report does not contain.
- **No process audit trail.** Attribution inside the lane rests on file content and mtimes. F8 shows `.git`
  mtimes are unreliable for the 08:36 window; F6 is attributed by self-identification only.
- **Sibling-lane writes are out of scope.** Files changed in `kasegi`, `mado`, `chousa`, `kaidoku`, `souji`,
  `tabi` during the wave belong to those lanes' own rounds; no round-48 artifact references a write there. I did
  not audit their rounds.
- **No scored execution, no fixture.** This seat ran no counter, probe, gate, fence, mutation or fixture Git
  write; no test of the C1/C2 predicates is claimed. Source-faithfulness review of the claims is other seats'
  work, except the single digest mismatch I verified (F9).
- **Scratch cost.** 25 GB under `/fast/scratch/hyaku/kengaku-r48` at 08:40 (30 % of `/fast`); largest single seat
  `R48C1ExecControls` 3.9 GB across 7 `--shared` clones. Within the rule (no full mirror; one shared clone per
  tree), but the control seat's footprint is the wave's main disk exposure.
- **Scratch removed.** `/fast/scratch/hyaku/kengaku-r48/R48SentHygiene` was deleted before yield; this report
  cites only lane and wave-dir bytes.

VERDICT: **no boundary breach blocks the wave.** Stage-1 freeze is committed, byte-identical to the worktree and
predates every observed measurement; no scored R48 counter/probe run exists and none was made. Two defects need L1
action before stage 2 — pre-stage-2 non-dry control runs whose receipts now sit in `w1/` and must never become the
`claims/` receipts (F1), and a receipt citing a mutable sibling scratch artifact whose measured bytes are already
superseded (F2) — plus low-severity scope deviations (F4 false cleanup claim; F5 three artifact dirs; F6 production
write attributable to the L1), an operability gap (five seats stalled after cloning, F17), and the frozen-text
probe-digest mismatch (F9). No secrets, no `/tmp` evidence paths, no fleet-repo touches, no duplicate writer paths,
no lane production edit by any wave seat. The 08:36 `.git` rewrite (F8) is host-level, not a seat.
