# R32 FxEntryTruth — attack on the drafted C1 entry's truth conditions

Seat: `L1Kengaku32.FxEntryTruth` (UFO-FSD critic, leaf). Date: 2026-10-25 (fetches and receipt runs
~09:52–09:54 local). Target: `corpus/knowledge/benchmark-grader-semantics.md` (staged, uncommitted), its
frozen predicate (plans/round-32-claims.md C1), the counters `plans/adoption_check.py` /
`plans/round32_c1_verify.py`, and the rows S093/S094/S097 in `corpus/SOURCES.md`. No production bytes
modified; scratch `/tmp/r32f-FxEntryTruth/` (≈ 80 KB). No tool installed (curl + stdlib only).

## Evidence base (bytes I fetched myself, 2026-10-25)

| fetch | pin | bytes | sha256 | used for |
|---|---|---|---|---|
| Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py` | `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` | 14,138 | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` | S094 quotes, line-accurate |
| Toolathlon `utils/evaluation/retry.py` (repo root) | same pin | 4,519 | `db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e` | retry constants/loop |
| SWE-bench_Pro-os `v2/tasks/…openlibrary-…/tests/test.sh` | `66f92766bba642462d4bbe5479e83f91f9211862` | 7,864 | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` | S093 reset/reward |
| same task `tests/parser.py` | same pin | 4,229 | `303ceda2c97816c27383b767baa9e2f28f8e9b0cebed4dd5d6159c6760770b66` | S093 log-scan/last-write-wins |
| arXiv `2412.05579v2` abs page | v2 | 43,661 | `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` | S097 abstract sentence |

Receipts run read-only from lane root (same session):
- `python3 plans/adoption_check.py --expect .ufo/waves/round-32/claims/adoption-expect.json --census`
  → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=fail`, **rc=1**.
- `python3 plans/round32_c1_verify.py --lane .` → `checks=6 defects=0`, **rc=0**.
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc=1, errors
  `E03 S094 duplicate id`, `E04 S094 duplicate url …`, same for S097/S101/S102 (see §6).

---

## 1. Per-claim verdicts on the six strongest claims

### 1.1 Deterministic grader (no LLM/judge path) — CONFIRMED (scoped)
`grep -inE 'prompt|judge|model|openai|chat|gpt|llm|claude|anthropic'` over the fetched `main.py` →
zero matches (exit 1). Imports (`main.py:1-12`) are stdlib + `google.cloud.storage/logging`,
`google.oauth2.service_account`, `google.api_core.exceptions`, `utils.evaluation.retry` — no HTTP/OpenAI/
Anthropic SDK, no API-key handling. One `subprocess.run` only (`:149-152`, `gcloud storage buckets list`,
not an LLM). The reading is solid for this file. Scope caveat: it is a *token/import-level* absence for one
file; the entry itself scopes to this file, so this is fair. (See §2 item 7 for the strength note.)

### 1.2 0.05 tolerance at the call site — CONFIRMED
Exactly one call site: `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` at
`main.py:280`, preceded by `# Validate with 0.05% tolerance` at `:279`; the `:58` default `tolerance_pct:
float = 0.1` is never executed. `diff_A = abs(actual_A - expected_A)`, `if diff_A > tolerance_pct` (`:83-84`)
→ absolute percentage-point comparison. "within 0.05 percentage points per scenario" is accurate. The
`0.1` default is correctly quarantined in the entry's negative space.

### 1.3 Fail-open log-bucket check — REFUTED as stated
The entry says: "a log-check failure never fails the task by itself." The code contradicts this on **two
reachable paths** in `check_abtesting_logging_bucket_clean` (`main.py:168-218`):
1. **Missing-credential path returns `None` (falsy) → task fails.** `get_project_id_and_credentials()`
   (`:104-123`) returns `(None, None)` when the service-account file is absent (its documented fallback).
   Inside the log check, the whole body is `if project_id_from_creds and credentials:` (`:176`); when that is
   false the function falls off the end and implicitly returns `None`. Then `validate_task_completion`:234
   `if not check_abtesting_logging_bucket_clean(...):` → `not None` is True → `raise ValueError(...)` at
   `:235` → gate fails. The fail-open `return True` at `:218` is reachable **only** when an exception is
   raised inside the `try`. The common no-credentials dev path is the opposite of fail-open.
