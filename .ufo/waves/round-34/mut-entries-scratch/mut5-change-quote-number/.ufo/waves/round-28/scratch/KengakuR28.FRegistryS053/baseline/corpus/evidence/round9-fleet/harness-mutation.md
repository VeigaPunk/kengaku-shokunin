# Round-8 harness mutation report — parser/grader adversarial battery (kengaku r9)

Target: `corpus/evidence/round8-horizon/horizon.py` @ HEAD `f147a27` (functions `extract_json_block`
L38-47, `grade_state` L119-123, `grade_c` L270-289, `valid_latin` L232-236, `rows_perm_only`
L238-241, `col_conflict_free` L229-230). Method: 50 synthetic adversarial cases against verbatim
copies; runtime fidelity check re-execs the original source text and cross-checks every case;
blast radius re-extracts and re-grades all 258 non-meta records of `results.jsonl`.
OFFLINE (no HTTP). No repo writes.

- Script: `/tmp/kengaku-r9/test_harness.py` — run: `python3 /tmp/kengaku-r9/test_harness.py` (exit 0)
- Full output also at `/tmp/kengaku-r9/battery_output.txt`.

## Findings at a glance

| # | Severity class | Defect | Live in r8 data? | Blast radius |
|---|---|---|---|---|
| D1 | **MODEL error → PASS** | `grade_c` `ok` ignores `over_repair`; `preserved` trusts self-declared violations (L279, L287-288) | **YES — 1 record** | FIX-O flips 1: C-benign rep0 `ok` True→False → SUMMARY C-benign 1/4 → 0/4 |
| D2 | MODEL/harness artifact → PASS (latent) | `extract_json_block` returns an EARLIER fence when the final fence is truncated/unmatched (L39-42) | no (0 events) | FIX-P flips 0 |
| D3 | MODEL error → PASS (latent) | `grade_state` folds `5.0`/`true` into `5`/`1` via Python `==` (L121-122) | no (0 floats/bools/nulls) | FIX-T flips 0 |
| D4 | nwrong undercount (latent) | extra key with `null` value → `(ok=False, nwrong=0)` (L121-122 `.get` None-equality) | no | ok direction still correct |
| D5 | fragment-as-answer (latent) | fenceless ≥2-level nested JSON → innermost fragment parsed as the answer (L43-46) | no (sanity 188/188) | 0 |

Everything else the battery attacked (multi-fence selection, fenceless dicts, uppercase/inline/
zero-width labels, orphan closers, arrays, trailing commas, non-dict parses, wrong/under repair
targets, string-vs-int values, key order, zero-valued MOV keys) classified **correctly**.

## Import side-effect (why functions are copied, not imported)

`horizon.py` L15-16 execute at module level:
`os.makedirs("/tmp/bench-r8", exist_ok=True)` and `LOGF = open("/tmp/bench-r8/results.jsonl", "a")`.
Merely `import horizon` creates `/tmp/bench-r8` and append-opens the live round-8 results file
(creating it if absent) — a re-run analysis could silently append to or resurrect corpus data.
The battery therefore embeds verbatim copies (provenance comments per function) and adds a
**fidelity check**: the six function defs are extracted from the repo source text, exec'd, and run
against all 50 cases — **0 divergences**. Severity: harness hygiene, not a scoring bug.

## Battery output (verbatim from `python3 /tmp/kengaku-r9/test_harness.py`)

