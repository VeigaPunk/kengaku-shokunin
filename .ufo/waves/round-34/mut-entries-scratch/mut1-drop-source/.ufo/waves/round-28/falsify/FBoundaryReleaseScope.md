# FBoundaryReleaseScope — release-boundary falsification of the round-28 C1 candidate

Seat: `KengakuR28.FBoundaryReleaseScope` (critic, leaf, author-side; not outside closure, not a judgment, no production edits).
Target: final draft `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, read at SHA256
`77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`, which equals `candidate-freeze.json`.
Canonical candidate path `corpus/knowledge/webarena-task-spec-audit.md` is absent, so the candidate is not admitted.
Also read: `plans/round-28-claims.md` (prereg plus Amendment 1), `corpus/lessons/round-28.md`,
`plans/fixtures/r28/webarena/manifest.json`, `build/CritClaimScope.md`.
Axes: calibration (primary), and legacy novelty, now canonical coverage/constructs 7, as a held score only.
Scope: the boundary between the 2025-11-26 revised snapshot, the paper-era release, other named releases and WebArena-Verified,
plus the candidate's statements that it makes no new-method, leaderboard or contamination claim.

## Verdict up front

The disclaimers hold, but the release identity and one negative certainty fail.

- **The disclaimers hold.** The candidate makes no new-method, model-capability, contamination or WebArena-Verified claim.
- **The pin's identity and date are correct.** The 2025-11-26 commit date is right, and the pin equals upstream `main` today.
- **The release-to-pin numbers reproduce.** I reproduced CritClaimScope's comparison exactly.
- **The release identity is incomplete.** The candidate says the pin is "not its 2023-07-25 paper-era release", as if there were one prior release. It never names two populations:
  - the formal GitHub release `v0.2.0`, which is only 36 tasks away from the pin;
  - arXiv paper version v4 (ICLR 2024), which postdates the pin's last task-file change.
- **"Cannot be attached" is unsupported certainty.** The candidate says leaderboard numbers "cannot be attached to these bytes". The evidence only supports "not established".

All failures are fixable wording or identity defects. None needs repricing or is a tradeoff the Rust judge must reject.

## Counterexample 1 — the candidate names one prior release; upstream has several distinct populations

Candidate lines 14–16: "not its 2023-07-25 paper-era release and not WebArena-Verified".
The lesson gate row says "this snapshot represents the 2023 paper release … reject".

What I observed on 2026-10-21, using the GitHub API, raw files and arXiv (fetched as data, never executed):

| population | identity | test.raw.json sha256 | evaluators.py / helper sha256 (prefix) | judge model in helper |
|---|---|---|---|---|
| release commit | `b454f2dc`, 2023-07-25 "release commit" | `4ea85923…` | `acff3581` / `b3c155e8` | `gpt-3.5-turbo` (L170) |
| GitHub release `v0.1.0` | tag `a17bc336`, published 2023-08-23 | `4ea85923…` (byte-equal to release) | `acff3581` / `b3c155e8` (byte-equal) | `gpt-3.5-turbo` |
| GitHub release `v0.2.0` | tag `e32b71e3`, published 2023-10-21 | `71f0877b…` | `fed6502a` / `9392bf8e` | `gpt-4` (L162) |
| pin | `dce04686`, 2025-11-26, equals `main` HEAD on 2026-10-21 (compare: identical) | `7b50386f…` | `e23edb39` / `ec758da4` | `gpt-4-1106-preview` (L162, L197) |

Independent task census by my own stdlib JSON parser (`scratch/FBoundaryReleaseScope/census.py`, `census.json`). It imports no production or oracle code.

- **Release to pin:** 531 eval blocks changed, 480 of them substantively. This equals CritClaimScope.
- **`v0.2.0` to pin:** only **36** tasks changed, all in `reference_answers`. Also changed: `eval_types` in 2 tasks (301/302 duplicate removed), `intent` in 2 and `string_note` in 2.
  - The string operators go from `exact_match` 81 to 45, and `fuzzy_match` 82 to 118, with 36 `fuzzy_match: "N/A"`.
  - The evaluator-type-set histogram is already identical to the pin's: 325, 282, 66, 10, 129.
  - Among the 16 sampled tasks, only **791** differs substantively from `v0.2.0`. Against the release, 12 of 16 differ.
- **All three populations** have 812 tasks, IDs 0–811, and 27 strata. The frozen rule selects the same 16 IDs in each, and no selected stratum includes `shopping`. So the candidate's sample statements survive.
- **The `v0.2.0` task file is not strict JSON.** Tasks 301/302 have `"string_match"` twice with no comma, at line 9418 column 9. Upstream fixed this on 2023-10-22 (`3065fda6`).
  - I parsed it only through an in-memory comma repair in scratch.
  - The shipped instrument would correctly refuse those bytes.
  - This supports the candidate's rule that each release must be separately frozen and audited, but the candidate never names this release.

The paper has four arXiv versions: v1 on 2023-07-25, v2 on 2023-10-24, v3 on 2023-10-25 and v4 on 2024-04-16. v4 says "Published as a conference paper at ICLR 2024".

Compared with the pin:
- **Task file:** v4 postdates the pin's last task-file change (`bb6e4c62`, 2024-03-14).
- **Judge:** v4 names `gpt-4-0613` as the judge. It mentions `gpt-4-1106-preview` only in its Table 6 date/time check.
- **GPT-4-evaluated examples:** v4 counts "82 examples that require using GPT-4". That equals `v0.2.0`'s 82 `fuzzy_match` tasks and the pin's 82 non-N/A fuzzy tasks, not the pin's 118 LLM-dependent tasks.
- **Fuzzy prompt:** v4's prompt line about `N/A` matches the pin's `llm_fuzzy_match` (S063:153).
- **Unachievable-task path:** v4 does not describe the pin's `llm_ua_match` path, added 2023-12-22.

So "paper-era" does not mean one population. The closest paper and release populations to the pin are v4 and `v0.2.0`, not the 2023-07-25 release.

The candidate's only cited evidence of difference is CritClaimScope's diff against the 2023-07-25 release (480 tasks). A reader holding `v0.2.0` or v4 sees no excluding statement. They could infer either "not covered at all" or "close enough", and both are wrong:
- `v0.2.0` differs in 36 tasks (one sampled case), its judge model and its unachievable-task path;
- 15 of the 16 sampled eval blocks are identical.

**Impacted axis:** calibration, through population identity and provenance. Coverage counts are unaffected.
**Defect class:** fixable wording defect. It is not a regression in counted results.

## Counterexample 2 — "leaderboard performance numbers cannot be attached to these bytes" is an unsupported negative

Candidate lines 16–17.

The behavior-relevant bytes in the pin are older than its commit date:
- **Task file:** last changed 2024-03-14 (`bb6e4c62`, "fix typo in intent"). The bytes at `bb6e4c62` hash to `7b50386f…`, equal to the pin.
- **Helper:** last changed 2023-12-22 (`3c4dcab8`). The bytes at `3c4dcab8` hash to `ec758da4…`, equal to the pin.
- **Scorer:** last changed 2025-09-02 (`60a6ca1a`, "Fix mypy type-checking errors"). My diff from `73d9de71` is exactly one line: `from nltk.tokenize import word_tokenize  # type: ignore` becomes the same import without the comment. No scoring behavior changed.