2. **File open outside the `try`.** `with open(…/groundtruth_workspace/log_bucket_name.txt)` at
   `:171-172` precedes `try:` (`:173`). A missing/unreadable `log_bucket_name.txt` raises an unhandled
   `FileNotFoundError`; the gate fails (retried 3×, then exit 1).
So "fails open on error" is true only for the except-branch; "never fails the task by itself" is false. The
entry's own negative-space bullet ("the code fails open when its own credential/API path errors") is also
over-narrow: the credential path *errors silently* into `(None, None)`, which is a fail-closed path, not a
fail-open one.

### 1.4 Survey five-part split — CONFIRMED verbatim; the "separates deterministic graders from LLM judges" attribution is NOT in the source
The quoted abstract sentence is a byte substring of the fetched v2 page: "This paper presents a comprehensive
survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications,
Meta-evaluation, and Limitations." (20 whitespace-words; blockquote verified). "Meta-evaluation is kept
distinct from methodology" is supportable as a listing fact. However, the *survey never mentions deterministic
graders* and never draws a deterministic-vs-LLM-judge dichotomy; it is a survey of LLMs-as-judges only. The
entry's intro ("and for the survey frame that separates deterministic graders from LLM judges") and the
claims-doc surface ("adds the survey frame that separates deterministic graders from LLM judges") attribute to
S097 a separation the source does not make. The entry's §S097 explicitly admits this ("That classification is
this entry's own framing; the abstract itself only separates the parts") — so the entry internally
self-corrects, but the intro/claims/README wording stays an overclaim (see §2 items 1–2, §4).

