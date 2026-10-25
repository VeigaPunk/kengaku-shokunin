# R33MistakeMine — mistake candidates for `corpus/lessons/round-33.md` §Mistakes

Seat: `R33MistakeMine` (scribe, leaf). Round: kengaku 33 (hyaku run 7). Date: 2026-10-25.
Access date for every source opened this round: 2026-10-25.

Scope: collect and classify mistake candidates for the round-33 lesson's `## Mistakes` table.
Nothing was written outside this file. No product edit, no git write, no fleet write, nothing in
`/home/vgpnk/Projects/shokuknow` beyond reads, no pacman, no tool installed.

Read at lane HEAD `2b4cef2` (`round-33: renumbered assimilation (S103/S104), routed-defect closure
N1-N6, catalog re-probe receipts`). `git status --porcelain -- corpus plans SCORECARD.md` was empty
at the time of every counter run below, so the runs read committed tip bytes; other seats moved
`.ufo/waves/round-33/build/` under me, and each quote below is anchored to a named commit or to a
file whose bytes I print.

## 1. Class vocabulary and how classes were assigned

`CORPUS.md:173-176` fixes nine classes for a lesson `## Mistakes` row — `vacuous`, `survivor`,
`stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider` —
and `CORPUS.md:171-173` fixes the four columns: class · evidence pointer · captured-by (the
criterion or protocol rule that should have caught it, or `none`) · fix. `.ufo/waves/kaika-w1/mistakes.md:447-448`
is the vocabulary's source; its §3 exemplars (C01 `reference-drift`, C02 `number-drift`, C04
`vacuous`, C06 `stale-premise`) are the precedents used for each call. Where a candidate fits two
terms, the chosen term is stated with the rejected alternative and the reason.

`record` is **not** a term in that vocabulary. The round-33 claims file calls item (d) "record
class" (`plans/round-33-claims.md` §C2, N2); the nearest vocabulary term is `landing` — an artifact
asserted by the round but absent from the round's tree — and that is the class used, with the
mismatch named in the row.

