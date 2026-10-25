# R33RowDrafts — registry rows S103/S104 + quote/url-map inputs for the adoption gate

Seat: scribe (kengaku round 33, hyaku run 7, 2026-10-25). Role: draft the two new
fleet-schema registry rows and the gate inputs. Leaf: no subagents, no background jobs.

## 0. Verdict

**VERDICT: rows-drafted**

Three artifacts on disk under `.ufo/waves/round-33/assimilation/` plus one gate-input
re-derivation. The adoption gate accepts the rows **and** every quoted span locates in
the captured bytes at the pinned revision:

```
QUOTE rows=2 spans=8 located=8 found=8 overlong=0 absent=0 malformed=0 cap=25 artifacts=SHA256SUMS.txt,arxiv-2412.05579v2-abs.html,swebench-pro-tests-test.sh,toolathlon-ab-testing-evaluation-main.py,toolathlon-utils-evaluation-retry.py mismatch=0 unmapped=0 urlmap=url-map.json entries=3   (exit 0)
registry=95 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0                                                       (exit 0)
SELFTEST cases=17 failed=0                                                                                                        (exit 0)
```

## 1. What I opened (not re-run to decorate: each line is a command I ran)

| probe | command | outcome |
|---|---|---|
| freeze claims | read `plans/round-33-claims.md` | C1 predicate: entry cites exactly S093/S103/S104; rows `status=mined`, `opened=2026-10-25`, `used-by` names the entry |
| staged rows | read `shokuknow/merge/kengaku/SOURCES.append.md` lines 30-38 | staged S094 = Toolathlon `evaluation/main.py`; staged S097 = arXiv 2412.05579 |
| capture identity | `curl -fsSL https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` → `/tmp/r33-R33RowDrafts/main.pinned.py` | 297 lines / 14,138 B; sha256 `3bad26b6…9b9ad` **identical** to `captures/toolathlon-ab-testing-evaluation-main.py` (I fetched, I did not assume) |
| quote line numbers | `nl -ba` on both captures | see §2; every `:NN` in the rows is a line of the capture |
| gate source | read `plans/sources_adopt.py` (row parser, `quote_check`, `bind_failure`, `main`) | `--quote-file` parses **markdown 11-cell rows**, not JSON (§5) |
| adoption path | `plans/sources_adopt.py --registry /tmp/…/SOURCES.head.md --package …/append-rows.md --admit-ids S103,S104 --entries corpus/knowledge/benchmark-grader-semantics.md --access-date 2026-10-25 --out /tmp/…/block.md` | `registry=95 staged=2 collisions=0 malformed=0 duplicates=0 defects=0 prose=0`, exit 0; emitted block is line-identical to my draft |
| census (post-append working tree) | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | `kengaku ok …/corpus/SOURCES.md`, exit 0, **15 W04** (unchanged) |

`SOURCES.head.md` is `git show HEAD:corpus/SOURCES.md` (95 rows, ids ≤ S102): the true
pre-append tree. Running the adoption gate against the *working-tree* registry would
report S103/S104 as collisions — because that tree already carries them (§4).

## 2. The three artifacts

### (1) `.ufo/waves/round-33/assimilation/append-rows.md`
sha256 `9d00d4a1f068efebf90fad4e711a12e5994257715dd6e4660b265a8a2726aace`, 3,103 B,
**two rows, no header** (append-ready; the gate parses them without one).

Cell-by-cell, S103 (Toolathlon, `code`, tier **A** — primary source code):

