# R42RevC2Counter — review of `plans/round42_c2_verify.py` vs `plans/round41_c2_verify.py`

Reviewer seat, kengaku round 42 wave 1, 2026-10-26. Scope: is the V1–V8 re-pointing faithful (no check
relaxed; every pin right — recomputed), is V9 sound (CASE_ROW regex, receipt parse, `source:` exclusion,
PROVINCE/README checks; can a disagreeing receipt+entry pass?), is V8 still sound for this round's file
names. Reviewed at clone HEAD `fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`; counter digest unchanged from
freeze (file is frozen; nothing frozen was edited by this seat).

## 1. Re-pointing faithfulness — FAITHFUL

AST comparison of every top-level function (`ast.dump` equality), r41 vs r42:

```
r41-only: []          r42-only: ['v9']
derive: IDENTICAL   dry: IDENTICAL   main: DIFFERS   receipt_cases: IDENTICAL   rows: IDENTICAL
sha256: IDENTICAL   spec: IDENTICAL  v1: IDENTICAL   v2: DIFFERS  v3: IDENTICAL  v4: IDENTICAL
v5: IDENTICAL       v6: IDENTICAL    v7: IDENTICAL   v8: IDENTICAL
```

The two DIFFERS bodies differ only in:

- `v2`: scratch filename `"pkg-spec-r41-effective.json"` → `"pkg-spec-r42-effective.json"` (cosmetic; the
  gate invocation, its flags `--rerun --require-clean-tree`, timeout 1800, and the `receipt_sha256` fill
  are byte-identical).
- `main`: tempdir prefix `k41-c2-` → `k42-c2-` and the checks list gains `("V9", lambda: v9(lane))`.
  `checks=8` → `checks=9` printing falls out of `len(checks)`.

No V1–V8 predicate, regex (`SOURCE_ROW`, `SUMMARY`, `MAP_ROW` all identical), pin, or error path changed.
The r41 docstring's V3 parenthetical (round-37 D3 binding note) was dropped from the r42 docstring — prose
only; `v3` AST is identical. The r41 V8 docstring clause "no freeze-time claims/ file shows the probe
executed" moved into order_check's own docstring long ago; r42's shorter V8 docstring does not weaken the
code (identical `v8`, same order_check at frozen digest).

## 2. Every pin recomputed — ALL MATCH (13/13)

`sha256sum` in my clone vs the counter's constants vs the frozen `SHA256SUMS` vs spec rows:

| object | counter constant | recomputed | match |
|---|---|---|---|
| plans/pkg-spec-r42.json | e836c425…a710439 | e836c425…a710439 | ✓ |
| plans/pkg_gate.py | ea638822…766edd41 | ea638822…766edd41 | ✓ |
| plans/fibsqrt_probe.py | fc58bf3f…ed061b3 | fc58bf3f…ed061b3 | ✓ |
| …/fibsqrt-dry-cases-freeze.txt | 9ee60af6…f6898b5 | 9ee60af6…f6898b5 | ✓ |
| captures Dockerfile, README.md, gates.txt, instruction.md, sim.c, solve.sh, task.toml, test.sh, test_outputs.py | CAPTURES dict | 9/9 equal, and equal to `corpus/evidence/round42/tb2-circuit-fibsqrt/SHA256SUMS` line-for-line, and equal to spec rows S125 (`6117b8ed…`), S126 (`a7f50026…`), S127 (`700645ac…`) | ✓ |

Capture dir holds exactly the 9 captured files + `SHA256SUMS` (no strays). `TASK = "circuit-fibsqrt"`
matches spec `raw_base` and receipt header. Spec keys consumed by the code all exist: `receipt`, `entry`,
`readme`, `rows`, `sources`.

## 3. Run in my clone (bwrap envelope, QUALITY Q32)

Envelope (every run below):
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`

```
date +%T before 17:30:26   after 17:31:26   (60 s wall)
ls -A /home/vgpnk/.local/bin | sha256sum
  before 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18
  after  436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18   (unchanged)