## 2. Mistake table (paste-ready)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `landing` | `.ufo/waves/round-32/` — 84 of its 89 files were untracked at the pushed tip `112091c`: `git ls-tree -r --name-only 112091c -- .ufo/waves/round-32 \| wc -l` → `5`; at `c227e486` → `89`; the 84 = build 35 + falsify 35 + assimilation 7 + 7 loose files | R2 (`corpus/QUALITY.md:162`: "no round-owned path is left untracked", check = every `git status --porcelain` entry committed or named). The non-author spot-check ran that check and recorded `untracked=10` (`corpus/lessons/round-32-verifier-spotcheck.md:26`) yet the round closed | committed at `c227e486`; `plans/round33_defects.py` N1 now re-checks every file at each tip |
| `number-drift` | the same defect carries three different counts. `corpus/lessons/round-33.md:32` (committed `2b4cef2`) says "89 files sat untracked"; the artifact is **84 untracked of 89 total**. `corpus/lessons/round-32-verifier-spotcheck.md:26` and `plans/round-33-claims.md:78` say "10 paths"; 10 is the `git status --porcelain` entry count (3 directories + 7 loose files) | `none` — R2's check is entry-based by design, so both numbers pass it, and nothing joins the file count to the entry count | state the unit once: "84 untracked files in 10 porcelain entries"; `plans/round33_defects.py` N1 counts files, so the lesson should quote N1's number |
| `landing` | `corpus/evidence/round32/catalogs/after.txt:10-11` — "Raw JSON is retained in R32CatProbe's bounded /tmp capture only; its sha256 + byte count are in that seat report." / "This output is the committed evidence receipt; it is not the raw response." (recorded as a row at `corpus/lessons/round-32.md:17`) | `none` — no criterion at round 32 required retained evidence bytes; Q20 (`corpus/QUALITY.md:198`) covers gate landings and C3 is not a gate. The round-32 row's captured-by cell names seats (`FxSentinel.md`, `FxEvidence.md`) where `CORPUS.md:171-173` asks for a criterion or `none` | round-33 C3: bounded raw bytes + `SHA256SUMS` in `corpus/evidence/round33/catalogs/`, re-derived offline by `--verify`; red-before is `raw=absent` exit 1 (`claims/control-verify.txt`) |
| `reference-drift` *(alt reading: `survivor`)* | `git show c227e486:corpus/knowledge/benchmark-grader-semantics.md:2-3` → `source: S094 — …` / `source: S097 — …`; those ids resolve to rejection records — `git show c227e486:corpus/SOURCES.md:114` "supersedes S094 — duplicate staged row refused after registry collision…", `:115` "rejected correction record for a staged S097 duplicate; not a new source and not an admitted citation" — while the entry is already indexed, so the index sends a reader to refused citations | Q2 (`corpus/QUALITY.md:24-28`): a rejected correction record is not a tier-A/B row "for that claim's scope". Q1's triad is satisfied formally, which is why the file passed as a draft | round-33 C1 re-points `source:` to S093/S103/S104; `plans/round33_c1_verify.py` V8 fails if the refusal rows are overwritten |
| `landing` *(the claims' "record class" is not a vocabulary term)* | `git show c227e486:SCORECARD.md \| grep -c '^## Round 32'` → `0`, exit 1 (also `0` at `f0b20ae`). The section lands only at `7895588`: `SCORECARD.md:1094`, where it says "This section lands late under round 33 — its absence at the round-32 tip is routed defect N2." | R2 + R3 (`corpus/QUALITY.md:162-163`), whose check is literally `grep -c '^## Round <N>' LOG.md SCORECARD.md` → `1 1`; LOG had the section, so the check would have printed `1 0` | section appended at `7895588` with per-claim before/after and the correction carry; N2 in `plans/round33_defects.py` guards it |
| `number-drift` | `plans/round-33-claims.md:58` — "the same counter on the pre-append tree prints `entries=0 …` and exits 1" — against the receipt it cites, `.ufo/waves/round-33/claims/control-nothing.txt:5-6`: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok` / `exit=1`. The sentence is round-32's verbatim (`.ufo/waves/round-32/claims/control-nothing.txt:5` → `entries=0 …`), where the draft entry did not yet exist; at `f0b20ae` it does | `none` — no criterion compares a claims file against its own committed control; Q22 constrains receipts at the tip, not prose against a receipt | append a dated one-line correction in the round-33 lesson/SCORECARD naming the receipt's real first key; do **not** rewrite the frozen claims (the predicate itself is unaffected — only its control's description is wrong) |
| `vacuous` | Q22 (`corpus/QUALITY.md:257`) requires "every receipt a claim cites must name the revision it was produced at". Its first round violates it twice. (i) None of the four cited controls names a revision: `claims/control-nothing.txt` carries a date and `expect_sha256` only, `claims/defects-before.txt`, `claims/control-verify.txt` and `claims/census-before.txt` carry none; `grep -rnE "rev=\|revision\|@ [0-9a-f]{7}" .ufo/waves/round-33/claims/` → no hits. (ii) `corpus/evidence/round33/catalogs/after.txt` still reads `entry=pending` at a tip whose entry carries the block (`corpus/knowledge/open-model-catalogs.md:66`); `--verify` never compares that cell, so it prints `verify=ok` over it | `none` — Q22 ships as prose; its "Executable check" sentence has no counter and nothing reads receipt headers or the `entry=` cell | put `rev=<sha>` in each control header and compare the `entry=` cell in `verify()`, or record Q22's first-round unmet state as debt inside the criterion (as its own Limits paragraph already does for `defects.jsonl`) |
| `stale-premise` | the round-32 refusal's stated basis is contradicted by the wave's own committed artifacts. (1) The frozen predicate said the ids were new: `plans/round-32-claims.md` C1 — "S094 and S097 are new rows". (2) The baseline registry `f20a1097` has 91 rows, max `S100`, gaps `{87,88,89,94,95,96,97,98,99}` — no `S094`/`S097`/`S101`/`S102` row; `git log --oneline -S"\| S094 \|" -- corpus/SOURCES.md` → `bcd2a6c` only. (3) The committed collision census `.ufo/waves/round-32/assimilation/collisions` lists 15 ids — `S077–S086, S090–S093, S100` — and none of the four. (4) The lane's own gate: `.ufo/waves/round-32/build/R32GateBlock.md` — `registry=91 staged=173 collisions=0 malformed=0 duplicates=0 defects=0 prose=2`, `wrote …/block.md rows=2`, `EXIT=0`; the same report's draft verdict was "**admit**". (5) `corpus/evidence/round32/adoption-after.txt` shows the adoption in place: `rows_mined=3 usedby_ok=1 census=fail` (only the census key red; its cause is captured nowhere). (6) Yet `corpus/lessons/round-32.md:7` ("its staged S094/S097 rows collide with existing registry ids"), `:25` ("four staged identifiers collide with the lane registry"), `SCORECARD.md:1104` ("staged S094/S097 collided with live ids") and `.ufo/reports/round-32/kengaku.md:12` ("S094/S097 are already present") all say they collided. (7) Round 33 recomputes the census from the post-refusal registry and prints 19 ids (`.ufo/waves/round-33/assimilation/collisions`) — exactly the 15 plus the four rows round 32 itself created | Q9 (`corpus/QUALITY.md:67`) — "The source cited against a rejected claim must address the same property the claim asserts … A correct verdict with a wrong reason is a gate failure" | append-only erratum to `corpus/lessons/round-32.md` §Gate/§Assimilation (and one line in round 33's): S094/S097 were unused at `f20a1097`; 15 ids is the collision set actually found; the `census=fail` was the only red key and its cause was never committed; the S103/S104 renumber stands because its predicate does not depend on this; the four refusal rows stay (rule 2) but their "use the existing S094 row" pointers are self-referential |
| `vacuous` | `corpus/lessons/round-32-verifier-spotcheck.md:33` — "19 total package intersections … Existing S094/S097/S101/S102 rows are already live identities." The spot-check read `bcd2a6c`, the commit that created those four rows; at `bcd2a6c^` = `6084cd3492c6aef10fd66afc36ffc00e79ace94a` the registry has 91 rows, max `S100`, and 15 staged ids intersect. 19 − 15 is exactly the refusal's own footprint, so the confirmation could not have failed on the tree it read | `none` — no criterion fixes which tree a *closure* verifier must read; Q15/Q16 (`corpus/QUALITY.md:123`, `:132`) pin the tree only for an admitting commit | a closure verifier's cited state must be pinned before the change under review (or both states shown); append the correction to round-32's lesson |

## 3. Evidence dossiers for the five assigned items

### (a) round-32 uncommitted wave evidence — `landing`

```
$ git ls-tree -r --name-only 112091c -- .ufo/waves/round-32 | wc -l
5
$ git ls-tree -r --name-only c227e486 -- .ufo/waves/round-32 | wc -l
89
$ git show --stat --oneline c227e48 | head -1
c227e48 round-33: inherit round-32 wave evidence (routed defect N1)
```

The five tracked at `112091c` were `.ufo/waves/round-32/claims/{adoption-expect.json,
catalogs-before.txt,control-nothing.txt,defects-before.txt}` and `gate-receipt.txt`; the 84 added by
`c227e486` group as `assimilation 7 · build 35 · falsify 35 · loose 7`, which is 3 directories + 7
files = the 10 porcelain entries the spot-check reported. The spot-check's own words
(`round-32-verifier-spotcheck.md:26`): "but `untracked=10` and porcelain lists 10 round-32 wave
paths … defect: residual uncommitted work despite pushed tip". The defect was known, recorded, and
landed a round late — that is `landing`, not `number-drift`, which is why the count drift is a
separate row.

### (b) the round-32 lesson's own `landing` row — summary receipt without raw bytes

`corpus/lessons/round-32.md:17`:

> `| landing | corpus/evidence/round32/catalogs/after.txt is a summary receipt, not retained raw API responses | FxSentinel.md, FxEvidence.md | Preserve raw response bytes and digests in the lane if the C3 observation is to be independently rechecked. |`

The receipt confirms it in its own last lines (`corpus/evidence/round32/catalogs/after.txt:10-11`):

> `# Raw JSON is retained in R32CatProbe's bounded /tmp capture only; its sha256 + byte count are in that seat report.`
> `# This output is the committed evidence receipt; it is not the raw response.`

So the row is an accurate record of a real `landing` defect: the numbers (`hf=50 or=467
hf_schema_delta=4`) cannot be re-derived from anything committed. Two secondary observations, both
recorded in the table's `none` row above: the captured-by cell names two seats where
`CORPUS.md:171-173` asks for a criterion or `none`, and no criterion existed to name. The fix is
round 33's C3, which I read and ran (see §4): committed bounded bytes plus digests plus an offline
`--verify`, with a red-before control.

### (c) committed draft entry citing refused ids — admission debt

At the freeze tip (`c227e486`) the entry cites three ids, two of them rejected:

```
$ git show c227e48:corpus/knowledge/benchmark-grader-semantics.md | sed -n '1,3p'
source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `v2/tasks/…/tests/test.sh` … commit `66f92766…`, accessed 2026-10-25
source: S094 — https://github.com/hkust-nlp/Toolathlon — `tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe…`, accessed 2026-10-25
source: S097 — https://arxiv.org/abs/2412.05579 — arXiv 2412.05579v2 (preprint), accessed 2026-10-25
```

Those two ids resolve to refusal records, not sources (`git show c227e48:corpus/SOURCES.md:114-115`;
full `:114` row ends `| rejected | 2026-10-25 | 180d | — |`). The entry was also indexed, so the
index sent a reader to refused citations. The committed freeze control records exactly that state
(`.ufo/waves/round-33/claims/control-nothing.txt:5-6`, corpus bytes unchanged from `f0b20ae` to
`c227e486`): `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok`,
`exit=1` — `rows_mined=1` is S093 only, and `SCORECARD.md:1131` quotes the same string as
round 33's "before". Class call: `reference-drift` (no number is stale; the pointer lands on
a row that says something else — C01's exemplar shape). Alternative reading `survivor`: the entry
survived a round closure and a non-author spot-check in this state.

The repair in flight is correct and grounded. The two staged misstatements the claims name are
verifiable in the captured bytes: the tolerance the code executes is the call site's, not the
signature default —

```
main.py:58   def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:
main.py:279          # Validate with 0.05% tolerance
main.py:280          validate_record_data(actual_records, expected_records, tolerance_pct=0.05)
(capture: .ufo/waves/round-32/assimilation/captures/toolathlon-ab-testing-evaluation-main.py)
```

— and the log check has a caught-exception `return True` path at `:217-218` (`return True  # Don't
fail evaluation if we can't check logs`), so "fail open" is right for that path and wrong as a
statement about credential absence. I did not re-fetch the source; I read the committed capture.

### (d) round-32 missing SCORECARD section — `landing`

```
$ git show c227e486:SCORECARD.md | grep -c '^## Round 32'
0            (exit 1)
$ git show f0b20ae:SCORECARD.md | grep -c '^## Round 32'
0            (exit 1)
```

The section now exists at `SCORECARD.md:1094` (commit `7895588`) and names itself: "This section
lands late under round 33 — its absence at the round-32 tip is routed defect N2." R2 and R3 already
carried the exact one-line check (`QUALITY.md:162-163`); the round closed with the check unrun, so
the defect is a missing landing plus an unrun detector, not a missing rule.

### (e) this wave's own run

Five candidates above (`number-drift` claims-vs-control; `vacuous` Q22; `stale-premise` collision
premise; `vacuous` circular spot-check; the 89/84/10 count drift), each with committed byte
pointers. The two highest-value ones for the canonical judge:

1. **The collision premise.** Two of this wave's frozen/committed artifacts inherit it:
   `plans/round-33-claims.md:27` ("staged ids S094/S097 collide with live registry identities") and
   `corpus/lessons/round-33.md:21` ("collisions S094/S097/S101/S102 (staged package)"). Both are
   *true at the round-33 tree* and both are true only because round 32's refusal created the rows;
   at the round-32 baseline the same sentence was false. The frozen C1 predicate does not mention
   collisions, so nothing about C1's execution needs to change; the lesson line and the claims'
   justification do.
2. **Q22 is prose.** `corpus/QUALITY.md:257` and its "Executable check" sentence have no
   implementation, and this round's own cited receipts fail both halves of it (no `rev=`; one stale
   `entry=pending` cell). Landing it as a criterion while its first round violates it is the
   `vacuous` pattern C04 names.

