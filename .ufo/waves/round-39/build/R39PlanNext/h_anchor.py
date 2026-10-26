#!/usr/bin/env python3
"""R39PlanNext harness: mutants of plans/anchor_digest_check.py (post-D3) vs fixture detectors."""
import json, os, pathlib, re, shutil, subprocess, sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r39/R39PlanNext")
BASE = S / "lane"
TAG = os.environ.get("TAG", "")
FX = S / ("fx_anchor" + TAG)
MUT = S / ("mut_anchor" + TAG)
TOOL = pathlib.Path(os.environ.get("TOOL") or (BASE / "plans/anchor_digest_check.py"))
SRC = TOOL.read_text()

S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S112 = "1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05"
S070 = "45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd"
S073 = "97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2"
S113 = "62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97"
S114 = "c217d37253c89a71d6cc4d1c14f588c02ce49039cb1118dd3694150cf4c64193"
URL111 = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
          "2fd12b88aafdd04a52c298e3940bcb189f9766d6/configure-git-webserver/tests/test_outputs.py")


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True)


def clone(name):
    d = FX / name
    if d.exists():
        shutil.rmtree(d)
    r = sh("git", "clone", "-q", "--shared", str(BASE), str(d))
    assert r.returncode == 0, r.stderr
    return d


def edit(d, rel, old, new, count=1):
    p = d / rel
    t = p.read_text()
    assert t.count(old) == count, (rel, old[:60], t.count(old))
    p.write_text(t.replace(old, new, 1))


def row_edit(d, sid, fn):
    p = d / "corpus/SOURCES.md"
    lines = p.read_text().split("\n")
    for i, l in enumerate(lines):
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % sid, l):
            lines[i] = fn(l)
            break
    else:
        raise AssertionError(sid)
    p.write_text("\n".join(lines))


SO, LE = "corpus/SOURCES.md", "corpus/lessons/round-37.md"
FIXT = []  # (id, builder(d)->extra argv, group)


def fx(fid, group):
    def deco(f):
        FIXT.append((fid, f, group))
        return f
    return deco


@fx("F00-tip", "tip")
def _(d): return []

# ---- the twelve round-38 fixtures (run_fixtures.py needles) ----
@fx("M4b", "r38")
def _(d): edit(d, SO, S111, S111 + "; sha256 " + S108); return []
@fx("M5", "r38")
def _(d): edit(d, SO, "sha256 " + S111, "sha256 " + S108); return []
@fx("M6", "r38")
def _(d): edit(d, SO, "sha256 " + S111, "sha256 " + S112); return []
@fx("M7", "r38")
def _(d): edit(d, SO, "sha256 `" + S070, "sha256 `" + S073); return []
@fx("M8", "r38")
def _(d): edit(d, SO, "sha256 " + S111, "sha256 " + "dead00beef" * 6 + "dead"); return []
@fx("M9", "r38")
def _(d): edit(d, SO, "sha256 " + S114, "sha256 " + S113); return []
@fx("M11", "r38")
def _(d):
    edit(d, LE, "Erratum (round 37): S110 anchor sha256",
         "Erratum (round 37): S111 anchor sha256 " + S108 + " corrected-by " + S108
         + "\nErratum (round 37): S110 anchor sha256"); return []
@fx("R1", "r38")
def _(d): edit(d, LE, "Erratum (round 37): S110 anchor sha256", "Erratum withdrawn: S110 anchor sha256"); return []
@fx("R2", "r38")
def _(d):
    e = "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"
    edit(d, LE, e, e[:-1] + "d"); return []
@fx("R3", "r38")
def _(d): edit(d, SO, "sha256 " + S108, "sha256 " + S108[:-1]); return []
@fx("M10", "r38")
def _(d): edit(d, SO, URL111, "(pinned at 2fd12b88, task configure-git-webserver, tests/test_outputs.py)"); return []
@fx("M12", "r38")
def _(d):
    edit(d, SO, "corpus/evidence/round37/prior-art/tb21-issue-133-body.md", "corpus/evidence/round37/prior-art"); return []

