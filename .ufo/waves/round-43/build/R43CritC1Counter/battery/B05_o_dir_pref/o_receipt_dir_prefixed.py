"""Round-42 substitute XO1, argv spelled with a leading './' on the receipt. Leg i compares the RAW
argv token against 'HEAD:<tok>'; the tool normalizes via resolve().relative_to(root). If git's rev
parsing handles 'HEAD:./x' differently from 'HEAD:x', the directory check may be bypassed while the
tool still sees the tree.
"""


def build_rdir_pref(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "plans/round-43-claims.md", "# claims\nclean\n")
    ctx.write(repo / "corpus/evidence/r43/claimsdir/placeholder.txt", "x")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    return ["--lane", str(repo), "--claims", "plans/round-43-claims.md",
            "--receipt", "./corpus/evidence/r43/claimsdir"]


FIXTURES = [
    {"fid": "o-receipt-dir-prefixed", "tool": "order", "expect": "reject", "defects": [],
     "build": build_rdir_pref},
]
