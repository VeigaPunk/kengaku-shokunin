#!/usr/bin/env python3
"""Round-46 stage-2 control runner (L1 KengakuR46). Reproduces every freeze control receipt in this directory.

Each control runs on a fresh `git clone --shared` of the lane at REV (the stage-2 instrument commit), inside
`envelope.sh`, after the transform named in its receipt header. No control touches the claimed work: the C1 fence
controls run the base fence or a control fence; C2 transforms run on the base tree plus the two frozen tools; C3
controls run on the stage-2 tree, which holds no package.

usage: stage2_controls.py REV SCRATCH [c1|c2|c3 ...]
"""
import concurrent.futures
import pathlib
import re
import shutil
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CL = LANE / ".ufo/waves/round-46/claims"
ENV = CL / "envelope.sh"
W1 = LANE / ".ufo/waves/round-46/w1"
R45F = LANE / ".ufo/waves/round-45/claims/fences"
BASE = "64ba8385ea10af1b78d367dcb242b92d97062af7"


def clone(scr, name, rev):
    d = scr / name / "lane"
    d.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--shared", str(LANE), str(d)], check=True)
    subprocess.run(["git", "-C", str(d), "checkout", "-q", rev], check=True)
    return d


def run(scr, name, d, argv, header):
    out = subprocess.run([str(ENV), str(scr / name / "env")] + argv, cwd=d, capture_output=True, text=True)
    head = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    body = f"# control {name}: {header}\n# measured HEAD {head} (+ transform above)\n" + out.stdout
    if out.stderr.strip():
        body += "# stderr (last 20 lines)\n" + "\n".join(out.stderr.splitlines()[-20:]) + "\n"
    body += f"# exit={out.returncode}\n"
    (CL / f"{name}.txt").write_text(body)
    pred = [l for l in out.stdout.splitlines() if l.startswith("PREDICATE")]
    return name, out.returncode, pred[-1] if pred else "no predicate line"


def c1(rev, scr):
    jobs = []
    d = clone(scr, "control-c1-no-fence", rev)
    (d / "plans/fixture_fence.py").unlink()
    jobs.append(("control-c1-no-fence", d, [], "plans/fixture_fence.py deleted"))
    d = clone(scr, "control-c1-base-fence", rev)
    jobs.append(("control-c1-base-fence", d, [], f"no transform: the base fence (plans/fixture_fence.py @ {BASE})"))
    fences = [R45F / n for n in ("admit_all.py", "refuse_all.py", "static_only.py", "keyed_name.py")]
    fences += sorted((W1 / "R46CritC1Forged/fences").glob("*.py"))
    fences += [W1 / "R46ExecC1Counter/probes/p_nlink_key.py", W1 / "R46ExecC1Counter/probes/p_listdir_parent.py"]
    for f in fences:
        name = f"control-c1-fence-{f.stem}"
        d = clone(scr, name, rev)
        shutil.copy(f, d / "plans/fixture_fence.py")
        jobs.append((name, d, [], f"plans/fixture_fence.py replaced by {f.relative_to(LANE)}"))
    out = []
    with concurrent.futures.ThreadPoolExecutor(3) as ex:
        futs = [ex.submit(run, scr, n, d, ["python3", "plans/round46_c1_verify.py", "--lane", ".", "--work",
                                           str(scr / n / "w"), "--jobs", "6"], h) for n, d, _a, h in jobs]
        for f in futs:
            out.append(f.result())
    return out


