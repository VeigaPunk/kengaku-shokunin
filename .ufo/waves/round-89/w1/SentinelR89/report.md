# SentinelR89 — adversarial security review of the round-89 instruments (read-only)

Seat: SentinelR89 (sentinel, leaf). Lane `kengaku-shokunin`, measured tip `a9b8a1a00b6a5ab5206be4d377dba439e02f8244`, freeze `d1c4f1b04bb39d18967075974b5984238b7c97f7`.

Method: every forgery was built in a scratch clone (`git clone --no-hardlinks`, detached/branch checkouts, throwaway identity `seat@scratch` used only inside that clone, toplevel asserted before every git write). No production file, branch, index, ledger or receipt in the lane was written. Counters were run with `--lane` only on the scratch clone. Read in full: `plans/round89_polyglot_probe.py` (277 lines), `plans/round89_c1_replay.py` (288), `plans/round89_claim_figures.py` (629), `plans/round-89-claims.md`, the captured grader `corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py`, and all eight `result` blobs of `plans/round89-cases.json`.

**Environment caveat (I-3).** During the review the host's `user.max_user_namespaces` changed to `0` (`cat /proc/sys/user/max_user_namespaces` → `0`; `bwrap --unshare-all ... /usr/bin/true` → `bwrap: Creating new namespace failed: nesting depth or /proc/sys/user/max_*_namespaces exceeded (ENOSPC)`). Every bwrap run after that point fails. Runs that needed bwrap were executed before the change; their outputs are kept verbatim in `transcripts/in-session-sandbox-and-forgery.txt`. Runs made after the change are cited only where they reached a passing or failing predicate without needing the sandbox (the C2 runs, the echo-probe and ledger-only C1 runs, the stage sweep, the BASE do-nothing run); the three L6-dependent runs made during the outage are kept under `transcripts/outage-confounded/` and are not cited as results. I did not change the sysctl.

## Summary

| ID | Sev | Finding | Key evidence (transcript) |
|---|---|---|---|
| H1 | High | C2 record table is not pinned; regenerating it in the same commit defeats the deleted-figure check | `forge-c2-ii-regen-table.txt`: `PREDICATE R89-C2 pass` after a before-figure deletion |
| H2 | High | C2 counter bytes are unpinned; a KNOWN edit plus doctored claim passes the predicate | `forge-known-kv-counter-edit.txt`: `PREDICATE R89-C2 pass` |
| H3 | High | C1 `TRUSTED_TOOL_SHA` pins the probe, but the pin lives in the mutable counter; echo-probe forgery passes | `forge-f1-echo-same-commit-pin.txt`: `PREDICATE R89-C1 pass` |
| M1 | Medium | `PREDICATE R89-C2` omits the controls that the frozen predicate says it includes | `forge-known-kv-controls.txt`: `PREDICATE R89-C2-CONTROLS fail` on the tree whose predicate passed |
| L1 | Low | A hostile case can stall the probe 120 s, then crash it uncaught (exit 1) | in-session V-denial result (§4) |
| L2 | Low | Empty or `"."` case paths pass validation, then crash in `stage()` | `stage-validation.txt` |
| L3 | Low | Controls: "red" means `rc != 0`, and each control is red for a check other than the one it names | `tip-c2-controls.txt` |
| L4 | Low | `claims=17` is a string literal in both emitted summary lines | `round89_claim_figures.py:527,532` |
| L5 | Low | Prior counters run from the lane working tree, not the BASE blobs (code-read, not executed) | `round89_claim_figures.py:220` |
| L6 | Low | Case binaries can write to the harness's stdout via `/proc`; the parser fails closed, no forgery found | in-session V1/V2 (§4) |
| I-1 | Info | Containment verified (flags, reach, env, network, writes) | in-session containment run (§1) |
| I-2 | Info | No credential, env or HOME read in the instruments; receipt holds only paths, hashes and host versions | grep (§3) |
| I-3 | Info | Host user namespaces disabled during the review; bwrap-dependent C1 re-run blocked | `/proc/sys/user/max_user_namespaces` = 0 |
| I-4 | Info | Lane working tree and HEAD are not mine: `M corpus/lessons/round-89.md`; HEAD now `00462b59` | `git status --porcelain` (read-only) |
| I-5 | Info | Dangling commit `2169b673` (parent = freeze commit) carries the record table; not reachable from any ref | `git branch -a --contains 2169b673` (empty) |

