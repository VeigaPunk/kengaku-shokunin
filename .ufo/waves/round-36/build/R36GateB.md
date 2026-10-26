# R36GateB — C1 gate candidate (`pkg_gate.py`), round 36 wave 1

Seat: executor (leaf). Deliverable: one file, `.ufo/waves/round-36/build/R36GateB/pkg_gate.py`.

```
$ sha256sum .ufo/waves/round-36/build/R36GateB/pkg_gate.py
ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41  .ufo/waves/round-36/build/R36GateB/pkg_gate.py
$ wc -l .ufo/waves/round-36/build/R36GateB/pkg_gate.py
398
```

Python 3 stdlib only (`argparse dataclasses hashlib json pathlib re subprocess sys`), no network call of its own,
398 physical lines. Nothing outside `.ufo/waves/round-36/build/` was written; no lane file, no git index, no jj
state touched (`git status --porcelain | grep -v '^?? .ufo/waves/round-36/'` → empty).

## Structure

`Package.load()` parses the tree once into a dataclass (`entry` text, `quote_section`,
`quotes: list[Quote]`, `bad_rows`, `sources: {sid: [cells]}`, `readme`, `_captures` cache). Every clause is a
read-only function over that parsed state; the subcommand only decides which clauses run.

| | clause (spec field it reads) |
|---|---|
| P1 | `frozen_instruments` sha256 pins |
| P2 | `receipt` pin (`receipt_sha256`) |
| P3 | `## Located quotes` section present; **every** data row parses (`QUOTE_ROW`); ≥`min_quotes` distinct quotes, each `quote_words` 3..25 words; ≥`min_distinct_locations` distinct `(capture,start)` |
| P4 | every quote verbatim on its cited capture line(s) (multi-line ranges joined; capture path must be relative and `..`-free) |
| P5 | capture `SHA256SUMS`: every manifest line parses and matches its file's bytes; each spec row's capture is pinned at the spec digest; every quoted capture is pinned; no unlisted direct capture file |
| P6 | SOURCES rows: each id exactly once, 11 cells, `row_tier`, `row_status`, URL == `raw_base + upstream`, `used-by` == entry, teaches ≥`min_teaches_words`, teaches pairwise distinct |
| P7 | provenance trio (one `source: S10x — <pinned url>` per row), `verified-at: <frozen date>`, `recheck:`, `## Negative space` non-empty with a falsifier word |
| P8 | README index row for the entry (cites all rows) + coverage bullet naming entry and receipt + `knowledge files == index rows` (set equality) |
| P9 | `--require-clean-tree` → `git -C ROOT ls-files --others --exclude-standard` empty |
| P10 | `--rerun` → run `probe_cmd` in ROOT, require exit 0 **and** byte-equal receipt |
| D4 | exactly one non-blank line, `d4.label` prefix, all `d4.patterns` in order-sensitive regex form (this is what makes the swapped-citation line fail) |
| D5 | `d5.label` prefix, `require` present / `forbid` absent, capture digest pinned in `manifest_name`, `d5.quote` present in the capture after tag-strip + whitespace removal |

Exit codes: `0` accept, `1` reject, `2` setup (missing/unparsable spec, missing root, or an uncaught
exception — `except Exception` at the top prints `setup: <type>: <msg>` and returns 2, so a crash can never be
read as accept or reject). A clause that raises inside `run_checks` is printed as `DEFECT clause error …` and
counts as a defect.

No fixture identity is read: no fixture id, fixture path, or marker string appears in the file. All labels,
digests, row ids and bounds come from `--spec`.

Two implementation choices worth naming, because they are the difference from the round-35 counters:

- **P5 is a byte pin, not a presence check.** L6's quote-injected capture contains the quote; only the manifest
  digest separates it.
- **D5 is directional and digest-verified.** The genuine line is accepted only when the manifest still pins the
  capture's bytes *and* `is present` is un-negated; "not present" is checked before the quote.

## Battery (fixture clone per the fixture rule)

```
D=$(mktemp -d /tmp/k36-XXXX); git clone -q --no-checkout --shared <lane> "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation /.ufo/waves/round-34/build
git -C "$D/lane" checkout -q master          # rev-parse --show-toplevel == $D/lane checked
# copied in: plans/{regex_log_probe,round36_c1_verify,round36_c2_verify}.py, plans/pkg-spec-r35.json,
#            corpus/defects-round35.jsonl, corpus/evidence/round36/, and the gate as plans/pkg_gate.py
$ cd "$D/lane" && python3 plans/round36_c1_verify.py --lane "$D/lane"
```

