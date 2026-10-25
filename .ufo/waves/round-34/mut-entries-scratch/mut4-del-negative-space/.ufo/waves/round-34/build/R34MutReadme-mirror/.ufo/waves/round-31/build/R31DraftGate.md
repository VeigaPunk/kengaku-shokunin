# R31DraftGate — the round-31 lesson `## Gate` block, drafted

Seat: `L1Kengaku31.R31DraftGate` (scribe, calibration). Date of every observation below: **2026-10-25**.
Scratch: `/tmp/r31-R31DraftGate/` (2.4 MB, of which 1.0 MB is the SWE-bench Pro task listing).
No production file was created, edited or deleted by this seat; the only lane write is this report.
No tool was installed or upgraded (nothing was needed).

Lane state this draft is written against — measured, not assumed:

- `git log --oneline -1` → `0883e72 round-30 verifier spot-check (integrator, hyaku): non-author admit/reject`
  (worktree carries the round's uncommitted work; `git status --porcelain` at 06:0x lists `M LOG.md`,
  `M corpus/SOURCES.md`, `M corpus/README.md`, `M corpus/knowledge/contamination-transparency-card.md`,
  `M corpus/lessons/round-30.md`, `M plans/sources_adopt.py`, the five round-30 seat reports, and
  `?? .ufo/waves/round-31/ ?? corpus/evidence/round31/ ?? plans/round-31-claims.md ?? plans/round31_*.py`).
- `corpus/SOURCES.md` → **91 rows** (88 at baseline + S092, S093, S100 landed in the worktree).
- `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` →
  `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0.
- `python3 plans/round31_defects.py --lane .` → `checks=10 defects=1` + `DEFECT R9 …R30DraftGate.md still
  differs from HEAD`, exit 1.
- `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=17 failed=0`, exit 0.
- fleet census `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` →
  `kengaku ok`, **15** `W04` lines (14 at baseline; the new one is `S100 duplicate url
  github.com/laude-institute/terminal-bench-2 across scopes`).

The draft below is the block as the lesson should carry it. Where a value is not yet observable it is
marked **OPEN** with the command that closes it — an unrun check is not written as a pass.

---

## Draft: `## Gate`

