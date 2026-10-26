# R40SentinelCounter — security review of the round-40 instruments

Seat: sentinel (leaf). Surface: `plans/round40_c1_verify.py` (build child + tool runs) and
`plans/db_wal_probe.py` (captured `solve.sh` and per-case recipes). Frozen reference read in full:
`plans/round-40-claims.md` (freeze `bbb1095`), `claims/frozen-digests.txt` (11/11 digests re-verified `ok`),
`claims/control-c1-nothing.txt` (`killed=0 survived=21`). Nothing frozen was edited; nothing in the lane was
written. Receipts with every command and output: `R40SentinelCounter/receipts.md` (R1–R14). Scratch
`/fast/scratch/hyaku/kengaku-r40/R40SentinelCounter` removed at the end.

**Axes** (Godspeed): confinement (fs / net / pid), detection completeness (what a run can change and still print a
clean receipt), verdict attribution (mutant kills, grader verdicts), operability of each proposed fix.

---

## F1 — HIGH — the C1 sandbox is a *process* sandbox: whole host fs writable, network open

**Exploit path.** `plans/round40_c1_verify.py:303-304` builds every sandbox as
`bwrap --dev-bind / / --proc /proc --unshare-pid --die-with-parent --new-session` — no `--ro-bind`, no
`--unshare-net`, no `--unshare-ipc`, no uid/cap split. It is used for every module build (`:419`) and every tool run
(`:378`). So a `plans/battery40` module — non-author code on the critical path to `killed=21` — executes as the
operator's uid with the host filesystem read-write and with DNS/outbound network for up to 1800 s (`:421`), and each
tool run for up to 900 s (`:380`).

**Evidence** (R2–R4, R6; same argv as the counter, no adaptation): a hostile module run *through* the frozen
counter printed

```
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
PINS-AFTER mismatched=0
```

while its own build reported `WRITE_OUTSIDE_D=ok`, `SSH_KEY_BYTES=411` (`~/.ssh/id_ed25519` read),
`LANE_DOT_GIT_W_OK=True`, `LANE_PINNED_TOOL_W_OK=True`, `LANE_CLAIMS_W_OK=True`. The same argv reached
`DNS example.com = 172.66.147.243` and `inet 1.1.1.1:443 CONNECT=ok`, and `~/.ssh` (so
`authorized_keys` could be planted), `~/.bashrc` and `~/.config/systemd/user` are all writable (R4). Module source in
the demo uses none of the `SIDECHANNEL` tokens, so the token scan stays silent by construction.

**Impact.** Any module (honest mistake or a future dishonest one) can read the operator's private key material,
plant login/unit persistence, rewrite the lane's `plans/`, `corpus/` and `.git`, and exfiltrate — while the receipt
that gates C1 says `tampered=0 sidechannel=0`. The frozen limits name only that "tool runs inherit the caller's PATH
and HOME" (`plans/round-40-claims.md:64-66`); filesystem and network exposure is not named, and the docstring's A5
("the counter owns every fixture directory", `round40_c1_verify.py:52-53`) reads as containment.

**Smallest remediation — needs a counter change (frozen: route).** One line in `sandbox()`:

```python
argv = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
        "--bind", str(root), str(root), "--unshare-pid", "--unshare-net", "--unshare-ipc",
        "--die-with-parent", "--new-session"]
```

Validated for the counter's own primitives (R10): outside write `OSError`, inside write `ok`,
`git clone --shared` rc=0, `git add`/`git commit` rc=0, network `OSError`. Caveat to decide at the same time: with
`--ro-bind / /` the operator's `~/.ssh` stays *readable*; closing that needs `Runner.env` HOME redirected, which
would break the ledger's R35-D1 `uv` lookup unless `~/.local/bin` is bound read-only.

**Review rule now** (battery40 is being authored this wave, before any counter can change): a module is admissible
only if it writes under `d`/via `ctx`, never opens an absolute host path, never calls `subprocess` directly, and
contains no `socket`/`urllib`/`http`; and the L1 runs `R40SentinelCounter/l1-guard.sh` after every battery run
(read-only `git status --porcelain` + `sha256sum -c claims/frozen-digests.txt`, tested: prints the L1's own in-flight
changes, all 11 digests `OK`).

## F2 — HIGH — nothing detects out-of-tree writes; a module can forge a sibling's fixture *within the same run*

