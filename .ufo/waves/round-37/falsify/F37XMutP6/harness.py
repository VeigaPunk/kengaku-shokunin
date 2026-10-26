#!/usr/bin/env python3
"""F37XMutP6 — four NEW non-frozen mutants of gate clause P6 (c_sources), run against the full battery.

Reuses plans/round37_c1_verify.py as a module: load_r36, Ctx, r36_fixtures, battery37_fixtures,
run_gate. The fixtures are built once; the reference gate and then each new mutant run over every
fixture. A mutant is killed iff some fixture's (exit code, DEFECT clause set) differs from the
reference. It also checks whether each plans/battery37/p6.py fixture isolates the one defect its
docstring names: single-row registry diff, no other file touched, and accept once the genuine
registry is restored.
"""
import argparse
import difflib
import hashlib
import importlib.util
import pathlib
import shutil
import sys
import py_compile

# (id, clause, label, old, new) — old must occur exactly once in plans/pkg_gate.py
MUTANTS = [
    ("X1", "P6", "teaches threshold one below min_teaches_words (off-by-one)",
     'if len(cells[6].split()) < rules["min_teaches_words"]:',
     'if len(cells[6].split()) < rules["min_teaches_words"] - 1:'),
    ("X2", "P6", "row cell-count equality loosened: 11 required -> at least 11",
     "if len(cells) != 11:", "if len(cells) < 11:"),
    ("X3", "P6", "tier check runs on the first registry row only",
     '        if cells[3] != rules["row_tier"]:',
     '        if not teaches and cells[3] != rules["row_tier"]:'),
    ("X4", "P6", "url check loosened to a scheme/host-blind suffix compare",
     'url.group(0) != p.spec["raw_base"] + row["upstream"]',
     'url.group(0).split("://", 1)[-1] != (p.spec["raw_base"] + row["upstream"]).split("://", 1)[-1]'),
]


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def files_of(base):
    out = {}
    for p in pathlib.Path(base).rglob("*"):
        rel = p.relative_to(base)
        if ".git" in rel.parts or not p.is_file():
            continue
        out[str(rel)] = sha256(p)
    return out


