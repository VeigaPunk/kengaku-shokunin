# R32DraftRows — C1 registry rows S094 and S097, plus the S093 `used-by` cell change

Seat: `L1Kengaku32.R32DraftRows` (scribe, leaf — no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`, access date **2026-10-25** for every source opened.
Claims read first: `plans/round-32-claims.md` (freeze commit `0d32691d`), C1 only. Lane tip observed at
draft time: `6084cd3` ("round-32: freeze-commit gate receipt"), baseline `f20a1097` + `0d32691` + `6084cd3`;
`git status` shows sibling work in progress (`M plans/catalog_probe.py`, `M plans/round32_defects.py`,
untracked `.ufo/waves/round-32/…`) — not this seat's edits, untouched.

**No production edit was made by this seat.** Nothing under the lane was created, edited or deleted except
this one report file. All simulation ran on a copy in `/tmp/r32-R32DraftRows/sim/` (344 KB total scratch,
`/tmp/r32-R32DraftRows`, well under 60 MB). No tool was installed or upgraded (curl 8.23.0, Python 3.14.8 —
both already present; no channel used).

## 1. What I opened (fetch identity)

| Artefact | URL (pinned) | Bytes | sha256 |
|---|---|---|---|
| `main.py` | `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` | 14,138 (297 lines) | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` |
| `retry.py` | `…/9be8d8fe…/utils/evaluation/retry.py` | 4,519 | `db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e` |
| `abs.html` | `https://arxiv.org/abs/2412.05579v2` | 43,661 | `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` |

Both file digests are byte-identical to the captures in the landed scout reports (`R32SrcS094a.md` header,
`R32SrcS094b.md` header) and the abstract page digest matches `R32SrcS097.md` and `R32DraftEntry.md` — three
independent fetches, same bytes.

## 2. The two rows (verbatim, ready to append after `| S100 |`, i.e. after `corpus/SOURCES.md:113`)

```markdown
| S094 | Toolathlon task evaluation script (tasks/finalpool/ab-testing/evaluation/main.py) and the retry wrapper it imports — https://github.com/hkust-nlp/Toolathlon | code | A | the executed scoring code for one Toolathlon task at a pinned commit — what is compared against what, the tolerance the call site actually passes, which side-effect checks fail open, and how many retries the grade gets | commit 9be8d8fe07a497b18ee61e3f2ae694e9797f39eb, tasks/finalpool/ab-testing/evaluation/main.py:279-280 `# Validate with 0.05% tolerance` then `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)`, overriding the :58 default `tolerance_pct: float = 0.1`; :25 `required_fields = ["scenario", "A_conversion %", "B_conversion %"]`; :55 `expected_ratio.csv` against :268 `record.csv`; :70 `Missing scenarios:` and :72 `Unexpected scenarios:`; :100 `raise ValueError(f"Record validation failed:`; :218 `Don't fail evaluation if we can't check logs` (8 words); utils/evaluation/retry.py:44-45 `DEFAULT_MAX_ATTEMPTS = 3` and `DEFAULT_POLL_S = 5` | the grader is a state comparison whose operative tolerance is set at the call site, not the default: the produced record.csv must match groundtruth_workspace/expected_ratio.csv within 0.05 percentage points per scenario, and one missing or extra scenario name fails the task; before it, two infrastructure checks run — the bucket check falls back to the gcloud CLI and returns False on failure, while the log-bucket check fails open on any exception (:218) and fails closed only by falling off its credential guard; and the whole gate is re-run up to three times five seconds apart, so a state that converges on retry scores pass | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |

| S097 | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579 | paper | B | the survey's own five-part structure for LLM-as-a-judge evaluation — functionality, methodology, applications, meta-evaluation, limitations — for the preprint's own text; tier B because the abstract page names no peer-review venue and carries no journal reference | arXiv 2412.05579v2 (submitted 7 Dec 2024, last revised 10 Dec 2024), Abstract: "This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." (20 words); Comments: "60 pages, comprehensive and continuously updated" (6 words) | the field's own survey gives meta-evaluation its own part, separate from methodology and applications, so a grader's kind decides which part its validation belongs to — a deterministic comparison needs no judge meta-evaluation, an LLM judge does; the Limitations part is where a lane looks for the known failure modes of judge-based scoring | mined | 2026-10-25 | 180d | corpus/knowledge/benchmark-grader-semantics.md |
```

Row identity, as parsed: 11 cells each (`split("|")` on the stripped row → 11), no literal and no escaped
`|` in any cell, byte sizes 1,777 (S094) and 1,166 (S097). Cells 8-11 are `mined`, `2026-10-25`, `180d`,
`corpus/knowledge/benchmark-grader-semantics.md` in both rows. Tiers per the registry's own restatement
(`corpus/SOURCES.md:11-16`): S094 = **A** (source code, primary for its scope); S097 = **B** (survey /
strong secondary, and a preprint — the abstract page carries no journal reference and no venue, verified at
`abs.html`: `Journal reference` absent, `Comments: 60 pages, comprehensive and continuously updated`,
submission history `[v1] Sat, 7 Dec 2024` / `[v2] Tue, 10 Dec 2024`).

## 3. S093 `used-by` cell change — append-only, in place

One row, one cell, cell 11 only; no new row, no reordering, no other cell touched.

Row `S093` at `corpus/SOURCES.md:112`; cells 1-10 unchanged (id, source, kind, tier, scope, anchor, teaches,
`mined`, `2026-10-25`, `180d`). Cell 11:

```diff
- corpus/knowledge/benchmark-verifier-execution-model.md
+ corpus/knowledge/benchmark-verifier-execution-model.md, corpus/knowledge/benchmark-grader-semantics.md
```

Mechanism, verified mechanically: `new_row == old_row.replace(old_cell, new_cell)` is true, the changed cell
index set is exactly `[10]`, both rows parse to 11 cells, and the row grows 923 → 971 bytes (**+48 bytes
appended at the end of the cell**). The existing path stays first, so the round-31 entry keeps its citation
and `adoption_check.py`'s all-of test (it splits cell 11 on `,` and requires the citing entry among the
parts) is satisfied by an append, not a replacement. This is an **append-only in-place cell change**: the
registry is not a log, so the row is edited rather than superseded, and the previous citation is preserved
byte-for-byte as a prefix.

## 4. Verification receipts (all run by this seat)

**4.1 Schema, pipes, cell count, quote word counts** — assertions over the two row strings:

```
S094 cells= 11   S097 cells= 11
no literal `|` and no escaped `\|` in any cell: pass (both rows)
max whitespace-word count of any quoted span in the S094 anchor: 8   (<=25)
S097 abstract quote word count: 20                                   (<=25)
```

**4.2 Every quoted span is a byte substring of the pinned bytes** — 14/14 true, checked with
`q in <fetched file>`:

```
main.py   : '# Validate with 0.05% tolerance'
main.py   : 'validate_record_data(actual_records, expected_records, tolerance_pct=0.05)'
main.py   : 'tolerance_pct: float = 0.1'
main.py   : 'required_fields = ["scenario", "A_conversion %", "B_conversion %"]'
main.py   : 'expected_ratio.csv'
main.py   : 'record.csv'
main.py   : 'Missing scenarios:'
main.py   : 'Unexpected scenarios:'
main.py   : 'raise ValueError(f"Record validation failed:'
main.py   : "Don't fail evaluation if we can't check logs"
retry.py  : 'DEFAULT_MAX_ATTEMPTS = 3'
retry.py  : 'DEFAULT_POLL_S = 5'
abs.html  : 'This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key
            perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.'
abs.html  : '60 pages, comprehensive and continuously updated'
```

**4.3 Fleet census parser on a simulated append** (`sources-census.sh validate`, the same parser the
`--census` clause of C1 runs):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --file /tmp/r32-R32DraftRows/sim/corpus/SOURCES.md --today 2026-10-25
rc=0 ; 15 findings, all W04, identical set to the baseline run on the real lane:
  W04 S040, S048, S057, S058, S059, S064, S065, S066, S067, S068, S069, S071, S075, S076, S100
  ok  /tmp/r32-R32DraftRows/sim/corpus/SOURCES.md
```

Baseline for comparison (`--file` on the real lane, read-only): `rc=0`, the same 15 `W04`, `ok`. So the
append adds **no E-code and no new W-code** — no E01 (row shape), no E03/E04 (id or URL+scope duplicate: no
lane row carries `github.com/hkust-nlp/Toolathlon` as a bare repo URL or `arxiv.org/abs/2412.05579`), no
E05/E06/E07 (kind `code`/`paper`, tier `A`/`B`, status `mined` all in the enums), no E08 (opened
`2026-10-25` = today), no E09 (`180d` is the accepted `NNd` cadence), no E10, no E11 (both `used-by` paths
resolve once the entry file exists — see F6), no E12 (rows are inside `## Registry`).

**4.4 The C1 counter's own row-side fields**, on the simulated tree with a stub entry carrying exactly the
three `source:` lines and `verified-at: 2026-10-25` plus one index row:

```
$ python3 plans/adoption_check.py --lane /tmp/r32-R32DraftRows/sim --expect .ufo/waves/round-32/claims/adoption-expect.json
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=skipped   (rc=1: --census not passed, by design)

control, same command on the pre-append registry copy (no S094/S097, S093 cell unchanged):
entries=1 indexed=1 cited_rows=3 rows_present=1 rows_mined=1 usedby_ok=0 census=skipped
```

The delta `rows_present 1→3`, `rows_mined 1→3`, `usedby_ok 0→1` is exactly these two rows plus the S093
cell edit; nothing else in the simulated tree differs from the lane. `census=ok` and exit 0 remain the main
agent's Gate run against the real lane (the entry file and the README index row are other seats' bytes).