Findings counted for the verdict: 3 High, 1 Medium, 6 Low = 10.

---

## 1. Containment (item 1)

**bwrap flags** (`probe.sandbox_argv`, `plans/round89_polyglot_probe.py:176-189`; printed verbatim by `sandbox_argv` in scratch):

```
/usr/bin/bwrap --unshare-all --die-with-parent --new-session
  --ro-bind /usr /usr --ro-bind /etc /etc
  --symlink usr/bin /bin --symlink usr/bin /sbin --symlink usr/lib /lib --symlink usr/lib /lib64   (only if the host path is a symlink)
  --proc /proc --dev /dev
  --bind <case>/app /app          # the only writable host-backed mount
  --dir /tests
  --ro-bind <capture> /tests/test_outputs.py
  --ro-bind <case>/harness.py /harness.py
  --clearenv --setenv PATH /usr/bin --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --chdir /app /usr/bin/python3 -I -B /harness.py
```

`run_case` launches it with `env={"PATH": "/usr/bin"}` and `timeout=120` (`probe.py:200-201`). Nothing is bound from `$HOME`, `/home`, `/root`, `/tmp`, `/fast`, the lane tree, or the fleet root. There is no `--ro-bind / /`, so the sandbox root is an empty tmpfs.

**What the case harness can reach (observed, in-session).** Diagnostic harness run through `sandbox_argv`, caller env carrying `SENTINEL_CANARY=should-not-appear`:

- `uid_gid = [1000, 1000]`; `env_keys = ['LANG','LC_ALL','PATH','PWD']`. The canary and any host variable are absent.
- `ls_home = ERR FileNotFoundError: '/home'`; `tmp_exists = False`; `fast_exists = False`; `lane_exists = False`; `var_list = ERR ... '/var'`; `run_list = ERR ... '/run'`.
- `write_etc = ERR OSError [Errno 30] Read-only file system: '/etc/zz_sentinel'`; `write_usr = ERR OSError [Errno 30] Read-only file system: '/usr/zz_sentinel'`; `write_app = 1` (only `/app` writable).
- `read_etc_passwd_bytes = 1819` (`/etc` is readable: world-readable host config, see I-2).
- `proc_pids = ['1','2']` (own PID namespace); `connect_1111_53 = ERR ... Network is unreachable`; `connect_loopback_22 = ERR ConnectionRefusedError` (loopback only, no host network).
- After the run, on the host: `/etc/zz_sentinel` absent, `/usr/zz_sentinel` absent, host case-app holds only the sandbox's own `zz_sentinel`.

**Staged paths cannot escape the case directory.** The only validation is in `load_inputs` (`plans/round89_polyglot_probe.py:157-161`):

```python
for rel, content in files.items():
    if not isinstance(rel, str) or ".." in rel.split("/") or rel.startswith("/"):
        raise SetupDefect(f"wrong-table path {case_id}:{rel}")
    if not isinstance(content, str):
        raise SetupDefect(f"wrong-table content {case_id}:{rel}")
```

and `stage` (`:169-173`) writes `app / rel` with `write_bytes(content.encode("utf-8"))`. Tested against modified case tables in scratch (`transcripts/stage-validation.txt`, no sandbox needed):

- rejected (`SetupDefect: wrong-table path`): `../escape.txt`, `/tmp/abs.txt`, `polyglot/../../escape.txt`, `a/..`, `..`, `x/../../y`
- accepted and written inside `app`: `polyglot/./main.rs`, `a//b`, `polyglot/..x`, `polyglot\..\..\x` (one component on Linux), `polyglot/...`, `polyglot/main.rs\n../x`
- accepted, then crash (see L2): `""`, `"."`

