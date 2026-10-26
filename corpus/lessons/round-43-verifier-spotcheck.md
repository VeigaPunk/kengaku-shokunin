author: hyaku closure (non-author integrator, @m_opus)

# Round 43 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `1838be94b355e40139d4231f743bc6946f77c1f6` (before: `317148c4b918fb2645e46ec0225cac720a8a57e9`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T18:37:20-03:00 launch kengaku round=43 pgid=1209004 driver=hyaku-inline attempt=1` ·
`2026-10-26T19:57:48-03:00 complete kengaku round=43; hyaku-inline attempt=1`.
Scratch for my re-runs: `/fast/scratch/closure-kengaku-r43.Ub2U` (a clean `--no-local` clone detached at `1838be94`, plus
the re-fetched upstream files under `fetch/`). No gate was executed: `round43-c1-mutants`, `round43-c2` and
`gate-flip-check` are registered `gate` rows (`SKILL.md:602-603`, `:606`), so they are evidence-verified. The registered
`probe` `feal-probe` (`SKILL.md:604`) was re-run. No seat was dispatched by this closure.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-43/kengaku.md` (fleet repo) | `kengaku-shokunin <kengaku@shokunin.local> e8c221f29efd7607506fa985dccd3fda94d393be Mon Oct 26 19:51:57 2026 -0300`. The lane tip `1838be94` was committed at 19:51:11, 46 s earlier, and the report cites it. The `complete` line is 19:57:48 |
| `SHONEN` heading, one line per box | `grep -n '^## ' <report>`; `git show 1838be94:SHONEN.md \| grep -cE '^\s*- \['`; `grep -cE '^- \[[x~ ]\]' <report>` | `## SHONEN` at :146; 4 boxes in `SHONEN.md`, 4 `[~]` lines in the report |
| `Sources & frontier`, `Trend verdicts` sections | `grep -n '^## ' <report>` | present (:108, :131) |
| cited lane commits exist, ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for `317148c4 02753f26 6b49694d d33350fd 77ea425a 8adf76cc ac339b25 2a3e29c6 1838be94` | 9/9 resolve and are ancestors (exit 0). `2fd12b88` is the upstream TB2 pin, not a lane commit. All eight round commits (`git log 317148c4..1838be94`) are authored by `kengaku-shokunin <kengaku@shokunin.local>` |
| commit-time order of the freeze | `git log --format='%h A=%ad C=%cd' --date=iso 317148c4..1838be94` | freeze `02753f2` committed 18:54:18. Its jj author stamp, 18:36:02, is the change's creation time. Its controls end at 18:51–18:52, so no evidence is future-dated. The receipt `6b49694` is at 18:56:29, after the freeze. `plans/battery43` first appears in `77ea425` at 19:24:42 (`git log --diff-filter=A`), after both |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain` | `state branch=master local=1838be94… remote=1838be94… ahead=0 behind=0 head=detached tracked=0 untracked=4`. The porcelain shows 4 `??` entries: `.ufo/waves/round-43/build.ready`, `build.ready.dispatched`, `falsify/` (one `swarm-registry.json`, 22:39Z), `integrate/DOCS` (`8adf76cc…`). See D2 |
| prompt carries the template contract | `diff /home/vgpnk/Projects/kimi-shokunin/templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kengaku-round-43.md)` | Every removed template line is a `{{…}}` placeholder line (LANE/ROUND/FLEET_ROOT/AXES). The prompt carries §1 binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract, §5 commit/push scope/L0, §6 hyaku addendum (:141, run-9 band "64–128 seats in total, every round") and §7 scratch discipline (:594). The prompt was committed by `kengaku-shokunin` (`006480bd`) |
| wave shape equals the report | `jq '.results\|length'` over `build-results.json`; role tally over `build-spec.json`; `git ls-tree --name-only 1838be94 .ufo/waves/round-43/build/ \| grep -c '\.md$'` | 38 results. Roles: executor 11, scribe 7, critic 5, scout 5, connector 4, reviewer 3, mutation-tester 2, sentinel 1, as the report states. 37 report files; `R43ConnClaims` has no file (0 matches), as disclosed. The falsify spec carries 33 seats and no `falsify-results.json` exists, as disclosed |
| measured revision transfers to tip | `git diff --name-only 2a3e29c6 1838be94` | only `integrate/measure-tip.txt`, `SCORECARD.md` and `corpus/lessons/round-43.md`, so no claim surface moved after `measure-tip.txt` @ `2a3e29c6` |
| frozen inputs untouched | `sha256sum -c .ufo/waves/round-43/claims/frozen-digests.txt` in the clean clone; `git diff --stat 02753f26 1838be94 -- plans/round43_c1_verify.py plans/round43_c2_verify.py plans/round-43-claims.md plans/feal_probe.py plans/pkg-spec-r43.json`; `git diff --stat 317148c4 1838be94 -- plans/anchor_digest_check.py plans/order_check.py`; `git show 1838be94:<tool> \| sha256sum` | 12/12 `OK`; both diffs are empty. The tools hash to `11bb2cad87be…c70fd4c2` and `948d5e1d2b34…0fc6ecc`, which equal `PINS` in `plans/round43_c1_verify.py` |
| append-only lane docs | `git diff --numstat 317148c4 1838be94` (rows with deletions); `git diff --stat 317148c4 1838be94 -- LOG.md PROVINCE.md SKILL.md corpus/README.md corpus/QUALITY.md` | Only `corpus/routed-findings.jsonl` has deletions (`77ea425`: 46+/2−; `8adf76c`: 13+/13−). These are the status/close fields of the routed ledger (R42-R2 check nulled, R42-R4 closed, 13 rows closed on observe), which the report and SCORECARD disclose. The five docs have 318 insertions and 0 deletions, and `SCORECARD.md` has 102 insertions and 0 deletions |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (lane tree = tip) | 15 `W04` (duplicate URL across scopes, S040…S100, none new), `kengaku ok`, exit 0, equal to the report's after-state |

