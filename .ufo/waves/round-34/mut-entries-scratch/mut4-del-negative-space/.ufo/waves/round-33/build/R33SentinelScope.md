# R33SentinelScope — scope-discipline review of the round-33 build wave

Reviewed: `.ufo/waves/round-33/build-spec.json` (36 items, lines 7–297), the shared spec
context (spec line 5), `build-dispatch.json` + `build/swarm-registry.json` (reportDir
`.ufo/waves/round-33/build`), and every executable surface an item invokes. The falsify
wave (claims line 18: 36 build + 36 falsify) has no spec on disk yet — this review covers
the build wave, the only spec present.

## Method

Bounds tested per item: (a) writes confined to `.ufo/waves/round-33/**` (incl. assigned
`assimilation/` artifacts) + `/tmp/r33-*` scratch + the item's `Report:` path;
(b) no production edit (`corpus/**`, `SCORECARD.md`, `QUALITY.md`, `PROVINCE.md`,
`considerthese/**`, `plans/**`, `l0-questions.md`, lessons); (c) no fleet-repo write;
(d) no sibling or shokuknow write; (e) no git mutation. Read-only git
(log/show/diff/status/cat-file/archive) and read-only cross-repo reads are allowed by the
bounds. Every tool an item runs was opened and its write surface checked (evidence below).

## Item table

