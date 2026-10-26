# F38XMutP — extra (non-frozen) gate mutants vs clauses P1–P8 (round-38 wave 2, falsify)

Seat: F38XMutP (mutation-tester, leaf). Target: `plans/pkg_gate.py` at lane tip `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`
(gate digest `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`, the frozen value in
`plans/round38_c1_verify.py` PINS). Scope: mutant shapes **beyond** the frozen lists N01–N22
(`plans/round38_c1_verify.py`) and M01–M55 (`plans/round37_c1_verify.py`), run over the **full landed battery**
(round-36 + `plans/battery37` + `plans/battery38`) with the **round-38 attributed kill rule**.

## Method

Harness `.ufo/waves/round-38/falsify/F38XMutP/xmutp_harness.py` imports the frozen counter from a clean clone of
the landing tip and reuses its own functions (`run_gate`, `attributed`, `battery38_fixtures`, `FAMILY`, plus
`round37_c1_verify`'s `load_r36`/`Ctx`/`r36_fixtures`/`battery37_fixtures`) — the fixture assembly, argv
validation, reference runs and attribution predicate are the counter's code, not a reimplementation. The lane was
never written: mutant gate copies live under scratch.

- Clone: `git clone -q --no-local …/kengaku-shokunin $S/lane && git -C $S/lane checkout -q 8c7422d7…`;
  `git -C $S/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r38/F38XMutP/lane`; `rev-parse HEAD` →
  `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`. Scratch `$S=/fast/scratch/hyaku/kengaku-r38/F38XMutP`, `TMPDIR=$S`.
- Hygiene, enforced in-harness before any run: every `old` occurs **exactly once** in the gate source; no
  `(old,new)` pair equals any frozen N/M pair; every mutant compiles (`py_compile doraise`); every mutant file
  re-hashed after its run (unchanged). Output: `HYGIENE mutants=20 old-unique=yes frozen-pair-overlap=no`.
- Direction discipline (N21 lesson, `plans/mutant_direction_check.py`): for every fixture the harness tries
  **both** `attributed(…, "silence", …)` and `attributed(…, "mirror", …)` and reports the direction that actually
  fired — a mislabelled direction cannot hide a kill.
- Battery sanity on the reference and a null (unchanged) gate copy, same predicates as the counter.

## Battery sanity (independent re-run on the clean clone)

Command: `python3 …/xmutp_harness.py $S/lane $S …/falsify/F38XMutP/xmutp-run.txt` →

```
BATTERY fixtures=86 wrong=0 null_detected=0 sidechannel=0
```

This reproduces the landing receipt's battery line (`.ufo/waves/round-38/integrate/measure-final.txt`:
`BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`) — the renamed-copy leg was not re-run here (it is
the counter's own check, already green at landing); ref, null, wrong and sidechannel were.

## Results — 20 extra mutants, 17 killed, 3 survived, 0 invalid

Receipt: `.ufo/waves/round-38/falsify/F38XMutP/xmutp-run.txt` (pass 2; pass 1 with the since-withdrawn X06:
`xmutp-run-pass1.txt`). `MUTANTS total=20 killed=17 survived=3 invalid=0`.

| id | clause | shape | verdict | killed by (dir) |
|----|--------|-------|---------|-----------------|
| X01 | P1 | first-item-only | **SURVIVED** (no fixture differs) | — |
| X02 | P1 | mirror | killed | r36-P0 (mirror) |
| X03 | P2 | mirror | killed | r36-P0 (mirror) |
| X04 | P3 | off-by-one (`>=`→`>` on min_quotes) | killed | p3m-exact-min-distinct-locations (mirror) |
| X05 | P3 | off-by-one (upper word bound +1) | **SURVIVED** (no fixture differs) | — |
| X07 | P4 | off-by-one (verbatim slice starts one line low) | killed | r36-P0 (mirror) |
| X08 | P4 | mirror (`lines is None` inverted) | killed | r36-P0 (mirror) |
| X09 | P5 | mirror (manifest-vs-bytes compare inverted) | killed | r36-P0 (mirror) |
| X10 | P5 | first-item-only (quote-capture pin check) | killed | p4-capture-unreadable (silence) |
| X11 | P6 | loosened compare (`cells != 11` → `< 11`) | killed | p6-m21-row-with-twelve-cells (silence) |
| X12 | P6 | loosened compare (`found != 1` → `< 1`) | killed | p6-m20-registry-row-duplicated (silence) |
| X13 | P6 | mirror (teaches-distinct inverted) | killed | r36-P0 (mirror) |
| X14 | P7 | first-item-only (prov loop) | killed | r36-P0 (mirror) |
| X15 | P7 | loosened compare (extra source lines tolerated) | **SURVIVED** (no fixture differs) | — |
| X16 | P7 | mirror (verified-at inverted) | killed | r36-P0 (mirror) |
| X17 | P8 | first-item-only (index loop) | killed | r36-P0 (mirror) |
| X18 | P8 | first-item-only (cited sids) | killed | p8-index-row-missing-sid (silence) |
| X19 | P8 | mirror (coverage-bullet inverted) | killed | r36-P0 (mirror) |
| X20 | P5 | reordered branch (uncovered-file check before manifest parse) | killed | r36-P0 (mirror) |
| X21 | P7 | reordered branch (per-sid source compare before prov collect) | killed | r36-P0 (mirror) |

Pattern: every mirror/false-red shape on P1–P8 dies on `r36-P0` (the genuine-package accept fixture) — the
false-red direction the round-37 list lacked is now broadly demonstrated. The three survivors are all
false-green (silence-direction) gaps.

## Survivors — round-39 candidates (all proven non-equivalent by witness)

Each survivor produced **no differing fixture anywhere in the 66-fixture package family** (`no-fixture-differs`),
then a hand-built witness package flipped the clause — real behaviour gaps, not equivalent mutants.
Witness receipt: `.ufo/waves/round-38/falsify/F38XMutP/witness-run.txt` (`WITNESSES total=3 ok=3`).

1. **X01 — P1 checks only the first pinned instrument.** The battery's only instrument-mismatch fixture corrupts
   the *first* pin: `round36_c1_verify.py:120-123` `stub_probe` overwrites `spec["probe_cmd"][0]`, which is
   `plans/tb2_grader_probe.py` — first key of `frozen_instruments` in `plans/pkg-spec-r35.json`. No fixture
   corrupts a later pin. Witness W-X01 (second instrument `plans/round35_c1_verify.py` corrupted):
   `ref_defects=P1,P9 mut_defects=P9 flip=P1->P1-ok ok`. *Round-39 candidate:* a fixture corrupting a non-first
   pinned instrument.
2. **X05 — P3 accepts a quote one word above the range.** `quote_words=[3,25]`; the only word-range fixture is
   below the bound (`p23-p3-two-word-quote`, 2 words), none above 25. Witness W-X05 (26-word quote):
   `ref_defects=P3,P4,P9 mut_defects=P4,P9 flip=P3->P3-ok ok` (P4 fires in both — text no longer verbatim — the
   clause under test is P3). *Round-39 candidate:* a fixture with a quote above the upper word bound.
3. **X15 — P7 tolerates extra `source:` lines for a row.** `p7-m29-source-url` *changes* the S106 URL
   (`battery37/p7.py:67-70`, `text.replace(SOURCE_URL, BROKEN_URL, 1)`); no fixture gives one sid two source
   lines. Witness W-X15 (duplicate `source: S106 …` line appended): `ref_defects=P7,P9 mut_defects=P9
   flip=P7->P7-ok ok`. *Round-39 candidate:* a fixture with a duplicated source line for one sid.

## Limit reported (not a survivor): X06, withdrawn after pass 1

Pass 1 ran X06 (P3: unparsed-row early return hoisted below the `ok` computation) → `SURVIVED
no-fixture-differs`. On inspection it is **observationally equivalent**, not a battery gap: `bad_rows` is fixed
at parse time, the hoisted computation never writes it, and the guard's `return False` and the final
`return ok, …` are mutually exclusive on `bad_rows` — reordering them cannot change any (rc, DEFECT set). The
r36-P3 fixture (`mut_unparsed` appends a straight-quotes row beside 28 genuine rows) cannot separate them.
Reported as a limit per the round's own discipline (frozen claims: "A mutant later shown equivalent is reported
as a limit, never removed from the list"); replaced in pass 2 by X21, a reorder that reads state a later loop
fills (prov) and is killed.

## Attack on the frozen 21 kills / N21 — scope note

This seat's assignment is the extra-mutant probe; the 21 attributed kills and the N21 `silence`/mirror question
are attacked by the dedicated seats (e.g. C2MutEntry-2, F38MapV7Control). One incidental datum from this run:
with both directions scanned, no frozen mutant's kill here depended on its declared direction alone —
`mutant_direction_check.py`'s `N21 … declared=silence observed=mirror MISLABELLED` (measure-final.txt) remains
the authoritative N21 record; this harness's direction-agnostic scan is the pattern that catches such
mislabels.

## Restoration / non-mutation evidence

- Lane gate before run: `ea638822…dd41` (`sha256sum`, pre-run); after both passes: `ea638822…dd41` — identical;
  no lane file was written at any point (mutant copies lived under `$S`).
- Clone HEAD after runs: `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`.
- Scratch contents after runs: `lane` only (harness `finally` removed its work root); `$S` deleted at cleanup.
- No tools installed or upgraded (none needed); pacman untouched.

## Receipts

- `.ufo/waves/round-38/falsify/F38XMutP/xmutp_harness.py` — harness (imports the frozen counter).
- `.ufo/waves/round-38/falsify/F38XMutP/xmutp-run.txt` — pass-2 receipt (final, 20 mutants).
- `.ufo/waves/round-38/falsify/F38XMutP/xmutp-run-pass1.txt` — pass-1 receipt (X06 present).
- `.ufo/waves/round-38/falsify/F38XMutP/witness.py`, `witness-run.txt` — survivor witnesses.

VERDICT: xmut-p-killed-17/20
