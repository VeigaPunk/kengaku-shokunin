writer: KengakuR29-2.FReviewOutputScope-2

# FReviewOutputScope — LIMIT lines and summary/JSON fields vs prereg lines 49-71

Item scope: the ten `LIMIT` lines and the `summary` / `--json` field surface of
`plans/config_projection.py`, checked against prereg `plans/round-29-claims.md` lines 49-71
(tool interface; required-output list; "do not pool units"; "no claim beyond source").

I read the production source (this item explicitly permits it). I did **not** read the corpus
candidate draft until after the measurements below; no finding depends on it.

## Version under test — the artifact moved under me twice

`plans/config_projection.py` was **edited in the working tree by another seat while I reviewed
it**, then committed by that seat mid-review. Observed revisions:

| rev | sha256 (prefix) | state | note |
|---|---|---|---|
| `56fd949` | `5673405e` | committed, admitted | the instrument the round's receipts were first filed against |
| wt-1 | `7d42acb9` | uncommitted, 14:16:12 | added `EXPECTED_STATEMENTS`, `witnesses()`, duplicate-key census — **`--summary` and `--selftest` both crashed here** |
| wt-2 | `a91f3943` | uncommitted, 14:17:41 | renamed `index_mapping` keys, fixed `summary_lines` |
| wt-3 | `e88471ca` | uncommitted, 14:21:12 | added `-I -S`/empty-env child, `python -O` refusal |
| wt-4 | `135cc682` | **committed as `dbcecde`**, 14:23:00 | final observed state |

All findings below are re-verified against the **committed `dbcecde` / `135cc682`**, except
B1, which is a property of the uncommitted wt-1 state and is reported as such.

Commands (read-only against the lane; all my probe artifacts under `/tmp/kengaku-r29-freview/`):

```
python3 plans/config_projection.py --summary   # exit 0, 53 lines
python3 plans/config_projection.py --json       # exit 0, sha256 a4fb5d6d…
python3 plans/config_projection.py --selftest   # exit 0, 27 cases
python3 -O plans/config_projection.py --json    # exit 2, assertions_disabled
```

## What is attacked

1. Does the scope statement name scope and the three profiles' synthetic purposes (prereg L55)?
2. Does the output keep occurrence / leaf / task units separate and never pooled (prereg L71)?
3. Are there hidden exclusions — tasks, leaves, or occurrences dropped from the census (prereg L63)?
4. Does any LIMIT or field claim more than the pinned source supports (prereg L45-47, L64-69)?

## Verdict summary

**Every frozen-data number is correct and I reproduced all of them independently** (§Independent
re-derivation): 812 tasks, 812 distinct ids, 3 profiles, 2436 projections, 1435 occurrences,
1416 changed leaves, 812 changed tasks, 10869 string leaves, 13 multi-occurrence leaves,
per-token occurrences 385/336/281/300/0/133, per-token tasks 204/128/192/182/0/128,
index==task_id 812/812, 697 slash junctions, 0 remaining env tokens, `__last_url__` 65 /
`__page__` 12, and all three `projected_text_sha256` digests.

**Unit separation is substantially honest**: occurrence, leaf, task and task×profile counts are
four separately-named fields; `TASKS_WITH_TOKEN_NOT_ADDITIVE` names the one non-additive
breakdown; `INDEX` carries an explicit `"unit": "input tasks"`.

But I found **seven concrete defects**. Three are in the exact surface I was asked to audit and
are live at the committed revision: an **unenforced scope claim** (the `*.invalid` /
"not deployment recommendations" assertion is never checked), an **unlabelled non-additive leaf
breakdown** that can silently disagree with `changed_leaf_count`, and **per-profile surviving
placeholders that are never reported**. One further defect (**the same JSON key carries two
different types** across `--json` and `--summary`) is an interface hazard for anything that
parses both. And the lane's **filed receipts no longer correspond to the committed instrument**.

---

## Blocking findings

### B1 (HIGH — receipts) — the filed build receipts describe a superseded instrument

