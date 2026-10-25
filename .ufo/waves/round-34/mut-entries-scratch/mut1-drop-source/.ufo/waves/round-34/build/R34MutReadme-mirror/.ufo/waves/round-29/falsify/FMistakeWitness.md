writer: KengakuR29-2.FMistakeWitness-2

# FMistakeWitness — falsification of round-29 mined-mistake fix M87 and the `mutation-witness.txt` receipt

Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Scope: the mined-mistake fix proposed in
`.ufo/waves/round-29/drafts/lesson-and-mistake.md` (§1 principal, §4 W1–W5, §3 gate table) and the
canonical form of that fix in `corpus/lessons/round-29.md:15` (row **M87**), plus the receipt
`corpus/evidence/round29-calibration/mutation-witness.txt` and the provider/crash file
`.ufo/waves/round-29/build-dead-seats.json`.

Read-only leaf. I edited nothing in the lane. All experiments ran on `/tmp/fm-witness-2/**` copies.
My scratch is `.ufo/waves/round-29/scratch/falsify/FMistakeWitness/` (6 files).

**Did I read the production source?** Yes — `plans/config_projection.py` in full (548 lines), because
the attack requires mutating it. Two of my checks are nonetheless derived **only** from the pinned
generator text (`plans/fixtures/r29/generate_test_data.py` lines 11–16, six global `str.replace` calls)
and the pinned data, without reference to the instrument's implementation:
`perm_census.py` (720-permutation census) and `w1_w5.py` (draft W1–W5 re-derivation). Both are in my
scratch and were written against the generator contract, not the tool.

**Lane state moved during this run.** My `/tmp` base snapshot was taken at lane master `56fd949`
(`plans/config_projection.py` sha256 `5673405e…`, the exact bytes named by the receipt and by
`candidate-freeze-v1.json`). While I worked, the lane advanced to `dbcecde` and
`plans/config_projection.py` became sha256 `135cc682…` (`candidate-freeze-v2.json`). I did not cause
this. Every reproduction below is stated against the bytes named by the artifact under attack, and I
re-verify each against the current HEAD where the difference is material.

---

## 1. What the assignment asked, and the direct answer

| Asked | Result |
|---|---|
| Reproduce `mutation-witness.txt` on a /tmp copy | **Reproduced exactly** — control and all three mutants, byte-for-byte on the recorded fields (§3). |
| Confirm the URL-only mutant fails the selftest | **Confirmed** — exit 1, `AssertionError`. |
| Confirm the wrong-order mutant fails the selftest | **Confirmed** — exit 1, `AssertionError`. |
| Confirm frozen data alone does not reveal wrong order | **Confirmed, with one precision defect** — findings/exit are blind to order, but the `--summary` body is *not* identical to the control's (§4, F1). |
| Check `build-dead-seats.json` as provider/crash evidence | **Internally consistent**, with two specific gaps (§7, F10). |

The core mechanism of the fix holds: I built the exact derived control the row is about — a
value-shape URL-only substitution that is **byte-identical to the control on the frozen 812×3 data** —
and the adopted URL-only hand fixture kills it (§5, F4). So the fix is sound in substance.

The failures are in **evidence pointers, labels and provenance**, not in the mechanism. Four are
material; the most serious is a misquotation inside M87 itself.

---

## 2. Findings by severity

### F1 (HIGH) — M87's "identical to the control" is false for the `--summary`/`--json` artifacts

`corpus/lessons/round-29.md:15` states that a reversed-order mutant

> yields `TOTAL findings=0 exit=0` on the frozen 812×3 data, identical to the control

The `TOTAL findings=0 exit=0` half is exactly right. The "identical to the control" half is **not** true
of the artifacts the receipt actually records. On `/tmp` copies of `5673405e…`:

`--summary`: 47 lines; **3 differ** (one `applied_replacements` line per profile) —

