# C2ExecClosedChecks — executor seat, kengaku round 51 (hyaku run 11)

REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7 (lane `master`; clean-clone measurement,
`git -C <clone> rev-parse HEAD`; stage-1 freeze `e07f131cf7037e58a21db6e1f3986cf401ad257c`,
`plans/round51_routing.py` byte-identical between the two: `git diff --stat e07f131..HEAD -- plans/round51_routing.py plans/round51_surfaces.py plans/round51-surfaces.json` → empty).

Item: run the `check` command of every CLOSED row (41 rows) the same way and classify into
`still-verifies` / `no-longer-verifies` / `stale-check` / `not-a-check`, with counts and ids.

**Axes named:** (1) *check eligibility under the frozen counter* — does the row's `check` exit 0
when the frozen instrument runs it, which is what `disposition: fixed-verified` requires;
(2) *check falsifiability* — does the command actually fail when the artifact it names is absent,
which separates a real check from a vacuous one. Axis (1) is the C2 predicate's `CHECK_FAILED`;
axis (2) is the difference between an honest `fixed-verified` and a false one.

---

## 0. Incident disclosure (my own defect, repaired — read this first)

While building a discrimination probe I used a symlink farm of the lane. Directory symlinks made
`unlink()`/`write_text()` resolve **through** them into the real lane: eight tracked files were
truncated to 0 bytes in the lane working tree
(`corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`,
`corpus/lessons/round-42.md`, `corpus/routed-findings.jsonl`, `plans/round42_c1_verify.py`,
`plans/routed_open.py`, `plans/scratch_guard.py`).

Repair, immediately after detection, without any git mutation (`git show HEAD:<path>` + `mv`):

```
corpus/QUALITY.md                              want=47fa517e6b828f61da9045d37e0c082f98652e72 got=same size=108725
corpus/SOURCES.md                              want=6a6f4954b1a90e55bb67d624b5bc9e0bf2af7350 got=same size=142293
corpus/knowledge/tb2-circuit-fibsqrt-grader.md want=671e038ac5b53dc6b96667fda644f3d35325f0ce got=same size=51550
corpus/lessons/round-42.md                     want=169de65b000732eb6d29c5eb350731a35f3921a3 got=same size=28895
corpus/routed-findings.jsonl                   want=2e819d7aa175137a43129edba932c3f853a51574 got=same size=48957
plans/round42_c1_verify.py                     want=775c9734c00ef217bc610ccc9256d75254a79de9 got=same size=35983
plans/routed_open.py                           want=3895c024219fe66e04a90b23b62796a286cb138e got=same size=10877
plans/scratch_guard.py                         want=650de39dd355f293d19e91a4202457e8d394bccc got=same size=25643
```

Three of the `.py` files lost their exec bit through the redirect; restored with
`chmod 755` (index mode `100755` for all three). Final state:

```
$ git -C <lane> status --porcelain | grep -v '^?? '
CLEAN: no modified tracked files, no mode changes
$ wc -l corpus/routed-findings.jsonl
71 corpus/routed-findings.jsonl
$ git hash-object corpus/routed-findings.jsonl
2e819d7aa175137a43129edba932c3f853a51574
```

The lane is byte-identical to HEAD at `4090c3d`. Everything below was then measured against a
**real copy farm** (`cp -a` of the working tree into my scratch, guarded by
`assert not str(path.resolve()).startswith(str(LANE))`) and a `git clone --shared` clean clone;
no lane path is writable by the probe any more. Residual risk: if a sibling seat read one of the
eight files in the ~2-minute window it would have seen an empty file — the window closed before
any of my own measurements and the hashes above are the proof of the restored state.

---

## 1. Commands run (exact)

All with `TMPDIR=/fast/scratch/hyaku/kengaku-r51/C2ExecClosedChecks/work`; lane read-only.

1. Baseline reproduction of the frozen before-receipt:
   `python3 plans/round51_routing.py --lane . --run-checks`
   → `LEDGER corpus/routed-findings.jsonl rows=71` / `CHECKS present=61 absent=10` /
   `VERIFIED ran=0 passed=0 failed=0` / `PREDICATE R51-C2 fail` — identical to
   `.ufo/waves/round-51/claims/c2-before.txt`. The environment reproduces the frozen baseline.