**Symlinks are impossible.** The table's `content` is type-checked as `str` (line 160), keys are type-checked as `str`, and `stage` only ever calls `write_bytes` on regular paths inside a freshly created `app/`. JSON has no symlink type, and nothing stages a link. Confirmed by reading and by the `isinstance` checks above.

## 2. Forgery surface (item 2)

C1 pins: `TRUSTED_TOOL_SHA` (`round89_c1_replay.py:46`) pins the probe bytes only (L9, `:166-170`). No leg hashes the counter, the claim file, or the table relative to the freeze commit, except L4 (`FREEZE_REV` table comparison, `:147-164`). C2 pins nothing: no hash of the counter, of `KNOWN`, or of the record table (`pinned_records`, `:356-361`, reads `{rev}:{RECORD_TABLE}`).

| Forgery (scratch commit) | Edited | Result | Refused by |
|---|---|---|---|
| F1 echo probe, `TRUSTED_TOOL_SHA` rewritten in counter in the same commit, fresh receipt | probe, counter, receipt | `TARGET ... located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0` / `PREDICATE R89-C1 pass` (rc 0) | **nothing** (H3) |
| F1b echo probe only, pin untouched | probe, receipt | `DEFECT L9-tool probe sha=52769fd5a9b202d8 != TRUSTED_TOOL_SHA 03c202f5072e8aa5` / `fail` (rc 1) | L9 |
| F2 receipt `CASE exact predicted=P observed=F` | receipt | `DEFECT L5-vectors exact observed=F predicted=P`, `DEFECT L6-reproduce ... differs` (in-session, pre-outage) | L5, L6 |
| F3 `LANE_TIP` = orphan commit | receipt | `DEFECT L3-tip LANE_TIP 1e4c215a919d is not an ancestor of f0165e5b4a23` (in-session) | L3 |
| Ledger-only (receipt removed) | receipt | `DEFECT L1-receipt ... absent` (rc 1) | L1 |
| C2-i deleted before-figure, table stale | claims | `DEFECT F7-record-missing ...` ×7, `PREDICATE R89-C2 fail` (rc 1) | F7 |
| C2-ii deleted before-figure, table regenerated from that commit | claims, table | `DEFECTS n=0`, `PREDICATE R89-C2 pass` (rc 0) | **nothing** (H1) |
| FK doctored claim + KNOWN edit + regenerated table | claims, counter, table | `MISMATCH KNOWN R87-C1 kv:defects claimed==9 measured 3`, `PREDICATE R89-C2 pass` (rc 0) | **predicate: nothing** (H2); `--controls` refuses it (M1) |
| Counter file rewritten to print `PREDICATE ... pass` (no other edit) | counter | not run; the counter is hashed by nothing, so the trivial stub passes by construction | none (code-read) |

Each leg does its job for the edit it names. The weakness is that the pins live in files that a single commit can rewrite. Verified commits: `transcripts/forgery-provenance.txt` (branch → commits → `--stat`).

## 3. Confidentiality (item 3)

- Credential, environment and home reads: `git grep -n -E "os\.environ|getenv|expanduser|Path\.home|HOME|\.ssh|credential|token"` over the three instruments at `a9b8a1a` returns only two `token` loop variables (`round89_claim_figures.py:184,188`). No env, HOME, cookie, token or credential is read.
- Subprocess environments: C1 and C2 counters and the probe's L6 re-run use `env={"PATH": "/usr/bin", "TMPDIR": ...}`. `git()` helpers and the probe's `git_out` inherit the caller environment; they only read commit metadata.
- Receipt content (`corpus/evidence/round89/polyglot-rust-c-probe.txt`, lines 1-25): member, relative paths, SUBJECT_SHA, CASE_TABLE_SHA, TOOL_SHA, `HOST_PYTHON Python 3.14.8`, `HOST_OPENSSL OpenSSL 3.6.5 ...`, `LANE_TIP`, `WORKTREE clean`, and `COMMAND ... --work /fast/scratch/hyaku/kengaku-r89/probe-run` (an absolute scratch path, Info). `git grep -n -I -E "/home/vgpnk|vgpnk|/root/|\.ssh|\.netrc|GITHUB_TOKEN|AWS_|PRIVATE KEY|Authorization|cookie"` over the round-89 evidence, instruments and table: no hits.
- `tool_label` (`probe.py:85-90`) writes an absolute probe path into the stamp when the probe runs outside the lane. Not triggered by the frozen receipt.

