#!/usr/bin/env python3
"""R45LabratReadProof v2: independent classification of the counter's retained strace logs.

For each `FENCE-RUN` line (job index n -> kept/f{n:05d}.txt, per plans/round45_c1_verify.py:run_fence
`keep = os.environ.get('K45_KEEP_STRACE')` / `shutil.copy(log, .../'f{n:05d}.txt')`) this parses every
successful open/openat/openat2/creat destination from the RAW log and classifies it:

  INSIDE       under the fixture dir d (derived from the counter's own naming: root/fx/<battery-file>/f<k>,
               k = nth fixture of that module in build order)
  HARNESS      root/harness.py or root/fence/fixture_fence.py (the code under test, not fixture data)
  SIBLING      a different root/fx/<dir>/f<k> group, or any other path under root not under d  <- the leak
  SYSTEM       anything else (/usr, /etc, /dev/null, ...)

d is derived independently of the log content, so a log whose ONLY opens are in a sibling still shows SIBLING.
"""
import collections
import json
import pathlib
import re
import sys

OPEN_RE = re.compile(r"\b(open|openat|openat2|creat)\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")
HARNESS_TAIL = ("/harness.py", "/fence/fixture_fence.py")


def main():
    run, kept = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    jobs = [l for l in run.read_text(errors="replace").splitlines() if l.startswith("FENCE-RUN ")]
    per_module = collections.Counter()
    rows = []
    for n, line in enumerate(jobs):
        p = line.split()
        group, module, fid, verdict = p[1], p[2], p[3], p[4]
        mod_dir = module.replace("/", "-").removesuffix(".py")
        k = per_module[module]
        per_module[module] += 1
        log = kept / f"f{n:05d}.txt"
        lines = log.read_text(errors="replace").splitlines()
        root = None
        for ln in lines:
            m = re.search(r'"(/[^"]*/)harness\.py"', ln)
            if m:
                root = pathlib.Path(m.group(1))  # trailing slash: this IS the scratch root
                break
        if root is None:  # derive from any /fx/ path
            for ln in lines:
                m = re.search(r'"(/[^"]*/)fx/', ln)
                if m:
                    root = pathlib.Path(m.group(1))  # trailing slash: this IS the scratch root
                    break
        d = (root / "fx" / mod_dir / f"f{k:03d}") if root else None
        cls = collections.Counter()
        sib, inside_ex, sysc = [], [], collections.Counter()
        for ln in lines:
            if not OPEN_RE.search(ln):
                continue
            m = DONE_RE.search(ln)
            if not m or m.group(1).startswith("E") or m.group(1).startswith("-") or not m.group(2):
                continue
            dest = m.group(2)
            path = pathlib.Path(dest)
            if d and (path == d or path.is_relative_to(d)):
                cls["INSIDE"] += 1
                inside_ex.append(dest)
            elif root and any(dest.endswith(t) for t in HARNESS_TAIL):
                cls["HARNESS"] += 1
            elif root and (path == root or path.is_relative_to(root)):
                cls["SIBLING"] += 1
                sib.append(ln.strip()[:220])
            else:
                cls["SYSTEM"] += 1
                sysc[dest] += 1
        rows.append({"n": n, "group": group, "module": module, "fid": fid, "verdict": verdict,
                     "d": str(d), "d_inside": cls["INSIDE"], "harness": cls["HARNESS"],
                     "sibling": cls["SIBLING"], "sibling_lines": sib[:4], "system": cls["SYSTEM"],
                     "system_top": sysc.most_common(3), "log": str(log), "lines": len(lines),
                     "inside_examples": inside_ex[:3]})
    out = kept.parent / "kept-analysis-v2.json"
    out.write_text(json.dumps(rows, indent=1))
    print(json.dumps({
        "jobs": len(rows),
        "sibling_total": sum(r["sibling"] for r in rows),
        "jobs_with_sibling": [f'{r["module"]}/{r["fid"]}' for r in rows if r["sibling"]],
        "harness_total": sum(r["harness"] for r in rows),
        "inside_total": sum(r["d_inside"] for r in rows),
        "system_total": sum(r["system"] for r in rows),
        "jobs_with_zero_inside": [f'{r["module"]}/{r["fid"]}' for r in rows if r["d_inside"] == 0],
        "refusal_jobs": len([r for r in rows if r["group"] == "refusal"]),
        "honest_jobs": len([r for r in rows if r["group"] == "honest"]),
    }, indent=1))
    for r in rows:
        if r["group"] == "refusal" or r["fid"] in ("f1-gitdir-outside", "f4-fifo-include", "f6-repo-above-d",
                                                   "f10-lane-include-regular"):
            print(json.dumps({k: r[k] for k in ("n", "module", "fid", "verdict", "d", "d_inside", "harness",
                                                "sibling", "sibling_lines", "system")}))
    print(json.dumps({"analysis": str(out)}))


if __name__ == "__main__":
    main()
