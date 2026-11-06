# ScribeLesson — proof-read of `corpus/SOURCES.md` rows S303–S309 against the CORPUS contract

Seat ScribeLesson (leaf scribe). Read-only audit; nothing here is committed by me. The
contract read is `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a
shokunin learns" (Contract v1, kaika 2026-10-19, frozen). The rows read are the seven
added at commit `afe9c229…` (C, the measured tip T): `git diff --stat d9cd18a… afe9c229… --
corpus/SOURCES.md` → `1 file changed, 7 insertions(+)`, and the diff's added lines are
**only** the seven `| S30x |` rows — no existing row was touched.

**Result in one line: no column of S303–S309 violates the contract's Shape or Rules.**
One column is *stricter* than the contract requires in a way worth noting, and one
house-wide convention makes `used-by` point at a plan file rather than a knowledge entry
or lesson — both are listed below as observations, not violations. Every mechanical
check the contract states passes.

## The contract, column by column, against S303–S309

The contract's Shape section fixes the eleven columns:
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`,
and states the census command that proves the table's shape.

### `id` — "`S` + 3 or more digits, the next unused; never reused. No `|` inside any cell."

| check | result |
|---|---|
| S + 3+ digits | S303…S309 ✓ |
| next unused, never reused | the seven ids are consecutive and new; the previous maximum in the file was S302, and the round-94 wave's *draft* supersede row was also numbered **S303** (`.ufo/waves/round-94/w1/ScribeQuality/lesson-gate.md:101` — "appending one row `S303` whose `teaches` cell opens supersedes S299"). **That draft was never landed** — `grep -c "supersedes S299" corpus/SOURCES.md` = 0, and S299's word count was corrected in place instead (its anchor cell now reads "(10 words)", the count the round-94 lesson M1 fix records). So S303 was free and is used once. ✓ |
| no `|` inside any cell | every row splits into exactly 13 fields (11 columns + 2 empty edge cells) ✓ |

### `source` — "title — canonical URL or DOI (a repo path or command for `own-work`)."

All seven carry a title and a canonical `raw.githubusercontent.com` URL pinned to the
terminal-bench-2 commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (S306 to bottlepy
`0207a34f0c5716cd292dd4480253ad35d3da49f3`) ✓.

### `kind` — "`spec` · `docs` · `paper` · `code` · `tool` · `dataset` · `talk` · `book` · `community` · `own-work`."