```

Command: `python3 plans/round42_c2_verify.py --lane . --work "$S/absent/x"` (work path absent — counter
created it; round-40 D10(b) fix intact). Clone clean (`git status --porcelain` = 0 lines). Full output:

```
V1 ok listed=9 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 DEFECT no '## Located quotes' section
    gate: P4 DEFECT no parsed quote
    gate: P5 ok manifest_entries=9 bad=0 first=0
    gate: P6 DEFECT rows=3 bad=3 first=S125: rows=0
    gate: P7 DEFECT entry unreadable
    gate: P8 DEFECT index_rows=48 knowledge_files=48 bad=2 first=index rows for knowledge/tb2-circuit-fibsqrt-grader.md=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4212
    gate: defects=5
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V3 DEFECT rows=3 bad=['S125:row', 'S126:row', 'S127:row']
V4 DEFECT receipt or entry absent
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 DEFECT receipt or entry absent
V8 ok order_exit=0 result=PASS
V9 DEFECT receipt, entry, PROVINCE.md or README absent
checks=9 defects=5
PREDICATE C2 fail
exit=1
```

Reading: exactly the not-yet-written wave-1 surfaces fail (entry, SOURCES rows, index row, PROVINCE).
Crucially **P10 ok probe_rerun=byte-equal bytes=4212** — the frozen probe rerun inside V2 reproduced the
receipt byte-for-byte on this host today, so receipt authenticity is live, and V8 is already green (the
receipt commit `523b278` landed after the freeze commit `bc856d8`; `git merge-base --is-ancestor bc856d8
523b278` → true). The freeze-time do-nothing control's 6 defects shrink to exactly 5 because V8's
precondition (receipt committed after claims) is now satisfied — the intended trajectory.

Receipt sanity for V4/V9 parsers: 16 CASE lines, ids in dry-table order (verified by extraction, identical
list), `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, zero `match=NO` lines, receipt is 4212
bytes (= P10's byte count). All 16 case ids match `[a-z0-9-]+`; all `tests=` cells are 3 chars of `[PF]`;
the one extra token on `gates-is-directory` (`test_gates_file_size:error=IsADirectoryError`) sits after
`violates=` and is ignored by both parsers by design.

## 4. V9 soundness — 19 crafted scenarios, fail-closed everywhere it claims

Driver: import the frozen counter, call `v9()` on crafted lanes (spec at pinned digest, receipt variants,
entry/PROVINCE/README variants). `falsify.py` is archived next to this report. Results:

Fail-closed (DEFECT) as required:

| scenario | result |
|---|---|
| D extra 17th row | `case_rows=17/16 … equal=False` |
| E permuted row order | `16/16 equal=False` |
| F tests letters flipped (PPF→PPP) | `16/16 equal=False` |
| G observed verdict flipped | `16/16 equal=False` |
| O uppercase cid row (`NOP`) — regex skips it, count drops | `15/16 equal=False` |
| R heading `## case table` (lowercase) | `no '## Case table' section` |
| T row missing trailing pipe | `15/16 equal=False` |
| U only a divergent case-table section, first section absent | `case_rows=2/16 equal=False` |

Passing (ok) — each matches V9's frozen contract exactly, with named laxness:

| scenario | what it shows |
|---|---|
| A honest 16-row table | baseline `case_rows=16/16 bad=0` |
| B text cell contradicts the receipt's own description (`nop` row text claims full pass) | `<text>` cell is unconstrained — V9 compares only (cid, letters, observed) |
| H ids only in a blockquote line | (b) counts any line not starting exactly with `source:` |
| I ids only as substrings `S1250 S1260 S1270` | (b) is substring, not token, matching |
| J2 valid first table + divergent second `## Case table` later | only the FIRST section is policed |
| K PROVINCE line naming only the entry file name | `circuit-fibsqrt` ⊂ `tb2-circuit-fibsqrt-grader.md`, so `TASK in l` is implied by `name in l`; (c) reduces to "a PROVINCE line contains the entry file name" |
| P fabricated receipt (two observed verdicts flipped) + entry mirroring it | V9 alone passes a fabricated receipt — see below |
| Q ids only on `source-note:` lines | `startswith("source:")` does not exclude `source-note:` (the r41 entry uses that convention at line 366) |
| V CRLF receipt bytes | `read_text()` universal newlines normalize; consistent for entry and receipt, no bypass found |
| N CRLF entry heading | same normalization — my CRLF-strict expectation was wrong, counter is LF-normalized on both sides |

**Can V9 pass with a receipt and entry that disagree?** On every dimension V9's contract checks — case-id
set and order, tests letters, observed verdict — no (E, F, G, D prove the traps fire; O, R, T prove
malformed rows fail closed). On dimensions outside its contract — the free-text cell, `predicted=`,
per-case `violates=` — yes, by design (B): the entry table can describe a case opposite to what its
receipt line says. **V9 in isolation also passes a fabricated receipt + mirrored entry (P).** That is not
a hole in the chain: receipt authenticity rests on V2's P10 fresh rerun byte-compare (observed green
today, §3), id-vs-frozen-table order rests on V4, tag derivation rests on V7, the dry table on V5. The
chain is closed; V9 is a content check, not an authenticity check, and the counter docstring says exactly
that.