```markdown
## Gate

Admission of one entry, `corpus/knowledge/benchmark-verifier-execution-model.md`, as the round that
discharges `corpus/README.md` §Frontier bullet 1's "runtime task validity" clause *for verifier execution
only*, and corrects the round-1 checklist's axis E ("grader integrity") from "partly observable" to a
coded default. The staged bytes are not admitted as they stand: every quoted span in the staged row set
was re-located at its pinned commit, three of the four staged anchor defects are repaired below, and the
staged entry's own guarantees were narrowed where the harness code makes them conditional.

|candidate|decision|reason|read|
|---|---|---|---|
|`corpus/knowledge/benchmark-verifier-execution-model.md` (staged, round 2 of the campaign) | **admit, re-grounded** | the axis-E sub-question is answered from the harness's own resolution rule (`src/harbor/models/task/verifier_mode.py:31` returns SHARED when neither `environment_mode` nor a verifier `environment` is set) and from the two benchmarks' manifests at their pins, not from either maintainer's prose; Q1 triad rebuilt (`source:` ×3 = S092/S093/S100, `verified-at: 2026-10-25`, `recheck: 180d` + action, `writer: KengakuR31`); the staged entry's claim that "the tests directory is re-uploaded" was **conditional** and is now stated with its guard (`verifier.py:209`); Q4 negative space carries six bullets including "no run was observed" and "a directory count is not a validity count" | §Round 31 admission; `.ufo/waves/round-31/build/R31DraftEntry.md`; `.ufo/waves/round-31/build/R31SrcS092a.md`–`R31SrcS100b.md` |
|`benchmark-grader-semantics.md` (package) | reject this round | a second theme (what a grader *is*, across SWE-bench Pro / Toolathlon / a judge survey) whose three cited rows are S093, S094, S097 — S094 and S097 are not opened this round, and CORPUS rule 4 forbids appending a row no admitted entry cites; admitting it would need two more source opens in a round whose one theme is the verifier *execution* model | `knowledge/corpus/knowledge/benchmark-grader-semantics.md:2-4` read in-package |
|`terminal-bench-release-identity.md` (package) | reject this round | third theme (release identity across two repositories) on the same two rows; its distinctive claim — "the repository carries no git tags" — is already carried by S100's own anchor and was re-derived this round (`GET /repos/laude-institute/terminal-bench-2/tags` → `[]`; `harbor-framework/terminal-bench` → exactly `v4.0.0`, `v3.0.0`), so a second entry on the same two rows would duplicate, not extend | `knowledge/corpus/knowledge/terminal-bench-release-identity.md:2-3`; this seat's two tag API calls |
|`judge-calibration-thresholds.md` (package) | reject this round | round 30's Q3 objection survives in the staged bytes: the entry's kappa paragraph attributes "per-variable linear-weighted kappa … 0.00 to 0.35 (median 0.21) … ceiling of 0.84 … pooling raises kappa to 0.46" to "the contamination-disclosure paper's pre-registered audit", and that paper is **not one of its three `source:` lines** (S078, S081, S087) — so no anchor cell carries the numbers, and the reason addresses the property the claim asserts (Q9) | `knowledge/corpus/knowledge/judge-calibration-thresholds.md:36-46` vs `:1-3` |
|remaining 64 staged entries and 172 staged rows | reject this round | CORPUS rule 4 (expansion is knowledge, not rows), plus the campaign-schema defects this round measured itself: **175** row lines, of which **173** parse as 11-cell rows; **S093** carries 12 cells and **S101** 15 (escaped pipes), **174/175** rows carry a `recheck` cell the gate's own `CADENCE_RE` (`^\d+d$`) scores as prose, and **12** staged ids collide with the pre-append registry | `.ufo/waves/round-31/assimilation/{reg-ids,staged-ids,collisions}`; §Id collisions; §Staged-row normalization below |
|`considerthese` — none proposed this round | not applicable | no proposal file was staged for round 31; nothing to land as a criterion | — |

**Flip conditions** (one per rejection, so a rejection is never "never"):

- `benchmark-grader-semantics.md` — flips when S094 and S097 are opened in a round whose theme is grader
  semantics, and its S093 claim is re-grounded on the `parser.py` log scan rather than on the reward line
  alone (the round-31 entry already records that reading at `:98-99`).
- `terminal-bench-release-identity.md` — flips when it carries a fact about release identity that S100's
  anchor does not: a tag *list* for the renamed repository, or a dated release note.
- `judge-calibration-thresholds.md` — flips when the kappa/ceiling figures are re-cited to the row of the
  paper that publishes them (the package's S123, `Jangulo7/contamination-disclosure-paper`) and that row
  is opened in the same round.
- the remaining 64 entries and 172 rows — flip one entry at a time under CORPUS rule 4, each with its own
  re-opened sources and schema-valid rows; the two pipe-broken rows are fixed by the rewrite pattern in
  §Staged-row normalization, not by an escape.

**Id collisions.** The decision was taken against the 88-row registry: ids in use were S001–S086 plus
S090 and S091 (`.ufo/waves/round-31/assimilation/reg-ids`, re-derived by this seat as
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 88). The staged space is S077–S251
(175 ids). The intersection is **12** ids — S077, S078, S079, S080, S081, S082, S083, S084, S085, S086,
S090, S091 (`.ufo/waves/round-31/assimilation/collisions`) — and it is larger than round 30's six only
because round 30 itself admitted S081–S086; the collision set grows by exactly the ids the lane has
already appended. **S092, S093 and S100 are not in it**: none of the three appears in `reg-ids`, so they
enter the lane's own S-space without renumbering, and no held row's id moves. The gate confirms the same
partition from the package itself: `registry=88 staged=173 collisions=…` with `--scope-to-admit` narrowing
to the three admitted ids (receipt in §Receipts). After the append the same invocation reports
`collisions=2` (S092, S100; S093 is not parsed, so it cannot collide) — a receipt of the append must
therefore be committed *with* the append and never re-run as a check.

**Staged-row normalization record.** Four repairs, each with the mechanism that forces it:

1. **Prose `recheck` → cadence.** Staged cell: `2026-10-23 — re-verify at the next upstream release (Gate
   S092 below)` (identical in form for S093, S100). The gate's `row_defects` accepts only
   `^\d{4}-\d{2}-\d{2}$`, `^\d+d$` or one of `on-release|on-request|on-commit|never`
   (`plans/sources_adopt.py:42-44`), so all three are prose; `--recheck 180d` writes the cadence and the
   stripped prose is *kept in the entry's frontmatter* (`recheck: 180d — re-run the three pinned fetches …`),
   which is where QUALITY Q1's "cadence **and** the re-check action" is satisfied. Measured across the whole
   package under the gate's own rule: **174 of 175** rows are prose — so this is a campaign-wide schema
   property, not a defect of the three rows.
2. **Escaped pipe → pipe-free anchor (S093; the same pattern applies to S101).** The staged S093 anchor
   quotes `all_required = fail_to_pass \| pass_to_pass`. Three independent failures follow from that one
   escape, and each was reproduced: (a) the row splits into **12** cells, so `collect()` drops it and the
   gate reports `malformed: S093:escaped-pipe` (package run) / `malformed=['S093:escaped-pipe']` (quote run);
   (b) the fleet census emits `kengaku E01 S093 fields=12` and exits 1 when the row sits inside
   `## Registry` (measured on a scratch root built from `0883e72:corpus/SOURCES.md`: 88 rows clean at
   exit 0 / 14 W04, the same tree plus this one row at exit 1), and `E12 S093 row outside Registry section`
   if the row is appended after the table instead (also measured); (c) as a
   *quote* the span is not a byte substring at all — `"\\|" in test.sh` is `False`, because the source byte
   is a bare `|`. The repair used here states the union in words and quotes only the pipe-free reward line:
   `line 213 assigns all_required as the set union of fail_to_pass and pass_to_pass and :214 "success =
   all_required <= passed_tests"`. Nothing is dropped from the claim; the operator character is.
