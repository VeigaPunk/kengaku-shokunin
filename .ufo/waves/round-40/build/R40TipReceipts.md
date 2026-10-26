# R40TipReceipts — `plans/tip_receipts.py` re-runs the round-39 and round-40 receipts

Round-39 closure routed item R4 / `F39TipReceipts` (`corpus/lessons/round-39-verifier-spotcheck.md:137`):
"`tip_receipts.py` skipping the new receipt". Tip measured: `3077adbc7145726519f60f01426a5d03381ad444`.
Scratch `/fast/scratch/hyaku/kengaku-r40/R40TipReceipts` (removed at the end); the lane was only ever read —
`git -C $S/lane status --porcelain | wc -l` → `0`.

## 1. Root cause

`RECEIPTS` (`plans/tip_receipts.py:53-59`) is a hand-written census of five round-35..38 receipts. A committed
`corpus/evidence/**/probe*.{txt,log}` file absent from it is printed as
`skip reason=no-committed-re-run-command` and never compared — although the probe script that produced it is
committed and its docstring carries the `Run as:` line `usage_argv()` already knows how to read. So every round
that lands a probe receipt adds a receipt nobody re-runs, and `--only <round>` reports success having compared
nothing (red-before, §3).

## 2. Fix — `.ufo/waves/round-40/build/R40TipReceipts/tip_receipts.py`

sha256 `e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3` (original
`f2a35b47d9e4d2ce3ec981dbb07a5c968d61d41c207ee32ecef4b9ea1932bcdd`). Full diff: `R40TipReceipts/diff-source.txt`
(4 hunks, no line of the comparator, control, masking, provenance or exit-code logic touched).

1. **`derive_map()`** (`:78-101`) resolves an unmapped candidate by name: receipt stem `git-leak-probe` and
   script stem `plans/git_leak_probe.py` are the same token once non-alphanumerics are dropped and case is
   folded (`STEM_RE = [^a-z0-9]+`). Only a **unique** match to a committed `plans/*.py` at HEAD is accepted, and
   the derived kind is the strict `byte`. `RECEIPTS` stays the override table (it wins, and it remains the only
   place a `temp-paths` kind is declared). This is the recurrence half of the fix: round 41's receipt needs no
   table edit.
2. `main()` builds one `plan = table + derived` and uses it for `--list`, the run loop and the counters;
   `--list` gained `origin=table|derived` so an inferred mapping is visible, never silent.
3. `note ... no_command=` now counts unmapped receipts **plus** mapped receipts skipped for
   `no-committed-re-run-command*` (it was `len(unmapped)` only). On this tip both formulas give `19` for the old
   receipts; the change only keeps the count honest once derivation can produce a commandless skip.
4. Docstring: the population paragraph describes the derivation and corrects a pre-existing drift — it promised
   one `boundary` line, the code has always printed one `skip reason=…` line per unmapped receipt.

The two named receipts resolve as:

```
receipt corpus/evidence/round39/git-leak-probe.txt kind=byte script=plans/git_leak_probe.py origin=derived provenance=SKILL.md:587+SKILL.md:876
receipt corpus/evidence/round40/db-wal-probe.txt kind=byte script=plans/db_wal_probe.py origin=derived provenance=plans/db_wal_probe.py:4+plans/pkg-spec-r40.json:5
```

## 3. Red-before (committed tool, clean `--shared` clone at `3077adbc`)

Command, cwd `$S/lane`: `python3 plans/tip_receipts.py --lane . --only round39 --work "$S/w-red39"`
(`R40TipReceipts/out-red-only-round39.txt`, `out-red-only-round40.txt`, `out-red-list.txt`):

```
tip 3077adbc7145726519f60f01426a5d03381ad444
receipt corpus/evidence/round39/git-leak-probe.txt skip reason=no-committed-re-run-command
note compared=0 declared_bounded=0 no_command=1
receipts=1 byte_equal=0 differ=0 skipped=1
rc=0
```

