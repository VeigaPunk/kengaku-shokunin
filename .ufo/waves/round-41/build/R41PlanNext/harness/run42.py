"""R41PlanNext wrapper around the round-40 R40PlanNext mutant harness: per-surface detector sets and regions.
Tools: round_close | state_main | sources_lib | mutant_direction_check. Standing vs witness detector indices are
reported by the harness's `info` field (indices of detectors that differ)."""
import os, sys, json, pathlib, shutil
sys.path.insert(0, os.path.dirname(__file__))
import mut_harness as mh

SURF = sys.argv.pop(1)
S = os.path.dirname(os.path.abspath(__file__))
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
orig = mh.detectors

def reg_row(i, cells=None):
    base = ["Fixture source %d — https://example.org/%d" % (i, i), "docs", "A", "claim %d" % i,
            "anchor %d" % i, "teaches %d" % i, "mined", "2026-10-26", "2027-01-24", "corpus/knowledge/x.md"]
    c = cells if cells is not None else base
    return "| S%03d | " % i + " | ".join(c) + " |"

def mk_sources(w):
    d = pathlib.Path(w) / "src"; d.mkdir(parents=True, exist_ok=True)
    hdr = "| id | source | kind | tier | claim | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
    ok = lambda i, st="mined", rc="2027-01-24": ["Fixture source %d — https://example.org/%d" % (i, i), "docs", "A", "claim", "anchor “alpha beta gamma”", "teaches", st, "2026-10-26", rc, "corpus/knowledge/x.md"]
    def row(i, cells): return "| S%03d | " % i + " | ".join(cells) + " |"
    def row11(i, cells): return "| S%03d | " % i + " | ".join(cells) + " |"
    # 11 cells = id + 10 others
    reg = hdr + row(1, ok(1)) + "\n" + row(2, ok(2)) + "\n"
    (d / "reg.md").write_text(reg)
    (d / "pkg_clean.md").write_text(hdr + row(10, ok(10)) + "\n" + row(11, ok(11, "queued")) + "\n")
    (d / "pkg_collide.md").write_text(hdr + row(2, ok(2)) + "\n")
    (d / "pkg_indented_collide.md").write_text(hdr + "  " + row(1, ok(1)) + "\n")
    (d / "pkg_12cell.md").write_text(hdr + row(10, ok(10) + ["extra"]) + "\n")
    (d / "pkg_10cell.md").write_text(hdr + row(10, ok(10)[:-1]) + "\n")
    (d / "pkg_escpipe.md").write_text(hdr + row(10, ["Fixture \\| pipe"] + ok(10)[1:]) + "\n")
    (d / "pkg_dup.md").write_text(hdr + row(10, ok(10)) + "\n" + row(10, ok(10)) + "\n")
    (d / "pkg_badstatus.md").write_text(hdr + row(10, ok(10, "done")) + "\n")
    (d / "pkg_badrecheck.md").write_text(hdr + row(10, ok(10, "mined", "soon-ish")) + "\n")
    (d / "pkg_prose_recheck.md").write_text(hdr + row(10, ok(10, "mined", "re-check in January")) + "\n")
    (d / "pkg_usedby.md").write_text(hdr + row(10, ok(10)[:-1] + ["corpus/knowledge/ghost.md"]) + "\n" + row(11, ok(11)) + "\n")
    art = d / "art"; art.mkdir(exist_ok=True)
    (art / "doc.txt").write_text("the alpha beta gamma delta text\n")
    (d / "rows_q.txt").write_text(hdr + row(10, ok(10)) + "\n")
    long_q = "anchor “" + " ".join("w%d" % k for k in range(30)) + "”"
    (d / "rows_qlong.txt").write_text(hdr + row(10, ok(10)[:4] + [long_q] + ok(10)[5:]) + "\n")
    (d / "rows_qabsent.txt").write_text(hdr + row(10, ok(10)[:4] + ["anchor “not in artifact”"] + ok(10)[5:]) + "\n")
    (d / "map_ok.json").write_text(json.dumps({"doc.txt": "https://example.org/10"}))
    (d / "map_bad.json").write_text(json.dumps({"doc.txt": "https://example.org/99"}))
    (d / "map_empty.json").write_text("{}")
    (d / "map_broken.json").write_text("{not json")
    (d / "pkg_scope1.md").write_text(hdr + row(10, ok(10)) + "\n" + row(11, ok(11) + ["extra"]) + "\n")
    (d / "pkg_scope2.md").write_text(hdr + row(10, ok(10)) + "\n" + row(11, ok(11, "mined", "re-check in January")) + "\n")
    (d / "pkg_scope3.md").write_text(hdr + row(10, ok(10, "mined", "re-check in January")) + "\n" + row(11, ok(11)) + "\n")
    (d / "pkg_scope4.md").write_text(hdr + row(10, ok(10)) + "\n" + row(2, ok(2)) + "\n")
    (d / "pkg_noopen.md").write_text(hdr + row(10, ok(10, "queued")) + "\n")
    (d / "map_list.json").write_text("[]")
    (d / "emptyart").mkdir(exist_ok=True)
    (d / "art2").mkdir(exist_ok=True); (d / "art2" / "sub").mkdir(exist_ok=True); (d / "art2" / "sub" / "doc.txt").write_text("the alpha beta gamma delta text\n")
    (d / "map_sub.json").write_text(json.dumps({"sub/doc.txt": "https://example.org/10"}))
    (d / "map_norm.json").write_text(json.dumps({"doc.txt": "HTTPS://Example.org/10/#frag"}))
    (d / "map_noscheme.json").write_text(json.dumps({"doc.txt": "not a url"}))
    return str(d)