```
FIDELITY: copies vs horizon.py source-extracted originals
  divergence across 50 cases x 6 fns: 0
ID   FAMILY            EXPECTED                                             OBSERVED                                                   VERDICT
--------------------------------------------------------------------------------------------------------------------------------------------
E01  extract           illustrative fence before answer -> answer dict      {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E02  extract           final fence truncated (finish=length shape) -> parse None {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} FAIL
E03  extract           E02 pipeline grade -> ok must be False (masking check) (True, 0)                                                  FAIL
E04  extract           no fence, bare balanced dict at end -> dict          {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E05  extract           fenced nested one-level dict -> full dict            {'nails': 5, 'meta': {'src': 1}}                           PASS
E06  extract           fenceless 2-level nesting -> outer dict (not fragment) {'min': {'low': 1}}                                        FAIL
E07  extract           only fence truncated, no earlier fence -> None       None                                                       PASS
E08  extract           fenced dict with trailing comma -> None (strict JSON) None                                                       PASS
E09  extract           answer fence then apology w/ stray dict -> answer fence {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E10  extract+grade     float values 5.0 vs int 5 -> grade ok must be False (spec: integers) (True, 0)                                                  FAIL
E11  extract+grade     JSON true vs int 1 -> grade ok must be False (type error) (True, 0)                                                  FAIL
E12  extract           empty string -> None                                 None                                                       PASS
E13  extract           fenced JSON array (C-cell shape) -> list             [['A', 'B', 'C', 'D'], ['B', 'C', 'D', 'A'], ['C', 'D', 'A', 'B'], ['D', 'A', 'B', 'C']] PASS
E14  extract           zero-width space inside dict body -> None (invalid JSON) None                                                       PASS
E15  extract           zero-width space in fence label -> dict via fallback {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E16  extract           uppercase ```JSON label -> dict via fallback         {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E17  extract           inline fence, no newline after label -> dict via fallback {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E18  extract           orphan closer: bare dict then ``` (real A-CKPT r8 shape) -> dict {'nails': 5, 'bolts': 2, 'screws': 3, 'washers': 4, 'hinges': 6} PASS
E19  extract           plain 'ok' text -> None                              None                                                       PASS
E20  extract           fence marker inside JSON string value -> dict (fallback rescue) {'note': 'use ```json fences', 'nails': 5}                 PASS
G01  grade_state       extra key -> (False,1)                               (False, 1)                                                 PASS
G02  grade_state       missing key -> (False,1)                             (False, 1)                                                 PASS
G03  grade_state       same items, different key order -> (True,0)          (True, 0)                                                  PASS
G04  grade_state       string '5' vs int 5 -> (False,1)                     (False, 1)                                                 PASS
G05  grade_state       null value vs int -> (False,1)                       (False, 1)                                                 PASS
G06  grade_state       non-dict got: list -> (False,len(want))              (False, 5)                                                 PASS
G07  grade_state       non-dict got: str                                    (False, 5)                                                 PASS
G08  grade_state       non-dict got: None                                   (False, 5)                                                 PASS
G09  grade_state       both empty dicts -> (True,0)                         (True, 0)                                                  PASS
G10  grade_state       zero-valued key present after MOV -> (True,0)        (True, 0)                                                  PASS
G11  grade_state       zero-valued key dropped -> (False,1)                 (False, 1)                                                 PASS
G12  grade_state       float 5.0 vs int 5 -> (False,1) per integer spec     (True, 0)                                                  FAIL
G13  grade_state       bool true vs int 1 -> (False,1) per integer spec     (True, 0)                                                  FAIL
G14  grade_state       extra key w/ null value -> nwrong must be 1, not 0   (False, 0)                                                 FAIL
C01  grade_c/conflict  minimal repair viol[3] + valid square -> ok True     ok=T viol_ok=T sq=T pres=T over=F parse=T                  PASS
C02  grade_c/conflict  under-repair viol[] + unchanged conflict square -> ok False ok=F viol_ok=F sq=F pres=T over=F parse=T             PASS
C03  grade_c/conflict  over-repair viol[1,2,3] full rewrite -> spec ok False ok=T viol_ok=T sq=T pres=T over=T parse=T                   FAIL
C04  grade_c/conflict  over-repair viol[1,3] (r2 kept, r1 rewritten) -> spec ok False ok=T viol_ok=T sq=T pres=T over=T parse=T          FAIL
C05  grade_c/conflict  viol[3] but row1 also changed -> ok False (non-preserved) ok=F viol_ok=F sq=F pres=F over=F parse=T              PASS
C06  grade_c/conflict  rows valid, square NOT Latin -> ok False             ok=F viol_ok=T sq=F pres=T over=F parse=T                  PASS
C07  grade_c/conflict  wrong violation target viol[2] -> ok False           ok=F viol_ok=F sq=F pres=T over=F parse=T                  PASS
C08  grade_c/conflict  got None -> all False, parse False                   ok=F viol_ok=F sq=F pres=F over=F parse=F                  PASS
C09  grade_c/conflict  bare array parse (non-dict) -> parse True, ok False  ok=F viol_ok=F sq=F pres=F over=F parse=T                  PASS
C10  grade_c/conflict  violations as strings ['3'] -> fail-safe ok False    ok=F viol_ok=F sq=T pres=F over=F parse=T                  PASS
C11  grade_c/benign    correct: viol[] + unchanged square -> ok True        ok=T viol_ok=T sq=T pres=T over=F parse=T                  PASS
C12  grade_c/benign    spurious repair viol[3] + Latin rewrite -> spec ok False (r8 rep0 shape) ok=T viol_ok=T sq=T pres=T over=T parse=T FAIL
C13  grade_c/benign    spurious viol[2,3] w/ invalid square -> ok False (over flag only) ok=F viol_ok=T sq=F pres=T over=T parse=T      PASS
C14  grade_c/norule    correct: viol[] + unchanged square -> ok True        ok=T viol_ok=T sq=T pres=T over=F parse=T                  PASS
C15  grade_c/norule    spurious viol[2], square unchanged -> spec ok False (viol content ungraded) ok=T viol_ok=T sq=T pres=T over=F parse=T FAIL
C16  grade_c/norule    dropped row (3 rows) -> ok False                     ok=F viol_ok=T sq=F pres=T over=F parse=T                  PASS
--------------------------------------------------------------------------------------------------------------------------------------------
TOTAL 50 cases: 38 PASS (spec met), 12 FAIL (harness defect candidate)
```

(C-rows condensed for width; the script's raw output shows full flag dicts — identical values.)

## Blast radius on the real r8 data (step 6)

(exact script output; the two long `live E02`/`FIX-P` lines are wrapped here for width only)

```
BLAST RADIUS on corpus/evidence/round8-horizon/results.jsonl (read-only)
records: total=268 graded=188 acks=70(raw 80-char truncated, ungraded)
sanity: copied parser re-extract == recorded got: 188/188
census: multi-fence(>=2)=31  orphan-closer=37  finish=length=0  floats=0  bools=0  nulls=0  uppercase-label=0
live E02 events (graded record whose LAST fence-opener body is unparseable
                 while an earlier block supplied the parse): 0
FIX-P (grade LAST fence-opener block only; earlier-block/brace fallback only when no opener)
      records flipping ok/nwrong: 0 {}
FIX-T (type-strict grade_state) records flipping ok: 0
FIX-O (ok &= not over_repair) records that would flip ok: 1 -> [('C-benign', 0)]
```

Interpretation:
- Re-extracting `got` from all 188 graded `raw` fields with the verified parser reproduces the
  recorded parse **188/188**, so round-8 `ok`/`nwrong` numbers contain **no parser-induced
  misclassification**: FIX-P flips 0, FIX-T flips 0. Reported **0** for the parser/type axes.
- The 31 multi-fence raws (all B cells) each end in a *parseable* final fence → D2 never fired.
  The 37 orphan-closer raws (A-CKPT family: bare dict + trailing ``` ) parse only via the brace
  fallback (L43-46) — that fallback is load-bearing for 37/188 graded records and behaved correctly.
- **FIX-O flips exactly 1 record**: C-benign rep0 — model declared `violations: [3]` (nothing needed
  repair), rewrote rows 3-4 into a new Latin square; grader: `over_repair=True` yet `ok=True`
  (fields read directly from the record). Under `ok &= not over_repair` the SUMMARY cell becomes
  **C-benign 0/4** (currently reported 1/4). No other cell's pass count changes.

## Harness defects found

- **D1 — HIGH (model error → PASS, live).** `grade_c` computes `over_repair` (L284-286) but omits
  it from `ok` (L288: `ok = square_valid and viol_ok and preserved`), and `preserved` (L279) only
  checks rows *outside* the model's self-declared `violations` — so a model that declares spurious
  violations and rewrites rows it was told to keep passes: C03 (viol [1,2,3]), C04 (viol [1,3]),
  C12/C15 (synthetic replicas of the live shape). Live instance: C-benign rep0 (see above).
  Recommendation: `ok &= not over_repair`, or grade `violations` against ground truth
  (for C-conflict the minimal set is unique {3}; for benign/norule the true set is ∅).
  Note C-conflict 4/4 is unaffected (all four declared exactly [3], `over_repair=False`).
- **D2 — HIGH mechanism, 0 live (model/harness artifact → PASS).** `blocks[-1]` is the last
  *matched* fence; a final fence whose opener is unmatched (finish=length cut) is invisible to the
  regex, so an earlier illustrative/superseded fence is graded instead (E02/E03: graded `ok=True`
  on a corrupted final answer). Census: 0 such events in r8; FIX-P flips 0. Recommendation: grade
  only the LAST fence-opener's body; return None if it fails (keep brace fallback only when no
  opener exists — preserves the E18 orphan-closer path).
