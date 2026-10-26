# F42RevBatOscan — non-author honesty review of `plans/battery42/o_scan.py` (XO5, XO6, XO7)

Round 42 wave 2 (falsify), 2026-10-26. Leaf reviewer seat; no subagents. Target named: the six order-tool
fixtures in `plans/battery42/o_scan.py`, which the landing measurement credits with killing XO5, XO6, XO7.
Question per fixture: does it build the shape the killed mutant's `adv` cell advertises, or a substitute that
reaches the declared direction another way (the wave-1 `R42CritC1Counter` §1 substitutes: receipt-is-directory,
emptied-directory, staged-manifest-only)? Plus: witness copy check and repo-config/symlink/gpg trick check.

## 1. What the mutants advertise (frozen counter, unedited this round)

From `plans/round42_c1_verify.py:201-215` (verified identical to the landing tip, §2):

| mutant | direction | adv sentence | old -> new |
|---|---|---|---|
| XO5 | order, rc-mirror, direct | "Every blob ever committed under claims_dir up to and including `upto`" (`plans/order_check.py:116-117`) — upto replaced by HEAD: blobs committed AFTER the receipt are scanned too | `git.out("rev-list", "--reverse", upto, "--", claims_dir)` -> `git.out("rev-list", "--reverse", "HEAD", "--", claims_dir)` |
| XO6 | order, rc-mirror, indirect | "a gate output line, with or without the C2 counter's `gate: ` echo prefix" (`plans/order_check.py:52-53`) — verdict alternation widened with PASS | `GATE_P10 = re.compile(r"^\s*(?:gate:\s*)?P10\s+(DEFECT|ok)\b[ \t]*(.*)$")` -> same with `(DEFECT|ok|PASS)` |
| XO7 | order, rc-silence, direct | "a probe receipt line (the probe's per-case verdict record)" (`plans/order_check.py:54-55`) — observed narrowed to pass\|fail | `CASE_LINE = re.compile(r"^\s*CASE\s+\S+.*\bobserved=[^\s]*")` -> `...observed=(?:pass|fail)")` |

adv line numbers check out in the clone: GATE_P10 regex `plans/order_check.py:53`, CASE_LINE `:55`,
scan_claims docstring `:116`, rev-list call `:117`.

Reference semantics that decide the directions (read in full, `plans/order_check.py:44-214`):
- the scan window `upto` is `receipt_commit`, the first commit adding the receipt path (`order_check.py:171,190`);
- `blob_hits` excuses only lines with verdict `DEFECT` and detail matching `^receipt unreadable(?:: \S+)?$`
  (`order_check.py:57-59,88-89`); the excuse test requires `m.group(1) == "DEFECT"`, so a `PASS` line is never excused;
- exits: hits or order failures -> 1, clean -> 0, SetupError -> 2.

## 2. Environment and envelope (Q32)

- Clone: `git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" && git -C "$S/lane" checkout -q 508434ad55c709337065611691c426f05875492d` with `S=/fast/scratch/hyaku/kengaku-r42/F42RevBatOscan`, `TMPDIR="$S"`.
  - `git -C "$S/lane" rev-parse --show-toplevel` -> `/fast/scratch/hyaku/kengaku-r42/F42RevBatOscan/lane`; HEAD -> `508434ad55c709337065611691c426f05875492d`.
  - `git -C "$S/lane" diff --stat ff14d76d32d662f7b7073a2acb049594cb740d84 508434ad55c709337065611691c426f05875492d -- plans/` -> **empty**: counter and battery42 byte-identical to the landing tip, so this run characterizes the landing.
- Battery dir holds only the module under review: `ls -A "$S/bat"` -> `o_scan.py`; `cmp` clone copy vs working-tree file -> equal; `sha256sum` -> `4a9ef972806481eaa07349f109a843fa0a3e091057d3f6c33b13bfbec4b5279c  o_scan.py`.
- Envelope for the counter run (host-safety rule):
  `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent python3 "$S/lane/plans/round42_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat" --only XO5,XO6,XO7 --work "$S/work"`