def sources_dets(tool, S_, lane):
    d = mk_sources(S_ + "/w"); R = d + "/reg.md"
    def chk(p, *x): return ["--registry", R, "--package", f"{d}/{p}", *x]
    dets = [["--selftest"]]
    dets += [chk("pkg_clean.md"), chk("pkg_collide.md"), chk("pkg_indented_collide.md"), chk("pkg_12cell.md"),
             chk("pkg_10cell.md"), chk("pkg_escpipe.md"), chk("pkg_dup.md"), chk("pkg_badstatus.md"),
             chk("pkg_badrecheck.md"), chk("pkg_prose_recheck.md", "--admit-ids", "S010", "--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md"),
             chk("pkg_clean.md", "--admit-ids", "S010,S011", "--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md", "--recheck", "90d"),
             chk("pkg_clean.md", "--admit-ids", "S010", "--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md", "--recheck", "never", "--attest-opened"),
             chk("pkg_clean.md", "--admit-ids", "S010", "--scope-to-admit", "--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md", "--out", d + "/out.txt"),
             chk("pkg_usedby.md", "--admit-ids", "S010", "--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md", "--recheck", "30d"),
             chk("pkg_12cell.md", "--scope-to-admit", "--admit-ids", "S011", "--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md"),
             chk("pkg_clean.md", "--admit-ids", "S099", "--access-date", "2026-10-26", "--entries", "e"),
             chk("pkg_collide.md", "--scope-to-admit", "--admit-ids", "S002", "--access-date", "2026-10-26", "--entries", "e")]
    for q in ("rows_q.txt", "rows_qlong.txt", "rows_qabsent.txt"):
        dets.append(["--quote-file", f"{d}/{q}", "--artifact", f"{d}/art"])
        dets.append(["--quote-file", f"{d}/{q}", "--artifact", f"{d}/art/doc.txt", "--url-map", f"{d}/map_ok.json"])
    for m in ("map_bad.json", "map_empty.json", "map_broken.json"):
        dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/art", "--url-map", f"{d}/{m}"])
    A=["--access-date", "2026-10-26", "--entries", "e"]
    for pk, ids in (("pkg_scope1.md","S010"),("pkg_scope2.md","S010"),("pkg_scope3.md","S010"),("pkg_scope4.md","S010"),("pkg_scope3.md","S011"),("pkg_noopen.md","S010")):
        dets.append(chk(pk, "--scope-to-admit", "--admit-ids", ids, *A)); dets.append(chk(pk, "--admit-ids", ids, *A))
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/emptyart"])
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/nonexistent"])
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/art", "--url-map", f"{d}/map_list.json"])
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/art2", "--url-map", f"{d}/map_sub.json"])
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/art2"])
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/art", "--url-map", f"{d}/map_norm.json"])
    dets.append(["--quote-file", f"{d}/rows_q.txt", "--artifact", f"{d}/art", "--url-map", f"{d}/map_noscheme.json"])
    return dets

def rc_dets(tool, S_, lane):
    L = lane; C = CENSUS
    return [["--lane", L, "--census", C, "--selftest"],            # 0 standing
            ["--lane", L, "--round", "40", "--census", C],                              # 1 live gate
            ["--lane", L, "--round", "41", "--census", C],
            ["--lane", L, "--round", "39", "--census", C],
            ["--lane", L, "--round", "99", "--census", C],
            ["--lane", L, "--census", C],
            ["--lane", L, "--round", "40", "--census", "/nonexistent/c.sh"],
            ["--lane", L + "/plans", "--round", "40", "--census", C],
            ["--lane", S_ + "/w", "--round", "40", "--census", C]]

def sc_dets(tool, S_, lane):
    w = S_ + "/w"; emp = pathlib.Path(w) / "emp"; emp.mkdir(parents=True, exist_ok=True)
    ef = pathlib.Path(w) / "emptyfiles"; (ef / "corpus").mkdir(parents=True, exist_ok=True)
    for n in ("SCORECARD.md", "SHONEN.md", "PROVINCE.md", "corpus/README.md"): (ef / n).write_text("")
    fl = pathlib.Path(w) / "afile.txt"; fl.write_text("x")
    return [["--selftest"], ["--root", "@ROOT@", "--summary"],                           # 0,1 standing
            ["--root", w + "/nonexistent", "--summary"], ["--root", str(fl), "--summary"],
            ["--root", str(emp), "--summary"], ["--root", str(ef), "--summary"],
            ["--root", "@ROOT@", "--json"], ["--root", "@ROOT@"]]

if SURF == "round_close":
    tool = "round_close"; mh.EXCLUDE[tool] = []; mh.detectors = rc_dets
elif SURF == "state_main":
    tool = "state_check"; mh.EXCLUDE[tool] = [(1, 4648), (4707, 99999)]; mh.detectors = sc_dets
elif SURF == "sources_lib":
    tool = "sources_adopt"; mh.EXCLUDE[tool] = [(610, 1083)]; mh.detectors = sources_dets
elif SURF == "mdc":
    tool = "mutant_direction_check"; mh.EXCLUDE[tool] = []
sys.argv += ["--tool", tool]
mh.main()
