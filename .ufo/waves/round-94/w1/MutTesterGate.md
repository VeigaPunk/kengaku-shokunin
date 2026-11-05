# MutTesterGate — scoped findings, round 94 wave 1

Mutation test of `plans/round94_freeze_integrity.py` (v2, frozen sha 8574b4d5…) through the frozen
`plans/round94_c2_counter.py` at measured tip T = 90c7677f0ba95d0930d93bda6a14aa50605ebe2e.
20 byte-level mutants (all distinct from the counter's K1–K7) + pristine null; every run through
the counter CLI (`--tool-file`, --shared clone at T). **Baseline: null passes 5/5, rc 0.**
**Result: 11 killed, 9 survived.** Full table, receipts and mutant bytes:
`waves/round-94/w1/MutTesterGate/report.md`, `…/mutants/`, `…/receipts/`, `…/tabulation.json`.

Kills (counter strength confirmed): M03 rev-list --merges-only, M05 intact/broken summary swap,
M06 battery truncated to 14, M08 `inside` never set, M09 ancestry check dropped, M11 freeze-bytes
check weakened, M12 rev-bytes check dropped, M13 touched threshold >1, M14 exit polarity flipped,
M16 blob rc ignored, M17 empty table accepted — each dies at its battery case and/or W1/W2/W4/W5,
with W5-null inheritance doubling every evaluate/parse_table-site kill.

## FINDING lines

FINDING F1 minor calibration-coverage: M01-paths-dup-guard-dropped survives 5/5 — no leg exercises duplicate `--paths`; round-93 W-6 (dup rows) is only closed in claims mode (K7), a gate accepting dup paths-mode rows passes the counter. Route: round 95 battery/W2 case `--paths probe.py probe.py` → rc 2.
FINDING F2 minor calibration-coverage: M02-unterminated-block-accepted survives 5/5 — gate docstring promises could-not-evaluate for an unterminated frozen-instruments block but neither the 15-case battery nor any W2 fixture contains one. Route: round 95 case.
FINDING F3 minor calibration: M15-predicate-always-pass survives 5/5 — the counter polices rc/summary/INSTRUMENT lines but never the gate's own `PREDICATE freeze-integrity …` line; a gate printing `pass` while exiting 1 is invisible to it (lane receipts do read that line).
FINDING F4 minor calibration (sharp): M20-battery-broken-and-concealed survives 5/5 with a genuinely red battery — receipt `receipts/direct/M20-direct-gate.txt` shows `BATTERY B02 RED` and forged `SELFTEST cases=15 ok=15` in the same stdout, rc 0; W3 checks the echo's format, not its truth, and W5 has no battery-path mutant, so a gate controlling its own echo conceals a broken battery from every leg. Does NOT flip R94-C2 at T (real gate honest; no W leg fails at T). Route: round 95 K8 battery-path mutant in W5 and/or re-derive `ok=` from echoed BATTERY lines.
FINDING F5 info: M04 (rev bytes compared to freeze bytes instead of table) is semantically absorbed — with an ancestor freeze and `--full-history`, any table-vs-rev byte difference implies touched ≥ 1, so brokenness and summaries are invariant; verdict strings differ only for lying-table+edited-path, a combo no fixture constructs.
FINDING F6 info: M10 (rev-list rc ignored) unobservable in-harness — rev-list runs only on resolve()-validated, ancestor-connected revs; no leg forces a rev-list failure.
FINDING F7 info: M18 (`^{commit}` peel dropped) unobservable — every counter rev is a raw commit id.
FINDING M07 info: battery failures made non-fatal are indistinguishable on a green battery; reds still surface via the W3 SELFTEST echo unless the echo is forged too — see F4 for that escalation.

No tabled instrument was changed; the frozen rule is respected. No tool installs. Lane bytes
re-verified unchanged after all runs (8574b4d5… / 17d2a7d5…); scratch removed.