So the pin's scoring-relevant bytes are byte-equal to upstream `main` from 2024-03-14 onward, with the scorer behavior-equal.

The lane has no evidence about which revision any leaderboard entry used. Entries evaluated against `main` after 2024-03-14 may have used byte-identical task and scorer files. [INFERENCE: not observed; no leaderboard source was opened, by design.]

"Cannot be attached" therefore turns an unknown into a certain negative. The paper-era half of the sentence survives on the evidence: v4 differs in judge model and in the 82-versus-118 LLM-judged count. But it survives for that reason, not because of the 2023-07-25 diff cited.

**Impacted axis:** calibration.
**Severity:** moderate. The wording errs toward caution, so it cannot license a false attachment. But it states as fact something nobody measured.

## Counterexample 3 (minor) — the commit date is presented as the snapshot's date

"committed 2025-11-26" is true, but that commit only merges a README change (PR #183).

CritClaimScope recommended stating each file's last-change date. The final draft dropped those dates, so a reader could think the scorer reflects 2025 revisions.

Each file's effective date is given in Counterexample 2: task file 2024-03-14, helper 2023-12-22, scorer 2025-09-02 (comment-only).

**Impacted axis:** calibration (provenance). This is low severity.

## Claims tested that survive (bounded no-objection)

- **Pin identity matches.** `manifest.json` digests match the files at `bb6e4c62` / `3c4dcab8` and at the pin. The pin commit date is author and committer 2025-11-26T21:15:59Z.
- **Pinned counters match the candidate's table.** Evaluator-type sets are 325 / 282 / 66 / 10 / 129. String operators are `exact_match` 45, `must_include` 176, `fuzzy_match` 118. Strata are 27 and the selected IDs are identical. I derived these independently.
- **"Shopping site is omitted" from the sample is true** in all three populations.
- **CritClaimScope's release diff reproduces exactly.** The candidate does not import that count as a new result (line 18). It is honest that the result is "found", but CritClaimScope is a separate seat of this lane's own wave, so "independently" means a separate seat, not outside evidence.
- **No new-method, task-validity, model-capability, contamination or benchmark-run claim appears anywhere.** I checked candidate lines 10–13, 136–141 and 85–90, and the lesson gate rows. No leaderboard number is quoted.
- **WebArena-Verified:** the only claim is that it is a distinct population. I did not open WebArena-Verified. Calling it a "verified successor" (candidate line 129, Amendment 1) is a mild lineage claim I did not verify. It does not change any count.

## Smallest safe correction (wording only; L1 decides)

Replace candidate lines 14–19 with something equivalent to:

> The source is web-arena-x/webarena at dce04686 (committed 2025-11-26; behavior-relevant bytes last changed: test.raw.json 2024-03-14, helper_functions.py 2023-12-22, evaluators.py 2025-09-02 comment-only). It is not the 2023-07-25 release commit or tag v0.1.0 (byte-equal to it), not tag v0.2.0 (2023-10-21; 36 tasks differ, judge `gpt-4`, task file not strict JSON), not any arXiv version v1–v4, and not WebArena-Verified. No paper or leaderboard number is established for these bytes; attaching one requires that run's pinned revision.

Apply the same wording to the lesson gate row ("2023 paper release" should become "any tagged release or paper version"). Operational rule 6 can stay as written.

## Sources opened (accessed 2026-10-21; data only, never executed or imported; quotes ≤25 words)

| URL | location | quote |
|---|---|---|
| https://api.github.com/repos/web-arena-x/webarena/releases | release entries | `"tag_name":"v0.2.0" … "published_at":"2023-10-21T04:35:19Z"`; `"v0.1.0" … "2023-08-23T22:16:04Z"` |
| https://api.github.com/repos/web-arena-x/webarena/commits/dce04686a56253aefba7b18a4fa0937cf1dc987b | commit | "Merge pull request #183 from alzambranolu13/patch-2 … Update README.md", 2025-11-26T21:15:59Z |
| https://api.github.com/repos/web-arena-x/webarena/compare/dce04686a56253aefba7b18a4fa0937cf1dc987b...main | compare | `"status":"identical"` |
| https://raw.githubusercontent.com/web-arena-x/webarena/e32b71e3f5b2463bb102457591bc06c0f2c93acf/config_files/test.raw.json | L9417–9418 | `"string_match"` / `"string_match"` (no separating comma) |
| https://raw.githubusercontent.com/web-arena-x/webarena/e32b71e3f5b2463bb102457591bc06c0f2c93acf/evaluation_harness/helper_functions.py | L162 | `model="gpt-4",` |
| https://raw.githubusercontent.com/web-arena-x/webarena/73d9de71/evaluation_harness/evaluators.py | L13 | `from nltk.tokenize import word_tokenize  # type: ignore` |
| https://export.arxiv.org/abs/2307.13854 | submission history | "[v4] Tue, 16 Apr 2024 15:13:18 UTC" |
| https://export.arxiv.org/pdf/2307.13854v4 (sha256 f9731b92…) | §3.3 / A.8 | "in this work, we use gpt-4-0613 to perform this evaluation"; "among the 82 examples that require using GPT-4 for evaluation" |

I also re-fetched the release commit (`b454f2dc`), `v0.1.0`, `bb6e4c62` and `3c4dcab8` task and helper files from GitHub raw; their digests are in the table above. Path-history listings are in `scratch/FBoundaryReleaseScope/*.history.tsv`. arXiv v1 was opened only to confirm the judge `gpt-3.5-turbo-0613` (§3.3).

## Commands and limits

- **Commands run:** `curl` and `gh api` against GitHub and arXiv only; `sha256sum`; `diff`; `pdftotext`; my own `python3 -B census.py`, which parses JSON only.
- **Not done:** I ran no upstream code, contacted no benchmark sites and took no browser actions. I ran no builds, tests or production instruments, and opened no REA MCP.
- **Tool installs or updates:** none.
- **Not adjudicated:** I did not judge whether individual diffs are semantic, or how good `v0.2.0` is compared with the pin. The "substantive" field split mirrors CritClaimScope's.
- **Not opened:** leaderboard provenance, so the leaderboard point in Counterexample 2 stays an inference about possibility, not an observed attachment.
- **Scratch evidence:** `.ufo/waves/round-28/scratch/FBoundaryReleaseScope/` (fetched files, `census.py`, `census.json`, `mypy-fix.diff`, arXiv PDFs and text).

VERDICT: PARTIAL — the boundary disclaimers and the pinned numbers survive. The release identity misses `v0.2.0` and paper versions v2–v4, and "cannot be attached" for leaderboard numbers is unsupported certainty. Both are fixable wording; no score change.

---

## Addendum — candidate v2 re-read (2026-10-21, same seat; v1 findings above preserved unchanged)

Read candidate SHA256 `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182`, which matches the digest KengakuR28 announced.

Scope of the re-read:
- I read candidate lines 8–27 in full, including the corrected release paragraph at lines 15–19.
- I grepped the whole of v2 for leftover wording: `cannot be attached`, `paper-era`, `leaderboard`, `contaminat`, `novelty`, `release`, `commit`, `Verified` and `successor`.
- I did not fetch anything again, did not re-read the rest of v2 for other issues, and made no production edits.

How each v1 counterexample is handled in v2:
1. **Release identity (counterexample 1): fixed.** v2 says the entry "does not audit a tagged release, paper version or leaderboard run, including the 2023-07-25 release and WebArena-Verified". That covers `v0.1.0`, `v0.2.0` and arXiv v1–v4 as a class. It no longer suggests there was only one earlier release. v2 also says "No historical-release comparison count is imported", so there is no longer a 480-task distance standing in for the nearest population. Naming each tag is optional; a class-level exclusion is enough for this scope.
2. **Leaderboard and paper numbers (counterexample 2): fixed.** v2 says "Performance-number comparability is **not established**; it requires that run's pinned revision and configuration, even if some files overlap." This replaces the unsupported "cannot be attached" and allows for overlap without claiming a match. The phrase "cannot be attached" no longer appears anywhere in v2.
3. **Commit date (counterexample 3): fixed.** v2 says "The date names the repository commit, not each file's last change." Leaving out the dates themselves is acceptable now that the date is no longer presented as the date of the scoring bytes.
4. **Disclaimers: still hold.** Line 13 still disclaims a new method, a task-validity seal, a capability result, a contamination audit and a benchmark run. Lines 21–24 add a bounded prior-art check (S005/S006) that declines any method or novelty increase. Lines 157–158 keep the scores at novelty 7 and calibration 8.

Residuals (none of them in the corrected paragraph):
- **Lesson gate row.** `corpus/lessons/round-28.md` line 30 still says "this snapshot represents the 2023 paper release". Here it only labels a rejected reading, so it does no harm. But it is narrower than v2's class-level wording, so it should be aligned at admission.
- **Stale freeze record.** `.ufo/waves/round-28/candidate-freeze.json` still pins the v1 digest `77e19d5b…`. Under Amendment 1 §6, v2 needs a new freeze and full same-identity re-reads. This addendum is **not** a complete re-read of v2.
- **"Verified successors".** Candidate line 146 still uses this phrase. It remains a mild lineage claim I have not verified, and it changes no count.

Bounded final verdict for v2, covering only the release-boundary scope (lines 15–19 plus the grep above): **PASS**. All three v1 counterexamples are fixed in the final wording, and no new release-scope overclaim appears in the text I re-read. This does not approve the rest of the v2 text, C2, task validity or admission. The verdict v1 PARTIAL above still applies to digest `77e19d5b…`.

VERDICT: PASS (v2 3eb2afe5…ff182, release-boundary scope only; v1 77e19d5b… remains PARTIAL)