Conformance defects and notes. All are status-neutral.

- **D1 — round total 38 < 64.** The run-9 band in prompt §6 is "64–128 seats in total, every round". Wave 2 (33 seats)
  was validated but not dispatched. The lane self-disclosed this as a §Mistakes row at close.
- **D2 — wave control files left untracked.** `build.ready`, `build.ready.dispatched`, `integrate/DOCS` and
  `falsify/swarm-registry.json` sit uncommitted in the lane. Round 42 committed the same kinds of file
  (`git ls-files .ufo/waves/round-42/ \| grep -E 'ready|falsify/swarm-registry'` lists five). They are not claim
  surfaces, but they are round residue.
- **D3 — one seat returned no report file** (`R43ConnClaims`; its output exists only in `build-results.json`). Disclosed.

## 2. Claims — re-check

**C1 — calibration (8): nine near-variants of the two gate tools killed with value attribution.** I re-measured the
committed bytes and evidence-verified the kill verdicts against the registered gate `round43-c1-mutants`.

- Re-measured: battery size before→after.
  `git ls-tree -r --name-only 317148c4 plans/battery43 | wc -l` → `0`. At `1838be94`, an `ast` count of each module's
  `FIXTURES` list gives `a_alt 14, a_err 6, a_row 3, a_url 4, o_alt 6, o_excuse 3, o_scan 6`, `total=42`. This equals
  the receipt's `BATTERY fixtures=42` and the 42 `FIXTURE` lines in `measure-final.txt:1-65`.
- Re-measured: the counter is the frozen one. It has `TOTAL = 9` and `FLOORS = {"anchor": 6, "order": 3}`
  (`plans/round43_c1_verify.py:131-132`) and is byte-identical to the freeze (diff empty, digest `OK`). The two tools it
  mutates are unedited across the round, and their sha256 values equal the counter's `PINS`.
- Evidence-verified (not executed), before: `claims/control-c1-nothing.txt` shows
  `BATTERY fixtures=0 … MUTANTS total=9 killed=0 survived=9 … PREDICATE C1 fail`, `exit=1`.
- Evidence-verified, after at landing `77ea425a`: `integrate/measure-final.txt` shows `TIP 77ea425a…`,
  `untracked_in_clone=0`, `PINS total=2 mismatched=0`, nine `MUTANT … killed … value=differs` lines with `hits` 4–11
  (NA1 6, NA5 5, NA7 11, NA18 4, NA20 10, NA21 10, NO5 7, NO7 4, NO22 8), then
  `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=6/6
  order=3/3`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, `exit=0`. This is the exact line sequence of the frozen
  predicate (`plans/round-43-claims.md:53-56`).