| cell | content |
|---|---|
| source | `…(tasks/finalpool/ab-testing/evaluation/main.py) — https://github.com/hkust-nlp/Toolathlon — pinned blob https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe…/tasks/finalpool/ab-testing/evaluation/main.py` |
| scope | what is compared (produced `record.csv` vs `groundtruth_workspace/expected_ratio.csv`), against what reference, and with **the tolerance the sole call site passes rather than the signature default** |
| anchor | pin `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` + six located spans at `:58`, `:279`, `:280`, `:218`, `:234` (all ≤25 words, word counts are the gate's own counter) |
| teaches | scores a *produced artefact* against a *ground-truth artefact* under a tolerance **fixed at the call site — 0.05 percentage points per scenario, not the 0.1 signature default**; the same task's log check fails open on caught exceptions while absent credentials fall through to implicit `None` and fail the task |
| status / opened / recheck / used-by | `mined` / `2026-10-25` / `180d` / `corpus/knowledge/benchmark-grader-semantics.md` |

S104 (arXiv, `paper`, tier **B** — preprint at opening):

| cell | content |
|---|---|
| source | `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://arxiv.org/abs/2412.05579` |
| anchor | pin `2412.05579v2` (v1 Sat 7 Dec 2024, v2 Tue 10 Dec 2024, abs page `:165`/`:167`) + `:41` title (8 words), `:124` abstract (20 words), `:131` comments (6 words) |
| teaches | the survey separates **meta-evaluation** — how a judge itself is scored — from methodology, so judge-based scoring owns a validation protocol a deterministic grader does not need; quoted in the survey's own spelling (**LLMs-as-Judges** in the title, **LLMs-as-judges** in the abstract), not the staged single-L typo (`LMs-as-judges`) |

Two staged misstatements repaired, both grounded in the capture:
1. **executed tolerance.** `main.py:58` declares `tolerance_pct: float = 0.1`; `:279-280`
   override it — `# Validate with 0.05% tolerance` then
   `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)`, the only
   call in the file. The `0.1` is a declaration, never executed; the row says so explicitly.
2. **error paths.** `:218` is `return True  # Don't fail evaluation if we can't check logs`
   inside `except Exception as e:` (fail **open** on caught exceptions). But
   `if project_id_from_creds and credentials:` at `:176` has no `else`: absent credentials
   fall out of the `try` with an implicit `None`, and `:234`
   `if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):` then
   raises. Credential absence fails **closed** — not "fail open" as the staged row said,
   and not "both paths fail open" either.

### (2) `.ufo/waves/round-33/assimilation/quotes.json`
sha256 `48cf004f94beaf2243c051e21908aae22ba9d462eafd0f0241ef1e37f424023e`, 4,077 B.
Per row: `id`, `staged_as`, `capture` filename, capture sha256/bytes/lines, `cited_url`,
`pin`, `path`, the fetch check, and each quote with its line, word count and role. It also
carries the one-command gate line and the two pieces of provenance the byte check cannot
supply: the `gate.note` (§5) and `uncited_capture` (`toolathlon-utils-evaluation-retry.py`
is mapped but no quote of these rows locates there — it belongs to the entry's retry
paragraph).

### (3) `.ufo/waves/round-33/assimilation/url-map.json`
sha256 `76c75639110cd95cf56e6cc1a5f0aa16fb129f02d9e818e9580454d15f5c9082`, 410 B.

```
toolathlon-ab-testing-evaluation-main.py → https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe…/tasks/finalpool/ab-testing/evaluation/main.py
arxiv-2412.05579v2-abs.html              → https://arxiv.org/abs/2412.05579
toolathlon-utils-evaluation-retry.py     → https://github.com/hkust-nlp/Toolathlon/blob/9be8d8fe…/utils/evaluation/retry.py
```

(The map already existed at 161 B with **repo-root** values, written by a sibling seat this
wave; I replaced it with the pinned blob URLs the assignment specifies. The rows therefore
cite *both* the repo root and the blob URL — see §3.)

## 3. Two schema constraints that shaped the draft

- **`check_v2` of `plans/round33_c1_verify.py` takes the FIRST URL of the source cell** and
  requires `host_path` to be a substring of the entry's `source: S103` line. The entry (not
  mine to edit) names `https://github.com/hkust-nlp/Toolathlon` — so the repo root must
  stay first, and the pinned blob URL rides second. Verified for both rows by replicating
  the rule: `S103 host_path github.com/hkust-nlp/Toolathlon → True`,
  `S104 arxiv.org/abs/2412.05579 → True`. Multiple URLs in one source cell are precedented
  (`S105`, `S112`).
- **The census reads only the first URL** (`url_of`), so the second URL is invisible to
  E04/W04. Census is unchanged: exit 0, 15 W04, same 15 ids as the freeze receipt.

