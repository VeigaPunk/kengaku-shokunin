#!/usr/bin/env python3
"""R44MutC1Fences driver: run the bounded behavioral detector (counter under envelope, timeout 60)
on pristine + 18 guard mutants across the six hostile modules, the honest witness, and the drafted
fixtures. Checkpoints one JSON line per run into results.jsonl; restartable."""
import json
import pathlib
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r44/R44MutC1Fences")
ENVELOPE = "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-44/claims/envelope.sh"
MUT = {p.stem: p for p in (S / "mut").glob("*.py")}
DRAFTS = sorted(p.name for p in (S / "drafts").iterdir() if p.is_dir())
STD = ["f1_gitfile", "f2_deep", "f3_abbrev", "f4_fifo", "f5_alternates", "f6_above", "W"]
BAT = {t: (S / "bat" / "witness" if t == "W" else S / "bat" / t) for t in STD}
for n in DRAFTS:
    BAT[n] = S / "drafts" / n
DRAFT_TARGET = {"f1b_gitdir_inside": "RB1", "f2c_bare_worktree": "RB6", "f3b_tree_exact": "OA1",
                "f3c_extra_token": "AS1", "f4b_decoy_fifo": "PG1", "f7_anchor_abbrev": "AS2",
                "f8_lane_fifo": "LB2", "f12_wide": "RB2", "hceiling_above": "PG2"}
MUTANTS = ["PG1", "PG2", "PG3", "GT1", "OS1", "AO1", "RB1", "RB2", "RB3", "RB4", "RB5", "RB6",
           "AS1", "AS2", "AS3", "LB1", "LB2", "OA1"]
RES = S / "results.jsonl"


def load_done():
    done = set()
    if RES.exists():
        for line in RES.read_text().splitlines():
            try:
                r = json.loads(line)
                done.add((r["mut"], r["tag"]))
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def classify(out_path, rc):
    text = out_path.read_text(errors="replace")
    lines = [l for l in text.splitlines()]
    setup = [l for l in lines if l.startswith("SETUP")]
    bat = [l for l in lines if l.startswith("BATTERY fixtures=")]
    mut = [l for l in lines if l.startswith("MUTANTS ")]
    if setup:
        return "REFUSED", setup[0][:220]
    if bat:
        return "ADMITTED", (bat[0] + " | " + (mut[0] if mut else "")).strip()
    if rc == 124:
        return "HANG", "no BATTERY/SETUP line before the 60 s kill"
    tail = [l for l in lines if l.strip()][-3:]
    return "OTHER", " ;; ".join(tail)[:220]


def run(mut, tag):
    out = S / "out" / f"{mut}.{tag}.txt"
    cmd = [ENVELOPE, str(S / "env"), "timeout", "60", "python3", str(MUT[mut]),
           "--battery-dir", str(BAT[tag]), "--lane", str(S / "lane"),
           "--only", "U14c", "--work", str(S / "w")]
    with open(out, "w") as fh:
        p = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, cwd=str(S))
    verdict, detail = classify(out, p.returncode)
    row = {"mut": mut, "tag": tag, "rc": p.returncode, "verdict": verdict, "detail": detail}
    with open(RES, "a") as fh:
        fh.write(json.dumps(row) + "\n")
        fh.flush()
    print(f"{mut:6s} {tag:18s} rc={p.returncode:<3d} {verdict:9s} {detail[:130]}", flush=True)
    return row


def main():
    done = load_done()
    todo = []
    for tag in STD + DRAFTS:                      # phase B: pristine baseline on everything
        todo.append(("REF", tag))
    for m in MUTANTS:                             # phase M: mutants on the standard seven
        for tag in STD:
            todo.append((m, tag))
    for d, target in DRAFT_TARGET.items():        # phase D: drafts under their target + GT1
        for m in (target, "GT1"):
            todo.append((m, d))
    todo = [(m, t) for m, t in todo if (m, t) not in done]
    print(f"{len(todo)} runs to do (done={len(done)})", flush=True)
    for mut, tag in todo:
        run(mut, tag)
    print("DRIVER-DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