| # | Item | Role | Planned writes (all in scope) | Out-of-lane access | Scope |
|---|------|------|------------------------------|--------------------|-------|
| 1 | R33ReconPackage | scout | report only | READ shokuknow merge pkg, corpus/SOURCES.md | clean |
| 2 | R33ReconRegistry | scout | report only | reads corpus/SOURCES.md, README.md, PROVINCE.md | clean |
| 3 | R33CaptureToolathlon | executor | `assimilation/captures/toolathlon-…main.py` (assigned) | network curl to pinned raw file | clean |
| 4 | R33CaptureArxiv | executor | `assimilation/captures/arxiv-2412.05579v2-abs.html` (assigned) | network curl | clean |
| 5 | R33CaptureSwePro | executor | `assimilation/captures/swebench-pro-tests-test.sh` (assigned) | one GitHub trees API call + raw fetch (bounds allow exactly this) | clean |
| 6 | R33IdGuard | executor | `assimilation/{reg-ids,staged-ids,collisions}` (assigned) + `/tmp/r33-idguard/` fixture | READ shokuknow SOURCES.append.md | clean |
| 7 | R33RowDrafts | scribe | `assimilation/{append-rows.md,quotes.json,url-map.json}` (assigned); fallback fetch also into captures/; `sources_adopt.py --selftest` (hermetic, tmp) | READ shokuknow staged rows | clean |
| 8 | R33EntryPatch | scribe | `assimilation/entry-patched.md` (assigned) | read draft + captures; /tmp fetch if capture absent | clean |
| 9 | R33ReadmePatch | scribe | report only (paste-ready blocks; README edit is L1's) | — | clean |
| 10 | R33ScorecardPatch | scribe | report only (verbatim section text) | READ fleet `.ufo/reports/round-32/kengaku.md` | clean |
| 11 | R33Lesson31Err | scribe | report only (append block; lesson edit is L1's) | — | clean |
| 12 | R33Lesson30Err | scribe | report only | — | clean |
| 13 | R33FleetErrata | scribe | report only — "DRAFT ONLY; the L1 applies them via fleet-commit"; l0-questions line drafted in report | READ both fleet reports; `git cat-file -t` (read-only) | clean |
| 14 | R33EntryTruth | reviewer | report only; /tmp fetches | reads captures/committed draft | clean |
| 15 | R33CounterAttack | mutation-tester | `/tmp/r33-counterattack/`; exploits import the module, never edit it; `git archive f0b20aea` (allowed class) | reads fleet reports via N3/N4 defaults | clean |
| 16 | R33C1Counter | critic | `/tmp` only ("never edit lane files") | — | clean |
| 17 | R33C3Design | critic | `/tmp`; verify()/selftest on live tree are read-only | — | clean |
| 18 | R33ClaimsReview | reviewer | report only | — | clean |
| 19 | R33CensusWatch | executor | 5 receipts under `build/receipts/` | EXECUTES fleet `scripts/sources-census.sh validate` (read-only mode, see N3) + lane grader.py (tmp-only writes) | clean¹ |
| 20 | R33Connector | connector | report only | READ sibling PROVINCE.md/SKILL.md (read-only; "touch"=write) | clean |
| 21 | R33FrontierText | scout | report only | — | clean |
| 22 | R33C1KillRule | critic | report only | — | clean |
| 23 | R33ReportOut | scout | report only | — | clean |
| 24 | R33SeatLedger | scribe | report only | — | clean |
| 25 | R33MistakeMine | scribe | report only | — | clean |
| 26 | R33WaveBook | executor | report only | reads build/*.md | clean |
| 27 | R33ExecDefsBefore | executor | `build/receipts/defs-repro.txt`; `/tmp/r33-base/` from `git archive` (allowed class) | counter reads fleet reports (N3/N4 defaults) | clean |
| 28 | R33ExecVerifySelf | executor | `build/receipts/selftests.txt` | — (all selftests hermetic/read-only) | clean |
| 29 | R33SentinelScope | sentinel | this report | — | clean |
| 30 | R33SourcesAdoptDry | executor | `/tmp` registry COPY; conditional drafting of the assigned `assimilation/` artifacts; "do not write to the real registry" | — | clean² |
| 31 | R33CaptureVerify | reviewer | `/tmp/r33-capture-verify/` only | network re-fetch | clean |
| 32 | R33IndexTruth | reviewer | report only | — | clean |
| 33 | R33GraderSemantics | revenger | report only; /tmp fetch fallback | reads capture | clean |
| 34 | R33SurveyScope | critic | report only; /tmp fetch fallback | READ staged row | clean |
| 35 | R33L0Packet | scribe | report only (l0 append line + Q22 row drafted; application is L1's) | READ considerthese files | clean |
| 36 | R33GateMutants | mutation-tester | `/tmp` copies ("never write to the real registry") | — | clean² |

## Write-surface evidence for every executed tool

- `plans/sources_adopt.py` — main (lines 973–1085): quote-mode prints only; registry mode
  writes only via explicit `--out` (line 1075), otherwise stdout; `--selftest` builds
  fixtures under `tempfile.TemporaryDirectory()` (line 628). No lane write unless a seat
  invents `--out <lane path>`, which no prompt does (items 7/30/36 pin /tmp copies).
- `plans/state_check.py --selftest` — all fixture writes under tempdirs (lines 3819, 4140).
- `plans/round33_defects.py --selftest` — tempdir (line 180); N3/N4 selftest fixtures are
  synthetic precisely so the selftest does not touch live fleet paths (comment at 182–185).
  The `--lane` counter run itself is read-only; its N3/N4 read absolute fleet report paths —
  reads only.
- `plans/round31_c1_verify.py --selftest` — fully read-only (checks against
  `Path("/nonexistent-lane-31")`, lines 148–165). r32/r33 c1_verify and r31/r32 defects
  selftests: `TemporaryDirectory` present in each (r32_c1, r33_c1, r32_def, r31_def).
- `plans/catalog_probe.py` — `capture()` (lines 86–134) is the only mode writing
  `corpus/evidence/round33/catalogs/` (production); NO wave item invokes capture mode —
  item 17 uses `verify()` (line 163, "no network", reads committed bytes) and `--selftest`
  (tempdir, line 348). The production capture is L1 work.
- lane `grader.py` (item 19) — every write sits under `tempfile.mkdtemp` roots
  (`kengaku-r12-fixture-` 5313, `kengaku-r12-degenerate-` 5363, `kengaku-grader-selftest-`
  5526); the `IMPORT-SIDE-EFFECT.txt` open (line 4265) is inside `SYNTH_PROBE_SRC`, a
  fixture-module source string instantiated under those tmp roots. Main grade path: prints
  only.
- fleet `scripts/sources-census.sh` (item 19) — header lines 5–7: "Read-only: parses
  shokunin.conf LANES rows textually (never sources the conf), reads corpus/SOURCES.md,
  writes only stdout or --out". Item passes no `--out`. Executing a fleet script in
  validate mode is not a fleet write.
- Dispatch/swarm: all 36 `Report:` trailers resolve to
  `.ufo/waves/round-33/build/<Name>.md` (swarm-registry `reportDir` ditto). Existing wave
  artifacts (`assimilation/{append-block.md,append-package.md,captures/*,collisions,
  gate-receipts.txt,quotes-rows.txt,reg-ids,staged-ids,url-map.json}`,
  `build/receipts/*.txt`) all sit inside the allowed subtrees.
- Git: only `archive`, `status --porcelain`, `cat-file -t` appear — all inside the bounds'
  read-only class. No item runs add/commit/checkout/reset/push or any jj mutation; no item
  names `.ufo/state`, `watchdog.log`, `MANIFEST.json`, a lane index, or a sibling/shokuknow
  write.

## Residual notes (wording risk, none acceptance-forcing)

1. Items 3–5 accept "Capture file committed path + sha256" — "committed path" denotes the
   path destined for the L1's commit (captures dir is "committable" per context), not an
   instruction to git-commit. A literal-minded seat running `git add` would exceed scope,
   but no prompt instructs it and the shared bounds forbid it.
2. Items 30/36 guard the real registry by prompt text plus /tmp copies; the gate's only
   write flag is `--out`. Safe as routed; would break only if a seat invented a lane `--out`.
3. Item 19 executes a fleet-repo script — read-only by the script's own header, verified
   above; flagging so the L1 knows it was checked, not missed.
4. Items 28 and 26 carry a dispatch bounds line "no subagent dispatch except your single
   labrat" — an operator-granted spawn exception, not a write-scope change.
5. Observed tree state (not wave-produced): working tree already carries L1 integration
   edits (`corpus/SOURCES.md`, `corpus/README.md`, both knowledge entries,
   `plans/round33_c1_verify.py` modified; `corpus/evidence/round33/catalogs/` and
   `corpus/lessons/round-33.md` untracked) on tip 7895588. No build item is instructed to
   produce any of those; they are the L1's integration surface.

## Verdict

Every one of the 36 items writes only inside `.ufo/waves/round-33/**` (build reports,
assigned assimilation artifacts, captures) plus `/tmp/r33-*` scratch; cross-repo and
cross-lane access is read-only; every invoked counter/selftest/grader is hermetic or
read-only as run; git use is exclusively the allowed read-only class; the C3 production
capture and all production edits (registry, README, SCORECARD, lessons, QUALITY, fleet
errata, l0-questions) are L1-only and are merely drafted inside reports. No item's
acceptance can force an out-of-scope write.

VERDICT: scope-clean
