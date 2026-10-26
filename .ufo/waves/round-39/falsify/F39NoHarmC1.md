# F39NoHarmC1 — no-harm on the earlier C1 instruments at lane tip `a6832f53`

Seat: wave-2 critic, round 39 (hyaku run 8, 2026-10-26). Lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
measured on a clean `git clone --no-local` at **`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`** (`git -C $S/lane rev-parse HEAD`
→ that sha; `--show-toplevel` → `$S/lane`). Scratch `S=/fast/scratch/hyaku/kengaku-r39/F39NoHarmC1`, removed at the end.
Python 3.14.8, git 2.56.0 (`receipts/commands.txt`). Lane HEAD at review time is `acf43754`; between the assigned tip and
HEAD only `.ufo/waves/round-39/falsify-dispatch.json` and `falsify-spec.json` were added (`receipts/protected-diff.txt`),
so measurements at the tip describe HEAD's lane bytes too.

## What was attacked

1. The protected round-36/37/38 instruments (`plans/battery37`, `plans/battery38`, `plans/round3[678]_c1_verify.py`,
   `plans/pkg_gate.py`, `plans/pkg-spec-r35.json`) versus the freeze `088f7c36`.
2. `plans/round37_c1_verify.py`'s landed `killed=55` and `plans/round38_c1_verify.py`'s landed `killed=21 survived=1`.
3. Whether round-39 corpus edits changed bytes the round-36..38 batteries *copy* into their fixtures, and whether that
   changed any measured verdict.

## F1 — protected instruments untouched (both sides)

```
$ git -C <lane> diff --stat 088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8 a6832f53c1a94bb092a6cfd79fb4e449f2d4054c \
    -- plans/battery37 plans/battery38 plans/round3[678]_c1_verify.py plans/pkg_gate.py plans/pkg-spec-r35.json
(no output; exit 0)
```
Same command with `a6832f53..acf43754` → also empty. Receipt: `receipts/protected-diff.txt`.
No harm on axis **provenance/identity** of the instruments: no byte of the frozen battery modules, counters, gate or
round-35 spec moved since the claims freeze.

## F2 — round-37 counter at the tip: `killed=55`, pass

```
$ python3 plans/round37_c1_verify.py --lane . --work $S/w1      # clean clone at a6832f53
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass                                                # exit 0
```
All 64 fixture lines `ok` (no accept/reject and no declared-DEFECT-set drift). Receipt: `receipts/r37-at-tip.txt`.
The required `killed=55` holds, and the gate digest still matches the frozen pin in the counter
(`GATE plans/pkg_gate.py sha256=frozen`).

## F3 — round-38 counter at the tip: `killed=21 survived=1` (its landed state), not a wave-2 regression

```
$ python3 plans/round38_c1_verify.py --lane . --work $S/w3      # clean clone at a6832f53
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
MUTANT N21 D5 silence SURVIVED -- the capture digest is looked up in every manifest row, not only the first [F37XMutD5 X3]
PREDICATE C1 fail                                                # exit 1
```
`killed=21 survived=1` is the landed number, and the fail line is the recorded honest stop, not new: the round-38 lesson
says `the round reports C1 as an honest stop` (`corpus/lessons/round-38.md:70`), and its line 35 records that N21's
frozen `killed=22` `was unreachable by any battery`. Its 14 pins re-hash clean at the tip (`mismatched=0`). Receipt:
`receipts/r38-at-tip.txt`.

## F4 — yes, round-39 changed copied bytes; measured effect is one P8 note count and no verdict

`plans/round36_c1_verify.py`'s `copy_package` copies the spec's entry, receipt, `corpus/SOURCES.md`, `corpus/README.md`,
the frozen instruments and the capture dir, and additionally **every** file matched by
`for p in (lane / "corpus/knowledge").glob("*.md")` (`plans/round36_c1_verify.py:64`) and the same for
`corpus/lessons` (`:67`). So the question premises a real coupling: the older batteries are corpus-live, not pinned.

Changed bytes in that copied set, `088f7c36..a6832f53` (`receipts/corpus-change-inventory.txt`):

