"""a7str — build() returns a bare string (review F2): it used to be char-split into a passing argv, so a
fixture with no argv at all still landed as `expect=error` and could credit an error-direction kill.
"""


def build(ctx, d):
    return "reject"


FIXTURES = [
    {"fid": "a7-bare-string", "tool": "anchor", "expect": "error", "defects": [], "build": build},
]
