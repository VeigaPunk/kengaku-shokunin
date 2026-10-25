#!/usr/bin/env bash
# Round-35 C1 cheapest skip-control: re-dress round-34's unadmitted draft entry at the C1 path,
# append S105-S107 rows built from its (round-34) source lines, add an index row and a coverage
# bullet, but skip the claimed work (no capture manifest, no grader run, no located-quote table).
# Runs in a throwaway sparse clone; the lane checkout is never written. Scored by the frozen counter.
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
D=$(mktemp -d /tmp/k35-c1ctl.XXXX)
git clone -q --no-checkout --shared "$L" "$D/lane"
git -C "$D/lane" sparse-checkout set corpus plans
git -C "$D/lane" checkout -q master
[ "$(git -C "$D/lane" rev-parse --show-toplevel)" = "$D/lane" ] || { echo "fixture toplevel mismatch"; exit 3; }
C="$D/lane"
cp "$L/plans/round35_c1_verify.py" "$L/plans/tb2_grader_probe.py" "$C/plans/"
mkdir -p "$C/corpus/evidence/round35/tb2-eval"
cp "$L"/.ufo/waves/round-34/assimilation/captures/tb2-eval/* "$C/corpus/evidence/round35/tb2-eval/"
E=corpus/knowledge/tb2-protein-assembly-grader.md
cp "$L/.ufo/waves/round-34/build/R34EntryTB2/entry.md" "$C/$E"
python3 - "$C" "$E" <<'PY'
import re, sys, pathlib
c, e = pathlib.Path(sys.argv[1]), sys.argv[2]
src = [l for l in (c / e).read_text().splitlines() if l.startswith("source: S10")]
rows = []
for l in src:
    m = re.match(r"source: (S\d+) — (\S+)", l)
    rows.append(f"| {m.group(1)} | TB2 protein-assembly — {m.group(2)} | code | A | pinned task file | pin 2fd12b88 | grader predicate | mined | 2026-10-25 | 180d | {e} |")
s = (c / "corpus/SOURCES.md").read_text()
anchor = "\n## Leads (unopened)"
s = s.replace(anchor, "\n".join([""] + rows) .rstrip() + "\n" + anchor, 1) if anchor in s else s + "\n".join(rows) + "\n"
(c / "corpus/SOURCES.md").write_text(s)
r = (c / "corpus/README.md").read_text()
r = r.replace("| `knowledge/benchmark-grader-semantics.md` |",
              "| `knowledge/tb2-protein-assembly-grader.md` | TB2 protein-assembly grader | S105, S106, S107 |\n| `knowledge/benchmark-grader-semantics.md` |", 1)
r = r.replace("## Coverage map\n", "## Coverage map\n\n- TB2 grader: knowledge/tb2-protein-assembly-grader.md\n", 1)
(c / "corpus/README.md").write_text(r)
PY
git -C "$C" add -- "$E" corpus/SOURCES.md corpus/README.md
cd "$C"
set +e
python3 plans/round35_c1_verify.py --lane "$C"
echo "exit=$?"
rm -rf "$D"
