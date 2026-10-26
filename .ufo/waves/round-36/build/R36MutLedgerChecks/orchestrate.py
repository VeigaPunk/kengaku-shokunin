#!/usr/bin/env python3
"""R36MutLedgerChecks — mutation probes for r35_d1..r35_d4 + row/predicate logic.

Two disposable fixtures cloned per the round-36 fixture rule (clone --no-checkout --shared,
sparse-checkout, checkout master, verify toplevel). All writes stay inside the fixtures + /tmp.
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = "/tmp/k36mut/mutprobe.py"
LOGPATH = pathlib.Path("/tmp/k36mut/log.json")
LOG = []
DIGEST_FILES = [
    "plans/round36_c1_verify.py", "plans/pkg-spec-r35.json",
    "corpus/defects-round35.jsonl", "corpus/evidence/round36/toolathlon-package.md",
    "SCORECARD.md", "corpus/lessons/round-34.md",
]


def rec(kind, **kw):
    LOG.append({"kind": kind, **kw})
    print(f"[{kind}] " + " ".join(f"{k}={v}" for k, v in kw.items() if not isinstance(v, str) or len(v) < 90))


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def sh(args, cwd=None, check=True, input=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, input=input)
    if check and r.returncode != 0:
        raise RuntimeError(f"rc={r.returncode} args={args}\nSTDOUT{r.stdout}\nSTDERR{r.stderr}")
    return r


def lane_state(tag):
    st = {"tag": tag, "head": sh(["git", "-C", str(LANE), "rev-parse", "HEAD"]).stdout.strip(),
          "digests": {f: sha(LANE / f) for f in DIGEST_FILES}}
    rec("lane_state", **st)
    return st


def make_fixture(tag, cleanup_nested):
    D = pathlib.Path(tempfile.mkdtemp(prefix="k36mut-"))
    fix = D / "lane"
    sh(["git", "clone", "-q", "--no-checkout", "--shared", str(LANE), str(fix)])
    sh(["git", "-C", str(fix), "sparse-checkout", "set", "--no-cone",
        "/plans/**", "/corpus/**", "/SCORECARD.md", "/.ufo/waves/round-34/assimilation/captures/**"])
    sh(["git", "-C", str(fix), "checkout", "-q", "master"])
    top = sh(["git", "-C", str(fix), "rev-parse", "--show-toplevel"]).stdout.strip()
    assert pathlib.Path(top).resolve() == fix.resolve(), (top, fix)
    head = sh(["git", "-C", str(fix), "rev-parse", "HEAD"]).stdout.strip()
    rec("fixture", tag=tag, path=str(fix), head=head, toplevel_ok=True)
    if cleanup_nested:
        paths = [l for l in sh(["git", "-C", str(fix), "ls-tree", "-r", "--name-only", "refs/heads/master"]).stdout.split("\n")
                 if re.match(r"^\.ufo/waves/round-3[0-9]/.*/\.ufo/waves/round-", l)]
        assert len(paths) == 21, f"expected 21 nested paths, got {len(paths)}"
        for p in paths:
            sh(["git", "-C", str(fix), "update-index", "--force-remove", p])
        commit(fix, "fixture: drop 21 committed nested round-3x paths (d3 baseline)")
        rec("d3_baseline", removed=len(paths))
    return D, fix


def commit(fix, msg):
    r = sh(["git", "-C", str(fix), "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", msg])
    return r


def git_add_blob(fix, rel, content="k36 probe\n"):
    blob = sh(["git", "-C", str(fix), "hash-object", "-w", "--stdin"], input=content).stdout.strip()
    sh(["git", "-C", str(fix), "update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}"])


def git_rm(fix, rel):
    sh(["git", "-C", str(fix), "update-index", "--force-remove", rel])


def probe_check(fix, name, tag):
    r = sh([sys.executable, PROBE, str(fix), name], check=False)
    out = r.stdout.strip() or r.stderr.strip()[-300:]
    rec("check", tag=tag, check=name, rc=r.returncode, out=out)
    return r


def counter(fix, tag):
    r = sh([sys.executable, "plans/round36_c1_verify.py", "--lane", "."], cwd=str(fix), check=False)
    rec("counter", tag=tag, rc=r.returncode, stdout=r.stdout, stderr_tail=r.stderr.strip()[-300:])
    return r


try:
    before = lane_state("before")

    # ---- fixtures first, both at the same lane HEAD ----
    DA, fixA = make_fixture("A-d3-d4-gates", cleanup_nested=True)
    DB, fixB = make_fixture("B-ledger", cleanup_nested=False)
    ident = sh(["git", "-C", str(fixA), "log", "-1", "--format=%an <%ae>"]).stdout.strip()
    rec("fixture_identity", identity=ident)
    assert DA != DB

    # ================= d3 probes =================
    probe_check(fixA, "r35_d3", "d3-P0-pristine")            # expect ok=True
    D3 = [
        ("d3-M1-nested-round-34", ".ufo/waves/round-34/k36probe/.ufo/waves/round-34/deep.txt", False),
        ("d3-M2-nested-round-28", ".ufo/waves/round-28/k36probe/.ufo/waves/round-28/deep.txt", True),
        ("d3-M3-depth-1", ".ufo/waves/round-34/k36shallow.txt", True),
        ("d3-M4-nested-round-30", ".ufo/waves/round-30/k36probe/.ufo/waves/round-30/deep.txt", False),
    ]
    for tag, rel, must_not_count in D3:
        git_add_blob(fixA, rel)
        commit(fixA, f"mutant {tag}: add {rel}")
        probe_check(fixA, "r35_d3", tag + ("-expect-NOCOUNT" if must_not_count else "-expect-COUNT"))
        git_rm(fixA, rel)
        commit(fixA, f"restore {tag}")
        probe_check(fixA, "r35_d3", tag + "-restored")

    # ================= d1/d2 gate stubs + untracked (before lesson exists) =================
    gate = fixA / "plans" / "pkg_gate.py"
    probe_check(fixA, "r35_d1", "d1-P0-no-gate")
    probe_check(fixA, "r35_d2", "d2-P0-no-gate")
    for tag, body in [
        ("gate-accept-all", "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"),
        ("gate-reject-all", "#!/usr/bin/env python3\nimport sys\nsys.exit(1)\n"),
        ("gate-crash-other", "#!/usr/bin/env python3\nimport sys\nsys.exit(2)\n"),
    ]:
        gate.write_text(body)
        sh(["git", "-C", str(fixA), "add", "plans/pkg_gate.py"])  # index-only, keeps d2's untracked count clean
        probe_check(fixA, "r35_d1", "d1-" + tag)
        probe_check(fixA, "r35_d2", "d2-" + tag)
        git_rm(fixA, "plans/pkg_gate.py")
        gate.unlink(missing_ok=True)
    probe_check(fixA, "r35_d2", "d2-gates-restored")
    stray = fixA / "plans" / "k36stray_probe.py"
    stray.write_text("# stray untracked file\n")
    probe_check(fixA, "r35_d2", "d2-M-stray-untracked")
    probe_check(fixA, "r35_d1", "d1-M-stray-untracked")
    stray.unlink()
    probe_check(fixA, "r35_d2", "d2-stray-restored")

    # ================= d4 probes =================
    lesson = fixA / "corpus" / "lessons" / "round-36.md"
    lesson.parent.mkdir(parents=True, exist_ok=True)
    GENUINE = ("# Round 36 lessons (k36 fixture)\n\n## Gate\n"
               "Erratum (round 36): S130 recount from the committed package copy: "
               "13 + 23 + 1 = 37, denominator 38.\n\n## Notes\nplaceholder\n")
    lesson.write_text(GENUINE)
    cap = fixA / "corpus" / "evidence" / "round36" / "toolathlon-package.md"
    cap0, les0 = cap.read_bytes(), GENUINE
    cap_sha, les_sha = sha(cap), sha(lesson)
    probe_check(fixA, "r35_d4", "d4-P0-pristine")            # expect ok=True

    def d4_mut(tag, lesson_text=None, cap_bytes=None, hide_lesson=False):
        if hide_lesson:
            lesson.rename(lesson.with_suffix(".md.bak"))
        else:
            if lesson_text is not None:
                lesson.write_text(lesson_text)
            if cap_bytes is not None:
                cap.write_bytes(cap_bytes)
        probe_check(fixA, "r35_d4", tag)
        if hide_lesson:
            lesson.with_suffix(".md.bak").rename(lesson)
        else:
            lesson.write_text(les0)
            cap.write_bytes(cap0)
        assert sha(lesson) == les_sha and sha(cap) == cap_sha, f"restore failed at {tag}"
        rec("d4_restored", tag=tag, lesson_sha=sha(lesson), cap_sha=sha(cap))

    d4_mut("d4-M1-wrong-sum-36", lesson_text=GENUINE.replace("1 = 37", "1 = 36"))
    d4_mut("d4-M2-omits-S130", lesson_text=GENUINE.replace("S130 recount", "recount"))
    d4_mut("d4-M3-outside-Gate", lesson_text=GENUINE.replace("## Gate\n", "## Gates\n"))
    d4_mut("d4-M4-line-twice",
           lesson_text=GENUINE.replace("## Gate\n",
                                       "## Gate\nErratum (round 36): S130 duplicate line: 13 + 23 + 1 = 37, denominator 38.\n"))
    d4_mut("d4-M5-denominator-39", lesson_text=GENUINE.replace("denominator 38", "denominator 39"))
    assert cap0.count(b"| Outcome | Count | of 38 |") == 1
    d4_mut("d4-M5c-guard-den37-consistent", lesson_text=GENUINE.replace("denominator 38", "denominator 37"),
           cap_bytes=cap0.replace(b"| Outcome | Count | of 38 |", b"| Outcome | Count | of 37 |"))
    assert cap0.count(b"| isolated and callable | 13 | 38 |") == 1
    d4_mut("d4-M6-capture-sums-38",
           cap_bytes=cap0.replace(b"| isolated and callable | 13 | 38 |", b"| isolated and callable | 14 | 38 |"))
    d4_mut("d4-M7-lesson-absent", hide_lesson=True)
    d4_mut("d4-M8-indented", lesson_text=GENUINE.replace("\nErratum", "\n  Erratum"))

    # ================= ledger / row / predicate probes (fixture B = faithful master) =================
    led = fixB / "corpus" / "defects-round35.jsonl"
    orig = led.read_bytes()
    led_sha = sha(led)
    rows = [json.loads(l) for l in orig.decode().splitlines() if l.strip()]
    assert len(rows) == 4 and all(r["status"] == "open" for r in rows), rows

    def led_mut(tag, lines):
        led.write_text("\n".join(lines) + ("\n" if lines else ""))
        counter(fixB, tag)
        led.write_bytes(orig)
        assert sha(led) == led_sha, f"ledger restore failed at {tag}"
        rec("ledger_restored", tag=tag, sha=sha(led))

    counter(fixB, "led-P0-pristine")
    r0 = json.loads(orig.decode().splitlines()[0])
    u = dict(r0, check="r35_dX")
    led_mut("led-M1-unknown-check", [json.dumps(u)] + orig.decode().splitlines()[1:])
    uc = dict(r0, check="r35_dX", status="closed")
    led_mut("led-M1b-unknown-check-closed", [json.dumps(uc)] + orig.decode().splitlines()[1:])
    rows2 = [json.loads(l) for l in orig.decode().splitlines() if l.strip()]
    rows2[2]["status"] = "Closed"
    led_mut("led-M2-status-Closed", [json.dumps(r) for r in rows2])
    rows3 = [json.loads(l) for l in orig.decode().splitlines() if l.strip()]
    rows3.append(dict(rows3[0]))
    led_mut("led-M3-fifth-row", [json.dumps(r) for r in rows3])
    led_mut("led-M4-empty-file", [])
    ledpath_bak = led.with_suffix(".jsonl.bak")
    led.rename(ledpath_bak)
    counter(fixB, "led-M5-missing-file")
    ledpath_bak.rename(led)
    assert sha(led) == led_sha
    rec("ledger_restored", tag="led-M5-missing-file", sha=sha(led))
    bad = orig.decode().splitlines()
    bad[0] = bad[0][:20]
    led_mut("led-M6-malformed-json", bad)

    after = lane_state("after")
    assert before["head"] == after["head"], "lane HEAD moved during run"
    for f in DIGEST_FILES:
        assert before["digests"][f] == after["digests"][f], f"lane digest changed: {f}"
    rec("lane_untouched", ok=True)

    shutil.rmtree(DA, ignore_errors=True)
    shutil.rmtree(DB, ignore_errors=True)
    rec("fixtures_removed", ok=True)
except Exception as e:
    rec("ERROR", err=repr(e), stderr=getattr(e, "stderr", "") if isinstance(e, RuntimeError) else "")
    raise
finally:
    LOGPATH.write_text(json.dumps(LOG, indent=1))
    print(f"LOG written: {LOGPATH} ({len(LOG)} records)")