`corpus/evidence/round29-calibration/` now holds **two generations of receipts** and no marker
says which tool each was produced by:

| file | tool sha256 it pins | matches committed `dbcecde`? |
|---|---|---|
| `build-json-sha256.txt` | `c8da0c5a2d31…` | **no** (committed tool yields `a4fb5d6dd9b7…`) |
| `build-summary.txt` (48 lines) | produced by `5673405e` | **no** — committed tool emits 53 lines |
| `build-selftest.txt` (20 cases) | produced by `5673405e` | **no** — committed tool runs 27 cases |
| `mutation-witness.txt` | `control sha256 5673405e…` | **no** |
| `repair-json-sha256.txt` | `a4fb5d6dd9b7…` | yes |
| `repair-summary.txt` (54 lines) | `135cc682` | yes (differs from mine only by a trailing `exit=0` line) |
| `repair-selftest.txt` (27 cases) | `135cc682` | yes |
| `repair-mutation-witness.json` | `tool_sha256 135cc682…` | yes |

Measured directly:

```
$ python3 plans/config_projection.py --json | sha256sum
a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851  -
$ cat corpus/evidence/round29-calibration/build-json-sha256.txt
c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630  -
```

A reader who picks `build-summary.txt` (the older, alphabetically-first name, and the one the
original round receipt cites) gets a summary and selftest transcript for an instrument that is
no longer the integrated state. **Both generations sit in the same directory with no
"superseded" marker.** Prereg L17 names the counting command `--summary` / `--json` and the
delivered receipts; the delivered receipt set is ambiguous about which artifact it certifies.

Separately, the **wt-1 intermediate state was genuinely broken**: at `7d42acb9` both
`--summary` and `--selftest` crashed with an uncaught `KeyError` (the `index_mapping` key rename
had landed in `audit_text` but not in `summary_lines` / the selftest assertion). I observed:

```
KeyError: 'index_equals_task_id'   (summary_lines, --summary)
KeyError: 'violations'              (selftest, --selftest)
```

That state was never committed, so it is not a defect of the delivered artifact — but it shows
the rename was not applied atomically across the three call sites, and it is the exact failure
mode that B2 below still survives in a *smaller* form.

### B2 (HIGH — summary/JSON interface) — one key, two types, across the two output modes

`index_mapping` in `--json` (line 387 of the committed rev):

```python
"index_task_id_mismatches": index_mismatches
```

`summary_lines` (line 427 of the committed rev):

```python
"index_task_id_mismatches": len(result["index_mapping"]["index_task_id_mismatches"])
```

Measured on the frozen input:

```
--json    index_mapping["index_task_id_mismatches"] == []      (list)
--summary INDEX {"unit": "input tasks", "index_equals_task_id_count": 812, "index_task_id_mismatches": 0}
```

The **same key name** is a list in one mode and an int in the other. A consumer that reads the
summary line and the JSON object with one accessor gets `0` and `[]` and cannot tell whether
"0 mismatches" and "empty mismatch list" are the same statement or whether one mode dropped the
mismatch records. HEAD had the identical collision under different names (`violations`: list in
JSON, int in summary); the wt-2 rename fixed the *name* but not the *type*.

Note this is exactly the defect class that broke wt-1 (a rename applied to one call site but not
the others) — it survived the repair in a different form.

**Fix direction:** emit `index_task_id_mismatch_count` (int) and `index_task_id_mismatches`
(list) as two distinct keys in **both** modes.

### B3 (HIGH — required output) — `--summary` carries no source-text digest, so the summary receipt cannot bind itself to the input it projected

Prereg L64 requires per-profile "source text/projection digests". The `--json` mode carries
`raw_text_sha256`, `manifest_sha256`, `upstream_revision` and the per-input pin map — verified
in the committed output: `raw_text_sha256` = `7b50386f…`, `manifest_sha256` = `f6390b92…`,
`upstream_revision` = `dce04686a56253aefba7b18a4fa0937cf1dc987b`.

`--summary` prints **none of them**:

```
$ grep -c "raw_text_sha256\|manifest_sha256\|upstream_revision" summary-dbcecde.txt
0
```

