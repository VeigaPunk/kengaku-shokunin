author: hyaku closure (non-author integrator, @m_opus)

# Round 37 — non-author closure spot-check (kengaku, 2026-10-26)

Measured against lane tip `dc90676b0a01bcb278dba3b5231b504fe2a9ff03` (before: `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd`).
Dispatch digest (`.ufo/watchdog.log`, mutable, copied here):
`2026-10-26T01:11:32-03:00 launch kengaku round=37 pgid=105920 driver=hyaku-inline attempt=1` ·
`2026-10-26T02:14:12-03:00 complete kengaku round=37; hyaku-inline attempt=1`.
Wave-2 (falsify) reports read at closure: 19 files under `.ufo/waves/round-37/falsify/*.md` (untracked, seats still
writing at 2026-10-26T05:22Z); cited below by seat name.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-37/kengaku.md` | `kengaku-shokunin 9b84562b9cb50f0d67934437c56a163b000d14bd 2026-10-26T02:13:26-03:00`; after the lane tip commit (02:12:25), before the 02:14:12 complete line; on `origin/main` and `origin/master` — ok |
| `SHONEN` heading, one line per box | read report | `## SHONEN`, 4 lines, all `[~]` with pointers — ok |
| cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `3ea9a1d9 ca790460 5c7b34e9 44b7298a a3163e67 c138da2b 5c7d5d75 aa3d6ead 188a2658 2a844a0d 357deceb 67cbe7a4 dc90676b` | 13/13 resolve, 13/13 ancestors; all 12 round commits authored `kengaku-shokunin` |
| pushed | `scripts/hyaku/jj-lane.sh state …` ; `git ls-remote origin refs/heads/master` | `local=remote=dc90676b… ahead=0 behind=0 head=detached tracked=0 untracked=1`; remote `dc90676b…` |
| uncommitted round work | `git -C lane status --porcelain` | `?? .ufo/waves/round-37/falsify/` — wave-2 seat outputs (19 reports + receipts), still being written by live seats; not lane-L1 edits, but uncommitted round evidence (defect D1 below) |
| prompt carries the template contract | `diff templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kengaku-round-37.md)` (prompt committed `8a940305`) | 10 hunks, every one a substituted placeholder (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); `grep -c '{{'` → 0; §6 hyaku addendum and §7 scratch discipline follow — ok |
| minimum report content | read report | work + evidence pointers, landed-changes table tied to `LOG.md`, before→after per claim with counting commands, Sources & frontier, trend verdicts, stale-lane line, tool-install line — ok |

Conformance defects (status-neutral):
- **Report filed before WAVE-DONE falsify** (the report says so, `kengaku.md:71-74`); wave 2's 37 seats were still running at
  closure and their outputs are uncommitted in the lane (D1).
- **Measured revision:** `integrate/measure-final.txt` is measured at `5c7d5d75`, not the cited tip. `git diff --stat
  5c7d5d75 dc90676b -- . ':!.ufo/waves'` touches only `SCORECARD.md`, `corpus/lessons/round-37.md` and
  `plans/round37_c1_attribution.py`; a grep of `round37_c1_verify.py`, `round37_c2_verify.py`, `pkg-spec-r37.json` and
  `pkg_gate.py` for `lessons|SCORECARD|waves|attribution` finds no read of those paths (the gate's P9 reads untracked
  files only, and a clean clone has none). The measurement transfers; I also re-ran the probe at `dc90676b` (§2).
- **Report's "landed changes" table** omits nothing I could find; the `ledger-tip` registry row (`SKILL.md:581`) is not
  among the two capability rows and is not claimed as one.

Status: `ok`.

## 2. Claims — re-measured vs evidence-verified

Plain measurements over committed bytes (`git show <rev>:…`, `git ls-tree`), a non-author seat's clean
`git clone --no-local` at `dc90676b` (`git status --porcelain --untracked-files=all | wc -l` → 0), and live re-opens.

