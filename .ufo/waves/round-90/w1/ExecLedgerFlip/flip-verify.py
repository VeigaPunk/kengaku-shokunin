import json, copy, hashlib, sys
from collections import Counter

BASE_PATH = "base-ledger.json"
OUT_LEDGER = "ledger-flipped.json"
MEMBER = "merge-diff-arc-agi-task"
ROW = {
    "classes": ["file-artifact", "git-plumbing", "serialization-schema", "stdout-inspection", "subprocess-exec"],
    "evidence": "no-blocker: tests/test_outputs.py sha256=2754ba6c5c5f75c9",
    "receipt": "corpus/evidence/round90/merge-diff-probe.txt",
    "round": 90,
    "status": "executed",
    "subject": "tb2-header",
    "verdict": "cases",
}
CLASSES = ["git-plumbing", "serialization-schema", "file-artifact", "stdout-inspection", "subprocess-exec"]
EXPECT_BEFORE = {"members": 88, "executed": 33,
                 "git-plumbing": (1, 3), "serialization-schema": (3, 10), "file-artifact": (24, 76),
                 "stdout-inspection": (9, 29), "subprocess-exec": (11, 45)}
EXPECT_AFTER = {"members": 88, "executed": 34,
                "git-plumbing": (2, 3), "serialization-schema": (4, 10), "file-artifact": (25, 76),
                "stdout-inspection": (10, 29), "subprocess-exec": (12, 45)}

def counts(d):
    m = d["members"]
    out = {"members": len(m), "executed": sum(1 for v in m.values() if v["status"] == "executed")}
    for c in CLASSES:
        mem = [k for k, v in m.items() if c in v["classes"]]
        out[c] = (sum(1 for k in mem if m[k]["status"] == "executed"), len(mem))
    return out

raw = open(BASE_PATH, "rb").read()
base = json.loads(raw)
# serializer round-trip: must reproduce the committed bytes exactly
ser = json.dumps(base, indent=2, ensure_ascii=False) + "\n"
rt_ok = ser.encode("utf-8") == raw
ser2 = json.dumps(base, indent=2) + "\n"
rt2_ok = ser2.encode("utf-8") == raw
print("roundtrip_indent2_ensure_ascii_false:", rt_ok, " roundtrip_indent2_default:", rt2_ok)
assert rt_ok or rt2_ok, "serializer does not reproduce BASE bytes"

before = counts(base)
print("BEFORE:", before)
for k, v in EXPECT_BEFORE.items():
    got = before[k]
    assert got == v, (k, got, v)
print("BEFORE matches measured-at-BASE figures: OK")

assert MEMBER in base["members"]
old_row = base["members"][MEMBER]
print("OLD ROW:", json.dumps(old_row, sort_keys=True))
assert old_row["status"] == "unexecuted"
assert old_row["classes"] == ROW["classes"], "class set must be unchanged"

new = copy.deepcopy(base)
new["members"][MEMBER] = copy.deepcopy(ROW)
assert list(new["members"].keys()) == list(base["members"].keys()), "member order must be preserved"
diff_members = [k for k in base["members"] if base["members"][k] != new["members"][k]]
assert diff_members == [MEMBER], diff_members
out_text = json.dumps(new, indent=2, ensure_ascii=(not rt_ok)) + "\n"
open(OUT_LEDGER, "w", encoding="utf-8").write(out_text)
flipped_raw = open(OUT_LEDGER, "rb").read()

after = counts(json.loads(flipped_raw))
print("AFTER:", after)
ok = True
for k, v in EXPECT_AFTER.items():
    good = after[k] == v
    ok = ok and good
    print(f"  {k}: got {after[k]} want {v} {'OK' if good else 'MISMATCH'}")
print("members=88 executed=34 class cells:", "ALL MATCH" if ok else "MISMATCH")
print("only_changed_member:", diff_members)
print("base_ledger_sha256:", hashlib.sha256(raw).hexdigest())
print("flipped_ledger_sha256:", hashlib.sha256(flipped_raw).hexdigest())
print("row_json:", json.dumps(ROW, sort_keys=True))
sys.exit(0 if ok else 1)
