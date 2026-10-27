# R44MutC2Guards — mutation-testing the round-44 C2 counter's V9/V10 (v2 wave, 2026-10-26)

Seat: R44MutC2Guards (mutation-tester, leaf). Routed from `R43MutC2Counter` (round-43 wave 1): 7/13 of the
round-43 V9/V10 mutation set survived the round-43 triple control. This seat re-runs that exact 13-mutant set
against the round-44 counter `plans/round44_c2_verify.py` (V9/V10 re-pointed, V11 added) using mirrors built from
the real round-44 probe receipt (`corpus/evidence/round44/feal-linear-probe.txt`) and a drafted entry shape, and
drafts one red control per survivor.

Target: `plans/round44_c2_verify.py` at lane tip `5e3d3aa06c6b7000929ac3e62563a39159c4501f`, sha256
`334ce2dac6828f8d7b0d57610f7204db2dcf5c5c2686ed406ab19880abfc82a6` (re-verified unchanged at end; the counter file
was never written, only read and copied into scratch).

## Method (same shape as round-43 R43MutC2Counter)

- Detector: three scratch mirrors exercising V9 + V10 — **filler** (entry teaches nothing: no `## Case table`, no
  `## Mechanism`), **informed** (case table copied verbatim from the receipt by `| `id` | <tests> | <observed> | measured |`
  rows, PROVINCE.md/README naming the task, every mechanism row pointing at `test_outputs.py:106` `def test_attack():`
  — a real verbatim line that is decisive for **no** frozen case), **content** (same mirrors but each mechanism row on
  a frozen DECISIVE line of the pinned captures with a verbatim ≥2-word quote). The round-44 receipt's 14 case rows
  are used in order; DECISIVE lines verified against the captures (test_outputs.py:4/120/121/122, gen.py:12/60/61/62,
  decrypt.c:136, solve.sh:304).
- The 13 single-line mutants are the round-43 set (M01–M13), applied to copies of the round-44 counter under
  `$S/muts/`; the pristine counter is run on the same mirrors as the reference. A mutant is CAUGHT iff any V9/V10
  leg flips vs pristine; verdicts are the counter's own printed legs.
- Hygiene: `PYTHONDONTWRITEBYTECODE=1` on every run (no `__pycache__`; the round-43 pyc-collision hazard is avoided
  by importing each mutant from its own path with a unique module name); lane read-only; all writes under `$S`.
- Lane bounds: leaf seat, no subagents; all measured runs inside the round-44 envelope.

## Envelope (QUALITY Q32)

Every measured run inside `claims/envelope.sh`; `~/.local/bin` content digest `328be01808ba022f` before/after in
both, no exit 4 (no run invalidated):