The only digests a `--summary` reader sees are the three per-profile `projected_text_sha256`
values. A summary receipt therefore cannot bind its projection to *which input bytes* produced
it. The summary is the artifact a human reviewer reads; the JSON is the machine artifact. As
filed, `repair-summary.txt` has the same gap.

---

## Non-blocking findings

### N1 (MEDIUM) — `distinct_task_ids` counts distinct **JSON encodings**, not distinct ids

`plans/config_projection.py:310`:

```python
"distinct_task_ids": len(set(map(json.dumps, ids))),
```

`json.dumps` separates values that a reader of the raw file considers the same id, and separates
values that differ only in a way JSON erases. Measured directly:

```
json.dumps distinct over [0, 1, True, 1.0]  ->  4   ('0','1','1.0','true')
numeric distinct over [0, 1, True, 1.0]      ->  2
```

Probed against the instrument (probe N1, task 0 id `1`, task 1 id `True`):

```
FINDING {"id": "input_population_mismatch"}
POPULATION {"distinct_task_ids": 812, "input_task_count": 812, ...}
```

`distinct_task_ids` reads **812** while ids 1 and `True` are the same id to any consumer of the
raw file. This is the only place the tool's "distinct IDs" claim (prereg L63) is computed, and
the field name promises a count of distinct ids while delivering a count of distinct
serialisations.

### N2 (MEDIUM) — `input_population_mismatch` fires on a **distinct** id set, contradicting the "distinct IDs" contract, and the summary then prints both

Prereg L63 requires "812 input tasks, **distinct IDs**". The gate (line 302) is:

```python
if not isinstance(original, list) or (expected_population is not None and (len(original) != expected_population or sorted(ids) != list(range(expected_population)))):
    findings.append({"id": "input_population_mismatch"})
```

`ids` is `task.get("task_id")` per task, so a population of 812 tasks with 812 distinct ids that
are **not** the integers 0..811 is reported as a population mismatch. Measured (probe I, ids
1..812; probe J, ids "0".."811"):

```
=== I (distinct ids 1..812) exit 1
  FINDING {"id": "input_population_mismatch"}
  POPULATION {"distinct_task_ids": 812, "input_task_count": 812, ...}
=== J (distinct string ids) exit 1
  FINDING {"id": "input_population_mismatch"}
  POPULATION {"distinct_task_ids": 812, ...}
```

The output simultaneously asserts `distinct_task_ids: 812` and raises a population finding — a
self-contradiction in one receipt. The implemented gate is *ids are exactly the integers 0..811*,
a stronger constraint than the prereg states, and no LIMIT line discloses it.

### N3 (MEDIUM) — `changed_leaves_with_multiple_occurrences` is a **leaf** count, and the occurrence-unit excess (19) is never reported

The field is 13 on the frozen input — verified independently: 13 leaves carry >1 token hit
(8 REDDIT, 5 SHOPPING), multiplicity distribution {1:1403, 2:8, 3:4, 4:1}. The **occurrence**
excess is **19** (1435 occurrences − 1416 leaves).

So 13 is a leaf count, while the field name contains "occurrences"; and the occurrence-unit
figure 19 — the number prereg L71 asks to keep distinct from the leaf count — is **not present
anywhere in the tool output**. A reader subtracting 1435 − 1416 gets 19 and has no field to
check it against. The neighbouring fields `changed_leaf_count` (1416) and
`original_occurrences_by_token` (1435) are both present, so the excess is derivable but never
stated.

### N4 (MEDIUM) — `changed_leaves_by_token` is a **double-count** view, not a partition, and only the *task* variant is flagged non-additive

`changed_leaves_by_token` counts, per token, how many changed leaves carry that token. A leaf
carrying two *different* tokens is counted under both, so the breakdown does **not** partition
`changed_leaf_count`. On the frozen input the sum happens to equal 1416 — because no leaf
carries two distinct tokens (verified: 0 such leaves). That equality is a property of this
input, not of the method, and is not asserted anywhere.