2. **Counter-faithful run of every closed check** (`run_closed.py`), i.e. the frozen
   instrument's own invocation (`round51_routing.py:120-125`):
   `bash -lc <check>`, `cwd=<scratch work dir>`, `env TMPDIR=<scratch> LANE=<lane>`, `timeout=60`.
3. **Lane-cwd run of the same 41 commands**: identical except `cwd=<lane>`.
4. **Falsifiability probe** (`probe2.py`): each check re-run in the copy farm with every lane
   artifact it names replaced by an empty file/empty dir (executed `.py` scripts deleted instead
   of emptied, since an empty script is a no-op success).
5. **Counter-level control** (`probe-ledger.jsonl`): the 71 real rows, every row given
   `owner`, closed rows `disposition: fixed-verified`, non-closed `accepted-risk`, run with
   `python3 plans/round51_routing.py --lane . --ledger <clone>/corpus/probe-ledger.jsonl --run-checks`
   inside a clean `--shared` clone, and again with a scratch copy of the counter patched only at
   `cwd=str(tmp)` → `cwd=str(lane)`.
6. **Close-receipt resolution** for all 41 closed rows using the counter's own `fixed-historical`
   rule (`round51_routing.py:143-155`: first whitespace token, stripped of `,`, must be a
   `[0-9a-f]{7,40}` commit or an existing lane path).

## 2. Result — counts

Primary partition (the item's literal definition, exit code under the frozen invocation):

| class | count |
|---|---|
| `still-verifies` (exit 0) | **2** |
| `no-longer-verifies` (nonzero) | **39** |

Refined partition (after the falsifiability probe, which overrides exit code where a row exits 0
vacuously):

| class | count | ids |
|---|---|---|
| `still-verifies` | **1** | R39-R5 |
| `no-longer-verifies` | **0** | — |
| `stale-check` | **38** | see table |
| `not-a-check` | **2** | R42-R3-03, R45-S5-7a |

Exit-code histogram under the frozen invocation: `0 → 2`, `1 → 3`, `2 → 36`. The `2`s are grep's
"file not found" exit status, i.e. path resolution, not a failed assertion — verbatim:
`R39-R1 rc 2 | grep: SKILL.md: No such file or directory`;
`R42-R2 rc 1 | python3: can't open file '<scratch>/work/plans/routed_open.py': [Errno 2] No such file or directory`.

**No closed row has regressed in substance**: all 41 checks exit 0 at lane cwd, and 39 of them
also fail the falsifiability probe (they really do read the artifact they name). The 39 nonzero
rows are *stale as commands*, not *unfixed as defects*.

## 3. The decisive structural finding — the frozen counter cannot pass a relative-path check

The frozen instrument runs each check with `cwd=str(tmp)` (a fresh temp dir) and only exports
`LANE`. **Not one of the 41 closed checks uses `$LANE`; all 41 use lane-relative paths.** So the
check leg of C2 is unreachable as frozen, no matter how the ledger is attributed. Measured on a
clean clone with a perfectly attributed probe ledger (41 × `fixed-verified`):

```
=== FROZEN counter (cwd=scratch, as written) ===
LEDGER corpus/probe-ledger.jsonl rows=71
CHECKS present=61 absent=10
VERIFIED ran=41 passed=2 failed=39
  DETAIL CHECK_FAILED R39-R1 fixed-verified but check exits nonzero
  ...
=== same ledger, counter patched to cwd=lane (single line: cwd=str(tmp) -> cwd=str(lane)) ===
VERIFIED ran=41 passed=41 failed=0
  DETAIL CHECK R40-R5 has no check command          (and 9 more, all non-closed rows)
PREDICATE R51-C2 fail
```

Consequence for the C2 after-target (`CHECK_FAILED 0` over every `fixed-verified` row): the L1
must either (a) amend the frozen counter so checks run with `cwd=lane` (measured: `passed=41
failed=0`, and the only remaining `CHECK` details are the 10 non-closed rows that carry no check
command at all), or (b) disposition 39 closed rows away from `fixed-verified`. Option (b) is
constrained by §4. Option (a) is a one-line change to a frozen instrument and therefore needs to
be named as a freeze amendment in `plans/round-51-claims.md`, not slipped in.

## 4. Second finding — 23 of 41 `close` fields do not resolve under the counter's own rule

If a counter-failing closed row is re-dispositioned to `fixed-historical`, the counter checks that
`close`'s **first token** is a commit or an existing path. Only **18 of 41** closed rows pass that
test today. The 23 failures, with the token the counter actually reads and the mechanical repair
where one exists (measured, not proposed):

| id | first token (as read) | repair |
|---|---|---|
| R39-R5 | `measured` | none — needs a real path/commit |
| R40-R1 | `F1-F4` | `.ufo/waves/round-42/claims/frozen-digests.txt` |
| R40-R2 | `.ufo/waves/round-41/build-spec.json:5` | strip `:5` |
| R40-R3 | `round` | `SKILL.md` |
| R40-R4 | `.ufo/waves/round-41/claims/control-c1-nothing.txt:28` | strip `:28` |
| R42-R2 | `children` | `plans/scratch_guard.py` |
| R42-R4 | `corpus/QUALITY.md:759` | strip `:759` |
| R40-R1.1 | `round-42` | `plans/round42_c1_verify.py` |
| R42-R3-11/12/13/15/17 | `round-43` | `corpus/lessons/round-42.md` |
| R42-R3-20/23 | `round-43` | `corpus/QUALITY.md` |
| R42-R3-31 | `round-43` | `SCORECARD.md` |
| R42-R3-38/39/40 | `round-43` | `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` |
| R45-S5-1, R45-S5-2 | `c1ec334c:` | bare `c1ec334c` **is** a commit (`git cat-file -e`) — drop the colon |
| R45-S5-3 | `round-46` | `LOG.md` |
| R45-S5-5 | `round-46` | `.ufo/waves/round-46/integrate/c2-landing.txt` |

So the "must become `fixed-historical`" route needs its `close` rewritten to lead with the
path/commit as well as its disposition — 22 of the 23 are a mechanical leading-token fix.

## 5. Per-row table

`counter` = exit code under the frozen invocation; `lane` = same command at lane cwd;
`falsif` = falsifiability probe (`pass` = still exits 0 with the named artifact emptied, i.e. the
command is not a check); `close` = does `close`'s first token resolve (counter's rule).

