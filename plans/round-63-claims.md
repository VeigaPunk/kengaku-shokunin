# Round 63 — frozen claims (kengaku, 2026-11-03)

Base tip `c78749a5` (`refs/heads/master` == `origin/master` at round start). This document is
written and committed BEFORE any scored run. Predicates, counters, kill rules and controls below
are fixed; a seat may not change them. A rule changed after any scored receipt is not this
claim's rule (kumitate r42). Any later amendment is a new dated section, never an edit.

Round shape: one v1 wave, 12 seats (`.ufo/waves/round-63/w1-spec.json`), build + attack.

## Declared claims (2), distinct axes

| claim | axis / capability | before → after | score effect |
|---|---|---|---|
| R63-C1 | coverage (lowest non-retired axis, L0-capped at 7) — capability acquisition `offline-network-service-grader-probe` | TB2 class `network-service`: 0 graders executed (8 members, `corpus/evidence/round62/class-survey.txt:11`) → 1 executed offline | score held at 7 (L0 cap `kengaku \| round-25/33/51`, still open) |
| R63-C2 | depth — decision table over the grader-class census | `SKILL.md` has 0 grader-class rows (base) → 16 rows, one per census class, each citing a resolvable receipt path | depth 9 → 10 iff the predicate passes |

Causal separation: C1 artifacts = the probe, its receipt, the knowledge entry, the capability row,
S228/S229. C2 artifacts = the SKILL.md section and the depth checker. They share no artifact
except the census receipt, which C2 reads and C1 does not write.

Frontier step (CORPUS.md rule 1 / §2b): C1 rests on S228 and S229, both opened live this round.
Mistake mined: round-62 knowledge entry `corpus/knowledge/tb2-grader-class-census.md` carries no
provenance trio (`grep -c verified-at` → 0, `grep -c recheck` → 0; routed defect 1 in
`corpus/lessons/round-62-verifier-spotcheck.md` §6).

---

## R63-C1 — offline execution of the `pypi-server` grader