## 4. Integrity of the observation (item 4)

The probe runs the grader in a sandbox whose stdout is the harness's stdout. The grader's own `subprocess.run` calls use `capture_output=True` and `os.popen(...).read()`, so compiled binaries cannot write to the harness through the grader's pipes. They can still reach the harness's fd 1 through `/proc/<harness pid>/fd/1`, because the sandbox shares a PID namespace. Tested through `probe.run_case` with an adversarial `main.rs` (in-session, pre-outage):

- **V0** (control, no injection, Rust prints a wrong value): `run_case -> [['test_fibonacci_polyglot', 'F', 'AssertionError']]`. Real verdict F is reproduced.
- **V1** (fake `PAYLOAD {"tests": [["test_fibonacci_polyglot", "P", ""]]}` written to `/proc/<ppid>/fd/1`, then the real line): `SetupDefect: sandbox-protocol`. The parser's `len(lines) != 1` check fails closed.
- **V2** (same fake line, then `kill -9` on the harness so the real line never prints): `SetupDefect: sandbox-exit=137`. bwrap reports the kill, so this also fails closed.
- **Denial** (`kill(ppid, SIGSTOP)`): `UNCAUGHT TimeoutExpired` after 120 s (L1).

No forged accepted verdict was produced. Acceptance would need the real line suppressed while bwrap still returns 0, and no such path was found. The `PAYLOAD` integrity guarantee is therefore fail-closed, not authenticated. Routing: the verdict channel should be a private file or descriptor with a nonce, not stdout that case code can reach.

## Findings

### H1 (High) — C2 record table is not pinned; a deletion committed with a regenerated table passes

