# F38XMutRerunMain — extra-mutant rerun: P9, P10, RUN (run_checks), MAIN, D4/D5 line subcommands

Round 38 wave 2 (FALSIFY), kengaku hyaku run 8, 2026-10-26. Landing tip under attack:
`8c7422d7a646515d80af44844e8ecc8a1fc1d30a` (clean clone, `git status --porcelain` empty, gate sha256
`ea638822…` = the frozen PINS digest). Frozen claims: `plans/round-38-claims.md` (freeze `e0a3785…`).

Report: .ufo/waves/round-38/falsify/F38XMutRerunMain.md

## Method

Sibling seat F38XMutP covered its mutant slice; this seat adds **16 extra mutants** (X01–X16) on the
assigned surfaces: P9 (`c_clean_tree`), P10 (`c_rerun`), RUN (`run_checks`), MAIN (`main`), and the
D4/D5 line subcommands (`cmd_d4`, `cmd_d5`). Harness: a dev counter that is the frozen
`plans/round38_c1_verify.py` byte-for-byte plus one appended block overriding `MUTANTS` with the 16
extras (diff receipt: `xmut-counter-diff.txt`, 53 added lines, 0 changed/removed harness lines). The
dev counter ran with the **default full battery** (r36 + battery37 + battery38 = 86 fixtures) and the
frozen ATTRIBUTED kill rule, unchanged. Mutant gates are generated in scratch by the counter's own
single `replace(old, new, 1)` mechanism; the lane tree is never written.

Commands (all in the tip clone `/fast/scratch/hyaku/kengaku-r38/F38XMutRerunMain/lane`):

    python3 plans/round38_c1_verify.py --lane . --work $S        # baseline, frozen counter
    python3 $S/xmut/counter_x.py --lane $S/lane --work $S        # dev counter, 16 extras

## Baseline (before)

`baseline-frozen.txt` — reproduces the landing receipt `measure-final.txt` exactly:

    PINS total=14 mismatched=0
    BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
    MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
    PREDICATE C1 fail

N21 (D5, silence) is the survivor — matching the L1's honest-stop report; see finding 5.

## Extra-mutant run (after)

`extra-run.txt` — same battery state (`fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`,
`null_detected=0`), then:

    MUTANTS total=16 killed=12 survived=4 invalid=0 null_detected=0

All 16 old-strings were unique in the pristine gate and every mutant compiled (`invalid=0`).

| id | clause | dir | mutation (old → new, abbreviated) | expected detector | verdict | killed by |
|----|--------|-----|-----------------------------------|-------------------|---------|-----------|
| X01 | P9 | silence | git-fail arm `return False` → `return True` ("root is not a readable git worktree") | p910-not-a-git-repo | killed | p910-not-a-git-repo |
| X02 | P9 | silence | `left = [x for x in r.stdout.splitlines() if x]` → `left = []` (untracked ignored) | any clean-tree reject fixture | killed | r36-P6 |
| X03 | P9 | mirror | `ls-files --others --exclude-standard` → `ls-files --exclude-standard` (tracked files redden) | accept fixture with tracked files | killed | r36-P0 |
| X04 | P10 | silence | probe-unrerunnable arm `return False` → `return True` | none (B4-class) | **survived** | — |
| X05 | P10 | silence | fresh-exit arm `return False` → `return True` | p910-probe-exits-1 | killed | p910-probe-exits-1 |
| X06 | P10 | silence | `if r.stdout != want:` → `if False:` (byte-compare dropped) | p910-receipt-one-byte | killed | p910-receipt-one-byte |
| X07 | RUN | silence | `defects += not ok` → `defects += 0` (reject rc destroyed) | predicted survive (rc-flip) | **survived** | — |
| X08 | RUN | silence | clause print `'ok' if ok else 'DEFECT'` → `'ok' if ok else 'ok'` | first package fixture with a defect | killed | r36-P1 |
| X09 | MAIN | silence | crash handler `return 2` → `return 1` | mainx-spec-invalid-json | killed | mainx-spec-invalid-json |
| X10 | MAIN | silence | `return 0 if cmd_package(...) == 0 else 1` → `return 1 if ... else 1` (accept→reject) | predicted survive (rc-flip) | **survived** | — |
| X11 | D4 | silence | label check dropped: `... or not lines[0].startswith(spec["d4"]["label"])` → removed | d4-m46 | killed | d4-m46-label-not-carried |
| X12 | D4 | silence | verdict `return not bad` → `return True` (patterns unchecked) | d4m-n19 | killed | r36-L2 (earlier family fixture) |
| X13 | D5 | silence | require-token check `if d5["require"] not in line:` → `if False:` | d5-m51 | killed | d5-m51-require-missing |
| X14 | D5 | silence | forbid-token check `if d5["forbid"] in line:` → `if False:` | d5-m52 | killed | d5-m52-forbid-present |
| X15 | D5 | mirror | tag-strip dropped: `re.sub(r"<[^>]+>", "", ...)` removed from the flat compare | uncertain | **survived** | — |
| X16 | D5 | silence | label check dropped: `... or not lines[0].startswith(d5["label"])` → removed | d5-m50 | killed | d5-m50-label-altered |

**killed=12/16.** Every kill is attributed to a named fixture under the frozen rule (family-matched
argv, declared defects, direction-checked).

## Survivor probes (non-equivalence evidence)

`survivor-probes.txt`, `survivor-probeB.txt` — for each survivor, ref gate vs mutant gate on a
crafted scratch fixture (never the lane):

