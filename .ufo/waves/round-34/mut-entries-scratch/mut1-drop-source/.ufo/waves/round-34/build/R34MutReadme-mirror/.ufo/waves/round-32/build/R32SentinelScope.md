# R32 SentinelScope — scope-discipline review of the round-32 wave

Review date: 2026-10-25. Scope: build spec `kengaku-r32-build` (34 items,
`.ufo/waves/round-32/build-spec.json`), lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
fleet `/home/vgpnk/Projects/shokunin`. Read-only inspection; no tool installed/upgraded.

## Verdict

`VERDICT: scope-clean`

No item's acceptance requires a production edit. Every planned write stays inside the
lane's report dir (`.ufo/waves/round-32/build/`) or `/tmp/r32-*` scratch; nothing in the
instructions touches the fleet repo outside the (absent, L1-owned) round-32 report,
sibling repos, `.ufo/state`, `watchdog.log`, `MANIFEST.json`, or lane git indexes.

## Item-by-item planned-write check (34/34)

All "Acceptance" clauses deliver through the seat's own report (written under
`.ufo/waves/round-32/build/` per the build spec's `reportDir`) or scratch; none lands a
production byte. Scribe items name production paths only as *draft targets*, with the
acceptance line explicitly resolving to "your report contains the draft":

- [5] R32DraftEntry — target `corpus/knowledge/benchmark-grader-semantics.md`; acceptance
  "Your report IS the draft (paste it fully)". No write.
- [6] R32DraftRows — target `corpus/SOURCES.md` rows + S093 used-by edit; acceptance
  "Your report contains the two full rows and the S093 old->new cell diff". No write.
- [7] R32DraftLesson — target `corpus/lessons/round-32.md`; acceptance "Your report
  contains the drafted sections". No write.
- [8] R32DraftMistakes — target `corpus/lessons/round-32.md`; acceptance "Your report
  contains the table". No write.
- [9] R32DraftErrata — target fleet `.ufo/reports/round-31/kengaku.md`, lessons,
  registry cell; acceptance "Your report contains all four drafted texts verbatim".
  No write (append is L1's landing job per `plans/round-32-claims.md` R1 kill rule).
- [10] R32DraftScorecard — target `SCORECARD.md`; acceptance "Your report contains the
  drafted table". No write.
- [11] R32DraftReport — target fleet `.ufo/reports/round-32/kengaku.md`, explicitly
  "(fleet repo, read-only for you)"; acceptance "Your report contains the skeleton";
  placeholders `<LANE-TIP>`/`<REPORT-COMMIT>` "the lane fills them at landing". No write.
- [12]-[19] executors — all output to `--out` scratch block files, `/tmp/r32-*` captures
  and manifests, or scratch mirrors; no production path is written.
- [20]-[23] reviewers, [24]-[26] critics ("Do not modify anything"), [27]-[28]
  mutation-testers (scratch copies), [29] connector (read-only greps), [30]-[31]
  sentinels, [32]-[33] scouts — report-only.

## Instructions touching protected paths

- No prompt mentions `watchdog.log`, `MANIFEST.json`, or `.ufo/state` as writable; the
  only occurrence of these tokens is this seat's own prompt restating the ban
  (`build-spec.json` item 31).
- [4]/[14] run `scripts/sources-census.sh validate` (fleet script) with `--root`/`--file`
  — verified read-only: header `scripts/sources-census.sh:7` "writes only stdout or
  --out"; writes are confined to `emit()`/`out_sink()` (lines 94-95).
- [8] runs `git -C /home/vgpnk/Projects/shokunin status --porcelain` — sanctioned
  read-only git per context ("Read-only git (log/show/diff/status/cat-file) is fine").
- [29] scans sibling lane repos read-only (grep of SKILL.md/PROVINCE.md/corpus).
- [16] reads `/home/vgpnk/Projects/shokuknow` (declared read-only source) and fetches the
  cited documents via curl into scratch; no write to the source tree.
- [17] preflights the three counters on the live lane tree; verified all three are
  read-only against lane/fleet in their main paths: `plans/round32_defects.py` (reads
  files; `git rev-parse`/`git log`-style subprocess only, lines 58-61, 88),
  `plans/catalog_probe.py` (URL fetch + entry read, lines 74-91), `plans/adoption_check.py`
  (reads registry/README/entry). `plans/sources_adopt.py` writes only to its `--out`
  path (line 1075) and selftest temp dirs (lines 628-634, 784-909).

## Observed state (no mid-wave writes)

- Lane git: HEAD `6084cd3` (freeze-commit gate receipt), freeze commit `0d32691d`
  present, both pre-wave; `git status --porcelain` shows only untracked entries under
  `.ufo/waves/round-32/` — zero tracked-file modifications, zero mid-wave commits.
- Fleet: `round-31/kengaku.md` mtime 2026-10-25 06:07 (pre-wave); `.ufo/reports/round-32/kengaku.md`
  absent (L1 has not landed); `watchdog.log`/`MANIFEST.json` last touched by harness at
  09:35/09:40 (wave start), `.ufo/state` baselines likewise harness-set at setup.
- Peer reports already emitted this wave (`R32CatProbe.md`, `R32SrcS097.md`) sit inside
  `build/` and declare `/tmp`-only captures; `R32CatProbe.md:5`: "raw JSON saved under
  `/tmp/r32-R32CatProbe/` … no production files touched".

## Low-risk notes (not violations)

1. Item [11]'s phrasing "Draft the round report skeleton at .ufo/reports/round-32/kengaku.md"
   could be misread as a write instruction; it is immediately qualified by "(fleet repo,
   read-only for you)" and the acceptance ("your report contains the skeleton"). Keep the
   read-only qualifier if this prompt is reused.
2. Item [5] notes `.ufo/waves/round-32/QUALITY-BAR.md` does not exist — confirmed absent;
   bar is `corpus/QUALITY.md` Q1-Q21.
3. Reading the lane with `git status` refreshes `.git/index` stat cache (mtime
   09:43:42) — within the sanctioned read-only git envelope.
