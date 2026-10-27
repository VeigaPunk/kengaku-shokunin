#!/usr/bin/env python3
"""R44LabratControls: NORMALIZED verdict diff of the C1 control replay against the committed receipts.

Normalization (documented in the report): the envelope command echo is dropped (paths necessarily differ); the
ENVELOPE start/end timestamps are dropped; `cwd=` is folded to <L>; the per-run work dir is folded to <W>; the
`k44-c1-<8 random chars>` fixture-run suffix is folded to RAND; `diff -u` `---`/`+++` header lines are dropped
(hunks stay). Everything else is compared byte for byte.
"""
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/kengaku-r44/R44LabratControls"
CL = f"{S}/lane"
REF = f"{CL}/.ufo/waves/round-44/claims"
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{S}/out"
NORM = f"{S}/out-norm-" + os.path.basename(OUT)

CONTROLS = [
    "control-c1-nothing.txt",
    "control-c1-standing-batteries.txt",
    "control-c1-witness-as-battery.txt",
    "control-c1-no-mutants.txt",
    "control-c1-attribution.txt",
    "control-c1-value.txt",
    "control-c1-tool-edited.txt",
    "control-c1-direction-mislabel.txt",
] + [f"control-c1-hostile-f{i}.txt" for i in range(1, 7)]


def norm(text):
    out = []
    for ln in text.splitlines():
        if ln.startswith("ENVELOPE /usr/bin/bwrap"):
            continue
        m = re.match(r"^ENVELOPE start \d\d:\d\d:\d\d cwd=(\S+)$", ln)
        if m:
            out.append("ENVELOPE start cwd=<L>")
            continue
        m = re.match(r"^ENVELOPE end \d\d:\d\d:\d\d exit=(-?\d+) "
                     r"local_bin_content_before=(\w+) after=(\w+) (\w+)$", ln)
        if m:
            out.append(f"ENVELOPE end exit={m.group(1)} localbin={m.group(4)}")
            continue
        if re.match(r"^DIFF (---|\+\+\+) ", ln):
            continue
        ln = re.sub(r"k44-c1-[0-9a-z]{8}", "k44-c1-RAND", ln)
        ln = re.sub(re.escape(S) + r"/ctl\d*", "<W>", ln)
        ln = ln.replace(f"{S}/lane", "<L>")
        ln = ln.replace("/fast/scratch/hyaku/kengaku-r44/L1/ctl", "<W>")
        ln = ln.replace("/home/vgpnk/Projects/shokunin/kengaku-shokunin", "<L>")
        out.append(ln)
    return "\n".join(out) + "\n"


def main():
    os.makedirs(NORM, exist_ok=True)
    ok = 0
    for name in CONTROLS:
        ref = norm(open(f"{REF}/{name}", encoding="utf-8", errors="replace").read())
        mine = norm(open(f"{OUT}/{name}", encoding="utf-8", errors="replace").read())
        open(f"{NORM}/{name}.ref", "w").write(ref)
        open(f"{NORM}/{name}.mine", "w").write(mine)
        d = subprocess.run(["diff", "-u", f"{NORM}/{name}.ref", f"{NORM}/{name}.mine"],
                           capture_output=True, text=True)
        verdict = "CONFIRMED" if d.returncode == 0 else "FALSIFIED"
        if d.returncode == 0:
            ok += 1
        print(f"{verdict} {name} ref_lines={len(ref.splitlines())} mine_lines={len(mine.splitlines())}")
        if d.returncode != 0:
            print("\n".join(d.stdout.splitlines()[:40]))
    # witness-run.txt is the direction re-derivation receipt (not a control-c1-* file): reported separately.
    ref = norm(open(f"{REF}/witness-run.txt", encoding="utf-8", errors="replace").read())
    mine = norm(open(f"{OUT}/witness-run.txt", encoding="utf-8", errors="replace").read())
    d = subprocess.run(["diff", "-u", "-", "-"], input=None, capture_output=True, text=True) if False else None
    same = ref == mine
    print(f"{'CONFIRMED' if same else 'FALSIFIED'} witness-run.txt (secondary, not counted in n)")
    if not same:
        import difflib
        print("\n".join(list(difflib.unified_diff(ref.splitlines(), mine.splitlines(), "ref", "mine"))[:40]))
    print(f"REPLAY-CTL {ok}/{len(CONTROLS)}")


if __name__ == "__main__":
    sys.exit(main())