Demonstrated on the committed revision (probe D, one leaf set to `"__GITLAB__/__REDDIT__"`):

```
PROFILE distinct_origins parsed_task_count=812 … changed_leaf_count=1416 …
PROFILE distinct_origins changed_leaves_by_token={"__GITLAB__": 386, "__REDDIT__": 324, …}
TOTAL findings=0 exit=0
```

sum = **1417** vs `changed_leaf_count` **1416**, with **no finding raised** — the
`leaf_change_unexplained` / `token_leaf_unchanged` invariants do not cover this. LIMIT line 9
warns only that "per-token **task** counts are not additive"; the equally non-additive
per-token **leaf** counts are unlabelled, so a reader who sums the frozen
`changed_leaves_by_token` (getting 1416) concludes it is a partition.

### N5 (MEDIUM) — per-profile *surviving* placeholders are never reported; "remaining known tokens: 0" hides 77 unresolved placeholders in 64 tasks

`population.other_double_underscore_markers` = `{"__last_url__": 65, "__page__": 12}` is computed
from the **original** raw text (`MARKER_RE.finditer(raw_text)`), at population level only — not
per profile, and not from the projection.

These markers are not replaced by any profile, so they **survive into every projection**.
Verified independently for all three profiles: **77 placeholder occurrences across 64 of the 812
projected tasks** still contain `__last_url__`/`__page__` after projection.

The per-profile record's remaining fields are `remaining_known_tokens_text` and
`remaining_known_tokens_decoded`, both **0** for every profile — because they count only the six
*env* tokens. So the summary reads, per profile, "remaining known tokens: all zero", and gives
no per-profile statement that 77 unresolved placeholders remain in the projected config. The
prereg L65 required output lists "remaining known placeholders" per profile; `__last_url__` and
`__page__` are known placeholders of the upstream raw file, and their survival is a **hidden
exclusion** from the per-profile remaining disclosure.

### N6 (MEDIUM) — the LIMIT scope line makes a checkable claim about the pinned fixture that no code verifies

`check_profiles` (lines 149-168 of the committed rev) checks only: profiles is a dict; the
profile-name set equals the `STIMULUS` key set; each profile has a `values` dict; `purpose` is
a `str`; each profile's `values` has exactly the six `ORDER` keys with `str` values.

It never checks that any value's host is a `*.invalid` domain, and never checks that `purpose`
is not a deployment claim — yet LIMIT line 4 asserts both:

> "profiles: three frozen synthetic *.invalid sensitivity stimuli, not deployment recommendations"

Probed (probe F): I rewrote the profiles fixture so `distinct_origins.purpose` =
`"deployment baseline"` and `distinct_origins.values.GITLAB` = `http://gitlab.example.com:10101`
(a non-`.invalid`, non-synthetic host), and re-pinned the manifest accordingly. Committed-revision
output:

```
LIMIT profiles: three frozen synthetic *.invalid sensitivity stimuli, not deployment recommendations; …
PROFILE distinct_origins purpose="deployment baseline"
TOTAL findings=0 exit=0
```

Exit 0, **no finding**, while the output simultaneously asserts "three frozen synthetic
`*.invalid` sensitivity stimuli, not deployment recommendations" and prints a purpose of
"deployment baseline" next to a non-`.invalid` host.

On the *frozen* fixture the claim happens to be true — I verified all 18 profile values use
`.invalid` hosts and all three purposes read "controlled synthetic text-substitution profile, not
an observed deployment" — so the delivered receipt is not false. But the guarantee is
**unenforced prose**: a coherent re-pin of `profiles.json` makes the printed scope statement
false while exiting 0. This is a direct "no claim beyond source" defect: the scope statement
asserts a property of the pinned data that the tool does not check.

### N7 (LOW) — the non-env marker census regex would miss a marker containing a non-identifier character

`MARKER_RE = re.compile(r"__[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*__")`. I scanned the frozen raw text
for **every** maximal `__…__` run with a permissive pattern: 7 distinct families, and `MARKER_RE`
matched all 7 — `missed by MARKER_RE: {}`. So the frozen census is complete; a marker such as
`__a-b__` would be invisible. Not triggered on this input; recorded as a scope-of-claim note.