| quantity | command | before (`3ea9a1d9`) | after (`dc90676b`) | reported |
|---|---|---|---|---|
| SOURCES registry rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 103 | 107 | 103→107 ✓ |
| tier / status histogram; malformed; duplicate ids | CORPUS census awk | A=88 B=13 C=2; mined=87 queued=8 rejected=8; 0; none | A=91 B=14 C=2; mined=91 queued=8 rejected=8; 0; none | A +3, B +1, all `mined` ✓ |
| knowledge files / README index rows | `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'`; `git show <rev>:corpus/README.md \| grep -cE '^\| \`knowledge/[^\`]+\` \|'` | 43 / 43 | 44 / 44 | 43/43→44/44 ✓ |
| anchor sha256 token lengths | `git show <rev>:corpus/SOURCES.md \| grep -o 'sha256 [0-9a-f]*' \| awk '{print length($2)}' \| sort \| uniq -c` | `3 0, 1 63, 8 64, 1 8` | `3 0, 1 63, 12 64, 1 8` | S110 still 63 hex in the row (append-only), corrected by the erratum at `round-37.md:32` ✓ |
| removed lines in lane-authored docs | `git diff --numstat 3ea9a1d9 dc90676b -- SCORECARD.md LOG.md SKILL.md PROVINCE.md corpus/{SOURCES,README,QUALITY}.md corpus/knowledge SHONEN.md` | — | `+33/0 +28/0 +50/0 +72/0 +72/0 +11/0 +4/0 +291/0 +53/0` | append-only ✓ |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | exit 0, 15 W04 | exit 0, 15 W04 (same set), `kengaku ok` | ✓ |

- **C1 (calibration) — evidence-verified, not executed.** `plans/round37_c1_verify.py` (`round37-c1-mutants`, `SKILL.md:578`)
  and `plans/pkg_gate.py` are registered gates, so I did not run them. Committed evidence read:
  `integrate/measure-final.txt` (clean clone of `5c7d5d75`, `untracked_in_clone=0`): `GATE plans/pkg_gate.py
  sha256=frozen`, `BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0
  null_detected=0`, `PREDICATE C1 pass`, `exit=0`. Red-before and skip-controls in `claims/`: nothing `killed=5 survived=50`
  exit 1 (also on committed `44b7298a`, `measure-before-committed.txt`); gate edited `invalid=55`; mislabel `wrong=1`;
  example `killed=6`. Plain cross-checks I ran: `git diff --stat ca790460 dc90676b --` the five frozen instruments, the
  dry table, `SHA256SUMS` and `claims/` → only `measure-before-committed.txt` added; 11/11 `frozen-digests.txt` entries
  MATCH at the tip (seat `R37CloseProbe`); `plans/battery37` absent at freeze (`git cat-file -e ca790460:plans/battery37`
  fails). Static AST read of the frozen counter and battery (no gate executed): 55 mutant ids, each `old` string occurs
  exactly once in the gate (`{1: 55}`); 50 battery37 fixtures in 9 modules (p6 8, d5 7, p5 7, p23 6, p7 6, p8 5, p4 4,
  p910 4, d4 3), 50 distinct `fid`s, 14 + 50 = 64 as printed; every mutant clause (P1–P10, D4, D5) is declared by ≥1
  battery37 fixture; no fixture id occurs in `pkg_gate.py`. Attribution audit (post-hoc, not the frozen rule):
  `integrate/c1-attribution.txt` `ATTRIBUTED 55/55 UNATTRIBUTED=0`; hostile battery `c1-attribution-hostile.txt` reaches
  `PREDICATE C1 pass` with `ATTRIBUTED 6/55 UNATTRIBUTED=49`. Wave 2 independently re-ran the frozen counter green
  (`F37C1Rerun` `c1-rerun-pass-killed-55/55`, `F37C1RerunPy313`). **Verified** (frozen predicate holds). Limits: the counter
  alone is gameable (lane-disclosed); `F37CritC1Axis` shows 6 of the 55 (M34–M39) map to no advertising sentence, so the
  freeze mismatch over *advertised* classes is 44, not 50 — still 44→0; wave-2 extra (non-frozen) mutants survive in
  P2/P3, P4, P5, P6, P7, P10, D4, D5 (`F37XMut*`), so the battery demonstrates the frozen 55 classes, not every branch.
