"""R42PlanNext witness fixtures (cheap, NOT a frozen battery): extra shapes for the unpriced advertised rows of
plans/tip_receipts.py and plans/sources_adopt.py. FIXTURES_TR / FIXTURES_SA: {fid, build(ctx,d)->argv, [env], [post], [cwd]}.
Tokens in argv/env: {WORK} {WORK:name} (run scratch), @D@ (this run's copy of the fixture dir)."""
import json

DOCS = {"README.md": "# fixture lane\n\n`plans/foo_probe.py` re-run; receipt foo-probe.txt\n", "SKILL.md": "# skill\n",
        "corpus/README.md": "# evidence\n"}


def probe(name, body="", runas=None, doc=True):
    ra = runas if runas is not None else f"python3 plans/{name}.py --lane ."
    return (f'"""Stub probe {name}.\n\n  {ra}\n"""\nimport sys\n{body}\n' if doc else f"import sys\n{body}\n")


def out(text):
    return f"sys.stdout.write({text!r})\n"


def lane(ctx, d, files, sub="lane"):
    root = ctx.init(d / sub)
    base = dict(DOCS); base.update(files)
    for rel in sorted(base):
        ctx.write(root / rel, base[rel])
    ctx.git(root, "add", "-A"); ctx.git(root, "commit", "-q", "-m", "fixture lane")
    return root


def rcpt(i, name="p"):
    return f"corpus/evidence/r{i}/{name}-probe.txt"


def two(ctx, d):
    return lane(ctx, d, {"plans/a_probe.py": probe("a_probe", out("A\n")), "plans/b_probe.py": probe("b_probe", out("B\n")),
                         "corpus/evidence/r/a-probe.txt": "A\n", "corpus/evidence/r/b-probe.txt": "B\n"})


def b_only(ctx, d):
    return ["--lane", str(two(ctx, d)), "--work", "{WORK}", "--only", "a-probe"]


def b_only_none(ctx, d):
    return ["--lane", str(two(ctx, d)), "--work", "{WORK}", "--only", "zzz"]


RV = ("import os,time\nopen('rv-%s','w').write('x')\nt=time.time()\n"
      "while not os.path.exists('rv-%s') and time.time()-t<3: time.sleep(0.05)\n"
      "sys.stdout.write('met\\n' if os.path.exists('rv-%s') else 'alone\\n')\n")


def b_rendezvous(ctx, d):
    r = lane(ctx, d, {"plans/a_probe.py": probe("a_probe", RV % ("a", "b", "b")),
                      "plans/b_probe.py": probe("b_probe", RV % ("b", "a", "a")),
                      "corpus/evidence/r/a-probe.txt": "met\n", "corpus/evidence/r/b-probe.txt": "met\n"})
    return ["--lane", str(r), "--work", "{WORK}", "--jobs", "2"]


TMPB = ("import os,pathlib\nt=os.environ\nsys.stdout.write('same %s\\n' % (t['TMPDIR']==t['TEMP']==t['TMP']))\n"
        "sys.stdout.write('under-ws %s\\n' % any(p.startswith('tip-receipts-') for p in pathlib.Path(t['TMPDIR']).parts))\n"
        "sys.stdout.write('wp %s\\n' % pathlib.Path(os.getcwd()).parent.parent.name)\n"
        "sys.stdout.write('cwd %s alt %s\\n' % (pathlib.Path(os.getcwd()).name, os.path.exists('.git/objects/info/alternates')))\n")
TMPOUT = "same True\nunder-ws True\nwp wp\ncwd tip alt True\n"


def tmplane(ctx, d):
    return lane(ctx, d, {"plans/t_probe.py": probe("t_probe", TMPB), "corpus/evidence/r/t-probe.txt": TMPOUT})


def b_work(ctx, d):
    return ["--lane", str(tmplane(ctx, d)), "--work", "{WORK:wp}"]


def b_env_tmp(ctx, d):
    return ["--lane", str(tmplane(ctx, d))]