Findings (all LOW, all within the frozen spec sentence — the counter is frozen, so these are named limits
for the L1's entry draft, not code changes):

1. L1 should copy the receipt's `-- text` cell verbatim into entry case-table rows; a future counter may
   pin the text cell.
2. V9(b) is satisfied by `source-note:`/blockquote/substring mentions; the L1 entry should mention
   S125–S127 in prose (the honest r41 shape already does, e.g. lines 34, 45, 57).
3. Only the first `## Case table`/`## Frontier` section is checked; the entry should carry exactly one.
4. V9(c)'s task-name half is implied by the file-name half (substring containment); one honest PROVINCE
   line naming both satisfies it as claimed.

## 5. V8 soundness for this round's file names — SOUND, observed green

`v8` is AST-identical to r41's and passes `--claims plans/round-42-claims.md --receipt <spec receipt>`.
order_check (frozen digest inside gate pin; read-only by construction) at `plans/order_check.py`:

- `CLAIMS_NAME = ^round-(\d+)-claims\.md$` parses `round-42-claims.md` → round 42 → scans
  `.ufo/waves/round-42/claims/` blobs up to the receipt commit for executed-probe evidence
  (`P10 …` lines other than the `receipt unreadable[: <path>]` excuse, or `CASE … observed=` lines). The
  freeze controls' only P10 lines are the allowed excuse (`control-c2-nothing.txt`); no CASE-observed
  lines exist under claims/ — order_check printed no HIT.
- Receipt `corpus/evidence/round42/fibsqrt-probe.txt`: first added at `523b278` (child of freeze
  `bc856d8`, verified `merge-base --is-ancestor`), not present in the freeze commit, committed in HEAD —
  all three FAIL clauses cleared.
- Empirical: `V8 ok order_exit=0 result=PASS` in the §3 run.

Round-41's docstring rationale ("a green round-40 run must not be re-filable as this round's evidence")
carries over: the receipt could not have existed at freeze (it did not — `control-c2-nothing.txt` shows
`receipt unreadable`), and no freeze-time claims blob shows a probe execution.

## 6. Residual risk / verification gaps

- I did not execute a full green predicate (the entry does not exist yet — that is the wave-1 work, not
  mine). The P10 rerun inside V2 is the strongest authenticity evidence observed today.
- V6 runs the unpinned host script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (same in
  r41 — not a regression; census_exit=0 today). The counter depends on that host path existing.
- Host python3/gcc stand in for the image's python 3.13/Debian gcc (named in the frozen claims; P10's
  byte-equality today still passed across that stand-in).
- All 19 falsifier lanes were crafted in scratch and deleted with the scratch dir; `falsify.py` is
  archived at `.ufo/waves/round-42/build/R42RevC2Counter/falsify.py`, raw counter output at
  `…/R42RevC2Counter/counter-run-main-clone.txt`.
- Scratch hygiene: `S=/fast/scratch/hyaku/kengaku-r42/R42RevC2Counter` contained only my clone and
  falsifiers; removed after this report was written. No lane file was edited; no git mutation anywhere
  (clone created with `git clone --shared`, verified `rev-parse --show-toplevel` before any call).

No blocking defect found. The re-pointing is faithful, all 13 pins verified, V9 is fail-closed on its
contract and its limits are named above, V8 is sound and already green.

VERDICT: c2-counter-defects-0
