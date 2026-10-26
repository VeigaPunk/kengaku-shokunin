"""Critic attack R40CritC1Counter (NOT a candidate battery40; development battery for the C1 counter).

The counter runs every tool with the caller's PATH (`Runner.env`), and this module's build writes a `git` shim
into a directory on that PATH — outside every fixture directory, so no fingerprint covers it, and no process has
to survive the build's pid namespace. The shim reads the tool's own program text at the one fixed variant path
(`<work>/slots/<tool>.py`, visible inside the tool's sandbox) and answers git differently for the reference and
for a mutant. Six fixtures; none of them exhibits the advertised behaviour of the mutants it kills. Source
carries no SIDECHANNEL token.
"""
raise SystemExit("NEUTRALIZED by the round-40 L1 (orchestrator host-safety ruling 2026-10-26): this attack module "
                 "wrote a git shim into the shared host PATH dir ~/.local/bin; kept as evidence text only. Re-run only "
                 "inside a sandbox with a private ~/.local/bin (bwrap --tmpfs) and SHIM_DIR under the fixture root.")

import hashlib
import pathlib
import re

SHIM_DIR = pathlib.Path("/nonexistent/neutralized-shim-dir")
CLAIMS = ".ufo/waves/round-50/claims"
ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
HEX = re.compile(r"\bsha256[ \t]+`?([0-9a-f]{64})")

SHIM = r'''#!/usr/bin/python3
import hashlib, os, subprocess, sys

REAL = "/usr/bin/git"
ROOT = "@ROOT@"
REF = @REF@
PLAN = @PLAN@
GITLINK = @GITLINK@


def phase():
    for tool, dig in REF.items():
        try:
            b = open(os.path.join(ROOT, "slots", tool + ".py"), "rb").read()
        except OSError:
            continue
        if b == b"# slot\n":
            continue
        return "ref" if hashlib.sha256(b).hexdigest() == dig else "mut"
    return "ref"


def real(argv, data=None):
    return subprocess.run([REAL] + argv, input=data, capture_output=True)


def main():
    argv = sys.argv[1:]
    repo, rest = None, list(argv)
    if "-C" in argv and argv.index("-C") + 1 < len(argv):
        i = argv.index("-C")
        repo = argv[i + 1]
        rest = argv[:i] + argv[i + 2:]
    entry = PLAN.get(repo) or {}
    spec = entry.get(phase(), "plain")
    if spec == "failtop" and "rev-parse" in rest and "--show-toplevel" in rest:
        sys.stderr.write("fatal: not a git repository (or any parent up to mount point /)\n")
        return 128
    if spec == "blobtext" and rest[:2] == ["cat-file", "blob"]:
        sys.stdout.write("P10 ok receipt unreadable\n")
        return 0
    if spec == "gitlink" and rest[:1] == ["ls-tree"]:
        r = real(argv)
        sys.stdout.buffer.write(r.stdout)
        if r.returncode == 0:
            sys.stdout.buffer.write(GITLINK.encode())
        return r.returncode
    if spec == "prov" and rest[:1] == ["ls-tree"] and rest[-1] == "corpus/evidence" and "-z" in rest:
        r = real(argv)
        sys.stdout.buffer.write(r.stdout)
        if r.returncode == 0:
            sys.stdout.buffer.write(entry["phantom"].encode() + b"\0")
        return r.returncode
    if spec == "prov" and rest[:2] == ["cat-file", "--batch"]:
        r = real(argv, sys.stdin.buffer.read())
        text = entry["ptext"]
        fake = b"b" * 40 + b" blob %d\n" % len(text) + text + b"\n"
        out = r.stdout
        for pre in (b"HEAD:", b""):
            out = out.replace(pre + entry["phantom"].encode() + b" missing\n", fake)
        sys.stdout.buffer.write(out)
        return r.returncode
    os.execv(REAL, [REAL] + argv)
    return 127


try:
    sys.exit(main())
except Exception:
    os.execv(REAL, [REAL] + sys.argv[1:])
'''

PLAN = {}


def _write_shim(root, lane):
    SHIM_DIR.mkdir(parents=True, exist_ok=True)
    ref = {t: hashlib.sha256((pathlib.Path(lane) / "plans" / f).read_bytes()).hexdigest()
           for t, f in (("anchor", "anchor_digest_check.py"),
                        ("ledger", "ledger_tip.py"), ("order", "order_check.py"))}
    text = (SHIM.replace("@ROOT@", str(root)).replace("@REF@", repr(ref))
            .replace("@PLAN@", repr(PLAN))
            .replace("@GITLINK@", repr("160000 commit " + "b" * 40 + "\t" + CLAIMS + "/zzinject\n")))
    p = SHIM_DIR / "git"
    p.write_text(text)
    p.chmod(0o755)


