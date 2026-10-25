#!/usr/bin/env python3
"""Which persisted hand-fixture expectation keys are actually asserted by the selftest?"""
import json
from pathlib import Path

HAND = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/hand")
SEL = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/config_projection.py").read_text()

files = {
    "cascade-order.case.json": "order_case",
    "url-only.fixture.json": "url_case",
    "url-only.expected.json": "url_expected",
    "index-shuffled-ids.fixture.json": "index_case",
}
for fname, var in files.items():
    data = json.loads((HAND / fname).read_text())
    print("== %s  (var %s)" % (fname, var))
    for k in sorted(data):
        # is the key referenced anywhere in the selftest source?
        used = ('["%s"]' % k) in SEL or ('"%s"' % k) in SEL
        print("   %-52s asserted_in_selftest=%s" % (k, used))
    print()