| id | counter | lane | falsif | close | first token | class |
|---|---|---|---|---|---|---|
| R39-R1 | 2 | 0 | fail | yes | `ec17216` | stale-check |
| R39-R5 | 0 | 0 | n/a | NO | `measured` | still-verifies |
| R40-R1 | 2 | 0 | fail | NO | `F1-F4` | stale-check |
| R40-R2 | 2 | 0 | fail | NO | `.ufo/waves/round-41/build-spec.json:5` | stale-check |
| R40-R3 | 2 | 0 | fail | NO | `round` | stale-check |
| R40-R4 | 2 | 0 | fail | NO | `.ufo/waves/round-41/claims/control-c1-nothing.txt:28` | stale-check |
| R42-R2 | 1 | 0 | fail | NO | `children` | stale-check |
| R42-R4 | 2 | 0 | fail | NO | `corpus/QUALITY.md:759` | stale-check |
| R40-R1.1 | 2 | 0 | fail | NO | `round-42` | stale-check |
| R42-R2.1 | 1 | 0 | fail | yes | `plans/scratch_guard.py` | stale-check |
| R42-R2.2 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-01 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-03 | 0 | 0 | **pass** | yes | `77ea425a` | **not-a-check** |
| R42-R3-04 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-10 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-11 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-12 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-13 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-15 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-17 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-20 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-21 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-22 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-23 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-24 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-25 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-28 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-29 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-30 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R42-R3-31 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-38 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-39 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-40 | 2 | 0 | fail | NO | `round-43` | stale-check |
| R42-R3-41 | 2 | 0 | fail | yes | `77ea425a` | stale-check |
| R45-S5-1 | 2 | 0 | fail | NO | `c1ec334c:` | stale-check |
| R45-S5-2 | 2 | 0 | fail | NO | `c1ec334c:` | stale-check |
| R45-S5-3 | 2 | 0 | fail | NO | `round-46` | stale-check |
| R45-S5-4 | 2 | 0 | fail | yes | `corpus/lessons/round-46.md` | stale-check |
| R45-S5-5 | 2 | 0 | fail | NO | `round-46` | stale-check |
| R45-S5-6 | 2 | 0 | fail | yes | `plans/round-46-claims.md` | stale-check |
| R45-S5-7a | 1 | 0 | **pass** | yes | `plans/round46_c1_verify.py` | **not-a-check** |

