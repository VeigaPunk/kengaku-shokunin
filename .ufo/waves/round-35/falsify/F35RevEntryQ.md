# F35RevEntryQ — Q1–Q7 review of `corpus/knowledge/tb2-protein-assembly-grader.md`

Seat: F35RevEntryQ (reviewer, wave-2 falsify, kengaku round 35, 2026-10-25).
Target: the C1 knowledge entry at lane tip `dfee6fff631ebc5f623ba4506e5c7992a215401c`, against `corpus/QUALITY.md` Q1–Q7.
Method: read-only in the lane (reads, `git rev-parse/log/ls-tree/merge-base --is-ancestor`, `sha256sum -c`, one probe re-run whose only writes are uv's ephemeral env under /tmp), plus live re-fetches of the three pinned URLs. No lane file was edited; no fixture was created.

## Verdict per criterion

| Criterion | Verdict | Core evidence |
|---|---|---|
| Q1 triad | PASS | Entry lines 1–5 = 3×`source:` (id, URL, exact anchor, commit, accessed date), `verified-at: 2026-10-25`, `recheck: 180d —` with concrete action; same shape as the two entries it extends |
| Q2 tier floor | PASS (one hygiene finding, F1) | S105/S106/S107 all tier A, scope-matched, `used-by` = this entry, sha256 cells match `SHA256SUMS`; receipt is unregistered (F1) |
| Q3 claim ⊆ quote | PASS (0 overclaims) | 22/22 located quotes byte-exact at cited lines, all ≤25 words; receipt line citations verified; static-table line ranges verified |
| Q4 negative space | PASS | `## Negative space` + runnable falsifier; both falsifier clauses executed live and held; unprobed legs named, `linker-g-only` pass not laundered |
| Q5 labels | PASS | Maintainers' task files = primary for what the grader checks / self-report for the PDB-match comments; receipt = lane's own re-runnable gate output, tier A for its own scope |
| Q6 extends | PASS | Both extended entries exist; S100 same-repo/same-commit is registry-evidenced (S100 anchor: citation URL 301-redirects to harbor-framework, tree sha equal); README §Frontier clause at `README.md:281`, discharge recorded at `README.md:282` |
| Q7 same-commit landing | PASS | Entry, `README.md` index row (:68), coverage bullet (:257) and Frontier discharge (:282) all first land in `4fe72a9`; probe at freeze `11d6453`; wave-1 report committed at tip |

## Q1 — triad

Entry lines 1–5: `source: S105 — <raw URL> — `test_gblock`, lines 10–73, commit 2fd12b88…, accessed 2026-10-25`; `source: S106 — … test.sh — reward mapping, lines 18–30 …`; `source: S107 — … instruction.md — requirement bullets, lines 9–34 …`; `verified-at: 2026-10-25`; `recheck: 180d — re-fetch the three pinned URLs, `sha256sum -c corpus/evidence/round35/tb2-eval/SHA256SUMS`, and re-run `plans/tb2_grader_probe.py`; any digest or receipt change supersedes this entry`. ISO dates present; recheck carries cadence + action + supersede rule. Anchor accuracy verified against the captures: `def test_gblock():` is at `test_outputs.py:10`, file is 73 lines (`read :10-46` → "Showing lines 9-49 of 73"); `test.sh:18-30` is the `uvx … fi` reward block; `instruction.md:9` is "The precise requirements are as follows:", bullets run 10–34.

Precedent: the two entries this one extends open identically (source ×3 → verified-at → recheck): `benchmark-verifier-execution-model.md:1-6`, `benchmark-grader-semantics.md:1-6`. This entry omits the optional `writer:` line those carry; Q1 does not require it (trivia, not a defect).

The recheck action is completable today: `sha256sum -c SHA256SUMS` (run inside `corpus/evidence/round35/tb2-eval/`) → all six files `OK`; live re-fetch of the three pinned URLs → digests `44a05a24…`, `9ede4664…`, `1bb2af1d…`, byte-identical (see F3 for a transient 404 on first attempt).

## Q2 — tier floor

`grep '^\| S10[0-7] \|' corpus/SOURCES.md` → S105 (code, **A**, scope "the executed scoring predicate of one TB2 task … for the code's own behaviour; the comments' claims about which PDB entries match are the authors' self-report", sha256 `44a05a24…`, used-by `corpus/knowledge/tb2-protein-assembly-grader.md`), S106 (code, **A**, sha256 `9ede4664…`, same used-by), S107 (docs, **A**, sha256 `1bb2af1d…`, same used-by). All three sha256 cells equal the `SHA256SUMS` lines, verified live and locally. Every claim about grader behaviour, reward mapping and instruction requirements rests on these rows squarely inside their scope.

**F1 (minor, registry hygiene — the one finding).** The executed-observation sentences (the 18-case table's observed column, `cases=18 observed_pass=5 observed_fail=13 mismatches=0`, the receipt's `components_aa`/`max_passing_nt` lines) rest on `corpus/evidence/round35/tb2-grader-probe.txt`, which has **no SOURCES.md row**: `grep 'tb2_grader_probe|tb2-grader-probe|round35' corpus/SOURCES.md` → no matches. The entry labels it inline ("The probe receipt is the lane's own re-runnable gate output (tier A for its own scope: these 18 inputs under Biopython 1.85)"), which matches the tier-A definition's own class ("the lane's own re-runnable gate output"), and every executed row is a prediction derivable from S105's pinned bytes that the receipt merely re-demonstrates — so no claim is left unsupported. But the lane's precedent for exactly this class is to register it (S024, S025, S036, S037, S047, S056 are all own-work gate-output rows). Fix: add an own-work row at the next SOURCES touch. Not counted as a Q2 failure because no load-bearing claim rests on a weak or out-of-scope source.

## Q3 — every load-bearing sentence, and its support

Mechanical audit (eval kernel): `quotes_checked=22 failures=0` — each of the 22 quotes in the entry's "Located quotes" table is a byte-exact substring of the cited line (`test_outputs.py:13,16,19,21,23,25,27,28,38,42,46,54,57,60,71`; `test.sh:21,27,29`; `instruction.md:11,29,30,33`), word counts 3–19 (all ≤25), and all 22 appear verbatim in the entry.

Sentence → support map (quote / receipt line / committed artifact):

| Entry sentence (location) | Support |
|---|---|
| "whole score is one pytest function, `test_gblock`" (intro) | Captured file has exactly one top-level def (`test_outputs.py:10`, 73 lines); `test.sh:23` runs pytest on `/tests/test_outputs.py` alone; S105 anchor `test_gblock` 10–73, S106 anchor 18–30 |
| "mapped by `tests/test.sh` to a binary reward (1 if pytest exits 0, else 0)" | Quotes `test.sh:27`, `test.sh:29` (table) + `:26-30` if/else verified by ranged read |
| "never opens the task's reference inputs" | Absence across the pinned function (only `open(gblock_path)` at :15; verified by full read) + quote `:25` (authors' rationale) |
| "five expected subproteins are amino-acid literals" | `:28`–`:36` literals in pinned bytes; quote `flag_aa = "DYKDDDDK"` at `:28` |
| "every … requirement that names a source … enforced only through those literals" | Static read (find-on-literal is the only mechanism, `:37-41`) + probe `donor-one-substitution` observed fail (receipt) |
| "matched every prediction … before the first run: cases=18 …" | Receipt last line, byte-equal to entry quote; freeze ordering (below) |
| "extends benchmark-verifier-execution-model.md … S100 same repository same commit" | S100 row anchor: citation URL 301-redirects to harbor-framework/terminal-bench-2, root tree sha equals pinned commit's tree; my re-fetch fetched identical bytes from **both** orgs |
| "extends benchmark-grader-semantics.md (one Toolathlon grader read)" | Entry exists (`README.md:67` row: S103 Toolathlon ab-testing grader) |
| "discharges … §Frontier round-33 clause … for this one task only" | Clause text at `corpus/README.md:281` ("the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; …)"); discharge recorded `README.md:282` "for that one task only" — scopes match |
| S105–S107 "primary for what this grader checks … self-report for everything else" | Q5 label; matches S105 scope cell verbatim in substance |
| receipt "tier A for its own scope: these 18 inputs under Biopython 1.85" | SOURCES tier-A class "the lane's own re-runnable gate output"; receipt line 1 `biopython=1.85`; quote `test.sh:21` |
| Static table rows (File shape 13–21; Alphabet/length 22–23; Translation 27; Expected parts 28–41; Order 42–44; Boundaries 46,60; Linkers 47–59; GC 65–73; Reward test.sh 26–30) | Every range verified by ranged reads of the capture; all content matches |
| Executed table, 15 rows (observed + first failing assertion "copied from the receipt") | Each row checked against its receipt line: e.g. `trailing-empty-line` → `'Invalid number of lines in gblock.txt.'`; `donor-one-substitution` → order message (the misattribution finding); `donor-repeated` → `'gBlock must be at most 3000 nucleotides.'`, `nt=3378`; `valid-balanced` `nt=2586`; 5 pass / 13 fail counted from the receipt's 18 `case=` lines. Instruction-requirement column entries are narrowed paraphrases of S107 bullets (e.g. "a DNA sequence" narrows "50 nucleotide window encoding the fusion protein") |
| Finding 1 (G-only linker passes; "scores 1") | Probe `linker-g-only` observed pass; quote `:54` `[GS]+`; reward mapping S106 |
| Finding 2 (cap never decides an otherwise-passing gBlock; 3 × (842+80) = 2766) | Independent recomputation: literal lengths `[8,259,158,235,182]`, sum 842, `3*(842+80)=2766 < 3000` (matches probe formula `3 * (sum(lens) + 4*20)` and receipt `max_passing_nt=2766`); only gaps are 4 linkers ≤20 aa, so 2766 is the true max; `donor-repeated` receipt line shows the cap changing which assertion fires first |
| Finding 3 (failure messages misattribute) | `donor-one-substitution` receipt line: one-residue donor error fails with the order assertion; quotes `:38` (find) + `:42` (order assert) |
| "Requirements the 18 cases do not exercise (wave-1 review R35RevProbePred)" | Probe case list has no FLAG-variant/repeat, no DHFR-substitution case, PDB identity probed for donor only (`mutant_donor` is the only substitution case); the cited wave-1 report is committed at tip (`git ls-tree HEAD -- .ufo/waves/round-35/build/R35RevProbePred.md` → blob `8314bf05`) |
| "predictions were committed in the freeze (11d64530) before the receipt first landed" | `git ls-tree 11d64530` contains `plans/tb2_grader_probe.py` (blob `50c5ee87`), does **not** contain the receipt; receipt first added in `4fe72a9` (2026-10-25 16:55:41 -0300) after freeze (16:29:25 -0300); freeze is ancestor of tip |
| Negative space list | Each item is a denial consistent with the pinned bytes and S105–S107 scope cells; "other 88 TB2 tasks" matches registry count (89 task dirs, S079/S100) |
| Falsifier | Both clauses executed today and held (below) |

Attack vectors named in the assignment all fenced: **Harbor** — entry claims nothing about Harbor's runtime ("Harbor's runtime execution of this test" is in Negative space; S106's scope cell itself excludes "Harbor's consumption or aggregation"); **the 88 other tasks** — Negative space: "nothing about the other 88 TB2 tasks"; **PDB literals** — Q5 label: the comments' PDB-match claims "are the authors' statements, not verified here", repeated in Negative space. Findings 1–3 are each bounded "to this grader at this commit".

Overclaims found: **0**.

## Q4 — negative space and falsifier

`## Negative space` denies literal correctness vs `pdb_ids.txt`/APIs/`antibody.fasta`, biological correctness, Harbor runtime, model performance/trajectories, PROVINCE task validity, and the other 88 tasks. The falsifier is concrete and runnable. Both clauses exercised now:

- Clause 1 (re-fetch digests): `curl -fsSL <pinned URL> | sha256sum` → `test_outputs.py` `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582`, `test.sh` `9ede46648fc67c9ce61975503de3e0fcff0b0fb110adc0f9e1d240a608c267b5`, `instruction.md` `1bb2af1d85e9a823a8ae7273a87df8a3f67e2c93b06cddf34f0051a8b003f7c5` — identical from both `harbor-framework` and `laude-institute` orgs and via the GitHub contents API. No digest differs; falsifier does not fire.
- Clause 2 (fresh probe run): `uv run --no-project --with biopython==1.85 python plans/tb2_grader_probe.py --lane <lane>` (run from /tmp; writes nothing to the lane) → exit 0 through the pipe; stdout sha256 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` = sha256 of the committed receipt file (eval-computed `byte_equal=True`). The receipt reproduces byte-for-byte at tip; `linker-g-only` still observed `pass`.

Indeterminate not laundered: `linker-g-only` pass carries "whether that is a 'GS linker' is not decided by the grader"; unprobed legs (antibody-binder FLAG variants, DHFR substitution, FPbase spectra) are named as unprobed, credited to wave-1 `R35RevProbePred`.

## Q5 — labels

"S105–S107 are the benchmark maintainers' own task files: primary for *what this grader checks*, and a self-report for everything else" — correct split, and matches the rows' own scope cells. Receipt labelled as the lane's own re-runnable gate output (tier A class), bounded to "these 18 inputs under Biopython 1.85". No source is passed off as independent replication.

## Q6 — extends, never overwrites

Names `knowledge/benchmark-verifier-execution-model.md` and `knowledge/benchmark-grader-semantics.md`; both exist and match the glosses (Harbor verifier execution; Toolathlon ab-testing grader). "S100 is the same repository at the same commit" — S100's own anchor records the laude-institute→harbor-framework 301 redirect with equal root tree sha at the same 40-hex commit; verified live. The discharged README §Frontier round-33 clause exists (`README.md:281`), and `README.md:282` appends the round-35 partial discharge scoped "for that one task only" — the entry's "discharges, for this one task only" neither overwrites the clause nor widens the discharge.

## Q7 — landed and discoverable in the same commit

`git log --oneline -n 2 --` per path at tip `dfee6fff631ebc5f623ba4506e5c7992a215401c`: entry, `corpus/README.md` (index row :68, coverage bullet :257, Frontier discharge :282), `corpus/SOURCES.md` (rows S105–S107) and the receipt all first land in **`4fe72a9`** ("round-35: C1 admit TB2 protein-assembly grader entry, S105-S107, probe receipt; …"). Probe landed earlier at freeze `11d6453` (predictions before receipt, as the entry states). Wave-1 report committed at tip. No support rests on /tmp, `local://`, or an unlanded working copy.

## Findings (severity-ordered)

- **F1 (minor, Q2 hygiene):** probe receipt is load-bearing but unregistered in SOURCES.md (grep evidence above), deviating from own-work-row precedent S024/S025/S036/S037/S047/S056. No claim is unsupported (tier-A-class gate output, self-labelled, falsifier-re-runnable); register an own-work row at the next SOURCES touch.
- **F2 (info, evidence wording):** "written before the run" rests on commit ordering (predictions at freeze 16:29:25, receipt first add 16:55:41) plus the frozen claims' process assertion ("Frozen before any grader run"); git alone cannot exclude a pre-freeze execution. The entry already states exactly this ("that ordering, not a byte inside the receipt, is the evidence") — residual, not an overclaim.
- **F3 (info, operability):** first live re-fetch attempt returned transient raw.githubusercontent 404s for both `tests/` files (`instruction.md` byte-matched on the same attempt); immediate retry, the alternate org, and the contents API all returned digest-identical bytes. The Q1 recheck action is completable, but a future recheck runner should expect a possible first-attempt 404 and retry before declaring a digest change.
- Trivia (non-defect): entry omits the optional `writer:` line its sibling entries carry; the entry's "3 × (842 + 80)" is the probe's own formula (`3 * (sum(lens) + 4 * 20)`), not an arithmetic slip.

## Residual risk and verification gaps

- Bare `python3 plans/tb2_grader_probe.py` in the lane shell exits 1 with `ModuleNotFoundError: No module named 'Bio'` — the probe (by design, "fail loudly") needs an environment with Biopython; I reproduced it via `uv run --with biopython==1.85`. Any counter that re-runs the probe must do so in such an environment.
- The probe executes the captured grader *function* with `mod.Path` monkey-patched to a temp file (the `/app/gblock.txt` path is never exercised); the entry discloses this ("not a run of Terminal-Bench, of the task image").
- I did not audit `task.toml`/harbor runtime surfaces (S079/S092) — out of this entry's claims; the entry likewise excludes them.
- Verification gaps: none remaining for Q1–Q7; every load-bearing sentence has named, re-derived support.

VERDICT: entry-q-7/7-0-overclaims
