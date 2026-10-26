# F42GpgVector — gpg-vector adjudication (`R42SentinelCounter` V1 vs `R42CritC1Counter` V1)

Seat: `F42GpgVector` (critic, leaf). Attack: the conflict between `R42SentinelCounter` V1
(a fixture `.git/config` with `log.showSignature=true` + `gpg.program=<exe>` runs that program inside
`order_check.py`'s `git log`) and `R42CritC1Counter` V1 ("a fake gpgsig commit … left GPG-LOG-RC 0").
Reproduced under `plans/round42_c1_verify.py`'s **exact** `Runner.env` and `ro_sandbox` (both imported
from the frozen counter, not transcribed). Questions: does the program execute? can it observe which
variant is running? can it change a verdict in any of the 14 declared directions? smallest remediation?

Envelope for every run (verbatim, one line):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

Q32: `date +%T`/`ls -A /home/vgpnk/.local/bin | sha256sum` before/after every run —
`18:06:12→18:06:12`, `18:07:21→18:07:21`, `18:07:26→18:07:27`, `18:07:42→18:07:42`,
`18:07:44→18:07:44`, `18:08:31→18:08:31`, `18:08:36→18:08:36`, `18:08:38→18:08:38`,
`18:08:59→18:08:59`, `18:09:56→18:09:57`, `18:10:15→18:10:16`, `18:10:29→18:10:29`;
listing digest `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` unchanged in all.
Scratch `/fast/scratch/hyaku/kengaku-r42/F42GpgVector` (round-root sentinel present), `TMPDIR` inside it;
lane clone at `$S/lane` = `508434ad55c709337065611691c426f05875492d` (docs tip), toplevel verified,
untouched. `git 2.56.0`, `bubblewrap 0.13.1`, `python 3.14.8`. Nothing written outside scratch and this
report subdir; no tool installed or upgraded.

## The conflict resolves: both reports reproduce — they measured different things

| | `R42SentinelCounter` V1 | `R42CritC1Counter` V1 |
|---|---|---|
| measurement | does `gpg.program` **execute**? | what is `git log`'s **exit status**? |
| verdict | `exec=YES GPG --keyid-format=long --status-fd=1` | `GPG-LOG-RC 0`, empty stderr |
| reproduced? | **yes** (below) | **yes** (below) |

Both are true at once: the program runs, but a failing/benign `gpg.program` does not change `git log`'s
exit code — git prints "No signature" state internally and carries on. The critic's fixture was also *not*
a signed commit in one earlier shape: a `gpgsig` header placed after the blank header/message separator is
parsed as *message content*, not a header (`%G?` prints `N`; no exec). With the header placed where git
writes it (contiguous with the other headers, continuation lines each prefixed with one space), gpg runs.

## Reproduction (exact `Runner.env` + `ro_sandbox`)

Fixture (mirrors battery42 build via `Ctx`): order repo with commit 1 adding `plans/round-42-claims.md`,
commit 2 a hand-crafted **signed** receipt commit (`git hash-object -t commit -w --stdin --literally`,
`gpgsig` header + fake armor), `.git/config` carrying `[log] showSignature=true` and
`[gpg] program=<payload>` — the same keys the sentinel flagged. Payload scripts: a logging payload, a
redirect-`a…a`-40 payload, and a kill-parent payload. Tool runs reuse the counter's own
`ro_sandbox(writable=(work,tmp), hide=(variants,slots,bin,tracer), ro_data=(variantfd→slots/order.py))`
and `Runner.env` (GIT_CONFIG_COUNT=2 pins: `core.fsmonitor=false`, `core.hooksPath=/dev/null`), cwd =
fixture dir, `--ro-bind-data` variant bound at the slot — byte-for-byte the counter's run path.

### Q1 — execution inside the run: YES
- `raw2.out` (raw git, same env): `git log --reverse --diff-filter=A --format=%H -- <receipt>` with the
  kill payload → `rc=-9` (SIGKILL) for **every** form tested (`--format=%H`, default pretty, `-1`,
  `--show-signature`). With `gpg.program=/bin/false` → `rc=0`, clean stdout, empty stderr (the critic's
  observation, verbatim shape). Sentinel's `exec=YES` line is reproduced: the payload's argv was
  `['payload.py', '--keyid-format=long', '--status-fd=1', '--verify', '<TMPDIR>/.git_vtag_tmp…', '-']`
  (`steer2.out` `log` extras).
