# R42BatOrdScan — battery42 module for `order_check.py`'s claims scan (frozen mutants XO5, XO6, XO7)

Seat: executor, kengaku round 42 wave 1. Deliverable: one battery42 module that kills the three assigned frozen
order mutants **attributably**, in their declared directions, with fixtures built from nothing.

Axes named before work: (1) calibration — the three assigned kills must be attributed, not merely exhibited;
(2) operability — one module, a fixed contract, rerun in ~2 s. Every move kept raises exactly one axis and
harms none (no lane file touched, nothing frozen edited).

## 1. Deliverable

| what | value |
|---|---|
| module | `battery/o_scan.py` (6033 bytes, stdlib only, no imports) |
| sha256 | `4a9ef972806481eaa07349f109a843fa0a3e091057d3f6c33b13bfbec4b5279c` |
| fixtures | 6, every `fid` starts `o_scan-`, every one `tool="order"`, `defects=[]` (the order tool prints no `class=` tokens) |
| receipts | `c1-dev-run.txt`, `c1-full-run.txt`, `load-bearing.tsv` in this same directory |

Each `build(ctx, d)` creates `d/repo` with `ctx.init` and builds a fresh git repo: claims file + blobs under the
round's claims directory → freeze commit → receipt commit → (XO5 only) one further commit. Returned argv is
`["--lane", str(repo), "--claims", <rel>, "--receipt", <rel>]`; the absolute lane path resolves inside `d`.

## 2. Which branch each fixture exercises

The mutant table rows read from `plans/round42_c1_verify.py:201-215`; the tool branch from
`plans/order_check.py:116-117` (`rev-list … upto`), `:52-53` (`GATE_P10` alternation), `:54-55` (`CASE_LINE`).

| fid (module line) | mutant / direction | reference rc | mutant rc | shape | one-line comment (module) |
|---|---|---|---|---|---|
| `o_scan-xo5-post-receipt-verdicts` (L53) | XO5 `rc-mirror` | 0 accept | 1 | new claims/ file committed after the receipt; multi-file claims dir | "the reference stops at the receipt" |
| `o_scan-xo5-amended-claims-blob` (L68) | XO5 `rc-mirror` (2nd trigger) | 0 | 1 | **same committed path amended** after the receipt (no new file name) | "new blob, no new file name" |
| `o_scan-xo6-pass-verdict-row` (L79) | XO6 `rc-mirror` (indirect) | 0 | 1 | multi-row verdict registry, `P10 PASS probe executed twice` beside the excused `P10 DEFECT receipt unreadable` | "a row the gate never prints" |
| `o_scan-xo6-echoed-pass-row` (L93) | XO6 `rc-mirror` (2nd trigger) | 0 | 1 | **echo-prefixed** `gate: P10 PASS receipt unreadable` + `gate: P10 DEFECT receipt unreadable` + `gate: P2 ok …` | "echo-prefixed … next to the excused" |
| `o_scan-xo7-timeout-rows` (L106) | XO7 `rc-silence` | 1 reject | 0 | three-row receipt echo, observed values `timeout`/`skip`/`error` (no `pass`/`fail`) | "never pass\|fail" |
| `o_scan-xo7-skipped-row-r38` (L120) | XO7 `rc-silence` (2nd trigger) | 1 | 0 | **round-38** claims directory (round number derived from the claims file name), single `observed=skipped` row | "round-38 claims directory" |

Shape difference against the pre-freeze witness modules is deliberate: I did not reuse the freeze modules'
single-file `control.txt` shapes — I added an amended-blob trigger, a multi-row registry, the `gate:` echo
prefix variant, a multi-row echo, and a different round's claims directory. The module does not import, copy or
read anything under `claims/`; the witness modules were read once for reachability only.

## 3. Counter run (dev, assigned mutants) — pasted

Command (envelope per host-safety rule; Q32 numbers in the header of `c1-dev-run.txt`):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent env TMPDIR="$S" python3 <lane>/plans/round42_c1_verify.py \
  --lane "$S/lane" --battery-dir <report>/battery --only XO5,XO6,XO7 --work "$S/w3"