**Exploit path.** The only write guards are `Ctx._inside`, which validates `cwd` and nothing else
(`round40_c1_verify.py:248-261`), `PINS` = three tool files (`:96-100`, re-hashed at `:457`/`:561-562`), and
`fingerprint()` over each fixture directory (`:310-323`). The battery directory in a default run is the lane's own
(`:474`), and each module file is read only at its own turn (`:411-412`) then loaded by its child (`:419-420`). A
module built earlier therefore rewrites a later module's source, and the run loads, builds and *attributes* it.

**Evidence.** R14: `a_first.py`'s build rewrote `b_second.py`; the receipt reads
`FIXTURE B-REWRITTEN-BY-SIBLING … ok`, `BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0`,
`PINS-AFTER mismatched=0`. Nothing in the predicate changes. Separately (R9), `plans/battery40/*.py`,
`plans/round40_c1_verify.py` (recorded as `4d47800e…` but verified by no program: `grep -rn "frozen-digests"
plans/*.py` → empty), the claims/witness files and the lane's `.git` are all writable from the build child (R2, R4).

**Impact.** The calibration count that C1 exists to produce is forgeable in one run with zero trace: a module can
install a killer fixture under another module's name, rewrite the counter itself for the *next* run, edit the claims
it must not touch, or commit into `.git`. A kill is attributed to a module that never wrote that fixture, and
`tampered=0` speaks only about directories the counter created.

**Smallest remediation — needs a counter change (frozen: route).** (a) F1's bind-root removes the write capability;
(b) additionally have the counter hash its own source and every `plans/battery40/*.py` **before** the loop and
re-hash **after** the last run, adding the result to the `BATTERY` line (same shape as `PINS-AFTER`); (c) have the
L1 verify `claims/frozen-digests.txt` mechanically (that file already lists the counter, both counters, probe, spec,
gate, dry table, captures, and the three tools — and nothing checks it).

**Review rule now.** `l1-guard.sh` after every run; and a battery receipt is only trusted if its `frozen-digests`
check is attached next to it.

## F3 — MEDIUM — a fixture's `.git` can point outside `d`; `fingerprint()` records the link and never walks it

**Exploit path.** `fingerprint()` (`:310-323`) walks the fixture tree, records a symlink's target string only, and
skips `.git/index` and `*.lock`. A fixture that replaces `d/.git` with a symlink to an out-of-`d` git directory makes
every git write of that fixture (add/commit/objects/refs) land outside the fingerprinted tree.

**Evidence.** R7: `dotgit islink= True -> …/decoy-repo/.git` while `fingerprint(d) = b95db572…`; the same run
committed into the decoy (`DECOY_REF=48723ff1ae6f`, R6) and still printed `tampered=0`.

