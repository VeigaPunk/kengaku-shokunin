"""The whole reachable d5-line space for N21 (manifest scan truncated to its first line)."""

import hashlib
import json

CAP = b"alpha\n"
DIG = hashlib.sha256(CAP).hexdigest()
WRONG = hashlib.sha256(b"other\n").hexdigest()
VARIANTS = {
    "digest-on-line2": f"{WRONG}  cap.txt\n{DIG}  cap.txt\n",
    "digest-absent": f"{WRONG}  cap.txt\n",
    "digest-on-line1": f"{DIG}  cap.txt\n{WRONG}  cap.txt\n",
    "digest-line1-only": f"{DIG}  cap.txt\n",
    "manifest-empty": "",
    "blank-lines": f"\n{DIG}  cap.txt\n\n",
    "blank-first": f"\n{DIG}  cap.txt\n",
}
BAD_LINE = {
    "ok": "DIR-R38: alpha\n",
    "missing-require": "DIR-R38: beta\n",
    "carries-forbid": "DIR-R38: alpha zzz\n",
}


def make(mvar, lvar):
    def build(ctx, d):
        (d / "spec.json").write_text(json.dumps({"d5": {
            "label": "DIR-R38: ", "require": "alpha", "forbid": "zzz",
            "capture_name": "cap.txt", "manifest_name": "SHA256SUMS",
            "quote": "alpha" if lvar == "ok" else "gamma"}}))
        (d / "line.txt").write_text(BAD_LINE[lvar])
        cap = d / "cap"
        cap.mkdir()
        (cap / "cap.txt").write_bytes(CAP)
        if mvar != "manifest-absent":
            (cap / "SHA256SUMS").write_text(VARIANTS[mvar])
        return ["d5-line", "--file", str(d / "line.txt"), "--capture-dir", str(cap),
                "--spec", str(d / "spec.json")]
    return {"fid": f"n21s-{mvar}-{lvar}", "expect": "accept" if (mvar, lvar) == ("digest-on-line1", "ok") else "reject",
            "defects": [], "build": build}


FIXTURES = [make(m, l) for m in list(VARIANTS) + ["manifest-absent"] for l in BAD_LINE]
