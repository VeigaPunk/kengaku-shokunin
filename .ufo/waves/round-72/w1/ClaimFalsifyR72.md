# ClaimFalsifyR72 — falsification of R72-C1 and R72-C2

Seat: critic (leaf, no dispatch), round 72 wave w1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
tip `b6336136e0e891522b113a94d8e0bd65e0eae8de` (`git rev-parse master` at start and end). No
predicate, case table, vector, digest, kill rule, target, claim or instrument was edited. No git/jj
mutation, no tool install, no sibling lane, no `.ufo/state/`, no `corpus/` path written. Scratch
`/fast/scratch/hyaku/kengaku-r72/ClaimFalsifyR72` was deleted after this report was written; every
result this report relies on is quoted below (the scratch-only drivers are not reproduced).

Method guard rails that matter for reading the results:

* the C1 probe was **copied byte-identically** to scratch (`sha256 99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e`),
  equal to the working tree file and to `git show master:plans/round72_c1_hf_probe.py`, and imported
  with `sys.dont_write_bytecode = True`; `plans/__pycache__` gained no round-72 entry;
* the C2 gate was executed **from the lane** against fixture lanes that are byte copies of the
  lane's `SKILL.md` and `plans/round-71-claims.md` with exactly one edit, and that contain no
  `plans/*.py` and no `.git`. The gate reads only those two files, so a fixture lane is a faithful
  counterfactual for "what if the correction bytes were these".

## What I ran (command → rc)

| # | command | rc | verdict line |
|---|---|---|---|
| 1 | `python3 plans/round72_c2_routed_defects.py --lane .` (lane tip) | **0** | `E1a ok` `E1b ok` `E1c ok` `E2 ok` `DEFECTS n=0` `PREDICATE R72-C2 pass` |
| 2 | `python3 plans/round72_c2_routed_defects.py --lane . --selftest --work S/c2-work2` | **0** | `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True ok=True` |
| 3 | `python3 plans/round72_c2_routed_defects.py --lane . --mutants --work S/c2-work2` | **0** | `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1`, `ARM accept-green=ok refuse-red=ok attribution=ok` |
| 4 | `python3 S/probe_copy.py --lane L --check-receipt S/handwritten-tip.txt --work S/check-work5` (no battery ever run) | **0** | `DEFECTS n=0` `PREDICATE R72-C1 pass` |
| 5 | same checker over 6 mutated receipts (`S/falsify_c1b.py`, `S/falsify_c1c.py`) | 0 ×6, 1 ×1 | matrix below |
| 6 | `python3 S/falsify_c1.py` — nine `run_case` calls through the instrument's own function, `--port-lock` held, no `--receipt`, no `--evidence-dir` | **0** | 9/9 `derived` equal the frozen vectors, all `sandbox_rc=0` (112.98 s) |
| 7 | `python3 S/falsify_c1.py` §B — every server mode's own source run on an ephemeral port, L4 request replayed | 0 | mode matrix below |
| 8 | `python3 S/falsify_c1d.py` — canary + breaking parent `PYTHONPATH` stub, K1 and K7 | **0** | K1 `PPPP`, K7 `FPPP`, `canary=ABSENT`, `transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py` |
| 9 | `python3 S/falsify_c2.py` — 7 fixture lanes | **0** | every fixture: `E1a ok` `E1b ok` `E1c ok` `E2 ok` `DEFECTS n=0` `PREDICATE R72-C2 pass` |
| 10 | `python3 S/falsify_c2b.py` — impostor + non-git fixture lanes | **0** | both `DEFECTS n=0` `PREDICATE R72-C2 pass` |
| 11 | read-only provenance checks against the round-71 commits | 128 / 0 / 0 | table in C2-d |

`S = /fast/scratch/hyaku/kengaku-r72/ClaimFalsifyR72`; `L` = the lane.

---

# R72-C1 — coverage

## C1-a — a hand-written receipt passes `--check-receipt` with no battery: **attack lands**