- Claim (d), `plans/round-89-claims.md:42-43`: "the record table is itself pinned to its blob sha at the freeze commit." Code: `round89_claim_figures.py:356-361` `pinned_records` reads `f"{rev}:{RECORD_TABLE}"` at the measured rev, and no blob sha appears anywhere in the counter (`grep -n "sha\|SHA\|blob"` hits only `git show` lines 236, 329, 357, 417 and `write_bytes` at 240).
- The table is not in the freeze commit: `git cat-file -e d1c4f1b04bb39d18967075974b5984238b7c97f7:plans/round89-q66-records.json` → `fatal: path 'plans/round89-q66-records.json' exists on disk, but not in 'd1c4f1b04bb39d18967075974b5984238b7c97f7'`. The first commit carrying it is `2169b673` (parent `d1c4f1b0`, unreachable from any ref), with the same bytes as tip (sha256 `f72db459f40755c8…`). Tip's copy comes from `0e6bb05`. The claim's freeze list (line 3) names only the claims file and the case table.
- Exploit, two commits: (1) delete the R85-C1 Before sentence with the counter's own `_drop_before`; (2) run `python3 plans/round89_claim_figures.py --lane <clone> --rev <commit1> --work <w> --freeze-records` and commit the result as the table.
  - Stale table (`forge-c2-i-stale-table.txt`, rc 1): `RECORDS ... records=49 ...`, seven `DEFECT F7-record-missing ('R85-C1', 'kv', ...)`, `DEFECTS n=7`, `PREDICATE R89-C2 fail`.
  - Regenerated (`forge-c2-ii-regen-table.txt`, rc 0): `RECORDS claims=17 files=8 records=49 checked=49 matched=48 mismatches=1 prose=0`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`. The table has zero `R85-C1` rows.
- Impact: round-88 finding 2 (a deleted before-figure is a defect) holds only against a stale table. The kill rule in the claims (lines 57-59: "any record-table divergence at the tip", "any edit to a frozen ... record table ... after commit A") cannot fire, because the counter never compares against the freeze commit.
- Route: frozen element (d) cannot be satisfied as written. A working fix pins the table blob (`f72db459f40755c8…`, sha256) in the counter and checks that the freeze commit's table is unchanged. Not edited here.

### H2 (High) — C2 counter bytes are unpinned; a counter-side KNOWN edit with a doctored claim passes

- `KNOWN` lives in the counter (`round89_claim_figures.py:97-99`). Nothing pins the counter's bytes. The prior counters run from the working tree (`:220`, see L5).
- Exploit (`forge-known-kv-counter-edit.txt`, rc 0): doctor `plans/round-87-claims.md` `defects=7`→`defects=9`, change `KNOWN` to `("R87-C1", "kv:defects", "claimed==9", 3)`, regenerate the table from that commit.
  - `MISMATCH KNOWN R87-C1 kv:defects claimed==9 measured 3`, `RECORDS ... records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`.
- Impact: anyone able to commit to the lane can make R89-C2 pass with a doctored claim. The main predicate has no leg that refuses a counter edit. Only the separate `--controls` run notices (M1).

### H3 (High) — C1's `TRUSTED_TOOL_SHA` pins the probe, but the pin lives in the mutable counter; an echo-probe forgery passes

- `round89_c1_replay.py:46` `TRUSTED_TOOL_SHA = "03c202f5072e8aa55636592fed9c2fb64b6a7684ec853f8968428e73d50df898"`; L9 (`:166-170`) compares probe bytes only.
- Exploit (`forge-f1-echo-same-commit-pin.txt`, rc 0): replace the probe's `payload = run_case(staged, work, case["result"]["files"])` (probe line 226) with `payload = {"tests": [[TESTS[0], case["predicted"], ""]]}`; rewrite the counter's `TRUSTED_TOOL_SHA` to the echo probe's sha (`52769fd5a9b202d8…`) in the same commit; mint a receipt from that tree; commit it.
  - `TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`.
- Control F1b (probe changed, pin untouched, `forge-f1b-probe-only.txt`, rc 1): `DEFECT L9-tool probe sha=52769fd5a9b202d8 != TRUSTED_TOOL_SHA 03c202f5072e8aa5`. So L9 works against probe-only edits. The round-88 echo hole reopens for anyone who also edits the counter.
- Route: the claim says the pin closes the round-88 forged-probe hole. It closes only probe-only edits. The pin needs a freeze-commit anchor (`git show d1c4f1b:plans/round89_c1_replay.py`-style check, or the counter's blob sha pinned in a frozen file).

### M1 (Medium) — `PREDICATE R89-C2` does not include the controls that the frozen predicate says it includes

- Claim, lines 53-56: "pass iff ... the selftest battery exits 0, and all four control fixtures are red while the unmodified tip is green", and the same sentence must appear in "the counter's `PREDICATE R89-C2` line".
- Code: `main()` (`round89_claim_figures.py:622-625`) calls `controls()` only under `--controls`; the default path is `rc, _defects = run_check(lane, rev, work)` and `run_check` (`:461-535`) never invokes `controls`.
- Evidence: the H2 tree gives `PREDICATE R89-C2 pass` with rc 0 (`forge-known-kv-counter-edit.txt`). The same tree with `--controls` gives `CONTROL doctored-claimed green rc=0 defects=0 first=none` (×2 green) and `PREDICATE R89-C2-CONTROLS fail red=2 of 4 tip=green`, rc 1 (`forge-known-kv-controls.txt`).
- Route: the frozen predicate sentence and the counter disagree. Not edited.

### L1 (Low) — hostile case can stall the probe 120 s, then crash it uncaught (exit 1, not 2)

- `probe.py:200` `subprocess.run(..., timeout=120)`; `main()` (`:264-269`) catches only `SetupDefect`. In-session: a case binary sending SIGSTOP to its parent produced `UNCAUGHT TimeoutExpired` after 120 s. The probe prints no receipt and exits 1, which the documented contract (line 18) reserves for "a case observed != predicted". C1's L6 maps this to "no observation block", so the outcome is fail-closed.

### L2 (Low) — empty or `"."` case paths pass validation and crash in `stage()`

- `probe.py:158` tests only `..` components and a leading `/`, so `""` and `"."` pass. `stage` (`:169-173`) then raises `IsADirectoryError` uncaught. Reproduced without the sandbox: `transcripts/stage-validation.txt` → `'' | ACCEPTED by load_inputs | stage raised uncaught IsADirectoryError`. Same exit-code contract issue as L1.

### L3 (Low) — controls: "red" means `rc != 0`, and each control is red for a check other than the one it names

- `round89_claim_figures.py:575` `verdict = "red" if rc != 0 else "green"`: any uncaught exception counts as red.
- Tip (`transcripts/tip-c2-controls.txt`): `CONTROL doctored-claimed red rc=1 defects=4 first=F7-record-missing ('R87-C1', 'kv', 'defects', '=', 7)`; `CONTROL doctored-key red rc=1 defects=4 first=F7-record-missing (...)`. The KNOWN check (claim (a)) is never what makes a control red, so no control isolates it. The H2 tree shows (a) is exercised only indirectly.

### L4 (Low) — `claims=17` is a literal in both summary lines

- `round89_claim_figures.py:527` `emit(f"RECORDS claims=17 files=...")` and `:532` `emit(f"TARGET claims=17 ...")`. `CLAIMS` has 17 keys today; a claim added without editing the literal would still print 17.

### L5 (Low) — prior counters execute from the lane working tree, not the BASE blobs (code-read; not executed)

- `round89_claim_figures.py:216-223` `run_rev`: `cmd = [sys.executable, str(lane / counter)] + argv` with `--rev` passed as data. The `tree` mode (`run_tree`, `:226-250`) does use the BASE archive, but the `rev` mode does not. "Re-run at that claim's own BASE" therefore runs whatever counter bytes the lane working tree holds. Not executed; the effect is inferred from the code.

### L6 (Low) — the stdout channel is reachable from case code; the parser fails closed

- See §4. V1 and V2 show the injected line reaches the parser and the parser rejects it. Consequence: a hostile case can make its own replay fail, but no forged verdict was accepted in tested variants. Route: the verdict channel should not share stdout with code under test.

## 5. Info items

- **I-1 Containment:** verified as in §1. Host `/etc` and `/usr` are read-only; host `/etc/passwd` (1819 bytes) is readable from the sandbox.
- **I-2 Confidentiality:** no credential, env, cookie, token or HOME read (§3). The receipt carries host Python and OpenSSL versions and one absolute scratch path.
- **I-3 Environment (blocker for re-run only):** `user.max_user_namespaces = 0` on the host at review time. C1 tip re-run and every L6 re-run fail closed until user namespaces are restored. The in-session tip result (`transcripts/in-session-tip-c1.txt`, `TARGET ... located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`, rc 0) was captured before the change. I did not alter host settings. The operator should restore the sysctl or the orchestrator should re-run C1 after restoration.
- **I-4 Lane state (not mine):** `git -C kengaku-shokunin status --porcelain --untracked-files=no` → ` M corpus/lessons/round-89.md`; lane HEAD is `00462b59` (past the measured tip `a9b8a1a`). I did not touch either.
- **I-5 Provenance:** `2169b673` is a dangling commit (parent = freeze commit) that carries the same record-table bytes as tip. It explains how the table came to be absent at the freeze commit (see H1).

## 6. Frozen elements that look wrong (reported, not edited)

1. `round-89-claims.md:42-43` (d): "the record table is itself pinned to its blob sha at the freeze commit". The table is not at the freeze commit, and no sha pin exists in the counter.
2. `round-89-claims.md:53-56`: the R89-C2 predicate includes the controls. The implemented `PREDICATE R89-C2` line does not (M1).
3. `round-89-claims.md:57-59`: the C2 kill rule ("any edit to a frozen claims file, case table, record table, counter ... after commit A") cannot be enforced by a counter that is not itself frozen.
4. `round-89-claims.md:3`: the freeze list names the claims file and case table but not the record table or the counters. C2 depends on the first two. C1 depends on the counter, which is not frozen.

## 7. Reproduction and transcripts

All paths relative to `.ufo/waves/round-89/w1/SentinelR89/`:

- `transcripts/tip-c2.txt`, `transcripts/tip-c2-controls.txt`: tip predicate and controls, run in scratch during the outage. Both reached their passing predicates, so the counters they ran did not fail on the sandbox then. Several prior counters mention bwrap in their sources, so this is evidence from the run, not a source reading.
- `transcripts/in-session-tip-c1.txt`, `in-session-tip-c2.txt`, `in-session-tip-c2-controls.txt`: earlier in-session runs, copied from scratch.
- `transcripts/base-c1-do-nothing.txt`: `--rev 192e809d…` → `PREDICATE R89-C1 fail` (rc 1); counter run from the tip working tree.
- `transcripts/forge-f1-echo-same-commit-pin.txt`, `forge-f1b-probe-only.txt`, `control-ledger-only-no-receipt.txt`: C1 forgeries and control (no bwrap needed).
- `transcripts/forge-c2-i-stale-table.txt`, `forge-c2-ii-regen-table.txt`, `forge-known-kv-counter-edit.txt`, `forge-known-kv-controls.txt`: C2 forgeries.
- `transcripts/stage-validation.txt`: path-validation sweep (no bwrap).
- `transcripts/in-session-sandbox-and-forgery.txt`: bwrap-dependent results (containment, V0–V2, SIGSTOP, F2, F3), copied verbatim from pre-outage runs.
- `transcripts/forgery-provenance.txt`: scratch commits per forgery branch, `--stat`.
- `transcripts/outage-confounded/`: three runs made during the outage (`tip-c1`, `forge-f2`, `forge-f3`). Their `L6 rc=2` lines are the sandbox refusing; they are not evidence.

Scratch clone commands, for re-running after the sandbox returns (fresh clone at `a9b8a1a`):

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane && git -C $S/lane checkout -q a9b8a1a00b6a5ab5206be4d377dba439e02f8244
python3 plans/round89_c1_replay.py --lane $S/lane --rev a9b8a1a00b6a5ab5206be4d377dba439e02f8244 --work $S/w
python3 plans/round89_claim_figures.py --lane $S/lane --rev a9b8a1a00b6a5ab5206be4d377dba439e02f8244 --work $S/w
python3 plans/round89_claim_figures.py --lane $S/lane --rev a9b8a1a00b6a5ab5206be4d377dba439e02f8244 --work $S/w --controls
```

Tip reproduction in this review: `C1 rc=0 ... PREDICATE R89-C1 pass`; `C2 rc=0 ... RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, `DEFECTS n=0`, `PREDICATE R89-C2 pass`; `--controls`: `PREDICATE R89-C2-CONTROLS pass red=4 of 4 tip=green`. These match the frozen figures.

Scratch tree (`/fast/scratch/hyaku/kengaku-r89/SentinelR89/`) is deleted before yield. No tool installs were made. No network was used.

## Verdict

FINDINGS — 3 High, 1 Medium, 6 Low (10 defects). Coverage (C1 seventh replay, tip figures) and calibration (C2 tip figures) reproduce; the defects are in how their pins are anchored, not in the measured figures.

SEAT SentinelR89 VERDICT FINDINGS findings=10