---

## Independent re-derivation (all frozen numbers reproduced from pinned bytes)

I re-derived the tool's headline numbers from
`plans/fixtures/r28/webarena/config_files/test.raw.json` and `plans/fixtures/r29/profiles.json`
alone, with my own leaf walk and my own six ordered `str.replace` calls, and compared to the
committed `--json`:

| quantity | mine | tool | match |
|---|---|---|---|
| input tasks / distinct ids | 812 / 812 | 812 / 812 | yes |
| occurrence counts by token | 385/336/281/300/0/133 (total 1435) | identical | yes |
| tasks by token (non-additive, sum 834) | 204/128/192/182/0/128 | identical | yes |
| string value leaves | 10869 | 10869 | yes |
| changed leaves / changed tasks | 1416 / 812 | 1416 / 812 | yes |
| leaves with >1 token hit | 13 | 13 | yes |
| changed leaves by category | url 1355 / non-url 61 | identical | yes |
| changed leaves by path template | start_url 812, program_html[].url 338, reference_url 205, must_include[] 60, raw_annotation 1 | identical | yes |
| projected_text_sha256 (3 profiles) | identical | identical | yes |
| would_be_file_sha256 vs real `json.dump(indent=2)` bytes | 0 mismatches / 812 | — | yes |
| occurrence offsets resolve to the right string | 1435 / 1435 | — | yes |
| index == task_id | 812 / 812, 0 violations | identical | yes |
| remaining env tokens (text, decoded) | 0 / 0 | 0 / 0 | yes |
| surviving `__last_url__`/`__page__` | 77 occurrences / 64 tasks (all 3 profiles) | **not reported per profile** | **gap N5** |

Frozen-input facts I confirmed *outside* the tool: the raw file is pure ASCII (0 bytes > 127)
with 0 carriage returns; its sha256 matches the manifest pin
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`; the manifest sha256 matches
the constant persisted in the instrument; all three input pins verify.

## Scope / claim checks that PASS

- **No claim beyond source — environment/network.** `grep -n "environ\|getenv\|expandvars"`
  over the instrument returns only the docstring line 7. No `os.environ`, no socket, no
  `urllib`/`requests`. The only `subprocess` use is the selftest's isolated child
  (`-I -S`, `env={}`).
- **Read-only.** `grep -n "write_text\|write_bytes\|mkdir\|shutil\.\|copyfile"` returns hits only
  inside `selftest`, all under a `tempfile.TemporaryDirectory`. The audit path never writes.
  Confirmed independently: `plans/fixtures/r28/webarena/config_files/` still contains exactly one
  file, `test.raw.json` (880776 bytes); no `test.json` and no per-index file was produced.
- **Upstream never imported or executed.** The generator is parsed with `ast.parse` and compared
  against `EXPECTED_STATEMENTS`; `browser_env.env_config` is never imported.
- **Exit-code contract.** `--json`/`--summary` exit 0 on the frozen input with `findings: []`;
  tampered manifest → exit 2 `manifest_tampered`; tampered input → exit 2 `snapshot_tampered`;
  missing input → exit 2 `input_missing`; usage error → exit 2; `python -O` → exit 2
  `assertions_disabled`. **HEAD `56fd949`'s `--summary` exits 0 and its output matches the filed
  `build-summary.txt` byte-for-byte** apart from the receipt's trailing `exit=0` line — I ran
  `git show 56fd949:plans/config_projection.py` directly to check this, because an intermediate
  working-tree state did crash (see B1).
- **Offsets are codepoint offsets in the ORIGINAL text**, never bytes, never step-input. All 1435
  provenance offsets are true positions of their token in the original raw text (re-verified
  against `raw_text.find`); LIMIT line 5 states this correctly.
- **"Do not pool units" is honoured in the frozen numbers.** Occurrence counts (1435), leaf counts
  (1416), task counts (812) and task×profile counts (2436) are four distinctly-named fields;
  `TASKS_WITH_TOKEN_NOT_ADDITIVE` names the one non-additive breakdown; `INDEX` carries
  `"unit": "input tasks"`. Residuals: N3 (the occurrence-excess figure 19 is unreported) and N4
  (the per-token **leaf** breakdown's non-additivity is unlabelled).
- **No hidden exclusion of tasks or occurrences.** All 812 tasks appear in every profile's
  `tasks[]` (verified: `sum(len(t["changed_leaves"]) for t in tasks) == 1416 == changed_leaf_count`
  and `len(tasks) == 812` for all three profiles), every changed leaf is attributed to exactly one
  task, and every token occurrence has exactly one provenance record (1435). The only exclusion
  found is the leaf-level one in N5.
- **`duplicate_object_keys` census** (new in wt-1) is a genuine addition: 0 on the frozen input,
  computed from parsed span key positions, so it would catch a duplicated JSON key that
  `json.loads` silently collapses (last-wins).

## Residual risk / verification gaps

- The instrument moved under me four times. Findings are pinned to `dbcecde` / `135cc682`; line
  numbers are for that revision. The **wt-1 intermediate state was genuinely broken** (`--summary`
  and `--selftest` both `KeyError`) — evidence that the `index_mapping` rename was not applied
  atomically, which is the same defect class that survives in B2.
- **Receipt generation is ambiguous** (B1): two receipt generations share one directory with no
  supersession marker, and the older `build-*` files pin a tool sha256 that is no longer integrated.
- `plans/fixtures/r29/hand/` fixtures are consumed by the selftest; I did not independently
  re-derive their expected values (out of my item scope — the mutation/contract reviewer).
- I did not re-derive the upstream WebArena README's `SHOPPING_ADMIN '/admin'` shape from live
  bytes; I relied on the lane's pinned copy
  `.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md` (sha256 `081c8264…`, matching the S072
  anchor), whose line 87 reads `export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"`.
  The instrument's `distinct_origins` stimulus text is consistent with that shape.