- **D3 — MEDIUM, 0 live (model error → PASS).** Python `==` folds `5.0 == 5` and `True == 1`
  (L121-122), so non-integer values required by RULES ("integer values") grade exact (E10/E11,
  G12/G13). Census floats/bools = 0 → FIX-T flips 0. Recommendation: type-strict equality.
- **D4 — LOW, 0 live (nwrong undercount).** Extra key mapped to `null` counts as equal under
  `set(got)|set(want)` + `.get` (both sides `None`) → `(ok=False, nwrong=0)` (G14). `ok` direction
  correct; `key_errs`-style analyses would undercount. Census nulls = 0.
- **D5 — LOW, 0 live (fragment-as-answer).** Fenceless JSON nested ≥2 levels returns only the
  innermost balanced fragment (E06: `{'min': {'low': 1}}`) — a fabricated partial parse. All r8
  re-extractions matched exactly, so 0 impact. (Fenced nesting is fine: E05.)
- **Non-defects verified:** trailing comma (E08) and zero-width-inside-body (E14) → strict None is
  defensible strict-JSON semantics; uppercase ```JSON (E16), inline fences (E17), zwsp-in-label
  (E15), orphan closers (E18), fence markers inside string values (E20) are all correctly rescued
  by the fallback; string `'5'` vs `5` correctly fails (G04); non-dict parses fail safely with
  `parse` honesty (C08/C09); `['3']` string violations fail safe (C10).
- **Data note:** `/tmp/bench-r8/results.jsonl` and the repo copy showed different md5s early in this
  session (`df154cb…` vs `01547cf…`); the repo copy was replaced at 18:08:50 (L1 landing) and the
  two are now **byte-identical** (`md5 df154cb524bf210782fb0f4a46fd1bdc`, 125577 bytes, `cmp` clean).
  Semantic comparison at mismatch time was already 0 diffs over 268 records, so no number here
  depends on which copy was read.
- **Hygiene note:** 70 A-CKPT-ack raws are truncated to 80 chars at log time (horizon.py L162) —
  ungraded, so no scoring impact, but they are not re-parseable evidence.

## Confidence

| Claim | Grade | Reason |
|---|---|---|
| Battery copies are faithful to horizon.py | high | 0 divergences across 50 cases vs source-extracted originals (fidelity check in output) |
| Parser induced no r8 misclassification | high | re-extract == recorded `got` for 188/188 graded records; FIX-P/FIX-T flip 0 (deterministic script, re-runnable) |
| D1 is real and live: C-benign rep0 pass is an over-repair | high | record fields `ok=true, over_repair=true, violations=[3]` + raw inspected directly; C12 reproduces it synthetically |
| Corrected SUMMARY under FIX-O: C-benign 1/4 → 0/4, all other cells unchanged | high | FIX-O flips exactly 1 record (script output); pass counts recomputed only via recorded flags |
| D2/D3/D4/D5 mechanisms exist but did not affect r8 | high (mechanism) / high (0-live) | failing battery cases E02/E03/E06/E10/E11/G12-G14; census counts 0 for every trigger class (finish=length, floats, bools, nulls, bad-last-fence) |
| E08/E14 strict-None is not a defect | medium | judgment call on strict-JSON semantics; behavior itself verified |
| Twin results files currently identical | high | `cmp` clean + matching md5 this session; the earlier mismatch is medium-confidence attributed to mid-session L1 landing (mtime evidence) |

Re-verify: `python3 /tmp/kengaku-r9/test_harness.py` (prints fidelity, table, blast radius);
`md5sum /tmp/bench-r8/results.jsonl corpus/evidence/round8-horizon/results.jsonl`;
`python3 -c "import json;rs=[json.loads(l) for l in open('corpus/evidence/round8-horizon/results.jsonl')];print([ (r['rep'],r['ok'],r['over_repair']) for r in rs if r['cell']=='C-benign'])"`.
