# C1 counter review — C1RevCounterRule

## Scope and revision reviewed

Reviewed the C1 claim and counter, including A1 at `07ea208`, and the current counter at `de616d7` (2026-10-28). The current counter has just landed the capture-census and hand-read-set corrections; findings below distinguish those fixed draft defects from defects still present. No lane source files were edited by this seat. No tools were installed. No LSP device/server was available in the tool inventory; file/rule checks below are direct text and executable-fixture evidence, not LSP semantic results.

## Findings by severity

### High — the current counter admits fabricated confirmations and unverified prior art

`plans/round52_c1_grader_audit.py:271-293` checks only truthiness for `reader` and `confirmed`, and checks that `quote` is a substring of the capture. `prior_art()` at lines 226-231 only counts URL-shaped strings. It does not verify reader independence, that the quote locates the weakness, that a primary was fetched, that a finding is priced, or that any finding is `phenomenon-new`—although the frozen score rule at `plans/round-52-claims.md:94-97` depends on that last distinction.

**Fixture and result:** using a synthetic lane with all 184 capture paths, locally generated checksums, presence-only fake grader bytes, `confirmations.json` entries for two un-read candidate tasks with `quote: "assert"`, `reader: "unverified"`, and `confirmed: "false"`, plus `prior-art.md` containing only three `https://example.org/...` URLs and `labels.json` with an empty list, the current counter reported:

```
TASKS total=89 records=89 classified=89
CAPTURES expected=184 present=184 mismatched=0
CONFIRMED new=2 ['adaptive-rejection-sampler', 'bn-fit-modify']
PRIOR-ART ok=True urls=3
LABELS agree=0 of 0
PREDICATE R52-C1 pass
exit 0
```

The falsy-looking JSON string is truthy in Python; the quote is an arbitrary common substring; the reader is an unchecked string; the URLs are placeholders, not evidence of fetched primaries. This directly demonstrates an input passing without the claimed independent confirmation and prior-art work. `LABELS` is expressly evidence-only, but `0 of 0` is also accepted and provides no blind-label evidence.

**Per-leg verdicts:** CONFIRMED — **vacuous** for the independence/confirmation semantics; PRIOR-ART — **vacuous** for fetched-primary/per-finding/novelty semantics; LABELS — **vacuous as evidence at zero denominator**, though non-gating by frozen contract.

### High — the classifier treats comments and strings as executable behavior or checks

`PRESENCE`, `CONTENT`, `BEHAVIOUR` and `BEHAV_T` are raw substring regexes (`plans/round52_c1_grader_audit.py:33-50`); comments and string literals are not removed. Fixture `# subprocess is mentioned here, but nothing executes` with an otherwise presence-only test classified the file `V2` and the test `P2`. A presence marker only in a comment classified the file `V1`; a test containing only the comment `# assert path.exists()` plus `pass` classified `P1`. These are false semantic classifications: comments can suppress a real presence-only candidate as behavioural or create one without an actual assertion/check. The requested comment-only `subprocess` probe therefore observes V2 by the frozen lexical rule, but the semantic result is not behavioural. Marker parsing should distinguish executable code from comments/strings (or this should be explicitly characterized as lexical triage, not behavioral classification).

### Medium — the per-test split misses indented/class test methods

`TESTDEF = re.compile(r"^def ...", re.M)` at line 47 does not accept indentation, unlike file-level `TESTFN` at line 41. Fixture:

```python
class TestPresence:
    def test_artifact_exists(self):
        assert artifact.exists()

def test_content():
    assert open("/tmp/x").read() == "x"
```

Observed: file class `V3`; only the top-level `test_content` was split (`P3`); the class-based presence-only test was absent and the combined candidate flag was false. Thus a mixed grader can hide its presence-only test whenever it is declared as a class method. A class-only test fixture produced `classify_tests=[]`.

### Medium — the implementation's marker vocabulary differs from the frozen C1 rule

The frozen claim at `plans/round-52-claims.md:72-77` does not list `assert.*\bin\b` as a content marker, but the counter adds it at `CONTENT` line 36. For `def test_a(): assert 'x' in output`, the frozen listed vocabulary yields no presence/content/behavior marker and one test (`V4`); the counter returns `V3`. The same extra term makes a presence-only test with an error message containing the standalone word `in` classify as file-level `V3`, rather than the frozen-rule `V1`. The counter also adds `os.path.isfile` to presence and narrows `curl` to `curl ` compared with the claims' marker lists. These are rule drift, not merely implementation details.

## Required hand-written classification fixtures