| file | status | read by the batteries as |
|---|---|---|
| `corpus/README.md` | M, 4 hunks all `-N,0 +`, **0 removed lines**: 1 index row, 1 coverage bullet, a 16-line open-gap discharge, a 6-line evidence section | P8 content (`plans/pkg_gate.py:71`) |
| `corpus/SOURCES.md` | M, **0 removed lines** (`+S117`, `+S118`) | P6/P7 rows; `entry not in cells[10]` (`plans/pkg_gate.py:202`) |
| `corpus/knowledge/tb2-{build-pmars,git-webserver,regex-log}-grader.md` | M, append-only `## Errata (round 39)` | **not read** — gate reads content only at `spec["entry"]` (`:70`) |
| `corpus/knowledge/tb2-git-leak-recovery-grader.md` | **A** (new) | P8 **filename only**: `files = {f.name for f in p.root.glob(p.spec["knowledge_glob"])}` (`:252`) |
| `corpus/lessons/round-38.md` | M append; `round-39.md` **A** | copied, never read (D5's source is `corpus/lessons/round-34.md`, unchanged) |
| `SCORECARD.md` | M, +47 lines appended | D4's label line is extracted from it (`plans/round36_c1_verify.py:162`) |

Unchanged, verified: the spec entry `corpus/knowledge/tb2-protein-assembly-grader.md` (empty name-only diff), rows
**S105/S106/S107 byte-identical** (`diff` → `IDENTICAL`), the receipt, the `corpus/evidence/round35` capture dir, the
frozen instruments, `corpus/defects-round35.jsonl`, `corpus/evidence/round36`, `corpus/lessons/round-{34,36}.md`. The
mentions of `corpus/QUALITY.md` in both counters are docstring prose, not reads; no battery module reads it.

Direct measurement on the genuine round-35 package (built by `copy_package`, `git init` + `git add -A`, then
`python3 plans/pkg_gate.py package --root <fixture> --spec plans/pkg-spec-r35.json`), base vs tip:

```
$ diff gate-genuine-package-at-base.txt gate-genuine-package-at-tip.txt
8c8
< P8 ok index_rows=45 knowledge_files=45 bad=0 first=0
---
> P8 ok index_rows=46 knowledge_files=46 bad=0 first=0
```
Every other clause line is `ok` and the notes are identical, with `defects=0` and RC=0 on both sides
(`receipts/gate-genuine-package-at-{base,tip}.txt`, `receipts/diff-gate-base-vs-tip.txt`). Knowledge files 45→46 and
lessons 52→53; index rows 45→46. P9 and P10 are flag-gated (`plans/pkg_gate.py:307-308`), so this plain call prints
P1–P8 only; both were exercised by the counters through fixtures `r36-P6` (P9), `p910-*` (P10), `p10a-*` and `d5m-n21`,
every one `ok` on both base and tip.

Full counters on a clean clone of the claims freeze `088f7c36` (i.e. **before** the round-39 corpus bytes) versus the tip:

```
$ diff receipts/r37-at-base.txt receipts/r37-at-tip.txt   → diff_exit=0   (byte-identical, 10416 bytes each)
$ diff receipts/r38-at-base.txt receipts/r38-at-tip.txt   → diff_exit=0   (byte-identical, 11436 bytes each)
```
Base outputs: R37 `BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0
null_detected=0`, `PREDICATE C1 pass`; R38 `PINS total=14 mismatched=0`, `BATTERY fixtures=86 wrong=0
renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`, `PREDICATE C1
fail`. So across 150 fixture runs and 77 mutant runs the round-39 corpus edits changed nothing measurable: `wrong=0`,
`renamed_disagree=0`, `sidechannel=0`, `invalid=0`, `null_detected=0` on both sides.

## Counterexamples tried (the strongest available)

1. **The additive knowledge file without a matching README row** would red every accept fixture through P8's
   `knowledge files={len(files)} index rows={len(indexed)}` (`plans/pkg_gate.py:255`) — the one genuine coupling in the
   copied set. It is not violated: the row is present and the counts move together 45/45 → 46/46, `P8 ok` on both sides.
2. **SCORECARD.md +47 lines shifting D4 extraction.** D4 takes the *first* line starting with the frozen label
   (`plans/round36_c1_verify.py:162`). The label occurs exactly once in both commits and the extracted line is
   byte-identical → `D4 LINE IDENTICAL` (`receipts/corpus-change-inventory.txt`); `r36-L1` (D4 genuine) accepts on both.
3. **Appended errata acting as parsed gate input.** The three appended TB2 entries are never parsed: the gate reads
   content at `pkg.entry`/`pkg.readme` and enumerates knowledge filenames only
   (`plans/pkg_gate.py:70-71`, `:252`). Confirmed dynamically by the identical clause output above.
4. **SOURCES.md additions perturbing `used-by`/row checks**: the diff is pure append (0 removed lines), S105–S107 are
   byte-identical, and both counters' P6 lines are `ok rows=3 bad=0`.

## Tradeoff this does not remove (hazard, not a defect this round)

The older batteries rebuild their genuine package from the *current* corpus trees each run, so
`plans/battery37`/`battery38` fixtures now embed round-39 corpus state (knowledge 45→46, lessons 52→53). Consequences to
carry forward, not to fix here: (a) a future README↔knowledge inconsistency — for example removing the round-39 index row —
would surface as a failure of the **round-36..38** counters and be misattributed to the gate; (b) any saved receipt
quoting the gate's P8 note `index_rows=45 knowledge_files=45` is now stale. No committed text quotes that note: the only
committed counts are round-scoped (`SCORECARD.md:1405` records `knowledge 45/45 → 46/46`), and a grep over `corpus/`,
`plans/` and `SCORECARD.md` for `index_rows=`/`knowledge_files=` returns only historical census files with their own
values.

**Impacted axes:** calibration (r36/r37/r38 C1 counters) — held; provenance of fixture bytes — held, with the corpus-live
coupling above named. **Smallest safe correction:** none required for this round; if the lane ever wants the older
batteries pinned to frozen corpus bytes, the fix belongs in `pkg-spec-r35.json` (pin the knowledge/lessons file set), not
in this report's scope.

## Receipts

`receipts/protected-diff.txt`, `receipts/corpus-change-inventory.txt`, `receipts/r37-at-{tip,base}.txt`,
`receipts/r38-at-{tip,base}.txt`, `receipts/diff-r37-base-vs-tip.txt`, `receipts/diff-r38-base-vs-tip.txt`,
`receipts/gate-genuine-package-at-{base,tip}.txt`, `receipts/diff-gate-base-vs-tip.txt`, `receipts/commands.txt`.
No tracked lane file was written and no git write command was run in the lane; my writes are confined to
`.ufo/waves/round-39/falsify/F39NoHarmC1.md` and `F39NoHarmC1/receipts/`; all fixture trees lived in scratch and scratch
was removed.

VERDICT: no-harm-c1-ok
