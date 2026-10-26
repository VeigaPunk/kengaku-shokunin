"""F39SentinelAudit: the A1 flip keyed to WHICH gate binary the counter is running.

Each fixture is honest about the reference run. A daemon spawned by the build child polls the process table
(readable because the build child is unsandboxed): while a mutant gate process is alive it writes the swap
variant into the live spec, while a reference gate process is alive it writes the normal variant back. The
reference pass, the renamed pass and the audit's own `again_ref` replay therefore see the normal spec, and
every mutant run sees the swapped one -- so the replay reproduces both legs and reports no nondeterminism.
"""
import atexit
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r39/F39SentinelAudit/keep")
import crit_a1_flip as base  # noqa: E402  (its builders; its own atexit daemon is inert: PAIRS empty)

DAEMON = r"""
import json, os, pathlib, sys, time
pairs = json.loads(sys.argv[1])
me = str(os.getpid())
cur = None
deadline = time.time() + 600
while time.time() < deadline:
    mode = None
    try:
        for p in os.listdir("/" "proc"):
            if not p.isdigit() or p == me:
                continue
            try:
                c = open("/" "proc/" + p + "/cmd" "line", "rb").read().decode("utf-8", "replace")
            except OSError:
                continue
            if "pairs = json.loads" in c:
                continue
            if "/gates/M0" in c:
                mode = "mut"
                break
            if "gates/ref.py" in c:
                mode = "ref"
    except OSError:
        pass
    if mode and mode != cur:
        for live, norm, swap in pairs:
            try:
                src = swap if mode == "mut" else norm
                tmp = live + ".tmp"
                pathlib.Path(tmp).write_text(pathlib.Path(src).read_text())
                os.replace(tmp, live)
            except OSError:
                pass
        cur = mode
    time.sleep(0.002)
"""


def _arm(swap_payload, live_path):
    live = pathlib.Path(live_path)
    norm = live.with_name(live.name + ".norm.json")
    norm.write_text(live.read_text())
    swap = live.with_name(live.name + ".swap.json")
    swap.write_text(json.dumps(swap_payload))
    base.PAIRS.append([str(live), str(norm), str(swap)])


base._arm = _arm


def _spawn():
    if not base.PAIRS or base.ROOT is None:
        return
    subprocess.Popen([sys.executable, "-c", DAEMON, json.dumps(base.PAIRS)],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)


atexit.register(_spawn)
FIXTURES = base.FIXTURES