## 5. Provenance of each anchor span

| Row | Span (pin `9be8d8fe` / arXiv `2412.05579v2`) | Located in |
|---|---|---|
| S094 | `main.py:58` default `tolerance_pct: float = 0.1` | `R32SrcS094a.md:5` |
| S094 | `main.py:279-280` comment + `tolerance_pct=0.05` call | `R32SrcS094b.md:20` (and `R32DraftEntry.md` §S094) |
| S094 | `main.py:69-72` missing / unexpected scenario errors | `R32SrcS094a.md:8` |
| S094 | `main.py:100` `raise ValueError(f"Record validation failed:` | `R32SrcS094a.md:8` (`:98-102`) |
| S094 | `main.py:55`/`:56` `expected_ratio.csv`, `:268` `record.csv` | `R32SrcS094b.md:34,55-56` |
| S094 | `main.py:218` `Don't fail evaluation if we can't check logs` | `R32DraftEntry.md:164-165` (`main.py:216-218`), function span `R32SrcS094b.md:32` |
| S094 | `main.py:225`/`:234` gate calls, `:149-152` gcloud fallback | `R32SrcS094b.md:26-27,29-30` |
| S094 | `retry.py:44-45` `DEFAULT_MAX_ATTEMPTS = 3`, `DEFAULT_POLL_S = 5` | `R32SrcS094b.md:47` ("max 3 attempts") + this seat at `retry.py:44-45` |
| S094 | `main.py:25` `required_fields = ["scenario", "A_conversion %", "B_conversion %"]` | **this seat**, byte-verified against sha256 `3bad26b6…` |
| S097 | abstract five-perspectives sentence (20 words) | `R32SrcS097.md:20` |
| S097 | `Comments: 60 pages, comprehensive and continuously updated` | this seat, `abs.html`; preprint status `R32SrcS097.md:27` |

