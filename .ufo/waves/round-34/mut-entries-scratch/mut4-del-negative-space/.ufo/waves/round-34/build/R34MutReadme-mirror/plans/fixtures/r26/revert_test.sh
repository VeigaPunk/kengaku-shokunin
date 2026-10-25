#!/bin/sh
# Check that reverting either Round 26 claim leaves the other claim's counter unchanged.
# Every copy and write is confined to a fresh /tmp directory; the lane is read-only.
set -eu

BASE_COMMIT=f11bffbf9caa9c9e286fb32c568b81b97719656a
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "usage: $0 LANE_TREE [BASE_COMMIT]" >&2
    exit 2
fi
lane=$(CDPATH= cd "$1" && pwd -P) || {
    echo "revert_test: cannot enter lane tree: $1" >&2
    exit 2
}
base=${2:-$BASE_COMMIT}
if [ "$(git -C "$lane" rev-parse --show-toplevel 2>/dev/null || true)" != "$lane" ]; then
    echo "revert_test: LANE_TREE must be a Git worktree root: $lane" >&2
    exit 2
fi
if ! git -C "$lane" cat-file -e "$base^{commit}" 2>/dev/null; then
    echo "revert_test: base commit is unavailable: $base" >&2
    exit 2
fi

tmp=$(mktemp -d /tmp/kengaku-r26-revert.XXXXXX)
trap 'rm -rf "$tmp"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
mkdir -p "$tmp/c1" "$tmp/c2" "$tmp/base"
cp -a "$lane/." "$tmp/c1/"
cp -a "$lane/." "$tmp/c2/"

# A tracked path that did not exist at the frozen base is removed only from the copy.
restore_base() {
    rel=$1
    dest=$2
    if git -C "$lane" cat-file -e "$base:$rel" 2>/dev/null; then
        mkdir -p "$(dirname "$dest")"
        git -C "$lane" show "$base:$rel" > "$dest"
    else
        rm -f "$dest"
    fi
}

# Keep only C1's README rows and newly registered sources out of its reverted copy.
# The source IDs are recognized through the C1 knowledge entry's citations/used-by field.
for rel in corpus/README.md corpus/SOURCES.md SCORECARD.md PROVINCE.md; do
    mkdir -p "$tmp/base/$(dirname "$rel")"
    git -C "$lane" show "$base:$rel" > "$tmp/base/$rel"
done
python3 - "$tmp/c1/corpus/README.md" "$tmp/base/corpus/README.md" \
    "$tmp/c1/corpus/SOURCES.md" "$tmp/base/corpus/SOURCES.md" \
    "$tmp/c1/corpus/knowledge/grader-perturbation-audit.md" <<'PY'
from pathlib import Path
import re
import sys

readme, base_readme, sources, base_sources, knowledge = map(Path, sys.argv[1:])
markers = (
    "plans/grader_perturb.py",
    "plans/fixtures/r26/",
    "grader-perturbation-audit.md",
)
readme_lines = readme.read_text(encoding="utf-8").splitlines(keepends=True)
readme_lines = [line for line in readme_lines
                if not (line.lstrip().startswith("|")
                        and any(marker in line for marker in markers))]
readme.write_text("".join(readme_lines), encoding="utf-8")

base_ids = {m.group(1) for line in base_sources.read_text(encoding="utf-8").splitlines()
            if (m := re.match(r"^\|\s*(S\d{3,})\s*\|", line))}
source_ids = set()
if knowledge.is_file():
    source_ids.update(re.findall(r"\bS\d{3,}\b", knowledge.read_text(encoding="utf-8")))
source_lines = sources.read_text(encoding="utf-8").splitlines(keepends=True)
kept = []
for line in source_lines:
    match = re.match(r"^\|\s*(S\d{3,})\s*\|", line)
    c1_row = (match and match.group(1) not in base_ids
              and (match.group(1) in source_ids
                   or "grader-perturbation-audit.md" in line))
    if not c1_row:
        kept.append(line)
sources.write_text("".join(kept), encoding="utf-8")
PY

restore_base plans/grader_perturb.py "$tmp/c1/plans/grader_perturb.py"
restore_base corpus/knowledge/grader-perturbation-audit.md \
    "$tmp/c1/corpus/knowledge/grader-perturbation-audit.md"
for path in "$tmp/c1/plans/fixtures/r26"/perturb_*; do
    [ -e "$path" ] || continue
    if [ -d "$path" ] && [ ! -L "$path" ]; then
        rm -rf "$path"
    else
        rm -f "$path"
    fi
done

# Revert only C2's checker and added R26-E correction lines, preserving other edits.
restore_base plans/state_check.py "$tmp/c2/plans/state_check.py"
python3 - "$tmp/c2/SCORECARD.md" "$tmp/base/SCORECARD.md" \
    "$tmp/c2/PROVINCE.md" "$tmp/base/PROVINCE.md" <<'PY'
