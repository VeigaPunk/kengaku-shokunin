# R36GateD — C1 gate candidate (round 36, wave 1)

Deliverable (candidate for `plans/pkg_gate.py`; the L1 integrates):

```
ce0fdca26fef040f375bd86d0be585bd8d5bebc24afe8073041c8fe291b2a0b4  .ufo/waves/round-36/build/R36GateD/pkg_gate.py
400 lines, Python 3 stdlib only, no network (interpreter fallback is `uv run --offline`)
```

No lane file was written; the only artifacts are this report and the gate under
`.ufo/waves/round-36/build/R36GateD/`. No tool installs this wave (the host already ships `uv`; the
rerun path used the cached `biopython==1.85` wheel offline).

## Contract implemented

```
pkg_gate.py package --root DIR --spec SPEC [--require-clean-tree] [--rerun]
pkg_gate.py d4-line --file F --spec SPEC
pkg_gate.py d5-line --file F --capture-dir D --spec SPEC
pkg_gate.py --selftest
```

One `P<n> ok|DEFECT <reason>` line per package check (`P<n> skip flag-absent` for an optional check
that is off), then `defects=<n>`. Line modes print one `D4|D5 ok|DEFECT <reason>` then
`defects=<n>`. Exit 0 accept / 1 reject / 2 usage-setup; a parse exception inside a check is a
DEFECT line and exit 1; unreadable spec, absent `--file`/`--capture-dir`/`--root` and unknown
subcommands exit 2. Nothing recognises a fixture by name, path or marker string: every threshold and
pin is read from the spec JSON (`entry_rules`, `rows`, `frozen_instruments`, `receipt_sha256`,
`d4.patterns`, `d5.*`).