3. **`used-by` projection.** The staged cells name two entries each — S092 and S100 →
   `benchmark-verifier-execution-model.md, terminal-bench-release-identity.md`; S093 →
   `benchmark-verifier-execution-model.md, benchmark-grader-semantics.md`. Since only one entry is admitted,
   the projected cell is exactly `corpus/knowledge/benchmark-verifier-execution-model.md`; the other two
   entries are rejected above, so a two-path cell would point at knowledge this lane does not hold.
   `adoption_check.py`'s `usedby_ok` reads precisely this (`:21`, `:90-98`).
4. **`opened` re-date.** Staged `2026-10-23` → `2026-10-25`, carried by `--access-date 2026-10-25
   --attest-opened`, because all three documents were re-fetched at their pinned commits this round (fetch
   identities below). The stage's own date stays visible in the staged bytes, which this lane never edits.

A fifth repair is recorded as *not made*: the staged `source` cells cite repository roots
(`https://github.com/laude-institute/harbor`, `…/SWE-bench_Pro-os`, `…/terminal-bench-2`). The lane's own
precedent for a file-level claim is a file URL (S077, S078), and the URL binding below is strict about
subpaths (`normalize_url` keeps the path case-sensitive and treats a subpath as a different document,
`plans/sources_adopt.py:349-362`). The rows as landed keep the repository root and name the file inside the
anchor; that is bindable **only** when the artifact is a tree capture mapped to the repository URL, which is
what §Access date and quote evidence demonstrates. A reader who maps a single-file capture to the repo root
gets exit 8 — correctly.