- Sweep (baseline + 13 mutants): `ENVELOPE start 20:37:42` … `ENVELOPE end 20:37:44 exit=0
  local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (receipt
  `wave/R44MutC2Guards/sweep_receipt.txt`).
- Drafts (8 controls): `ENVELOPE start 20:38:03` … `ENVELOPE end 20:38:04 exit=0
  local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` (receipt
  `wave/R44MutC2Guards/draft_receipt.txt`).

## Baseline (pristine counter on the three mirrors) — the detector's shape assumptions hold

```
BASELINE filler V9=DEFECT case_rows=0/14 bad=["no '## Case table' section"] V10=DEFECT no '## Mechanism' section
BASELINE informed V9=ok case_rows=14/14 bad=0 V10=DEFECT mechanism_rows=14/14 bad=[14× '<id>:test_outputs.py:106 not decisive']
BASELINE content V9=ok case_rows=14/14 bad=0 V10=ok mechanism_rows=14/14 bad=0
```

## Sweep result (13 mutants; expectations as round 43: 6 caught, 7 survived)

| id | point (v9/v10) | `old -> new` | filler V9/V10 | informed V9/V10 | content V9/V10 | caught-by | verdict | mut sha |
|----|-----------------|--------------|---------------|-----------------|----------------|-----------|---------|---------|
| M01 | v10 DECISIVE lookup | `.get(cap, ())` -> `.get(cap, range(1, 400))` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `634745ff9ed871de` |
| M02 | v10 `int(line) not in allowed` | `… not in allowed:` -> `… not in allowed and False:` | F/F | ok/**ok** | ok/ok | informed:V10 | caught | `9405bdbfc4b2319e` |
| M03 | v10 capture pin | `if cap not in CAPTURES or sha256(…) != CAPTURES[cap]:` -> `if cap not in CAPTURES:` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `a97a1f9b0ca6c76d` |
| M04 | v10 capture pin | `!= CAPTURES[cap]` -> `== CAPTURES[cap]` | F/F | ok/DEF | ok/**DEF** | content:V10 | caught | `997b68f432584cb4` |
| M05 | v10 `norm` | `return " ".join(t.split())` -> `return t` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `c120975054593a07` |
| M06 | v10 2-word floor | `len(q.split()) < 2` -> `< 0` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `6f3c58d83137e1b9` |
| M07 | v10 ids-equal check | `!= want or not want:` -> `!= want:` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `07c1977f514b1ca5` |
| M08 | v10 MECH_ROW | `“(.+?)”\s*\|\s*$")` -> `“(.+?)”\s*\|?\s*$")` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `e876f49476312b28` |
| M09 | v10 MECH_ROW | id class `[a-z0-9_-]+` -> `[a-z0-9_]+` (dash dropped) | F/F | ok/DEF | ok/**DEF** | content:V10 | caught | `f51d33e41353a6c7` |
| M10 | v9 CASE_ROW | id class `[a-z0-9_-]+` -> `[a-z0-9_]+` (dash dropped) | F/F | **DEF**/DEF | **DEF**/ok | informed:V9, content:V9 | caught | `e9a872a79820fc13` |
| M11 | v9 CASE_ROW | `([PF])` -> `([pF])` | F/F | **DEF**/DEF | **DEF**/ok | informed:V9, content:V9 | caught | `f641705903899445` |
| M12 | v9 CASE_ROW | `(pass|fail)` -> `(pass|fai1)` | F/F | **DEF**/DEF | **DEF**/ok | informed:V9, content:V9 | caught | `816d38892f02a979` |
| M13 | v9 CASE_ROW | `.*\|\s*$")` -> `.*\|?\s*$")` | F/F | ok/DEF | ok/ok | — | **SURVIVED** | `918d8f96edd6b2a4` |

`SWEEP total=13 caught=6 survived=7` — identical verdicts to the round-43 sweep: the round-44 V9/V10 code
(re-pointed) carries the same seven blind spots. All six kills are content-direction or informed-direction flips;
the filler leg never flips alone (it is already red on both checks for every mutant). `COUNTER_SHA_AFTER
334ce2dac6828f8d7b0d57610f7204db2dcf5c5c2686ed406ab19880abfc82a6`.

## Coverage finding: what the three mirrors do and do not exercise

The six caught mutants die exactly on the legs the mirrors were built for: M02 on the informed filler (uniform
assert-line rows become acceptable), M04/M09 on the content mirror (inverted digest check flags pinned captures;
dash-less id class drops 13 of 14 mechanism rows), M10–M12 on the case-table equality (dash-less id class drops 13 of
14 rows; `[pF]` drops all 8 P rows; `pass|fai1` drops all 6 fail rows).

The seven survivors share one shape, as in round 43: **the mirrors only feed the counter well-formed rows, untampered
captures, multi-word quotes, on-map decisive lines and a non-empty receipt.** No mirror varies those, so any mutant
that only *loosens* one of them is invisible:

1. M01 — no row ever cites a capture+line that is decisive for a *different* case (off-map pair).
2. M03 — no mirror ever ships a modified capture file.
3. M05 — every quote is byte-identical (modulo nothing) to the raw capture line; whitespace-tolerant matching is never needed.
4. M06 — every quote has ≥2 words.
5. M07 — the receipt always carries 14 CASE lines.
6. M08/M13 — every mechanism/case row ends in ` |`.

## Drafted red controls, one per survivor (report dir only; `draft_receipt.txt`, `drafts.py` in scratch)

Each draft builds its mirror in scratch and is asserted twice: the **pristine** counter must give the required
outcome and the **mutated** counter must flip. Measured in the drafts envelope run above:

| draft | kills | shape | pristine (required) | mutant (required) | result |
|-------|-------|-------|--------------------|--------------------|--------|
| D00-sanity | — | plain content mirror on pristine counter | V9 ok, V10 ok | — | PASS |
| D01-offmap-line | M01 | content mirror, nop row cites `gen.py:12` (decisive only for decrypt-public-keys) | V10 DEFECT (`nop:gen.py:12 not decisive`) | V10 ok | PASS |
| D03-tampered-capture | M03 | content mirror, `gen.py` appended `/* R44MutC2Guards D03 tamper */` | V10 DEFECT (`decrypt-public-keys:gen.py capture not pinned`, `replay-public-gen:gen.py capture not pinned`) | V10 ok | PASS |
| D05-spacing-quote | M05 | content mirror, every quote with doubled inner spacing (normalised-equal, raw-different) | V10 ok (spec: whitespace-normalised) | V10 DEFECT | PASS |
| D06-one-word-quote | M06 | content mirror, every quote one word from its decisive line | V10 DEFECT | V10 ok | PASS |
| D07-empty-receipt | M07 | receipt with no CASE lines + `## Mechanism` header with zero rows | V10 DEFECT (`mechanism rows=0 receipt cases=0 ids_equal=True`) | V10 ok | PASS |
| D08-mech-row-no-pipe | M08 | 14 mechanism rows missing the final pipe | V10 DEFECT (`mechanism rows=0 receipt cases=14 ids_equal=False`) | V10 ok | PASS |
| D13-case-row-no-pipe | M13 | case-table rows missing the final pipe | V9 DEFECT, V10 ok | V9 ok, V10 ok | PASS |