- **C2 (coverage) — re-measured.** In the seat's clean clone at `dc90676b`: `python3 plans/git_webserver_probe.py --lane .`
  (registered **probe**, `SKILL.md:577`) exit 0, `cmp` with `corpus/evidence/round37/git-webserver-probe.txt` → identical
  (no normalisation); `--dry` byte-identical to `git-webserver-dry-cases-freeze.txt`; `sha256sum -c SHA256SUMS` 6/6 OK;
  join recomputed from committed bytes: same 22 ids in the same order, 9 predicted pass = 9 observed pass, 0
  disagreements, no `match=NO`. Counter `round37_c2_verify.py` is a registered gate (`SKILL.md:579`) — evidence-verified:
  `measure-final.txt` `V1 ok … V7 ok`, `checks=7 defects=0`, `PREDICATE C2 pass`, `exit=0`; before `control-c2-nothing.txt`
  `checks=7 defects=4` (V2, V3, V4, V7) exit 1; skip-control `checks=7 defects=1` exit 1. Wave 2 `F37C2Rerun`
  `c2-rerun-pass-probe-byte-equal-yes`. Entry provenance trio first (`source:` S111–S114, `verified-at: 2026-10-26`,
  `recheck: 180d …`), README index row at `corpus/README.md:70`. **Verified.** One entry statement falsified on re-read
  (§3, D2).
- **Frontier fix (not a claim).** `anchor_digest_check.py` is a gate; evidence-verified (`measure-final.txt`
  `rows=107 tokens=15 defects=0`; `F37AnchorRerun` before `defects=5` at `3ea9a1d9`). By hand: S070, S072, S073, S074
  anchors equal the committed `anchor-captures/` digests and the live bytes; S110's erratum digest equals
  `corpus/evidence/round36/tb2-regex-log/SHA256SUMS` (seat `R37CloseSources`). Limit: `F37AnchorRerun` M4b/M5 — a row
  pointed at *another row's* real committed digest passes (D3).

### No-harm audit

`git diff 3ea9a1d9 dc90676b -- SCORECARD.md`: +50/−0 — two appended capability rows (`gate-mutation-harness`,
`service-grader-probe`, first-working round 37) and an appended round-37 section; every axis stated held (calibration 8,
coverage 7 under the L0 cap, novelty 7, depth 9, operability 8, freshness 8, adjacency 8). No removed line in any
lane-authored doc (table above). Wave 2 `F37CritNoHarmDiff`: zero removed lines, no score moved; `F37NoHarmSweep`: 25/25
wave-1 baseline commands reproduce, 29/30 green — the one red is the new `ledger-tip` gate in a detached-HEAD clone
(D4), not a regression of a previously-green instrument.

### Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration (C1) | **improved** | frozen predicate met (committed receipt, independently re-run by wave 2), red-before controls committed, static audit: 55/55 mutants apply once, every mutant clause has a declaring fixture, no fixture keying; mismatch 50→0 (44→0 over advertised classes, `F37CritC1Axis`); score held 8→8; gameability and extra-mutant survivors disclosed or routed |
| coverage (C2) | **improved** | probe re-run byte-equal at the tip, dry table byte-equal, captures 6/6, S111–S114 re-opened live (§3), 43/43→44/44, 103→107; third TB2 task moved frontier→core; score 7→7 held by the L0 cap |
| novelty | unchanged | no claim |
| depth | unchanged | SKILL §Service-class decision table added, not claimed |
| operability | unchanged | two capability rows entered with demonstrations (probe re-run by me; mutant harness by committed receipt); `ledger-tip` red in detached clones (D4) |
| freshness | unchanged | S070/S072–S074 captures re-verified live; not claimed |
| adjacency | unchanged | real-image run routed, not absorbed (`PROVINCE.md:268-281`); `F37ConnSiblingCite` finds sibling sandbox prior art uncited (D6) |

No axis harmed. Both claims verify. Neither claim is exploratory.

