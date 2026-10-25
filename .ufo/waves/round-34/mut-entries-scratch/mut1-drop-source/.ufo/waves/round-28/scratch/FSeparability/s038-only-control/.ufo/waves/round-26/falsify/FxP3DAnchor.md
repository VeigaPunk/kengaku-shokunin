# FxP3DAnchor — frozen axis-table anchor

Axes: calibration / P3d sensitivity; frozen P2 population; bounded claim scope. Advisory only.
Integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; P3 population base: `f11bffbf9caa9c9e286fb32c568b81b97719656a`.
Scratch export: `/tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base`; no lane production files changed. Installs: none. Python: `3.14.8` (`python3 --version`, exit 0).

## Probe

Export/overlay command: `set -o pipefail && mkdir -p /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive f11bffbf9caa9c9e286fb32c568b81b97719656a | tar -x -C /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 plans/state_check.py plans/fixtures/r25/shonen-seed.txt plans/fixtures/r26/state_p3 | tar -x -C /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base && printf 'export_exit=0\n'` → `export_exit=0`.

`python3 -B /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base/plans/state_check.py --selftest` → exit 0; P3d red mutation reported `P3d.axis.novelty.anchor.1.pin`; `[selftest] ALL PASS`.

Frozen-base control, `python3 -B /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base/plans/state_check.py --root /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base --json` → exit 1 (the registered base mismatches, not a P3d failure): `assertions=275 match=266 mismatch=5 offline_unverifiable=3 out_of_population=12 superseded=1`. P2 population: 247 IDs (231 MATCH, 3 OFFLINE_UNVERIFIABLE, 12 OUT_OF_POPULATION, 1 SUPERSEDED; no P2 mismatches). P3d IDs: `P3d.axis-table.round24=MATCH`, `P3d.axis-table.round25=MATCH`, `P3d.axis.novelty.anchor.1.pin=MATCH`; P3d out-of-population assertions: 0.

Mutation: in the scratch `SCORECARD.md` only, changed line 162's axis token `**novelty**` to `**depth**`; the single physical line/range stayed at line 162. Command `printf 'frozen=' && git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin show f11bffbf9caa9c9e286fb32c568b81b97719656a:SCORECARD.md | wc -l && printf 'mutated=' && wc -l /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base/SCORECARD.md` → `frozen=730`, `mutated=730 /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base/SCORECARD.md`, exit 0.

`python3 -B /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base/plans/state_check.py --root /tmp/kengaku-r26-FxP3DAnchor.T4uCGe/base --json` → exit 1, `assertions=275 match=264 mismatch=7 offline_unverifiable=3 out_of_population=12 superseded=1`. `P3d.axis.novelty.anchor.1.pin` changed MATCH→MISMATCH while the recorded anchor remained `:162` and the observed target line was the mutated `**depth**` row. The fixed P2 ID set remained 247/247 identical; only the overlapping `P2b.axis.novelty.anchor.1` verdict also changed MATCH→MISMATCH, as expected for the shared frozen target. No P2 population expansion or re-scope.

## Scope and gaps

P3d inventories anchors only from its two named re-derived axis tables. This run observed the one frozen anchor `round24/:162`; surrounding section prose anchors are intentionally outside the registered claim, and no all-anchors-covered conclusion is made. This content mutation establishes rejection of a changed axis token, not byte-for-byte immutability of every character on the target line.

LSP unavailable: `read xd://lsp` returned “No such tool”; therefore no LSP status, references, definition, or diagnostics were available. No grep output was used as semantic proof. No build/lint/formatter run.

VERDICT: PASS — P3d detects the assigned target-line content mutation at unchanged range; no actionable finding in this scoped probe.