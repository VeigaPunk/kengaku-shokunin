# R34 C2 counter draft

Files changed: `.ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py` (executable draft); this report.

Behavior: implements N1–N8 as an offline lane-root counter, prints individual `DEFECT` lines and `checks=8 defects=<n>`, returns 0 only when defect-free, and includes `--selftest`. N7 explicitly reads the round-33 falsify ledger and requires a dated correction giving 36+53=89. No repository artifacts were edited outside the assigned wave directory. No tools installed.

Exact retained evidence (command → output):
- `python3 .ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py --selftest` → `SELFTEST cases=10 failed=0` (all ten CASE lines PASS).
- `python3 .ufo/waves/round-34/build/R34C2CounterDraft/round34_defects.py --lane .` → `DEFECT N3 ... .ufo/reports/round-31/kengaku.md is unreadable`; `DEFECT N4 ... .ufo/reports/round-32/kengaku.md is unreadable`; `DEFECT N7 ... no dated correction stating ledger sum 36+53=89`; `checks=8 defects=3`, exit 1. N3/N4 paths could not be opened in the lane, and N7's pristine-tip red is expected per L1 coordination; correction is integration-owned.
- Frozen claim source: `plans/round-34-claims.md:71-101` defines C2 checks and mutation mapping; `corpus/lessons/round-33.md:48-53` gives seat ledger values 36 build + 53 falsify = 89. L1 coordination specifically directed N7 to be red until its integration correction.

Risks/blockers: the external fleet report files referenced by N3/N4 are absent at the expected paths in this checkout, so the report checks cannot evaluate their content here. The N7 dated correction is not yet present. Main integration should review append-only and width/newline resistance details, then rerun after landing.

VERDICT: c2-counter-drafted (selftest 10 cases, tip defects=3)
