# R37BatP23 — C1 battery module for M02, M03, M04, M06, M07, M08

Seat: executor (leaf), round 37 wave 1. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Gate under test: `plans/pkg_gate.py`, sha256 `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`
(its freeze digest; `sha256sum plans/pkg_gate.py`). Nothing frozen was touched: gate, counters, probe,
mutant list, spec and lane bytes are unmodified; my only lane writes are this report and
`.ufo/waves/round-37/build/R37BatP23/`.

## Deliverable

`.ufo/waves/round-37/build/R37BatP23/battery/p23.py` — stdlib only (imports nothing), fid prefix `p23-`,
six single-defect fixtures built from the genuine round-35 package via `ctx.genuine_package` + index-only
`ctx.git_add`. L1 integrates by copying the file to `plans/battery37/p23.py` unchanged.

sha256:
```
518340e4d6403b396abd6d871722f6cfa76001a77c5b033bd5702a0bbd399990  p23.py
```
(`sha256sum .ufo/waves/round-37/build/R37BatP23/battery/p23.py`; receipt `receipts/module-sha256.txt`.)

| fid | mutant | branch silenced | one change | declared DEFECT set |
|---|---|---|---|---|
| `p23-p2-receipt-deleted` | M02 | P2 `got is None` return False→True | receipt file deleted, deletion staged | P2 |
| `p23-p2-receipt-byte` | M03 | P2 `return got == want`→True | byte 0 of the receipt changed | P2 |
| `p23-p3-heading-renamed` | M04 | P3 `no '## Located quotes' section` | heading renamed to `## Quotes, located` | P3, P4 |
| `p23-p3-seven-texts` | M06 | P3 `len(texts) >= min_quotes` | 8 rows, 7 distinct texts, 8 distinct lines | P3 |
| `p23-p3-seven-locations` | M07 | P3 `len(locs) >= min_distinct_locations` | 8 distinct texts on 7 distinct (capture,line) | P3 |
| `p23-p3-two-word-quote` | M08 | P3 `and not short` | genuine `test_outputs.py:27` quote cut to two words | P3 |

Construction notes (why each stays single-defect):

- **M02/M03.** P1 pins only the three frozen instruments, P8's coverage bullet matches the receipt *path*
  text, so the receipt's bytes/absence reach P2 alone. Both stage the change (`git add -A`), so P9 stays
  `untracked=0`. `--require-clean-tree` is passed, `--rerun` is not (P10 is a different clause).
- **M06.** The genuine row `“assert 15 <= gc <= 35, (”` cites `test_outputs.py:71`; the same text is
  verbatim on `test_outputs.py:66` (line 66 is `    assert 15 <= gc <= 35, (`). A copy of that row
  re-cited at `:66` gives 8 rows / 7 distinct texts / 8 distinct lines, and P4 stays green
  (`checked=8 bad=0`), so only the `min_quotes` conjunct fires.
- **M07.** Two *different* texts are both verbatim on `test_outputs.py:23`: the whole genuine line and its
  first five words (`assert len(gblock) <= 3000,`). 7 genuine rows at 7 distinct lines + that second text at
  `:23` gives 8 distinct texts on 7 distinct locations; P4 green, only `min_distinct_locations` fires.
- **M08.** Cut row 6 (`test_outputs.py:27`, `gblock_aa = str(Seq(gblock).translate())`) to its first two
  words `gblock_aa =`, which is still verbatim there: 22 distinct texts and 22 distinct lines are
  untouched, only `out_of_word_range` moves 0→1. (Same technique as the pre-freeze API example, on a
  different row; the example module is not in my battery dir.)
- **M04 (the one two-clause fixture).** Renaming the heading makes `Package._parse_quotes` return before
  any row is parsed, so `p.quotes` is empty and P4's `if not p.quotes: return False, "no parsed quote"`
  fires. There is no construction that silences P3's "no section" branch while keeping quotes parsed,
  because parsing is keyed on that exact heading; the second clause is therefore unavoidable and declared.
  M04 is still killed on the observable result: `(1, {P3,P4})` → `(1, {P4})`.

