#!/usr/bin/env python3
"""Mutation driver for scratch_guard.py's selftest (R42ScratchGuard wave-1 falsifier).

For each named mutation: assert the guarded text occurs exactly once, write a scratch copy,
run that copy's --selftest, and report the exit code plus the selftest cases that went red.
A mutant is KILLED iff its selftest exits non-zero and names at least one failing case.
The unmutated copy is the control and must stay green.
"""
import os
import subprocess
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
text = open(SRC, encoding="utf-8").read()

MUTANTS = {
    # drop the lexical `..` refusal: the resolved-containment check must still hold, but the
    # named reasons (and the reason-level assertions) must go red
    "dotdot-removed": (
        '    raw_parts = target.replace(os.sep, "/").split("/")\n'
        '    if ".." in raw_parts:\n'
        '        return _refuse("target-dotdot", target=json.dumps(target))\n',
        '    raw_parts = target.replace(os.sep, "/").split("/")\n'),
    # stop resolving symlinks: a link or a symlinked directory inside the seat now looks inside
    "realpath-off": (
        "    real = os.path.realpath(cand)\n",
        "    real = os.path.normpath(cand)\n"),
    # drop the "seat name must not be a symlink" refusal
    "seat-symlink-ok": (
        "    if os.path.islink(seat_lex):\n"
        '        return _refuse("seat-is-symlink", seat=seat,\n'
        "                       resolves=os.path.realpath(seat_lex))\n",
        ""),
    # drop the explicit sentinel-target branch
    "sentinel-branch-off": (
        "    if real == sentinel_path or cand == sentinel_path:\n"
        '        return _refuse("target-is-sentinel", target=cand)\n',
        ""),
    # drop the explicit root-target branch
    "root-branch-off": (
        "    if real == root:\n"
        '        return _refuse("target-is-root", target=cand)\n',
        ""),
    # stop requiring the sentinel: an unguarded directory becomes deletable
    "sentinel-optional": (
        "    text, why = sentinel_state(root)\n"
        "    if text is None:\n"
        '        return _refuse("root-untrusted", root=root, sentinel=why)\n',
        ""),
    # drop the resolved-containment boundary itself
    "containment-off": (
        "    if not (real == seat_real or real.startswith(seat_real + os.sep)):\n"
        '        return _refuse("target-resolves-outside-seat", seat=seat, target=cand,\n'
        "                       resolves=real, seat_dir=seat_real)\n",
        ""),
}


def run(path):
    tmp = os.path.join(OUT, "tmp-" + os.path.basename(path))
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = tmp
    proc = subprocess.run([sys.executable, path, "--selftest"],
                          capture_output=True, text=True, env=env)
    lines = proc.stdout.splitlines()
    fails = [ln.split()[1] for ln in lines if " FAIL " in ln]
    summary = [ln for ln in lines if ln.startswith("SELFTEST ")]
    return proc.returncode, fails, (summary[-1] if summary else "SELFTEST no-summary")


control = os.path.join(OUT, "control.py")
with open(control, "w", encoding="utf-8") as fh:
    fh.write(text)
code, fails, summary = run(control)
print("control %-22s exit=%d %s" % ("(unmutated)", code, summary))
if code != 0:
    print("CONTROL-NOT-GREEN")
    sys.exit(1)

killed = 0
for name, (old, new) in MUTANTS.items():
    count = text.count(old)
    if count != 1:
        print("mutant %-22s SKIP anchor-count=%d" % (name, count))
        continue
    path = os.path.join(OUT, "mut-%s.py" % name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new, 1))
    code, fails, summary = run(path)
    if code != 0 and fails:
        killed += 1
    print("mutant %-22s exit=%d %s failing=%s"
          % (name, code, summary, ",".join(fails) if fails else "-"))

print("MUTANTS total=%d killed=%d survived=%d"
      % (len(MUTANTS), killed, len(MUTANTS) - killed))
sys.exit(0 if killed == len(MUTANTS) else 1)