**Access date and quote evidence.** Access date `2026-10-25` for all three rows; every fetch is a pinned
commit; word counts are whitespace tokens (`words()`, the counter the gate prints).

| row | fetch (bytes, sha256 prefix) | quote, located | words |
|---|---|---|---|
| S092 | `src/harbor/models/task/config.py` @6099b8cf — 39055 B, `ac9f5d19…` | `:587-594` `environment_mode` description; the default rule is a **four-line implicit concatenation** (`:590-593`), so it is quoted by physical line: "Whether the verifier runs in the agent's environment ('shared')" / "or in a dedicated container ('separate'). When omitted: defaults" / "to 'separate' if a verifier 'environment' is set, otherwise" / "'shared'." | 9/10/10/1 |
| S092 | `src/harbor/verifier/verifier.py` @6099b8cf — 11910 B, `fc5d9fc6…` | `:168` "Discard stale rewards without removing other verifier inputs or logs."; `:207` `await self._remove_reward_files()`; `:209` `if not self._skip_tests_upload:` guards `:220-223` `await self.environment.upload_dir(source_dir=source_dir, target_dir=str(env_paths.tests_dir))`; `:50` `skip_tests_upload: bool = False`; `:128` "The verifier image already owns /tests/test.{sh,bat}." | 10 / — / — / 6 |
| S092 | `src/harbor/models/task/verifier_mode.py` @6099b8cf — 5142 B, `e5893be9…` | `:31` `return _resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED`; `:84-87` `class VerifierEnvironmentDefinition` with `bundled_tests: bool` (`:86`) | — |
| S093 | `v2/tasks/instance_internetarchive__openlibrary-00bec1e7…/tests/test.sh` @66f92766 — 7864 B, `b6f26eec…` | `:33` "Resetting test-space to base state (full test-code surface)..."; `:29` "find . -name '__pycache__' -type d -prune -exec rm -rf {} +" (the staged cell drops the trailing `2>/dev/null \|\| true` — a narrowing, not a widening); `:71` `T) git checkout HEAD -- "$path"`; `:93` "untracked files the patch merely MODIFIES are left alone (image-provided context)"; `:97` `git diff --name-only HEAD --`; `:213-214` reward union + `"success = all_required <= passed_tests"` | 8/12/1/11/5/5 |
| S093 | `v2/README.md` @66f92766 — 6858 B, `dde4168f…` (the qualifier the entry corrects) | `:75` "The verifier never runs in the agent's sandbox."; `:99` "731 -> 642 tasks: 89 dropped after review." | 8/8 |
| S100 | `README.md` @2fd12b88 — 4574 B, `7dfa9992…` | `:51` "You can view them at https://github.com/laude-institute/terminal-bench-2"; `:46` "--dataset terminal-bench@2.0" | 10/2 |
| S100 | contents API `GET /repos/laude-institute/terminal-bench-2/contents/?ref=2fd12b88…` — 96537 B | 92 top-level entries = **89 directories** + `.gitignore`, `LICENSE`, `README.md`; the same call on `/repos/scaleapi/SWE-bench_Pro-os/contents/v2/tasks?ref=66f92766…` — 956505 B → **642** entries, all directories | — |
| S100 | `GET /repos/laude-institute/terminal-bench-2` and `/tags` | the name **301-redirects** to `harbor-framework/terminal-bench-2` (repo id 1063848495); `/tags` → `[]`; `/repos/harbor-framework/terminal-bench/tags` → exactly `v4.0.0` (452bf30), `v3.0.0` (2b0442c) | — |
| S092/S093 | `task.toml` at both pins — 973 B / 889 B | TB2 `protein-assembly`: `[verifier]` = `timeout_sec = 1800.0` only, `[environment] allow_internet = true`; SWE-bench Pro V2 `…openlibrary-00bec1e7…`: `[verifier] network_mode = "public"`, `timeout_sec = 3000.0`, `collect = []`. Neither sets `environment_mode` or `[verifier.environment]`; both carry an **empty `[verifier.env]`**, which is the env dict and not an opt-in | — |