# ---- candidate round-40 fixtures (token-shape, row-shape, mode, usage) ----
@fx("X01-upper", "new")
def _(d): edit(d, SO, "sha256 " + S111, "sha256 " + S111.upper()); return []
@fx("X02-abbrev-wrongprefix", "new")
def _(d): edit(d, SO, "sha256 afaae9dd…", "sha256 afaae9de…"); return []
@fx("X03-abbrev-7hex", "new")
def _(d): edit(d, SO, "sha256 afaae9dd…", "sha256 afaae9d…"); return []
@fx("X04-abbrev-upper", "new")
def _(d): edit(d, SO, "sha256 afaae9dd…", "sha256 AFAAE9DD…"); return []
@fx("X05-abbrev-64hex-ellipsis", "new")
def _(d):
    e = "afaae9dd"
    # a 64-hex prefix is not an abbreviation (8-63 only)
    import hashlib
    h = hashlib.sha256((d / "corpus/evidence/attrib-r23-stream.log").read_bytes()).hexdigest()
    edit(d, SO, "sha256 afaae9dd…", "sha256 " + h + "…"); return []
@fx("X06-token-in-teaches", "new")
def _(d):
    def f(l):
        cells = l.split("|")
        # cells[0]='' ; anchor index 5 -> cells[6]; teaches -> cells[7]
        t = re.search(r"sha256 ([0-9a-f]{64})", cells[6]).group(0)
        cells[6] = cells[6].replace("; " + t, "").replace(t, "")
        cells[7] = cells[7].rstrip() + " " + t + " "
        return "|".join(cells)
    row_edit(d, "S111", f); return []
@fx("X07-12-cells", "new")
def _(d): row_edit(d, "S111", lambda l: l.rstrip().rstrip("|") + "| extra |"); return []
@fx("X08-indent3-wrong", "new")
def _(d):
    edit(d, SO, "sha256 " + S111, "sha256 " + S108)
    row_edit(d, "S111", lambda l: "   " + l); return []
@fx("X09-indent4-wrong", "new")
def _(d):
    edit(d, SO, "sha256 " + S111, "sha256 " + S108)
    row_edit(d, "S111", lambda l: "    " + l); return []
@fx("X10-second-url (R5 shape)", "new")
def _(d):
    edit(d, SO, "sha256 " + S111, "sha256 " + S108)
    row_edit(d, "S111", lambda l: l.rstrip().rstrip("|") + "| https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py |"
             if False else l.replace(" | code | A |", " | code | A |", 1))
    # add the second URL inside the source cell (cell index 1)
    def f(l):
        cells = l.split("|")
        cells[2] = cells[2].rstrip() + " https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py "
        return "|".join(cells)
    row_edit(d, "S111", f); return []
@fx("X11-token-removed", "new")
def _(d): edit(d, SO, "sha256 " + S111, "no digest claim"); return []
@fx("X12-erratum-unresolved-hex", "new")
def _(d):
    edit(d, LE, "Erratum (round 37): S110 anchor sha256",
         "Erratum (round 37): S110 anchor sha256 " + "ab" * 32 + " [bogus extra token]\nErratum (round 37): S110 anchor sha256"); return []
@fx("X13-erratum-4space-indent", "new")
def _(d):
    edit(d, LE, "Erratum (round 37): S110 anchor sha256", "    Erratum (round 37): S110 anchor sha256"); return []
@fx("X14-erratum-incomplete", "new")
def _(d):
    e = "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"
    edit(d, LE, "is 63 hex digits (the", "is 63 hex digits (the", 1)
    # drop the correction digest from the erratum line only (first occurrence is the "wrong" token after S110: lines carry wrong+right)
    p = d / LE
    t = p.read_text().split("\n")
    for i, l in enumerate(t):
        if l.startswith("Erratum (round 37): S110 anchor sha256"):
            t[i] = l.replace("the capture's digest is sha256 " + e, "the capture's digest is lost")
            break
    p.write_text("\n".join(t)); return []


