author: hyaku closure (non-author integrator, @m_flash)
round: kengaku 31
lane HEAD before: 0883e72ef8474ca42ac1a54eb0273079f1507035
lane HEAD after:  87f0d32e4a4416a918020bf3fcd2df51cc2d3732
date: 2026-10-25

# Round 31 — non-author verifier spot-check

Dispatch digest (copied from `.ufo/watchdog.log`, which is mutable):

```
2026-10-25T05:41:06-03:00 launch kengaku round=31 pgid=451980 driver=hyaku-inline attempt=1
2026-10-25T06:07:59-03:00 complete kengaku round=31; hyaku-inline attempt=1
```

Scope: kengaku round 31 only — three claims, a filed report with one erratum and two addenda. I did not
author this round. Claims C1 and C2 were re-measured with plain commands over committed bytes; C3 rests on
a lane-owned gate (`plans/sources_adopt.py`) and was **evidence-verified, not executed** (PROTOCOL
§Gate standard, Closure consequence). C1's three adopted sources were re-opened live at their pins.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-31/kengaku.md` (fleet) | four commits, all `kengaku-shokunin`: `22c82baf` (filed, +193), `feac950c` (erratum, +30), `ba3515f3` (addendum, +7), `1180c217` (addendum 2, +9) | ok |
| erratum is append-only | `git diff <a> <b> -- <report> \| grep -c '^-[^-]'` for each consecutive pair | `0`, `0`, `0` | ok |
| `SHONEN` heading, one line per box | report §SHONEN vs `grep -c '^- \[' SHONEN.md` → 4 | four `[~]` lines, each with a pointer; no `[x]` | ok |
| cited lane commits exist and are ancestors | every 7–40-hex token in the report: `git cat-file -t` + `git merge-base --is-ancestor <h> master` | `0883e72`, `dbb07364`, `d6aa66e`, `97e69c7b`, `b54611c3`, `f6422263`, `634ded8`, `a6ff2f0e`, `3e13607e`, `9591131e`, `ae14f46d` → commit, ancestor. `6099b8cf`, `66f92766`, `2fd12b88` are upstream pins (not lane commits). **`a44b5a8` → missing** | defect D1 |
| lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `branch=master local=remote=87f0d32… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | ok |
| prompt carries template contract | `diff templates/round-prompt.md` (140 lines) vs `.ufo/prompts/kengaku-round-31.md:1-140` | placeholder substitutions only (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §4 report path, SHONEN, hash-citation, §5 commit-before-report, write scope present; §6 hyaku addendum follows | ok |

Round commits (`git log 0883e72..87f0d32`): 13, all `kengaku-shokunin`. `dbb0736` carries author date
`05:05:22-03:00`, 36 min before the launch line, with committer date `06:01:14` — consistent with a jj
change created before dispatch and described later; noted, not a defect.

## 2. Claim re-checks

### C1 — coverage: shokuknow assimilation round 3 (benchmark verifier execution model)

Plain re-measurement (both revisions):

```
for r in 0883e72 87f0d32: entry exists / ls-tree corpus/knowledge *.md / grep -c '^| `knowledge/' corpus/README.md / grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md
0883e72: entry=no  knowledge=39 index=39 registry=88
87f0d32: entry=yes knowledge=40 index=40 registry=91
```

Entry head at tip: exactly three `source:` lines (S092, S093, S100), `verified-at: 2026-10-25`, `recheck:`
names all three pins. Cell parse of the three rows (pipe-split, escaped pipes respected): each `tier A`,
`status mined`, `opened 2026-10-25`, `recheck 180d`, `used-by corpus/knowledge/benchmark-verifier-execution-model.md`.
The frozen predicate's conditions all hold on plain greps; matches the report (39 → 40 after the
SCORECARD correction `3e13607e`; the filed "40 → 40" was the lane's own error, corrected by append).

**Live re-open (all three adopted sources, 2026-10-25, my own fetches):**

| source | fetched | observed | vs lane |
|---|---|---|---|
| S092 Harbor `6099b8cf` `config.py` | raw.githubusercontent | `:590` "Whether the verifier runs in the agent's environment ('shared') ", `:592` "to 'separate' if a verifier 'environment' is set, otherwise " | sha256 `ac9f5d19…` = lane capture |
| S092 `verifier_mode.py` | same | `:31` `return _resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED`; docstring `:18-21`; precedence `:39-40` (the addendum's corrected locators are right) | `e5893be9…` = lane |
| S092 `verifier.py` | same | `:168` "Discard stale rewards without removing other verifier inputs or logs."; `:207` `await self._remove_reward_files()`; `:209` `if not self._skip_tests_upload:`; `:220-223` `upload_dir(... tests_dir)` | `fc5d9fc6…` = lane |
| S093 SWE-bench Pro `66f92766` `test.sh`, `parser.py` | same | `test.sh:33/:38/:43-44/:60/:63/:71/:213-214` all as cited; `:97-104` restores edited tracked `*fixtures/*` paths (confirms the falsify-wave correction landed in `f6422263`); `parser.py:68/:71/:90/:121` as cited (`:121` dict dedupe = last-write-wins) | `b6f26eec…`, `303ceda2…` = lane |
| S100 terminal-bench-2 `2fd12b88` | raw README; `gh api …/contents?ref=` | README line 46 `uv run harbor run --dataset terminal-bench@2.0 \`; root `92` entries = `dir=89 file=3` (`.gitignore,LICENSE,README.md`); `curl -sI` → `301` to `harbor-framework/terminal-bench-2` | `7dfa9992…` = lane; count matches |

All six capture digests in `.ufo/waves/round-31/assimilation/captures/SHA256SUMS.txt` equal my independent
fetches byte-for-byte. I also re-opened the SWE-bench Pro V2 `task.toml` for the cited task: `[verifier]`
has `network_mode`, `timeout_sec`, `collect` and no `environment_mode`/`[verifier.environment]`, so Harbor
resolves **shared**, as the entry's table says; and `v2/README.md:75-76` shows S078's "The verifier never
runs in the agent's sandbox." is achieved by `patch_replay:PatchReplayAgent` on a pristine image — a
property of the locked release protocol, not the harness, exactly as the entry's §Extends states.
**C1 verifies — coverage `improved`** (net-new entry on a new coverage row; canonical score stays 7 per the
frozen axis-verdict shape).

### C2 — calibration: R1–R10 closed (judged on byte-level review)

The lane discloses the counter is not self-proving (`R31FxC2Survivors.md`: every item has a fakeability
route). I therefore did not rest on `defects=0`; I re-read each repair against round-30 closure §5:

| item | my check (base `0883e72` → tip `87f0d32`) | observed | verdict |
|---|---|---|---|
| R1 `LOG.md:792` | `git diff --numstat -- LOG.md` | `71 0` (pure append); appended heading "correction to the round-30 C1 entry above (appended 2026-10-25, not rewritten)" quotes "two new fields, one new value set" and names it retracted | closed |
| R2 lesson Q6 basis | `git diff --numstat -- corpus/lessons/round-30.md` → `21 0`; read `## Errata (round 31 …)` | states the admitted basis "one field, and the rest is not a delta at all", verdict unchanged | closed (locator drift, D6) |
| R3 Q2 tier cell | same errata; registry cell parse | erratum says `S085 B, S086 B`; registry `S085 tier B`, `S086 tier B` | closed |
| R4 duplicated sentence | `grep -oF 'reconciled truth'` count | 2 → 1 | closed |
| R5 falsifier clause | diff of the bullet | duplicate `and populated (not "unknown")` removed; sentence reads once | closed |
| R6 staged-source count | diff `:39-45` | "two of its three source rows are not in this lane's registry (… registered … at tier A as S001)"; S001 is the GEM 2026 review (`aclanthology.org/2026.gem-main.50`) | closed |
| R7 S2 "only new field" | diff `:71-75` | narrowed to the card-level field; states the four values are already published by CTC v1.1 | closed |
| R8 licence adjective | `grep -oF CC0` | 1 → 0 ("the card design") | closed |
| R9 five seat reports | `sha256sum` of the five blobs at `dbb0736` vs `R31DefR9.md:43-49` worktree digests | `3712b4d9`, `6abe86bf`, `de7711fa`, `e11974a8`, `1d2cef2a` and line/byte counts all equal the seat's recorded worktree blobs — committed as authored, not reverted | closed |
| R10 round shape | `jq '.members\|length' .ufo/waves/round-30/falsify/swarm-registry.json` | `33`; erratum supersedes `:3` "34" with 33 | closed |

Receipts agree: `defects-before-final.txt` ten `DEFECT` lines, `checks=10 defects=10 exit=1`;
`defects-after.txt` `checks=10 defects=0 exit=0`. **C2 verifies on the byte-level review — calibration
`improved`.** Bound: round-30 §5 item 7 (report ordering) is outside R1–R10, is disclosed open, and
recurred this round (D2).

### C3 — operability: capture-to-citation binding in the adoption gate (evidence-verified)

| evidence | observed |
|---|---|
| plain code count, `git show <r>:plans/sources_adopt.py` | `0883e72`: 815 lines, 14 `case(`, 0 `url_map`; `87f0d32`: 1083 lines, 17 `case(`, 23 `url_map`, exits 8 and 9 present |
| control `.ufo/waves/round-31/claims/gate-before.txt` | baseline `error: unrecognized arguments: --url-map` `url_map_exit=2`; `SELFTEST cases=14 failed=0` |
| self-test tally `corpus/evidence/round31/gate-selftest-after.txt` | 17 `CASE … PASS` incl. `quote-url-bound-accepted`, `quote-url-mismatch-refused`, `quote-url-unmapped-refused`; `SELFTEST cases=17 failed=0` |
| failure capability `gate-binding-neutered.txt` | binding neutered → the two refusal cases `FAIL`, `cases=17 failed=2`, `exit=1` |
| CLI receipt `gate-cli-exits.txt` @ `634ded8` (and unchanged @ `ae95fe0`) | map-ok `exit=0` bound; map-bad `exit=8` url-mismatch; map-unmapped `exit=9`; no-map `exit=0`; registry path `exit=2` |
| revision measured | gate bytes unchanged `d6aa66e..87f0d32` (`git diff --quiet` → equal), so the `634ded8` receipt measured the landed gate |

**C3 verifies — operability `improved`.** Two defects, both status-neutral: the tip copy of the CLI receipt
is broken (D3), and the gate has no registry row (D4).

### Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | **improved** | C1 above |
| calibration | **improved** | C2 above; ten mismatches closed by bytes I re-read. New report-level mismatches (D1–D3, D5) routed, none in a pre-existing artifact |
| operability | **improved** | C3 above |
| depth | unchanged | `SCORECARD.md` diff `0883e72..87f0d32` is `+49 −0` (pure append, no score cell rewritten); "depth 9 held" |
| novelty | unchanged | non-claim in the frozen prereg; no phenomenon claimed |
| freshness | unchanged | census exit 0 at both ends; 14 → 15 `W04`, the 15th (S100↔S079 same repo, different scope) disclosed |
| adjacency | unchanged | `PROVINCE.md` unchanged; no sibling contest reported |

**No axis is harmed:** SCORECARD diff has zero deletions; `git diff --name-status -- corpus/knowledge` is
`A` one entry, `M` two (the R4–R8 copyedits and a Q21 recheck pin), no removal; census exit 0.

## 3. Discernment spot-check (non-author sample)

Source: `corpus/lessons/round-31.md` `## Gate` (1 admit, 4 rejects). Census:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, 15 `W04`, exit 0.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `benchmark-verifier-execution-model.md` | admit, re-grounded | Harbor `6099b8cf` (3 files), SWE-bench Pro `66f92766` (`test.sh`, `parser.py`, `task.toml`, `v2/README.md`), terminal-bench-2 `2fd12b88` (README, contents API) — all fetched live | **agree** | every locator resolves at the pin; captures digest-equal; the staged copy's `verified-at: 2026-10-23` and "partly observable" premise are present in `shokuknow/merge/kengaku/…/benchmark-verifier-execution-model.md:5,:11,:78`, so the re-grounding was needed; the S078 "never runs in the agent's sandbox" tension is correctly scoped to `PatchReplayAgent` |
| `benchmark-grader-semantics.md` | reject this round | staged file in `shokuknow/merge/kengaku/knowledge/corpus/knowledge/` | **agree** | its `source:` lines cite S094 (Toolathlon) and S097 (arXiv 2412.05579); `grep -cE '^\| S09[47] ' corpus/SOURCES.md` → 0 — neither row opened in-lane, so appending them would cite unopened rows (CORPUS rule 4) |
| `judge-calibration-thresholds.md` | reject (carried) | same package; staged S078/S081/S087 rows in `SOURCES.append.md` | **agree** | body's load-bearing figures (kappa 0.84 / 0.46 / 0.21) appear in **none** of the three anchor cells (cell parse: `[]` for each) — Q3 fails |
| SOURCES row S092 (new) | quote check | Harbor `config.py`, `verifier.py` @ `6099b8cf` | **agree** | three spans of 9, 9 and 10 words (≤25), each a byte substring of the cited line (`:590`, `:592`, `:168`) |

No disagreement: no new criterion is owed from this sample.

## 4. Trend verdicts

- **expansion: improved** — one net-new admitted entry on a new coverage-map row, citing three `mined`
  rows opened this round; registry 88 → 91, knowledge/index 39 → 40.
- **quality: improved** — the round-30 entry was corrected at five locations I re-read; the new entry
  re-verifies live with digest-equal captures; no admitted entry failed my re-check.
- **discernment: improved** — the outside sample agrees on 1 admit, 2 rejects and 1 new row.

## 5. Routed defects (the lane must fix next round; status-neutral)

- **D1 phantom hash.** Report addendum (`.ufo/reports/round-31/kengaku.md:226`) cites "`a44b5a8`-class
  commits"; `git cat-file -t a44b5a8` → missing. The locator fix landed in `ae95fe0`. Correct by erratum.
- **D2 report ordering recurred (round-30 §5 item 7, still open).** The final lane commits `ae95fe0` and
  `87f0d32` are never cited by the report; the erratum names `9591131e` as "the lane tip this round
  actually leaves". Land the report's last append after the last lane commit and cite that tip.
- **D3 broken CLI receipt at tip.** `ae14f46` rewrote `corpus/evidence/round31/gate-cli-exits.txt` with a
  run whose path `../../../plans/sources_adopt.py` resolves to `.ufo/plans` (absent); every line reads
  `can't open file` and `exit=2`. The report's addendum 2 calls this receipt "self-contained", and the
  SCORECARD C3 row's "0 / 8 / 9 / 2" no longer matches the file at tip. The valid receipt is in history at
  `634ded8`. Regenerate with `../../../../plans/` and append a correction.
- **D4 gate registry row missing.** `plans/sources_adopt.py` (exit map 0/2/4/6/7/8/9, `--selftest`) has no
  row in `SKILL.md` §Gate/probe registry (`grep -n sources_adopt SKILL.md` → none). Per §Gate standard
  (Delivery), no closure grades this gate conformant until that row exists.
- **D5 unreported falsify seat.** The falsify registry holds 36 members; 35 reports are committed — `R31FxEntryBar`
  has none (`comm` of registry keys vs `git ls-tree`). The report says "0 dead" and the lesson's Seat
  ledger says "none". Land the report or record the seat as dead.
- **D6 correction sweep misses.** Lesson `## Gate` table still cites `verifier_mode.py` precedence at
  `:35-38` (corrected to `:39-40` in the entry). The round-30 lesson erratum points the Q6 retraction at
  entry `:78-81`; at tip it is `:72` and `:82-83` (moved by the R7 edit).
- **Carried debt (lane-disclosed):** round-30 lesson `:66` "peer-reviewed" for S083/S086; claims freeze not
  committed before data (`R31FxClaimsOrder.md`); C2 counter survivors; C1 kill-rule branch unreachable;
  wave-report sealing routed to the protocol lane.

**Operator note (promotion is operator-owned):** the four SHONEN boxes look checkable by a non-author
from this round's evidence — box 2 and box 3 have runnable round-31 pointers, box 4 rests on an unchanged
`PROVINCE.md`. Box 1 points to an entry, not `SKILL.md`, so it is weaker. I wrote no `[x]`.