def registry_rows(text, row_re):
    out = {}
    for line in text.splitlines():
        m = row_re.match(line)
        if m:
            out.setdefault(m.group(1), []).append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    root = pathlib.Path(a.work).resolve() / "run"
    root.mkdir(parents=True, exist_ok=True)

    r37 = load(lane / "plans/round37_c1_verify.py", "k37_counter")
    gate_src = (lane / "plans/pkg_gate.py").read_text()
    frozen = sha256(lane / "plans/pkg_gate.py") == r37.GATE_SHA256
    print(f"GATE plans/pkg_gate.py sha256={'frozen' if frozen else 'NOT-AT-FREEZE-DIGEST'} "
          f"value={sha256(lane / 'plans/pkg_gate.py')}")
    print(f"LANE {lane} battery37={sorted(p.name for p in (lane / 'plans/battery37').glob('*.py'))}")
    r36 = r37.load_r36(lane)
    ctx = r37.Ctx(lane, r36)
    fixtures = r37.r36_fixtures(r36) + r37.battery37_fixtures(lane / "plans/battery37")
    print(f"FIXTURES total={len(fixtures)} r36={sum(1 for f in fixtures if f.get('r36'))} "
          f"battery37={sum(1 for f in fixtures if not f.get('r36'))}")

    built = []
    for i, fx in enumerate(fixtures):
        d = root / "fx" / f"f{i:03d}"
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        if "--spec" in argv or not argv or argv[0] not in ("package", "d4-line", "d5-line"):
            print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
            return 2
        built.append((fx, d, argv))

    gdir = root / "gates"
    gdir.mkdir()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    ref, wrong = [], 0
    for fx, d, argv in built:
        res = r37.run_gate(ref_gate, ctx.spec_path, argv)
        ref.append(res)
        want_rc = 0 if fx["expect"] == "accept" else 1
        declared = fx.get("defects")
        if not fx.get("r36") and (declared is None or fx.get("expect") not in ("accept", "reject")):
            ok = False
        else:
            ok = res[0] == want_rc and (declared is None or res[1] == frozenset(declared))
        if fx["expect"] == "accept":
            ok = ok and not res[1]
        wrong += not ok
        print(f"FIXTURE {fx['fid']} expect={fx['expect']} "
              f"declared={','.join(sorted(fx['defects'])) if fx['defects'] else '-'} "
              f"rc={res[0]} defects={','.join(sorted(res[1])) or '-'} {'ok' if ok else 'WRONG'}")
    print(f"BATTERY fixtures={len(built)} wrong={wrong}")

    killed = 0
    for mid, clause, label, old, new in MUTANTS:
        occ = gate_src.count(old)
        state = "invalid"
        if occ == 1:
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError:
                print(f"MUTANT {mid} {clause} invalid(compile) -- {label}")
                continue
            diffs = [fx["fid"] for j, (fx, d, argv) in enumerate(built)
                     if r37.run_gate(mg, ctx.spec_path, argv) != ref[j]]
            if diffs:
                killed += 1
                print(f"MUTANT {mid} {clause} killed by={diffs[0]} "
                      f"all={','.join(diffs)} -- {label}")
            else:
                print(f"MUTANT {mid} {clause} SURVIVED -- {label}")
            print(f"  old={old!r}")
            print(f"  new={new!r} occurrences={occ}")
        else:
            print(f"MUTANT {mid} {clause} invalid -- old occurs {occ} times -- {label}")
    print(f"NEW_MUTANTS total={len(MUTANTS)} killed={killed} survived={len(MUTANTS) - killed if killed <= len(MUTANTS) else 'n/a'}")

    # ---- isolation of each p6.py fixture against its docstring -------------------------------
    p6 = load(lane / "plans/battery37/p6.py", "k37_p6")
    gen = ctx.genuine_package(root / "genuine")
    gen_files = files_of(gen)
    gen_text = (gen / "corpus/SOURCES.md").read_text()
    g = registry_rows(gen_text, p6.SOURCE_ROW)
    print(f"ISOLATION genuine_registry_rows={sorted(g)} cells="
          f"{ {k: [len(r) for r in v] for k, v in g.items()} } teaches_words="
          f"{ {k: len(v[0][6].split()) for k, v in g.items()} }")
    entry = ctx.spec["entry"]
    raw_base = ctx.spec["raw_base"]

    def same_rest(fcells, gcells, skip):
        return all(fcells[i] == gcells[i] for i in range(min(len(fcells), len(gcells))) if i not in skip)

    def claims(fid, f, fx_dir):
        c = {}
        if fid == "p6-m20-registry-row-duplicated":
            c["S105 has exactly 2 rows"] = len(f.get("S105", [])) == 2
            c["duplicate is byte-identical"] = f["S105"][0] == f["S105"][1] == g["S105"][0]
            c["S106/S107 untouched"] = all(f[k] == g[k] for k in ("S106", "S107"))
        elif fid == "p6-m21-row-with-twelve-cells":
            row = f["S106"][0]
            c["S106 has 12 cells"] = len(row) == 12
            c["cells 0-10 keep their values"] = row[:11] == g["S106"][0]
            c["extra cell is the only addition"] = row[11] != ""
            c["S105/S107 untouched"] = all(f[k] == g[k] for k in ("S105", "S107"))
        elif fid == "p6-m22-url-off-the-pinned-raw-path":
            row = f["S107"][0]
            url = str(next((t for t in row[1].split() if t.startswith("http")), ""))
            c["S107 cell1 is the only changed cell"] = same_rest(row, g["S107"][0], {1})
            c["cell1 is a real URL"] = url.startswith("https://raw.githubusercontent.com/")
            c["URL is not the pinned raw path"] = url != raw_base + ctx.spec["rows"]["S107"]["upstream"]
            c["S105/S106 untouched"] = all(f[k] == g[k] for k in ("S105", "S106"))
            print(f"  m22 url={url}")
        elif fid == "p6-m23-row-tier-b":
            row = f["S106"][0]
            c["S106 tier is B"] = row[3] == "B"
            c["genuine tier is A"] = g["S106"][0][3] == "A"
            c["cell 3 is the only changed cell"] = same_rest(row, g["S106"][0], {3})
            c["S105/S107 untouched"] = all(f[k] == g[k] for k in ("S105", "S107"))
        elif fid == "p6-m24-row-status-queued":
            row = f["S105"][0]
            c["S105 status is queued"] = row[7] == "queued"
            c["genuine status is mined"] = g["S105"][0][7] == "mined"
            c["cell 7 is the only changed cell"] = same_rest(row, g["S105"][0], {7})
            c["S106/S107 untouched"] = all(f[k] == g[k] for k in ("S106", "S107"))
        elif fid == "p6-m25-used-by-another-path":
            row = f["S107"][0]
            c["S107 used-by names the regex-log file"] = row[10] == "corpus/knowledge/tb2-regex-log-grader.md"
            c["that file is not the entry"] = row[10] != entry
            c["cell 10 is the only changed cell"] = same_rest(row, g["S107"][0], {10})
            c["S105/S106 untouched"] = all(f[k] == g[k] for k in ("S105", "S106"))
        elif fid == "p6-m26-five-word-teaches-cell":
            row = f["S105"][0]
            teaches = [f[k][0][6] for k in ("S105", "S106", "S107")]
            c["S105 teaches cell has 5 words"] = len(row[6].split()) == 5
            c["5 < min_teaches_words"] = len(row[6].split()) < ctx.spec["entry_rules"]["min_teaches_words"]
            c["cell 6 is the only changed cell"] = same_rest(row, g["S105"][0], {6})
            c["all three teaches cells stay distinct"] = len({t.lower() for t in teaches}) == 3
            c["S106/S107 untouched"] = all(f[k] == g[k] for k in ("S106", "S107"))
        elif fid == "p6-m27-two-identical-teaches-cells":
            row = f["S107"][0]
            c["S107 teaches == S106 teaches"] = row[6] == f["S106"][0][6]
            c["both are >= 8 words"] = len(row[6].split()) >= 8
            c["it differs from the genuine S107 cell"] = row[6] != g["S107"][0][6]
            c["cell 6 is the only changed cell"] = same_rest(row, g["S107"][0], {6})
            c["S105/S106 untouched"] = all(f[k] == g[k] for k in ("S105", "S106"))
        return c

    p6ids = [fx["fid"] for fx in p6.FIXTURES]
    for j, (fx, d, argv) in enumerate(built):
        if fx["fid"] not in p6ids:
            continue
        text = (d / "corpus/SOURCES.md").read_text()
        f = registry_rows(text, p6.SOURCE_ROW)
        pred_ids = {k for k in set(f) | set(g) if f.get(k) != g.get(k)}
        diff_files = sorted(k for k in set(files_of(d)) | set(gen_files)
                            if files_of(d).get(k) != gen_files.get(k))
        ud = [l for l in difflib.unified_diff(gen_text.splitlines(), text.splitlines(),
                                              "genuine/corpus/SOURCES.md", "fixture/corpus/SOURCES.md",
                                              lineterm="", n=0)
              if (l[:1] in "+-" and not l.startswith(("+++", "---")))]
        # restore the genuine registry: the tree must be accepted if the fixture isolates one defect
        iso = root / "iso" / fx["fid"]
        shutil.copytree(d, iso, symlinks=True)
        (iso / "corpus/SOURCES.md").write_text(gen_text)
        import subprocess
        subprocess.run(["git", "-C", str(iso), "add", "-A"], check=True)
        iso_argv = [t.replace(str(d), str(iso)) for t in argv]
        restored = r37.run_gate(ref_gate, ctx.spec_path, iso_argv)
        c = claims(fx["fid"], f, d)
        print(f"ISOLATION {fx['fid']} declared_defects={','.join(sorted(fx['defects']))} "
              f"observed_defects={','.join(sorted(ref[j][1]))} "
              f"diff_files={diff_files or '-'} differing_rows={sorted(pred_ids)} "
              f"source_diff_lines={len(ud)} restore_genuine_rc={restored[0]} "
              f"restore_genuine_defects={','.join(sorted(restored[1])) or '-'} "
              f"single_defect={'yes' if (diff_files == ['corpus/SOURCES.md'] and restored == (0, frozenset())) else 'NO'}")
        for line in ud:
            print(f"  diff {line}")
        for label, ok in c.items():
            print(f"  claim {'ok ' if ok else 'FAIL'} {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