| check | clause (spec-driven) |
|---|---|
| P1 | every `frozen_instruments` file exists at its pinned sha256 (non-empty pin set) |
| P2 | `capture_dir/SHA256SUMS`: every listed digest equals the file bytes; every `rows` capture listed at its pinned sha256 |
| P3 | receipt sha256 equals the pin |
| P4 | one SOURCES row per spec row id, 11 cells, tier/status/opened from `entry_rules`, URL `raw_base+upstream`, used-by = entry, teaches >= `min_teaches_words`, teaches pairwise distinct |
| P5 | `source: <id> ` line per row in spec order carrying its pinned URL, then `verified-at`, then `recheck:` date/cadence |
| P6 | `## Negative space` section carrying a falsifier |
| P7 | `## Located quotes`: a `Quote`/`Location` header, then every data row parses; each quote within `quote_words` and verbatim on its cited capture lines; >= `min_quotes` distinct quotes at >= `min_distinct_locations` distinct lines |
| P8 | readme: exactly one index row for the entry citing every row id + a `## Coverage map` bullet |
| P9 | knowledge files (`git ls-files` of `knowledge_glob`) == readme index rows |
| P10 | `--require-clean-tree`: `git -C ROOT ls-files --others --exclude-standard` empty |
| P11 | `--rerun`: probe command re-runs in ROOT, exit 0, stdout byte-equal to the receipt (pin read from the receipt's `biopython=` line, run through `uv --offline`) |
| D4 | exactly one line with `d4.label`, and every `d4.patterns` regex matches it (directional: each citation is followed by its own token) |
| D5 | exactly one line with `d5.label`; `forbid` absent; the `require` phrase sits **before** the cited capture in the same sentence (not bare co-occurrence); capture digest pinned by the manifest; every manifest entry matches; the spec quote occurs in the capture |

The extra D5 sentence-binding was added after a self-attack showed the plain token test accepted
`Erratum (round 35): x is present` against the real captures (`rc=0`); with binding that line is
`D5 DEFECT require phrase not bound to the cited capture` (`rc=1`).

## Proof — frozen battery (fixture clone per the fixture rule)

```
D=$(mktemp -d /tmp/k36-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans /SCORECARD.md \
    /.ufo/waves/round-34/assimilation /.ufo/waves/round-34/build
git -C "$D/lane" checkout -q master          # top == $D/lane (verified)
cp plans/{regex_log_probe.py,round36_c1_verify.py,round36_c2_verify.py,pkg-spec-r35.json} "$D/lane/plans/"
cp corpus/defects-round35.jsonl "$D/lane/corpus/"; cp -r corpus/evidence/round36/. "$D/lane/corpus/evidence/round36/"
cp <gate> "$D/lane/plans/pkg_gate.py"; git -C "$D/lane" add -A   # index only, no commit
PYTHONDONTWRITEBYTECODE=1 python3 plans/round36_c1_verify.py --lane "$D/lane"
```

Full output (exit 1, as expected while the four ledger rows are still `open`):

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
R35-D1 status=open observed=pass agree=NO fixtures=14 false_green=0 false_red=0 unevaluated=0 tip_package_rc=0
R35-D2 status=open observed=pass agree=NO untracked_anywhere=0 line_fixtures_wrong=0/6
R35-D3 status=open observed=fail agree=yes committed_nested_wave_paths=21
R35-D4 status=open observed=fail agree=yes round-36 lesson absent; recount 13 + 23 + 1 = 37 vs stated denominator 38
rows=4 closed=0 observed_pass=2 mismatches=2
PREDICATE C1 fail
C1_VERIFY_RC=1
```

`FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` is the wave-1 target and holds. The
ledger half is integration work outside the gate:

- R35-D1 and R35-D2 now observe **pass** in a clean clone (`tip_package_rc=0`,
  `untracked_anywhere=0 line_fixtures_wrong=0/6`); they read `mismatches=2` only because
  `corpus/defects-round35.jsonl` still says `open` — the L1 flips `status`/`closed_round`.
- R35-D3 is red on committed state (`committed_nested_wave_paths=21`, the round-34 scratch mirrors);
  no gate clause can see that, the lane paths must go.
- R35-D4 is red because `corpus/lessons/round-36.md` does not exist yet; its check is the lesson's
  `Erratum (round 36):` line, not a gate clause.

## Which clause kills which fixture (observed, not designed)

Built the same 14 fixtures via the counter's own `build_package_fixtures` /
`build_line_fixtures` and ran the gate on each, printing the first DEFECT line:

| fixture | rc | first defect |
|---|---|---|
| P0 genuine | 0 | ACCEPTED |
| P1 8 one-word quotes | 1 | `P7 DEFECT quote has 1 words (want 3..25): 'gblock_path'` |
| P2 8 copies of one quote | 1 | `P7 DEFECT distinct quotes=1 locations=1 below 8/8` |
| P3 unparsed quote row | 1 | `P7 DEFECT unparsed quote rows=1: '\| a claim \| "straight quotes row" \| `test_outputs.py:13` \|'` |
| P4 junk teaches | 1 | `P4 DEFECT S105 teaches has 1 words` |
| P5 stub probe | 1 | `P1 DEFECT instruments=3 mismatched=['plans/tb2_grader_probe.py']` |
| P6 untracked leftover | 1 | `P10 DEFECT untracked=1: plans/round35_scratch.py` |
| P7 cheapest all-junk | 1 | 4 defects, first `P1 … tb2_grader_probe.py` (also P4/P7/P10) |
| L1 genuine D4 | 0 | ACCEPTED |
| L2 D4 citations swapped | 1 | `D4 DEFECT pattern_1_absent` |
| L3 D4 harness token missing | 1 | `D4 DEFECT pattern_2_absent` |
| L4 genuine D5 | 0 | ACCEPTED |
| L5 D5 "not present" | 1 | `D5 DEFECT forbid 'not present' present` |
| L6 altered capture | 1 | `D5 DEFECT capture digest not pinned by quarantine-SHA256SUMS` |

Note P5/P7: the stub probe is killed by the frozen-instrument pin (P1), not by `--rerun` — a stub
that prints the receipt byte-for-byte passes a bare rerun, which is exactly why that pin exists.

## Real lane (working tree, no `--require-clean-tree`; the lane holds untracked wave files)

```
python3 .ufo/waves/round-36/build/R36GateD/pkg_gate.py package \
  --root /home/vgpnk/Projects/shokunin/kengaku-shokunin --rerun \
  --spec /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/pkg-spec-r35.json
```

```
P1 ok instruments=3 mismatched=0
P2 ok listed=6 pinned_rows=3
P3 ok receipt_sha256=2359d9067906f59d matched=True
P4 ok rows=3 min_teaches=23
P5 ok source_lines=3 verified_at=2026-10-25
P6 ok falsifier=True
P7 ok rows=22 quotes=22 locations=22
P8 ok index_rows=1 cites=3 coverage=yes
P9 ok knowledge_files=42 index_rows=42
P10 skip flag-absent
P11 ok probe=uv stdout=byte_equal
defects=0
REAL_LANE_RC=0
```

`--rerun` reproduced `corpus/evidence/round35/tb2-grader-probe.txt` byte-for-byte on the real lane
through `uv run --offline --no-project --with biopython==1.85` (host `python3` has no `Bio`).

## Selftest and exit-code matrix

`python3 <gate> --selftest` builds three tiny fixtures in a temp dir (git init + index add, no lane
bytes) and asserts the exit codes:

```
SELFTEST pass=0 one-word=1 unparsed=1        (rc=0)
```

Each selftest run prints its own P lines; `pass` is `defects=0`, `one-word` is
`P7 DEFECT quote has 1 words`, `unparsed` is `P7 DEFECT unparsed quote rows=1`.

Contract checks on the fixture clone (`set +e` wrapper; every line is the gate's last stdout line):

| invocation | rc |
|---|---|
| no subcommand | 2 (`usage: …`) |
| `package --spec /nope.json` | 2 (`P0 DEFECT spec unusable`) |
| `d5-line --capture-dir /nope` | 2 (`P0 DEFECT capture dir absent`) |
| `d4-line --file /nope.md` | 2 (`P0 DEFECT file absent`) |
| `package --root /nope` | 2 (`P0 DEFECT root is not a directory`) |
| `d5-line` on two labelled lines | 1 (`defects=1`) |
| `d5-line` on the real captures with a line that only says `x is present` | 1 (`require phrase not bound to the cited capture`) |

## Residual limits (reported, not repaired into the frozen battery)

1. P4 counts words: eight repeats of one nonsense word pass the teaches test; only pairwise
   distinctness and length are enforced, not sense.
2. P9 is count parity: deleting a knowledge file together with its index row keeps parity. The
   frozen C1 sentence is "knowledge files == index rows", not a floor.
3. P2 does not forbid unlisted files in the capture dir (a third file there is invisible unless it
   is listed); the pinned rows and listed digests are what it enforces.
4. D4/D5 are textual over one labelled line. D5 binds the assertion to the cited capture in the
   same sentence and pins the capture digest, but a line that asserts presence in the capture while
   describing a different quote than `d5.quote` would still pass; the spec has no per-line content
   pin.
5. P11 needs the `uv` offline cache for `biopython==1.85`; without it the rerun is a DEFECT (a
   rejection, never an accept). Host `python3` alone cannot run the probe.
6. The battery's P6 is only killed by `--require-clean-tree`; the r35-D1 ledger invocation is the
   only place that flag is exercised, and it reads the whole lane, so any untracked file anywhere in
   a lane reds it by design (D1 class).

VERDICT: gateD-false_green-0-false_red-0-unevaluated-0