- **X07** (probe A2, empty-dir package): ref `rc=1 … defects=8` with 8 `P* DEFECT` lines; X07 prints
  the identical 8 `DEFECT` lines but `defects=0` and `rc=0`. Non-equivalent: the gate accepts a
  package it just called defective in every clause.
- **X10** (probe A1, genuine accept package): ref `rc=0`, all clauses `ok`; X10 identical clause
  lines but `rc=1`. Non-equivalent: a genuine package is rejected.
- **X04** (probe A3, `probe_cmd=["no-such-probe.py"]`): both ref and X04 print `P10 DEFECT fresh
  probe exit=2` — a missing probe *script* lands on the fresh-exit arm, not the OSError arm. The
  OSError arm is reachable only through the gate's own interpreter/environment (missing `uv` in the
  fallback, or a probe slower than the hardcoded 600 s timeout) — the same class the freeze already
  excluded as B3/B4 ("reachable only through the gate's interpreter/environment, which the counter
  fixes", plans/round38_c1_verify.py docstring). Survived, and the freeze's exclusion reasoning
  holds for this arm too.
- **X15** (probe B, genuine D5 capture with `<b>` injected mid-quote, manifest re-pinned): ref
  `D5 ok directional=True digest_pinned=True bad=0` (rc 0); X15 `D5 DEFECT directional=False …
  bad=['quote absent from the capture']` (rc 1). Non-equivalent: the mutant is killable, just not by
  anything in the battery.

## Findings

1. **12/16 extra mutants killed, attributedly, across all six assigned surfaces** (P9 ×3, P10 ×3,
   RUN ×2, MAIN ×2, D4 ×2, D5 ×4). The battery's demonstrated surface is wider than the 22 frozen
   mutants alone show: the round-37/round-36 fixtures also kill four of these new shapes
   (X02, X03, X08, X12) without b38 help.
2. **The ATTRIBUTED kill rule has an exit-code blind spot (X07, X10).** Two non-equivalent mutants
   that change only `main`/`run_checks`' exit code survive: the silence/mirror/RUN rules compare
   DEFECT sets (unchanged here), and the MAIN rule reads the exit code only in the error direction
   (`expect=error`, ref 2 → mutant 0/1). The round-38 rule was introduced because round-37's
   "any result differs" rule was gameable; it over-corrected: a rc-flip with an unchanged DEFECT set
   is now invisible. A one-line extension (treat a rc difference as attribution when the fixture's
   `expect` is accept/reject) would close it. This is a counter-rule finding, not a gate defect.
3. **X04 confirms the freeze's B4 exclusion**: P10's probe-unrerunnable arm is not reachable from
   package inputs (probe A3), so no fixture could kill it; it stays a documented limit, not a gap.
4. **X15 is a genuine battery gap**: D5's tag-strip half of the flat compare is advertised by the
   code but demonstrated by no fixture (the genuine capture carries the quote without intervening
   markup). Probe B gives the fixture shape that kills it: a capture with markup inside the quote
   span, manifest re-pinned, mirror direction. Candidate for a future battery module.
5. **N21 corroboration (adjacent)**: my baseline rerun independently reproduces `N21 … SURVIVED`
   under its frozen `silence` cell, and `plans/battery38/d5m.py`'s own docstring names the only
   available kill as mirror-shaped (`d5m-n21-manifest-row-2`: ref `D5 ok`, mutant `D5 DEFECT`), which
   the frozen direction cell cannot count. My X13/X14/X16 kills show the rest of the D5 surface is
   attributed-killed. This supports the L1's honest-stop treatment of C1 (not relabelled).
6. **Minor rule observation**: X02/X03/X08/X12 were killed by r36-* fixtures whose `defects` cell is
   absent; the counter then sets `declared := observed reference DEFECT set`
   (plans/round38_c1_verify.py, `attributed`), so the "declared" half of the silence rule is vacuous
   for the round-36 modules. All battery38 fixtures declare explicitly. Not a defect of this round;
   worth remembering when the rule is next tightened (finding 2).

## Receipts

Under `.ufo/waves/round-38/falsify/F38XMutRerunMain/`:

- `baseline-frozen.txt` — frozen counter on the tip clone (before; killed=21/22, N21 survived).
- `extra-run.txt` — dev counter, 16 extras (after; killed=12/16, per-mutant kill lines).
- `survivor-probes.txt` — probes A1 (X10), A2 (X07), A3 (X04).
- `survivor-probeB.txt` — probe B (X15 tag-strip differential).
- `xmut-counter-diff.txt` — dev counter vs frozen counter: append-only override block.
- `restoration.txt` — before/after hashes and git state.

## Restoration

Scratch `/fast/scratch/hyaku/kengaku-r38/F38XMutRerunMain` (clone + dev counter + probes) is deleted
after this report; receipts were copied out first. No lane file, no sibling lane, no fleet-root file
was written; no mutating git/jj command was run anywhere. Evidence (`restoration.txt`):

- clone HEAD `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`, `status --porcelain` 0 lines;
- clone gate sha256 `ea63882240e6…edd41` = frozen PINS digest, before and after all runs
  (both counter runs printed `PINS total=14 mismatched=0`);
- original lane gate sha256 unchanged `ea63882240e6…edd41`; the live lane's only dirty entries are
  the wave's own `falsify.ready.dispatched` marker and this report dir (concurrent wave activity;
  this seat wrote nothing there but this report).

VERDICT: xmut-rest-killed-12/16
