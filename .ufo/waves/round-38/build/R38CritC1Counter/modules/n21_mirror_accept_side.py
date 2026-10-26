"""N21 is frozen as direction=silence, but its mutation only shortens the manifest scan, which can only turn
`pinned` True->False.  This fixture shows the reachable direction: reference D5 ok, mutant D5 DEFECT."""

import hashlib
import json


def build(ctx, d):
    (d / "spec.json").write_text(json.dumps({"d5": {
        "label": "DIR-R38: ", "require": "alpha", "forbid": "zzz",
        "capture_name": "cap.txt", "manifest_name": "SHA256SUMS", "quote": "alpha"}}))
    (d / "line.txt").write_text("DIR-R38: alpha\n")
    cap = d / "cap"
    cap.mkdir()
    body = b"alpha\n"
    (cap / "cap.txt").write_bytes(body)
    wrong = hashlib.sha256(b"other\n").hexdigest()
    (cap / "SHA256SUMS").write_text(f"{wrong}  cap.txt\n{hashlib.sha256(body).hexdigest()}  cap.txt\n")
    return ["d5-line", "--file", str(d / "line.txt"), "--capture-dir", str(cap), "--spec", str(d / "spec.json")]


FIXTURES = [{"fid": "n21-accept-side", "expect": "accept", "defects": [], "build": build}]