**Grader under execution:** `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`,
sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c`
(= `corpus/evidence/round52/graders/SHA256SUMS` line 134; verified this round with `sha256sum`).
The grader's `test_api()` calls `install()`, which runs
`python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0`, then imports
`vectorops` and asserts four `dotproduct` values. The host has no listener on 8080 at round start
(`ss -ltnp` → none), but the grader hardcodes port 8080: the probe must prove the index it
reaches is its own, not a foreign service.

**Probe:** `plans/round63_c1_pypi_probe.py` (to be built in the wave, copied in by the L1).
Runs the grader's `test_api` inside a bwrap sandbox against a lane-built simple index
(PEP 503 layout, one wheel `vectorops-0.1.0`, built by the probe from frozen literal sources).
The sandbox's `python` is a probe-owned venv; no host pip config, no host credentials, no
network beyond loopback.

**Cases (frozen):**

| case | setup | expected `test_api` leg |
|---|---|---|
| K1 compliant | index on 127.0.0.1:8080 serves `vectorops-0.1.0` with a correct `dotproduct` | **P** |
| K2 do-nothing control | nothing listening on 8080; no index | **F** |
| K3 wrong math | index serves `vectorops-0.1.0` whose `dotproduct` returns `sum(a*b)+1` | **F** (AssertionError) |
| K4 wrong version | index serves only `vectorops-0.2.0` | **F** (`CalledProcessError` from install) |

**Leg rule:** P iff `test_api()` returns normally; F on any exception.

**Predicate R63-C1 (one sentence, the same in the plan, the probe's `check` and the receipt):**
pass iff the observed leg vector over K1–K4 equals the frozen vector P/F/F/F, AND K2's captured
pip stderr names `localhost:8080`, AND K1's receipt records the index server's own PID and the
served wheel's sha256.

**Counting command (re-derivable from committed bytes):**
`python3 plans/round63_c1_pypi_probe.py --check-receipt corpus/evidence/round63/pypi-probe.txt; echo $?`
→ last line `PREDICATE R63-C1 pass`, exit 0. Coverage counter: `grep -c 'CLASS network-service executed=1' corpus/evidence/round63/pypi-probe.txt` → 1.

**Kill rules:**
- K2 returns P (the target is reachable with nothing listening) → the counter or the grader
  reading is wrong; the claim is dead and the round reports it. Not patched, not re-frozen.
- K1 returns F → the probe or the candidate is wrong; the claim is a miss (honest stop). No
  re-freeze in this round.
- Any seat finds the probe reaching a foreign service on 8080 → predicate fails.

**Do-nothing control (run before this freeze):** `corpus/evidence/round63/control-k2.txt` —
the grader's `test_api` run with the venv on PATH and nothing on 8080. Observed:
`CONTROL-LEG test_api F CalledProcessError` (rc of the capture run: 0; sha256 of the capture file
`73f1fa330f02eecc9825e5538cb63c6d9fb76a404cb8a33ee067f408259100c9`). K2 = F as predicted; the
claim's counter is not already met by the control.

**Capability row (enters only if predicate passes):**
`offline-network-service-grader-probe` → runs a TB2 grader whose `install` step reaches a
localhost index, against a lane-built PEP 503 index, inside bwrap, with the leg vector frozen
above → `python3 plans/round63_c1_pypi_probe.py --check-receipt corpus/evidence/round63/pypi-probe.txt`
→ first working round 63.

---

## R63-C2 — depth: grader-class → offline replay recipe table

**Surface moved:** `SKILL.md` gains one new section, `## Decision table — grader class → offline
replay recipe`, placed after the existing benchmark-selection tables. It has exactly 16 rows, one
per class in `corpus/evidence/round62/class-survey.txt` (the `CLASS` lines, `container-image`
included). Columns: class · member count (copied from the receipt) · executed-status (from
`corpus/evidence/round52/graders/executed17.lst`, plus `pypi-server` if C1 passes) · replay
recipe (sandbox/stub/service needed, one line) · receipt pointer (a repo path that resolves).

Recipes are derived from the census receipt and from the executed probes' committed code
(`plans/round61_c1_cancel_probe.py` sandbox, `plans/round63_c1_pypi_probe.py` service, the round-59
openssl probe). A recipe for an un-executed class is marked `recipe-unexecuted` — it is not
claimed as replayed.

**Predicate R63-C2:** pass iff, in the new SKILL.md section, (a) there are exactly 16 class rows and
their names equal the set of `CLASS` names in the census receipt; (b) every count cell equals the
receipt's count for that class; (c) every backticked repo-relative path in the section resolves
(`test -e` from the lane root); and (d) the resolution share is ≥ 90 %.

**Counting command:**
`python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt; echo $?`
→ exit 0 and `PREDICATE R63-C2 pass`.

**Before (base, predicted at the freeze, measured by the executor from base bytes before any edit):** `git show c78749a5:SKILL.md` run through the same command → `PREDICATE R63-C2 fail` (0 class rows), exit 1. The base receipt is `corpus/evidence/round63/depth-before.txt`, produced before the SKILL.md edit lands.

**Kill rules:** any count cell mismatching the receipt → miss. Resolution <90 % → miss. Rows added
without a receipt pointer → miss. A miss is reported as a miss; the section is not narrowed after
landing.

**Depth verdict rule:** depth moves 9 → 10 only on pass. Depth stays 9 otherwise; the table's
existence alone does not move the score (anti-double-count, SCORECARD round 14 ruling).

---

## Frontier step — provenance-trio gate (mistake fix, red-before shown)

**Fix:** `plans/round63_gate_checks.py trio <file>` — exit 0 iff, within the first 12 lines and
before the first `## ` heading, the keys `source:`, `verified-at:`, `recheck:` appear in that order
(CORPUS.md "a new knowledge entry opens with its provenance trio").

**Red-before (committed receipt):** `trio corpus/knowledge/tb2-grader-class-census.md` → exit 1
(`TRIO fail missing=verified-at,recheck`). **Green:** the new entry
`corpus/knowledge/tb2-network-service-offline-grader.md` → exit 0. A fix counts only with both.

**Scope honesty:** the defect in the round-62 entry is not rewritten in place (CORPUS rule: corrections
are new entries). The round-62 entry gets a dated erratum appended to its lesson; the gate is what
captures the class for future entries.

---

## Sources (opened this round; rows appended only after the scribe drafts and the L1 validates)

- **S228** — TB2 `pypi-server` grader at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`
  (raw.githubusercontent.com `.../pypi-server/tests/test_outputs.py`), tier A (code, scope: the
  grader's install and assertion contract). Opened live by the scout; sha must equal the pinned
  sha above.
- **S229** — PEP 503 Simple Repository API, `https://peps.python.org/pep-0503/`, tier A (spec,
  scope: the `/simple/<name>/` index layout the probe serves). Opened live by the scout.

## Controls summary

- Do-nothing control: K2 (receipt committed before the freeze).
- Before-state counters: C2 base run (`depth-before.txt`), trio red (`trio-red.txt`, produced from base bytes before the new knowledge entry exists), C1 host state (`ss -ltnp` shows no 8080 listener, recorded in `.ufo/waves/round-63/w1/recon/`).
- Kill rules: stated per claim above; no rule is changed after data.