```
FIXTURE P0 expect=accept observed=accept ok -- genuine round-35 package
FIXTURE P1 expect=reject observed=reject ok -- 8 one-word quotes
FIXTURE P2 expect=reject observed=reject ok -- 8 copies of one quote
FIXTURE P3 expect=reject observed=reject ok -- an unparsed quote row beside the genuine rows
FIXTURE P4 expect=reject observed=reject ok -- junk teaches cells
FIXTURE P5 expect=reject observed=reject ok -- stub probe printing the receipt
FIXTURE P6 expect=reject observed=reject ok -- untracked leftover file
FIXTURE P7 expect=reject observed=reject ok -- cheapest package: one-word quotes + junk teaches + stub probe + stray file
FIXTURE L1 expect=accept observed=accept ok -- D4 genuine correction line
FIXTURE L2 expect=reject observed=reject ok -- D4 line with the two file:line citations swapped
FIXTURE L3 expect=reject observed=reject ok -- D4 line without the harness token
FIXTURE L4 expect=accept observed=accept ok -- D5 genuine erratum line
FIXTURE L5 expect=reject observed=reject ok -- D5 erratum saying the quote is not present
FIXTURE L6 expect=reject observed=reject ok -- D5 genuine line over an altered (quote-injected) capture
FIXTURES total=14 false_green=0 false_red=0 unevaluated=0
R35-D1 status=open observed=fail agree=yes fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=1
R35-D2 status=open observed=fail agree=yes untracked_anywhere=1 line_fixtures_wrong=0/6
R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21
R35-D4 status=open observed=fail agree=yes round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
rows=4 closed=0 observed_pass=0 mismatches=0
PREDICATE C1 fail
```

Exit 1, `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` — the C1 battery target is met. The four
rows stay red for reasons outside this gate, each named from the run above:

- **R35-D1 (`tip_package_rc=1`)**: the tip package run inside the clone is
  `package --root <clone> --rerun --require-clean-tree`. `git -C <clone> ls-files --others --exclude-standard`
  is exactly one line — `plans/pkg_gate.py`, the gate itself, which a leaf seat may not commit. With the gate
  committed by L1 the same command is clean: run *without* `--require-clean-tree` at the same tip it prints
  `P1..P8 ok`, `P10 ok probe_rerun=byte-equal bytes=3399`, `defects=0`, exit 0.
- **R35-D2**: the same single untracked file (`untracked_anywhere=1`); `line_fixtures_wrong=0/6`.
- **R35-D3**: 21 committed nested round-34 paths; removing them is the round-35 rout's job, not this gate's.
- **R35-D4**: `corpus/lessons/round-36.md` does not exist yet; the recount itself already resolves
  (`13 + 23 + 1 = 37` vs stated `denominator 38`).

## Real lane

```
$ python3 .ufo/waves/round-36/build/R36GateB/pkg_gate.py package \
    --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --rerun \
    --spec /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r35.json
P1 ok pinned=3 mismatched=0
P2 ok receipt_sha256=pinned
P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
P4 ok checked=22 bad=0 first=0
P5 ok manifest_entries=6 bad=0 first=0
P6 ok rows=3 bad=0 first=0
P7 ok source_lines=3 bad=0 first=0
P8 ok index_rows=42 knowledge_files=42 bad=0 first=0
P10 ok probe_rerun=byte-equal bytes=3399
defects=0
REAL_LANE_RC=0
```

(`P9` omitted as instructed: the lane carries the round-36 wave files.) `--rerun` used the round-35 counter's
own fallback because the host `python3` has no Biopython: `import Bio` fails → `uv run --no-project --with
biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`, resolved from the local uv cache in 0.77 s, byte-equal
to the receipt. No network fetch was needed and none was attempted by the gate itself.

## Clause → battery fixture

