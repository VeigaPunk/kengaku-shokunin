# R44ExecShapeDiff — normalised-AST re-spelling screen (executor, round 44 wave)

**Deliverable:** `.ufo/waves/round-44/wave/R44ExecShapeDiff/shape_diff.py` (17830 bytes,
sha256 `61d974f631751b0cf5214dcf1c11515c54e13120c83d1394ce8471209eda98ab`), stdlib only, read-only:
it parses text with `ast` and never imports, executes or writes anything.
**Verdict:** selftest passes — witness against itself flags all 6 fixture self-pairs at 1.000; against
`plans/battery43` it flags 0 of 252 enforced pairs (max 0.577).

## Axes (Godspeed)

| axis | this seat's move |
|---|---|
| calibration | the non-author screen the C1 counter cannot do: witness-vs-fixture shape distance, with a measured true positive (0.961) and a measured false-positive floor (0.577/0.700) |
| evidence | every number below is a pasted command output; envelope lines kept (Q32) |
| harm | zero writes outside the wave dir + scratch; no tool, battery, counter or corpus file touched |

## What the tool does

For every module-level function in the battery and in the witness it builds a normalised token sequence of
`ast.dump` and reports `difflib.SequenceMatcher` ratios:

- normalisation: local/parameter/function names → `_`; every constant → a type marker (`<S>` str, `<B>` bytes,
  `<N>` number); docstrings dropped; **attribute names survive** (`_.write`, `_.sha256`) so the ctx/API surface
  stays part of the shape;
- inventory is static and exact: a module-level `FIXTURES` table is resolved through list aliases, `+`
  concatenation and the `if f["fid"] == "<cid>"` comprehension filter, so each `build` target is a `fixture` and
  everything else is a `helper`; a module with no resolvable table falls back to `ctx`-first functions and says
  so (`table=absent`);
- **enforced** pairs = battery *fixture* × witness *fixture* — the screen's subject. Any pair with a helper on
  either side is **advisory** (shared plumbing); advisory pairs are always printed, never gate the exit status;
- exit 0 = no enforced pair above `--threshold` (default 0.80), exit 1 = flagged, exit 2 = bad input.
  `--all`, `--json`, `--quiet`, `--selftest`, `--control DIR` available.

## Selftest (pasted, whole file `.ufo/waves/round-44/wave/R44ExecShapeDiff/selftest.txt`)

```
$ .ufo/waves/round-44/claims/envelope.sh "$S/env" python3 .ufo/waves/round-44/wave/R44ExecShapeDiff/shape_diff.py --selftest
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind .../R44ExecShapeDiff/env .../env
  --bind .../env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid
  --die-with-parent -- python3 .../shape_diff.py --selftest
ENVELOPE start 20:38:23 cwd=/home/vgpnk/Projects/shokunin
SELFTEST witness=.../.ufo/waves/round-44/claims/witness/w_u.py table=resolved fixtures=6 helpers=4
SELFTEST self fixtures=6 self-pairs-flagged=6/6 all1.0=yes
SELFTEST self off-diagonal-flagged=4 (informational: witness near-variants)
SELFTEST self near 0.930 w_u:u14_missing_claims_flag ~ w_u:u14c_odd_claims_name
SELFTEST self near 0.927 w_u:u3_row_path ~ w_u:u6_long
SELFTEST self near 0.924 w_u:u5_short ~ w_u:u6_long
SELFTEST self near 0.913 w_u:u3_row_path ~ w_u:u5_short
SELFTEST control battery=.../plans/battery43 fixtures=42 pairs=630 enforced=252 flagged=0 advisory=1 max-enforced=0.577
SELFTEST control advisory 0.823 a_alt:row ~ row
SELFTEST RESULT pass
ENVELOPE end 20:38:28 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Witness inventory the resolver finds: fixtures `u3_row_path u5_short u6_long u7_twin_captures u9_dirty_erratum
u14c_odd_claims_name` (6 = the 5 `FIXTURES_ROWS` entries plus `u14c` selected out of `FIXTURES_ORD` by the
comprehension; `u14_missing_claims_flag` correctly stats as a helper because the filter drops it), helpers
`row lane repo u14_missing_claims_flag` (4).

## Controls (all under the round-44 envelope; receipts in `.ufo/waves/round-44/wave/R44ExecShapeDiff/`)

| # | control | command tail | result |
|---|---|---|---|
| A | witness as battery (true positive at 1.0) | `--battery .ufo/.../claims/witness/w_u.py` | `pairs=100 enforced=36 flagged=12 max-enforced=1.000`, all six self-pairs `FLAG 1.000`, plus the four in-family near-variants 0.913–0.930; exit 1 |
| B | rename/reformat re-spelling (true positive) | `--battery $S/battery-respell` (module kept as `respell-control-module.py`, sha256 `ba53660a…`) | `pairs=40 enforced=12 flagged=4 max-enforced=0.961`: `rs_short ~ u5_short` 0.961, `rs_twin ~ u7_twin_captures` 0.925; exit 1 |
| C | required control: `plans/battery43` (expect low) | `--battery plans/battery43` | `fixtures=42 pairs=630 enforced=252 flagged=0 advisory=1 max-enforced=0.577`; only advisory `0.823 a_alt:row ~ row` (helper/helper, `"| " + join`); exit 0 |
| D | `plans/battery42` (second low control) | `--battery plans/battery42` | `fixtures=29 pairs=490 enforced=174 flagged=0 advisory=7 max-enforced=0.700` (`o_scan:xo7_skipped_r38 ~ u9_dirty_erratum`); advisories are `o_clause:clean_order ~ repo` 0.812 and `o_clause:xo3_withdrawn ~ repo` 0.800 (battery42:96-104 really is the witness `repo` outline: `ctx.init` + two writes + two commits), `o_scan:_args ~ u14c…` 0.891; exit 0 |
| E | no-table fallback | `--battery $S/notable.py` (a single `ctx`-first function) | `fixtures=1` via the fallback, `enforced=6 flagged=0 max-enforced=0.634`; exit 0 (receipt `screen-no-table-fallback.txt`) |
| F | JSON path | `--battery plans/battery43 --json` | parses (`.ufo/.../R44ExecShapeDiff/screen-battery43.json.txt`); keys `advisory battery enforced_pairs fixtures flagged max modules pairs threshold witness`; `enforced 252 flagged 0 advisory 1 max 0.5769 pairs 630`; exit 0 |

Envelope line for every run: `ENVELOPE end 20:38:2x/3x exit=0|1 local_bin_content_before=328be01808ba022f
after=328be01808ba022f unchanged` — no PATH-dir content change, every measurement valid (A and B exit 1 by
design: they are the flagged cases; C, D, E exit 0).

Fixture-count cross-check against the frozen claims: `battery42 fixtures=29` + `battery43 fixtures=42` = **71**,
the number in `plans/round-44-claims.md` ("battery42 + battery43 (71 fixtures)"), so the inventory agrees with the
counter's own fixture enumeration.

## Use at integration (for the L1, not run here — `plans/battery44` does not exist yet: `ls plans | grep battery4[234]` → `battery42 battery43`)

```
.ufo/waves/round-44/claims/envelope.sh "$S/env" python3 .ufo/waves/round-44/wave/R44ExecShapeDiff/shape_diff.py \
  --battery plans/battery44            # exit 0 = no fixture re-spells a witness fixture above 0.80