## 4. Counters I ran (readings, not my claims)

All from the lane root at HEAD `2b4cef2`, product tree clean:

```
$ python3 plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census
entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok        EXIT=0
$ python3 plans/round33_c1_verify.py --lane .
checks=8 defects=0                                                                        EXIT=0
$ python3 plans/round33_defects.py --lane .
checks=6 defects=0                                                                        EXIT=0
$ python3 plans/catalog_probe.py --verify --lane .
raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok            EXIT=0
  HF missing fields: author, sha, lastModified, gated
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku
kengaku W04 …  (15 lines) ; kengaku ok …/corpus/SOURCES.md                                 EXIT=0
```

`corpus/evidence/round33/catalogs/after.txt` (committed) reads
`probed=2026-10-25 hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 entry=pending`
plus a `raw_sha256 hf=… or=… cap=65536` line; the entry's block is at
`corpus/knowledge/open-model-catalogs.md:66`.

I did **not** run a mutation test on any of these counters. Their green is the counters' own printed
reading of the tip bytes, which is what Q22 says a receipt proves — no more.

## 5. Conflicts to state verbatim for the canonical judge

- **Class of item (c).** `corpus/lessons/round-33.md:33` (committed `2b4cef2`) classes the
  refused-id citation `number-drift`: "cited the *refused* ids S094/S097 — an entry file whose
  citations are rejected rows". I class it `reference-drift`. No count is stale in that defect; the
  `source:` line lands on a row that says something different, which is C01's shape
  (`.ufo/waves/kaika-w1/mistakes.md:109`). `number-drift`'s precedents (M25, M30) are arithmetic
  cells, not pointers.