| clause | killed by | observed line |
|---|---|---|
| P1 instruments | **P5**, **P7** | `P1 DEFECT pinned=3 mismatched=['plans/tb2_grader_probe.py']` |
| P2 receipt | — (no battery fixture; **M4**) | `P2 DEFECT receipt_sha256=9f80b206…` |
| P3 quote shape | **P1**, **P2**, **P3**, **P7** | `P1: out_of_word_range=8`; `P2: distinct_quotes=1 distinct_lines=1`; `P3: unparsed_rows=1` |
| P4 verbatim | — (**M1**) | `P4 DEFECT … test_outputs.py:14: quote not verbatim there` |
| P5 captures | — (**M3**) | `P5 DEFECT … manifest digest does not match the bytes` |
| P6 sources | **P4**, **P7** | `P6 DEFECT rows=3 bad=4 first=S105: teaches words=1` |
| P7 provenance | — (**M2** partially, see limits) | `P7 ok source_lines=3 bad=0` |
| P8 readme | — | `P8 ok index_rows=42 knowledge_files=42` |
| P9 clean tree | **P6**, **P7** | `P9 DEFECT untracked=1 first=plans/round35_scratch.py` |
| P10 rerun | — (**M4**) | `P10 DEFECT fresh probe output is not byte-equal to the receipt` |
| D4 patterns | **L2**, **L3** | `L2: failed=['pattern1','pattern2']`; `L3: failed=['pattern2']` |
| D5 directional+digest | **L5**, **L6** | `L5: missing 'is present', carries 'not present'`; `L6: digest_pinned=False` |

The frozen battery exercises 7 of the 12 clauses (P1 P3 P6 P9 D4 D5, plus P0's acceptance of all ten). P2, P4,
P5, P7, P8 and P10 have no junk fixture of their own — recorded as calibration data, not repaired into the
frozen battery.

## First falsifiers run this wave (not part of the frozen battery)

Built on `copy_package()` + a fresh `git init` per probe, gate run as the battery runs it:

| probe | mutation | observed |
|---|---|---|
| M1 | one quote's citation moved to `test_outputs.py:14` | `P4 DEFECT … quote not verbatim there`, rc=1 |
| M2 | the S106 registry row duplicated | `P6 DEFECT rows=3 bad=1 first=S106: rows=2`, rc=1 |
| M3 | one byte appended to `test_outputs.py`, manifest untouched | `P5 DEFECT … manifest digest does not match the bytes`, rc=1 |
| M4 | a line appended to the receipt, run with `--rerun` | `P2 DEFECT` + `P10 DEFECT`, rc=1 |
| M5 | stray untracked file, gate **without** `--require-clean-tree` | accepted, rc=0 — the flag is what decides P9, not file content |
| M6 | a 26-word quote (upper bound) | `P3 DEFECT … out_of_word_range=1` (+P4), rc=1 |

## Limits (named, not repaired)

1. **The 3..25 upper bound is unreachable by a genuine row of this package.** The longest lines in the
   captures are 16 (`test_outputs.py`), 17 (`test.sh`) and 20 (`instruction.md`) whitespace words, so no
   verbatim single-line quote can exceed 25 words; M6 had to use a non-verbatim quote, which trips P4 as well.
   The frozen battery exercises only the lower bound (P1).
2. **P7 and P8 have no battery fixture.** Their behaviour is observed only as acceptance on P0/L-fixtures
   (`source_lines=3`, `index_rows=42 knowledge_files=42`). A wave-2 mutant that adds a provenance or index
   defect is the first real test of those two clauses.
3. **P5's manifest coverage is per direct file.** Files inside a capture *subdirectory* are covered only if a
   spec row or a quote cites them; the current spec's capture dir is flat.
4. **P10 depends on a runtime that has Biopython.** Without the host module it shells out to `uv run … --with
   biopython==1.85` (the round-35 counter's own fallback). If both are absent the clause is a `DEFECT`
   (`probe could not be re-run`), never a crash — but a red P10 could then mean "toolchain absent", which the
   reason string distinguishes.
5. **Not tested here:** symlinked captures, a `## Located quotes` section appearing twice, and a README index
   that lists a knowledge file twice under different case (`knowledge files == index rows` compares basenames).

## Hand-off to L1

1. Commit the gate as `plans/pkg_gate.py` (byte-identical: sha256 `ea6388…edd41`, 398 lines). That alone turns
   R35-D1's `tip_package_rc` green.
2. Two `--rerun` details the row depends on: `import Bio` in the host interpreter, else `uv` on PATH with
   biopython 1.85 cached.
3. Run the frozen predicate in a fresh clean clone of the landing tip; P0 and L1/L4 are the false-red guards, so
   do not "fix" a red P0 by loosening a clause.

No tools were installed or upgraded (nothing needed; uv was already present and used only as the probe runner).

VERDICT: gateB-false_green-0-false_red-0-unevaluated-0
