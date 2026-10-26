"""Round-43 hostile module `h6_receipt_dir` — leg i (R42CritC1Counter §1 `b-xo1-receipt-is-directory`).

Vector: `order_check.py` tests `git cat-file -e <freeze>:<receipt>` (:183), which succeeds for a TREE. A fixture whose
`--receipt` names the claims directory reaches the freeze-contains-receipt clause with no receipt artefact anywhere
in its history, so a "kill" there demonstrates nothing about receipts. Observable, on a fixture declaring `reject`:
  round-42 counter  FIXTURE h6-receipt-is-directory ... observed_rc=1 ... ok   (the substitute is admitted)
  round-43 counter  SETUP fixture 'h6-receipt-is-directory' ... --receipt ... is a tree at HEAD, not a blob
"""
CLAIMS = "plans/round-43-claims.md"
CDIR = ".ufo/waves/round-43/claims"


def build(ctx, d):
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS, "# round 43 - frozen claims\n")
    ctx.write(repo / CDIR / "note.txt", "nothing executed\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze; the receipt argument names the claims directory")
    return ["--lane", str(repo), "--claims", CLAIMS, "--receipt", CDIR]


FIXTURES = [
    {"fid": "h6-receipt-is-directory", "tool": "order", "expect": "reject", "defects": [], "build": build},
]