**What the quote gate says about the landed rows** (each run is `plans/sources_adopt.py --quote-file … --
artifact <tree capture> --url-map <repo root>`; the tree capture is the fetched files at the pinned commit,
mapped to the repository URL each was fetched from):

| row | exit | detail |
|---|---|---|
| S093 | **0** | 3 spans, all located in the tree capture |
| S092 | **7** | 1 of 2 spans located; the 13-word default-rule quote is `absent` — it is not a byte substring of `config.py`, because the description is four implicitly concatenated string literals |
| S100 | **4** | `S100:no-quote` — the anchor carries no `"` span at all; its evidence is a re-derived listing, not a sentence |

The binding itself, measured on real bytes (the three outcomes the C3 claim names, plus the two it does
not): a file-level citation mapped to its own file URL → **0**; the same row mapped to the repository root
→ **8**; one artifact unmapped → **9**; no map at all → **0** (byte-presence only, unchanged); and a row
that cites *two* URLs, one of them an ancestor of the artifact, accepts either mapping → **0**, which is
the multi-URL weakening of the binding, not a pass.

**Per-criterion record for the admitted entry** (Q1–Q19; the bar is `corpus/QUALITY.md`). Q1 pass
(`:1-6`: three `source:` lines, `verified-at: 2026-10-25`, `recheck: 180d` with its action, `writer:
KengakuR31`); Q2 pass (S092 A code, S093 A code, S100 A dataset — each load-bearing claim rests on the row
whose `scope` names it; the two manifest reads rest on S092/S093, the count on S100); Q3 pass for every
span in the landed rows **except** the S092 default-rule sentence, which must be quoted by physical line
(see the exit-7 row above — this is an OPEN repair, not a pass); Q4 pass (§What this does not establish,
six bullets, plus a named falsifier at `:129-137`); Q5 pass (S092/S093 are the maintainers' own code read
at a pin, S100 a repository tree; the entry states "no run was observed" rather than treating code as
behaviour); Q6 pass (§Extends names `benchmark-task-validity-checklist.md` and the coverage row, and
corrects rather than overwrites); Q7 **OPEN** — entry, index row, registry rows and coverage row must land
in one commit, and at the time of this draft they are worktree changes only; Q8 pass (this Gate: one admit,
four rejects — a fifth row records the `considerthese` slot as not applicable — each reject with a flip); Q9 pass (each rejection's reason addresses its own property: a theme
mismatch for two, an unanchored number for one, schema for the bulk); Q10 **OPEN** — the second seat is the
placeholder below; Q11–Q12 not engaged (no interval-gated pass is claimed); Q13 **OPEN** — the admitting
commit must already contain every report this Gate cites, and the entry itself cites
`.ufo/waves/round-31/build/R31DraftEntry.md` and `R31SrcS093b.md`; Q14/Q15 apply to that commit's tree;
Q16–Q17 not engaged; Q18 not engaged (no forecast); Q19 **OPEN** — `.ufo/waves/yield.tsv` still has to be
appended, one row per dispatched seat.

**C1 receipt (frozen predicate, `plans/round-31-claims.md`).**
`python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` →
`entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0. Control on
the pre-append tree: `.ufo/waves/round-31/claims/control-nothing.txt` =
`entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok`, exit 1. Census delta:
14 → **15** `W04`, the new line being `S100 duplicate url github.com/laude-institute/terminal-bench-2
across scopes` — expected, not a defect: S100 and S079 cite the same repository for different scopes and
S100's own `scope` cell names S079 as the other reading. No other warning class appears, and no held row
changed id, tier or status.

**C2 receipt.** `python3 plans/round31_defects.py --lane .` → `checks=10 defects=1`, exit 1, the open
defect being R9 (five round-30 seat reports still differ from `HEAD`). Control:
`.ufo/waves/round-31/claims/defects-before.txt` = `checks=10 defects=10`, exit 1. C2 is therefore a
**partial** closure at the time of this draft and is not written as a pass. One check changed during the
round and the change is recorded, not smoothed: R6 first reported `the entry states 2 unregistered staged
sources, the registry gives 3` while the entry was right — S001 holds the GEM 2026 review under
`https://aclanthology.org/2026.gem-main.50/`, the staged file cites `…50.pdf`, and the counter's
`url.rstrip("/") in registry` test could not see the difference. The counter now normalises through
`document_key()` (`plans/round31_defects.py:180`, strips a trailing `.pdf`, lowercases) and R6 passes. The
defect was in the comparator, not in the entry.