S303 `code`, S304 `code`, S305 `code`, S306 `code`, S307 `docs`, S308 `code`, S309 `code`
— all in the enum ✓. (The census's enum check prints nothing.)

### `tier` — "scoped to `scope`, never global. **A**: primary or authoritative for that
scope (spec, official docs, source code, original paper, maintainer statement, the lane's
own re-runnable gate output). **B**: … **C**: lead only. `community` is never A."

All seven are tier **A**, and each is a pinned upstream source file at a fixed commit —
source code / official docs / a task statement — which is A's own definition ✓. The
tier-inflation check (`t=="A" && k=="community"`) prints nothing ✓.

### `scope` — "the claim or topic the tier applies to."

Each row names the specific topic it is admitted for (e.g. S303 "the six test functions
this round's thirteenth offline replay grades, as the captured bytes define them") ✓.

### `anchor` — "exact section / heading / page / line plus revision (version, commit, or
publication date). Never a bare homepage."

Each row's anchor names `file:line`, a located quote, and the revision:

| row | anchor cell |
|---|---|
| S303 | `tests/test_outputs.py:45 quote "cwe_ids = [str(cwe_id).lower() for cwe_id in cwe_ids]" (7 words)` + `byte-identical to the lane's round-52 capture` + sha256 |
| S304 | `solution/solve.sh:20 quote "{"file_path": "/app/bottle.py", "cwe_id": ["cwe-93"]}" (4 words)` + sha256 |
| S305 | `environment/Dockerfile:22 quote "RUN sed -i -e '1562,1563d' bottle.py" (6 words)` + sha256 |
| S306 | `upstream-bottle/bottle.py:1562 quote "if '\n' in key or '\r' in key or '\0' in key:" (12 words)` + sha256 |
| S307 | `instruction.md:18 quote "- The exact files and that exact CWE-ids must appear in the /app/report.jsonl file." (14 words)` + sha256 |
| S308 | `tests/test.sh:9 quote "pip install pytest==8.4.1 pytest-json-ctrf==0.3.5" (4 words)` + sha256 |
| S309 | `task.toml:29 quote "docker_image = "alexgshaw/fix-code-vulnerability:20251031"" (3 words)` + sha256 |

Every anchor's revision is a sha256 of a byte-exact capture **plus** the source URL's
pinned commit — so the revision requirement is met twice over ✓.

Every anchor was **re-verified by this seat** against the lane capture, independently of
the lane's own gate: sha256 → the captured file; the quoted line → the line actually
holding the quote; the declared word count → `len(quote.split())`. All seven match on all
three counts (`receipts/receipt-sources-s303-s309.txt`).

### `teaches` — "one grounded learner benefit. Rejected rows read `REJECTED: <reason>;
flip: <what would change the verdict>`."

The five mined rows each carry one grounded learner benefit, every one of them naming a
case id that exists in `plans/round95-cases.json` and matching the committed observation
for that case in `corpus/evidence/round95/vuln-probe.txt`:

| row | cited cases | observed in the receipt |
|---|---|---|
| S303 | C08, C10, C11, C15 | `P,P,F,P,P,P` / `P,E:JSONDecodeError,E:JSONDecodeError,P,P,P` / `P,P,P,P,P,P` / `P,P,P,P,P,P` — all as the row describes |
| S304 | C01 | `P,P,P,P,P,P` |
| S305 | (none — it names the two `sed` deletions, not a case) | the two deletions verified against the capture, below |
| S306 | C02, C05 | `F,E:FileNotFoundError,…` / `P,P,P,P,P,P` |
| S307 | C06, C09 | `P,P,P,P,P,P` / `P,P,P,P,P,P` |

The two rejected rows read exactly in the contract's rejected form — `REJECTED: <reason>;
flip: <what would change the verdict>`:

- **S308**: "REJECTED: pip-installs pytest over the network and first runs the cloned
  repository's own test suite (python -m pytest in /app), which the offline replay does
  not stage; the replay calls the six functions of test_outputs.py directly; **flip:** an
  offline copy of bottle's test tree at 0207a34f and pinned pytest wheels" ✓
- **S309**: "REJECTED as an input: the harness runs a prebuilt image the replay never
  pulls, so the Dockerfile recipe (S305) is the modelled /app, not the image's bytes;
  **flip:** the image pulled and its /app/bottle.py compared with VULNERABLE_BOTTLE_SHA" ✓

### `status` — "`queued` (opened, worth mining) · `mined` (cited by ≥1 path in `used-by`) ·
`rejected` (kept — a rejection is evidence of taste)."

S303–S307 `mined`, S308–S309 `rejected` ✓; the census's status histogram prints
`mined=266 queued=8 rejected=27` with no invalid value ✓.

### `opened` — "ISO date the row's author opened the source."

All seven say `2026-11-05` ✓, and the round's own fetch receipt
(`.ufo/waves/round-95/L1/capture-fetch.txt`) shows every one of the seven URLs fetched
`http=200` on 2026-11-05T19:43:32-03:00 with the byte count and sha256 the row states ✓.

### `recheck` — "ISO date or cadence (`90d`, `180d`, `on-release`)."

All seven say `on-release` ✓ — the same cadence the round-94 rows for this benchmark use
(S297–S302).

### `used-by` — "repo-relative paths of the knowledge entries or lessons citing the row,
comma-separated, or `—`."

S303–S307 name `plans/round95-cases.json`; S308 and S309 name `—` ✓ (rejected rows
properly cite nothing). Every named path exists (`[ -e "$p" ]` over all mined rows prints
nothing missing) ✓.

**Observation, not a violation.** The contract's wording is "the knowledge entries **or
lessons** citing the row". `plans/round95-cases.json` is neither a knowledge entry
(`corpus/knowledge/`) nor a lesson (`corpus/lessons/`) — it is the round's case table. But
this is the lane's established convention for this benchmark: the round-94 rows S297–S300
name `plans/round94-cases.json` in the same cell, and 38 mined rows across the file point
at a `plans/` or `corpus/evidence/` path rather than a knowledge/lesson path. The rows are
also **not cited by** `plans/round95-cases.json` in the S-id sense — that file contains
no S-id at all (`grep -oE "S[0-9]{3}" plans/round95-cases.json` → nothing) — it names the
*member* (`fix-code-vulnerability`, once) and the case ids. So `used-by` here records
"the case table this row's claim rests on", which is the same sense the round-94 rows
used. Reported for the L1's awareness; I do not claim it is a defect.

## The census the contract states, run on the tip

The contract gives the census commands; this seat ran them at the tip
(`receipts/receipt-sources-census.txt`):

```
rows                        301
malformed rows (NF!=13)      0
tier histogram              A=271 B=24 C=6
status histogram            mined=266 queued=8 rejected=27
duplicate ids               (none)
enum violations / tier inflation   (none)
mined rows whose used-by path does not exist   (none)
```

The lane's own maintained census CLI agrees:
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` →
`kengaku rows 301 / tier.A 271 / tier.B 24 / tier.C 6 / status.mined 266 / status.queued 8
/ status.rejected 27`, and the fleet totals report `missing 0`.

## The lane's own anchor gate, at F and at T

`plans/anchor_line_check.py` is the gate the contract's rule 1 leans on (it checks the
located quote against the capture). Run by this seat on a clean clone of each revision:

