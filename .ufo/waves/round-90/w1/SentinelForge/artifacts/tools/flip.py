import json, sys
# usage: flip.py <ledger-path> <receipt-path-in-repo>   (flips merge-diff row to executed, keeps byte format)
path, receipt = sys.argv[1], sys.argv[2]
text = open(path).read()
doc = json.loads(text)
doc["members"]["merge-diff-arc-agi-task"] = {
    "classes": ["file-artifact", "git-plumbing", "serialization-schema", "stdout-inspection", "subprocess-exec"],
    "receipt": receipt, "round": 90, "status": "executed", "subject": "tb2-header", "verdict": "cases"}
open(path, "w").write(json.dumps(doc, indent=2) + "\n")
