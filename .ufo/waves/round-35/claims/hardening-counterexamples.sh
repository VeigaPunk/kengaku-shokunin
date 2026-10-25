#!/usr/bin/env bash
# Shows the post-hoc hardening checks (plans/round35_hardening.py) fail on the wave-1 seats'
# counterexamples that the frozen counters accepted. Throwaway copies under /tmp only.
set -uo pipefail
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
P=$L/.ufo/waves/round-35/build/R35CritControls/package
H="python3 $L/plans/round35_hardening.py --repo $L --skip H6"
mk() {  # minimal lane copy holding everything H1-H5 read
  local d; d=$(mktemp -d /tmp/k35-hard.XXXX)
  mkdir -p "$d/plans" "$d/corpus/knowledge" "$d/corpus/lessons" "$d/.ufo/waves/round-34/assimilation"
  cp "$L"/plans/tb2_grader_probe.py "$L"/plans/round35_c1_verify.py "$L"/plans/defect_ledger.py "$d/plans/"
  cp "$L/corpus/knowledge/tb2-protein-assembly-grader.md" "$d/corpus/knowledge/"
  cp "$L/corpus/SOURCES.md" "$d/corpus/"; cp "$L/SCORECARD.md" "$d/"
  cp "$L/corpus/lessons/round-34.md" "$d/corpus/lessons/"
  cp -r "$L/.ufo/waves/round-34/assimilation/captures" "$d/.ufo/waves/round-34/assimilation/"
  echo "$d"
}
echo "== control: honest landed copy (expect failed=0)"
D=$(mk); $H --lane "$D"; rm -rf "$D"
echo "== CE1 R35CritControls junk package: stub probe + 8x 'import' quotes + 'junk' teaches (expect H1,H2,H3 FAIL)"
D=$(mk)
cp "$P/tb2_grader_probe.py" "$D/plans/"; cp "$P/tb2-protein-assembly-grader.md" "$D/corpus/knowledge/"
grep -E '^\| S10[5-7] ' "$P/SOURCES.md" > "$D/junkrows"
python3 - "$D" <<'PY'
import sys, pathlib, re
d = pathlib.Path(sys.argv[1]); junk = (d / "junkrows").read_text().splitlines()
s = (d / "corpus/SOURCES.md").read_text().splitlines()
s = [l for l in s if not re.match(r"^\| S10[5-7] ", l)]
i = max(k for k, l in enumerate(s) if l.startswith("| S104 "))
s[i + 1:i + 1] = junk
(d / "corpus/SOURCES.md").write_text("\n".join(s) + "\n")
PY
$H --lane "$D"; rm -rf "$D"
echo "== CE2 R35CritC2 EXP1: false-but-labelled D4 line (expect H4 FAIL)"
D=$(mk)
python3 - "$D" <<'PY'
import sys, pathlib
d = pathlib.Path(sys.argv[1]); p = d / "SCORECARD.md"
s = [l for l in p.read_text().splitlines() if not l.startswith("- **D4 correction (round 34 C2):**")]
s.append("- **D4 correction (round 34 C2):** the counter draft's selftest was red (SELFTEST green failed at R34C2CounterDraft.md:8, cases=10 failed=0 at R34MutC2Harness.md:12)")
p.write_text("\n".join(s) + "\n")
PY
$H --lane "$D"; rm -rf "$D"
echo "== CE3 R35CritC2 EXP2: erratum saying the quote is not present (expect H5 FAIL)"
D=$(mk)
python3 - "$D" <<'PY'
import sys, pathlib
d = pathlib.Path(sys.argv[1]); p = d / "corpus/lessons/round-34.md"
s = [l for l in p.read_text().splitlines() if not l.startswith("Erratum (round 35):")]
s.append("Erratum (round 35): the staged S091 quote is not present in nec-s091-reopen.html")
p.write_text("\n".join(s) + "\n")
PY
$H --lane "$D"; rm -rf "$D"
echo "== CE4 R35CritC2 secondary: quote injected into an altered capture (expect H5 FAIL on digest)"
D=$(mk); printf '\n<!-- injected -->\n' >> "$D/.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html"
$H --lane "$D"; rm -rf "$D"
echo "== CE5 R35MutC1Quotes M4: one quote row in straight quotes (expect H2 FAIL: unparsed row)"
D=$(mk); sed -i '0,/| “gblock = lines\[0\].lower()” |/s//| "gblock = lines[0].lower()" |/' "$D/corpus/knowledge/tb2-protein-assembly-grader.md"
$H --lane "$D"; rm -rf "$D"