**C3 receipt.** `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=17 failed=0`, exit 0; the
three new cases are `quote-url-accepted`, `quote-url-mismatch-refused`, `quote-url-unmapped-refused`.
Control: `.ufo/waves/round-31/claims/gate-before.txt` — the baseline tool rejects `--url-map` with argparse
exit **2** and its selftest prints `cases=14`. Limits this Gate records rather than hides: (a) the binding
is only as strong as the map, and a row that cites an ancestor URL accepts an ancestor mapping (measured,
exit 0); (b) `normalize_url` is deliberately narrow, so a repository rename is a mismatch — this round's own
S100 citation 301-redirects to `harbor-framework/terminal-bench-2`, and a capture fetched from the canonical
name is refused against a row citing the alias (exit 8, measured); (c) a row whose evidence is a tree
listing carries no quoted span, so it cannot be quote-gated at all (S100, exit 4).

**Non-author spot-check (placeholder; QUALITY R6/Q10/Q13 — filled by a seat outside this round's dispatch
roster, never by a lane seat).**

> Spot-checker id: `<outside id>` — `grep -rn '<id>' .ufo/prompts/` must return nothing.
> Sample (one admit, one reject, one new row): the entry's S092 default-rule sentence re-read at
> `config.py:590-593`; the `judge-calibration-thresholds.md` rejection re-read against its own `:1-3`
> source lines; the S093 row's `test.sh:213-214` reward claim re-read. Per item: agree / disagree, the
> re-opened capture's identity, and the reason. Verdict: `<AGREE|DISAGREE>`.
```

---

## Draft: `## Mistakes`

The round-30 closure routed ten defects to this lane (`corpus/lessons/round-30-verifier-spotcheck.md` §5
items 1–8, expanded into R1–R10 by `plans/round31_defects.py`). The rows below are the classes those
defects share, written in the round-30 lesson's form, plus the two defects this round's own drafting
found. Each row states what would have caught it, because "captured-by: none" is the interesting case.

