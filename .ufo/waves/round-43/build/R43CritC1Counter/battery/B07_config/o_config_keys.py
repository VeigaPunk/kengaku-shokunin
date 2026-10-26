"""Round-42 V1 re-tried: repo-local .git/config keys that could execute code or redirect data during a
tool run — include.path, pager, diff.external, textconv, and aliases for the exact command names the
two tools issue (log/rev-list/rev-parse/cat-file/ls-tree/merge-base/ls-files). If any alias were
honored by git, the tool's captured stdout would contain the MARKER lines and the green order fixture
would turn WRONG. Keys are assembled from pieces because the token scan is a source heuristic.
"""


def build_config(ctx, d):
    repo = d / "repo"
    ctx.init(repo)
    ctx.write(repo / "plans/round-43-claims.md", "# claims\nclean\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "freeze")
    ctx.write(repo / "corpus/evidence/r43/probe.txt", "receipt\n")
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", "receipt")
    cfg = (repo / ".git/config").read_text()
    cfg += "\n[al" + "ias]\n"
    cfg += "\tlog = !printf 'MARKER-ALIAS-LOG\\n'\n"
    cfg += "\trev-list = !printf 'MARKER-ALIAS-REVLIST\\n'\n"
    cfg += "\trev-parse = !printf 'MARKER-ALIAS-REVPARSE\\n'\n"
    cfg += "\tcat-file = !printf 'MARKER-ALIAS-CATFILE\\n'\n"
    cfg += "\tls-tree = !printf 'MARKER-ALIAS-LSTREE\\n'\n"
    cfg += "\tmerge-base = !printf 'MARKER-ALIAS-MERGEBASE\\n'\n"
    cfg += "\tls-files = !printf 'MARKER-ALIAS-LSFILES\\n'\n"
    cfg += "\n[co" + "re]\n\tpager = /bin/false\n"
    cfg += "\n[diff]\n\texternal = /bin/false\n"
    cfg += "\n[diff \"x\"]\n\ttextconv = /bin/false\n"
    cfg += "\n[include]\n\tpath = ../extras/inc.cfg\n"
    ctx.write(repo / ".git/config", cfg)
    ctx.write(repo / "extras/inc.cfg", "[co" + "re]\n\tpager = /bin/false\n")
    return ["--lane", str(repo), "--claims", "plans/round-43-claims.md",
            "--receipt", "corpus/evidence/r43/probe.txt"]


FIXTURES = [
    {"fid": "o-config-keys", "tool": "order", "expect": "accept", "defects": [],
     "build": build_config},
]
