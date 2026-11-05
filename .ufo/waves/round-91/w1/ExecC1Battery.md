# ExecC1Battery — R91-C1 control battery (round-91 w1)

Verdict: all 9 battery lines executed in a `--shared` scratch clone at tip C
`a8de3e6933a220ad12e3fb3523ce4627a44c8cf0`; lane untouched; every rc recorded as measured.
Evidence files: `.ufo/waves/round-91/w1/ExecC1Battery/controls.txt` (9 CONTROL lines) and
`.ufo/waves/round-91/w1/ExecC1Battery/report.md`.

1. **Measured positive at C = rc 1, not the frozen prediction's rc 0.** Command
   `python3 $S/c1_replay.py --lane $S/lane --rev a8de3e6933a2… --work $S/w-pos` → exit 1,
   `TARGET executed_rows=35 member=modernize-scientific-stack located=1 executed=0 cases=10
   legs=20 mismatches=10 defects=10`, `PREDICATE R91-C1 fail`, ten identical
   `DEFECT L5 receipt names unknown case ?`. Recorded as a mispredict against the frozen
   "After (predicted) exit 0" claim.
2. **Routed defect (instrument, not predicate): `parse_receipt()` reads the case id from an
   `id=` token the receipt never emits.** The receipt's case id is the bare second whitespace
   token of each `CASE` line; the parser harvests only `key=value` tokens and defaults the id to
   `"?"`, so all 10 cases print `L5 receipt names unknown case ?`. Scratch-copy repair changing
   only that token extraction (`line.split()[1]`; predicate untouched) at C: exit **0**,
   `executed=1 cases=10 legs=20 mismatches=0 defects=0`, `PREDICATE R91-C1 pass` — the parser
   defect alone accounts for the L5 failure; legs L1-L4 and L6-L9 all pass at C.
3. **Tamper controls all fail at their named leg (exit 1 each):**
   - ledger-only (receipt deleted, rev `9d010ad4…`): first defect `L1 receipt absent at
     revision: corpus/evidence/round91/modernize-probe.txt`.
   - forged-tip (sibling `092783db…` via `commit-tree`, `merge-base --is-ancestor` rc 1; rev
     `a458f262…`): first defect `L3 LANE_TIP 092783db… not an ancestor of a458f262ced1`.
   - forged-stamp (TOOL_SHA→`e70210cb…`, rev `297e245b…`): `L9 stamp fields mismatch
     (tool=e70210cb…)` — 11th defect line, after the L5 noise.
   - decorative-stamp (`HOST_PYTHON Python 9.9.9`, rev `dfd4d58f…`): `L9 stamp fields mismatch
     (… python=Python 9.9.9 …)` — 11th defect line.
   - probe-tamper (one appended line, rev `9189e646…`): `L8 probe pin d70210cb… vs bytes
     be042c25…` and `L9 stamp fields mismatch (tool=d70210cb…)` — 11th-12th defect lines.
4. **Executed-gating holds:** counter L262 `all_pass = all(legs)` → L266 `executed=` `1 if
   all_pass else 0` → L271 `return 0 if all_pass else 1`; at the receipt-deleted revision TARGET
   prints `executed=0`, exit 1. No code path prints `executed=1` without all legs passing.
5. **Caveat for integration:** defect ordering puts L5 parser noise ahead of L8/L9 lines, so
   first-three-DEFECT excerpts for controls 5/6/7 show L5 lines; decisive tail lines are recorded
   verbatim in both evidence files.

Scratch `/fast/scratch/hyaku/kengaku-r91/ExecC1Battery` deleted at exit. No tools installed.
