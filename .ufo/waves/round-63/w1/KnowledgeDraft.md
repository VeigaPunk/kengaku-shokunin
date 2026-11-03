# KnowledgeDraft — round 63, wave 1 (v1)

Seat report. Scope: draft the R63-C1 knowledge entry plus its gate block. No predicate, counter,
kill rule, leg vector or control was changed by this seat; the frozen file
`plans/round-63-claims.md` was read first and treated as the only rule source.

## Files written

| path | what |
|---|---|
| `.ufo/waves/round-63/w1/draft/corpus/knowledge/tb2-network-service-offline-grader.md` | the new knowledge entry (mirrors lane path `corpus/knowledge/tb2-network-service-offline-grader.md`) |
| `.ufo/waves/round-63/w1/draft/gate-block.md` | the gate block for S228 and S229 (splice target: the round-63 lesson `## Gate` table) |
| `.ufo/waves/round-63/w1/draft/corpus/evidence/round63/pypi-probe.txt` | copy of the build seat's probe receipt, kept with the entry so the results paragraph is re-derivable |
| `.ufo/waves/round-63/w1/draft/corpus/evidence/round63/k2-pip-stderr.txt` | copy of the probe's captured K2 pip stderr, the evidence for the rendering fact below |
| `.ufo/waves/round-63/w1/draft/corpus/evidence/round63/k2-pip-stderr-repro.txt` | this seat's own first-hand reproduction of the same pip install's stderr |
| `.ufo/waves/round-63/w1/draft/corpus/evidence/round63/k2-pip-stdout-repro.txt` | the matching stdout, which is where pip puts the index URL |
| `.ufo/waves/round-63/w1/KnowledgeDraft.md` | this report |

No lane file outside `.ufo/waves/round-63/w1/draft/` and this report path was written. The
scratch dir `/fast/scratch/hyaku/kengaku-r63/KnowledgeDraft/` was removed after the receipts were
copied.

## Verdict: both deliverables complete; C1 observed PASS

The probe receipt (build seat, `.ufo/waves/round-63/w1/build/pypi-probe.txt`, sha256
`b3d3ec1f…c5038db9eb`) carries, quoted verbatim:

```
CASE K1 leg=test_api observed=P expected=P exception=none index_pid=795645 wheel_sha256=6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6
CASE K2 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=none wheel_sha256=none
CASE K3 leg=test_api observed=F expected=F exception=AssertionError index_pid=959703 wheel_sha256=df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa
CASE K4 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=967177 wheel_sha256=b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92
PREDICATE R63-C1 pass
```

Observed leg vector **P/F/F/F** = the frozen vector. `K2 stderr_mentions_8080=True`,
`CLASS network-service executed=1`, `PREDICTION-VECTOR P/F/F/F derived=P/F/F/F`,
`CLASS-PROBE-EXIT=0`. The receipt's verdict lines were identical across every battery run
observed this round; only the `index_pid` values differ between runs. The receipt was stable
across two consecutive 270 s re-checks (mtime `15:24:01`, sha `b3d3ec1f…`) before quoting.

**Note for the L1 (not a rule change, a reading aid):** the K2 stderr clause is satisfied by
pip's **urllib3 host/port rendering**, not by the contiguous literal. The captured K2 stderr
names the endpoint as `host='localhost', port=8080` as two separate fields; the literal string
`localhost:8080` appears **0** times in that stderr (measured `grep -c 'localhost:8080'` → 0),
because pip 26.2.1 writes `Looking in indexes: http://localhost:8080/simple` to **stdout**. The
build seat's probe matches two endpoint forms (`ENDPOINT_PATTERNS`: `url`, `urllib3-host-port`).
A re-check that greps the stderr alone for the contiguous literal will read `False` and
mis-report a passing predicate as failing. Reproduced independently in this seat's scratch
venv (pip 26.2.1): stderr contains `port=8080` 5× and `localhost` 5×, `localhost:8080` 0×;
stdout carries the URL once. Both are kept in the seat's evidence dir.

**Timeline worth recording.** The first battery run **failed** the predicate: `K2
stderr_mentions_8080=False`, `PREDICATE R63-C1 fail` (that receipt is preserved by the build
seat as `pypi-probe-attempt1.txt`, sha256 `edab0cb8…`, with the same P/F/F/F leg vector). The
cause was the endpoint-name rendering above, not a grader or sandbox fault. The build seat
widened the endpoint match and re-ran; the predicate then passed. The frozen leg vector, the
predicate's three clauses and the kill rules were not changed at any point by this seat.

## Entry composition (what is in it, and what is deliberately not)

- Provenance trio first, in order, before the first `## ` heading: `source:` (S228, tier A
  code, with the pinned URL) → `verified-at:` (2026-11-03, base `c78749a5`) → `recheck:` (the
  frozen `--check-receipt` command).
- What the grader asserts: the pin, the grader sha256 (SHA256SUMS line 134) and the wrapper's
  (line 135), the install command with its hardcoded `--index-url` and version pin (S228 lines
  23, 24-32, 58), and the four `dotproduct` asserts (S228 lines 85-88), each with a line cite.
