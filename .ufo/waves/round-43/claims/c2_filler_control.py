#!/usr/bin/env python3
"""Round-43 freeze control for C2's V9 and V10 (round-42 closure R5): a filler package must stay red on V10 even when
it copies the receipt.

Builds three scratch mirrors (nothing in the lane is written) and calls the frozen counter's `v9()` and `v10()`:
  filler    the round-41/42 filler shape: an entry that teaches nothing, no case table, no mechanism section;
  informed  the round-42 informed filler (`R42CritClaims` §1): the case table copied from the receipt, PROVINCE and
            README naming the task, and a `## Mechanism` section that points every case at the grader's assert
            line with a verbatim quote of it — everything a reader of the receipt alone can write;
  content   the same mirror with each mechanism row on a decisive line of the captures and a verbatim quote.
V10 must be DEFECT for filler and informed and ok for content; V9 must be ok for informed and content.
The synthetic receipt is generated from the frozen dry table's case ids (every case observed as predicted); it is
a fixture for V9/V10 only, never a probe run. Captures are copied from the lane (their digests are checked by V10).

  python3 .ufo/waves/round-43/claims/c2_filler_control.py --lane . --work <scratch>
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys
import tempfile

# the mechanism rows the `content` mirror writes: one decisive line per case, quoted from the capture
CONTENT = {
    "nop": ("test_outputs.py", 24, "import attack"),
    "oracle-solve-sh": ("solve.sh", 90, "if (c1l ^ c2l) == 0x02000000:"),
    "wrong-key": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen"),
    "oracle-off-by-one": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen"),
    "return-str": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen"),
    "cheat-import-get_keys": ("feal_module.c", 51, '{"get_keys", py_get_keys, METH_NOARGS,'),
    "cheat-always-equal": ("test_outputs.py", 30, "get_keys()[5] == stolen"),
    "cheat-sysmodules-shadow": ("test_outputs.py", 25, "import feal_in_c"),
    "cheat-patch-get_keys": ("test_outputs.py", 30, "assert feal_in_c.get_keys()[5]"),
    "cheat-exit-zero": ("test.sh", 25, "if [ $? -eq 0 ]; then"),
    "cheat-clock-seed": ("feal.c", 65, "uint32_t x = rand() & 0xFFFF;"),
    "slow-oracle-45s": ("test_outputs.py", 29, "stolen = attack.attack(feal_in_c.encrypt)"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    spec_ = importlib.util.spec_from_file_location("c2", lane / "plans/round43_c2_verify.py")
    c2 = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(c2)
    pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)
    root = pathlib.Path(tempfile.mkdtemp(prefix="k43-c2filler-", dir=a.work))
    try:
        rows = []
        for l in (lane / c2.DRY_REL).read_text().splitlines():
            p = l.split()
            if p and p[0] == "CASE":
                rows.append((p[1], p[3].split("=")[1], p[2].split("=")[1]))
        receipt = [" ".join(["CASE", cid, f"predicted={v}", f"observed={v}", f"tests={t}", f"predicted_tests={t}",
                             "match=yes", "regrade=same", "violates=", "--", "x"]) for cid, t, v in rows]
        results = {}
        for kind in ("filler", "informed", "content"):
            m = root / kind
            for rel in (c2.SPEC_REL, c2.DRY_REL):
                (m / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(lane / rel, m / rel)
            shutil.copytree(lane / c2.CAP, m / c2.CAP)
            s = c2.spec(m)
            (m / s["receipt"]).parent.mkdir(parents=True, exist_ok=True)
            (m / s["receipt"]).write_text("\n".join(receipt) + "\n")
            entry = ("# tb2 feal-differential-cryptanalysis grader\n\n"
                     + "".join(f"source: {sid} https://example.invalid/\n" for sid in s["rows"])
                     + "\nThis entry intentionally teaches nothing about the grader.\n")
            province, readme = "# PROVINCE\n", "# corpus\n\n## Frontier\n\n- nothing new\n"
            if kind in ("informed", "content"):
                entry += ("\n" + " ".join(s["rows"]) + " are the pinned files.\n\n## Case table\n\n"
                          "| case | test | verdict | what |\n|---|---|---|---|\n"
                          + "".join(f"| `{c}` | {t} | {v} | measured |\n" for c, t, v in rows))
                entry += "\n## Mechanism\n\n| case | line | quote |\n|---|---|---|\n"
                for c, _t, _v in rows:
                    cap, line, quote = (("test_outputs.py", 30, "assert feal_in_c.get_keys()[5] == stolen")
                                        if kind == "informed" else CONTENT[c])
                    entry += f"| `{c}` | `{cap}:{line}` | “{quote}” |\n"
                province += f"- feal-differential-cryptanalysis: {pathlib.PurePosixPath(s['entry']).name}\n"
                readme = readme.replace("- nothing new", "- feal-differential-cryptanalysis read")
            (m / s["entry"]).parent.mkdir(parents=True, exist_ok=True)
            (m / s["entry"]).write_text(entry)
            (m / "PROVINCE.md").write_text(province)
            (m / s["readme"]).write_text(readme)
            ok9, note9 = c2.v9(m)
            ok10, note10 = c2.v10(m)
            results[kind] = (ok9, ok10)
            print(f"CONTROL {kind} V9 {'ok' if ok9 else 'DEFECT'} {note9}")
            print(f"CONTROL {kind} V10 {'ok' if ok10 else 'DEFECT'} {note10}")
        good = results == {"filler": (False, False), "informed": (True, False), "content": (True, True)}
        print(f"CONTROL-C2-INFORMED-FILLER {'red-as-required' if good else 'BROKEN'}")
        return 0 if good else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