## Acceptance run (exact command, full output)

```
$ S=/fast/scratch/hyaku/kengaku-r37/R37BatP23   # TMPDIR=$S
$ python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c1_verify.py \
    --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatP23/battery \
    --only M02,M03,M04,M06,M07,M08 --work "$S"
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE p23-p2-receipt-deleted expect=reject declared=P2 observed_rc=1 observed_defects=P2 ok
FIXTURE p23-p2-receipt-byte expect=reject declared=P2 observed_rc=1 observed_defects=P2 ok
FIXTURE p23-p3-heading-renamed expect=reject declared=P3,P4 observed_rc=1 observed_defects=P3,P4 ok
FIXTURE p23-p3-seven-texts expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p23-p3-seven-locations expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE p23-p3-two-word-quote expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
BATTERY fixtures=20 wrong=0 renamed_disagree=0
MUTANT M02 P2 killed by=p23-p2-receipt-deleted -- receipt unreadable
MUTANT M03 P2 killed by=p23-p2-receipt-byte -- receipt digest differs from the pin
MUTANT M04 P3 killed by=p23-p3-heading-renamed -- no Located quotes section
MUTANT M06 P3 killed by=p23-p3-seven-texts -- fewer distinct quotes than min_quotes
MUTANT M07 P3 killed by=p23-p3-seven-locations -- fewer distinct located lines than min_distinct_locations
MUTANT M08 P3 killed by=p23-p3-two-word-quote -- a quote outside the word range
MUTANTS total=6 killed=6 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```
(Receipt: `receipts/dev-run.txt`. A second run of the same command is byte-equal — `cmp` printed
`SECOND-RUN-BYTE-EQUAL` — so the module is deterministic. `python3 -m py_compile …/p23.py` → `COMPILE-OK`.)

All six `FIXTURE` lines for my module end `ok`; `wrong=0`, `renamed_disagree=0` (the counter re-runs every
fixture under a random other directory name), `null_detected=0`; each of my mutants is `killed by=` my own
fid. The renamed run also shows the gate keys on no fixture name: the fixtures are built by byte edits to
the genuine package, never by a marker string.

## Load-bearing check (delete one fixture at a time)

Each variant is a scratch copy of `p23.py` with exactly the one `FIXTURES` line for that fid removed
(`grep -v '"fid": "<fid>"'`), run with `--battery-dir <variant> --only <mutant>`. Full receipt:
`receipts/load-bearing.txt`.

| variant (fixture removed) | fixture count | mutant under test | result |
|---|---|---|---|
| `p23-p2-receipt-deleted` | 19 | M02 | `MUTANT M02 P2 SURVIVED`, `survived=1` |
| `p23-p2-receipt-byte` | 19 | M03 | `MUTANT M03 P2 SURVIVED`, `survived=1` |
| `p23-p3-heading-renamed` | 19 | M04 | `MUTANT M04 P3 SURVIVED`, `survived=1` |
| `p23-p3-seven-texts` | 19 | M06 | `MUTANT M06 P3 SURVIVED`, `survived=1` |
| `p23-p3-seven-locations` | 19 | M07 | `MUTANT M07 P3 SURVIVED`, `survived=1` |
| `p23-p3-two-word-quote` | 19 | M08 | `MUTANT M08 P3 SURVIVED`, `survived=1` |

Every removal flips exactly its own mutant to SURVIVED and no other fixture's declaration changes
(`wrong=0 renamed_disagree=0` in all six variants). So each fixture is load-bearing for exactly one mutant,
and no fixture of mine kills a mutant other than its own (checked in the other direction too: with the full
module the six kills are attributed one-to-one above).

## Clause-level evidence (unmodified gate, per fixture)