**Sentence attacked** (frozen predicate, `plans/round-72-claims.md`): "`PREDICATE R72-C1 pass` iff
`python3 plans/round72_c1_hf_probe.py --lane . --check-receipt …` prints `DEFECTS n=0` and
`PREDICATE R72-C1 pass` **and exits 0 at the round tip**; the **receipt of record** carries nine
`VECTOR` lines with `agree=True`, … and a `PROVENANCE` line with `env_cleared=True`,
`allowlist_seen=9/9`, `distinct=1`, `canary_seen=0` and a `transformers_file` under `/venv/`".

**What I built.** `S/falsify_c1.py` stages the nine cases with the probe's own `prepare_work` /
`stage_case` (byte work, no server, no sandbox), takes `library_versions()`, `probe_blob_sha(lane)`
and `git_tip(lane)` from the instrument, and writes a receipt by hand; `S/falsify_c1b.py` repeats
that construction for three variants. That second driver — staging all nine cases and running three
`--check-receipt` invocations — completed in **4.99 s** of tool-reported wall time, so the whole
fabrication is a few seconds of file copying; the
`--check-receipt` path spawns only `git` and the venv `python3 -c` for `LIBRARIES` — no `bwrap`,
no listener, no case execution.

The receipt of record I hand-wrote and its verdict:

```
REV b6336136e0e891522b113a94d8e0bd65e0eae8de
GRADER sha256=61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857
INSTRUCTION sha256=29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1
MODEL tree_sha256=c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944 files=5
PROBE sha256=99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e
PROBE_BLOB sha256=99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e rev=b6336136e0e891522b113a94d8e0bd65e0eae8de
LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2
SANDBOX bwrap=bwrap port=5000 net=shared cleared_env=True
PROVENANCE env_cleared=True allowlist=PATH,HOME,LANG,PYTHONPATH,PYTHONNOUSERSITE,PYTHONWARNINGS,TMPDIR,HF_HUB_OFFLINE,TRANSFORMERS_OFFLINE allowlist_seen=9/9 cases=9 distinct=1 canary_seen=0 transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py
CASE K1 case_sha256=4512bfa2140124948903dc7b0f80941656f2b8bf18da8a6ef60d442f89e533f1 server_pid=- sandbox_rc=0
LEGS K1 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K1 expected=PPPP derived=PPPP agree=True
CASE K2 case_sha256=e0c2dc8e799f31a6e8a41413801c53930b10f6249041d368ce7a2f5105d2c3c8 server_pid=- sandbox_rc=0
LEGS K2 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=F test_api_error_handling=P
VECTOR K2 expected=PPFP derived=PPFP agree=True
CASE K3 case_sha256=36ce18bf679d0c12d5214386dad24178c545125be9f3575450a6f49c2c75acac server_pid=- sandbox_rc=0
LEGS K3 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=F test_api_error_handling=P
VECTOR K3 expected=PPFP derived=PPFP agree=True
CASE K4 case_sha256=eaff30ccaff69ff34e3e8c4ec0bdfb20984c83f5ed8245bbf0ff99ae24d61cbe server_pid=- sandbox_rc=0
LEGS K4 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=F
VECTOR K4 expected=PPPF derived=PPPF agree=True
CASE K5 case_sha256=d0e8574ca9dafacf7c2e51b6434aa3585b53b03237048057d14a2871d901572a server_pid=- sandbox_rc=0
LEGS K5 test_model_downloaded=P test_flask_api_running=F test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K5 expected=PFPP derived=PFPP agree=True
CASE K6 case_sha256=6317bec0d99e7c94bc0fd169655e32ee5c43900af5c8d3c6b4e2ebd132eaf7bd server_pid=- sandbox_rc=0
LEGS K6 test_model_downloaded=P test_flask_api_running=F test_sentiment_endpoint=F test_api_error_handling=F
VECTOR K6 expected=PFFF derived=PFFF agree=True
CASE K7 case_sha256=494f5d59138b69abdd11a2ea72d6b6f2aaf35d721a7b16e20f66f618c3ecbc1a server_pid=- sandbox_rc=0
LEGS K7 test_model_downloaded=F test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K7 expected=FPPP derived=FPPP agree=True
CASE K8 case_sha256=b229944fa7b9665ccb02854edce0127a7ee1b36deb8b5dc280eecd163add329a server_pid=- sandbox_rc=0
LEGS K8 test_model_downloaded=F test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K8 expected=FPPP derived=FPPP agree=True
CASE K9 case_sha256=3ecda97029e6108b91b8eae3cd31fa07fbed05c7f87c4daa5e7484e0850bf33f server_pid=- sandbox_rc=0
LEGS K9 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=F
VECTOR K9 expected=PPPF derived=PPPF agree=True
LEG-COVERAGE legs=4 seen_p=4 seen_f=4
SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=0
PREDICATE R72-C1 pass
```