- Q32 receipt: pre `18:08:52`, `ls -A /home/vgpnk/.local/bin | sha256sum` -> `77408cab9a10361a9f6025bab21f5f07933d94ce46e6a10b9117805d58811c11`; post `18:08:52`, same digest. No write outside my scratch and this report.
- First attempt at `18:08:27` failed on my own invocation, disclosed: without `--lane` the counter hashes the pins against cwd (`PINS total=2 mismatched=2 first=plans/anchor_digest_check.py`) and refuses `--work` (`SETUP --work must not lie inside the lane (the build sandbox hides the lane)`), RC=2, nothing executed. Corrected by passing `--lane "$S/lane"`; second run clean.

## 3. Counter run output (verbatim, command in §2)

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
RC=0
```

(The trailing `-- label` text is the counter's own 90-char truncation, `round42_c1_verify.py:632`; full adv
cells are quoted in §1. `hits=2` = both of the mutant's fixtures produced the declared-direction difference,
`round42_c1_verify.py:632` `hits={len(hits)}`.) With only `o_scan.py` in the battery dir, XO5/XO6/XO7 are
killed 3/3 — the module alone carries these three kills, matching the landing's `order=5/5` (the other two
order mutants are outside this module).

## 4. Per-fixture honesty analysis

### o_scan-xo5-post-receipt-verdicts (expect=accept) — XO5 — HONEST
Builds (`o_scan.py:38-48`): freeze commit = claims file + `claims/control-c1-nothing.txt` (the HONEST
do-nothing text, matches no gate regex) + `claims/frozen-digests.txt` (`plans/order_check.py 948d5e1d` — the
true frozen pin prefix, `round42_c1_verify.py:98`; inert to the gate); receipt commit = a real 2-line file at
`corpus/evidence/round42/fibsqrt-probe.txt`; then a third commit adding `claims/rerun-verdicts.txt` =
`P10 ok fresh probe output is byte-equal to the receipt`.
Shape vs adv: the distinguishing blob is a claims/ blob committed AFTER the receipt commit, containing a
`P10 ok` gate line without the echo prefix. Reference window (`rev-list upto=receipt_commit`) excludes it ->
exit 0; mutant window (HEAD) includes it -> GATE_P10 matches, detail is not the excuse -> hit -> exit 1.
That is exactly the advertised widening and the round-40 wit-xo5 source shape ("P10-ok claims blob committed
after the receipt"). No substitute mechanism anywhere: the receipt is a real committed file, the claims dir a
normal directory, nothing staged-only, no argv trickery.

### o_scan-xo5-amended-claims-blob (expect=accept) — XO5 — HONEST
Builds (`o_scan.py:50-58`): freeze with `claims/control-c1-nothing.txt` = HONEST; receipt; then the SAME path
rewritten to HONEST + `gate: P10 ok rerun exit=0` and committed (new blob, no new filename).
Shape vs adv: same advertised window widening, reached through a new BLOB at an existing path — this exercises
"Every blob ever committed" in the adv sentence (`scan_claims` keys `first_seen` by blob sha,
`order_check.py:118-124`), not merely new filenames. Reference sees only the pre-receipt blob -> 0; mutant
sees the amended blob -> `gate: P10 ok …` (echo-prefix branch) -> hit -> 1. A refinement of the same
advertised sentence, not another route to the direction.

### o_scan-xo6-pass-verdict-row (expect=accept) — XO6 — HONEST
Builds (`o_scan.py:60-71`): freeze-time `claims/c1-verdicts.txt` with three lines: `P10 DEFECT receipt
unreadable` (excused identically in reference and mutant), `P10 PASS probe executed twice` (the trigger),
`advertised rows priced=0` (inert); receipt after the freeze.
Shape vs adv: a `P10 PASS` line the gate never prints becomes a hit under the widened alternation; the
reference alternation `(DEFECT|ok)` cannot match PASS. The detail `probe executed twice` does not match
EXECUTED_EXCUSE, and the excuse is further gated on verdict==DEFECT (`order_check.py:88-89`), so the mutant's
hit stands. Reference 0 / mutant 1 = rc-mirror, the advertised mechanism (round-40 wit-xo6 source: claims blob
`P10 PASS receipt unreadable`). The fixture's row is a registry-style sentence instead of the literal wit-xo6
text; the mechanism exercised is identical, so honest, not substitute.

### o_scan-xo6-echoed-pass-row (expect=accept) — XO6 — HONEST
Builds (`o_scan.py:73-83`): freeze-time `claims/gate-echo.txt`: `gate: P10 DEFECT receipt unreadable`
(excused), `gate: P10 PASS receipt unreadable` (trigger — the wit-xo6 literal text under the echo prefix),
`gate: P2 ok receipt readable` (inert: GATE_P10 requires `P10`; no other order_check pattern matches P2 lines).
Shape vs adv: demonstrates the echo-prefix branch of the advertised sentence ("with or without the … echo
prefix"). It also proves the hit comes from the alternation widening and not from the excuse: the PASS line's
detail is `receipt unreadable`, which WOULD be excused if the excuse applied to PASS — it does not
(`m.group(1) == "DEFECT"` guard), and the run's `hits=2` for XO6 confirms both xo6 fixtures trigger. If the
excuse leaked, this fixture would go quiet and XO6's hits would be 1. Honest.

### o_scan-xo7-timeout-rows (expect=reject) — XO7 — HONEST
Builds (`o_scan.py:85-99`): freeze-time `claims/probe-echo.txt`: `stagecheck cases=16 failed=0` (inert:
CASE_LINE requires `^\s*CASE\s`), `CASE lookup-28 observed=timeout rc=timeout`, `CASE oracle observed=skip
rc=0`, `CASE nop observed=error rc=3`; receipt after.
Shape vs adv: CASE rows whose `observed=` values are timeout/skip/error — precisely the "other verdicts" the
narrowed regex misses. Reference matches all three (`observed=[^\s]*`) -> 3 hits -> reject (observed_rc=1,
declared ok); mutant matches none -> accept. rc-silence direction. The timeout row is the round-40 wit-xo7
literal shape; skip and error are additional values inside the advertised narrowing. Honest.

### o_scan-xo7-skipped-row-r38 (expect=reject) — XO7 — HONEST
Builds (`o_scan.py:101-111`): claims file `plans/round-38-claims.md`, claims dir
`.ufo/waves/round-38/claims`, `control-c2-nothing.txt` = `checks=9 defects=0` + `CASE c7 observed=skipped`;
receipt (the round-42 receipt path) after.
Shape vs adv: one CASE row with `observed=skipped` — neither pass nor fail, i.e. the adv's "other verdicts".
Reference hits -> reject; mutant misses -> accept. The round-38 wrapper additionally exercises the
claims-filename -> claims_dir derivation (`CLAIMS_NAME`, `order_check.py:50,176-177`) but is not the source of
the direction — the trigger is the skipped row, the advertised mechanism. Honest. Neutral observation: the
gate does not cross-check that the receipt belongs to the same round as the claims file; the fixture relies on
that caller-side pairing, which is how the counter passes the pair anyway.

## 5. Table

| fixture | mutant(s) killed | verdict | reason |
|---|---|---|---|
| o_scan-xo5-post-receipt-verdicts | XO5 (hits=2 pair) | honest | claims/ blob with `P10 ok` committed after the receipt commit; reference window excludes, mutant window includes — the advertised rev-list widening, wit-xo5 shape |
| o_scan-xo5-amended-claims-blob | XO5 (hits=2 pair) | honest | same widening via a new blob at an existing path; exercises "every blob" (first_seen by blob sha), echo-prefix branch |
| o_scan-xo6-pass-verdict-row | XO6 (hits=2 pair) | honest | freeze-time `P10 PASS` row the gate never prints; reference alternation cannot match, mutant's hit not excusable (excuse is DEFECT-only) |
| o_scan-xo6-echoed-pass-row | XO6 (hits=2 pair) | honest | wit-xo6 literal text with `gate: ` echo prefix; also proves the excuse does not leak to PASS (hits=2) |
| o_scan-xo7-timeout-rows | XO7 (hits=2 pair) | honest | CASE rows observed=timeout/skip/error; reference matches all, narrowed mutant matches none — the advertised narrowing, wit-xo7 shape |
| o_scan-xo7-skipped-row-r38 | XO7 (hits=2 pair) | honest | observed=skipped ("other verdicts") in a round-38 claims dir; trigger is the advertised mechanism, r38 wrapper is extra coverage |

No fixture is a substitute in the wave-1 sense: none uses an argv receipt that is a directory, an
emptied/removed directory, a staged-only manifest, or any other route around the advertised sentence. Every
fixture commits a real file receipt and normal claims blobs; the direction in every kill flows through the
exact `old -> new` difference quoted in §1.

## 6. Witness-copy and trick checks

- `o_scan.py` contains zero import statements and no `open(`/`subprocess`/`os.`/`readlink`/`witness`/
  `w_anchor`/`w_order` strings (grep over the module: no matches). It cannot read the witness: only `ctx`
  helpers, whose paths the counter restricts to the fixture dir (`round42_c1_verify.py:53-55`), and the
  counter's own sidechannel token scan — which includes the token `witness` (`round42_c1_verify.py:101-103`)
  — reported `sidechannel=0`.
- Structure vs `.ufo/waves/round-42/claims/witness/w_order.py`: different constants
  (`CLAIMS_42/DIR_42/RECEIPT=fibsqrt-probe.txt` vs `CLAIMS/CDIR/RECEIPT=probe.txt`), different helpers
  (`_freeze/_receipt/_later/HONEST` vs `c/args/gate_repo`), different fixture set (6 vs 5; o_scan has no
  XO1/XO3 at all), different blob texts. Shared idioms (`ctx.init(d / "repo")`, `add -A`/`commit -q`, the
  `["--lane", str(repo), "--claims", …, "--receipt", …]` argv tail) are the battery contract's mandated shape
  (`round42_c1_verify.py:51-55`), not evidence of copying. Not a renamed copy.
- vs the wave-1 build battery `.ufo/waves/round-42/build/R42CritC1Counter/battery/b_order.py`: o_scan drops
  both wave-1 substitutes (receipt-is-directory, emptied-directory) entirely and expands each honest trigger
  to two variants. Neither substitute mechanism appears in o_scan.py.
- No repo-local git config, no symlink, no `core.worktree`, no gpg/signature anything: the only git calls in
  the module are `add -A` and `commit -q -m` (`o_scan.py:18-21`); `ctx.init` is the counter's pinned
  `git init -b master`; the build sandbox pins git config and HOME, and the run reported `tampered=0`.

## 7. Residual risk and verification gaps

- All three attributed spans (L117 rev-list call, L53 GATE_P10 compile, L55 CASE_LINE compile) execute on
  every tool invocation, so the wave-1 `R42CritAttribution` vacuity limit applies to these kills too; what
  makes them non-vacuous is the fixture shape, which this review verifies per fixture. The counter's freeze
  text states the kill rule is result-difference-based: "a kill records a result difference in the declared
  direction on a fixture that executes the mutated line, not the fixture's intent"
  (`plans/round42_c1_verify.py:66-67`).
- Inert filler noted, harmless: `gate: P2 ok receipt readable` (xo6_echoed_pass) and `stagecheck cases=16
  failed=0` (xo7_timeouts) match no order_check pattern.
- Development mode prints `PREDICATE C1 n/a` as designed; `PINS mismatched=0` before and after.
- Out of scope, not reviewed: the other four battery42 modules (`a_row.py`, `a_route.py`, `a_class.py`,
  `o_clause.py`) and the anchor mutants.
- Tooling: installed nothing (no pacman, no uv, no binaries); existing python3/git/bwrap only.

VERDICT: battery42-o_scan-honest-6/6-substitute-0