```
at F  d9cd18a7519a… : ANCHORLINE rows=294 cited=104 captured=91 uncaptured=13
                        defective=10 repaired=10 live=0 cells=0   rc 0
at T  afe9c229e37a… : ANCHORLINE rows=301 cited=111 captured=98 uncaptured=13
                        defective=10 repaired=10 live=0 cells=0   rc 0
```

`+7 rows, +7 cited, +7 captured` — the seven new rows are all *cited* (they carry a
line-located quote) and all *captured* (their sha256 matches a tracked capture under
`corpus/evidence/`), and the gate's `live`/`cells` counts are unchanged at 0/0. **No new
defect was introduced by S303–S309.** (The ten `defective` rows are the lane's pre-existing
repaired ones — S108, S149–S155, S201, S221 — unchanged from F.)

## The claims file's own statement about these rows, checked

`plans/round-95-claims.md` § "Source (sourced claim, CORPUS rule 1)": "New rows for the
grader, the reference solution, the Dockerfile's oracle-removal lines, the upstream
bottle.py and the instruction, opened 2026-11-05 (HTTP 200, sha256 equal to the table
above); `tests/test.sh` and `task.toml` are opened and rejected as replay inputs."

Checked against the rows: the seven rows are exactly those seven sources (S303–S309),
each `opened 2026-11-05` ✓, each sha256 equal to its capture ✓, and the two rejected ones
carry the rejected status ✓.

**One imprecision in the claims file's prose, which does not affect the rows.** "sha256
equal to the table above" — the `frozen-instruments` table above it holds **four** of the
seven capture digests (the grader `c006a5de…`, the solution `7a0131b3…`, the Dockerfile
`09174709…`, the upstream bottle `abf64368…`); the instruction's `89b1abdf…`, the test
wrapper's `f1611da6…` and the task manifest's `9aa2bd14…` are **not** in that table,
because they are not instruments the counters read (they are the cited source and the two
rejected inputs). The claims file is F-frozen and this seat does not edit it; the
sentence is ambiguous rather than wrong (it can be read as "the sha256s of the rows
named are those of the captures named"), and the rows themselves carry the correct
digests. **Reported so the L1 can decide whether to route it; no row is affected.**

## What I could not check from here

- I did not re-fetch the seven upstream URLs. The round's own fetch receipt
  (`.ufo/waves/round-95/L1/capture-fetch.txt`, HTTP 200 for all seven with byte counts
  and sha256) and the lane captures are the evidence of opening; the "Non-author
  verification re-opens a sample" clause of rule 1 is a separate seat's job (a
  `ScoutSources` seat exists in this wave).
- I did not verify the `teaches` prose against the *grader's semantics* beyond the case
  ids each row cites — that check is the C1 counter's, and the counter's own committed
  receipt at T records `mismatches=0 defects=0` over 15 cases and 105 legs.

## Summary table

| contract clause | S303 | S304 | S305 | S306 | S307 | S308 | S309 |
|---|---|---|---|---|---|---|---|
| id shape / no reuse / no pipe | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| source title + canonical URL | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| kind in enum | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| tier A justified, not community | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| scope present | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| anchor has location + revision + quote | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| quote re-verified against the capture | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| teaches grounded (or rejected form) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| status in enum | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| opened is ISO, matches the fetch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| recheck is a legal cadence | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| used-by paths exist (or `—`) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| census: rows / malformed / tier / status / dup-ids / enums / missing paths | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Verdict: no contract violation in S303–S309.** Two observations for the L1: the
`used-by` convention (a plan file, not a knowledge entry or lesson — house-wide), and the
claims file's "sha256 equal to the table above" phrasing (only four of the seven digests
are in that table).