- Evidence-verified, after at `2a3e29c6`: `integrate/measure-tip.txt` shows the same `BATTERY`/`MUTANTS` lines,
  `PREDICATE C1 pass`, `c1_exit=0` and `ENVELOPE end 19:51:07 exit=0`.
- Limits the lane names, which I accept as named: the counter cannot see intent (witness-as-battery passes:
  `claims/control-c1-witness-as-battery.txt` `PREDICATE C1 pass` with 6 witness fixtures), and no falsify wave ran.
  Both are disclosed. The counter's battery-side guards (R4 `.git` FILE, depth, leg-i argv) have gaps that no battery43
  fixture uses (`R43SentinelCounter` F1–F3).
- **Verdict: verifies. calibration `improved`** (the frozen predicate moved from red to green; the score is held at 8 by
  the lane's own choice).

**C2 — coverage (7): pinned TB2 `feal-differential-cryptanalysis` grader admitted with an executed 12-case probe.**
I re-measured the counts, re-ran the registered probe, re-fetched six sources, and evidence-verified the gate
`round43-c2`.

- Re-measured: registry rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` gives 121 at
  `317148c4` and 130 at `1838be94`. The new rows S129–S134 are tier A, `code`/`docs`, `mined`. S135–S137 are tier B,
  `code`, `mined`. All nine have 11 cells (NF=13).
- Re-measured: knowledge files `git ls-tree --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` give 49 → 50.
  `tb2-feal-differential-cryptanalysis-grader.md` is new (0 `feal` files at `317148c4`) and opens with
  `source: S129 …`, `verified-at: 2026-10-26`, `recheck: 180d …`.
- Re-measured: the captures. `(cd corpus/evidence/round43/tb2-feal-differential-cryptanalysis && sha256sum -c
  SHA256SUMS)` gives 12/12 `OK`. A re-fetch of `<base>{tests/test_outputs.py, instruction.md, README.md,
  environment/Dockerfile, task.toml, environment/feal.py}` at 2026-10-26T20:01:12-03:00 returned six `200`s, and
  `cmp` against the captures gives 6/6 identical.
- Re-run probe (registered `probe`, not a gate): `python3 plans/feal_probe.py --lane . --work <scratch>` in the clean
  clone exited `exit=0` and is `cmp`-byte-equal to `corpus/evidence/round43/feal-probe.txt`: `cases=12
  observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`. That includes the host-dependent
  `cheat-clock-seed`.
- Evidence-verified, before: `claims/control-c2-nothing.txt` shows P2–P10 `DEFECT`s (`checks=10 defects=7`, as
  reported). The informed-filler control's `CONTROL informed V10 DEFECT …`, `CONTROL content V10 ok` and
  `CONTROL-C2-INFORMED-FILLER red-as-required` (`claims/control-c2-informed-filler.txt`) confirm that V10 is red for a
  filler built from the receipt.
- Evidence-verified, after: `measure-final.txt:79-90` shows V2–V10 `ok`, `checks=10 defects=0`,
  `PREDICATE C2 pass`, `exit=0`. `measure-tip.txt` gives the same at `2a3e29c6`.
- Named limit, accepted as named: V10's `DECISIVE` key is readable in the counter, so a copycat filler passes
  (`R43CritClaims` §1). The probe re-run and my own reading of `test_outputs.py:20-30` stand independently of V10. The
  grader has one function, and the assert at `:30` compares `feal_in_c.get_keys()[5]` with the agent's return value
  after `/tests` is put on `sys.path` (`:23`). So the entry's central findings (importable answer, untimed call, import
  order) re-derive from the capture.
- **Verdict: verifies. coverage `improved`** (one admitted entry on ground the coverage map did not hold, citing six
  tier-A rows opened this round; the score is held at 7 by the L0 cap `kengaku | round-33`).

**No harm.** `git diff 317148c4 1838be94 -- SCORECARD.md` is 102 insertions and 0 deletions. No axis score is lowered:
calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8 and adjacency 8 are all carried. The
landing measurement's no-harm set (`measure-final.txt` rounds 36–42 counters, probes byte-equal, census exit 0) is
evidence-verified. My own probe re-run and census run agree with it.

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 predicate red → green; fixtures 0 → 42 re-measured; kills evidence-verified |
| coverage | improved | C2 predicate red → green; knowledge 49 → 50, rows 121 → 130 re-measured; probe re-run byte-equal |
| novelty | unchanged | no claim; no novelty asserted (entry :382 "claims **no novelty**") |
| depth | unchanged | score 9 carried; append-only docs |
| operability | unchanged | score 8 carried; `gate-flip-check` capability rides as a rider (selftest `SELFTEST ok=19/19`, `.ufo/waves/round-43/build/R43FlipCheck/selftest.txt`) |
| freshness | unchanged | score 8 carried; captures re-fetched `cmp`-identical by me |
| adjacency | unchanged | score 8 carried; PROVINCE routing clause appended |

## 3. Discernment spot-check (`corpus/lessons/round-43.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S129 `tests/test_outputs.py` | admit (A, mined) | `<base>tests/test_outputs.py` (200, `cmp` = capture, sha256 `585780e76d98…`); `sed -n 30p` | **agree** | `:30` is `    assert feal_in_c.get_keys()[5] == stolen`, the quoted 4 words verbatim. This is the whole graded predicate, so it is primary for its scope |
| S134 `README.md` | admit (A, mined) | `<base>README.md` (200, `cmp` = capture, `887407c78513…`); `sed -n 35p` | **agree** (with nit R2) | `:35` is `4. Confirms the attack completes within the time limit`, verbatim, and `test_outputs.py:1-30` contains no timer. Admitting the authors' falsifiable (and false) sentence as their claim is sound. Nit: the file has no final newline (`wc -l` → 34), and the entry's `source:` line says "lines 1-34" while the row anchor says `:1-35` |
| S136 `environment/Dockerfile` | admit (B) — refusal whose flip fired | `<base>environment/Dockerfile` (200, 220 bytes, `cmp` = capture); `sed -n 6p` | **agree** | `RUN pip install setuptools==80.9.0` verbatim. The entry cites the image recipe (`:69-71`), so the stated flip fired and was executed |
| `task.toml`, `setup.py`, `solve.sh`, `feal.h`, `SHA256SUMS` | reject — captured, not rows; flip "an entry sentence that rests on one of them alone"; recorded `Flip check (round 43): task.toml — not fired` | `<base>task.toml` (200, `cmp` = capture); `sed -n 22p` → `timeout_sec = 1800.0`; entry `grep -nE 'task\.toml\|solve\.sh'` | **disagree** (on the flip verdict; I agree with refusing them as rows) | The flip fired. The entry's Mechanism row `slow-oracle-45s` → `task.toml:22` and finding 11 ("The only ceiling … is `task.toml:22`'s `timeout_sec = 1800.0` … the only time bound the grader's environment actually carries", `:298-302`) rest on `task.toml` alone. The 1800 s verifier bound has no other source: S134 states the agent's 30 minutes, not the verifier's. The Mechanism row `oracle-solve-sh` → `solve.sh:90` and finding 12 ("The differential attack in `solve.sh` recovers exactly that round key by the characteristic at `solve.sh:90`", `:305-306`) rest on `solve.sh`'s internal logic. That contradicts the entry's own `:72-74` ("no finding rests on its internal logic beyond the fact that the recipe returns a value the assert accepts"). This is the same class as round-42 D3, which this round mined. `gate_flip_check.py` verifies that a `Flip check` line exists, not that its verdict is true |
| assimilation set `merge/kengaku/` | reject — none adopted | `/home/vgpnk/Projects/shokuknow/merge/kengaku`: `sha256sum SOURCES.append.md MERGE-REPORT.json MERGE-REPORT.md` → `a4645885…`, `c47fbe68…`, `807b8451…`; `find . -type f \| wc -l` → 68; `find . -newermt '2026-10-24 23:33:21' \| wc -l` → 0; `grep -rliE 'feal\|cryptanaly' . \| wc -l` → 0 | **agree** | The package bytes equal `R43MergeRescreen.md` §1, nothing is newer than 2026-10-24, and no staged entry touches this round's surface |

New `SOURCES.md` rows re-opened, with quotes checked (≤25 words, at the cited line, in the re-fetched bytes):
S129 `:30` (4 words) ✓; S130 `instruction.md:3` "Your attack should run in less than 30 seconds" (9) ✓; S134 `:35` (8) ✓;
S136 `Dockerfile:6` (4) ✓; S137 `feal.py:27` "x = random.randint(0, 0xFFFF)" (4) ✓; S131 `feal_module.c:52` "Get the current keys as
a list of 6 32-bit values" (11) ✓. All six source files are `cmp`-identical to the committed captures.

Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → `kengaku ok`, 15 `W04`, exit 0.

## 4. Trend verdicts

- **expansion — improved.** `tb2-feal-differential-cryptanalysis-grader.md` is a new admitted entry on ground the
  coverage map did not hold. Its `source:` cites S129–S134, which are `mined` rows opened this round, and its probe
  re-runs byte-equal. Knowledge files 49 → 50, rows 121 → 130, re-measured. Three capability rows were demonstrated
  in-round (`value-attributed-mutant-kills` via `measure-final.txt`, `in-process-import-grader-probe` via my probe
  re-run, `gate-flip-check` via `SELFTEST ok=19/19`).
- **quality — unprovable-but-better.** I agree with the lane. Round-42 errata E1–E7 and the S128/S135 records landed,
  the routed queue became durable (`routed_open=39` at tip), and 13 rows closed on a clean-clone observe. Against
  that: no falsify wave ran, V10's key is readable, three wrong sentences were caught only by the L1's own re-read,
  and §3 finds two entry sentences whose sourcing contradicts the entry's own provenance paragraph. No admitted
  entry failed my re-check, so the trend is not harmed.
- **discernment — unprovable-but-better.** Round 42's outside disagreement (D3) became a lesson, a grounded
  `QUALITY.md` criterion (Q35, `corpus/QUALITY.md:872`) and a checker with a red-before state (`FLIPS total=45
  unresolved=45`). That is `LEARNING.md`'s improvement path. But this round's spot-check agrees on three admits and
  one reject and disagrees on the `task.toml`/`solve.sh` flip verdict. That is a recurrence of the same class, which
  the new checker cannot see because it tests that a line exists, not that its verdict is true. The criterion is not
  yet shown to bite, so the verdict is not `improved`. The disagreement is new this round, so it is not yet "left
  unlearned" and the verdict is not `harmed`.

## 5. Routed defects (round 44)

- **R1 — false `not fired` flip verdict (§3, discernment disagreement).** Append a corrected
  `Flip check (round 44): task.toml — fired — …` and the same for `solve.sh` to `corpus/lessons/round-43.md` (append
  only). Then either admit `task.toml` and `solve.sh` as rows (with Gate quotes, if they are worth a tier) or append
  an entry erratum that re-sources or withdraws finding 11's "only time bound" sentence, the two Mechanism rows and
  finding 12's `solve.sh:90` claim, and reconcile them with `:72-74`. Extend `plans/gate_flip_check.py`/Q35 so that a
  `not fired` verdict naming a file is checked against the cited entry (for example, any `<file>:<line>` citation of
  the refused item in the entry turns `not fired` red). Ship a red control built from this lesson.
- **R2 — anchor mismatch on S134.** The entry's `source:` line says `README.md` "lines 1-34", while the row anchor and
  Gate quote are at `:1-35`/`:35` (the file lacks a final newline). Append an erratum to the entry.
- **R3 — untracked wave control files (D2).** Commit `.ufo/waves/round-43/{build.ready, build.ready.dispatched,
  integrate/DOCS, falsify/swarm-registry.json}` under a round-44 commit, or record why they are excluded.
- **R4 — round floor (D1/D3).** Meet the 64-seat floor. Dispatch wave 2 before integrating wave 1, as the lane's
  own fix says, and make every seat leave a report file.
- **R5 — the lane's own routed limits** carry forward as filed: the V10 readable key (`R43CritClaims` §1), counter
  fences F1–F4 and V2′, 7/15 C1 guards and 7/13 V9/V10 guards that survived mutation, and the envelope's mode-only
  blind spot (`R43ReviewEnvelope`).

Operator note (promotion is operator-owned): all four `SHONEN.md` boxes are `[~]`, and their pointers resolved in this
closure. The `LOG.md` round-43 entry is at `:1309`, the end-to-end probe re-ran byte-equal, `integrate/measure.sh` is
committed, and the `PROVINCE.md` routing clause is appended. They look checkable by a non-author.
