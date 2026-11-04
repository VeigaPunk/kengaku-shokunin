# ProbeR84 — R84-C1 instrument (gcode-to-text offline probe)

Status: ok. Full detail: .ufo/waves/round-84/w1/ProbeR84/report.txt

Delivered (drafts; L1 installs production copies):
- plans/round84_gcode_probe.py ← .ufo/waves/round-84/w1/ProbeR84/round84_gcode_probe.py
  sha256 82f359e67840ec5ed876dc1904c0f69b158d2f1bc33278df3dfd64c51d528e75
- plans/round84-cases.json ← .ufo/waves/round-84/w1/ProbeR84/round84-cases.json
  sha256 5b86f8d7efc24a529b4c53a23c6a4ccaed51866428535e6f0fcb4dbf13982cb5
- corpus/evidence/round84/gcode-to-text-probe.txt ← .ufo/waves/round-84/w1/ProbeR84/gcode-to-text-probe.txt
  sha256 8224f12e53b456ccdfacd49cb2b60895497a19f7f42d5bca304ebccfcb71fbda (pre-commit mint)

Acceptance evidence:
- Real-lane replay: probe-run.txt, exit 0, all 8 vectors as predicted (16 legs), mismatches=0.
- Negative control (staged `exact` row one byte long, predicted P/P → observed P/F):
  probe-negative.txt, exit 1, cases=8 mismatches=1, table sha recorded as drifted.
- Selftest: probe-selftest.txt, 13/13 (frozen table bytes, stamp order/values, observations,
  wrong-subject → 2, wrong-predicted → 2, content drift → 1, three classification fixtures).
- Subject sha verified at load: 6b049dc626aa103b20d165552e5cb39ba02c6803b04ba06a43d79435b5f701a6.

Host: Python 3.14.8, OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026),
bubblewrap 0.13.1. No tool installs or upgrades.

Deviations from the frozen claims: none in predicate/target/case table/controls/kill rule.
Disclosed instrument-level notes: (a) lane table preferred, tool-adjacent frozen copy as
byte-pinned fallback for the acceptance run; (b) staged content is data, so a drifted staging
row is a mismatch (exit 1) rather than a re-freeze, while CASE_TABLE_SHA carries the full pin;
(c) the delivered receipt is pre-commit (WORKTREE dirty, LANE_TIP b12a9d46…) — the L1 re-mints
after committing with `python3 plans/round84_gcode_probe.py --lane . --work <dir>`, which yields
WORKTREE clean and the committing tip.

Table-strength note (no claim change): no non-UTF-8 or non-regular-file row in the eight frozen
cases, so the P/F partition is proven on the text-decodable subset only; no vector is affected.
