#!/usr/bin/env python3
"""ScribeLesson: red/green reconstruction of the round-97 staging sentinel collision.

The frozen probe (plans/round97_sparql_probe.py at T) dispatches a case's staged query on
`source`:

    source, edits = VARIANTS[kind]
    ...
    if source is None:            # no file
        return app
    if source != "solve":         # literal query text (fixed predicate)
        target.write_text(source)
        return app
    ... run solve.sh ...

The dry-run README (L1/dryrun/README.md) re-describes dry run 1 as using
`isinstance(source, str)` instead: the sentinel "solve" is a str, so every solve-based case
wrote the literal text `solve` as the query (12 of 18 cases, per the README).

This script reconstructs the dispatch decision at the level of the two predicates over the
FROZEN case table and the FROZEN VARIANTS map, and counts cases whose staged text would be the
literal sentinel. It does not run the probe or the grader; it is a dispatch-level
reconstruction, and it is the red/green evidence for the lesson criterion
"no solve-based case stages the literal sentinel".

Exit 0 when the fixed predicate leaks 0 and the old predicate leaks >0; 1 otherwise.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PROBE = LANE / "plans/round97_sparql_probe.py"
TABLE = LANE / "plans/round97-cases.json"
SENTINEL = "solve"


def load_probe():
    spec = importlib.util.spec_from_file_location("r97probe", PROBE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def staged_text(source, old: bool) -> str | None:
    """The text `stage()` would write as /app/solution.sparql for this source value.

    None = no file (the `absent` case). For the solve sentinel the real path runs solve.sh;
    at dispatch level its output is not available here, so it is represented by the marker
    "<solve.sh output>" (never the literal sentinel).
    """
    if source is None:
        return None
    if old:
        if isinstance(source, str):
            return source
        return "<solve.sh output>"
    if source != SENTINEL:
        return source
    return "<solve.sh output>"


def main() -> int:
    probe = load_probe()
    cases = json.loads(TABLE.read_text())["cases"]
    variants = probe.VARIANTS
    old_leaks, new_leaks = [], []
    rows = []
    for case in cases:
        kind = case["app"]
        source, _edits = variants[kind]
        old = staged_text(source, old=True)
        new = staged_text(source, old=False)
        if old == SENTINEL:
            old_leaks.append(case["id"])
        if new == SENTINEL:
            new_leaks.append(case["id"])
        rows.append((case["id"], kind, type(source).__name__, old == SENTINEL, new == SENTINEL))
    print(f"PROBE {PROBE}")
    print(f"TABLE {TABLE} cases={len(cases)} variants={len(variants)}")
    print("CASE  KIND                 SOURCE-TYPE  OLD-LITERAL  NEW-LITERAL")
    for cid, kind, typ, ol, nl in rows:
        print(f"{cid}  {kind:<20} {typ:<12} {str(ol):<12} {str(nl)}")
    print(f"OLD_LEAKS n={len(old_leaks)} ids={','.join(old_leaks)}")
    print(f"NEW_LEAKS n={len(new_leaks)} ids={','.join(new_leaks) or '-'}")
    print(f"CRITERION no-solve-case-stages-the-literal-sentinel old={'fail' if old_leaks else 'pass'} "
          f"new={'fail' if new_leaks else 'pass'}")
    ok = bool(old_leaks) and not new_leaks
    print(f"RECONSTRUCTION {'ok' if ok else 'NOT-OK'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