def _plan(ctx, d, repo, ref, mut, phantom=None, ptext=None):
    PLAN[str(repo)] = {"ref": ref, "mut": mut, "phantom": phantom or "", "ptext": ptext or b""}
    _write_shim(d.parents[2], ctx.lane)
    return ["--lane", str(repo)]


def _pick(repo):
    """A row whose anchor token is a committed capture in a dir with a sibling capture and no PROVENANCE.md."""
    text = (repo / "corpus/SOURCES.md").read_text()
    errata = set()
    for p in (repo / "corpus/lessons").rglob("*.md"):
        for m in re.finditer(r"^ {0,3}Erratum \(round 37\): (S\d{3,}) ", p.read_text(errors="replace"), re.M):
            errata.add(m.group(1))
    ev = repo / "corpus/evidence"
    files = {}
    for p in sorted(ev.rglob("*")):
        if p.is_file():
            files["corpus/evidence/" + str(p.relative_to(ev))] = hashlib.sha256(p.read_bytes()).hexdigest()
    by_dig = {}
    for p, dig in files.items():
        by_dig.setdefault(dig, p)
    for line in text.splitlines():
        m = ROW.match(line)
        if not m or m.group(1) in errata:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 11:
            continue
        for tok in HEX.findall(cells[5]):
            cap = by_dig.get(tok)
            if not cap:
                continue
            d0 = cap.rsplit("/", 1)[0]
            if (repo / d0 / "PROVENANCE.md").exists():
                continue
            sib = sorted(p for p in files if p.rsplit("/", 1)[0] == d0 and p != cap)
            if not sib or files[sib[0]] == files[cap]:
                continue
            rels = [cap.rsplit("/", 1)[1], sib[0].rsplit("/", 1)[1]]
            ptext = "".join("| %s | `%s` | capture |\n" % (m.group(1), r) for r in rels).encode()
            return m.group(1), d0 + "/PROVENANCE.md", ptext
    raise AssertionError("no row with a resolvable single capture and a sibling capture")


def anchor_defect(ctx, d):
    repo = ctx.clone(d / "lane")
    _sid, phantom, ptext = _pick(repo)
    return _plan(ctx, d, repo, "prov", "plain", phantom, ptext)


def anchor_clean(ctx, d):
    repo = ctx.clone(d / "lane")
    _sid, phantom, ptext = _pick(repo)
    return _plan(ctx, d, repo, "plain", "prov", phantom, ptext)


def anchor_upper(ctx, d):
    """A01's honest direction: one anchor cell holds an uppercase 64-hex token."""
    repo = ctx.clone(d / "lane")
    p = repo / "corpus/SOURCES.md"
    t = p.read_text()
    tok = ""
    for line in t.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 11 or not HEX.findall(cells[5]):
            continue
        for cand in HEX.findall(cells[5]):
            if t.count("sha256 " + cand) == 1:
                tok = cand
                break
        if tok:
            break
    assert tok and t.count("sha256 " + tok) == 1
    p.write_text(t.replace("sha256 " + tok, "sha256 " + tok.upper(), 1))
    return _plan(ctx, d, repo, "plain", "plain")


def _order(ctx, d, ref, mut):
    r = ctx.init(d / "repo")
    (r / "plans").mkdir()
    (r / "plans/round-50-claims.md").write_text("# frozen claims\n")
    (r / CLAIMS).mkdir(parents=True)
    (r / CLAIMS / "control.txt").write_text("P10 DEFECT receipt unreadable\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    (r / "corpus/evidence/round50").mkdir(parents=True)
    (r / "corpus/evidence/round50/probe.txt").write_text("cases=1 observed_pass=1\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    _plan(ctx, d, r, ref, mut)
    return ["--lane", str(r), "--claims", "plans/round-50-claims.md",
            "--receipt", "corpus/evidence/round50/probe.txt"]


def order_p10(ctx, d):
    return _order(ctx, d, "blobtext", "plain")


def order_gitlink(ctx, d):
    return _order(ctx, d, "plain", "gitlink")


def order_error(ctx, d):
    return _order(ctx, d, "failtop", "plain")


FIXTURES = [
    {"fid": "crit-sh-anchor-defect", "tool": "anchor", "expect": "reject",
     "defects": ["capture-unanchored"], "build": anchor_defect},
    {"fid": "crit-sh-anchor-clean", "tool": "anchor", "expect": "accept", "defects": [],
     "build": anchor_clean},
    {"fid": "crit-sh-anchor-upper", "tool": "anchor", "expect": "reject",
     "defects": ["digest-uppercase"], "build": anchor_upper},
    {"fid": "crit-sh-order-p10", "tool": "order", "expect": "reject",
     "defects": ["hit:gate-p10"], "build": order_p10},
    {"fid": "crit-sh-order-gitlink", "tool": "order", "expect": "accept", "defects": [],
     "build": order_gitlink},
    {"fid": "crit-sh-order-error", "tool": "order", "expect": "error", "defects": [],
     "build": order_error},
]
