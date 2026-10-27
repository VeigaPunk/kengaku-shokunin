"""Name-keyed control fence (R48C1ExecControls, kengaku round 48 wave 1).

A stricter name-keyed variant of the round-45 control fence (`.ufo/waves/round-45/claims/fences/keyed_name.py`,
sha256 d21a6a173c68b13ce9abcd2716f37afaed1930646faa43a266adfd4258b9452e), which keyed only on the literal
path component `/refusals45-`.

This variant tries HARDER to key the verdict on names, and is the control that tests Q39 name hiding:

  * the last three path components of the fixture directory `d` (the counter-chosen path),
  * the basename of `d` itself,
  * the basename of every argv token,

are scanned for group or module name markers (`refusal`, `sealed`, `hostile`, `battery`, `h01`..`h09`,
`f1_`..`f20_`, `a_class`, `a_row`, `a_route`, `a_alt`, `a_err`, `a_url`, `o_alt`, `o_clause`, `o_excuse`,
`o_scan`, `u5_`, `u6_`, `u7_`, `u9_`, `u14c_`, `n01`..`n16`). A hit refuses the fixture with the marker.

SCOPE OF THE SCAN (deliberate, and the reason this fence is a meaningful control): only the components at or
below the fixture's own build root are scanned. The absolute scratch prefix is NOT scanned, because the
scratch prefix is the measurement harness's own name, not the counter's choice of name - a fence that matched
it would be a refuse-all fence, not a name-keyed fence. The scanned components are exactly the names the
counter chooses (fixture dir, fixture parent, build dir) plus the argv basenames.

It opens no file and starts no git child: the decision is name-shaped, which is precisely the shortcut the v3
counter's Q39 name hiding must defeat. Under the frozen v3 predicate the control must therefore FAIL: the
hostile modules it cannot name are admitted, an admission in a hostile leg keeps `clean < total`, and the
frozen line cannot print.

This file is a control fixture only. It is never proposed as the C1 fence and it lives in scratch, not in the
lane.
"""
import os

MARKERS = (
    "refusal", "sealed", "hostile", "battery",
    "h01", "h02", "h03", "h04", "h05", "h06", "h07", "h08", "h09",
    "n01", "n02", "n03", "n04", "n05", "n06", "n07", "n08", "n09",
    "n10", "n11", "n12", "n13", "n14", "n15", "n16",
    "f1_", "f2_", "f3_", "f4_", "f5_", "f6_", "f7_", "f8_", "f9_",
    "f10_", "f11_", "f12_", "f13_", "f14_", "f15_", "f16_", "f17_", "f18_", "f19_", "f20_",
    "a_class", "a_row", "a_route", "a_alt", "a_err", "a_url",
    "o_alt", "o_clause", "o_excuse", "o_scan",
    "u5_", "u6_", "u7_", "u9_", "u14c_",
)
SCAN_DEPTH = 3          # fixture dir, its parent, and the build dir the counter names


def _names(d, argv):
    """The names the counter chose, and the argv basenames. The scratch prefix is never scanned."""
    out = []
    parts = [p for p in str(d).split(os.sep) if p]
    for part in parts[-SCAN_DEPTH:]:
        out.append(part.lower())
    if parts:
        out.append(os.path.basename(str(d)).lower())
    for tok in argv:
        if isinstance(tok, str) and tok:
            out.append(os.path.basename(tok).lower())
    return out


def breach(d, argv, tool):
    for name in _names(d, argv):
        for marker in MARKERS:
            if marker in name:
                return f"name-keyed refusal: {marker} in {name}"
    return None