```
control  PROFILE distinct_origins applied_replacements={"GITLAB": 385, "REDDIT": 336, "SHOPPING": 281, "SHOPPING_ADMIN": 300, "WIKIPEDIA": 0, "MAP": 133}
mutant   PROFILE distinct_origins applied_replacements={"MAP": 133, "WIKIPEDIA": 0, "SHOPPING_ADMIN": 300, "SHOPPING": 281, "REDDIT": 336, "GITLAB": 385}
```

`--json`: top-level differing key = `['profiles']`; per profile the differing key is `['steps']`:

```
control  profiles.distinct_origins.steps[*].name = ['GITLAB','REDDIT','SHOPPING','SHOPPING_ADMIN','WIKIPEDIA','MAP']
mutant   profiles.distinct_origins.steps[*].name = ['MAP','WIKIPEDIA','SHOPPING_ADMIN','SHOPPING','REDDIT','GITLAB']
```

Identical between control and mutant: `population`, `occurrence_provenance`, `index_mapping`,
`findings`, every `projected_text_sha256`, every per-profile `tasks`, and the per-name
`applied_replacements` *counts* (`{name: count}` maps compare equal).

So the precise statement is: **the frozen data do not discriminate order in the projected text, the
per-task objects, the census or the findings — but the instrument's own `steps` metadata discloses the
order it used, and the `--summary` body shows it.** The receipt does not record this because it stores
only the `TOTAL` line (see F6).

The candidate draft inherits the same overstatement.
`.ufo/waves/round-29/drafts/webarena-config-projection.md:73-74` (identical in v1 `7006b93d…` and v2
`435d4bb1…`):

> **Order is invisible on the frozen profiles.** No profile value contains a token, so a reversed-order
> mutant produces identical output on real data; only the cascade hand witness distinguishes it.

"identical output on real data" holds for `--json` only under a projection-only reading; the emitted
`steps` list and the `--summary` `applied_replacements` line differ. This is a scoping defect, not a
false numerical claim, and it is the same defect the row it supports is about.

### F2 (HIGH) — the receipt's `url_only_substitution` mutant is not the URL-only control the row is about, and it does not touch the hand fixtures

Receipt line 4 records `url_only_substitution selftest exit 1 killed AssertionError | summary
['TOTAL findings=6 exit=1']`. I reproduced it exactly using the mutant source persisted later at
`plans/fixtures/r29/mutation_witness.py` (and mirrored in
`corpus/evidence/round29-calibration/repair-mutation-witness.json`):

```
old  '        text = text.replace(token, values[name])\n    return text, steps'
new  '        text = re.sub(r\'("(?:start_url|reference_url|url)": ")\' + re.escape(token), lambda m: m.group(1) + values[name], text)\n    return text, steps'
```

Two observed properties of this mutant, both load-bearing:

**(a) The regex requires a space after the colon. The three adopted hand fixtures use compact JSON.**
All three hand fixtures are written without a space:

```
cascade-order.case.json          raw_serialized_text = '[{"task_id":0,"start_url":"__GITLAB__/probe"}]\n'
url-only.fixture.json             raw_text             = '[{"task_id":66,"start_url":"__REDDIT__","intent":"Literal __REDDIT__ is task text, …'
index-shuffled-ids.fixture.json   input_raw_text       = '[{"task_id":1,"intent":"ID 1 occurs first","start_url":"__GITLAB__/index-witness/first"},{'
```

`re.search(r'("(?:start_url|reference_url|url)": ")')` matches **none** of the three (verified: `False`
for each). The mutant therefore substitutes nothing in any hand fixture, and the hand-fixture-only
attribution is not the URL-only fixture failing — it is *every* fixture failing because no substitution
happened at all:

```
url_only_substitution  hand_fixture_only: H1_cascade FAIL, H2_urlonly FAIL, H3_index FAIL
```