from pathlib import Path
import re
import sys

for current, baseline in zip(map(Path, sys.argv[1::2]), map(Path, sys.argv[2::2])):
    baseline_lines = set(baseline.read_text(encoding="utf-8").splitlines())
    lines = current.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [line for line in lines
            if line.rstrip("\r\n") in baseline_lines
            or not re.search(r"\bR26-E\d+\b", line)]
    current.write_text("".join(kept), encoding="utf-8")
PY

capture_c1() {
    label=$1
    tree=$2
    out="$tmp/$label.out"
    status="$tmp/$label.status"
    if [ ! -f "$tree/plans/grader_perturb.py" ]; then
        printf '%s\n' MISSING > "$status"
        : > "$out"
        return
    fi
    if (CDPATH= cd "$tree" && PYTHONDONTWRITEBYTECODE=1 python3 plans/grader_perturb.py --summary) > "$out" 2>&1; then
        printf '%s\n' 0 > "$status"
    else
        rc=$?
        printf '%s\n' "$rc" > "$status"
    fi
}

capture_c2() {
    label=$1
    tree=$2
    out="$tmp/$label.out"
    status="$tmp/$label.status"
    if [ ! -f "$tree/plans/state_check.py" ]; then
        printf '%s\n' MISSING > "$status"
        : > "$out"
        return
    fi
    if (CDPATH= cd "$tree" && PYTHONDONTWRITEBYTECODE=1 python3 plans/state_check.py --summary) > "$out" 2>&1; then
        printf '%s\n' 0 > "$status"
    else
        rc=$?
        printf '%s\n' "$rc" > "$status"
    fi
}

capture_c1 c1_original "$lane"
capture_c2 c2_original "$lane"
capture_c2 c2_without_c1 "$tmp/c1"
capture_c1 c1_without_c2 "$tmp/c2"

python3 - "$tmp" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])

def read_count(label: str, claim: str):
    status = (root / f"{label}.status").read_text(encoding="utf-8").strip()
    text = (root / f"{label}.out").read_text(encoding="utf-8")
    if status == "MISSING":
        return None, "UNAVAILABLE (counting instrument absent)"
    try:
        code = int(status)
    except ValueError:
        return None, f"ERROR (invalid command status {status!r})"
    if claim == "C1":
        if code != 0:
            return None, f"ERROR (exit {code})"
        lines = tuple(line for line in text.splitlines()
                      if line.startswith("FAMILY ") or line.startswith("TOTAL "))
        if not any(line.startswith("TOTAL ") for line in lines):
            return None, "ERROR (summary TOTAL line absent)"
        return (code, lines), "OK"
    if code not in (0, 1):
        return None, f"ERROR (exit {code})"
    summary = next((line for line in text.splitlines()
                    if line.startswith("assertions=") and " mismatch=" in line), None)
    if summary is None:
        return None, "ERROR (summary count line absent)"
    return (code, summary), "OK"

def concise(claim: str, signature):
    if claim == "C1":
        code, lines = signature
        total = next(line for line in lines if line.startswith("TOTAL "))
        return f'{total!r}; family_lines={sum(line.startswith("FAMILY ") for line in lines)}'
    code, line = signature
    return f'{line!r}; exit={code}'

print("C1 counting command: python3 plans/grader_perturb.py --summary")
print("C2 counting command: python3 plans/state_check.py --summary")
result = 0
for claim, original, reverted in (
        ("C1", "c1_original", "c1_without_c2"),
        ("C2", "c2_original", "c2_without_c1")):
    before, before_status = read_count(original, claim)
    after, after_status = read_count(reverted, claim)
    if before is None or after is None:
        print(f"{claim} comparison=UNAVAILABLE baseline={before_status} reverted={after_status}")
        result = 2 if result == 0 else result
        continue
    moved = before != after
    if moved:
        result = 1
    if claim == "C1":
        before_families = [line for line in before[1] if line.startswith("FAMILY ")]
        after_families = [line for line in after[1] if line.startswith("FAMILY ")]
        changed = sum(a != b for a, b in zip(before_families, after_families))
        changed += abs(len(before_families) - len(after_families))
        before_total = next(line for line in before[1] if line.startswith("TOTAL "))
        after_total = next(line for line in after[1] if line.startswith("TOTAL "))
        print(f"C1 baseline={before_total!r}")
        print(f"C1 after_C2_revert={after_total!r}; family_lines_changed={changed}")
    else:
        print(f"C2 baseline={concise(claim, before)}")
        print(f"C2 after_C1_revert={concise(claim, after)}")
    print(f"{claim} comparison={'MOVED' if moved else 'UNCHANGED'}")
print("RESULT=" + ("UNCHANGED" if result == 0 else "MOVED" if result == 1 else "INCOMPLETE"))
sys.exit(result)
PY