### 1.5 S093 binary-containment restatement — CONFIRMED
`test.sh:213-214`: `all_required = fail_to_pass | pass_to_pass`; `success = all_required <= passed_tests` —
binary set containment, no threshold. `passed_tests` derives from `parser.py` regex
`^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR)` over stdout+stderr (`:68,71,88-90`) and dedupes at
`parser.py:121` `unique_results = {result.name: result for result in results}.values()` — dict comprehension,
**last write wins**. "log-derived, last-write-wins PASSED set" is accurate. Reset claim ("restores tracked
test code but not newly added fixture files"): `is_test_code` excludes `DATA_DIRS` (`:37-55`), tracked test
code gets `T) git checkout HEAD -- "$path"` (`:71`), untracked created-by-patch files are deleted (`:77-79`),
untracked modifier-only files left alone (`:93`). Confirmed.

### 1.6 Discharge wording ("one task only") — HONEST in the artifact, slightly broader in the claims doc
The entry and the landed README sub-bullet (`README.md:279`) say "for that one task whose evaluation script
is read … not for the benchmark's whole scoring surface" — honest. The claims doc (`round-32-claims.md:21-22`)
says the claim "closes that open clause **for Toolathlon's scoring code** (the task evaluation script)" —
without the "one task" qualifier, which reads broader than what is delivered. Verdict: artifact honest; claim
sentence loose.

---

## 2. Sentences in the entry that claim more than the quoted bytes establish

1. **Intro:** "and for the survey frame that separates deterministic graders from LLM judges" — the survey
   separates five perspectives of LLMs-as-judges; it says nothing about deterministic graders. Paraphrase-as-
   fact (contradicted by the entry's own §S097 caveat).
2. **Claims doc / README index row / coverage row** repeat the same "separates deterministic graders from LLM
   judges" attribution (README.md:67, :255; claims.md:22) — pervasive overclaim.
3. **"every claim below is a reading of code and of an abstract page, quoted byte-for-byte from the pinned
   revisions"** — true for the quoted spans; false as a blanket statement: the S093 half quotes no source byte
   (it restates), and several load-bearing sentences ("never calls a model", fail-open universality) are scan/
   inference results, not quotes. Overstates the quote discipline.
4. **"a log-check failure never fails the task by itself"** — refuted (`§1.3`).
5. **Word-count labels are wrong for three of four code quotes** (asserted byte metadata, all against the same
   fetched bytes):
   - `main.py:58` signature quote labelled "9 words" — actual whitespace-words: **11**.
   - `main.py:279` `# Validate with 0.05% tolerance` labelled "4 words" — actual: **5**.
   - `main.py:280` call labelled "4 words" — actual: **3**.
   - `main.py:217-218` `return True  # Don't fail evaluation if we can't check logs` labelled "8 words" —
     actual: **11** (8 only if counting the comment sentence alone, dropping "return True #").
   The same wrong "8 words" label appears in the S094 registry row (`SOURCES.md:114`).
6. **"the only extra module import resolves to a poll-retry wrapper"** — the file has five non-stdlib
   imports (`google.cloud.storage`, `google.cloud.logging`, `google.oauth2.service_account`,
   `google.api_core.exceptions`, `utils.evaluation.retry`). True only if "extra" means "non-standard-library,
   non-Google-cloud"; the phrase is ambiguous and unanchored.
7. **"never calls a model: a case-insensitive scan … finds no LLM or judge path"** — confirmed for the token
   list, but a token scan cannot exclude a dynamically constructed endpoint; here the absence of any HTTP/IO
   client makes the conclusion robust. Strength caveat, not a defect.
8. **"deterministic state comparison"** headline — "deterministic" is accurate for the *comparison*, but the
   gate depends on eventually-consistent external cloud state (the retry exists precisely because of it); the
   label should be read as "no LLM path", which the entry's own text supports.
9. **"Toolathlon's ab-testing grader … with a call-site tolerance"** — accurate; the word "grader" scopes to
   this one file, which §S094 makes explicit.

## 3. Falsifier clause — non-vacuous but incomplete

- The falsifier ("a Toolathlon ab-testing task whose grading path calls an LLM judge, or executes
  `validate_record_data` with a tolerance other than 0.05, while still being graded by exactly this `main.py`
  at 9be8d8fe") is observable and satisfiable in principle — not vacuous.
- **Second disjunct is effectively inert:** there is exactly one call site and the tolerance is a literal
  (`main.py:280`); a different tolerance would require a different file/commit, which the "exactly this
  main.py" guard excludes. Only the first disjunct can ever fire.
- **Coverage gap:** the falsifier does not cover the fail-open defect found in §1.3 (missing credentials →
  task fails). If the entry's fail-open claim is wrong, the falsifier as written would not trigger. The
  falsifier should add "or a run of this grader that fails when the log-bucket check cannot read its inputs /
  credentials".
- Kill-rule reachability: all three quoted spans resolve at the pins (verified above), so the kill rule would
  pass; but no receipt executes the kill rule (see §6).

## 4. Discharge honesty — verdict

- "One task only": honest in the artifact and in the README landing wording; the claims doc omits the "one
  task" qualifier once.
- The discharge correctly does **not** claim runtime task validity (PROVINCE.md:201/210/219 refuse it), and
  the "What this does not establish" section is genuinely negative-space (no contamination/task-validity/run
  claims). The S093 half is now labelled restatement ("restates that result and does not repeat its
  derivation"), which is the honest form.
- One honesty gap: the intro's "survey frame that separates deterministic graders from LLM judges" (item 1)
  is stated before the entry's own §S097 correction — a reader stopping at the intro takes a false attribution.

## 5. Counter/registry state findings (frozen predicate on current disk)

1. **The C1 predicate is currently NOT satisfied.** Receipt 1 prints `census=fail` and exits 1 because
   `sources-census.sh validate` fails with `E03 duplicate id` / `E04 duplicate url` for S094, S097, S101,
   S102. `corpus/SOURCES.md` carries each of those four rows **twice** (S094 at :114 and :118; S097 at :115
   and :119; S101 at :116 and :120; S102 at :117 and :121). Registry now has 99 rows; freeze said 91
   pre-append, and the planned append adds only 4 → 95. Assuming a clean merge, the duplicates must be removed
   before the counting command can print the frozen line (`census=ok`, exit 0).
2. **The two receipts disagree on the same tree:** receipt 2 (`round32_c1_verify.py`) prints
   `checks=6 defects=0` rc=0 while receipt 1 fails on census. The duplicate rows are invisible to receipt 2
   because it parses rows into a dict (last row wins) and never runs census.
3. **No receipt checks quote truth against the pinned revisions.** V1–V6 are presence/shape checks
   (verified-at line, URL host+path substring, pin fragments, one non-trivial index row, ≥40 lines/≥3000
   bytes, control digest). A body asserting the opposite tolerance (0.1) or an LLM judge passes both receipts
   (demonstrated by `R32CritC1` routes b/c). The content items in §1/§2 are unpoliced.
4. **Kill rule is process-only:** a cited source whose located quote cannot be found at the pin is not
   refused by either receipt (0/3 resolved quotes still pass); the kill rule lives in prose (R32CritC1 route c).
5. **Word counts (item 5) and the fail-open overclaim pass all receipts** — no counter reads them.
6. The staged `SOURCES.append.md` S097 row carried the `LMs-as-judges` typo (missing L) and was refused by
   the quote gate (exit 7, `R32QuoteMode`); the live `SOURCES.md:115` row now has `LLMs-as-judges` — the row
   text and the staged package currently disagree, and the duplicate rows make the registry state inconsistent
   anyway.

## 6. C2 / C3 secondary findings (recorded, attributed)

C2 counter (`plans/round32_defects.py`) — from `R32CritC2` (re-executed escape matrix, all routes GREEN on
current bytes; M1/M3 by `R32MutCounters`):
1. R1: wrong-commit, negation, and rewrite routes all GREEN; erratum never has to name `ae95fe0` as its
   locator; append-only is proxied by token presence.
2. R2: substring "tip in report" anywhere; no ordering proof (report can predate the tip it cites).
3. R3: only the literal `can't open file` string is killed; a hand-written receipt with the blessed path
   passes; nothing binds the receipt to a run.
4. R4: first-match heading race — prose under an earlier heading, or under the real registry heading without a
   row, passes.
5. R5: `dead` matches inside `deadline`; explicit negation passes.
6. R6: `:39-40`/`:72`/`:82-83` tokens unanchored; a question or a denial passes; rewrite+note passes.
7. R7: "S086 … not peer-reviewed either" (meaning the opposite) passes; the natural markdown erratum is a
   false red.
8. Selftest: `registry-complete` is a tautology; `*-red-on-empty` exercises only the file-existence guard;
   five predicate mutants (including deleting R4/R6 predicates) pass `--selftest`.
9. The frozen-seven guard is dead code: deleting R7 from `CHECKS` gives `checks=6 defects=6` with no
   `DEFECT registry:` line (false green on a repaired tree).
10. R3's blessed path arithmetic is correct (`../../../../plans/sources_adopt.py` resolves), but only its
    occurrence is checked.

C3 counter (`plans/catalog_probe.py`) — from `R32CritC3` and `R32DraftMistakes` row 12:
11. `hf_models=50` is the request's own page limit (`?limit=50`, catalog_probe.py:29) — the frozen figure
    cannot tell a catalog from a request.
12. Schema-delta parses `data[0]` only (HF 53-58, OpenRouter 65-71) — a heterogeneous catalog is certified
    from one item.
13. `entry_ok` accepts a receipt pointer with no receipt file; the built-in selftest codifies that absence.
14. `probe()` is all-or-nothing: an OpenRouter failure after an HF success erases the HF result (fails
    closed, violating the claim's honest-partial kill-rule wording).
15. S101/S102 citations are not checked against registry provenance or the access date.

## 7. Attack-item tally

§1: 6 headline-claim verdicts (3 confirmed, 1 refuted, 1 confirmed-with-attribution-defect, 1 honest).
§2: 9 distinct unestablished-claim sentences (items 1–9).
§3: 3 falsifier findings (non-vacuous; inert disjunct; coverage gap).
§4: 3 discharge-honesty findings.
§5: 6 counter/registry state findings.
§6: 15 C2/C3 counter findings.
Total distinct attack items: **42** (≥32 required).

---

VERDICT: <attack-finished>
