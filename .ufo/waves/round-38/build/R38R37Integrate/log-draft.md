# LOG.md draft — round 37 wave-2 integration (paste-ready, L1 owns the edit)

Source: `.ufo/waves/round-38/build/R38R37Integrate.md` (seat R38R37Integrate, round-38 wave 1).
Integrate under `.ufo/waves/round-38/` in LOG.md's round-38 entry, not as a round-37 edit.

- **Round-37 wave 2 read in full (closures D1).** `37/37` seats wrote `.ufo/waves/round-37/falsify/*.md`
  (spec `falsify-spec.json` has 37 items, `missing=[]`); all 37 reports end on a `VERDICT:` line
  (`nonconforming=0`), last write `2026-10-26T02:37:19-03:00`, committed together at `21e6251`
  (`round-37: wave-2 reports and results (37/37)`, 380 files). Round 37's closure read 19 of them; this
  round integrates all 37 (`inventory.tsv` beside the report).
- **What wave 2 returned.** 33 of the 37 carry at least one defect, survivor or observation; 3 report "no defect found"
  (`F37ReopenRows`, `F37RevBatteryCode`, `F37MutProbeCases`) and 1 (`F37C1RerunPy313`) reports no finding at all. 13 non-frozen gate survivors plus 1 diagnostic survivor
  (`F37MutP7` D1) became the frozen round-38 mutant list N02–N07, N09–N12, N19–N22; the remaining
  survivors (P5 X4 branch shadow, P8 S1 mirror half, D5 S1, P23 Y2/Y3) are not in N01–N22 and are routed.
- **Routed items D1–D7, disposition.** D1: this report + the `21e6251` commit (integration complete, no
  lane edit by the seat). D2: `R38MapErratum` + `R38MapRetro`; the round-38 C2 counter's V7 now derives
  every label from all receipt cases carrying the tag (`plans/round38_c2_verify.py:241-247`). D3:
  `R38AnchorBind` (per-row binding; `rows=107 tokens=15 defects=0` at the tip). D4: `R38LedgerTip`. D5:
  twelve `R38Bat*` seats against N01–N22. D6: `R38SiblingCite` + `R38ConnSibling`. D7: done at freeze —
  `plans/round38_c2_verify.py` pins every input it reads (claims §C2).
- **Carried open into round 39 (not defect-free, not closed).** The C1 predicate's observable is
  `(exit code, DEFECT set)`, so a gate that recognises a fixture by content prints the full pass
  (`F37CritRenamed`); `wrong=0` is a drift pin over transcribed declarations (`F37CritOverfit`); the
  round-37 C1 count of 50 over-counts by 6 (`F37CritC1Axis`); round-38 V4/V5 still read the receipt's own
  `match=` text and compare decoded text (`plans/round38_c2_verify.py:171,195`); `pkg_gate.py:285` still
  labels a character count `bytes=`; the ledger-tip `--work` precondition and the P10 `uv`/biopython
  dependency are undocumented on the rows that need them.
- **Round-38-facing risk recorded this round.** `plans/anchor_digest_check.py:80` hardcodes
  `Erratum \(round 37\)`; any round-38 erratum that corrects an anchor token will be invisible to the
  exemption (it will red, not launder). If round 38 appends such an erratum, the pattern needs extending
  in the same landing.