- Sandboxed tool run (`steer2.out`): `kill` tag → the order tool's `git log` is killed (`ORDER ERROR git
  log … rc=-9`) and the tool exits `2` (SetupError). `clean-kill` tag (passing history) → same. Execution
  happens inside the counter's own sandbox with the run's capabilities (host read-only, work/tmp writable).

### Q2 — can the program observe which variant is running: YES
The payload derives the counter's scratch root from its parent git's `/proc/<ppid>/cmdline`
(`/fx/` token), reads the bound variant at `<root>/slots/order.py`, and compares it with the lane's
pristine `plans/order_check.py` (`steer2.out` `detect-*` tags):

```
detect-ref : VARIANT=REF   SLOT_SHA=948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc
detect-mut : VARIANT=MUTANT SLOT_SHA=eac915ee42e5b32c2fd25b368dece67996fc1047d0bd90252fc86c68c95fac63
```

(REF slot sha = the frozen PINS digest of `order_check.py`.) So a fixture-supplied program can tell the
mutant re-run from the reference re-run — the repair-(a) property "nothing inside a run can read which
variant it is" (round42_c1_verify.py:22) is defeated for this tool, exactly as the sentinel argued.

### Q3 — can it change a verdict in any of the 14 declared directions: NO (today)
- Channels the payload could in principle use: (i) stdout pollution of the tool's parsed output, (ii)
  forced exit codes.
- (i) is closed: `steer2.out` `prefix` tag — a payload that prints a fake 40-hex line into its stdout
  leaves the tool's output untouched (`receipt_commit=0c2cf011…` still the real hash; no `a…a` token
  anywhere; `rc=1` FAIL verdict for the broken history unchanged). Git consumes gpg's stdout for
  status parsing; it does not splice it into `--format=%H` output. The earlier `drv2.out` anomaly
  (`receipt_commit=import:`) came from a malformed-signature fixture variant and is not reproducible with
  a correctly signed commit (`steer2.out`); it is not a channel.
- (ii): the only exit code a payload can force is `2` (kill the git parent → `SetupError`). The 14
  declared directions (`drv2.out` `mutant_directions`) are: `silence` (X6, X7, X14), `rc-silence`
  (X9, X13, X15, XO1, XO3, XO7), `rc-mirror` (X1, X3, X12, XO5, XO6). None is `error`-direction; all
  five order directions require a `0↔1` reference/mutant pair, and `exhibits` rejects any result outside
  (0,1) for them (round42_c1_verify.py:442-457). Forcing 2 in both runs yields no exhibited direction.
- The anchor tool never issues `git log` (its command set: `rev-parse`, `ls-tree`, `ls-files`,
  `cat-file`, `rev-list`, `merge-base` — order_check.py:29-30, anchor_digest_check.py:187-205,374-398),
  so the gpg vector cannot run at all for the nine anchor mutants, including both `silence` directions.
- Conclusion: V1 is a real **code-execution property break + information channel** (variant
  identification, unhidden lane read), but today it cannot fabricate any of the 14 directional kills.
  This matches the sentinel's own impact (iii).

## Remediation draft (smallest safe correction; draft only, in this seat's dir)

`plans/round42_c1_verify.py` `Runner.env` (round42_c1_verify.py:380-387): raise
`GIT_CONFIG_COUNT` 2 → 4 and pin the two keys, so a fixture cannot re-arm them and includes cannot
re-inject them (env-level `GIT_CONFIG_*` behave like `-c`, highest precedence):

```python
"GIT_CONFIG_COUNT": "4",
"GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": "false",
"GIT_CONFIG_KEY_1": "core.hooksPath", "GIT_CONFIG_VALUE_1": "/dev/null",
"GIT_CONFIG_KEY_2": "gpg.program", "GIT_CONFIG_VALUE_2": "/bin/true",
"GIT_CONFIG_KEY_3": "log.showSignature", "GIT_CONFIG_VALUE_3": "false",
```

Same two pins belong in `Ctx.ENV` (build side; sentinel V4). Optional hardening: add the lane to the
tool-run hide list (V5) — not required to block this vector.

**Shown to block** (`remediate.out`): with the 4-pin env, the kill payload never executes
(`pinned-kill rc=0`, normal hash output) — including when the fixture pulls the same keys in via
`include.path` (`pinned-kill-include rc=0`); the unpinned controls run the payload and kill git
(`unpinned-kill rc=-9`, `unpinned-kill-include rc=-9`). Calibration parity: the order tool's verdicts
under the pinned env are unchanged — broken history `rc=1` (ORDER RESULT FAIL), clean history `rc=0`
(ORDER RESULT PASS) — so pinning does not alter any frozen fixture result.

## Limits
- One host (git 2.56.0, bwrap 0.13.1); other git builds may add exec keys — the fix is the pinned
  `GIT_CONFIG_*` set, not two literals.
- Payloads used a `python3` shebang; exec also verified for `/bin/false`/`/bin/true` (no shebang).
- I did not re-audit the 14 mutants' advertised sentences; only their directions and the two tools'
  command sets were used.

## Receipts (all < 1 MiB; in `falsify/F42GpgVector/receipts/`)

| file | sha256 |
|---|---|
| `raw2.out` | `3852264099a90d631e4f0c9a79ec80f88efcaf959b09b780a9d29132a789e8ff` |
| `drv2.out` | `8af62b5eee6db3f7dbfada76f9e74d8ef675aa2ca3d55fd6e0c757ff55f7f004` |
| `steer2.out` | `9d41d652ad4c4079a17177aa6129e69a7701e15c637f2ca65a564bdb8c8f1d91` |
| `remediate.out` | `c134920847511c3ec3aa9e3421386b041c2e575f10bd81f02f111d89f567ec5a` |

VERDICT: gpg-vector-real-verdict-change-impossible
