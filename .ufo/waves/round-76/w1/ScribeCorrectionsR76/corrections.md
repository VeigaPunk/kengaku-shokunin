# Correction handoff

Axes: coverage; calibration. Paths are relative to the lane root.

## Integration instruction superseding the initial drafting request

KengakuR76 directed this seat not to allocate Q56, duplicate Q55, or replace already integrated QUALITY/SKILL/lesson text. This handoff therefore checks all seven existing legs and supplies only D6 ledger text. No production file was edited.

## Seven discharge dispositions

1. R75-D1: existing QUALITY.md Q55, lines 1264–1270, passes the frozen leg. It cites the report-ordering rule, erratum commits and round-75-verifier-spotcheck.md. Do not append another criterion.
2. R75-D2: existing SCORECARD.md:3439 passes: actual receipt stamp 9f8f0f2180821d165f60e400277f192d92afbbce and report tip 5d9a0ccc both appear on its defect line.
3. R75-D3: existing SCORECARD.md:3440–3443 passes. Independent committed-tree derivation at 43255758 produced total=60 split=4/36/20; receipt derive-index.txt.
4. R75-D4: existing SKILL.md:708–709 passes. Executed selftests printed cases=8 red=7 and arms=5, both exit 0. C2 also printed real=10 expected_matched=10 wrong_id=0.
5. R75-D5: existing LOG.md:2855–2859 passes its six-line-block leg; it explicitly supersedes cases=7 red=6 and the erroneous receipt revision attribution.
6. R75-D6: both named receipts exist, print their respective predicate pass, and stamp 6977019bdf56a88921e14f728167da8f5726c1fc; the leg resolved that stamp as ancestor.
7. R75-D7: existing corpus/lessons/round-74.md:72–77 passes; its separate correction entry names the in-place reflow and requires appended entries.

## D6 ledger field values — byte-ready

Use these exact JSON string values in the R75-D6 row; retain the ledger's other required fields. The integrator must set close_commit to the actual committed discharge tree, not infer it from the receipt's measured stamp.

```json
"close": "2026-11-04 R75-D6: round-74 tip receipts retained; both print predicate pass and stamp 6977019bdf56a88921e14f728167da8f5726c1fc."
"verified_at": "2026-11-04"
"check": "grep -q 'PREDICATE R74-C1 pass' corpus/evidence/round76/r74-c1-tip.txt && grep -q 'PREDICATE R74-C2 pass' corpus/evidence/round76/r74-c2-tip.txt"
```

These are field values, not a complete JSON object. The grep command checks pass literals; the C2 D6 leg independently resolves receipt-stamp ancestry. This seat observed receipt bytes and executed that leg, but did not mint either round-74 receipt or rerun either round-74 gate.

## Exact leg-only results

```text
LEG D1 ok QUALITY criterion cites R75-D1 + lesson
LEG D2 ok SCORECARD line with R75-D2, stamp 9f8f0f218082, 5d9a0ccc
LEG D3 ok SCORECARD line with R75-D3, total 60, split 4/36/20 at 43255758
LEG D4 ok registry rows carry cases=8 red=7 / arms=5
LEG D5 ok LOG block with R75-D5, cases=8 red=7, stamp 9f8f0f218082
LEG D6 ok r74-c1-tip.txt=pass/ancestor r74-c2-tip.txt=pass/ancestor
LEG D7 ok round-74 lesson appended correction naming R75-D7
LEG_ONLY_EXIT 0
```

This is not a full R76-C2 predicate or ledger verdict. See legs.txt for execution provenance.