| Fixture | Expected under frozen rules / semantic intent | Observed current counter | Assessment |
|---|---|---|---|
| `assert os.path.exists('/app/x')` and `assert open('/app/x').read().strip() == 'y'` | V3 (content marker defeats V1) | V3; per-test P3 | Sound for this case |
| One `test_` function with three plain equality asserts and no frozen markers | V4 (≤2 test functions) | File V4; per-test P3 because A1's `VALUE` includes `==` | File-level match; A1 per-test scale differs |
| Three `test_` functions, each with a plain equality assert and no frozen markers | V0 (>2 test functions) | File V0; per-test P3 for each | File-level match |
| Shell-only task (`tests/test.sh`, no `test_outputs.py`) | No primary Python class; record should be missing/error | `primary_grader()` returns `None`; `collect()` records V0 with `error="no test_outputs.py"`, excluded from classified count | Sound for missing-primary detection; frozen population itself has Python graders for all tasks. The 89 `test.sh` and one `verify.sh` capture files are not classified as graders by this instrument. |
| `subprocess` only in a comment, alongside a presence-only test | Semantically not behavioural; should remain eligible for presence-only review | File V2; when comment is inside the test block, P2 | False behavioural marker; candidate can be suppressed |

## Other legs and current status

| Leg | Verdict | Evidence / qualification |
|---|---|---|
| CAPTURES present/mismatched | **Sound for census and local digest consistency; vacuous for upstream byte provenance** | Current `de616d7` iterates all `capture_population` paths and counts absent sum entries as mismatches. A full synthetic set yielded 184/184 and zero mismatches. However, the counter validates bytes only against the locally supplied `SHA256SUMS`; the synthetic fake bytes plus a locally generated sums file passed. There is no expected digest/source check against the frozen upstream pin in the counter. |
| TASKS classified | **Vacuous for claimed pin authenticity** | A record is built and classified from each local primary capture. Fake primary bodies in the fixture produced 89/89 classified. The counter does not establish those bytes came from the frozen upstream pin; local hashes are not an upstream authenticity proof. |
| CONFIRMED new | **Vacuous** | As above: `confirmed: "false"`, arbitrary reader, and quote `"assert"` yielded two confirmations and predicate pass. Candidate and literal-substring checks exist, and the current read-set mapping correctly produced the 12 existing task IDs; those checks do not establish independence or a weakness-specific quotation. |
| PRIOR-ART | **Vacuous** | `prior_art()` returned `(True, 3)` for three `example.org` URL strings. No fetch, source-quality, finding linkage, or phenomenon-new check. |
| LABELS agree/total | **Vacuous as evidence; intentionally non-gating** | `labels.json: {"labels": []}` prints `0 of 0` and predicate still passes, consistent with the frozen text saying it is evidence-only. It cannot substantiate blind agreement without a positive denominator and verified blind-label provenance. |

### Previously committed A1 defects, corrected in `de616d7`

At `07ea208`, the capture loop incremented `present` once per task's primary grader (maximum 89) while comparing it to `capture_file_count=184`; thus `present == expected` was unreachable. It also skipped mismatch checks when a primary path had no `SHA256SUMS` entry. The hand-read regex returned `{'this', '0'}` for the 12 knowledge entries, allowing previously read tasks to count as new. The later `de616d7` change counts all capture-population paths, treats missing sum entries as mismatches, and derives the 12 task IDs from knowledge-entry names. These earlier defects are not reported as remaining defects in the current revision.

## Verification and residual risk

Custom fixture probes exercised the current counter and the requested classifier cases; no repository build, linter, or project test suite was run. Main integration should require fetched/pinned source digests (not only locally generated sums), typed `confirmed is True` plus an auditable independent-reader identity, a weakness-specific quote/reference, and per-finding fetched-primary/phenomenon classification before accepting C1. The exact claim’s phenomenon-new score rule remains unmeasured by the counter.

## Commands run

Working-directory changes were explicit. The core inspection/probe commands were:

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && git rev-parse HEAD && git status --porcelain=v1 -- plans/round52_c1_grader_audit.py plans/round-52-claims.md && git log --oneline -5
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin && python3 plans/round52_c1_grader_audit.py --lane .
mkdir -p /fast/scratch/hyaku/kengaku-r52/C1RevCounterRule/{tmp,fixtures,receipts}
cd /fast/scratch/hyaku/kengaku-r52/C1RevCounterRule && cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c1_grader_audit.py ./counter_frozen.py && cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52-tasks.json ./ && python3 probe.py
cd /fast/scratch/hyaku/kengaku-r52/C1RevCounterRule && cp /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round52_c1_grader_audit.py counter_latest.py && python3 probe_latest.py
cd /fast/scratch/hyaku/kengaku-r52/C1RevCounterRule && python3 class_shell_probe.py
```

The full fixture driver and generated lane existed only under `/fast/scratch/hyaku/kengaku-r52/C1RevCounterRule/` and were removed before handoff. No tool installs or version changes.