`CHECK_RC=0`. So: **yes, it passes, and the checker's trust boundary is what limitation (v)
says.** The gaps are wider than (v)'s single example, per this mutation matrix (each receipt differs
from the one above only in the named field; every other digest is still re-derived from committed
bytes):

| variant | change | rc | what it shows |
|---|---|---|---|
| `S/handwritten-tip.txt` | none | **0** | a receipt with zero sandbox runs is accepted |
| stale revision | `REV` and `PROBE_BLOB rev` = `c6322972…` (round-71 tip) | **0** | "at the round tip" is not a checked clause; any ancestor of `master` passes `git_is_ancestor` |
| blob at a rev where it did not exist | `PROBE_BLOB sha256=<HEAD blob> rev=c6322972…` | **0** | the blob/rev pair is never re-opened; the receipt can claim a blob at a commit that lacks the file |
| no `SANDBOX` line | line dropped | **0** | the sandbox declaration is not part of the predicate's check |
| black-hole provenance path | `transformers_file=/venv/DOES-NOT-EXIST/…/transformers/__init__.py` | **0** | the provenance clause is `startswith("/venv/")`, not a resolution of that file |
| K9 declared an exception red | `EXC K9 test_api_error_handling=E` | **0** | the receipt may state that K9's L4 red was an exception, i.e. **not** the `:107` assert, and still pass |
| bare `CASE` lines | no `server_pid`/`sandbox_rc` fields | **1** | only because `parse_receipt` requires `len(parts) >= 5` on a `CASE` line (`DEFECT case-set receipt=[]`, `DEFECTS n=12`); not a witness rule — the two fields are free-text and may be false |

**Verdict.** Limitation (v) is accurate and was declared before data, so the claim sentence is not
dishonest. But the *frozen predicate* is weaker than the claim sentence it is supposed to witness:
`--check-receipt` cannot distinguish a realised replay from a written one, and "at the round tip" is
an unchecked property of the receipt, not a condition the checker enforces. Nine `VECTOR` lines with
`agree=True`, the `SUMMARY` arithmetic and the `PROVENANCE` line are all satisfiable from committed
bytes plus the host's `library_versions()` in ~5 s. Read strictly, "the receipt of record carries …"
does the whole work in the predicate, and nothing in the predicate establishes that there *was* a
receipt of record.

**Smallest safe correction** (not applied): make the predicate's command include
`--evidence-dir`, and extend `check_receipt` to read each `manifest.json` and require it to
re-derive the same `legs`/`exc`/`detail` as the receipt's `VECTOR`/`EXC` lines; change
`git_is_ancestor(rev)` for `REV` to `rev == git_tip(lane)`; and resolve `transformers_file` under the
`/venv` bind instead of a string prefix. That would make my six passing variants fail while changing
no case, vector, digest or kill rule.

## C1-b — K9's `PPPF` without the intended mechanism: **attack fails on the mechanism, lands on the evidence binding**

**Sentence attacked.** "the ninth case (`K9` `400-no-error-field`, `PPPF`) prices the
`assert "error" in error_data` site at `tests/test_outputs.py:107` that the round-71 eight-case table
could not reach".

**What I built.** `S/falsify_c1.py` §B loads every mode's server source with the probe's own
`server_source(mode)` and replays the grader's L4 request (`{"invalid_field": "This should cause an
error"}`, `tests/test_outputs.py:98-101`) and a valid L3 request against each. The only substitution
is the listening port (`5000` → an ephemeral port), because the template hard-codes 5000 and the
shared port is serialised by `port_lock`; the handler logic is untouched. Result of one full matrix
run (the handler branches only on `MODE` and on whether `text` is a non-empty string):