`DRAFT-CONTROLS total=8 pass=8 fail=0`. D07 note: the empty receipt is red on V9 for both counters by construction;
the discriminator is V10, which is the check M07 lives in. D03 note: the tampered capture is `gen.py` because it is
the capture actually cited by content rows (decrypt-public-keys, replay-public-gen); the earlier draft tampered
`decrypt.c`, which no content row cites, and correctly failed the pristine leg — fixed before the measured run.

## Restoration evidence

- Mutants exist only as copies under `$S/muts/` (`M01.py`…`M13.py`, `pristine.py`); the lane file was never opened
  for writing. `COUNTER_SHA_AFTER 334ce2dac6828f8d7b0d57610f7204db2dcf5c5c2686ed406ab19880abfc82a6` == the setup
  value; `git -C "$S/lane" status --porcelain` empty; `git -C "$S/lane" rev-parse --show-toplevel` ==
  `$S/lane` asserted before any write; no `__pycache__`/`*.pyc` left under `$S` (PYTHONDONTWRITEBYTECODE=1, no
  bytecode files created).

## Limits

- One plausible defect per named point (the round-43 set); other edits of the same lines exist. M05's catchability
  depends on a whitespace-varied quote being reachable — the drafted D05 supplies one. M01 is killable only by an
  off-map (case, capture, line) triple — drafted D01 supplies one.
- Verdicts are relative to the three mirrors as detector; per seat rules these are coverage findings, not proposals to
  change the frozen counter.
- The round-44 V11 predictor leg is not exercised here (it is the C2 `## Predictor`/grader execution; the routed set
  covers V9/V10 only).

Deliverables: `wave/R44MutC2Guards/sweep_receipt.txt` (sha256 `c0f45d5e3dd4c48d7ea513e89da6def78e9f91265145eb2e38e2efae720fd9f9`),
`wave/R44MutC2Guards/draft_receipt.txt` (sha256 `299a42ed4c007458af7bef5b87e40cc21aa14992ced8f46175a4b2040698c438`),
`wave/R44MutC2Guards/sweep_results.json` (sha256 `6175842b5af18b730b9950a1e4b8710224ddd92d1ee55c6c85fde37032438dba`);
scratch `/fast/scratch/hyaku/kengaku-r44/R44MutC2Guards` removed after this report.

VERDICT: c2-guards-caught-6/13