def b_work_and_env(ctx, d):
    return ["--lane", str(tmplane(ctx, d)), "--work", "{WORK:wp}"]


def b_runas_args(ctx, d):
    r = lane(ctx, d, {"plans/arg_probe.py": probe("arg_probe", "sys.stdout.write(repr(sys.argv[1:]) + '\\n')",
                                                    runas="python3 plans/arg_probe.py --mode full  prose after"),
                      "corpus/evidence/r/arg-probe.txt": "['--mode', 'full', '--lane', '.']\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_no_runas(ctx, d):
    r = lane(ctx, d, {"plans/nr_probe.py": probe("nr_probe", out("N\n"), doc=False), "corpus/evidence/r/nr-probe.txt": "N\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_runas_uvish(ctx, d):
    r = lane(ctx, d, {"plans/u_probe.py": probe("u_probe", out("U\n"), runas="uv run --no-project python3 plans/u_probe.py"),
                      "corpus/evidence/r/u-probe.txt": "U\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_firstdiff_byte(ctx, d):
    r = lane(ctx, d, {"plans/d_probe.py": probe("d_probe", out("aaaa\nbbbb\n")), "corpus/evidence/r/d-probe.txt": "aaaa\nbbbX\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_firstdiff_len(ctx, d):
    r = lane(ctx, d, {"plans/d_probe.py": probe("d_probe", out("abc\nd\n")), "corpus/evidence/r/d-probe.txt": "abc\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_script_absent(ctx, d):
    r = lane(ctx, d, {"corpus/evidence/round36/regex-log-probe.txt": "X\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_temp_differ(ctx, d):
    r = lane(ctx, d, {"plans/regex_log_probe.py": probe("regex_log_probe", out("p /tmp/tmpAAAAAAAA q\nTAIL1\n")),
                      "corpus/evidence/round36/regex-log-probe-first-run.txt": "p /tmp/tmpBBBBBBBB q\nTAIL2\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def three(ctx, d):
    return lane(ctx, d, {"plans/a_probe.py": probe("a_probe", out("AAAAAAAAAAAA\n")),
                         "plans/b_probe.py": probe("b_probe", out("BB\n")), "plans/c_probe.py": probe("c_probe", out("CCCCCC\n")),
                         "corpus/evidence/r/a-probe.txt": "AAAAAAAAAAAA\n", "corpus/evidence/r/b-probe.txt": "BB\n",
                         "corpus/evidence/r/c-probe.txt": "CCCCCC\n"})


E = "corpus/evidence/r/"


def b_tamper_comma(ctx, d):
    return ["--lane", str(three(ctx, d)), "--work", "{WORK}", "--tamper", E + "a-probe.txt," + E + "c-probe.txt"]


def b_tamper_twice(ctx, d):
    return ["--lane", str(three(ctx, d)), "--work", "{WORK}", "--tamper", E + "a-probe.txt", "--tamper", E + "b-probe.txt"]


def b_auto_control(ctx, d):
    return ["--lane", str(three(ctx, d)), "--work", "{WORK}"]


def b_post(ctx, d):
    return ["--lane", str(two(ctx, d)), "--work", "{WORK:wp}"]


def b_clonefail(ctx, d):
    r = lane(ctx, d, {"plans/a_probe.py": probe("a_probe", out("A\n")), "corpus/evidence/r/a-probe.txt": "A\n"})
    lst = ctx.sh("git", "-C", str(r), "cat-file", "--batch-all-objects", "--batch-check").stdout.splitlines()
    for line in lst:
        oid, typ, _ = line.split()
        if typ == "blob":
            p = r / ".git/objects" / oid[:2] / oid[2:]
            p.chmod(0o644); p.write_bytes(b"corrupt")
    return ["--lane", str(r), "--work", "{WORK}"]


def b_probe_dir(ctx, d):  # derived-stem receipt whose name has uppercase/underscore differences + list
    r = two(ctx, d)
    return ["--lane", str(r), "--list"]


FIXTURES_TR = [
    dict(fid="tr-only-subset", build=b_only), dict(fid="tr-only-none", build=b_only_none),
    dict(fid="tr-jobs2-rendezvous", build=b_rendezvous),
    dict(fid="tr-work-parent", build=b_work, post=True), dict(fid="tr-env-tmpdir", build=b_env_tmp, env={"TMPDIR": "{WORK:wp}"}),
    dict(fid="tr-work-beats-env", build=b_work_and_env, env={"TMPDIR": "{WORK:other}"}),
    dict(fid="tr-runas-args", build=b_runas_args), dict(fid="tr-no-runas", build=b_no_runas), dict(fid="tr-runas-uv", build=b_runas_uvish),
    dict(fid="tr-firstdiff-byte", build=b_firstdiff_byte), dict(fid="tr-firstdiff-len", build=b_firstdiff_len),
    dict(fid="tr-script-absent", build=b_script_absent), dict(fid="tr-temp-differ", build=b_temp_differ),
    dict(fid="tr-tamper-comma", build=b_tamper_comma), dict(fid="tr-tamper-twice", build=b_tamper_twice),
    dict(fid="tr-auto-control-cheapest", build=b_auto_control),
    dict(fid="tr-post-state", build=b_post, post=True), dict(fid="tr-list-only", build=b_probe_dir),
    dict(fid="tr-clonefail-measure", build=b_clonefail),
]

# ---------------- sources_adopt ----------------
HDR = ("| id | source | kind | tier | claim | anchor | teaches | status | opened | recheck | used-by |\n"
       "|---|---|---|---|---|---|---|---|---|---|---|\n")


def srow(i, st="mined", rc="2027-01-24", opened="2026-10-26", anchor="anchor “alpha beta gamma”", src=None, extra=None, cells=None):
    c = cells or [src or f"Fixture source {i} — https://example.org/{i}", "docs", "A", "claim", anchor, "teaches", st, opened, rc,
                  "corpus/knowledge/x.md"]
    if extra: c = c + extra
    return f"| S{i:03d} | " + " | ".join(c) + " |\n"


def sa_tree(ctx, d, extra_files=None):
    ctx.write(d / "reg.md", HDR + srow(1) + srow(2))
    ctx.write(d / "pkg.md", HDR + srow(10) + srow(11, "queued"))
    ctx.write(d / "pkgq.md", HDR + srow(10))
    ctx.write(d / "art/doc.txt", "the alpha beta gamma delta text\n")
    ctx.write(d / "map_ok.json", json.dumps({"doc.txt": "https://example.org/10"}))
    for k, v in (extra_files or {}).items():
        ctx.write(d / k, v)


def cli(*args, files=None, post=None):
    def b(ctx, d):
        sa_tree(ctx, d, files)
        return list(args)
    return b


R = ["--registry", "reg.md", "--package", "pkg.md"]
A = ["--access-date", "2026-10-26", "--entries", "corpus/knowledge/x.md"]
QA = ["--quote-file", "pkgq.md", "--artifact", "art"]
W = {}
FIXTURES_SA = [
    dict(fid="sa-selftest", build=cli("--selftest")),
    dict(fid="sa-admit-ok", build=cli(*R, "--admit-ids", "S010", *A)),
    dict(fid="sa-admit-two-opened-elsewhere", build=cli(*R, "--admit-ids", "S010", *A, "--attest-opened"), ),
    dict(fid="sa-admit-out", build=cli(*R, "--admit-ids", "S010", *A, "--out", "out.txt"), post="out.txt"),
    dict(fid="sa-admit-no-date", build=cli(*R, "--admit-ids", "S010", "--entries", "e")),
    dict(fid="sa-admit-no-entries", build=cli(*R, "--admit-ids", "S010", "--access-date", "2026-10-26")),
    dict(fid="sa-admit-bad-date", build=cli(*R, "--admit-ids", "S010", "--access-date", "26/10/2026", "--entries", "e")),
    dict(fid="sa-admit-bad-recheck", build=cli(*R, "--admit-ids", "S010", *A, "--recheck", "soon")),
    dict(fid="sa-admit-recheck-iso", build=cli(*R, "--admit-ids", "S010", *A, "--recheck", "2027-03-01")),
    dict(fid="sa-admit-recheck-90d", build=cli(*R, "--admit-ids", "S010", *A, "--recheck", "90d")),
    dict(fid="sa-admit-recheck-never", build=cli(*R, "--admit-ids", "S010", *A, "--recheck", "never")),
    dict(fid="sa-admit-missing-id", build=cli(*R, "--admit-ids", "S099", *A)),
    dict(fid="sa-admit-queued", build=cli(*R, "--admit-ids", "S011", *A)),
    dict(fid="sa-check-only", build=cli(*R)),
    dict(fid="sa-scope-dirty-other", build=cli("--registry", "reg.md", "--package", "pkgs1.md", "--scope-to-admit", "--admit-ids", "S010", *A,
                                               files={"pkgs1.md": HDR + srow(10) + srow(11, extra=["extra"])})),
    dict(fid="sa-noscope-dirty-other", build=cli("--registry", "reg.md", "--package", "pkgs1.md", "--admit-ids", "S010", *A,
                                                 files={"pkgs1.md": HDR + srow(10) + srow(11, extra=["extra"])})),
    dict(fid="sa-scope-dirty-requested", build=cli("--registry", "reg.md", "--package", "pkgs2.md", "--scope-to-admit", "--admit-ids", "S011", *A,
                                                   files={"pkgs2.md": HDR + srow(10) + srow(11, extra=["extra"])})),
    dict(fid="sa-scope-collide-other", build=cli("--registry", "reg.md", "--package", "pkgs3.md", "--scope-to-admit", "--admit-ids", "S010", *A,
                                                 files={"pkgs3.md": HDR + srow(10) + srow(2)})),
    dict(fid="sa-scope-collide-requested", build=cli("--registry", "reg.md", "--package", "pkgs4.md", "--scope-to-admit", "--admit-ids", "S002", *A,
                                                     files={"pkgs4.md": HDR + srow(10) + srow(2)})),
    dict(fid="sa-scope-dupe-other", build=cli("--registry", "reg.md", "--package", "pkgs5.md", "--scope-to-admit", "--admit-ids", "S010", *A,
                                              files={"pkgs5.md": HDR + srow(10) + srow(12) + srow(12)})),
    dict(fid="sa-scope-prose-other", build=cli("--registry", "reg.md", "--package", "pkgs6.md", "--scope-to-admit", "--admit-ids", "S010", *A,
                                               files={"pkgs6.md": HDR + srow(10) + srow(11, rc="re-check in Jan")})),
    dict(fid="sa-scope-prose-requested", build=cli("--registry", "reg.md", "--package", "pkgs7.md", "--scope-to-admit", "--admit-ids", "S010", *A,
                                                   files={"pkgs7.md": HDR + srow(10, rc="re-check in Jan") + srow(11)})),
    dict(fid="sa-noscope-prose", build=cli("--registry", "reg.md", "--package", "pkgs7.md", "--admit-ids", "S010", *A,
                                           files={"pkgs7.md": HDR + srow(10, rc="re-check in Jan") + srow(11)})),
    dict(fid="sa-quote-ok-dir", build=cli(*QA)),
    dict(fid="sa-quote-ok-file-map", build=cli("--quote-file", "pkgq.md", "--artifact", "art/doc.txt", "--url-map", "map_ok.json")),
    dict(fid="sa-quote-artifact-missing", build=cli("--quote-file", "pkgq.md", "--artifact", "nope")),
    dict(fid="sa-quote-file-missing", build=cli("--quote-file", "nofile.md", "--artifact", "art")),
    dict(fid="sa-quote-artifact-emptydir", build=cli("--quote-file", "pkgq.md", "--artifact", "emp", files={"emp/.keep": ""})),
    dict(fid="sa-quote-artifact-nonutf8", build=cli("--quote-file", "pkgq.md", "--artifact", "bin", files={"bin/x.bin": b"\xff\xfe\x00bad"})),
    dict(fid="sa-quote-malformed-row", build=cli("--quote-file", "pkgm.md", "--artifact", "art",
                                                  files={"pkgm.md": HDR + srow(10, extra=["extra"])})),
    dict(fid="sa-quote-malformed-pipe", build=cli("--quote-file", "pkgm.md", "--artifact", "art",
                                                   files={"pkgm.md": HDR + "| S010 | a | b |\n"})),
    dict(fid="sa-quote-long", build=cli("--quote-file", "pkgl.md", "--artifact", "art",
                                        files={"pkgl.md": HDR + srow(10, anchor="anchor “" + " ".join(f"w{k}" for k in range(30)) + "”")})),
    dict(fid="sa-quote-25words", build=cli("--quote-file", "pkgl.md", "--artifact", "art",
                                           files={"pkgl.md": HDR + srow(10, anchor="anchor “" + " ".join(f"w{k}" for k in range(25)) + "”"),
                                                  "art/doc.txt": " ".join(f"w{k}" for k in range(25)) + "\n"})),
    dict(fid="sa-quote-26words", build=cli("--quote-file", "pkgl.md", "--artifact", "art",
                                           files={"pkgl.md": HDR + srow(10, anchor="anchor “" + " ".join(f"w{k}" for k in range(26)) + "”"),
                                                  "art/doc.txt": " ".join(f"w{k}" for k in range(26)) + "\n"})),
    dict(fid="sa-quote-absent", build=cli("--quote-file", "pkga.md", "--artifact", "art",
                                          files={"pkga.md": HDR + srow(10, anchor="anchor “not in artifact”")})),
    dict(fid="sa-quote-mismatch", build=cli("--quote-file", "pkgq.md", "--artifact", "art", "--url-map", "map_bad.json",
                                            files={"map_bad.json": json.dumps({"doc.txt": "https://example.org/99"})})),
    dict(fid="sa-quote-unmapped", build=cli("--quote-file", "pkgq.md", "--artifact", "art", "--url-map", "map_empty.json",
                                            files={"map_empty.json": "{}"})),
    dict(fid="sa-quote-map-broken", build=cli("--quote-file", "pkgq.md", "--artifact", "art", "--url-map", "map_broken.json",
                                              files={"map_broken.json": "{nope"})),
    dict(fid="sa-quote-map-list", build=cli("--quote-file", "pkgq.md", "--artifact", "art", "--url-map", "map_list.json",
                                            files={"map_list.json": "[]"})),
    dict(fid="sa-quote-map-nested", build=cli("--quote-file", "pkgq.md", "--artifact", "art", "--url-map", "map_n.json",
                                              files={"map_n.json": '{"a": {"b": "c"}}'})),
    dict(fid="sa-quote-map-norm", build=cli("--quote-file", "pkgq.md", "--artifact", "art", "--url-map", "map_norm.json",
                                            files={"map_norm.json": json.dumps({"doc.txt": "HTTPS://Example.org/10/#frag"})})),
    dict(fid="sa-quote-mapped-ok-multi", build=cli("--quote-file", "pkgq.md", "--artifact", "art2", "--url-map", "map_sub.json",
                                                   files={"art2/sub/doc.txt": "the alpha beta gamma delta text\n",
                                                          "map_sub.json": json.dumps({"sub/doc.txt": "https://example.org/10"})})),
    dict(fid="sa-quote-multi-first-refusal", build=cli("--quote-file", "pkgx.md", "--artifact", "art",
                                                       files={"pkgx.md": HDR + srow(10, anchor="anchor “not here”") + srow(
                                                           11, anchor="anchor “" + " ".join(f"w{k}" for k in range(30)) + "”")})),
    dict(fid="sa-quote-and-registry", build=cli(*QA, "--registry", "reg.md")),
    dict(fid="sa-quote-only-file", build=cli("--quote-file", "pkgq.md")),
    dict(fid="sa-urlmap-alone", build=cli("--url-map", "map_ok.json")),
    dict(fid="sa-bare", build=cli()),
]


# ---- second pass: shapes for the first run's survivors ----
def b_only_unmapped(ctx, d):
    r = lane(ctx, d, {"plans/a_probe.py": probe("a_probe", out("A\n")), "corpus/evidence/r/a-probe.txt": "A\n",
                      "corpus/evidence/r/zz-probe.txt": "Z\n", "corpus/evidence/r/yy-probe.log": "Y\n"})
    return ["--lane", str(r), "--work", "{WORK}", "--only=yy-probe"]


def b_work_new(ctx, d):
    return ["--lane", str(two(ctx, d)), "--work", "{WORK}/new/sub"]


def b_fallback(ctx, d):
    r = lane(ctx, d, {"plans/regex_log_probe.py": probe("regex_log_probe", out("F\n"), doc=False), "corpus/evidence/round36/regex-log-probe.txt": "F\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def b_runas_prior_line(ctx, d):
    body = ('"""Stub.\n\n  python3 other_tool.py --lane .\n  python3 plans/o_probe.py --lane . --mode x\n"""\nimport sys\n'
            "sys.stdout.write(repr(sys.argv[1:]) + '\\n')\n")
    r = lane(ctx, d, {"plans/o_probe.py": body, "corpus/evidence/r/o-probe.txt": "['--lane', '.', '--mode', 'x']\n"})
    return ["--lane", str(r), "--work", "{WORK}"]


def prov_lane(ctx, d, pad=0, readme=None):
    files = {"plans/foo_probe.py": probe("foo_probe", out("X\n")), "corpus/evidence/r/foo-probe.txt": "X\n"}
    files["README.md"] = readme or "# lane\nthe command is plans/foo_probe.py here\nand the receipt foo-probe.txt there\n"
    if pad: files["README.md"] = files["README.md"] + "z" * (pad - len(files["README.md"]))
    return lane(ctx, d, files)


def b_prov_both(ctx, d):
    return ["--lane", str(prov_lane(ctx, d)), "--list"]


def b_prov_2000000(ctx, d):
    return ["--lane", str(prov_lane(ctx, d, pad=2_000_000)), "--list"]


def b_prov_2000001(ctx, d):
    return ["--lane", str(prov_lane(ctx, d, pad=2_000_001)), "--list"]


def b_tamper_masked_equal(ctx, d):
    blob = "/" + "b" * 40 + "/tmpBBBBBBBB\n"
    r = lane(ctx, d, {"plans/regex_log_probe.py": probe("regex_log_probe", out(blob)),
                      "corpus/evidence/round36/regex-log-probe-first-run.txt": blob})
    return ["--lane", str(r), "--work", "{WORK}", "--tamper", "corpus/evidence/round36/regex-log-probe-first-run.txt"]


FIXTURES_TR += [dict(fid="tr-only-unmapped", build=b_only_unmapped), dict(fid="tr-work-new-dir", build=b_work_new),
                dict(fid="tr-fallback-cmd", build=b_fallback), dict(fid="tr-runas-prior-line", build=b_runas_prior_line),
                dict(fid="tr-prov-both", build=b_prov_both), dict(fid="tr-prov-2000000", build=b_prov_2000000),
                dict(fid="tr-prov-2000001", build=b_prov_2000001), dict(fid="tr-tamper-masked-equal", build=b_tamper_masked_equal)]
FIXTURES_SA += [
    dict(fid="sa-admit-dup-request", build=cli(*R, "--admit-ids", "S010,S010", *A)),
    dict(fid="sa-scope-both-bad-status", build=cli("--registry", "reg.md", "--package", "pkgb.md", "--scope-to-admit", "--admit-ids", "S010", *A,
                                                    files={"pkgb.md": HDR + srow(10, st="done") + srow(11, st="done")})),
    dict(fid="sa-noscope-both-bad-status", build=cli("--registry", "reg.md", "--package", "pkgb.md", "--admit-ids", "S010", *A,
                                                     files={"pkgb.md": HDR + srow(10, st="done") + srow(11, st="done")})),
]