## 3. Discernment spot-check (`round-37.md` `## Gate`)

| item · decision | re-opened source | agree/disagree | reason |
|---|---|---|---|
| `knowledge/tb2-git-webserver-grader.md` · **Admitted** | the entry at `dc90676b`; probe re-run; receipt `git-webserver-probe.txt` | **agree on admission; disagree on one requirement-map row** | sources, captures and the 22-case receipt reproduce byte-equal, headline findings hold. But the map row `instruction.md:9 \| enforced \| capitalised, leading-space` (entry `:107`, prose `:122`) is false under the entry's own definition (`:97-98`: `enforced` = a violating case observed `fail`): `CASE token-in-body … observed=pass` serves `TEST PASSED`, not `hello world`, and passes — as the entry's own `:30` and `:155` say. Strongest supported label is `partly` (`F37CritC2Map` row 9). The lane's flip clause ("a re-read falsifying an entry claim") is triggered for that row; I rule correct-by-erratum, not refuse, because the falsified sentence is one summary label contradicted by the entry's own receipt and headline, and V7 stays satisfiable with `partly`. Routed D2. |
| S111 `tests/test_outputs.py` · **Admitted (mined)** | live raw URL at `2fd12b88`, `sha256sum`, `sed -n 13p` | **agree** | live = row = capture = manifest `526aee3d…46b37`; line 13 `assert "TEST PASSED" in result.stdout, "Did not pass test"` (9 words, verbatim minus indent) |
| S112 `tests/verify.sh` · **Admitted (mined)** | live URL, `sed -n 62p` | **agree** | `1dc44c92…3d05` four-way match; `echo "Content: $CONTENT"` at :62 (3 words; also at :79, the cited line is genuine) |
| S113 `instruction.md` · **Admitted (mined)** | live URL, `sed -n 9p` | **agree** | `62151b73…1d97` four-way match; `then I see the output "hello world".` exact (7 words) |
| S114 TB2.1 issue #133 · **Admitted (mined, tier B)** | `gh api repos/harbor-framework/terminal-bench-2-1/issues/133` | **agree** | body sha256 `c217d372…4193` = row = capture (`diff` identical); body line 39 verbatim (14 words); `state=open`, `created_at=2026-07-14T06:32:15Z`; tier B right for a third-party report about the file |
| Real-image run (`build/R37DockerOracle.md`) · **Refused for the corpus; routed** | `PROVINCE.md:268-281` at `dc90676b`; `R37DockerOracle.md` §A–C | **agree** | the round-37 PROVINCE paragraph says the admission "does not run Terminal-Bench, the task image or a harness" and that real-image observations are "a separate, routed observation"; the run (oracle, static-file and `TEST PASSED`-body states all `reward.txt = 1`) is one run per scenario in apt-mutated containers — wave evidence, not an admitted instrument |
| Package `terminal-bench-release-identity.md` (merge/kengaku; S100, S092) · **Refused** | `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/terminal-bench-release-identity.md:1-12` (shokuknow `d9583b5a`); lane `SOURCES.md` S092/S100 | **agree** | its only sources are S100 (`terminal-bench-2` at `2fd12b88`) and S092 (harbor at `6099b8cf`) — the same URLs and pins the lane already holds as `mined` rows used by `benchmark-verifier-execution-model.md`, and lane S100's anchor already records the 92-entries/89-directories identity the package resolves; no new ground |

New SOURCES rows re-opened: S111, S112, S113, S114 (all four). All URLs resolve, all digests match live and capture,
every quote is verbatim at its stated line and ≤25 words. Census exit 0, `kengaku ok`, 15 W04 — the same set as before.

**Discernment conclusion:** the spot-check agrees with the gate on 5/5 sampled admits at the admission level and 2/2
sampled refusals; one narrow disagreement — a requirement-map label in the admitted entry (row 9 `enforced`). The
round-36 disagreement (S110 digest) and routed items 2–3 became lessons (`round-37.md` §Mistakes rows 1–2, 6–7) with
grounded criteria `QUALITY.md` Q26 and Q27, each citing `round-37.md`.

