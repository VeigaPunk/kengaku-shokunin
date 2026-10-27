#!/usr/bin/env python3
"""Draft control for the R44MutC2V11 sandbox survivor (NOT frozen, offered to the L1). The frozen predictor
control cannot see that sandboxed() lost `--unshare-net`: no grader or predictor behaviour depends on the
network, so every verdict stays identical. This canary runs through the counter's own sandboxed() and
requires the loopback-only netns fence: /proc/net/dev inside the sandbox must list exactly `lo`. Green on
the pristine counter; red when the net fence is gone (host interfaces visible).
  usage: python3 draft-c2-fence-canary.py <work dir>     (from a lane root holding the counter under test at plans/round44_c2_verify.py)"""
import importlib.util
import pathlib
import shutil
import sys

L = pathlib.Path.cwd()
W = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("c2", L / "plans/round44_c2_verify.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)
shutil.rmtree(W, ignore_errors=True)
W.mkdir(parents=True)
(W / "states.json").write_text("[]")
(W / "fence.py").write_text(
    "import json\n"
    "nics = [l.split(':')[0].strip() for l in open('/proc/net/dev').read().splitlines()[2:]]\n"
    "print(json.dumps(sorted(nics)))\n"
)
try:
    nics = c2.sandboxed(W, "fence.py", [])
except Exception as e:  # fenced: the sandbox refused / crashed is the required state
    ok = True
    print(f"CONTROL fence netns=fenced ok ({type(e).__name__})")
else:
    ok = nics == ["lo"]
    print(f"CONTROL fence nics={nics} required=['lo'] {'ok' if ok else 'DEFECT'}")
print(f"CONTROL-C2-FENCE-CANARY {'red-as-required' if ok else 'NOT-AS-REQUIRED'}")
sys.exit(0 if ok else 1)
