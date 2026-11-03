# Round 63 — kengaku lesson (2026-11-03)

author: kengaku L1 (round 63, attempt 1). Base `c78749a5`; freeze `9ebde3a7` (claims doc, do-nothing
control receipt, wave spec, validated dispatch) landed BEFORE the wave ran; the wave is
`.ufo/waves/round-63/w1` (v1, 12 seats: 2 executor, 2 scribe, 2 reviewer, scout, connector, critic,
mutation-tester, revenger, sentinel). Claims: R63-C1 (coverage, network-service class, capability
acquisition) and R63-C2 (depth, grader-class decision table). The frozen C1 predicate was **missed** on
its literal stderr clause (see `## Gate` and `## Mistakes`); the amendment is dated in
`plans/round-63-claims.md` (Amendment A1) and no run is re-scored as the record.

## Gate

**Sources opened this round (2026-11-03).**

- **S228** — TB2 `pypi-server` grader at pin `2fd12b88`,
  https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pypi-server/tests/test_outputs.py .
  Re-fetched by curl in the scout seat (`.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py`) and
  re-opened independently by the SourceReview seat (`.ufo/waves/round-63/w1/attack/S228-reopen.py`):
  sha256 `82c63517…650be4c` in both, = `corpus/evidence/round52/graders/SHA256SUMS` line 134; `cmp`
  byte-identical. Located quotes (≤25 words): `"http://localhost:8080/simple",` (:30) and
  `assert v.dotproduct([1, -1, 0, 0.01], [0, 0, 10, 0]) == 0` (:88). Tier A code.
- **S229** — PEP 503 "Simple Repository API", https://peps.python.org/pep-0503/ . Fetched by curl
  (`recon/S229-pep-0503.html`, sha256 `5b97cb7e…2c453c4f`, 20398 bytes), re-opened by SourceReview
  (`attack/S229-reopen.html`), byte-identical. Located quote (13 words):
  "Below the root URL is another URL for each individual project contained within" (:165). Tier A spec.

Both rows are appended to `corpus/SOURCES.md` (S228, S229; 220 → 222). Quote verdicts by SourceReview:
`verified` for both (`.ufo/waves/round-63/w1/attack/source-review.md`).

**Admit / reject decisions (LEARNING.md discernment).**

- ADMIT `corpus/knowledge/tb2-network-service-offline-grader.md` (network-service class, first offline
  replay of the `pypi-server` grader). Its Results section records run 1 as the frozen-predicate
  verdict (FAIL on the stderr clause) and the amended runs as detector evidence only.
- REJECT as a verdict: the amended-detector pass (runs 2–3) as the frozen C1 predicate. Reason: the frozen
  sentence was not met on the receipt of record; the amendment is an instrument change after data, so it
  is routed to the operator (`.ufo/l0-questions.md`) rather than admitted.
- REJECT the wave's first depth counter (share ≥ 0.90 only). It did not implement the frozen sentence,
  which also requires every path to resolve. Corrected to the frozen sentence before any measurement of
  the real section (`plans/round63_gate_checks.py`, the `resolved == total` clause).
- REJECT the coverage counter `grep -c 'CLASS network-service executed=1'` as an independent check
  (FreezeReview FR-02): the CLASS line is a fixed string the probe writes. The counter is the
  `--check-receipt` verdict (A1 §3).
- ADMIT the provenance-trio gate as the fix for the round-62 defect (`plans/round63_gate_checks.py trio`).

**Non-author spot-check (agree/disagree, for the closure).** The round's gate decisions were sampled by
non-author seats: FreezeReview (`freeze-needs-amendment`, 2 blockers, 14 majors) — **agree** with the
admit/reject of the counters, **disagree** with the freeze as written (its C1 counter and C2 pass sentence
were not the same sentence in doc, wave and code); ClaimFalsifier/critic — **agree** with the probe's
refusal behaviour under port contention, **disagree** with `--check-receipt` as evidence of a live run
(text re-derivation only; FALSIFIED as a counting command, survives as a structure check); SourceReview —
**agree** with both admits (both quotes located, both shas verified).

**Flip checks.** S227 unchanged (not touched). No existing row flipped. No rejected row written.