The S094a/b and S097 scout reports landed while this seat was drafting; the rows were rebuilt to carry the
spans those reports located, and every one of them was re-checked by this seat against its own byte-identical
fetch rather than copied on trust.

## 6. Findings routed (not fixed here — outside a leaf's write scope)

**F1 — the staged S097 row's quote is not a byte substring (kill-rule exposure).** `SOURCES.append.md` S097
anchors `"the LMs-as-judges paradigm"`. That string is absent from `abs.html` (`'the LMs-as-judges paradigm'
in page == False`); the page reads `the LLMs-as-judges paradigm` (`== True`). Under C1's kill rule ("a cited
source whose located quote cannot be found at the pinned revision is refused for that row") the staged row
would be refused. My row carries the true bytes, agreeing with `R32SrcS097.md:20`.

**F2 — the staged S094 row quotes a tolerance the grader never uses.** It anchors
`tolerance_pct: float = 0.1` (the signature default, `main.py:58`) as if it were operative. The executed call
site is `main.py:280` → `tolerance_pct=0.05` under the comment `# Validate with 0.05% tolerance` (`:279`).
My row quotes both spans and says which one runs; the entry seat's draft already does the same.

**F3 — staged status cells.** Both staged rows carry `opened=2026-10-23` and a prose `recheck` cell
("re-verify at the next upstream release"). C1 requires `opened=2026-10-25` (the pins were re-opened today)
and this draft's contract fixes `recheck=180d`; the rows above carry those cells.

