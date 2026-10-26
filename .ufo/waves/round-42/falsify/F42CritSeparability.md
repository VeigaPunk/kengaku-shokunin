# F42CritSeparability — wave 2 (falsify): separability of C1 and C2

Seat: F42CritSeparability. Date: 2026-10-26. Base: 508434ad55c709337065611691c426f05875492d (docs tip, wave-2 cut).
Claims freeze bc856d8; first probe 523b278; landing ff14d76d. Attack target: the frozen Separability statement
(plans/round-42-claims.md §Separability): "C1 reads only the two tools, plans/battery42 and fixtures it builds from
nothing (no lane clone); C2 reads only its captures, spec, gate, probe, receipt, entry, SOURCES, README, PROVINCE and
the git history of this file and the receipt. Neither counter reads the other's work product: each passes with the
other's work wholly absent."

## Method

Two scratch mirrors of the base, each a full-history clone with one commit on top:

- mirror-a (C2's work removed): deleted `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (entry, 449 lines),
  `corpus/evidence/round42/fibsqrt-probe.txt` (receipt, 24 lines), rows S125–S128 from `corpus/SOURCES.md` (lines
  140–143), the `tb2-circuit-fibsqrt-grader.md` index row (line 75), the eighth-task coverage bullet (line 271) and
  the §Frontier round-42 sub-bullet (lines 362–376) from `corpus/README.md`, the whole `## Round42 partial frontier
  admission` section (lines 537–568) from `PROVINCE.md`, and from `SKILL.md` the `round42-c2` and `fibsqrt-probe`
  registry rows (lines 600–601), the C2 tail of the round-42 registry addendum (lines 683–688 → one sentence), and
  the entire `## Simulator-executed data-artefact TB2 grader — round 42` section (lines 1160–1204). Commit
  `cac6719`; 6 files changed, +1/−579. `plans/` untouched (verified: `git diff 508434ad -- plans/` empty).
  Left in place deliberately (not in the enumerated removal set): captures `corpus/evidence/round42/tb2-circuit-fibsqrt/`,
  `fibsqrt-dry-cases-freeze.txt`, `plans/fibsqrt_probe.py`, `plans/pkg-spec-r42.json`, `plans/pkg_gate.py`,
  QUALITY.md Q33/Q34, and the kake `c42_count.py` PROVINCE row (a different round-42 claim). After the commit the
  only remaining "round-42" reference in the edited files is the kake row; `git status --porcelain` empty.
- mirror-b (C1's work removed): deleted `plans/battery42/` (5 modules, 783 lines). Commit `bfb63d7`; `git status
  --porcelain` empty.

Both mirrors keep the full git history (required for C2's V8/order_check history clauses: freeze commit first adds
claims; receipt commit after; no executed-probe blob under `.ufo/waves/round-42/claims/` at/before receipt commit).

## Runs (host-safety envelope)

Envelope (both runs): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>`.

Run 1 — C1 counter on mirror-a: `env TMPDIR=$S python3 $S/mirror-a/plans/round42_c1_verify.py --lane $S/mirror-a --work $S/c1work`
- before `18:07:37`, after `18:07:41`; `ls -A /home/vgpnk/.local/bin | sha256sum` = `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` before and after.
- exit 0. Key output (full log captured in scratch, quoted predicate lines):
```
BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0
MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=9/9 order=5/5
ADVERTISED direct=13 indirect=1 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass
```
- PINS line (head) `PINS total=2 mismatched=0`; all 14 MUTANT rows killed with `attributed=L<line>` and `hits=2`
  (X6 hits=6); FIXTURE rows all `ok`; no NULL/TAMPERED/SIDECHANNEL lines.

Run 2 — C2 counter on mirror-b: `env TMPDIR=$S python3 $S/mirror-b/plans/round42_c2_verify.py --lane $S/mirror-b --work $S/c2work`
- before `18:07:37`, after `18:08:34`; same `~/.local/bin` digest before and after.
- exit 0. Key output:
```
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=24 distinct_quotes=24 distinct_lines=24 out_of_word_range=0
    gate: P4 ok checked=24 bad=0 first=0
    gate: P5 ok manifest_entries=9 bad=0 first=0
    gate: P6 ok rows=3 bad=0 first=0
    gate: P7 ok source_lines=3 bad=0 first=0
    gate: P8 ok index_rows=49 knowledge_files=49 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4212
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=3 bad=0
V4 ok cases=16 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=7 tags=7 bad=0
V8 ok order_exit=0 result=PASS
V9 ok case_rows=16/16 bad=0
checks=9 defects=0
PREDICATE C2 pass
```

Result: C1 passes with C2's work wholly absent; C2 passes with C1's work wholly absent (battery42). The frozen
separability statement is reproduced.

## Shared-file analysis (any file whose change could move both?)

Runtime read/execute sets from counter source:

- C1 (`plans/round42_c1_verify.py`): `plans/anchor_digest_check.py`, `plans/order_check.py` (PINS digests +
  TOOLS sources, line 544), `plans/battery42/*.py` (line 545), its own source (line 476), fixture dirs built from
  nothing. It reads no corpus file, no claims file, no README/PROVINCE/SKILL/QUALITY at runtime (SKILL/QUALITY
  appear only in its docstring as the advertised contract).
- C2 (`plans/round42_c2_verify.py`): captures + `SHA256SUMS` (V1), `plans/pkg-spec-r42.json` + `plans/pkg_gate.py`
  (V2), `plans/fibsqrt_probe.py` + dry table (V5), `corpus/SOURCES.md` (V3, V6 census via
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`), receipt + entry (V4/V7/V9), `PROVINCE.md` +
  `corpus/README.md` (V9), `plans/order_check.py` + `plans/round-42-claims.md` (V8). It never reads
  `plans/battery42`.

Intersection: **{ `plans/order_check.py` }** — the only file read/executed by both counters. It is pre-existing
lane baseline (unchanged since round 39, pinned `948d5e1d…`), not the work product of either side: C1 treats it as a
tool under test (pin mismatch → `PINS mismatched=1` → fail; 5 of its 14 mutants are edits inside it), C2 executes it
as the V8 ordering gate. Any edit to `order_check.py` moves both counters. Secondary, one-sided dependencies:
C2 also depends on `plans/round-42-claims.md` and the lane git history (via V8); C1 depends on neither. The claims
file is C2-only.

No file belonging to C2's landed work product (entry, S125–S128 rows, README/PROVINCE/SKILL round-42 text, receipt)
is read by C1 at runtime, and no file belonging to C1's work product (`plans/battery42`) is read by C2 at runtime —
confirmed both by source inspection and by the live runs above.

## Limits

- The mirrors are the exact base plus one commit each; the removal commit sits after the receipt commit in history, so
  C2's V8 order clauses (freeze-vs-receipt order, claims-dir scan up to receipt commit) evaluate the original history
  unchanged.
- C2's captures, dry table, probe, spec and gate were left in mirror-a (they are C2 instruments, not in the seat
  spec's enumerated removal list); C1 demonstrably never reads them, so their presence cannot affect the C1 result.
- C1's run on mirror-a finished in ~4 s; the full output contains all 14 attributed kills and 29 fixtures, matching
  the frozen predicate line for line.

VERDICT: separable-yes
