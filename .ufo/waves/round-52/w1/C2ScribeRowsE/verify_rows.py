#!/usr/bin/env python3
"""Insert the five drafted rows into a scratch mirror of the lane SKILL.md and re-run the frozen
round-52 C2 counter against that mirror.  Nothing is written inside the lane."""
import importlib.util
import pathlib
import re
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
MIRROR = pathlib.Path(sys.argv[1])
ROWS = pathlib.Path(sys.argv[2])


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_mirror():
    lane = MIRROR / "lane"
    lane.mkdir(parents=True, exist_ok=True)
    for entry in LANE.iterdir():
        if entry.name in ("SKILL.md",):
            continue
        link = lane / entry.name
        if not link.exists() and not link.is_symlink():
            link.symlink_to(entry, target_is_directory=entry.is_dir())
    text = (LANE / "SKILL.md").read_text()
    new_rows = [l for l in ROWS.read_text().splitlines() if l.startswith("| `round")]
    anchor = "| `gate-flip-check` |"
    lines = text.splitlines()
    at = next(i for i, l in enumerate(lines) if l.startswith(anchor))
    out = lines[: at + 1] + new_rows + lines[at + 1:]
    (lane / "SKILL.md").write_text("\n".join(out) + "\n")
    return lane, new_rows


def main():
    lane, new_rows = build_mirror()
    reg = load(LANE / "plans/round52_c2_registry.py", "c2reg")
    adv, rows, regmap, missing, incomplete, entry_missing, unbacked = reg.collect(lane)
    print(f"ROWS-INSERTED {len(new_rows)}")
    print(f"ADVERTISED {len(adv)} REGISTERED {len(regmap)} ROWS {len(rows)}")
    print(f"MISSING {len(missing)} INCOMPLETE {len(incomplete)} "
          f"ENTRY-MISSING {len(entry_missing)} SELFTEST-UNBACKED {len(unbacked)}")
    for r in new_rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        name = cells[0]
        script = reg.entry_script(cells[2])
        print(f"ROW {name} cells={len(cells)} entry={script} "
              f"registered={script in regmap} empty={[i for i, c in enumerate(cells) if not c]} "
              f"unbacked={name in unbacked}")
    for p in missing:
        if "round46_c2" in p or "round46_c3" in p or "round50_c1" in p or "round50_c2" in p or "round51_routing" in p:
            print(f"STILL-MISSING {p}")
    for r in incomplete:
        print(f"INCOMPLETE-ROW {r}")
    print(f"SELFTEST-UNBACKED-LIST {unbacked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
