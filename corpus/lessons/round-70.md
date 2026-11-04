# Round 70 — kengaku (hyaku run 15)

Round 70 declared two claims (`plans/round-70-claims.md`, frozen at `384e9c76`; Amendment A1
dated before data): **R70-C1** coverage — replay the `nginx-request-logging` TB2 grader offline
under a re-frozen seven-case table that carries the two red witnesses round 69 lacked — and
**R70-C2** calibration — close the round-69 non-author closure's eight routed defects D1–D8 with
a re-deriving gate. R70-C1 is **admitted on its frozen sentence** (`PREDICATE R70-C1 pass`,
seven vectors, 56/56 legs, `LEG-COVERAGE legs=8 seen_p=8 seen_f=8`, staged-input
`case_sha256`); R70-C2 is **admitted on its frozen sentence** (`DEFECTS n=8` → `n=0`,
selftest 8/8, gate mutation 8/8), with the limitations below named rather than smoothed.

## Gate

SOURCES contract v1 — rows opened this round, each with its access date and a located quote.

- **S242 — the task instruction at the pin. Admit** (tier A, docs). Opened live 2026-11-03 by
  `curl` at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/instruction.md`
  (HTTP/2 200, 1882 bytes, 24 lines, sha256
  `26a7ac98aced6107f147206790ada77bbf8ed3c25fb360cf323d5fc6889edf99`). Located quote (≤25
  words), line 16: `"Welcome to the benchmark webserver"`; the 404 literal at line 18. The row
  is what closes D3: the entry's anchor now names `instruction.md:6-11,15-18`, and the
  instruction states four clauses the grader never checks (error-log path, default-site
  removal, `limit_req` application, burst/zone sizes).
- **S243 — the corrected leg map. Admit** (tier A, code, supersedes S241's summary cell). The
  same pinned grader bytes re-opened 2026-11-03 (`sha256 045cc716…acda0`, 5947 bytes, `cmp`
  byte-identical to the committed capture). Located quote, line 61:
  `result = subprocess.run(["nginx", "-t"], capture_output=True, text=True)`. Leg 5 is that
  subprocess (a shim satisfies it); legs 6-8 read config bytes and a log the server writes.
  S241's "legs 5-6 are file reads" is wrong and stays as written (append-only); S243 supersedes
  it. Closes D4.
- **S244 — the `merge/kengaku` package entry `grader-fixture-coverage`. Reject — reason:** the entry fails on its own bytes before any transcript is weighed — its triad is offset by a leading blank line (`recheck:` at `:4`, not `:3`; QUALITY Q1) — and its cited `S155` resolves in this lane to a different source (`corpus/SOURCES.md:170`, the TB2 password-recovery `solve.sh`). The cited transcript is now carried in this wave (`.ufo/waves/round-70/w1/SourceOpen70/S155-toolathlon-transcript-copy.md`, 7033 B, sha256 `3b9a4902…42ee`), but its Run section invokes `lanes/kengaku/round8/toolathlon-grader-fixture-probe2.py`, a script and receipt this lane does not hold, so the tier-A `own-work` claim (QUALITY Q2) is not re-derivable here. **Flip:** the probe script and its receipt land in this lane and re-run (`plans/…fixture_probe.py` + a receipt), with the entry re-registered against a source id that resolves here. **Registry:** `corpus/SOURCES.md:259`. Recorded as D7's required reject; one package entry was considered, none admitted, so `Assimilation: none` this round.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **staged-digest blind spot (a staged-state digest that excludes the state it is meant to identify)** | first `--stage-sha` run gave K1/K2/K3/K6/K7 one digest (`c6884ff0…`): the bodies and the log/service flags lived in `run/server.json`, which the digest excluded as path-dependent (`plans/round70_c1_nginx_probe.py` `case_dir_sha`; freeze transcript `plans/round-70-claims.md` R70-C1 "staged-state digests") | the freeze step's own `--render-table --stage-sha` run (two cases differed only in bytes the digest skipped) | split the payload: `run/bodies.json` carries bodies + `log_enabled` + `server_enabled` and is hashed; `run/server.json` keeps only the absolute log path. All seven digests now differ; `--selftest` arms `PATH-INDEPENDENT` and `STAGED-STATE` prove both directions. Q52 records the rule. |
| **self-unreadable receipt, recurrence (a checker that cannot parse its own writer's output)** | the copied `check_receipt` required 4 whitespace tokens on `CASE` lines; the writer emits 5 (`CASE K1 case_sha256=… server_pid=… sandbox_rc=0`) → every genuine receipt would have been refused (`DEFECTS case-line` × 7 in `--selftest`) | the selftest's acceptance arm, on the first run after the digest fix | parse the 5-token form. Same class as round-69's `VECTOR` 5-vs-6 defect: a checker's parser is not evidence until the acceptance arm runs on its writer's own output. |
| **argument-order in a gate check (a check whose red is its own wiring, not the correction)** | `E1 defect … problems=['change-wider-than-counts','recorded-pair']` on bytes that satisfy the correction: `check_depth_identity` normalised the landing line towards the wave line instead of the reverse and compared the pair in the opposite order to the provenance file | the C2 red-before run at base, re-run after the provenance landed | Amendment A1: order the pair `wave -> corpus` and normalise the corpus line's `total=34`/`resolved=34`. The predicate, recorded pair and frozen sentence are unchanged; no receipt was scored before the repair. |
| **exception-red folded into the verdict (a receipt that cannot distinguish an assertion failure from a raised exception)** | `LegWitnessProof` §5: K6's legs 3, 4, 7, 8 are `requests.exceptions.ConnectionError`, scored `F` by the runner's `E`→`F` mapping; the receipt records only `F` (`corpus/evidence/round70/nginx/receipt.txt`) | the `LegWitnessProof` seat, reading the per-case sandbox stdout | named limitation, not patched: the frozen predicate says `P`/`F` and pytest scores an exception as a test failure, so the direction is right; a successor probe that prints `E` separately would price the distinction. |
| **speedy claim about isolation (K6's note reads "legs 2, 3, 4, 7, 8 red", but only K7 isolates one leg)** | `CaseTableAudit` §4 item 1: K6 leg 4's red is the refused connection, not `:53`; the note is exact about *which* legs are red but not about *which assertion* each red is | the `CaseTableAudit` and `LegWitnessProof` seats, independently | recorded in the claims doc's named limitation (iii) and in the knowledge entry's round-70 addendum; no frozen element changed. |

| **freeze-doc overclaim (a frozen document asserting an equality broader than the artefact)** | `plans/round-70-claims.md:27` said "`--render-table` must byte-equal it"; the rendered table prints the instrument's own `note` wording, so the blocks differ in prose while the case set, the seven vectors and the `FROZEN-VECTOR` line agree (reproduced by `Lesson70Draft`; `--render-table` output in `.ufo/waves/round-70/w1/NginxBatteryR70/render-table.out`) | the `Lesson70Draft` seat, comparing the frozen block with the rendered output | Amendment A3 narrows the sentence to the bound fields; no vector, digest, kill rule or predicate changed, and the battery was scored against the vectors. |

| **dead check clause (a guard that can never fire, counted as a check)** | `check_instruction_row`/`check_s241_correction` guarded `used-by` with `len(c) > 11`, while `cells(row)` returns 11 items — a row with `used-by = —` passed E3 and E4 (`ClaimFalsify70`; the repair's red arm is `corpus/evidence/round70/c2/a4-usedby-arm.txt`) | the `ClaimFalsify70` critic, reading the check against its own `cells()` helper | guards corrected to `len(c) != 11 or NGINX_ENTRY not in c[10]` (Amendment A4), and both clauses are exercised on blanked-cell fixtures. The same critic found S243's quote cited `:59` (the `def` line) instead of `:61`; both the row and the entry's errata are corrected. |

| **unre-derived landing prose (an index row and a rejection reason asserted instead of counted)** | the README round-70 row said "six Mistakes rows" while the lesson carries seven; the S244 reject reason said the candidate's `source:` line is `:1` (it is `:2`, after a leading blank line) and that its transcript is not in the lane (the wave carries it at `.ufo/waves/round-70/w1/SourceOpen70/S155-toolathlon-transcript-copy.md`, 7033 B, sha256 `3b9a4902…42ee`); the entry body still cited `:59` for the `nginx -t` statement after A4 corrected the registry row to `:61` (`CorrectionDraft` §4/§5). The round-69 index row this round added also said "five Mistakes rows" for a six-row lesson and named D2 as a Mistakes row; it is corrected in the same commit. | the `CorrectionDraft` seat, re-reading each landed line against the artefact it names | the README count, the reject paragraph (Q1 triad offset, the S155 collision in this lane, the missing runnable probe as the surviving ground) and the entry pointer are corrected against the bytes; the lexical gate could not catch any of the three — named limitation, not smoothed. |

## Census

- Before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  → rc 0, 233 data rows (`.ufo/waves/round-70/census-before.txt`).
- After: same command at round end → rc 0, 236 data rows, tier A +2 (S242, S243), tier C +1
  (S244, rejected); W04 warnings 24 → 25, the new one naming S243's superseding row
  (`corpus/evidence/round70/census-after.txt`).

## Verdicts

- **R70-C1**: admitted on the frozen sentence; coverage held at its L0 cap (7).
- **R70-C2**: admitted on the frozen sentence; calibration held at ceiling (10), exercised.
- No owned axis harmed (see the SCORECARD section).