`--only round40` is the same three lines with `round40/db-wal-probe.txt`, `rc=0`: **skip, and exit 0 having
compared nothing**. `--list` shows both on the unmapped path; the 19 `probe-r19-*.log` receipts are unchanged.

## 4. Green-after (fixed copy, same clone, same tip)

`python3 <fixed> --lane . --only round39 --work "$S/w-green39"` (`out-green-only-round39.txt`):

```
tip 3077adbc7145726519f60f01426a5d03381ad444
receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0 doc=SKILL.md:587+SKILL.md:876
control receipt=corpus/evidence/round39/git-leak-probe.txt flip=byte 2933 0x65->0x64 verdict=differ
note compared=1 declared_bounded=0 no_command=0
receipts=1 byte_equal=1 differ=0 skipped=0
rc=0
```

`--only round40` (`out-green-only-round40.txt`):

```
receipt corpus/evidence/round40/db-wal-probe.txt equal bytes=8257 exit=0 doc=plans/db_wal_probe.py:4+plans/pkg-spec-r40.json:5
control receipt=corpus/evidence/round40/db-wal-probe.txt flip=byte 4128 0x72->0x73 verdict=differ
note compared=1 declared_bounded=0 no_command=0
receipts=1 byte_equal=1 differ=0 skipped=0
rc=0
```

Explicit `--tamper` on each new receipt (`out-green-tamper-round39.txt`, `out-green-tamper-round40.txt`) prints
the same receipt line and `control ... verdict=differ`, `rc=0`: the comparator is not vacuous on the derived
pair, and `--tamper` accepts a derived receipt (the `unknown` check is against `results`, which now holds it).

## 5. No previously-equal receipt changes status

Both tools run whole on the same clone/tip (`--jobs 6`), then the verdict lines are sorted and diffed
(`out-red-full-old.txt`, `out-green-full-new.txt`, `diff-full-ab.txt`):

```
$ diff -u <(grep -E '^(receipt|control|note|receipts=)' out-red-full-old.txt | sort) \
          <(grep -E '^(receipt|control|note|receipts=)' out-green-full-new.txt | sort)
-note compared=4 declared_bounded=1 no_command=21
+note compared=6 declared_bounded=1 no_command=19
-receipt corpus/evidence/round39/git-leak-probe.txt skip reason=no-committed-re-run-command
-receipt corpus/evidence/round40/db-wal-probe.txt skip reason=no-committed-re-run-command
-receipts=26 byte_equal=4 differ=0 skipped=22
+receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0 doc=SKILL.md:587+SKILL.md:876
+receipt corpus/evidence/round40/db-wal-probe.txt equal bytes=8257 exit=0 doc=plans/db_wal_probe.py:4+plans/pkg-spec-r40.json:5
+receipts=26 byte_equal=6 differ=0 skipped=20
```

Nothing else in the diff: the four `equal` receipts keep their exact byte counts (`3399`, `5907`, `8529`,
`5537`), `regex-log-probe-first-run.txt` keeps its declared-bounded skip, the automatic control keeps
`receipt=…round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ`, and both runs exit 0.

## 6. Derivation semantics — negative controls (fixture repo, not the lane)

`$S/fixture` (`git init` + one commit, `out-green-fixture-derivation.txt`): `plans/gamma_probe.py` with a
`Run as:` line, `plans/alpha_probe.py` **and** `plans/alpha-probe.py` (stem collision), receipts
`gamma-probe.txt`, `gamma-probe-first-run.txt`, `alpha-probe.txt`, `probe-r19-legacy.log`:

```
receipt corpus/evidence/r41/gamma-probe.txt kind=byte script=plans/gamma_probe.py origin=derived provenance=command=plans/gamma_probe.py:4,receipt=undocumented
receipt corpus/evidence/r41/alpha-probe.txt skip reason=no-committed-re-run-command
receipt corpus/evidence/r41/gamma-probe-first-run.txt skip reason=no-committed-re-run-command
receipt corpus/evidence/r41/probe-r19-legacy.log skip reason=no-committed-re-run-command
--- run ---
receipt corpus/evidence/r41/gamma-probe.txt equal bytes=14 exit=0 doc=command=plans/gamma_probe.py:4,receipt=undocumented
control receipt=corpus/evidence/r41/gamma-probe.txt flip=byte 7 0x61->0x60 verdict=differ
receipts=4 byte_equal=1 differ=0 skipped=3
```

So the rule is exact-stem and unique-match: a `-first-run` sibling does **not** inherit the mapping by prefix,
an ambiguous stem resolves to nothing, and a legacy log stays unmapped. Real-data confirmation that the rule
adds no false positive: `--list` on the lane maps 7 of 26 candidates, the same 19 `probe-r19-*` logs stay
unmapped, and `regex-log-probe-first-run.txt` keeps `kind=temp-paths origin=table`.

## 7. Integration for the L1

- Land `R40TipReceipts/tip_receipts.py` over `plans/tip_receipts.py` (nothing else moves; no `RECEIPTS` row was
  added for round 39/40 — the mapping is the derivation, so it is exercised by the very receipts it fixes).
- `SKILL.md:586` registry row needs no edit: same command, same verdict map, same population, same scratch
  contract. The only output change is the added `origin=` field on `--list` mapped lines.
- Suggested registry self-test receipt for the row: `R40TipReceipts/out-green-full-new.txt`
  (`receipts=26 byte_equal=6 differ=0 skipped=20`, control `differ`, rc 0).

## 8. Risks and limits

- The derivation is name-based. A receipt whose stem does not match its script (`probe-r19-*`, `-first-run`)
  still needs a table row; that is deliberate (prefix matching would silently bind `*-first-run` to a script
  whose receipt is declared non-reproducible) and is visible as a `skip` line.
- A derived receipt whose script has no parseable `Run as:` and no `FALLBACK` entry becomes a mapped `skip
  reason=no-committed-re-run-command:no-command`, still exit 0. That is the registry row's declared contract
  ("with a committed re-run command"), not a change here; no such script exists at this tip.
- `--only` selecting only skips still exits 0 (unchanged, by the same contract). It is how the round-39 skip
  went unnoticed; if the lane wants that to fail, it is a separate decision for a later round — I did not
  change an exit code the frozen registry row spells out.
- Measured on host git 2.56.0, python3 3.x, bwrap and sqlite3 3.54.0; both probes ran green here, but this seat
  ran no build/lint/test gate (parent owns post-integration gates).

No tool was installed or upgraded for this seat.

## Evidence index (`R40TipReceipts/`)

| file | sha256 | what |
|---|---|---|
| `tip_receipts.py` | `e4f49714…f88f3` | the fixed copy (18 778 B) |
| `diff-source.txt` | `5161c04f…288bb7` | `diff -u plans/tip_receipts.py <fixed>` |
| `out-red-list.txt` | `39df07ec…94f8c5` | committed tool `--list` (both receipts unmapped) |
| `out-red-only-round39.txt` / `…round40.txt` | `8a11375b…` / `7d5fd241…` | red-before: `skip`, `compared=0`, rc 0 |
| `out-green-only-round39.txt` / `…round40.txt` | `a48ac47e…` / `3d76b67b…` | green: `equal`, control `differ`, rc 0 |
| `out-green-tamper-round39.txt` / `…round40.txt` | `a48ac47e…` / `3d76b67b…` | explicit `--tamper` on each new receipt |
| `out-red-full-old.txt` / `out-green-full-new.txt` | `3b94fcf9…` / `d492f40a…` | whole-lane A/B (26 receipts) |
| `diff-full-ab.txt` | `034a60c5…16b5d` | sorted verdict-line diff: only the two receipts + counters move |
| `out-green-fixture-derivation.txt` | `fdb4be2d…3476` | derivation negative controls (collision, `-first-run`, legacy) |

VERDICT: tip-receipts-r39-equal-r40-equal