- The `sites` metadata is *read* by the tool's own census (860 site-name leaves are inside the
  10869 string-leaf denominator) though not consumed as a predicate; LIMIT line 9's wording
  ("unread metadata such as `sites` is not a consumed predicate") mirrors prereg L47 and is true
  of upstream's generator, but "unread" is loose for the tool's own denominator.

## Tooling

No tools installed or upgraded. The task needed only `python3` (3.14, already present) and the
stdlib; no pacman/uv/cargo/npm action was taken, so no tool/version/channel record is due.
All probe artifacts live in `/tmp/kengaku-r29-freview/`; the only lane writes are this report and
my scratch directory `.ufo/waves/round-29/scratch/falsify/FReviewOutputScope/`. I did not touch
production, fixtures, corpus, SOURCES, SCORECARD, the candidate, the lane Git index, or any
sibling lane.

## Recommendation (for the coordinator, not an admission)

1. Mark the superseded `build-*` receipts (or regenerate them) so exactly one receipt generation
   in `corpus/evidence/round29-calibration/` corresponds to the integrated instrument.
2. Split `index_task_id_mismatches` into `_count` (int) and `_list` (list) in both output modes.
3. Add `raw_text_sha256` + `manifest_sha256` (+ `upstream_revision`) to the `--summary` receipt.
4. Either narrow the population gate to distinctness, or rename the finding to
   `input_id_set_mismatch` and add a LIMIT line stating the ids must be exactly 0..811.
5. Add a per-profile `remaining_non_env_placeholders` count (77 occurrences / 64 tasks on the
   frozen input) so the "remaining: 0" line cannot be read as "nothing unresolved remains".
6. Assert in code — not only in LIMIT prose — that profile values use `*.invalid` hosts and that
   no profile `purpose` claims a deployment baseline; the `STIMULUS` text is instrument-side and
   can drift from the pinned fixture (N6).
7. Report the occurrence-excess figure (19) alongside the 13 multi-occurrence leaves, and label
   the per-token leaf breakdown as non-additive (N3, N4).

VERDICT: FAIL
