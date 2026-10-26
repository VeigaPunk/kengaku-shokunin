# R43MutC2Counter — mutation-testing the C2 counter's V10 and re-pointed V9 (round 43, wave 1)

Seat: R43MutC2Counter (mutation-tester, leaf). 2026-10-26.
Target: `plans/round43_c2_verify.py` sha256 `f613bb1fc27775503c7276948ef5eb89ee60b457337b7f2929bcd87b0db62a5b` (frozen; digest re-verified unchanged at end).
Detector: the frozen triple in `.ufo/waves/round-43/claims/c2_filler_control.py` sha256 `e9fb3cee7090ce75ede2c9677828d5680f5ffbe1a8d733b8066d9db3eee5bb76` — filler must be V9 DEFECT + V10 DEFECT, informed V9 ok + V10 DEFECT, content V9 ok + V10 ok (`red-as-required`).
Method: one single-line mutant per named point (7 in `v10`, 4 one-character edits in `v9`'s `CASE_ROW`; 13 total). Each mutant was applied to a **copy of the counter inside my scratch clone** `/fast/scratch/hyaku/kengaku-r43/R43MutC2Counter/lane` (toplevel asserted `…/R43MutC2Counter/lane` before any write), the control ran against the patched copy, and pristine bytes were restored and digest-verified after every run. The lane was never written (`git -C "$S/lane" status --porcelain` empty at end; lane digests unchanged).

## Envelope (QUALITY Q32)

Every measured run inside `claims/envelope.sh`; `~/.local/bin` content digest `328be01808ba022f` before/after in all of them — no run was invalidated (no exit 4).

- Baseline (pristine counter): `ENVELOPE start 19:17:01` … `ENVELOPE end 19:17:03 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged` — output `CONTROL-C2-INFORMED-FILLER red-as-required`, rc=0 (`build/R43MutC2Counter/baseline_receipt.txt`).
- Mutant sweep: `ENVELOPE start 19:22:19` … `ENVELOPE end 19:22:21 exit=0 … unchanged` (`build/R43MutC2Counter/sweep_receipt.txt`; command `envelope.sh "$S/env" python3 "$S/mut_sweep.py"`).
- Drafted controls: `ENVELOPE start 19:26:19` … `ENVELOPE end 19:26:21 exit=0 … unchanged` (`build/R43MutC2Counter/draft_receipt.txt`).
- Three intermediate runs aborted on harness bugs (anchor-quoting assertion; a draft syntax error; a 6/8 draft run) — all with digest `unchanged`; superseded by the clean runs above.

## Result table (13 mutants; outcomes are the control's own printed legs)

Legend: caught-by lists the triple legs whose ok/DEFECT outcome flipped vs pristine. `mut sha` = first 16 hex of the mutated copy's sha256; every row shows `restored=f613bb1fc2777550` in the receipt (13/13 matches, `grep -c 'restored=f613bb1fc2777550' sweep_receipt.txt` → 13).

| id | point (v9/v10) | `old -> new` (one line) | filler V9/V10 | informed V9/V10 | content V9/V10 | caught-by | verdict | mut sha |
|----|----------------|--------------------------|---------------|-----------------|----------------|-----------|---------|---------|
| M01 | v10 DECISIVE lookup | `.get(cap, ())` -> `.get(cap, range(1, 400))` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `55535f32a4c5902b` |
| M02 | v10 `int(line) not in allowed` | `… not in allowed:` -> `… not in allowed and False:` | DEF/DEF | ok/**ok** | ok/ok | informed:V10 | caught | `edd70a91b3b0d01c` |
| M03 | v10 capture pin | `if cap not in CAPTURES or sha256(…) != CAPTURES[cap]:` -> `if cap not in CAPTURES:` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `b8231ac4f4e503ae` |
| M04 | v10 capture pin | `!= CAPTURES[cap]` -> `== CAPTURES[cap]` | DEF/DEF | ok/DEF | ok/**DEF** | content:V10 | caught | `58fed383977515d2` |
| M05 | v10 `norm` | `return " ".join(t.split())` -> `return t` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `a54e332e00a47372` |
| M06 | v10 2-word floor | `len(q.split()) < 2` -> `< 0` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `259c2268791a4291` |
| M07 | v10 ids-equal check | `!= want or not want:` -> `!= want:` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `198a2509121974c9` |
| M08 | v10 MECH_ROW | `“(.+?)”\s*\|\s*$")` -> `“(.+?)”\s*\|?\s*$")` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `c3ebf2505749618c` |
| M09 | v10 MECH_ROW | id class `[a-z0-9_-]+` -> `[a-z0-9_]+` (dash dropped) | DEF/DEF | ok/DEF | ok/**DEF** | content:V10 | caught | `a758ce921480afbb` |
| M10 | v9 CASE_ROW | id class `[a-z0-9_-]+` -> `[a-z0-9_]+` (dash dropped) | DEF/DEF | **DEF**/DEF | **DEF**/ok | informed:V9, content:V9 | caught | `d88c34f4c32c963f` |
| M11 | v9 CASE_ROW | `([PF])` -> `([pF])` | DEF/DEF | **DEF**/DEF | **DEF**/ok | informed:V9, content:V9 | caught | `62921111e4b3714e` |
| M12 | v9 CASE_ROW | `(pass|fail)` -> `(pass|fai1)` | DEF/DEF | **DEF**/DEF | **DEF**/ok | informed:V9, content:V9 | caught | `be642b618b3c7031` |
| M13 | v9 CASE_ROW | `.*\|\s*$")` -> `.*\|?\s*$")` | DEF/DEF | ok/DEF | ok/ok | — | **SURVIVED** | `d569a54821f3732e` |

`SWEEP total=13 caught=6 survived=7`.

## Coverage finding: what the triple does and does not exercise

Caught mutants show the triple's teeth: M02 dies exactly on the leg the informed filler was built for (uniform assert-line rows become acceptable); M04/M09 die on the content mirror (inverted digest check flags pinned captures; dash-less id class drops 11 of 12 rows); M10–M12 die on v9's case-table equality. All six kills are content-direction or informed-direction flips; the filler leg never flips alone (it is already red on both checks for every mutant).

The seven survivors share one shape: **the triple only feeds the counter well-formed rows, untampered captures, multi-word quotes, off-map-free decisive lines and a non-empty receipt.** No leg ever varies those, so any mutant that only loosens one of them is invisible to the triple:

1. M01 — no row ever cites a capture+line that is decisive for a *different* case (off-map pair).
2. M03 — no mirror ever ships a modified capture file.
3. M05 — every quote is byte-identical (modulo nothing) to the raw capture line; whitespace-tolerant matching is never needed.
4. M06 — every quote has ≥2 words.
5. M07 — the receipt always carries 12 CASE lines.
6. M08/M13 — every mechanism/case row ends in ` |`.

## Drafted controls, one per survivor (report dir only; `build/R43MutC2Counter/draft_controls.py`)

Each draft builds its mirror in scratch and is asserted twice: the **pristine** counter must give the required outcome (red where the shape must be rejected, green where it must not — no false positives), and the **mutated** counter must flip. Measured (`draft_receipt.txt`, envelope lines above):

| draft | kills | shape | pristine (required) | mutant (required) | result |
|-------|-------|-------|--------------------|--------------------|--------|
| D01-offmap-line | M01 | content mirror, nop row cites `feal.c:65` (decisive only for cheat-clock-seed) | V10 DEFECT | V10 ok | PASS |
| D03-tampered-capture | M03 | content mirror, `feal.c` appended `/* R43MutC2Counter D03 tamper */` in the mirror | V10 DEFECT (`capture not pinned`) | V10 ok | PASS |
| D05-spacing-quote | M05 | content mirror, every quote with doubled inner spacing (normalised-equal, raw-different) | V10 ok (spec: whitespace-normalised) | V10 DEFECT | PASS |
| D06-one-word-quote | M06 | content mirror, every quote one word from its decisive line | V10 DEFECT | V10 ok | PASS |
| D07-empty-receipt | M07 | receipt with no CASE lines + `## Mechanism` header with zero rows | V10 DEFECT (`rows=0 cases=0 ids_equal=True`) | V10 ok | PASS |
| D08-mech-row-no-pipe | M08 | 12 mechanism rows missing the final pipe | V10 DEFECT | V10 ok | PASS |
| D13-case-row-no-pipe | M13 | case-table rows missing the final pipe | V9 DEFECT, V10 ok | V9 ok | PASS |
| D00-sanity | — | plain content mirror on pristine counter | V9 ok, V10 ok | — | PASS |

`DRAFT-CONTROLS total=8 pass=8 fail=0`. D07 note: the empty receipt is red on V9 for both counters by construction; the discriminator is V10, which is the check M07 lives in. D13 note: first version kept the trailing pipe (draft bug, counter side fine); fixed template re-measured.

## Restoration evidence

- Per-mutant: the harness restores pristine bytes in a `finally` and asserts; receipt shows `restored=f613bb1fc2777550` on all 13 rows.
- End of session: `sha256sum` — lane `plans/round43_c2_verify.py` `f613bb1f…a5b` (== setup value), lane `claims/c2_filler_control.py` `e9fb3cee…b76` (== setup value), clone counter == `pristine_counter.py` == `f613bb1f…a5b`; `git -C "$S/lane" status --porcelain` empty; no `__pycache__`/`*.pyc` left in the clone.

## Operational hazard found on the way (worth carrying to other seats)

The first sweep run reported M10/M12 with another mutant's legs. Cause: the control imports the counter with `importlib` + `SourceFileLoader`, which consults `plans/__pycache__`; two mutants of the same file size compiled within the same second collide on the pyc header (mtime seconds + size), so the subprocess can execute the previous mutant's bytecode (observed: M10 printed M09's outcomes, M12 printed M11's). Direct repro of M10 with the cache cleared showed its true legs (`content V9 DEFECT case_rows=1/12`). Fix applied to the harness: `rm -rf plans/__pycache__` + `PYTHONDONTWRITEBYTECODE=1` before every control run, full re-sweep. Anyone running mutated copies of this counter (or the C1 counter's mutant loop) through subprocess imports needs the same purge, or same-size mutants can be mis-scored.

## Limits

- One plausible defect per named point; other edits of the same lines exist. M05's catchability depends on a whitespace-varied quote being reachable — the drafted D05 supplies one.
- The counter's own guard `sorted(DECISIVE) != sorted(frozen_ids)` and v10's `not want` placement were not separately mutated (M07 covers the `not want` half of the ids check).
- Mutant verdicts are relative to the frozen triple as detector; per the seat rules these are coverage findings, not proposals to change the frozen counter or control.

Deliverables in `build/R43MutC2Counter/`: `baseline_receipt.txt`, `sweep_receipt.txt`, `sweep_results.json`, `draft_receipt.txt`, `mut_sweep.py`, `draft_controls.py` (scratch `/fast/scratch/hyaku/kengaku-r43/R43MutC2Counter` removed after this report).

VERDICT: c2-counter-mutants-caught-6/13
