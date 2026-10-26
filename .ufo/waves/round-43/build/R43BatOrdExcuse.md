# R43BatOrdExcuse — battery43 module `o_excuse` (order mutant NO7)

Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only for this seat). Scratch:
`/fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse` (`S`). Clone: `git clone -q --shared <lane> "$S/lane"`,
`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse/lane` (asserted
before any write); clone HEAD `d33350fdb01ce27cbff47b04642fd2c1471e5c26`. No commit, no mutation in the lane.

## Files changed

| path (absolute) | role |
|---|---|
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatOrdExcuse/battery/o_excuse.py` | the battery43 module, 138 lines, sha256 `9f741fdc126d6f0f3e126aee22b45a66816c9d46141714cd8c0f7f1ed5631c96` |
| `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatOrdExcuse.md` | this report |

Nothing else in the lane was written. The module was also copied to `"$S/lane/plans/battery43/o_excuse.py"`
(identical sha256) only to run the full default counter; that is scratch, not the lane.

## The frozen behaviour being killed

NO7 (`plans/round43_c1_verify.py` MUTANTS, row 8): tool `order`, class `-`, direction `rc-mirror`, adv
`plans/order_check.py:56-57`, `old` `EXECUTED_EXCUSE = re.compile(r"^receipt unreadable(?:: \S+)?$")` → `new`
`EXECUTED_EXCUSE = re.compile(r"^receipt unreadable$")`. The branch: `blob_hits` (order_check.py:101-113) tests
`EXECUTED_EXCUSE.match(detail)` at order_check.py:107 for a `P10 DEFECT` line; a non-matching detail becomes a
`probe-executed-before-receipt` hit (order_check.py:197-198) → exit 1. So the P2-shaped echo `receipt unreadable:
<path>` is excused by the reference (exit 0) and flagged by the mutant (exit 1): direction `rc-mirror` = fixture
`expect=accept`, ref rc 0, mutant rc 1.

## Module contract compliance

`FIXTURES` = 3 order entries, each `{"fid","tool":"order","expect":"accept","defects":[],"build"}`; every fid starts
`o_excuse-`; every `build(ctx, d)` fills the empty `d`, builds its repo from nothing (`ctx.init`) and returns
`["--lane", ".", "--claims", <rel>, "--receipt", <rel>]`; all commits go through `ctx.git` (identity/date pinned by
`Ctx.ENV`), all writes through `ctx.write` inside `d`. `defects` is `[]` for every fixture because `order_check.py`
prints no `DEFECT class=` lines (counter `classes()` returns the empty set for `tool != "anchor"`).

| fid | shape | what it demonstrates |
|---|---|---|
| `o_excuse-echo-freeze-claims` | repo at `d`, 3 commits: freeze commit carries `.ufo/waves/round-43/claims/{round-43-claims.md, control-c1-nothing.txt, c2-stage-check.txt}`, the echo sits as raw gate output in a fenced block of the claims file **inside** the scanned claims dir; later commits add a mirror-as-battery control blob then `corpus/evidence/round-43/feal-probe.txt`; `--lane .` | the reference excuses the echoed path and accepts; the mutant reads a hit and rejects (killer 1) |
| `o_excuse-gate-prefix-late` | repo at `d`, 4 commits: the claims file stays clean, the hook is a **later** blob `control-c2-nothing.txt` carrying `gate: P10 DEFECT receipt unreadable: evidence/round43/feal-probe.txt` (the `gate: ` echo prefix, a relative path that never exists), receipt last | the `(?:gate:\s*)?` prefix path and a non-freeze-commit blob reach the same `EXECUTED_EXCUSE` branch (killer 2) |
| `o_excuse-bare-excused` | repo at `d`, claims file **outside** the claims dir (`plans/round-43-claims.md`), claims dir holds one transcript blob with the bare `P10 DEFECT receipt unreadable` | control: both the reference and the mutant excuse the path-less sentence, so the kill is attributable to the echoed path, not to the `P10 DEFECT` sentence (no hit, no kill) |

Divergence from the pre-freeze direction module (which this seat read only to learn reachability, as the ticket
allows; nothing was imported, copied or adapted): `w_near.py` puts the repo at `d/lane`, the claims file at
`plans/round-42-claims.md` outside the scanned claims dir, the echo in a separate `control.txt` in the **freeze**
commit, `--lane` absolute, 2 commits. This module puts the repo at `d` itself, the claims file **inside** the scanned
`.ufo/waves/round-43/claims/` dir, 3-4 commits, `--lane .` relative, adds the `gate: `-prefixed and the bare-sentence
shapes. No shared fixture text.

## Measurement 1 — development run, `--only NO7` (inside the envelope)

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh "$S/env" \
  python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py \
  --lane "$S/lane" --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatOrdExcuse/battery \
  --only NO7 --work "$S/w"
```

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse/env /fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse/env --bind /fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse/lane --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/build/R43BatOrdExcuse/battery --only NO7 --work /fast/scratch/hyaku/kengaku-r43/R43BatOrdExcuse/w
ENVELOPE start 19:08:26 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE o_excuse-echo-freeze-claims tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_excuse-gate-prefix-late tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_excuse-bare-excused tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NO7 order rc-mirror killed by=o_excuse-echo-freeze-claims attributed=L60 value=differs hits=2 -- plans/order_check.py:56-57 'The one P10 detail the gate prints before executing anything,
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=1/1
ADVERTISED direct=1 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
ENVELOPE end 19:08:29 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

`hits=2` = both killers exhibit; `attributed=L60` (span = the replaced `EXECUTED_EXCUSE` line, order_check.py:60, which
`grep -n` confirms), the
traced mutant run reproduces the untraced result, runs the span line, and its site record differs from the
reference's (`value=differs`, leg g). Sidechannel scan on the module source (the counter's own token list, lowercased
substring test, run before the counter): `TOKENS clean`.