def stage_capture(d, name="roundX/tb2-newtask", digest_ok=True, extra_toml=None):
    cap = d / "corpus/evidence" / name
    cap.mkdir(parents=True, exist_ok=True)
    (cap / "test_outputs.py").write_text("assert True  # r39 planning capture\n")
    import hashlib
    h = hashlib.sha256((cap / "test_outputs.py").read_bytes()).hexdigest()
    (cap / "SHA256SUMS").write_text(f"{h}  test_outputs.py\n")
    (cap / "task.toml").write_text('name = "harbor/new-task-r39"\n' if extra_toml is None else extra_toml)
    sh("git", "add", "-A", "corpus/evidence", cwd=d)
    return h


def add_row(d, sid, url_task, h):
    row = ("| %s | Terminal-Bench 2.0 new-task grader — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
           "2fd12b88aafdd04a52c298e3940bcb189f9766d6/%s/tests/test_outputs.py | code | A | scope | commit 2fd12b88, "
           "sha256 %s | teaches | mined | 2026-10-26 | 180d | corpus/knowledge/x.md |" % (sid, url_task, h))
    p = d / SO
    t = p.read_text().rstrip("\n").split("\n")
    # insert after S111 row
    for i, l in enumerate(t):
        if l.startswith("| S111 "):
            t.insert(i + 1, row)
            break
    p.write_text("\n".join(t) + "\n")


@fx("X15-index-staged-capture (index mode)", "new")
def _(d):
    h = stage_capture(d); add_row(d, "S900", "new-task-r39", h)
    return ["--evidence-ref", "index"]
@fx("X16-staged-capture-head-mode", "new")
def _(d):
    h = stage_capture(d); add_row(d, "S900", "new-task-r39", h)
    return []
@fx("X17-duplicate-task-slug (index mode)", "new")
def _(d):
    h = stage_capture(d, "roundX/tb2-dup1", extra_toml='name = "harbor/configure-git-webserver"\n')
    (d / "corpus/evidence/roundX/tb2-dup1/test_outputs.py").write_text("x\n")
    sh("git", "add", "-A", "corpus/evidence", cwd=d)
    return ["--evidence-ref", "index"]
@fx("X18-usage-no-sources", "new")
def _(d):
    (d / "corpus/SOURCES.md").unlink(); return []
@fx("X19-usage-no-evidence", "new")
def _(d):
    sh("git", "rm", "-q", "-r", "--cached", "corpus/evidence", cwd=d); return []


@fx("X20-stale-manifest-digest (index mode)", "new")
def _(d):
    import hashlib
    h = stage_capture(d)
    cap = d / "corpus/evidence/roundX/tb2-newtask"
    mdig = hashlib.sha256(b"some other bytes").hexdigest()
    (cap / "SHA256SUMS").write_text(f"{mdig}  test_outputs.py\n")
    sh("git", "add", "-A", "corpus/evidence", cwd=d)
    add_row(d, "S900", "new-task-r39", mdig)
    return ["--evidence-ref", "index"]
@fx("X21-uppercase-manifest-entry (index mode)", "new")
def _(d):
    import hashlib
    h = stage_capture(d)
    cap = d / "corpus/evidence/roundX/tb2-newtask"
    mdig = hashlib.sha256(b"some other bytes").hexdigest()
    (cap / "SHA256SUMS").write_text(f"{mdig.upper()}  test_outputs.py\n")
    sh("git", "add", "-A", "corpus/evidence", cwd=d)
    add_row(d, "S900", "new-task-r39", mdig)
    return ["--evidence-ref", "index"]
@fx("X22-abbrev-substring-not-prefix", "new")
def _(d):
    import hashlib
    h = hashlib.sha256((d / "corpus/evidence/attrib-r23-stream.log").read_bytes()).hexdigest()
    edit(d, SO, "sha256 afaae9dd…", "sha256 " + h[2:10] + "…"); return []


