"""Draft control `d6orderdir` (seat R44MutC1Guards) — order_argv_breach (round-43 leg i) red control.

An order fixture whose `--receipt` names a DIRECTORY that exists at HEAD (a tree, not a blob):
  pristine counter  -> `SETUP ... escapes its directory: --receipt corpus/evidence/round7/x is a tree at HEAD, not a blob` (exit 2)
  M06 counter (if got[0] == 0 and got[1] != "blob": -> if False:) -> the fixture is admitted.
"""


def build(ctx, d):
    r = ctx.init(d / "lane")
    ctx.write(r / "plans/round-7-claims.md", "# claims\n")
    ctx.write(r / "corpus/evidence/round7/x/inner.txt", "receipt content\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    ctx.write(r / "corpus/evidence/round7/receipt.txt", "CASE c1 observed=PASS\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    return ["--lane", str(r), "--claims", "plans/round-7-claims.md",
            "--receipt", "corpus/evidence/round7/x"]


FIXTURES = [{"fid": "d6-receipt-is-directory", "tool": "order", "expect": "error", "defects": [], "build": build}]
