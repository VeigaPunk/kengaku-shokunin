# F39RevBatP3 — falsify review of `plans/battery39/p3m39.py` (M03: P3 upper word bound, silence)

Seat F39RevBatP3 (wave 2 reviewer, kengaku round 39, hyaku run 8, 2026-10-26). Measured on a clean clone of the
assigned lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (`git rev-parse --show-toplevel` = the clone path;
`git status --porcelain` = 0 lines). Scope: the two questions below, about the one fixture
`p3m39-quote-one-word-above-upper-bound` and the one mutant M03. Receipts:
`.ufo/waves/round-39/falsify/F39RevBatP3/`. Scratch `/fast/scratch/hyaku/kengaku-r39/F39RevBatP3` (deleted).

**Tip bookkeeping.** Master has advanced one commit past the assigned tip to `acf4375` (wave-2 dispatch JSONs
only: `git diff --name-only a6832f5..acf4375` lists exactly `falsify-dispatch.json`, `falsify-spec.json`). The
L1's `measure-final.txt` was recorded at `34158b0`; `git diff --stat` over `plans/battery39/p3m39.py`,
`plans/pkg_gate.py`, `plans/round39_c1_verify.py`, `plans/pkg-spec-r35.json` is empty across both
`34158b0→a6832f5` and `a6832f5→acf4375`, so the landing measurement's M03 lines transfer verbatim, and the
at-tip runs below reproduce them.

## Q1 — is the reference's P3 DEFECT caused by the word count alone (not by P4 or another clause)?

**Yes.** Four legs, all at the assigned tip:

1. **Only P3 fires, and only its word-window term.** Reference gate on the built fixture
   (`ref-m03-stdout.txt`, command inside): `P3 DEFECT rows=22 distinct_quotes=22 distinct_lines=22
   out_of_word_range=1`, every other clause `ok` (P1 pinned=3, P2, P4 checked=22 bad=0, P5 manifest_entries=6,
   P6, P7, P8, P9 untracked=0), `defects=1`, rc=1, stderr empty. P3's accept term is
   `len(texts) >= min_quotes and len(locs) >= min_distinct_locations and not short` (`pkg_gate.py:133-134`);
   with 22/22/22 against min 8/8 (`pkg-spec-r35.json` `entry_rules`: `quote_words [3,25]`, `min_quotes 8`,
   `min_distinct_locations 8`), the only false term is `not short` — the word window (`pkg_gate.py:130`).
2. **The out-of-range row is the new row, and it is the only one** (`fixture-forensics.txt`): the table has 22
   data rows; the kept 21 are byte-identical to the genuine entry's rows (`kept_rows_identical: True`; the
   removed genuine row was the `instruction.md:33` "required order" row). The new row cites `task.toml:6`,
   `quote_words=26`, `verbatim_substring: True` — a byte substring of the copied capture's line 6 (29 words),
   no `|`, no `”` — `task.toml pinned: True`, `distinct_locations: 22` (the new location collides with no kept
   row), `distinct_quotes: 22`. So no unparsed row (rows=22, not 21), no distinct-count drop, no unpinned
   capture: nothing but the count is out of line.
3. **Counterfactual at the fixed reference gate** (`driver-out.txt`): the same row — same claim cell, same
   `task.toml:6` citation — with the last **25** words of the same line gives `VARIANT words=25 gate=REF rc=0 |
   P3 ok … out_of_word_range=0 | defects=0`. One word less → accept. The DEFECT is attributable to exactly the
   one-word excess over the frozen bound.
4. **Not P4.** P4 is `ok checked=22 bad=0` on the reference run: the verbatim route was preserved by
   construction — `_overlong_quote` returns a text only when `text in line` (`p3m39.py:40`) and P4 compares
   `q.text` against the cited capture lines (`pkg_gate.py:148`). The build reads the fixture's own copied
   bytes (`p3m39.py:50`), so the citation matches the copy.

## Q2 — does the mutant's `hi + 1` silence it on that fixture only?

**Yes.** Three independent proofs plus the counter-native ones:

1. **On the fixture** (`ref-m03-stdout.txt`): REF rc=1 `P3 DEFECT … out_of_word_range=1` → M03 rc=0 `P3 ok …
   out_of_word_range=0`; every other stdout line byte-identical, stderr empty on both. The declared `silence`
   direction holds with both exits in {0,1} (ref 1, mut 0), P3 in the reference's DEFECT set and the fixture's
   declaration, P3 absent from the mutant's.
