"""F39SentinelAudit S2: rewrite two pinned lane files AFTER the parent's PINS line.

The build child runs after `mism` is computed (audit :279) and before the final re-hash (:416).
Contributing no fixtures keeps every other number of the receipt unchanged.
"""
import pathlib

FIXTURES = []
_LANE = pathlib.Path(__file__).resolve().parents[2]
for _rel in ("plans/round37_c1_attribution.py", "plans/pkg_gate.py"):
    _p = _LANE / _rel
    _p.write_text(_p.read_text() + "\n# tampered by F39SentinelAudit\n")