```markdown
## Mistakes

- **Class: a retraction that stops at the entry.** Evidence: round 30 retracted the "two new fields, one
  new value set" delta inside the admitted entry (`corpus/knowledge/contamination-transparency-card.md`)
  and left the same declaration standing in `LOG.md:792-793`, so the lane's own log stated a claim its
  corpus had already withdrawn. **Captured-by:** the non-author closure, one round late — the entry and
  the log disagree, and only a reader holding both can see it. **Fix:** an appended, dated correction
  entry that quotes the superseded wording, labels itself a correction, and states the admitted wording;
  `LOG.md` is append-only, so the original line stays byte-identical (`plans/round31_defects.py` R1
  re-derives all three conditions).
- **Class: a lesson cell that certifies a basis the round had already retracted.** Evidence: the Q6 cell
  claimed the delta was "one field, one placement, one value set" — the exact reading the entry now
  withdraws — and the Q2 cell listed S086 as tier A where the registry and the same lesson's own tier
  histogram say B; a third cell stated the round shape as "34 falsify" seats against a committed registry
  of 33. **Captured-by:** the closure's sample, not the lane's self-check: each cell was internally
  checkable against a file the lane already held. **Fix:** append-only errata that name the superseded
  sentence and the re-derived value (R2, R3, R10); a lesson never rewrites its own cells.
- **Class: a repair that leaves a twin.** Evidence: the duplicated "reconciled truth" sentence
  (`:125-126`) and the repeated falsifier clause are residue of an earlier edit that removed a bullet
  marker and a duplicated line but not both copies of the text. **Captured-by:** a whole-file sweep for
  repeated substrings, which nobody ran before the commit. **Fix:** one occurrence each, asserted by
  count (`R4`, `R5` assert `count == 1`, not "contains").
- **Class: one fact asserted two ways in one file.** Evidence: the entry said at `:41` that three staged
  source rows are unregistered and at `:160` that "two of its three" are. **Captured-by:** the closure;
  the lane could have re-derived the count from the staged file's own `source:` lines. **Fix:** state the
  re-derived count and keep the derivation beside it (R6 re-derives from the staged file rather than
  trusting either wording).
- **Class: a late narrowing of an overclaim.** Evidence: "S2's tri-state integrity flag is the only new
  field" survived into the entry against its own R3 row, which records the same vocabulary in a published
  form. **Captured-by:** the closure's cross-row read. **Fix:** narrow to what is new — the card-level
  field, not the vocabulary (R7 requires the narrowed phrase, not the absence of the old one).
- **Class: an adjective no row supports.** Evidence: "the CC0 card" at `:139`; no registry row records a
  CC0 licence for that design, and the form is reported under a different licence. **Captured-by:** the
  closure. **Fix:** drop the adjective or cite the row that records the licence — a licence is a fact, not
  a modifier (R8 refuses the adjective unless the registry carries the string).
- **Class: round work that outlives the round.** Evidence: five round-30 seat reports were still modified
  in the worktree after the driver's completion line, so the round's own evidence sat outside `HEAD`.
  **Captured-by:** `git status --porcelain`, which the closure ran and the lane did not. **Fix:** commit
  the reports under the round's entry, with the committed blob — not the path — as the test, so a stub
  cannot stand in for a report (R9 reads `HEAD:<path>` and refuses a file under 100 lines). **This is the
  one routed defect still open at this draft** (`checks=10 defects=1`).
- **Class: a counter that reports a defect the property does not have.** Evidence: this round's own R6
  check, before its comparator was fixed, printed `the entry states 2 unregistered staged sources, the
  registry gives 3` while the entry was correct — S001 holds the same GEM 2026 review under
  `https://aclanthology.org/2026.gem-main.50/` and the staged file cites `…50.pdf`, so a literal substring
  test could not see the row. **Captured-by:** the seat writing this Gate, by re-deriving the count from
  the staged file and the registry independently (`0 of 3` matched by the naive test, `1 of 3` by
  document identity). **Fix:** `document_key()` normalisation at `plans/round31_defects.py:180`; a
  comparator that cannot be wrong in one direction is worth as much as a check that cannot be skipped.
- **Class: a quoted span that is not a byte substring of the source.** Evidence: this round's own S092
  anchor quotes the 13-word default rule as one sentence; in `config.py` it is four implicitly concatenated
  string literals (`:590-593`), so `locates()` finds nothing and the lane's own quote gate refuses the row
  with exit 7 (measured, §Gate). The staged row had the same defect one level up — a 28-word version of
  the same span, over the 25-word cap. **Captured-by:** the quote gate itself, which is the point of
  having one; the lane's habit of quoting a *rendered* sentence is the cause. **Fix:** quote by physical
  source line and say so in the anchor; four spans of 9/10/10/1 words locate and pass.
