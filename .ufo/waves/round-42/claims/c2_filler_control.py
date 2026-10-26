#!/usr/bin/env python3
"""Round-42 freeze control for C2's V9 (round-41 closure R3): a content-free filler package must stay red.

Builds two scratch mirrors (nothing in the lane is written) and calls the frozen counter's `v9()` on each:
  filler   the round-41 filler shape (`.ufo/waves/round-41/build/R41CritClaims/junk-entry.md`: an entry that
           says it teaches nothing, carries no case table), PROVINCE.md and README without the task;
  content  the same mirror with a case table equal to the synthetic receipt, a PROVINCE line naming the task
           and the entry, and a README `## Frontier` naming the task (shows V9 is reachable by the work).
The synthetic receipt is generated from the frozen dry table's case ids (every case observed as predicted);
it is a fixture for V9 only, never a probe run.

  python3 .ufo/waves/round-42/claims/c2_filler_control.py --lane . --work <scratch>
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys
import tempfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    spec_ = importlib.util.spec_from_file_location("c2", lane / "plans/round42_c2_verify.py")
    c2 = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(c2)
    pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k42-c2filler-", dir=a.work))
    try:
        dry = (lane / c2.DRY_REL).read_text().splitlines()
        rows = []
        for l in dry:
            p = l.split()
            if p and p[0] == "CASE":
                rows.append((p[1], p[3].split("=")[1], p[2].split("=")[1]))
        receipt = []
        for cid, letters, verdict in rows:
            receipt.append(" ".join(["CASE", cid, f"predicted={verdict}", f"observed={verdict}",
                                     f"tests={letters}", f"predicted_tests={letters}", "match=yes"]))
        results = {}
        for kind in ("filler", "content"):
            m = root / kind
            for rel in (c2.SPEC_REL,):
                (m / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(lane / rel, m / rel)
            s = c2.spec(m)
            (m / s["receipt"]).parent.mkdir(parents=True, exist_ok=True)
            (m / s["receipt"]).write_text("\n".join(receipt) + "\n")
            entry = ("# tb2 circuit-fibsqrt grader\n\nsource: S125 https://example.invalid/\n"
                     "source: S126 https://example.invalid/\nsource: S127 https://example.invalid/\n\n"
                     "This entry intentionally teaches nothing about the grader.\n")
            province, readme = "# PROVINCE\n", "# corpus\n\n## Frontier\n\n- nothing new\n"
            if kind == "content":
                entry += ("\nS125 S126 S127 are the three pinned files.\n\n## Case table\n\n| case | tests | verdict | what |\n"
                          "|---|---|---|---|\n" + "".join(f"| `{c}` | {t} | {v} | measured |\n" for c, t, v in rows))
                province += f"- circuit-fibsqrt: {pathlib.PurePosixPath(s['entry']).name}\n"
                readme = readme.replace("- nothing new", "- circuit-fibsqrt read")
            (m / s["entry"]).parent.mkdir(parents=True, exist_ok=True)
            (m / s["entry"]).write_text(entry)
            (m / "PROVINCE.md").write_text(province)
            (m / s["readme"]).write_text(readme)
            ok, note = c2.v9(m)
            results[kind] = ok
            print(f"CONTROL {kind} V9 {'ok' if ok else 'DEFECT'} {note}")
        good = results == {"filler": False, "content": True}
        print(f"CONTROL-C2-FILLER {'red-as-required' if good else 'BROKEN'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