**Census.** Round start: `sources-census.sh validate --root … kengaku` → exit 0, 220 rows, 22 W04
warnings (`.ufo/waves/round-63/frontier/census-start.txt`). Round end: exit 0, 222 rows, 22 W04 warnings
(`.ufo/waves/round-63/frontier/census-end.txt`). The two appended rows added no W04: the warning count is
unchanged, and no new duplicate-URL class appeared.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **unobserved predicate text** — the frozen C1 clause "K2's pip stderr names localhost:8080" was written before any captured K2 stderr existed. Pip 26.2.1 renders the endpoint as `HTTPConnection(host='localhost', port=8080)`; the literal `localhost:8080` appears 0 times in stderr. The control receipt recorded only the exception class | `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt` (K2 `stderr_mentions_8080=False`, `PREDICATE R63-C1 fail`); `corpus/evidence/round63/k2-pip-stderr.txt` (`grep -c 'localhost:8080'` → 0; `grep -c 'port=8080'` → 5); `corpus/evidence/round63/control-k2.txt` (exception only) | none — the freeze's control receipt had no stderr capture, and no wave seat checked the clause against captured bytes before the scored run (the first battery's refusal was its own discovery) | QUALITY criterion Round63 (a frozen predicate that reads a tool's output is checked against a captured output of that tool before freeze). Shown able to fail: run 1 is the red of record — the literal detector failed on the real stderr. The amended detector (A1) is not admitted as the verdict |
| **counter narrower than the frozen sentence** — the depth counter tested only `share >= 0.90`; the frozen predicate requires every path to resolve and share ≥ 0.90 | `.ufo/waves/round-63/w1/attack/freeze-review.md` FR-01, FR-24; `.ufo/waves/round-63/w1/gate/gate_checks.py` pre-fix line 300 | FreezeReview (non-author, after the freeze, before any real-section measurement) | `plans/round63_gate_checks.py` requires `resolved == total` and `share >= 0.90`; the base run stays `PREDICATE R63-C2 fail` rc 1 (`corpus/evidence/round63/depth-before.txt`); the real section passes 24/24 (`corpus/evidence/round63/depth-after.txt`) |
| **a literal written by the writer** — the coverage counter `grep -c 'CLASS network-service executed=1'` reads a fixed string the probe emits regardless of K1 | `.ufo/waves/round-63/w1/attack/freeze-review.md` FR-02 | FreezeReview | Amendment A1 §3: the coverage counter is the `--check-receipt` verdict on the receipt of record, not the CLASS string |
| **round-62 provenance-trio omission** — the new round-62 knowledge entry opens with two `source:` lines and carries no `verified-at:` or `recheck:` (grep counts 0 and 0) | `corpus/lessons/round-62-verifier-spotcheck.md` §6 item 1; `corpus/knowledge/tb2-grader-class-census.md` | none in round 62; the round-62 closure routed it | `plans/round63_gate_checks.py trio`: red `TRIO fail missing=verified-at,recheck` on the round-62 entry (`corpus/evidence/round63/trio-red.txt`), green on the round-63 entry (`corpus/evidence/round63/trio-green.txt`). The round-62 entry is NOT rewritten in place (corrections are new entries); its drift stays named |
| **shared port contention** — the grader hardcodes `localhost:8080`; concurrent seats (the probe, a replay copy under another seat's draft dir, and a `python3 -m http.server 8080 --directory /tmp` process) contended for the port during the wave | `.ufo/waves/round-63/w1/PypiProbeBuild.md` "Notes for the L1" (refusals `SETUP port-8080-occupied`, `K2 confounded`); `.ufo/waves/round-63/w1/attack/evidence/c1/` | none — no wave rule serialized port-bound graders | the probe refuses rather than grading through a foreign listener (its own defence, shown by the critic's adversarial run). Process rule for future waves: one owner per fixed port, named in the item |

## Carried → closed / open

- Round-62 routed defect 1 (provenance trio): CLOSED as a gate (red-before and green shown); the old entry
  is named drift, not rewritten.
- L0 questions still open and routed around: `kengaku | round-25/33/51` (coverage cap),
  `kengaku | round-56` (L2 surface; ledger host column). New this round: `kengaku | round-63` (the
  amended K2 detector — admit or not).
- The frozen C1 predicate's verdict is a MISS as declared; no re-freeze, no narrowing.