- **Count of item (a).** `corpus/lessons/round-33.md:32` says "89 files sat untracked"; the artifact
  is 84 untracked of 89 total (5 tracked at `112091c`). Same row, `captured-by` cell: "Q19" — Q19 is
  seat yield (`corpus/QUALITY.md:186`), not untracked paths; R2 (`:162`) is the criterion whose
  check covers them.
- **The collision premise.** `corpus/lessons/round-33.md:11` ("Their round-32 refusal rows stand")
  and `:21` ("collisions S094/S097/S101/S102 (staged package)") are true of the round-33 tree and do
  not by themselves repeat round 32's error; the repetition is in
  `plans/round-33-claims.md:27`'s justification and in the round-32 wording M08 quotes. I am not
  asking for any predicate change, only an append-only erratum.
- **C2 scope.** `plans/round-33-claims.md` §C2's surface sentence says "ten uncommitted round-32
  wave paths"; `plans/round33_defects.py` N1's own failure text at `claims/defects-before.txt:3`
  says "84 untracked files". Both are right in their unit; neither names the unit.

## 6. Limits

- The cause of round 32's `census=fail` is not recorded anywhere I could find: no census stdout or
  stderr was committed. `[INFERENCE]` The visible candidate is a malformed appended row — the same
  wave's gate printed `malformed: S093:escaped-pipe S101:escaped-pipe`
  (`.ufo/waves/round-32/build/R32GateBlock.md` (c)) and a `\|` inside a row yields `NF!=13` → E01.
  This is not proven, and the report says so rather than asserting it.
- I did not re-fetch S103/S104; I read the committed round-33 captures and the round-32 capture for
  the four `main.py` lines quoted above.
- No scratch repo was made and no `git clone` was run (lane bound). A mutation test of N1–N6 was
  therefore not performed.
- `.ufo/waves/round-33/` changed under me during the read (three build reports modified/added by
  other seats). Every quote is anchored to a commit (`f20a1097`, `6084cd34`, `112091c`, `bcd2a6c`,
  `c227e486`, `7895588`, `2b4cef2`) or to a file whose bytes are printed.
- No tools installed or updated; nothing under `/home/vgpnk/Projects/shokuknow`,
  `/home/vgpnk/Projects/shokunin` (including `.ufo/reports`), `.ufo/state`, `watchdog.log`,
  `MANIFEST.json` or any lane Git index was written.

VERDICT: mistakes-mined