## Measurement 2 — load-bearing table (remove one fixture per run, `--only NO7`)

Each run: `envelope.sh "$S/env" python3 plans/round43_c1_verify.py --lane "$S/lane" --battery-dir "$S/lb/<rmN>" --only NO7 --work "$S/w"`; `rmN/o_excuse.py` is a copy of the module with exactly one `FIXTURES` entry removed.

| removed | NO7 | `hits` | `killed by=` | flips? |
|---|---|---|---|---|
| `o_excuse-echo-freeze-claims` (`rm1`) | killed | 1 | `o_excuse-gate-prefix-late` | no — killer 2 carries it alone |
| `o_excuse-gate-prefix-late` (`rm2`) | killed | 1 | `o_excuse-echo-freeze-claims` | no — killer 1 carries it alone |
| `o_excuse-bare-excused` (`rm3`) | killed | 2 | `o_excuse-echo-freeze-claims` | no — the control never hits (`hits` stays 2) |

Envelope lines for the three runs (all `unchanged`, no exit-4 / `INVALID`, so no re-run was required):
`ENVELOPE start 19:08:57 / end 19:08:59 exit=0 … unchanged`; `start 19:09:00 / end 19:09:02 exit=0 … unchanged`;
`start 19:09:04 / end 19:09:06 exit=0 … unchanged`; every one `local_bin_content_before=328be01808ba022f
after=328be01808ba022f unchanged`, and each printed `BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=0` and
`MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0 unattributed=0`.

Reading: each of the two killers kills NO7 on its own (so the pair is redundant by design, as the ticket asks for two
shapes), and the control is load-bearing only as a discriminator: it is the fixture that shows the mutant still
excuses the bare sentence, so the kill cannot be credited to "any `P10 DEFECT` line".

## Measurement 3 — full default counter with the module in `plans/battery43`

```
cp <report>/battery/o_excuse.py "$S/lane/plans/battery43/o_excuse.py"   # sha256 9f741fdc…, identical
envelope.sh "$S/env" python3 plans/round43_c1_verify.py --lane "$S/lane" --work "$S/w2"
```

```
ENVELOPE start 19:09:13 cwd=/home/vgpnk/Projects/shokunin
PINS total=2 mismatched=0
FIXTURE o_excuse-echo-freeze-claims tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_excuse-gate-prefix-late tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_excuse-bare-excused tool=order expect=accept declared=- observed_rc=0 observed=- ok
MUTANT NA1 anchor silence SURVIVED exhibits=none
MUTANT NA5 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA7 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA18 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA20 anchor rc-mirror SURVIVED exhibits=none
MUTANT NA21 anchor rc-mirror SURVIVED exhibits=none
MUTANT NO5 order rc-silence SURVIVED exhibits=none
MUTANT NO7 order rc-mirror killed by=o_excuse-echo-freeze-claims attributed=L60 value=differs hits=2
MUTANT NO22 order rc-silence SURVIVED exhibits=none
BATTERY fixtures=3 wrong=0 tampered=0 sidechannel=0
MUTANTS total=9 killed=1 survived=8 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/6 order=1/3
ADVERTISED direct=8 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
ENVELOPE end 19:09:16 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The `SURVIVED` rows are the other seats' scope (this wave's other battery43 modules); `PREDICATE C1 fail` here is the
expected state of a one-module lane, not a defect of this module: `wrong=0 tampered=0 sidechannel=0
null_detected=0 unattributed=0 invalid=0` and NO7 is killed attributably.

## Limits

1. The two killers hit the same branch, so removing either does not flip NO7; the per-run `killed by=` field is the
   load-bearing evidence, not a flip. Redundancy is required by the ticket (two shapes per mutant), so no flip is
   possible while both are present.
2. The control fixture asserts a negative (both builds accept the bare sentence); it kills nothing. If a future tool
   edit widened the excuse to match everything, the control would still be `ok`, so it cannot substitute for the
   killers.
3. Order fixtures carry `defects: []` by tool contract; attribution for `order` rests on exit status plus the leg-g
   site record, never on a class set. A mutant whose only effect were hidden attribute state would read
   `unattributed` (counter's own named limit), not proven here.
4. The echoed path in both killers need not exist and is never opened; no fixture covers an existing-but-unreadable
   receipt file (that is the gate's own `receipt not committed in HEAD` setup error, exit 2, not this branch).
5. Cross-mutant isolation was not attempted: `o_excuse-gate-prefix-late` places its hook in a later claims commit,
   which NO5 (oldest-commit-only scan) cannot see, so it should not feed NO5; I did not measure NO5 and claim nothing
   about it. NO22 was likewise not exercised.
6. `hits=2` in the full run shows the reference accepts both killers with the echo present, i.e. both really take the
   excuse branch; the mutant's reject was observed only through the counter (rc 1 inside the sandbox), not by running
   the mutant by hand outside it.
7. Non-author review of "not a re-spelling of `w_near.py`" is not mine to give: I read that module for reachability
   (permitted by the ticket) and recorded the shape differences above for the reviewer to check.
8. No tool was installed or upgraded by this seat; no pacman/uv/npx invocation. No writes outside `$S` and the report
   directory; the PATH-dir content digest was byte-identical before/after all four measured runs.
9. `--jobs 8` default; run-to-run wall times 2-4 s. All measurements used the frozen counter and the pinned tools
   (`PINS total=2 mismatched=0`, `PINS-AFTER mismatched=0`); no frozen artifact was read-and-modified.

VERDICT: battery43-o_excuse-killed-1/1-wrong-0