```
Non-author review line to paste next to the C1 result: `SHAPE pairs=… flagged=0 max-enforced=…`. Expect a
`battery44` max-enforced well under 0.80 given 0.577/0.700 for the standing batteries; a fixture at ≥0.93 is a
re-spelling candidate and must be rewritten with a different construction, not relabelled.

## Limits named now

1. **Threshold band is narrow at the top.** The witness's own fixtures sit 0.913–0.930 from each other
   (`u3/u5/u6` differ only in the anchor expression; `u14/u14c` only in `--claims`), so a genuine
   distinct-construction fixture at ≤0.93 and a renamed copy of a witness fixture are separated only by the
   0.80 line and by the reviewer's eye. Use the number as a screen, not as proof.
2. **Intent is not observable.** A fixture rewritten by hand from the witness's *reading* rather than its AST
   scores low; a mechanically restructured copy scores high. This complements, it does not replace, the
   non-author read the frozen claims require.
3. **Enforced = fixture×fixture only.** Plumbing overlap (`row`, `lane`, `repo`) is advisory; `a_alt:row` at
   0.823 and `o_clause:clean_order ~ repo` at 0.812 are real overlaps that deliberately do not gate.
4. **One token sequence per function.** `autojunk=False`; no statement reordering, no sub-tree matching, so a
   fixture that inlines a witness helper's body while the witness calls it scores lower than it deserves.
5. **Not a battery module.** `shape_diff.py` contains the words `witness` and `/home/`, so it must **never** be
   placed in `plans/battery44/` — the counter's SIDECHANNEL scan would (correctly) reject the battery. It is an
   advisory tool in the wave dir only; it reads the witness by absolute path and nothing else.
6. Control B's module lives in this report dir (`respell-control-module.py`); it is a copy of two witness
   fixtures by construction, so it must never be dropped into `plans/battery44/` either.

## Files

- `.ufo/waves/round-44/wave/R44ExecShapeDiff/shape_diff.py` — the tool.
- `.ufo/waves/round-44/wave/R44ExecShapeDiff/{selftest,witness-as-battery,screen-battery42,screen-battery43,screen-battery-respell,screen-no-table-fallback}.txt` and `screen-battery43.json-summary.txt` — pasted receipts (<= 9.2 KB each; the 169881-byte full `--json` receipt `screen-battery43.json.txt` was quoted, its sha256 `a05da348c285aff1140af37813fdf82a7a7d14ac2ae624a3f587e9c87762cf1a` recorded in the summary, and deleted).
- `.ufo/waves/round-44/wave/R44ExecShapeDiff/respell-control-module.py` — control B's 2-fixture module.
- nothing else written; no install, no tool/corpus/plans edit; scratch `$S` removed with `scratch_guard.py safe-rm`.

VERDICT: shape-diff-selftest-ok