Full stdout: `receipts/full-gate-output.txt`; clause notes: `receipts/gate-clause-notes.txt`. Excerpts
(`python3 plans/pkg_gate.py package --root <fx> --require-clean-tree --spec plans/pkg-spec-r35.json`):

```
p23-p2-receipt-deleted      P2 DEFECT receipt unreadable: corpus/evidence/round35/tb2-grader-probe.txt   defects=1
p23-p2-receipt-byte         P2 DEFECT receipt_sha256=fd3829017c42bb6ad75bc93ac1b06336517c19249f62ec565eb9e3f10fde8850   defects=1
p23-p3-heading-renamed      P3 DEFECT no '## Located quotes' section / P4 DEFECT no parsed quote   defects=2
p23-p3-seven-texts          P3 DEFECT rows=8 distinct_quotes=7 distinct_lines=8 out_of_word_range=0   defects=1
p23-p3-seven-locations      P3 DEFECT rows=8 distinct_quotes=8 distinct_lines=7 out_of_word_range=0   defects=1
p23-p3-two-word-quote       P3 DEFECT rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=1   defects=1
```
All other clauses (P1, P5–P9; P4 where declared ok) print `ok` in those runs, e.g. for `seven-texts`:
`P4 ok checked=8 bad=0 first=0`, `P5 ok manifest_entries=6 bad=0 first=0`,
`P8 ok index_rows=43 knowledge_files=43 bad=0 first=0`, `P9 ok untracked=0 first=0`. The P3 notes are the
gate's own counters: they show the fixture moves exactly the intended conjunct (7 texts / 8 lines; 8 texts /
7 lines; 1 out-of-range quote) and nothing else.

## Integration notes for the L1

- Copy `.ufo/waves/round-37/build/R37BatP23/battery/p23.py` to `plans/battery37/p23.py`. No edits needed;
  fids are unique (`p23-…`), the module has no imports and no side effects at import time.
- Keep the file's byte content (the sha256 above) if you want the receipt to match.
- The module must not be renamed to a fixture-specific name; the counter's rename pass covers directory
  names, and the gate never reads the fixture's path, only the spec-relative paths inside it.

## Risks and limits

- **M04 declares two clauses.** P4 necessarily fires with P3 on this construction (reason above). If the
  integrator's convention requires one clause per fixture, this is the one exception; it cannot be avoided
  without a second, unfrozen gate change.
- **Observational demonstration.** As the freeze states, a fixture shows the branch is reached and its
  result is visible; it does not prove the branch's check is the right check. M03 changes byte 0 of the
  receipt (the receipt's first line), M08 changes one quote's word count; both are minimal, single-branch
  perturbations by construction, but they are perturbations of the genuine package, not independent junk.
- **P10 is never exercised** by my fixtures (`--rerun` is not passed), by design: a fresh probe run would
  add a second observable and blur the single-defect claim.
- **No dependency on uncommitted lane bytes** beyond what `ctx.genuine_package` already copies (the
  knowledge dir and README from the lane tree); this is the same source the frozen battery uses, so a
  half-landed C2 entry could still show up as a wrong declaration in C1 — the freeze names that as a C1/C2
  coupling, not a defect of this module.

## Operability / environment

- Scratch `S=/fast/scratch/hyaku/kengaku-r37/R37BatP23` (NVMe), `TMPDIR=$S`, `--work "$S"`; removed at the
  end (`ls` → `No such file or directory`, `SCRATCH-REMOVED`). Nothing under `/tmp`.
- No lane git/jj mutation; no `git add/commit/…` in the lane; fixture repos are temp dirs under `$S`.
- No tool installed or upgraded (nothing needed; python3 stdlib only). No pacman transaction.
- `git -C <lane> status --porcelain` after the work shows only other seats' untracked paths
  (`build.ready`, `claims/measure-before-committed.txt`, `integrate/`) plus my build dir — no lane file
  modified by me.
- No subagent, no background job; single seat.

VERDICT: battery-p23-killed-6/6-wrong-0