def run_tool(tool, d, extra):
    # evidence-ref index reads the index; head reads HEAD. Both are read from d.
    r = subprocess.run([sys.executable, str(tool), "--lane", str(d)] + extra, capture_output=True, text=True, cwd=d,
                       env=dict(os.environ, TMPDIR=str(S)))
    out = r.stdout.splitlines()
    classes = sorted(re.findall(r"class=(\S+)", r.stdout))
    last = out[-1] if out else ""
    err = (r.stderr.splitlines() or [""])[0][:120]
    return {"rc": r.returncode, "classes": classes, "last": last, "err": err, "full": r.stdout}


MUTANTS = []
def mut(mid, old, new, target, note=""):
    MUTANTS.append((mid, old, new, target, note))


mut("A01", 'HEX64 = re.compile(r"[0-9a-f]{64}")', 'HEX64 = re.compile(r"[0-9a-fA-F]{64}")', "digest-uppercase", "uppercase accepted by strict test")
mut("A02", "if not (8 <= len(tok) <= 63 and tok == tok.lower()):", "if not (1 <= len(tok) <= 63 and tok == tok.lower()):", "abbrev-unresolved", "abbrev floor 8 -> 1")
mut("A03", "if not (8 <= len(tok) <= 63 and tok == tok.lower()):", "if not (8 <= len(tok) <= 64 and tok == tok.lower()):", "abbrev-unresolved", "abbrev ceiling 63 -> 64")
mut("A04", "if not (8 <= len(tok) <= 63 and tok == tok.lower()):", "if not (8 <= len(tok) <= 63):", "abbrev-unresolved", "abbrev lowercase rule dropped")
mut("A05", 'elif not any(d.startswith(tok) for d in row_scope):', 'elif False:', "abbrev-unresolved", "abbrev prefix match unchecked")
mut("A06", 'ROW = re.compile(r"^ {0,3}\\|\\s*(S\\d{3,})\\s*\\|")', 'ROW = re.compile(r"^ {0,4}\\|\\s*(S\\d{3,})\\s*\\|")', "row-shape", "row indent 3 -> 4")
mut("A07", 'ROW = re.compile(r"^ {0,3}\\|\\s*(S\\d{3,})\\s*\\|")', 'ROW = re.compile(r"^ {0,2}\\|\\s*(S\\d{3,})\\s*\\|")', "row-shape", "row indent 3 -> 2")
mut("A08", "if cell_idx != ANCHOR_CELL:", "if False:", "token-outside-anchor", "outside-anchor rule off")
mut("A09", 'if len(r["cells"]) != NCELLS:', 'if len(r["cells"]) < NCELLS:', "row-malformed", "12-cell rows accepted")
mut("A10", "if not row_scope:", "if row_scope is None:", "anchor-unbound", "empty-binding rows not flagged unbound")
mut("A11", "            elif tok not in row_scope:\n                if tok in allowed:", "            elif tok not in row_scope:\n                if False:", "digest-wrong-capture", "wrong-capture relabelled digest-unknown")
mut("A12", "            if ex:\n                continue\n", "            if ex and False:\n                continue\n", "erratum", "erratum exemption off")
mut("A13", "and (t in row_scope if row_scope is not None else t in allowed)]", "and t in allowed]", "erratum-incomplete", "erratum laundering via global A")
mut("A14", "if HEX64_ANY.fullmatch(t) and t not in allowed and t not in cited_wrong:", "if False:", "erratum-digest-unresolved", "erratum unresolved-hex check off")
mut("A15", "        if len(owners) != 1:\n            continue  # ambiguous", "        if len(owners) < 1:\n            continue  # ambiguous", "anchor-unbound", "ambiguous task slug binds first owner")
mut("A16", "hits = [c for c in comps[:-1] if c in slugs]", "hits = [c for c in comps if c in slugs]", "url-task", "task component may be the file basename")
mut("A17", 'return (":" if ref == "index" else "HEAD:") + path', 'return (":" if ref == "head" else "HEAD:") + path', "evidence-ref", "head/index modes swapped")
mut("A18", "ntokens += len(r[\"rtoks\"])", "ntokens += len(r[\"atoks\"])", "summary", "tokens= counts anchor tokens only")
mut("A19", "return 0 if not defects else 1", "return 0", "exit", "defects never reach the exit code")
mut("A20", "    except Usage as e:\n        print(f\"USAGE: {e}\", file=sys.stderr)\n        return 2", "    except Usage as e:\n        print(f\"USAGE: {e}\", file=sys.stderr)\n        return 1", "exit", "usage exit 2 -> 1")
mut("A21", 'dig = m.group(1).lower()', 'dig = m.group(1)', "manifest-case", "manifest digest case not folded")
mut("A22", "if (d, base) in idx[\"dir_entries\"]:\n        got.setdefault(idx[\"dir_entries\"][(d, base)], f\"{d}/SHA256SUMS:{base}\")", "if False:\n        pass", "manifest-view", "manifest view of a capture ignored")
mut("A23", "        if base == \"task.toml\":", "        if False:", "slug", "task.toml slug binding off")
mut("A24", "elif not any(d.startswith(tok) for d in row_scope):", "elif not any(tok in d for d in row_scope):", "abbrev-unresolved", "prefix match -> substring match")
mut("A25", 'ERRATUM = re.compile(r"^ {0,3}Erratum \\(round 37\\): (S\\d{3,}) anchor sha256\\b")', 'ERRATUM = re.compile(r"^ *Erratum \\(round 37\\): (S\\d{3,}) anchor sha256\\b")', "erratum-shape", "erratum indent unbounded")
mut("A26", "if not row_scope:\n                defects.append(f\"DEFECT {sid} anchor token={tok} class=anchor-unbound \"", "if not row_scope and False:\n                defects.append(f\"DEFECT {sid} anchor token={tok} class=anchor-unbound \"", "anchor-unbound", "unbound rows silently pass through to digest tests")