2. **Boundary — the shift is exactly one word** (`driver-out.txt`): 25 words → REF ok AND M03 ok (rc=0);
   27 words (last 27 of the same 29-word line) → REF DEFECT **and** M03 DEFECT (rc=1,
   `out_of_word_range=1`). The mutant does not silence a two-word excess; only the exactly-26-word case
   flips. Lower edge: battery37's `p23-p3-two-word-quote` (2 < lo) shows ref==mut in the sweep below.
3. **Whole battery, byte-level** (`driver-out.txt`): reference vs M03 gate on every fixture the frozen counter
   builds (round-36 + battery37 in-process, battery38 + battery39 out-of-process), comparing rc + full stdout
   + full stderr: `SWEEP fixtures=90 ref_vs_M03_differing=1 ids=['p3m39-quote-one-word-above-upper-bound']`.
   No other fixture moves — not even a note-only delta (an `out_of_word_range` count change under an
   already-DEFECT P3 would have shown).
4. **Counter-native, at the tip**:
   - `python3 plans/round39_c1_verify.py --lane <clone> --work <S/w>` → `FIXTURE p3m39-… expect=reject
     declared=P3 observed_rc=1 observed_defects=P3 ok`, `MUTANT M03 P3 silence killed by=
     p3m39-quote-one-word-above-upper-bound`, `MUTANTS total=7 killed=7 survived=0 invalid=0
     null_detected=0`, `PREDICATE C1 pass`, exit 0 (`counter-full.txt`) — reproduces the landing measurement.
   - Deletion probe (module copy with `FIXTURES = []`): `MUTANT M03 P3 silence SURVIVED exhibits=none`
     (`nofx-run.txt`) — with the fixture gone, M03 differs from the reference on **no** fixture in **any**
     declared direction. The fixture is the sole source of the kill (reproduces R39BatP3 Evidence 2).
   - L1 audit: `AUDIT nondeterministic_kills=0`, `PINS final total=26 mismatched=0`, `AUDIT C1 clean`,
     `PREDICATE C1 pass`, exit 0 (`audit.txt`) — the kill survives the A1 re-check (reference re-run after the
     mutant run), so it is not a mid-run-flip artifact of the wave-1 A1 gameability.

## Fixture hygiene (admission re-checks)

- Module sha256 `fd16681e3ee0bb57e72779026fafccd3c0bf4b1cf603108574a39a297673d497` equals the wave-1
  deliverable digest (R39BatP3.md); gate `ea638822…` and spec `e085b435…` equal their PINS entries
  (`digests.txt`).
- M03 `old` occurs exactly once in the gate, `new` zero times (`digests.txt`) — the counter's invalid check
  cannot misfire and the one-term replacement is unambiguous.
- Module imports `pathlib` only (`p3m39.py:20`); 0 side-channel tokens (`grep -c -E
  '/proc|ppid|cmdline|psutil|environ'` → 0); counter reports `sidechannel=0`.
- Fixture argv carries no `--spec` (`build-fixture.txt` BUILT JSON) — the counter appends the frozen spec, so
  the bound the mutant widens is the frozen one, not a fixture-authored one.
- Build derives word count, line number and capture name from the fixture's own copied bytes
  (`p3m39.py:48-50`); the counter's `renamed_disagree=0` at the tip covers path-independence.

## Residual limits (named, not defects)

- The sweep compares the gate's observable outputs (rc, stdout, stderr); a difference invisible in all three
  is out of scope by construction.
- The 27-word probe used the same `task.toml` line (29 words); the upper edge is pinned at 27, the lower at 25
  — the exactly-26 window is bracketed on both sides.
- Wave-1's A1 mid-run-flip gameability of the **frozen** counter remains open as a class (the audit is
  post-hoc, not the frozen rule); for this kill the audit's A1 re-check is clean and my sweep observed stable
  reference results (`null_detected=0` in the counter run).

No defect found on either question; the fixture's declared leg (`reject`/`["P3"]`) matches the unmodified
gate's observed behaviour exactly, and the kill is attributed to this fixture alone.

VERDICT: p3m39-honest
