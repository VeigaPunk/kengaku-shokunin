#!/usr/bin/env python3
"""P10-disabled pre-receipt mode for the frozen package gate (round-49 C2, the V8 fix).

The package gate `plans/pkg_gate.py` keeps its P10 clause (fresh probe re-run compared byte-for-byte
against the receipt) only behind `--rerun`. The round-46 V8 defect was that pre-receipt controls ran
the gate *with* `--rerun`, so the frozen probe executed before its receipt was committed. The gate's
bytes are pinned twice (spec `frozen_instruments`, counter `GATE_SHA256`) and must not move, so this
wrapper supplies the disabled mode instead of editing the gate.

Four defence layers, each checkable from the printed receipt alone:

  L1  `--rerun` is never passed to the gate, so the P10 clause is not in its clause list.
  L2  the spec handed to the gate has `probe_cmd` replaced by a sentinel that prints
      `P10-PROBE-DISABLED` and exits 3. A mis-wired `--rerun` runs the sentinel, never the probe.
  L3  the wrapper asserts the gate's stdout carries no `P10 DEFECT|ok` line and no sentinel line;
      any hit is a setup error (exit 2), never a pass.
  L4  the wrapper asserts the gate file's sha256 equals its frozen pin, so the mode cannot be run
      against a doctored gate. The pin comes from `--gate-sha256`, else the spec's
      `frozen_instruments["plans/pkg_gate.py"]`; a missing or placeholder pin is a setup error.

Extra witness: the spec's probe file is stamped (digest + mtime) before and after the gate run; a
change during a pre-receipt run is an ordering violation (exit 2).

Fixed output (safe to commit as a control receipt; no `CASE … observed=` line is ever printed):

    GATE MODE pre-receipt p10=disabled
    GATE P10 disabled=1 probe_executed=no sentinel=<path> probe_stamp=<unchanged|absent|missing>
    GATE SPEC effective=<spec> probe=<original probe_cmd[0]> gate=<gate path> gate_sha256=<digest>
    <the gate's own clause lines, verbatim>
    [GATE ORDER VIOLATION <detail>]
    GATE RESULT accept|reject|setup-error

Exit: 0 accept - 1 reject (the gate found a defect) - 2 setup/ordering error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

GATE_REL = "plans/pkg_gate.py"
P10_LINE = re.compile(r"^\s*(?:gate:\s*)?P10\s+(DEFECT|ok)\b")
SENTINEL_TOKEN = "P10-PROBE-DISABLED"
DIGEST = re.compile(r"^[0-9a-f]{64}$")
SENTINEL_NAME = "p10-disabled-sentinel.py"
SPEC_NAME = "spec-p10-disabled.json"
SENTINEL_TEXT = '''#!/usr/bin/env python3
"""P10 sentinel: printed only if a mis-wired --rerun reaches the gate."""
import sys

print("{token}")
sys.exit(3)
'''.format(token=SENTINEL_TOKEN)


class SetupError(Exception):
    """Anything that makes the mode unanswerable: exit 2, never a silent pass."""


def sha256(path: pathlib.Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def is_pin(value) -> bool:
    return isinstance(value, str) and bool(DIGEST.match(value))


def read_spec(path: pathlib.Path) -> dict:
    try:
        text = path.read_text()
    except OSError as e:
        raise SetupError(f"spec unreadable: {path}: {e.strerror}")
    try:
        spec = json.loads(text)
    except ValueError as e:
        raise SetupError(f"spec is not JSON: {path}: {e}")
    if not isinstance(spec, dict):
        raise SetupError(f"spec is not a JSON object: {path}")
    return spec


def gate_pin(spec: dict, given: str) -> str:
    if given:
        if not is_pin(given):
            raise SetupError(f"--gate-sha256 is not a sha256 digest: {given!r}")
        return given
    pins = spec.get("frozen_instruments") or {}
    pin = pins.get(GATE_REL) if isinstance(pins, dict) else None
    if not is_pin(pin):
        raise SetupError(f"no frozen gate pin: --gate-sha256 not given and "
                         f"frozen_instruments[{GATE_REL!r}]={pin!r}")
    return pin


def probe_stamp(root: pathlib.Path, spec: dict) -> tuple[str, tuple[str, int] | None]:
    """(label, (digest, mtime_ns) or None for the original probe the spec names)."""
    cmd = spec.get("probe_cmd")
    first = cmd[0] if isinstance(cmd, list) and cmd else None
    if not isinstance(first, str) or not first:
        return "absent", None
    p = pathlib.Path(first)
    p = p if p.is_absolute() else (root / p)
    try:
        st = p.stat()
        return "unchanged", (sha256(p), st.st_mtime_ns)
    except OSError:
        return "missing", None


def resolve(root: pathlib.Path, given: str, default_rel: str) -> pathlib.Path:
    p = pathlib.Path(given) if given else (root / default_rel)
    p = p if p.is_absolute() else (root / p)
    return p.resolve()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="P10-disabled pre-receipt mode for the frozen package gate")
    ap.add_argument("--root", default=".", help="tree the package gate reads")
    ap.add_argument("--spec", required=True, help="package spec (JSON) the gate would read")
    ap.add_argument("--work", required=True, help="writable directory for the sentinel and effective spec")
    ap.add_argument("--gate", default="", help=f"gate path (default: <root>/{GATE_REL})")
    ap.add_argument("--gate-sha256", default="", help="frozen gate digest (default: the spec's pin)")
    ap.add_argument("--require-clean-tree", action="store_true",
                    help="also run the gate's P9 (no --rerun is ever passed)")
    args = ap.parse_args(argv)

    def finish(result: str, rc: int) -> int:
        print(f"GATE RESULT {result}")
        return rc

    try:
        root = pathlib.Path(args.root).resolve()
        if not root.is_dir():
            raise SetupError(f"root is not a directory: {root}")
        spec_path = pathlib.Path(args.spec)
        spec_path = (spec_path if spec_path.is_absolute() else (root / spec_path)).resolve()
        spec = read_spec(spec_path)

        gate = resolve(root, args.gate, GATE_REL)
        if not gate.is_file():
            raise SetupError(f"gate not found: {gate}")
        want = gate_pin(spec, args.gate_sha256)
        got = sha256(gate)
        if got != want:
            raise SetupError(f"gate is not at its frozen pin: "
                             f"{gate.name if gate == root / GATE_REL else gate} "
                             f"sha256={got} want={want}")

        work = pathlib.Path(args.work)
        work = (work if work.is_absolute() else (root / work)).resolve()
        try:
            work.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise SetupError(f"work directory is not creatable: {work}: {e.strerror}")

        sentinel = work / SENTINEL_NAME
        eff_spec = work / SPEC_NAME
        try:
            sentinel.write_text(SENTINEL_TEXT)
            effective = dict(spec)
            effective["probe_cmd"] = [str(sentinel)]
            eff_spec.write_text(json.dumps(effective, indent=1, sort_keys=False) + "\n")
        except OSError as e:
            raise SetupError(f"work directory is not writable: {work}: {e.strerror}")

        before_label, before = probe_stamp(root, spec)
        cmd = [sys.executable, str(gate), "package", "--root", str(root), "--spec", str(eff_spec)]
        if args.require_clean_tree:
            cmd.append("--require-clean-tree")
        if "--rerun" in cmd:  # unreachable by construction; fail closed if it ever becomes reachable
            raise SetupError("internal: --rerun would be passed")

        print("GATE MODE pre-receipt p10=disabled")
        probe_first = ((spec.get("probe_cmd") or [None])[0]
                       if isinstance(spec.get("probe_cmd"), list) else None)
        print(f"GATE P10 disabled=1 probe_executed=no sentinel={sentinel} probe_stamp={before_label}")
        print(f"GATE SPEC effective={eff_spec} probe={probe_first or '-'} gate={gate} gate_sha256={got}")

        try:
            r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True, timeout=1800)
        except (OSError, subprocess.SubprocessError) as e:
            print(f"GATE SETUP gate did not run: {type(e).__name__}: {e}")
            return finish("setup-error", 2)

        out = r.stdout.rstrip("\n")
        if out:
            print(out)

        p10_hits = [line for line in r.stdout.splitlines() if P10_LINE.match(line)]
        sentinel_hits = [line for line in r.stdout.splitlines() if SENTINEL_TOKEN in line]
        violation = ""
        if p10_hits:
            violation = f"P10 clause ran: lines={len(p10_hits)} first={p10_hits[0].strip()!r}"
        elif sentinel_hits:
            violation = f"P10 sentinel executed: lines={len(sentinel_hits)} first={sentinel_hits[0].strip()!r}"
        after_label, after = probe_stamp(root, spec)
        if before is not None and after != before:
            violation = (violation + "; " if violation else "") + \
                f"probe bytes moved during a pre-receipt run: {before[0][:12]}->{after[0][:12] if after else 'gone'}"
        if violation:
            print(f"GATE ORDER VIOLATION {violation}")
            return finish("setup-error", 2)

        if r.returncode == 0:
            return finish("accept", 0)
        if r.returncode == 1:
            return finish("reject", 1)
        err = " ".join(r.stderr.strip().split())[:200]
        print(f"GATE SETUP gate_exit={r.returncode} stderr={err!r}")
        return finish("setup-error", 2)
    except SetupError as e:
        print("GATE MODE pre-receipt p10=disabled")
        print(f"GATE SETUP {e}")
        return finish("setup-error", 2)


if __name__ == "__main__":
    sys.exit(main())