| staged mode | L4 status | L4 body | `error` key? | listening |
|---|---|---|---|---|
| `good` | 400 | `{"error": "missing text"}` | yes | yes |
| `wrong-label` | 400 | `{"error": "missing text"}` | yes | yes |
| `int-confidence` | 400 | `{"error": "missing text"}` | yes | yes |
| `no-400` | **200** | `{"sentiment": "negative", "confidence": {…}}` | no | yes |
| `root-drops` | 400 | `{"error": "missing text"}` | yes | yes |
| `400-no-error-field` | 400 | `{"detail": "missing text"}` | **no** | yes |
| `none`* | 400 | `{"error": "missing text"}` | yes | yes |

`*` `none` is not a staged mode: `stage_case` writes no `server.py` and `run_case` invokes the
harness with `none`, so the row only shows that the template's default branch answers 400-with-
`error`; it is listed for completeness, not counted as a mode.

**Answer: no.** Within the frozen mode set only `400-no-error-field` returns a 400 whose body lacks
`error`; `no-400` returns 200, and no mode can produce a non-JSON 400 from the grader's own request.
The intended mechanism is unique. The real instrument agrees on the assert sites (`run_case`, #6):

* `K4` → `AssertionError: API should return 400 for invalid request format` (`:103`)
* `K9` → `AssertionError: Error response should contain 'error' field` (`:107`)
* `K2` → `…should be classified as positive` (`:86/:90`); `K3` → `Confidence scores should be floats` (`:77/:80`)
* `K7` → `Model directory not found` (`:13`); `K8` → `Failed to load model or tokenizer: … not a valid JSON file` (`:22`)
* `K5` → `Could not connect to the Flask API on 0.0.0.0:5000` (`:31`, via `except ConnectionError`)

**Residual that does land.** (i) The *vector* `PPPF` is reachable without K9 — K4 already produces
it — so K9's novelty is only the assert site, exactly as the sentence says. (ii) The receipt of
record cannot witness that novelty: K4 and K9 lines are identical in `LEGS`/`VECTOR` and differ only
in `case_sha256` (a digest of the *staged input*, not of the outcome); the assert-site evidence
(`detail`) lives only in the per-case `manifest.json`, which the frozen predicate never names. A
receipt that says `EXC K9 …=E` is accepted (C1-a table). So "K9 prices `:107`" is true of the run I
made, and unwitnessed by the artefact the predicate scores.

**Smallest safe correction.** Add the capture manifest to the predicate and check the `detail`
string family for K4 and K9 (`:103` vs `:107`), as in C1-a.

## C1-c — "every one of its four legs is witnessed both `P` and `F`": **attack fails**

**Sentence attacked.** "a **nine-case** frozen table in which every one of its four legs is
witnessed both `P` and `F`".

**What I built.** Nine direct `run_case` calls (#6) — no receipt, no evidence dir, shared port lock
held per case. All nine derived exactly the frozen vectors (`agree` 9/9), `sandbox_rc=0` for all,
`server_pid=3` for the eight served cases and `-` for K6. Per-leg witness classification from the
instrument's own `exc`/`detail` fields:

| leg | P witnesses | F witnesses | F produced by |
|---|---|---|---|
| L1 `test_model_downloaded` | K1-K6, K9 | K7, K8 | `AssertionError` both (`:13` direct; `:22` `assert False` inside `except Exception`) |
| L2 `test_flask_api_running` | K1-K4, K7-K9 | K5, K6 | `AssertionError` both (`:31` `assert False` inside `except ConnectionError`) |
| L3 `test_sentiment_endpoint` | K1, K4, K5, K7-K9 | K2, K3, K6 | `AssertionError` (`:86/:90`, `:77/:80`); K6 is a raw `ConnectionError` on `exc` |
| L4 `test_api_error_handling` | K1-K3, K5, K7, K8 | K4, K9, K6 | `AssertionError` (`:103`, `:107`); K6 is a raw `ConnectionError` on `exc` |

**Answer: no leg's F is witnessed only by an exception.** Every leg has at least one
`AssertionError` F witness; K6's L3/L4 are extra exception witnesses, not the only ones. The claim's
literal wording holds on this table.

Two calibrated qualifications, worth a sentence in the round report rather than a defect:

1. L2 is the weakest leg: its P is an assertion-free `requests.get` whose response is discarded
   (`test_outputs.py:29`), and its F is the same code path's exception converted by the grader's own
   `assert False`. P and F are "no exception" vs "exception"; the leg never asserts anything about
   the API. Limitation (iv) declares the status-check half of this; it does not say that L2's F is
   also synthetic.
2. L1's K8 F is likewise an `assert False` inside `except Exception` (`:22`), so two of the four
   legs' F witnesses are grader-synthesised assertions rather than failed assert sites. The table
   still witnesses both polarities per leg, which is what the claim says.

## C1-d (extra) — the isolation clause: mechanism corroborated, witness wording imprecise

**Sentence attacked.** "the sandbox is proven isolated: it runs under `bwrap --clearenv` with an
explicit nine-variable allowlist and records its **own** `transformers.__file__`, so the same
`transformers` stub that changed the round-71 table on the parent `PYTHONPATH` is invisible here".

**What I built.** `S/falsify_c1d.py`: plant `R72_CANARY` via the probe's own `canary_env()` and a
`transformers/__init__.py` that raises on import on the **parent** `PYTHONPATH`, then run K1
(`good`/`good`) and K7 (`absent`/`good`) through `run_case`.

Observed: K1 `PPPP`, K7 `FPPP`, `sandbox_rc=0`; `prov.canary="ABSENT"`; `prov.transformers_file=
"/venv/lib/python3.13/site-packages/transformers/__init__.py"`; `env_keys` =
`HF_HUB_OFFLINE,HOME,LANG,PATH,PWD,PYTHONNOUSERSITE,PYTHONPATH,PYTHONWARNINGS,TMPDIR,
TORCHINDUCTOR_CACHE_DIR,TRANSFORMERS_OFFLINE` (K1) and without `TORCHINDUCTOR_CACHE_DIR` (K7). The
stub did not load; the canary did not leak. **The isolation clause is corroborated on the real
instrument** — this is the strongest positive datum of the seat, and it independently reproduces the
mechanism the `--stub-control` receipt is meant to print.

Precision note: `allowlist_seen=9/9` is computed as "every case's observed key set is a **superset**
of the nine allowed names" (`battery_lines`: `set(env_keys) >= set(allow_names)`), so it is a single
boolean rendered as 9/9 and it cannot detect keys that reached the sandbox outside the allowlist.
The observed sets do carry `PWD` and (K1) `TORCHINDUCTOR_CACHE_DIR`, both set inside the sandbox by
`--chdir` and the torch import, not inherited — consistent with `--clearenv`, but the receipt line
alone would not have shown an inherited extra. The mechanism is `bwrap`; the witness is weaker than
"exactly nine variables".

---

# R72-C2 — calibration

## C2-d — a junk erratum satisfies E1b and E2 without correcting anything: **attack lands**

**Sentence attacked.** "**R71-R7** (two `plans/round-71-claims.md` labels claim a freeze-commit
content the freeze commit does not hold) are closed by corrections that a re-deriving gate moves
from `DEFECTS n=6` to `DEFECTS n=0`", plus the check definitions "`E1b` the round-71 claims doc
carries an appended erratum quoting both superseded labels verbatim and naming both true revisions"
and "`E2` positional append-only: both superseded sentences still occur **above** the erratum".

**What I built.** Byte copies of the lane's `SKILL.md` (so E1a is green) and
`plans/round-71-claims.md` with only the erratum replaced/appended. Five fixture lanes under
`S/fx-*`, each run with the lane's gate: `python3 plans/round72_c2_routed_defects.py --lane S/fx-<name>`.

| fixture | erratum content | rc | gate stdout |
|---|---|---|---|
| `junk-hollow` | quotes both labels, names both revisions, and says "Nothing above is superseded … this block fixes nothing" | **0** | `E1a ok` `E1b ok` `E1c ok` `E2 ok` `DEFECTS n=0` `PREDICATE R72-C2 pass` |
| `junk-swapped` | states the **opposite** attribution (control→`d8a77d3f`, red-before→`c80fcdb3`) | **0** | same, pass |
| `junk-code` | only a fenced block with the two labels, the two revisions and the word `superseded` | **0** | same, pass |
| `impostor` | both original superseded sentences **deleted** above the erratum and replaced by unrelated sentences that merely contain the label strings; junk erratum | **0** | same, pass |
| `nongit` | fixture lane has no `.git` at all; revisions are bare tokens | **0** | same, pass |

`junk-hollow` verbatim (fixture text):

```
## Errata — round 72 (junk A: hollow, corrects nothing)

This block is deliberately hollow. It quotes `Do-nothing control (committed at freeze)` and
`Red-before (committed at freeze)` only as label strings, and writes the tokens c80fcdb3 and
d8a77d3f only as hex strings with no correction attached to either. Nothing above is
superseded: both sentences above stand exactly as written and this block fixes nothing.
```

`impostor` proof that E2 is a label-substring check, not a sentence-preservation check: the fixture
contains neither original sentence (`"The same eight case ids staged"` absent; `"records the gate at"`
absent) and still prints `E2 ok`.

**Answer: yes, the gate accepts all of it.** E1b is "both label substrings present in the block,
both revision substrings present in the block, and the word `supersed` present"; E2 is "the label
strings' **first** occurrence is before the heading, the heading is the file's last `##`, and the
block has ≥3 non-empty lines". Attribution, negation, and sentence identity are not checked, and the
revisions are never opened in git (the `nongit` fixture proves that).

**Calibration — this is a gate-discrimination finding, not a data falsification.** The *committed*
erratum is factually correct; I verified its three load-bearing claims read-only:

| check | rc |
|---|---|
| `git cat-file -e d8a77d3f:.ufo/waves/round-71/c1-control.txt` | **128** (absent — as the erratum says) |
| `git cat-file -e d8a77d3f:.ufo/waves/round-71/c2-red-before.txt` | **0** (present — as the erratum says) |
| `git cat-file -e c80fcdb3:.ufo/waves/round-71/c1-control.txt` | **0** (present — the control landed here) |
| `git log --diff-filter=A -- .ufo/waves/round-71/c1-control.txt` | added in `c80fcdb3` |

So R71-R7's closure holds on the bytes; what does not hold is "closed **by a re-deriving gate**" in
any discriminating sense — the gate would have passed a block that asserts the opposite and a
document that no longer contains the sentences it claims to preserve.

**Smallest safe correction** (not applied): (1) replace the two label constants with the full
superseded sentences and require those exact sentences above the erratum (kills `impostor`);
(2) require each label and its revision to share a line/paragraph with the fixed mapping (kills
`junk-hollow` and `junk-swapped`); (3) derive the two revisions from git (`git log --diff-filter=A --
<path>` and `git cat-file -e <rev>:<path>`) instead of hard-coding `TRUE_REVISIONS`, and fail when
the lane is not a repository (kills `nongit`).

## C2-e — a registry row that satisfies E1a while being factually wrong: **attack lands**

**Sentence attacked.** "**R71-R1** (neither round-71 instrument has a `SKILL.md` `## Gate/probe
registry` row) … closed by corrections that a re-deriving gate moves from `DEFECTS n=6` to
`DEFECTS n=0`", plus "`E1a` every instrument in `INSTRUMENTS` has an eight-column `SKILL.md` registry
row whose entry cell names its script, whose kind is `gate`/`probe`, and whose owner is `kengaku`".

**What I built.** Fixture `SKILL.md` copies with the four instrument rows replaced or contradicted.
Each fixture lane contains only `SKILL.md` and `plans/round-71-claims.md` — **no `plans/*.py` at
all** — and still earns `E1a ok`.

| fixture | rows | rc | gate stdout |
|---|---|---|---|
| `wrong-kind-entry` | 8 columns, right path, kind **swapped** (`round72-c1` labelled `gate`, `round72-c2` labelled `probe`), entry `python3 <script> --frobnicate --erase-everything`, verdict map `0 fail · 1 pass`, self-test `--nonesuch`, write scope "read-write, whole lane" | **0** | `E1a ok … DEFECTS n=0` |
| `defunct-entry` | entry cell contains the script path only in the sentence "this instrument is superseded; do not run `<script>`" — no command at all | **0** | `E1a ok … DEFECTS n=0` |
| `dup-rows` | the real table untouched, then four appended rows for the same names with `kind=gate`, no script named, `owner=somebody-else` | **0** | `E1a ok … DEFECTS n=0` (first row wins: `by_name.setdefault`) |
| `shadow` | four `…-shadow` rows appended with bogus entries | **0** | `E1a ok … DEFECTS n=0` |

Example row from `wrong-kind-entry` (verbatim, one of four):

```
| `round72-c2-routed-defects` | probe | `python3 plans/round72_c2_routed_defects.py --frobnicate --erase-everything` | `0` fail and delete the tree · `1` pass | `--nonesuch` | pinned to the value of the day | read-write, whole lane | kengaku |
```

**Answer: yes, the gate accepts it.** E1a checks four things only: the row exists exactly once by
*first* name, it has exactly 8 cells, cell 3 **contains** the script path as a substring, cell 2 is
the token `gate` or `probe`, and cell 8 is `kengaku`. It never checks that the script exists, that
the kind matches the instrument's actual behaviour, that the entry is runnable or even a command,
or that the verdict map / self-test / pinned values / write scope say anything true. Duplicates are
invisible because `by_name.setdefault` keeps the first row, so an appended contradicting row is
silently ignored — a duplicate-authority hole in a gate whose sibling in round 52 already has a
`DUPLICATE` leg.

**Calibration.** At the freeze commit (`git show b6336136:SKILL.md`) the four rows are 8 columns,
kinds `probe, gate, probe, gate`, owner `kengaku`, entry `python3 <script> --lane .` — accurate for
the instruments they name. R71-R1's closure holds on the bytes; what fails is the gate's ability to
distinguish a true row from a false one. This is not only a fixture result: while this seat ran, a
concurrent sibling edited `SKILL.md` in the working tree and **relabelled both C1 probe rows from
`probe` to `gate`** (observed at cleanup; not this seat's write). The gate on that working tree
still prints `E1a ok` … `DEFECTS n=0` … `PREDICATE R72-C2 pass`, rc 0 — a live instance of the same
hole, in the lane's own bytes, where a probe that answers `0` on a data line is now advertised as a
gate whose `0` means pass.

**Smallest safe correction** (not applied): pin the expected kind in `INSTRUMENTS`
(`(name, script, kind)`), require the entry cell to start with `python3 <script>` (not merely contain
the path), require `(lane / script).exists()`, and fail on duplicate row names (the round-52
`DUPLICATE` leg is the existing pattern). The remaining three columns are free text and should be
described as unverified in the claim rather than silently counted.

## C2-f (extra) — the metric reproduces, but the fixture matrix is closed under the gate's own vocabulary

Running the claim's own two commands at the tip (#2, #3) reproduces the claim exactly, rc 0 both:

```
SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True ok=True
MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1
ARM accept-green=ok refuse-red=ok attribution=ok
```

So the second sentence of R72-C2 is reproducible: the metric is real, not a stored tally. But the
matrix's green fixture is built by `claims_fixture()`/`registry_row()` — the gate's own templates —
and the seven red fixtures are variations of the same templates (`registry="cols"/"owner"`,
`paraphrase`, `revisions=False`, `errata_at_top`, `trailing_section`, `body_paraphrase`). The metric
therefore measures **rejection** of template-derived reds; it has no false-accept arm, and none of
its fixtures encode a semantically junk *accepted* lane. C2-d and C2-e are exactly such lanes and
every one of them passes. That is the gap the "six semantic mutants" sentence does not cover: the
mutants are semantic in the sense that each disables a comparison, but every comparison they disable
is one the fixture matrix already knows how to red.

Secondary observation on the mutant arm: `attribution_ok` is computed as "the mutated gate still
refuses *some* red fixture belonging to another check", which is a cross-check specificity test, not
an attribution of the kill to the target check; the kill itself is `escapes=1` among the target's
own reds. The printed `attribution=ok` is therefore true but weaker than the word suggests.

---

# Calibration ledger

| claim sentence | attack | result | severity |
|---|---|---|---|
| C1 predicate: "exits 0 at the round tip; the receipt of record carries …" | C1-a hand-written receipt, 7 variants | **lands** — 6 of 7 pass, incl. a stale base revision, an unresolved `/venv` path and a K9 red declared an exception; only the bare-`CASE` variant fails, on a parser arity quirk | predicate-wording defect (declared limitation (v) keeps the claim honest) |
| C1: "K9 … prices the `assert "error" in error_data` site at `:107`" | C1-b mode matrix + real `run_case` | **mechanism holds** (no other mode yields 400-without-`error`); **evidence binding fails** (receipt cannot show the assert site; `PPPF` itself is reachable via K4) | predicate-wording defect |
| C1: "every one of its four legs is witnessed both `P` and `F`" | C1-c nine-run witness table | **fails** — every leg has a genuine assertion F; K6's exceptions are extra | none; two qualifications for the round report (L2's P/F are both exception-absence/presence; K8's F is synthesised) |
| C1: "the sandbox is proven isolated … stub … invisible here" | C1-d canary + parent `PYTHONPATH` stub | **corroborated** on the real instrument; `allowlist_seen` is a superset boolean, not exactness | none; precision note |
| C2: "R71-R7 … closed by a re-deriving gate" | C2-d five junk errata + git re-derivation | **lands** — gate accepts all five; the committed erratum itself is factually right | gate-discrimination defect (data is true, gate is not a witness) |
| C2: "R71-R1 … closed by a re-deriving gate"; E1a definition | C2-e four wrong-row fixtures + duplicate rows | **lands** — gate accepts all four; committed rows are accurate | gate-discrimination defect |
| C2: "fixture matrix that kills six semantic mutants … attributes every kill" | C2-f reproduction | **reproduces exactly**; matrix is template-closed, no false-accept arm | metric-scope defect (wording) |

Net: **R72-C1's act is real on this host** — I independently reproduced all nine frozen vectors,
including K9's `:107` red, and the `--clearenv` mechanism under an injected parent stub. What I can
falsify is the *artefact discipline* around it: the predicate's `--check-receipt` accepts a
hand-written receipt, including a stale revision, an unresolved provenance path and a K9 red that it
declares to be an exception. **R72-C2's two routed defects are genuinely closed on the bytes** (rows
accurate, erratum accurate) but not *by the gate*: the gate's four checks are token/position checks
that accept a hollow, self-negating, falsely-attributed erratum and rows whose kind, entry and
verdict map are fabricated.

# Smallest safe corrections (reported, not applied)

1. `check_receipt`: `REV == git_tip(lane)`; resolve `transformers_file` under the `/venv` bind; read
   `--evidence-dir` manifests and require `legs`/`exc`/`detail` to re-derive the receipt's
   `VECTOR`/`EXC` lines; check `detail` for K4 (`:103`) and K9 (`:107`) separately.
2. `battery_lines`/`check_receipt`: record and check the exact `env_keys` set, not just
   "superset of the 9 allowed names".
3. `check_e1_errata`: full superseded sentences (not labels) above the erratum; label→revision
   attribution on one line; revisions derived from git, and a non-repository lane fails.
4. `check_e2_positional`: compare the exact sentences, not `text.find(label)`.
5. `check_e1_registry`: pin each instrument's kind; require `python3 <script>` as the entry prefix;
   require the script to exist; fail duplicate row names.

# Hygiene

No instrument, claim, case table, vector, digest, kill rule or target edited; no file in the fleet
repo, a sibling lane, `.ufo/state/`, `.scratch/` or `corpus/` written. No `git add/commit/push/
checkout/reset/stash/pull`, no `jj` mutation, no `agent://all`. No tool installed or upgraded
(pacman paused; nothing needed). Scratch discipline: all work under
`/fast/scratch/hyaku/kengaku-r72/ClaimFalsifyR72`, deleted at the end of this seat; the shared lock
`/fast/scratch/hyaku/kengaku-r72/port5000.lock` was used for every case run and is left in place for
the wave. `/tmp` gained nothing from this seat; `plans/__pycache__` gained no round-72 entry (it is
another seat's import cache).

Concurrent sibling edits observed at cleanup and **not** written by this seat: `LOG.md`,
`SCORECARD.md`, `SKILL.md` (both C1 rows relabelled `probe` → `gate`, see C2-e), `corpus/README.md`,
`corpus/SOURCES.md`, `corpus/knowledge/tb2-hf-model-inference-provenance.md`. The frozen surface is
untouched: `git status --porcelain -- plans` is empty, so `plans/round-72-claims.md`,
`plans/round72_c1_hf_probe.py` and `plans/round72_c2_routed_defects.py` are byte-identical to
`b6336136`.
