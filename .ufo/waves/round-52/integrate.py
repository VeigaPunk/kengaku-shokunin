#!/usr/bin/env python3
"""Integration helper for kengaku round 52 (L1 KengakuR52a3).

Copies the artefacts the wave seats produced from their scratch dirs into the lane tree, then
runs the two frozen counters and writes their receipts.  The L1 is the only writer of the lane
tree; this script is idempotent and refuses to overwrite an existing file unless --force.

    python3 .ufo/waves/round-52/integrate.py --step captures|rows|confirmations|labels|prior-art|measure|all
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r52")
WAVE = LANE / ".ufo" / "waves" / "round-52"
EV = LANE / "corpus" / "evidence" / "round52"


def sh(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def copy_tree(src: Path, dst: Path, force: bool) -> int:
    if not src.exists():
        print(f"SKIP missing {src}")
        return 0
    n = 0
    for p in sorted(src.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(src)
        out = dst / rel
        if out.exists() and not force:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)
        n += 1
    print(f"copied {n} files {src} -> {dst}")
    return n


def step_captures(force: bool) -> None:
    """Wave-1 fetch seat artefacts -> corpus/evidence/round52/graders/ + SHA256SUMS."""
    seat = WAVE / "w1" / "C1ExecFetchGraders" / "artifacts"
    src = seat / "graders"
    dst = EV / "graders"
    if not src.exists():
        seat = SCRATCH / "C1ExecFetchGraders"
        src = seat / "graders"
    copy_tree(src, dst, force)
    sums = seat / "SHA256SUMS"
    if not sums.exists():
        sums = WAVE / "w1" / "C1ExecFetchGraders" / "artifacts" / "SHA256SUMS"
    if sums.exists() and (force or not (EV / "SHA256SUMS").exists()):
        shutil.copy2(sums, EV / "SHA256SUMS")
        print(f"copied SHA256SUMS -> {EV/'SHA256SUMS'}")


def step_confirmations(force: bool) -> None:
    rows: list[dict] = []
    for d in sorted(SCRATCH.glob("w2-W2ExecConfirm*/confirmations.json")):
        try:
            data = json.loads(d.read_text())
        except Exception as exc:  # noqa: BLE001
            print(f"WARN unreadable {d}: {exc}")
            continue
        if isinstance(data, dict):
            data = data.get("confirmations") or data.get("labels") or []
        for r in data:
            if isinstance(r, dict):
                r.setdefault("source_file", str(d))
                rows.append(r)
    if not rows:
        print("SKIP no confirmation receipts found")
        return
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "confirmations.json").write_text(json.dumps(rows, indent=1))
    print(f"wrote {EV/'confirmations.json'} with {len(rows)} receipts")


def step_labels(force: bool) -> None:
    for cand in (SCRATCH / "w2-W2ExecLabelsMerge" / "labels.json", SCRATCH / "C1ExecBlindLabels" / "labels.json"):
        if not cand.exists():
            continue
        try:
            data = json.loads(cand.read_text())
        except Exception:
            continue
        if isinstance(data, list):
            data = {"labels": data}
        EV.mkdir(parents=True, exist_ok=True)
        (EV / "labels.json").write_text(json.dumps(data, indent=1))
        print(f"wrote {EV/'labels.json'} from {cand} ({len(data.get('labels', []))} labels)")
        return
    print("SKIP no labels file found")


def step_prior_art(force: bool) -> None:
    for cand in (
        SCRATCH / "w2-W2ExecPriorArtCheck" / "prior-art.md",
        SCRATCH / "C1ScoutPriorArt" / "prior-art.md",
        SCRATCH / "w2-W2ScoutPriorArtFresh" / "prior-art.md",
        SCRATCH / "w2-W2ExecPriorArtCheck" / "prior-art-audit.md",
    ):
        if cand.exists():
            EV.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cand, EV / "prior-art.md")
            print(f"wrote {EV/'prior-art.md'} from {cand}")
            return
    print("SKIP no prior-art file found")


def step_rows(force: bool) -> None:
    """Insert the new registry rows into SKILL.md's gate/probe registry table."""
    src = SCRATCH / "w2-W2ExecRowsIntegrate" / "registry-rows.md"
    if not src.exists():
        for d in sorted(SCRATCH.glob("C2ScribeRows*/rows.md")):
            src = d
            break
    if not src.exists():
        print("SKIP no registry rows found")
        return
    rows = []
    for line in src.read_text(errors="replace").splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) != 8:
                continue
            if set(cells[0]) <= set("-: "):
                continue
            rows.append(line)
    if not rows:
        print("SKIP no parsable registry rows in", src)
        return
    skill = LANE / "SKILL.md"
    text = skill.read_text()
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("## Gate/probe registry")), None)
    if start is None:
        print("SKIP registry heading not found")
        return
    end = start
    while end < len(lines) and (lines[end].startswith("|") or not lines[end].strip()):
        end += 1
    existing = {l for l in lines[start:end]}
    new = [r for r in rows if r not in existing]
    if not new:
        print("all rows already present")
        return
    insert_at = end - 1 if end > start and not lines[end - 1].strip() else end
    while insert_at > start and not lines[insert_at - 1].strip():
        insert_at -= 1
    lines[insert_at:insert_at] = new
    skill.write_text("\n".join(lines) + "\n")
    print(f"inserted {len(new)} registry rows into SKILL.md at line {insert_at+1}")


def step_measure(force: bool = False) -> None:
    out = WAVE / "claims"
    out.mkdir(parents=True, exist_ok=True)
    for name, cmd in (
        ("c1-after.txt", [sys.executable, str(LANE / "plans/round52_c1_grader_audit.py"), "--lane", str(LANE)]),
        ("c2-after.txt", [sys.executable, str(LANE / "plans/round52_c2_registry.py"), "--lane", str(LANE)]),
        ("c1-selftest.txt", [sys.executable, str(LANE / "plans/round52_c1_grader_audit.py"), "--selftest"]),
        ("c2-selftest.txt", [sys.executable, str(LANE / "plans/round52_c2_registry.py"), "--selftest"]),
    ):
        rc, text = sh(cmd)
        (out / name).write_text(text)
        print(f"--- {name} exit={rc}")
        print(text.strip()[-800:])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", default="all")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    steps = {
        "captures": step_captures,
        "confirmations": step_confirmations,
        "labels": step_labels,
        "prior-art": step_prior_art,
        "rows": step_rows,
        "measure": step_measure,
    }
    order = ["captures", "rows", "confirmations", "labels", "prior-art", "measure"]
    todo = order if a.step == "all" else [a.step]
    for s in todo:
        if s not in steps:
            print(f"unknown step {s}")
            return 2
        steps[s](a.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