def main():
    FX.mkdir(exist_ok=True)
    MUT.mkdir(exist_ok=True)
    extras = {}
    for fid, b, g in FIXT:
        d = clone(fid.split(" ")[0])
        extras[fid] = (d, b(d))
    ref = {fid: run_tool(TOOL, d, ex) for fid, (d, ex) in extras.items()}
    print("== pristine verdicts ==")
    for fid, r in ref.items():
        print(f"{fid:42s} rc={r['rc']} classes={r['classes']} last={r['last']} err={r['err']}")
    res = []
    for mid, old, new, target, note in MUTANTS:
        if SRC.count(old) != 1:
            print(f"{mid}: SETUP needle count {SRC.count(old)}")
            res.append((mid, target, note, None))
            continue
        mp = MUT / f"{mid}.py"
        mp.write_text(SRC.replace(old, new, 1))
        kills = []
        for fid, (d, ex) in extras.items():
            r = run_tool(mp, d, ex)
            q = ref[fid]
            if (r["rc"], r["classes"], r["last"], r["err"]) != (q["rc"], q["classes"], q["last"], q["err"]):
                kills.append((fid, "rc" if r["rc"] != q["rc"] else ("class" if r["classes"] != q["classes"] else "text")))
        res.append((mid, target, note, kills))
    print("\n== mutants ==")
    tot = {"tip": 0, "tip+r38": 0, "all": 0, "attributed": 0}
    n = 0
    groups = {fid: g for fid, _, g in FIXT}
    for mid, target, note, kills in res:
        if kills is None:
            continue
        n += 1
        kt = [f for f, _ in kills if groups[f] == "tip"]
        k38 = [f for f, _ in kills if groups[f] in ("tip", "r38")]
        tot["tip"] += bool(kt); tot["tip+r38"] += bool(k38); tot["all"] += bool(kills)
        print(f"{mid} target={target:24s} tip={'K' if kt else '-'} r38={'K' if k38 else '-'} all={'K' if kills else '-'}  {note}  killers={[f'{f}:{k}' for f,k in kills][:6]}")
    print(f"MUTANTS n={n} killed_by_tip={tot['tip']} killed_by_tip+r38_fixtures={tot['tip+r38']} killed_by_all_fixtures={tot['all']}")


if __name__ == "__main__":
    main()