## 4. Trend verdicts

- **expansion — improved.** One admitted entry on ground the coverage map held as Frontier (third TB2 grader, first whose
  graded state is a live service), S111–S114 `mined` and re-opened live, two capability rows entered with demonstrations.
  The entry's central findings re-verify; the falsified map label is a correction, not a failed admission bar.
- **quality — unprovable-but-better.** Stale or unsupported items were re-verified and marked: S110 erratum resolves to the
  manifest digest; S070/S072–S074 now have committed captures equal to live bytes; `tb2-regex-log-grader.md` §Errata
  appended; append-only throughout. Against that, the new admitted entry fails part of its re-check (map row 9, and row
  8 cites the wrong witness, `F37CritC2Map`), and the anchor checker accepts a cross-row digest (`F37AnchorRerun`). That
  keeps this short of `improved`. Not `harmed`: both were found by wave 2 and this closure, after the lane's filing, and are
  routed rather than left after notice.
- **discernment — improved.** The sampled admits and rejects agree at the admission level, and last round's outside
  disagreement became grounded criteria (Q26, Q27). Caveat: this round's new disagreement (D2) must become a lesson and
  criterion next round.

## 5. Routed defects (lane fixes next round; status-neutral)

1. **D1 — wave-2 outputs uncommitted and unintegrated.** `.ufo/waves/round-37/falsify/` (19 reports at closure, seats
   still live) is untracked. Commit it under the round-38 entry and integrate its findings (items 2–7 are the ones this
   closure verified or relied on).
2. **D2 — entry requirement map overstates enforcement.** `corpus/knowledge/tb2-git-webserver-grader.md:107,122`
   (`instruction.md:9 | enforced`) contradicts `token-in-body observed=pass`; `:106,119-121` (row 8) rests `partly` on
   `catch-all-200`, which satisfies line 8 as written — `status-then-content-split` is the real violating pass; `:116`
   "port half is enforced" needs the by-construction qualifier. Append an erratum (the entry is append-only lane text);
   add a QUALITY criterion that every map label is re-derived against *all* receipt cases violating that line, and make
   V7 check it.
3. **D3 — anchor check binds to any committed digest.** `F37AnchorRerun` M4b/M5: a row whose anchor carries another row's
   real committed digest passes (`defects=0`). Bind each token to the capture the row's `source` names, as Q26's wording
   implies.
4. **D4 — `ledger-tip` red in detached-HEAD clones.** `F37NoHarmSweep` §3: `plans/defect_ledger.py:29` and
   `round36_c1_verify.py:38` hard-code `refs/heads/master`; a `--shared` clone of a detached source has no such ref, so
   R34-D2/R35-D3 print `agree=NO` (exit 1) instead of the declared `2` clone refusal. Fix the ref or refuse with exit 2.
5. **D5 — C1 freeze limits.** Six frozen mutants (M34–M39) are not advertised classes (`F37CritC1Axis`); extra non-frozen
   mutants survive across eight clauses (`F37XMutP23/P4/P5/P6/P7/P910/D4/D5`). Round 38's frozen list should add the
   survivors and the counter should attribute kills (already in SCORECARD `### Planned (round 38)`).
6. **D6 — sibling prior art uncited.** `F37ConnSiblingCite`: tameshi's bwrap defect-probes and kumitate `cap-run.mjs` are
   absent from every round-37 surface; `PROVINCE.md:283` names siblings without file:line. Report-out with pointers.
7. **D7 — carried.** C2 counter does not pin `pkg-spec-r37.json` and admits an informed filler (lane-disclosed);
   `R36CritScope` F3–F5 wording still open; spot-check item 4 (hand-run a mutant) not executed here — I do not run a
   sibling's gate; the static audit in §2 (55/55 `old` strings present once; clause coverage) stands in for it.
8. **SHONEN (for the operator).** All four boxes remain `[~]`. The end-to-end-task box has non-author-checkable evidence in
   consecutive rounds (round 36 regex-log probe, round 37 git-webserver probe, each re-run byte-equal by the closure). I
   did not tick it; promotion is operator-owned.