**F4 — staged entry bytes contradict the code (entry seat's bytes, already corrected in its draft).**
`/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-grader-semantics.md`
carries `verified-at: 2026-10-23` (line 5) and, in
§Toolathlon, `validate_record_data(actual_records, expected_records, tolerance_pct=0.1)` (line 67) and "any
conversion rate outside the 0.1-percentage-point tolerance" (line 69) — both falsified by `main.py:279-280`.
`R32DraftEntry.md` (§S094, `verified-at: 2026-10-25`) fixes all three; the staged file must not land as-is.

**F5 — the staged package carries rows outside this claim.** Besides S094/S097 it stages S077-S092, S093,
S095, S096, S098-S115. Notably **S103** is a second row for the *same* paper as S097
(`https://arxiv.org/pdf/2412.05579` vs `…/abs/2412.05579` — different normalised URLs, so no E04) whose
`used-by` names `corpus/knowledge/judge-meta-evaluation-2026-10-23.md`, a path absent from the lane — appending
it would raise **E11** and would also be an uncited row for a paper S097 already covers. Only S094 and S097
belong to C1's three-citation predicate; the rest must be rejected for this round by the collision guard.

**F6 — landing order is load-bearing.** `corpus/knowledge/benchmark-grader-semantics.md` does not exist at
baseline, and census **E11** resolves every `used-by` path on disk. Appending the rows before the entry file
lands makes validate print three E11 lines (S093's new path, S094, S097). Rows, entry and README index row must
land in one commit, or entry-first.

**F7 — cosmetic citation mismatch.** `R32DraftEntry.md`'s S097 `source:` line uses
`https://arxiv.org/abs/2412.05579v2`; the registry row uses `https://arxiv.org/abs/2412.05579`. No counter
compares them (the predicate matches ids only); align if the lane wants byte-equal citations.

## 7. Limits of this report

- Quotes are located in the **pinned bytes**, not in a rendered page: `abs.html` is the HTML source of the
  abstract page, and the quoted sentence is inside its `<blockquote class="abstract mathjax">`.
- The two rows describe **one** Toolathlon task's evaluator (`ab-testing`). Nothing here is a benchmark-wide
  claim; the entry draft states the same limit.
- The census and counter receipts in §4 ran against a **simulated** tree (rows + stub entry + one index row,
  knowledge/lessons trees symlinked read-only to the lane). They prove the rows' cells, shapes and citations;
  they are not the Gate run, which needs the real entry bytes and the real README row.
- No source was executed and no benchmark trial was run; fail-open / fail-closed readings are code properties
  read at `9be8d8fe`.
- Unrun: `python3 plans/round32_c1_verify.py --lane .` and the `--census` half of `adoption_check.py` — both
  need the entry file and README index row this seat may not create. An unrun check has not passed.

VERDICT: schema-clean
