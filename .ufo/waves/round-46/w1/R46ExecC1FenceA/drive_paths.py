#!/usr/bin/env python3
"""Path audit for seat R46ExecC1FenceA: run one honest and one refusal fixture through the round-45 counter's
sandbox with `strace -e trace=%file` (open + stat + access + readlink + execve) and list every syscall whose
`-y` annotation names a path under the build scratch but outside the fixture dir `d`."""
import importlib.util
import json
import pathlib
import re
import subprocess
import sys

S = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("k45", S / "lane/plans/round45_c1_verify.py")
k45 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k45)
k44 = k45.load(S / "lane/plans/round44_c1_verify.py", "k44")
root = S / "w4"
root.mkdir(exist_ok=True)
(root / "harness.py").write_text(k45.HARNESS)
(root / "fence").mkdir(exist_ok=True)
fence_copy = root / "fence/fixture_fence.py"
fence_copy.write_bytes((S / "lane/plans/fixture_fence.py").read_bytes())
print(f"FENCE-COPY sha256={k45.sha256(fence_copy)}")

TARGETS = [
    ("honest", S / "lane/plans/battery42/a_class.py", 0),
    ("honest", S / "lane/plans/battery43/o_excuse.py", 0),
    ("refusal", S / "lane/plans/refusals45/f10_laneinclude.py", 0),
    ("refusal", S / "lane/plans/refusals45/f5_alternates.py", 0),
]
PATHISH = re.compile(r'<(/[^>]*)>|"(/[^"]*)"')
n = 0
for kind, mod, idx in TARGETS:
    fxs = k45.build_module(k44, S / "lane", root, mod)
    fx = fxs[idx]
    n += 1
    d = fx["dir"]
    logdir = root / "trace" / f"t{n:03d}"
    logdir.mkdir(parents=True, exist_ok=True)
    log = logdir / "log"
    cmd = k44.ro_sandbox(writable=(logdir,), hide=k44.hide_list((S / "lane",), existing=True),
                         empty=root / "empty") \
        + ["/usr/bin/strace", "-f", "-qq", "-y", "-e", "trace=%file", "-o", str(log),
           k44.PY, "-I", str(root / "harness.py"), str(fence_copy), str(d), fx["tool"],
           json.dumps(fx["argv"])]
    r = subprocess.run(cmd, cwd=str(d), capture_output=True, text=True, timeout=180,
                       stdin=subprocess.DEVNULL,
                       env={"PATH": k44.PATH, "HOME": "/nonexistent", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
                            "PYTHONDONTWRITEBYTECODE": "1"})
    outside, syscalls = [], {}
    try:
        text = log.read_text(errors="replace")
    except OSError:
        text = ""
    for line in text.splitlines():
        paths = [p for pair in PATHISH.findall(line) for p in pair if p]
        hits = []
        for p in paths:
            pp = pathlib.Path(p)
            if (pp == root or pp.is_relative_to(root)) and not (pp == d or pp.is_relative_to(d)):
                hits.append(p)
        if hits:
            call = line.split("(", 1)[0].strip()
            syscalls[call] = syscalls.get(call, 0) + 1
            outside.extend(hits)
    verdict = r.stdout.strip()[:40]
    print(f"AUDIT {kind} {mod.parent.name}/{mod.name} fid={fx['fid']} verdict={verdict!r}"
          f" outside_path_refs={len(outside)} by_syscall={syscalls}")
    for p in sorted(set(outside))[:8]:
        print(f"  OUTSIDE {p}")