## 4. Finding — the working tree already carries S103/S104 (uncommitted, another seat)

`corpus/SOURCES.md` (line 118/119) already holds S103 and S104, appended this wave and
still untracked-by-commit (`git status`: `M corpus/SOURCES.md`). They came from a sibling
build seat (the same text is in `assimilation/append-block.md` / `append-package.md`).
**Do not append my file on top of them: 11 cells each, duplicate ids, E03.**

My rows are a re-derivation that agrees on the load-bearing cells (kind, tier, status,
opened, recheck, used-by — identical) and differs only where precision improved:

| row | cell | live tree | my draft |
|---|---|---|---|
| S103 | 1 | repo root only | repo root **+ pinned blob URL** |
| S103 | 4 | "tolerance actually invoked" | names what is compared, and "the sole call site … rather than the signature default" |
| S103 | 5 | `(:58, signature default)` / `(:280)` | line-labelled `:58`, `:279`, `:280`, `:218`, `:234` with gate-counter word counts |
| S103 | 6 | "with a stated numeric tolerance" | names **0.05** as executed, not the 0.1 default |
| S104 | 4 | "because it is a preprint" | "…a preprint **at the time of opening**" |
| S104 | 5 | no line numbers, no title quote | `:41` title (spelling witness), `:124`, `:131` |
| S104 | 6 | generic | names the two spellings, three Ls |

So: either keep the live rows, or replace them with `append-rows.md`. Both satisfy the C1
predicate; mine carries the pin-precise citation and the 0.05 evidence the entry's prose
depends on. **This is the L1's call, not mine** — I wrote no production bytes.

## 5. Finding — `quotes.json` cannot be `--quote-file` (hollow-pass hazard)

`main()` routes `--quote-file` into `quote_check`, which runs `parse_rows` on the file with
`ROW_RE = ^( {0,3})\|[ \t]*(S\d{3,})[ \t]*\|`. A JSON file parses to **0 rows**, and
`quote_check` returns `EXIT_OK` for zero rows — `rows=0 spans=0 located=0 …`, exit **0**.
That is a green receipt proving nothing, and the sibling item `R33SourcesAdoptDry` is
instructed to run exactly `--quote-file quotes.json`. Recorded here so no receipt claims
otherwise; the gate-consumable file is `append-rows.md`. `quotes.json` carries this as
`gate.note` and `gate.command`. I did not modify the gate (no production edits).

## 6. Known limits / non-claims

- The gate's binding is **citation membership, not provenance** (its own docstring, round-31
  C3 critic): it cannot verify that the capture came from the cited URL. What *is* verified
  here: the Toolathlon capture's sha256 equals a fresh fetch of the pinned raw URL.
- The arXiv capture is HTML; `:41`, `:124`, `:131` are **page lines** of the saved document,
  not paper pages. No PDF page claim is made.
- One earlier draft span, the bare `return True` (2 words), located first in
  `swebench-pro-tests-test.sh` — another seat's capture, alphabetically earlier. It was
  replaced with the full 11-word line, which locates **only** in `main.py`; the receipt
  above shows every span at its own capture.
- I did not run `plans/round33_c1_verify.py` or `plans/round33_defects.py` (L1 receipts;
  the tree is mid-flight with sibling writes). I did not touch the entry, README, SCORECARD,
  lessons, or fleet reports. No tools installed.
- `/tmp/r33-R33RowDrafts/` holds only `main.pinned.py` (~14 KB) and the two temp registry
  copies — well under the 60 MB scratch bound.

## 7. Handoff

1. Reconcile §4 (keep or replace the live S103/S104 rows) — do not blind-append.
2. Re-run, in one line, to re-earn this receipt at the tip:
   `python3 plans/sources_adopt.py --quote-file .ufo/waves/round-33/assimilation/append-rows.md --artifact .ufo/waves/round-33/assimilation/captures --url-map .ufo/waves/round-33/assimilation/url-map.json`
   and `python3 plans/sources_adopt.py --selftest`.
3. Tell `R33SourcesAdoptDry` that `--quote-file` wants `append-rows.md`, not `quotes.json` (§5).