**Impact.** Fixture-side writes escape the only content check the counter has. It does not by itself flip a mutant
verdict (fixture content is the fixture's own), but it is the one hole that survives F1's bind-root fix, because the
decoy can be any path the bind still exposes (notably another fixture's directory or the lane clone).

**Smallest remediation — needs a counter change (frozen: route).** After each fixture's runs, require
`git -C <dir> rev-parse --git-dir --git-common-dir` of the argv's repo (and `realpath` of every symlinked dir entry)
to resolve inside `d`, and count a violation as `tampered`. Review rule now: no module may create a symlink whose
target is outside `d`.

## F4 — LOW — `path_ok()` checks only absolute tokens, only at build time

**Exploit path.** `:326-331` returns `True` for any token that does not start with `/`. R8:
`../../../../../../home/vgpnk/.ssh/id_ed25519` → `True`; `..` → `True`. The tool then runs with
`cwd=fx["dir"]` (`:380`), so a relative token resolves out of the fixture. The check also runs before the runs, so a
symlink retargeted after the build escapes it.

**Impact.** A fixture can point a pinned tool at a host path (e.g. `--lane ../../../..`) with the contract check
green, and the `wrong` computation then judges a result the fixture did not construct. It does not forge a kill by
itself (reference and mutant see the same input), which is why this is LOW, not HIGH.

**Smallest remediation — contract text (frozen docstring says "absolute") → route.** Require every argv path token,
resolved against `d`, to stay inside `d` (both the build-time and a post-build check). Review rule now: no `..` in
argv.

## F5 — MEDIUM — C2 verdicts are forgeable by any code the case recipe runs

**Exploit path.** `db_wal_probe.py:237-242` runs the recipe as a same-uid child in the same pid namespace, then
imports the grader and prints one `TEST <name> P|F` line per test; `:357-360` parses them into a dict where the
**last** line per `(tag, test)` wins. The harness's stdout pipe is addressable inside the case sandbox at
`/proc/$PPID/fd/1`, and the recipe is not waited on if it closes its own stdout first — so a recipe-launched
background writer can emit a line *after* the genuine verdict.

**Evidence.** R12, harness shape identical to the probe's: recipe
`H=$PPID; exec >/dev/null 2>&1; ( sleep 1; printf "TEST test_recovered_json_exists F\n" > /proc/$H/fd/1 ) & exit 0`
produced the stream `TEST … P` then `TEST … F`, and the probe's own parse rule yields `F` for a test the grader
passed.

**Impact.** "A case's verdict is `pass` iff all seven are `P`" is not true under adversarial end-state code. Today's
28 recipes are frozen probe text, so no frozen case exploits it — but case `oracle-solve-sh` (`:172`) executes the
captured third-party `solve.sh`, i.e. external code does run in the case sandbox, and any future case that runs
agent-produced output inherits the channel. Rejection semantics are unaffected (a non-zero rc or a missing verdict is
still a `SETUP` error, never a pass).

**Smallest remediation — needs a counter change (frozen: route).** In `main()`, count lines per `(tag, test)` and
fail with `SETUP …` when any count is not exactly 1 (a duplicate is never legitimate — the harness prints one line
per tag per test); the forgery then becomes a visible probe error instead of a silent verdict. `--unshare-user` with a
separate uid for the recipe stage would be the stronger fix but is not available to an unprivileged caller.

## Checked and found sound (no finding)

- **C2 confinement holds** (R11): `--unshare-net --unshare-pid --unshare-ipc`, `/usr`+`/etc` read-only, private
  `/tmp`, `/app` the only writable bind, `/cap` read-only, no `/home`, no `/run`. Measured inside the probe's own
  argv: DNS `gaierror`, host-listener connect refused, `~/.ssh` and the lane's `.git` absent, `/opt` and `/home`
  writes `FileNotFoundError`, `/usr` `OSError`, a double-fork + `setsid` leaves **0** survivors, `systemd-run --user`
  rc=1 (`Failed to connect to user scope bus … No such file or directory`).
- **C1 pid-namespace cleanup works** (R5): double fork + `setsid` + `sleep 600` leaves 0 survivors; `systemd-run
  --user` inside the C1 sandbox fails (the peer pid is invisible across the new pid namespace). This does not help
  F1 — no escape is needed when the host fs and the network are already open.
- **Command construction**: no `shell=True`, no `os.system`, no `eval`/`exec` in either instrument (R13); both pass
  argv lists; captures, work dirs and `{WORK}` tokens are counter-owned and removed (`:385`, `:372-377`).
- **Pins/freeze:** all 11 `claims/frozen-digests.txt` digests and the probe's 4 capture pins verify `ok`; the three
  tool pins match the working tree. `O13`'s equivalent-mutant note and the `control-c1-*` controls are consistent
  with what the counter prints.
- **C2 execution order**: capture digests are checked before any case runs (`:325-330`); `--dry` and
  `--stage-check` never import the grader.

## Routed (round 41; all frozen files untouched here)

| id | instrument | change | why |
|---|---|---|---|
| R40-S1 | `round40_c1_verify.py:sandbox()` | `--ro-bind / /` + `--bind <root> <root>` + `--dev /dev` + `--tmpfs /tmp` + `--unshare-net --unshare-ipc` | F1 |
| R40-S2 | `round40_c1_verify.py` | hash own source + every `battery40/*.py` before/after; print on the `BATTERY` line | F2 |
| R40-S3 | `round40_c1_verify.py` | require each fixture repo's `--git-dir`/`--git-common-dir` and every symlink target to resolve inside `d` | F3 |
| R40-S4 | counter contract text | every argv path token (relative too) resolved against `d`, re-checked after build | F4 |
| R40-S5 | `db_wal_probe.py:main()` | one line per `(tag, test)` or `SETUP` error | F5 |
| R40-S6 | L1 process | run `l1-guard.sh` after every C1 run and attach its output to the receipt | F1/F2 |

Immediate (this wave, no frozen change): battery40 review rule in F1; `l1-guard.sh` as the post-run guard.

VERDICT: sentinel-5-findings