```

---

## Findings — conflicts recorded verbatim for the canonical judge

1. **`plans/round31_defects.py` changed mid-round.** At this seat's first run (05:2x) it printed
   `checks=10 defects=3` including `DEFECT R6 … the entry states 2 unregistered staged sources, the
   registry gives 3`; at 05:56 the file carried `document_key()` (`:180`) and the run printed
   `checks=10 defects=1`. Both outputs are quoted above. The R6 verdict reversed without the entry
   changing — the comparator was repaired, not the prose. The frozen control
   (`.ufo/waves/round-31/claims/defects-before.txt`, `defects=10`) predates both.
2. **Round 30's `## Gate` number does not reproduce.** It records "167 prose `recheck` cells" for the
   staged package; measured under the gate's own `CADENCE_RE` (`^\d+d$`) this seat counts **174 of 175**
   rows with a prose `recheck` cell (51 in the `date — action` form, 123 in the `cadence — command` form,
   and 2 rows whose cells are broken by pipes). The classifiers differ; the round-30 figure is not
   re-derivable from the package as it stands, and this Gate states the count it measured.
3. **`staged=173` vs the package's 175 rows.** `MERGE-REPORT.md` says 175 rows accepted; the gate parses
   173 because S093 (12 cells) and S101 (15 cells) do not split into 11. Both numbers are true of
   different questions ("how many row lines" / "how many parse"), and the Gate says which it means.
4. **The landed S100 row contradicts nothing, but its citation redirects.** `laude-institute/terminal-bench-2`
   answers 301 to `harbor-framework/terminal-bench-2` (repo id 1063848495) while serving identical bytes at
   the pinned commit under both names. Under `normalize_url` those are different documents, so the URL
   binding refuses a canonical-name capture against an alias citation (exit 8, measured). The row records
   the redirect; the C3 limit is named in the Gate rather than repaired by widening the normalisation.

## Out of scope (named, not absorbed)

- The entry's own text is not this seat's to edit; the S092 quote repair and the S100 no-quote gap are
  recorded as OPEN items with the exact fix, not applied.
- The 64 rejected entries and 172 rejected rows: no row is appended, no entry is copied.
- `corpus/lessons/round-30.md` errata (R2/R3/R10), `LOG.md` (R1) and the five round-30 seat reports (R9)
  are peers' work in the same worktree; this seat read them read-only.
- No commit, push, deploy, judge or fleet-campaign command was run; no `agent://all`; no model passed.

## Artifacts

- This report: `.ufo/waves/round-31/build/R31DraftGate.md` (lane-relative).
- Scratch (60 MB bound respected — 2.4 MB total): `/tmp/r31-R31DraftGate/` —
  `harbor-config.py`, `harbor-verifier.py`, `tree/harbor/src/harbor/models/task/verifier_mode.py`,
  `tree/swb/v2/tasks/…/tests/test.sh`, `swb-readme.md`, `tb2-readme.md`, `tb2-task.toml`, `swb-task.toml`,
  `tb2-contents.json`, `swb-tasks.json`, `tb2-repo.json`, `tb2-tags.json`, `hf-tags.json`,
  `rows-staged.txt`, `rows-repaired.txt`, `S092|S093|S100.landed.rows`, `*.map.json`,
  `append-attempt.log`, `append-after.log`, and `fleet/` (the scratch census root with its `shokunin.conf`).
- Lane artifacts read: `.ufo/waves/round-31/{adoption-expect.json,build-spec.json,assimilation/*,claims/*}`,
  `plans/{adoption_check.py,round31_defects.py,sources_adopt.py}`, `corpus/{SOURCES.md,QUALITY.md,README.md}`,
  `corpus/lessons/round-30{,-verifier-spotcheck}.md`, `corpus/knowledge/benchmark-verifier-execution-model.md`.
- Read-only external: `/home/vgpnk/Projects/shokuknow/merge/kengaku/{MERGE-REPORT.md,SOURCES.append.md,
  knowledge/corpus/knowledge/*}` and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

VERDICT: DRAFTED — the `## Gate` and `## Mistakes` blocks above are complete and every number in them was
measured by this seat; four items are marked OPEN rather than passed (Q7 landing commit, Q10 second seat,
Q13 report timing, Q19 yield rows) and C2 is recorded as partial (`checks=10 defects=1`, R9 open).