def c2(rev, scr):
    tools = ("plans/anchor_line_check.py", "plans/round46_c2_verify.py")
    res = []

    def mk(name):
        d = clone(scr, name, BASE)
        for t in tools:
            subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{t}"], stdout=open(d / t, "wb"), check=True)
        return d

    def go(name, d, header):
        name = name + "-replay"  # the stage-1 receipts keep their committed bytes; these are the scripted replays
        return run(scr, name, d, ["python3", "plans/round46_c2_verify.py", "--lane", ".", "--work", str(scr / name / "w")],
                   header)

    d = mk("control-c2-nothing")
    res.append(go("control-c2-nothing", d, "base tree + the two frozen C2 tools, no transform"))
    d = mk("control-c2-inplace")
    s = (d / "corpus/SOURCES.md").read_text()
    for a, b in (('Dockerfile:1-16, :15 "RUN bash /app/setup.sh" (4 words)', 'Dockerfile:1-20, :17 "RUN bash /app/setup.sh" (3 words)'),
                 ('test.sh:1-31, :28 "echo 1 > /logs/verifier/reward.txt" (6 words)', 'test.sh:1-29, :26 "echo 1 > /logs/verifier/reward.txt" (4 words)'),
                 ('README.md:1-46, :44 "is among the recovered passwords" (5 words)', 'README.md:1-33, :31 "is among the recovered passwords" (5 words)')):
        assert a in s
        s = s.replace(a, b)
    (d / "corpus/SOURCES.md").write_text(s)
    res.append(go("control-c2-inplace", d, "S152/S153/S154 anchors corrected IN PLACE (Q34 forbids)"))
    d = mk("control-c2-junk-supersede")
    lines = (d / "corpus/SOURCES.md").read_text().split("\n")
    for sid, nid in (("S152", "S157"), ("S153", "S158"), ("S154", "S159")):
        row = next(l for l in lines if re.match(r"^\| " + sid + " ", l))
        cells = row.strip().strip("|").split("|")
        cells[0] = f" {nid} "
        cells[6] = f" supersedes {sid} — copied "
        k = max(i for i, l in enumerate(lines) if re.match(r"^\| S1\d\d ", l))
        lines.insert(k + 1, "|" + "|".join(cells) + "|")
    (d / "corpus/SOURCES.md").write_text("\n".join(lines))
    res.append(go("control-c2-junk-supersede", d, "superseding rows S157-S159 that copy the wrong anchors"))
    d = mk("control-c2-splitlines")
    e = d / "corpus/knowledge/tb2-password-recovery-grader.md"
    t = e.read_text()
    a = 'text.replace("\\r\\n", "\\n").strip().split("\\n")'
    assert a in t
    e.write_text(t.replace(a, "text.strip().splitlines()"))
    res.append(go("control-c2-splitlines", d, "entry predictor reads text.strip().splitlines()"))
    d = mk("control-c2-errata-only")
    e = d / "corpus/knowledge/tb2-password-recovery-grader.md"
    e.write_text(e.read_text() + "\n## Errata (round 46)\n\nlone-CR S152 S153 S154 empty-file\n")
    res.append(go("control-c2-errata-only", d, "only the five errata tokens appended"))
    return res


def c3(rev, scr):
    res = []
    d = clone(scr, "control-c3-base", rev)
    res.append(run(scr, "control-c3-base", d, ["python3", "plans/round46_c3_verify.py", "--lane", ".", "--work",
                                              str(scr / "control-c3-base" / "w")], "stage-2 tree, no package"))
    d = clone(scr, "control-c3-filler", rev)
    res.append(run(scr, "control-c3-filler", d, ["python3", "plans/round46_c3_verify.py", "--lane", ".", "--filler",
                                                "--work", str(scr / "control-c3-filler" / "w")],
                   "the committed filler package plans/filler46 scored as the package (--filler)"))
    d = clone(scr, "control-c3-echo", rev)
    shutil.copy(d / "corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt",
                d / "corpus/evidence/round46/polyglot-c-py-probe.txt")
    res.append(run(scr, "control-c3-echo", d, ["python3", "plans/round46_c3_verify.py", "--lane", ".", "--work",
                                              str(scr / "control-c3-echo" / "w")],
                   "the frozen dry table copied as the receipt (echo)"))
    return res


def main():
    rev, scr = sys.argv[1], pathlib.Path(sys.argv[2])
    which = sys.argv[3:] or ["c1", "c2", "c3"]
    scr.mkdir(parents=True, exist_ok=True)
    for w in which:
        for name, rc, pred in {"c1": c1, "c2": c2, "c3": c3}[w](rev, scr):
            print(f"{name} exit={rc} {pred}")


if __name__ == "__main__":
    main()