**(b) The receipt's url-only mutant is detected by the frozen data alone** (`summary … findings=6
exit=1`), i.e. it is *not* a frozen-data-blind witness. It is therefore not evidence for M87's
principal, which is about a control that **agrees** with the instrument on every real input.

### F3 (HIGH) — M87 misquotes the very source it cites, on the exact point that source says must be named precisely

M87's evidence pointer (`corpus/lessons/round-29.md:15`):

> build/R29CritCountUnit.md shows URL-only leaf rules miss 0 frozen URL leaves

`.ufo/waves/round-29/build/R29CritCountUnit.md:76-79` says the opposite for the key-name rule and
confines "misses 0" to a different rule:

> Substituting only leaves whose key name contains `url` misses 61 leaves: 60 `must_include` entries and 1 `reference_answer_raw_annotation`.

and, separately, for the value-shape rule:

> A *value-shape* URL-only rule (a leaf starting with a token) misses 0 leaves, because every token-bearing leaf starts with a token.

The source adds (lines 79-80) that the witness must name which URL-only definition it uses, and that
only the key-name variant counts as a frozen-data failing witness.

I independently confirmed both numbers against the pinned raw file and the frozen `distinct_origins`
values, without reference to the instrument:

- key-name rule (leaf key contains `url`): **misses 61** token-bearing leaves — 60 at
  `[].eval.program_html[].required_contents.must_include[]` and 1 at
  `[].eval.reference_answer_raw_annotation` — across **18** distinct tasks.
- value-shape rule (leaf value starts with a token): **misses 0**; all **1416** of the 1416
  token-bearing leaves start with a token.
- the receipt's regex mutant (which keys on `start_url`/`reference_url`/`url`): **misses the same 61**
  leaves (1355 changed, 61 missed), i.e. it is the *key-name* variant, the one the source says is
  **detectable on frozen data** — consistent with its recorded `findings=6 exit=1`.

So M87 cites the source for a sentence the source contradicts for the rule the receipt actually ran.
The source's own repair instruction ("the witness must name which URL-only definition it uses") is
exactly the instruction M87's citation violates. This is the same defect class as r28 M74/M75 (M87
names them as not re-credited): attribution of a property to the wrong artifact.

### F4 (MEDIUM, and the strongest positive) — the derived control the row needs is absent from the receipt, but it exists and is killed

The receipt contains no witness for the "derived control that agrees with the instrument on every real
input" that M87's principal names. I built that control (`vs_text_byteidentical_control.py`): a
value-shape URL-only substitution implemented at **text level** (byte surgery over the original
serialized text, no re-serialization), so it cannot differ from the source contract by construction.

Observed against the pinned `5673405e…` bytes:

- `--summary` output: **byte-identical to the control** (`summary identical to control: True`).
- `--json` output: **byte-identical to the control** (`JSON differing top keys: []`; per-profile
  differing keys `[]` for all three profiles).
- `--selftest`: **exit 1**, `AssertionError` — the fix fires.

Hand-fixture-only attribution for this byte-identical control:

```
control          H1_cascade PASS, H2_urlonly PASS, H3_index PASS
vs_text (byte-id) H1_cascade PASS, H2_urlonly FAIL, H3_index PASS
```

**The URL-only hand fixture kills exactly the control that the frozen data cannot see, and only that
fixture.** This is the witness M87's fix column asserts ("Selftest consumes three independently
authored hand fixtures (cascade order, URL-only with non-URL intent, shuffled IDs)") and it holds. The
fix works; the receipt simply does not carry the evidence for it.

Note the later `plans/fixtures/r29/mutation_witness.py` (created 14:21, after the receipt) adds five
further mutants but still contains **no** value-shape URL-only mutant, so the gap is not closed there
either.

### F5 (MEDIUM) — the draft's W1 label is under-specified; the predicted disagreement depends on an unstated oracle definition

`.ufo/waves/round-29/drafts/lesson-and-mistake.md` §4 W1 predicts, for the sequential-text production
versus the "URL-only single-pass decoded-leaf oracle", that the two differ, with the URL-only side
predicted as `{"url": "http://gitlab.invalid:1/__MAP__/x"}`.

Re-derived from the generator text and pinned data only (`w1_w5_rederivation.py`):

- sequential-text production → `{"url": "http://gitlab.invalid:1/http://map.invalid:2/x"}` — **matches
  the draft's prediction exactly.**
- URL-only oracle under a **strict** reading (each leaf substituted at most once, no rescan) →
  `{"url": "http://gitlab.invalid:1/__MAP__/x"}` — **matches the draft's prediction exactly.**
- URL-only oracle under the **other natural reading** (walk leaves once, apply all six replacements
  within each URL leaf) → `{"url": "http://gitlab.invalid:1/http://map.invalid:2/x"}` — **identical to
  the sequential production, so W1's predicted disagreement does not occur.**

The draft's phrase "single-pass" constrains the pass over *leaves*, not the substitutions *within* a
leaf, so both readings satisfy its wording. The draft's expected output is therefore a property of one
reading, not of the label as written — the same naming defect R29CritCountUnit:79-80 warns against.

W2 is robust under both readings and I confirmed it: sequential →
`{"intent": "open http://map.invalid:2 first"}`, URL-only → `{"intent": "open __MAP__ first"}`.
W3 confirmed: projected text `{"start_url": "http://q.invalid:3/"a""}` raises
`ValueError: Expecting ',' delimiter: line 1 column 36 (char 35)`, leaf-level oracle succeeds.
W4 confirmed: enumerate ordinals `[(0, 5), (1, 2)]`, i.e. `0.json` holds task_id 5.
W5: the source raises `KeyError 'MAP'` for a missing entry and
`TypeError replace() argument 2 must be str, not int` for a non-string one; the draft's stated
expectations (`profile_missing_key` / type finding) are the **instrument's** finding ids, which is a
different namespace from the source errors the section is otherwise describing. The instrument also
emits `profile_unexpected_key` for an extra key, which the draft omits (it does say "Not claimed as
exhaustive").

### F6 (MEDIUM) — the receipt is lossy and was not independently reproducible from any artifact in the repo

`corpus/evidence/round29-calibration/mutation-witness.txt` is 460 bytes, 6 lines. Measured:

- Line 1 `control sha256 5673405e…` — **matches** `56fd949:plans/config_projection.py` exactly. Good.
- Line 2 stores the control selftest stdout **truncated to 60 of 598 characters**, with no ellipsis or
  truncation marker: the real line ends `…cli_manifest_tampered`; the receipt ends `units_n` (cut
  mid-identifier). A prefix comparison passes; a suffix or length comparison fails; a changed case
  list cannot be detected from the receipt.
- Lines 3–5 record, per mutant, only `selftest exit`, the exception **class**, and the `TOTAL` summary
  line. **No mutant source text, no mutant sha256, no kill site, and not the summary body.**
- Consequence: at the time the receipt was written (file mtime 13:38) the mutant definitions were
  persisted nowhere in the repo. `grep -rl "wrong_order_reversed\|url_only_substitution\|index_by_task_id"`
  over `.ufo/waves/round-29/build/` and `corpus/` returned **no** build report and no canonical
  evidence file; the only hit was the receipt itself. The definitions first appear in
  `plans/fixtures/r29/mutation_witness.py` (mtime 14:21) and `repair-mutation-witness.json` (14:24),
  both created after the receipt, by a different seat.

Had the definitions been persisted at receipt time, the `index_by_task_id` line would have been
ambiguous. Two natural implementations of that mutation give different exception classes:

```
task.get("task_id")      -> selftest exit 1, TypeError: %d format: a real number is required, not NoneType
task.get("task_id", i)   -> selftest exit 1, AssertionError
```

The receipt records `AssertionError`, which selects the second — but only a reimplementer could have
known that, because the receipt names the mutant and not its source. (My first reconstruction used the
first form and produced `TypeError`, i.e. I could not reproduce the receipt from the receipt alone.)

### F7 (MEDIUM) — the receipt is stale-by-reference against the current lane HEAD, and the M87 row is untracked

- `mutation-witness.txt` names control sha256 `5673405e…` (the `56fd949` bytes). The current lane
  instrument is `135cc682…` and the current `candidate-freeze-v2.json` pins `135cc682…` with
  `json_output_sha256 a4fb5d6d…`.
- I verified **both** freeze files are internally consistent with their own instrument — no digest
  fabrication: `5673405e…` bytes → `--json` digest `c8da0c5a…` (matches `candidate-freeze-v1.json`
  and `corpus/evidence/round29-calibration/build-json-sha256.txt`), and `135cc682…` bytes → `--json`
  digest `a4fb5d6d…` (matches `candidate-freeze-v2.json` and `repair-json-sha256.txt`). The receipt's
  numbers remain exactly reproducible against the bytes it names; they are simply not about the current
  HEAD instrument.
- `corpus/lessons/round-29.md` — the file containing M87, the row this assignment attacks — is
  **untracked**: `git log --all -- corpus/lessons/round-29.md` is empty and `git ls-files` does not list
  it, at both `56fd949` and `dbcecde`. It appears only as `?? corpus/lessons/round-29.md` in
  `git status`. M87's fix is therefore not yet in any commit, while the receipt it cites is committed
  (`b98dcf3`).

### F8 (MEDIUM) — the instrument has no attributable author in the landed corpus, which M88's fix claims

M88 (`corpus/lessons/round-29.md:16`) fixes the crash by recording that

> The L1 integrated the instrument from landed build reports and adopted seat-authored fixtures byte-exact

The second half is **verified true**: the adopted fixtures are byte-identical to their authors' scratch
copies.

```
plans/fixtures/r29/hand/cascade-order.case.json            4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3
.ufo/waves/round-29/scratch/R29MutOrder-2/cascade-order.case.json  4f957db3c3a8c19e951b6b225e9520cfc631fc09f864c9b4aad72464d9639fb3
plans/fixtures/r29/hand/url-only.fixture.json               2c78b19909c0c9b4b601f500301d1036c7e00d31454594ec4435c7d28407055e
.ufo/waves/round-29/scratch/R29MutUrlOnly-2/fixture.json    2c78b19909c0c9b4b601f500301d1036c7e00d31454594ec4435c7d28407055e
plans/fixtures/r29/hand/url-only.expected.json              e68e7a0dd8719b85a8db143748989a36dbc955a23b67209b8d76add720f1f5e5
.ufo/waves/round-29/scratch/R29MutUrlOnly-2/expected.json   e68e7a0dd8719b85a8db143748989a36dbc955a23b67209b8d76add720f1f5e5
plans/fixtures/r29/hand/index-shuffled-ids.fixture.json     938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254
.ufo/waves/round-29/scratch/KengakuR28.R29MutIndex-2/index-shuffled-ids.fixture.json  938771045ddbe6bdf6323858bc2c3204e38d028f1086bf83758b79a255fc9254
```

The first half is **not supported**: no landed build report contains the instrument's source or its
digest. Across all 41 files in `.ufo/waves/round-29/build/*.md`, the counts are 0 for each of
`def audit_text`, `def source_contract`, `MANIFEST_SHA256`, `def string_spans`, `URL_FIELD_TEMPLATES`,
`def provenance`, and `grep -rl 5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` returns
nothing. The instrument that all receipts and both freezes pin has **no attributable author in the
landed corpus**. The three executor seats named in the build assignments
(`R29ExecCore`, `R29ExecOracle`, `R29ExecCases`) are all dead (§7).

### F9 (LOW-MEDIUM) — the draft's proposed mistake id collides with an id r28 already used

`.ufo/waves/round-29/drafts/lesson-and-mistake.md:26`:

> Proposed mistake row (provisional label; L1 assigns the final id, and the next free number after M84 is M85):

`corpus/lessons/round-28.md` already defines **M85** (line 281) and **M86** (line 285). The premise
"the next free number after M84 is M85" is false. The canonical file resolved this correctly by using
M87/M88/M89, so no canonical collision occurred; the defect is confined to the draft's stated premise,
in the artifact I was asked to attack.

### F10 (LOW-MEDIUM) — `build-dead-seats.json` is consistent, but two distinctions it flattens are material

`.ufo/waves/round-29/build-dead-seats.json` — all checks pass:

```
spawned 64 = landed_reports 41 + dead 23                       -> True
len(dead_seats) == dead == 23                                  -> True
41 landed .md files present in .ufo/waves/round-29/build/      -> True
overlap between landed reports and dead seats                  -> empty
all 23 dead seats have report == null                          -> True
all 23 dead seats carry one identical cause string              -> True
cause: host omp session 01a15c83 killed by SIGHUP 2026-10-21T16:10:51Z before the seat wrote its report
```

This is one host-level provider failure (single session id, single instant), not 23 independent
failures — consistent with M88's "provider" class. M88's specific claims verify: all three executors
(`R29ExecCore`, `R29ExecOracle`, `R29ExecCases`) are in the dead list with `final_output_bytes: 0`; and
the stray branch exists exactly as claimed — `git branch -a` shows `round29/R29ExecCore 31934e5`, while
`git worktree list` shows only the main worktree, so it is a leftover ref with no worktree directory.

Two distinctions the uniform cause string erases:

1. **Four of the 23 dead seats did produce output bytes**, contradicting the flat "before the seat wrote
   its report" framing: `R29CritPriorArt` 464, `R29CritByteIdentity` 366, `R29ReviewProvenance` 159,
   `R29ReviewGlobalFields` 23. Two of them retain partial work on disk —
   `.ufo/waves/round-29/scratch/R29CritPriorArt/census.py` (6562 bytes) and
   `.ufo/waves/round-29/scratch/R29ReviewProvenance/census.py` (13847 bytes) — which was recoverable and
   was not landed as a report. The other two have empty scratch directories.
2. Per F8, the instrument these dead executor seats were assigned to produce is committed but has no
   author in the landed corpus, so "never written" and "written but unattributed" are not
   distinguishable from this file.

---

## 3. Exact reproduction of the receipt

Base: `/tmp/fm-witness-2/base`, a copy of the `56fd949` tree — `plans/config_projection.py` sha256
`5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`, plus the pinned
`plans/fixtures/r29/{manifest.json,generate_test_data.py,profiles.json,hand/*}` and
`plans/fixtures/r28/webarena/config_files/test.raw.json`.

**Control** — `sha256sum` of the base copy = `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`,
identical to receipt line 1. `--selftest` exit 0, stdout begins
`SELFTEST clean cases=20 six_tokens_and_non_url_field,units_not_pooled,codepoint_offsets_and_key_token,…`;
`--summary` exit 0, last line `TOTAL findings=0 exit=0`. Matches receipt lines 1–2.

**Mutants** — each applied as a textual edit to a fresh copy of the base; the base file is restored by
re-copy afterwards, and the restored sha256 is re-verified equal to the pristine sha256 in every run
(`restored_identical: true` throughout). Mutant sources are the ones persisted in
`plans/fixtures/r29/mutation_witness.py` / `repair-mutation-witness.json`.

| Mutant | selftest exit | exception | `--summary` TOTAL | receipt line | match |
|---|---|---|---|---|---|
| `wrong_order_reversed` | 1 | `AssertionError` | `TOTAL findings=0 exit=0` | 3 | **exact** |
| `url_only_substitution` | 1 | `AssertionError` | `TOTAL findings=6 exit=1` | 4 | **exact** |
| `index_by_task_id` | 1 | `AssertionError` | `TOTAL findings=0 exit=0` | 5 | **exact** |

Mutant sha256 (mine, on `5673405e…` base): `wrong_order_reversed` `34cbba6e1137ef86ce7d4e3db03df50ab52517ba4687e6118b35f8158f3ff646`;
`url_only_substitution` `a558d2bc3169ff01025eefbd75dc97d5124df1f76c625542affc8c1fda71a0d1`;
`index_by_task_id` `579f57d09e5f4c50da7d2de36f9fed5779b99328b3451d4378463701ac5b870b`.

Kill sites, from the Python traceback frames, in the pinned `5673405e…` source:

- `wrong_order_reversed` → line **416**:
  `assert record["steps"][0]["applied_replacements"] == 1 and record["remaining_known_tokens_text"]["__GITLAB__"] == 0`
  — an **internal** assertion, *not* the cascade hand fixture.
- `url_only_substitution` → line **396**:
  `assert not findings and [s["applied_replacements"] for s in record["steps"]] == [2] * 6`
  — internal, not the URL-only hand fixture.
- `index_by_task_id` → line **456**:
  `assert [{"task_id": t["task_id"], "output_ordinal": t["output_index"], "output_filename": t["output_filename"], "projected_task": t["projected_task"]} for t in tasks] == index_case["expected_records"]`
  — the index hand fixture.

I confirmed the cascade hand fixture *is* independently load-bearing for the wrong-order mutant:
neutralizing only line 416 moves the kill to line **438**
(`assert text == order_case["expected_projected_text"] and …`), i.e. the hand fixture at
`plans/fixtures/r29/hand/cascade-order.case.json` fails the reversed-order mutant on its own.

Hand-fixture-only attribution for the receipt's three mutants (running just the three adopted fixture
assertions against each mutant, no other selftest code):

```
control                H1_cascade PASS, H2_urlonly PASS, H3_index PASS
wrong_order_reversed   H1_cascade FAIL, H2_urlonly PASS, H3_index PASS
url_only_substitution  H1_cascade FAIL, H2_urlonly FAIL, H3_index FAIL
index_by_task_id       H1_cascade PASS, H2_urlonly PASS, H3_index FAIL
```

The receipt's `url_only_substitution` row is the outlier: it fails all three fixtures, for the
whitespace reason in F2, so it cannot be attributed to the URL-only fixture.

---

## 4. Frozen data alone and wrong order — direct check

Independent census from the generator text only (`perm_census.py`, 720 permutations × 3 profiles,
source = the six `str.replace` calls at generator lines 11–16):

```
distinct_origins           canon=2aec098e5705c98c  perms_differing_from_canonical=0/720  distinct_digests=1  omit_WIKIPEDIA_identical=True
path_prefix                canon=54cf98337dc6751d  perms_differing_from_canonical=0/720  distinct_digests=1  omit_WIKIPEDIA_identical=True
trailing_slash_sensitivity canon=49bbee2e827996b7  perms_differing_from_canonical=0/720  distinct_digests=1  omit_WIKIPEDIA_identical=True
```

(The `distinct_origins` digest `2aec098e5705c98c…` matches `build-summary.txt`'s
`projected_text_sha256=2aec098e5705c98c…` for that profile.)

So: **0 of 720 orderings differ** on the frozen data, and omitting the `__WIKIPEDIA__` step entirely
is byte-identical too. The frozen data cannot discriminate order, and the receipt's
`findings=0 exit=0` for `wrong_order_reversed` is the correct consequence. The one caveat is F1: the
instrument's `steps` metadata and the `--summary` body still disclose the order it used, so "the frozen
data do not reveal order" is true of the projection and false of the tool's own emitted trace.

---

## 5. The strongest control I could construct, and its kill

`vs_text_byteidentical_control.py` — value-shape URL-only substitution at text level (byte surgery over
the original serialized text; no re-serialization, so it cannot drift from the source contract by
encoding choice). On the pinned `5673405e…` bytes:

```
--summary identical to control : True
--json differing top keys      : []      (per-profile differing keys: [] for all three profiles)
--selftest exit                : 1       (AssertionError)
hand-fixture-only              : H1_cascade PASS, H2_urlonly FAIL, H3_index PASS
```

This is the witness M87's principal requires and the receipt omits: a derived control that agrees with
the instrument on every real input, killed by exactly the URL-only hand fixture.

---

## 6. Draft lesson-and-mistake.md — gate-table status after execution

The draft's §3 gate table defers the Lesson and the proposed M85 row on the condition that "the
witness in §4 fails when run against the URL-only oracle and passes against the sequential-text
oracle, with both outputs recorded". Status per witness, after my execution:

| witness | draft status | after execution |
|---|---|---|
| W1 (cascade) | prediction, not run | prediction **confirmed** under one oracle reading; **not** under another (F5) |
| W2 (non-URL) | prediction, not run | **confirmed**, robust under both readings |
| W3 (JSON invalid) | prediction, not run | **confirmed** |
| W4 (index vs task_id) | prediction, not run | **confirmed** |
| W5 (missing/non-string map) | prediction, not run | **confirmed** at the instrument layer; source-layer errors differ in kind (F5) |

The draft's §1 disposition — "A control counts only after its witness is observed to fail" — is
**sound and now satisfied by the adopted fixtures** (F4). The draft's §2 "unobserved: every expected
output in §4" is now stale for W2–W5.

---

## 7. Residual risk and verification gaps

- **Reproduced against `5673405e…`, not the current `135cc682…` instrument.** The receipt, freeze v1 and
  the M87 row all predate the repair. I re-verified the receipt's three mutants against the pinned
  bytes; I did **not** re-run the whole mutation set against `135cc682…` (the lane moved again while
  I was writing this report). Whether the repair preserved the M87-relevant kill sites is unverified by
  me; `repair-mutation-witness.json` records the same three mutants as `killed: true`, and its
  `tool_sha256` is `135cc682…`, which is consistent but not independently reproduced by me.
- **The `index_by_task_id` receipt line cannot be reproduced from the receipt alone** (F6). Two
  implementations differ in exception class; only one matches.
- **The receipt stores no mutant digests**, so the receipt cannot detect a change in a mutant's
  definition. My reproduction used definitions that appeared in the repo only after the receipt was
  written.
- **`corpus/lessons/round-29.md` is untracked** (F7): the row I attacked is not yet in any commit, so a
  reader of the committed tree sees the receipt but not the row that cites it.
- **The instrument has no attributable author in the landed corpus** (F8), and four dead seats hold
  recoverable scratch work that was not landed (F10).
- **No independent oracle artifact for round 29 exists under `plans/` or `corpus/evidence/`** — the
  r29 oracle seat (`R29ExecOracle`) is dead and the only oracle-ish files are falsify-wave scratch
  artifacts. The prereg's "independent oracle agreement" is therefore carried by falsify-wave work
  (the v2 candidate cites `.ufo/waves/round-29/falsify/FOracle*.md`), not by a canonical artifact.
  I did not audit those four oracle reports.
- I did not audit the four falsify oracle reports, the `S074` BrowserGym source row, or the other
  falsify items; my scope was the mined-mistake fix, the receipt, and the dead-seat file.
- **Falsify-wave concurrency:** the lane's instrument, candidate, freeze and lesson files all changed
  under me between 14:21 and 14:25. Every claim above is pinned to the bytes named by the artifact
  under attack; a reader should re-check the current HEAD before acting on it.

---

## 8. What I did not do

No lane file was edited; no fixture, corpus file, SOURCES row, SCORECARD, candidate or lesson file was
touched; no git/jj state was mutated (read-only `log`/`show`/`diff`/`status`/`branch`/`worktree list`
only); no upstream import or execution; no network; no tool install or update (Python 3.14.8 stdlib
only, per the host-wide pacman pause). All mutation experiments ran on `/tmp` copies; all copies were
restored or deleted after use.

---

VERDICT: PARTIAL