```

```
PINS total=2 mismatched=0
FIXTURE o_scan-xo5-post-receipt-verdicts tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_scan-xo5-amended-claims-blob tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_scan-xo6-pass-verdict-row tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_scan-xo6-echoed-pass-row tool=order expect=accept declared=- observed_rc=0 observed=- ok
FIXTURE o_scan-xo7-timeout-rows tool=order expect=reject declared=- observed_rc=1 observed=- ok
FIXTURE o_scan-xo7-skipped-row-r38 tool=order expect=reject declared=- observed_rc=1 observed=- ok
MUTANT XO5 order rc-mirror killed by=o_scan-xo5-post-receipt-verdicts attributed=L117 hits=2 -- plans/order_check.py:116-117 'Every blob ever committed under claims_dir up to and includi
MUTANT XO6 order rc-mirror killed by=o_scan-xo6-pass-verdict-row attributed=L53 hits=2 -- plans/order_check.py:52-53 'a gate output line, with or without the C2 counter's `gate: ` 
MUTANT XO7 order rc-silence killed by=o_scan-xo7-timeout-rows attributed=L55 hits=2 -- plans/order_check.py:54-55 'a probe receipt line (the probe's per-case verdict record)' (o
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/0 order=3/3
ADVERTISED direct=2 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
start 17:18:44 / end 17:18:46; ~/.local/bin listing sha256 436b361f… before and after
```

`hits=2` per mutant: **both** fixtures of each pair exhibit the declared direction independently; the first hit
in `--only` order is the one the counter traced and attributed.

## 4. Load-bearing table

Two measurements, each in the same envelope, one counter run per row (`$S/only<i>`, `$S/minus<i>`, `$S/none`).
Full text: `load-bearing.tsv`.

| removed fixture | mutant state after removal | attributed span |
|---|---|---|
| `o_scan-xo5-post-receipt-verdicts` | killed by=o_scan-xo5-amended-claims-blob (hits=1) | L117 |
| `o_scan-xo5-amended-claims-blob` | killed by=o_scan-xo5-post-receipt-verdicts (hits=1) | L117 |
| `o_scan-xo6-pass-verdict-row` | killed by=o_scan-xo6-echoed-pass-row (hits=1) | L53 |
| `o_scan-xo6-echoed-pass-row` | killed by=o_scan-xo6-pass-verdict-row (hits=1) | L53 |
| `o_scan-xo7-timeout-rows` | killed by=o_scan-xo7-skipped-row-r38 (hits=1) | L55 |
| `o_scan-xo7-skipped-row-r38` | killed by=o_scan-xo7-timeout-rows (hits=1) | L55 |

Alone, each fixture is sufficient: six `--only <one mutant>` runs against a single-fixture module print
`killed by=<that fixture> attributed=L{117,53,55} hits=1` with `1 fixture ok`. The flip appears at pair
granularity — an empty battery dir (`--battery-dir $S/none`) gives:

```
MUTANT XO5 order rc-mirror SURVIVED exhibits=none -- plans/order_check.py:116-117
MUTANT XO6 order rc-mirror SURVIVED exhibits=none -- plans/order_check.py:52-53
MUTANT XO7 order rc-silence SURVIVED exhibits=none -- plans/order_check.py:54-55
BATTERY fixtures=0 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=0 survived=3 invalid=0 null_detected=0 unattributed=0
```

So each branch is load-bearing at the pair level and each fixture is a genuine second trigger, not filler.

## 5. Full default counter with the module in the clone's `plans/battery42/`

`cp battery/o_scan.py $S/lane/plans/battery42/` (sha256 `4a9ef97…`, `git -C $S/lane status` = `?? plans/battery42/`;
no commit, no add of the lane's own index concerns — clone only). Then
`--lane "$S/lane" --work "$S/w2"` inside the envelope (`c1-full-run.txt`):

```
PINS total=2 mismatched=0
FIXTURE … six lines, all ok …
MUTANT X1 anchor rc-mirror SURVIVED exhibits=none …
… X3 X6 X7 X9 X12 X13 X14 X15 anchor SURVIVED; XO1, XO3 order SURVIVED …
MUTANT XO5 order rc-mirror killed by=o_scan-xo5-post-receipt-verdicts attributed=L117 hits=2
MUTANT XO6 order rc-mirror killed by=o_scan-xo6-pass-verdict-row attributed=L53 hits=2
MUTANT XO7 order rc-silence killed by=o_scan-xo7-timeout-rows attributed=L55 hits=2
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=3 survived=11 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=0/9 order=3/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 fail
exit=1
```

The 11 survivors are the nine anchor mutants and XO1/XO3 — not this seat's assignment (the anchor seats own 9/9;
XO1/XO3 are unassigned in this wave). `wrong=0 tampered=0 sidechannel=0 invalid=0 unattributed=0` on the full
14-mutant sweep, and the three order kills land through the same attributed path as in the dev run.

## 6. Token scan (module source, case-insensitive)

```
$ python3 -c '…27 SIDECHANNEL tokens…'
hits= []
```

Also `sidechannel=0` reported by the counter itself in both runs.

## 7. Compliance

- Envelope used for every build/tool run: `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin
  /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>`; the counter's
  own read-only sandboxes nested inside it.
- `~/.local/bin` listing sha256 `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` before
  (17:17:49) and after (17:18:39, 17:18:46) — unchanged. No tool installed or updated this wave.
- Writes: only this report dir + `/fast/scratch/hyaku/kengaku-r42/R42BatOrdScan` (clone at `$S/lane`, verified
  `--show-toplevel` = `$S/lane`). No lane file, no corpus/, plans/, git index or jj state touched in the lane.
- No frozen artefact edited: both tool pins stayed `mismatched=0` before and after each run.

## 8. Limits and risks

- A kill is a result difference in the declared direction on a fixture that **executes the mutated line**, not
  evidence of fixture intent; attribution spans are L117 (XO5), L53 (XO6), L55 (XO7) as the counter computed them.
- Fixture pairs are individually sufficient, so the removal table shows attribution moving to the partner rather
  than a kill flip; the flip is demonstrated at pair granularity (empty battery).
- `XO6` is `indirect` by the frozen table (a `P10 PASS` line is not a gate verdict); its two fixtures change only
  the regex alternation's reach, not the tool's intent.
- The scan of my module is a heuristic token match, not proof of isolation: non-author review of `o_scan.py`
  remains part of admission (as named at the freeze).

VERDICT: battery42-o_scan-killed-3/3-wrong-0
