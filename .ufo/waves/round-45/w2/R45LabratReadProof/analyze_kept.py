#!/usr/bin/env python3
"""Independent parse of the strace logs the C1 counter retained via K45_KEEP_STRACE.

Reads `<run txt> FENCE-RUN` lines in order (job index n == kept/f{n:05d}.txt, see
plans/round45_c1_verify.py:run_fence `keep = os.environ.get('K45_KEEP_STRACE')` + `f'f{n:05d}.txt'`)
and re-derives, from the raw log, every successful open/openat/openat2/creat destination.
Classifies: inside d | scratch-outside-d (counter's LEAK rule) | system-outside-everything.
"""
import collections
import json
import pathlib
import re
import sys

OPEN_RE = re.compile(r"\b(open|openat|openat2|creat)\(")
DONE_RE = re.compile(r"=\s+(-?\d+|E[A-Z]+)(?:<(.+)>)?\s*$")


def main():
    run, kept = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    jobs = []
    for line in run.read_text(errors="replace").splitlines():
        if line.startswith("FENCE-RUN "):
            jobs.append(line)
    assert len(jobs) == len(list(kept.glob("f*.txt"))), (len(jobs), len(list(kept.glob("f*.txt"))))
    rows = []
    for n, line in enumerate(jobs):
        parts = line.split()
        group, module, fid, verdict = parts[1], parts[2], parts[3], parts[4]
        log = kept / f"f{n:05d}.txt"
        lines = log.read_text(errors="replace").splitlines()
        # fixture dir: longest common prefix of paths under "<root>/fx/<mod>/f<k>"
        prefixes = set()
        for ln in lines:
            for m in re.finditer(r'"(/[^"]*/fx/[^"]+)"', ln):
                p = m.group(1).split("/")
                if len(p) > 5:
                    prefixes.add("/".join(p[:6]))
        d = pathlib.Path(sorted(prefixes)[0]) if prefixes else None
        root = pathlib.Path(str(d).split("/fx/")[0]) if d else None
        inside = scratch_out = system = 0
        outside_examples = []
        system_paths = collections.Counter()
        for ln in lines:
            if not OPEN_RE.search(ln):
                continue
            m = DONE_RE.search(ln)
            if not m or m.group(1).startswith("E") or m.group(1).startswith("-"):
                continue
            dest = m.group(2)
            if not dest:
                continue
            p = pathlib.Path(dest)
            if d and (p == d or p.is_relative_to(d)):
                inside += 1
            elif root and (p == root or p.is_relative_to(root)):
                scratch_out += 1
                outside_examples.append(ln.strip()[:200])
            else:
                system += 1
                system_paths[dest] += 1
        rows.append({"n": n, "group": group, "module": module, "fid": fid, "verdict": verdict,
                     "d": str(d), "inside": inside, "scratch_outside_d": scratch_out, "system": system,
                     "outside_examples": outside_examples[:3],
                     "system_top": system_paths.most_common(4), "lines": len(lines)})
    # summary
    print(json.dumps({"jobs": len(rows),
                      "scratch_outside_d_total": sum(r["scratch_outside_d"] for r in rows),
                      "fixtures_with_scratch_outside_d": [f'{r["module"]}/{r["fid"]}' for r in rows if r["scratch_outside_d"]],
                      "inside_total": sum(r["inside"] for r in rows),
                      "system_total": sum(r["system"] for r in rows)}, indent=1))
    for r in rows:
        if r["group"] == "refusal" or r["fid"] in ("f1-gitdir-outside", "f4-fifo-include", "f6-repo-above-d",
                                                   "f10-lane-include-regular"):
            print(json.dumps(r))
    # honest: aggregate + any non-dest /dev or etc opens worth citing
    honest = [r for r in rows if r["group"] == "honest"]
    print(json.dumps({"honest": len(honest),
                      "honest_inside": sum(r["inside"] for r in honest),
                      "honest_scratch_outside": sum(r["scratch_outside_d"] for r in honest),
                      "honest_system": sum(r["system"] for r in honest),
                      "honest_zero_inside": [f'{r["module"]}/{r["fid"]}' for r in honest if r["inside"] == 0]},
                     indent=1))
    sys_paths = collections.Counter()
    for r in rows:
        for p, c in r["system_top"]:
            sys_paths[p] += c
    print("SYSTEM_DESTS", json.dumps(sys_paths.most_common(8)))
    (kept.parent / "kept-analysis.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