### The two `not-a-check` rows, with evidence

- **R42-R3-03** — `grep -q ':96' <entry> || ! grep -q 'dropped if that fails' <entry>`.
  Under the frozen invocation it exits 0 **because both greps failed on a missing file** and the
  `|| !` branch inverted that into success — verbatim stderr:
  `grep: corpus/knowledge/tb2-circuit-fibsqrt-grader.md: No such file or directory` (twice).
  At lane cwd branch 1 is genuinely true (`grep -q ':96'` → rc 0), so the fact holds, but the
  command can never fail when the artifact is missing: it is the one row that would be granted a
  **false** `fixed-verified` today.
- **R45-S5-7a** — `test -f .ufo/waves/round-46/claims/control-c1-fence-keyed_name.txt`. The
  receipt is 19654 bytes and exists; the probe empties it and the check still passes, so it
  asserts presence only and never reads the 21 failing controls the close claims. Presence-only
  receipt tests cannot carry `fixed-verified`. (Its open siblings R45-S5-7b…7e have no `check`
  at all — 4 of the 10 `CHECKS absent` rows — same receipt pattern; out of my item's scope.)

### `still-verifies` — R39-R5

`test ! -e /fast/scratch/hyaku/kengaku-r39` — absolute host path, independent of cwd, exits 0
under the frozen invocation. Falsifiable in principle (the check fails if that directory exists);
not probed because the path is outside my scratch and creating it would be a host mutation. Note
it verifies a *host scratch* fact, not a lane artifact: it is the only closed row whose check
survives the frozen cwd, and it does so by accident of being absolute.

## 6. Limits

- One invocation per row per mode; checks were not repeated to look for flakiness (none of the 41
  touches the network, a model endpoint, or the clock).
- The falsifiability probe replaces the named artifact with an empty file/dir, which proves the
  command *reads* it — not that the grep literal is the right literal for the claim. A row can be
  falsifiable and still assert the wrong thing; that is the critic axis, not mine.
- `close` resolution was measured with the counter's first-token rule only; a close can be
  semantically fine and still fail that rule, which is exactly what §4 lists.
- Non-closed rows (27 open, 2 refused, 1 blocked) were only touched where the counter control
  needed a legal disposition; their checks were not run and are not classified here.
- The 10 `CHECKS absent` rows are all non-closed (verified: every closed row has a non-empty
  `check`), so they are outside this item but they block the C2 predicate independently.

## 7. Tooling

No installs, no upgrades, no pacman transaction. `python3` (3.14) and `git` already present; the
only tools created are two throwaway scripts in my scratch (`run_closed.py`, `probe2.py`), deleted
with the scratch tree.

Scratch `/fast/scratch/hyaku/kengaku-r51/C2ExecClosedChecks` (pristine+copy farm 703M, shared
clone, probe ledger) removed after this report was written; no receipt cited above lives only in
scratch — every number in it is reproduced by the commands in §1 and quoted verbatim here.

VERDICT: PASS-WITH-FINDINGS — 41 closed checks run; 2 exit 0 under the frozen invocation
(R39-R5 sound, R42-R3-03 vacuous), 39 nonzero of which 38 are stale-check and 1 (R45-S5-7a) is
not-a-check; 0 rows regressed in substance (41/41 exit 0 at lane cwd). Eligibility verdict for
`fixed-verified`: **1 row today** (R39-R5); **41 rows** if the counter is amended to run checks
with `cwd=lane` (measured `passed=41 failed=0` on a clean clone at 4090c3d). The `fixed-historical`
route is blocked for 23 rows until their `close` leading token is rewritten (22 mechanical).
My own defect: the symlink-farm probe truncated 8 tracked files in the lane; restored to HEAD
byte-for-byte (hashes in §0) and the lane is clean.