- Why it is `network-service` class: the census receipt line 11 (count=8, `pypi-server`
  among the members), the frozen detector regex at `plans/round62_c1_class_survey.py` line 93,
  and the base coverage line 21 (`classes-uncovered=network-service,…`); plus the base
  executed roster count (17, `pypi-server` absent).
- The do-nothing control K2: F, `CalledProcessError`, `corpus/evidence/round63/control-k2.txt`
  sha256 `73f1fa33…59100c9`, its line 5 quoted and its `rc=0` last line explained.
- The probe's sandbox design, taken from the frozen design (`plans/round-63-claims.md` lines
  39-43) and from the instrument that landed this wave
  (`.ufo/waves/round-63/w1/build/round63_c1_pypi_probe.py`): the grader's own `test_api()`,
  read-only grader bind with a run-time byte check, the lane-built PEP 503 index on
  127.0.0.1:8080, the probe-owned venv (read-only venv + writable `site-packages`), `env -i`
  with `PIP_CONFIG_FILE=/dev/null`, the loopback-only `/etc/hosts`, shared network with a
  bind-test refusal (`SETUP port-8080-occupied`, exit 2), the K2 confound refusal unless pip's
  own words are "Connection refused", and the run-time-derived expected vector.
- The frozen leg vector P/F/F/F and the predicate's three clauses, with the two kill rules.
- The S229 PEP 503 layout fact, quoted with its location and citing S229 with the URL.
- The NOT-claimed list: no claim about the unfetched upstream `test.py` simulator; no claim
  that the grader is solvable by any model; no claim about the host's 8080 beyond the bind
  test; and (added) no claim that the census's other seven `network-service` graders are
  replayable.
- The results paragraph, written **only** from the receipt's CASE and PREDICATE lines quoted
  verbatim, plus the supporting receipt lines and the measured rendering fact.

Body length: 119 lines after the title (within the 120-line limit). No `op://` reference; no
token-shaped literal — the only 64-hex strings are the wheel sha256 digests quoted verbatim
from the receipt.

## Gate block

| row | URL | access date | located quote | file:line | `wc -w` | verdict |
|---|---|---|---|---|---|---|
| S228 | `…/terminal-bench-2/2fd12b88…/pypi-server/tests/test_outputs.py` | 2026-11-03 | `assert v.dotproduct([1, 1], [0, 1]) == 1` | `recon/S228-pypi-test_outputs.py:85` | 7 | **LOCATED** |
| S229 | `https://peps.python.org/pep-0503/` | 2026-11-03 | `Below the root URL is another URL for each individual project contained within` | `recon/S229-pep-0503.html:165` | 13 | **LOCATED** |

Supporting quotes, same copies, same date: S228 `"http://localhost:8080/simple",` (`:30`, 1
word), S228 `assert v.dotproduct([1, -1, 0, 0.01], [0, 0, 10, 0]) == 0` (`:88`, 7 words), S229
`is replaced by the normalized name for that project, so a project named` (`:167`, 13 words) —
all three **LOCATED**. **No quote is UNLOCATED.** Every quote was re-checked with `grep -n -F`
against the lane's own copies under `.ufo/waves/round-63/w1/recon/`, and every quote is ≤ 25
words. The recon bytes were re-hashed after the quoting: S228
`82c63517…650be4c` (identical to the lane's committed capture and to SHA256SUMS line 134),
S229 `5b97cb7e…2c453c4f` (identical to this seat's independent re-fetch of the PEP URL).

## Verification run by this seat

- trio gate rule re-implemented locally against the new entry: `source:`, `verified-at:`,
  `recheck:` in order, within the first 12 lines and before the first `## ` heading (at line 7)
  → **pass**. The same rule against the round-62 entry `corpus/knowledge/tb2-grader-class-census.md`
  → `fail missing=verified-at:,recheck`, reproducing the claimed red-before.
- all four gate quotes re-located with `grep -n -F`; all five recon/entry hashes re-verified.
- the entry's quoted CASE lines and PREDICATE line diffed against the settled receipt:
  `diff <(grep '^CASE ' …) <(grep '^CASE ' …)` → identical; same for the PREDICATE line.
- host at measurement time: `ss -ltn | grep -c ':8080'` → 0 (no listener before the probe bound
  it); `/usr/bin/bwrap` present (bubblewrap 0.13.1).

## Out of scope / not done by this seat

- The entry is **not** landed at `corpus/knowledge/tb2-network-service-offline-grader.md`, the
  gate block is **not** spliced into the round-63 lesson, and S228/S229 are **not** appended to
  `corpus/SOURCES.md` — the L1 integrates those; this seat produced the drafts only.
- `plans/round63_c1_pypi_probe.py` and `plans/round63_gate_checks.py` are the build and gate
  seats' artifacts; this seat read but did not write them. At the time of writing, `plans/`
  still had no `round63*` file (the probe existed only under the wave build dir), so the
  entry's `recheck:` line names the frozen command even though the file is not yet at `plans/`.
- No tool was installed or upgraded by this seat; `RULES.md` was not consulted because no
  installation was needed. (No pacman transaction was run.)
- `corpus/evidence/round63/pypi-probe.txt` (the lane-level receipt path the frozen counting
  command names) does not yet exist; the build seat's receipt is at
  `.ufo/waves/round-63/w1/build/pypi-probe.txt`. The L1's copy decision is the L1's.
