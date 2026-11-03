# SiblingOverlap — kengaku round 64, wave w1 (connector seat)

Full deliverable with the per-sibling table, quoted evidence and all receipts:
`.ufo/waves/round-64/w1/SiblingOverlap/sibling-overlap.md`
Measurement receipts: `.ufo/waves/round-64/w1/SiblingOverlap/{greps.py,greps.txt,measure_final.py,measure_final.txt,current.py,current.txt,base_tip.py,base_tip.txt,trio_cmp2.py,trio_cmp3.json}`

Scope: read-only scan of all 20 sibling lane repos under
`/home/vgpnk/Projects/shokunin/*-shokunin/` (`kumitate-shokinin` is a stray empty
dir, not a lane repo); every sibling `PROVINCE.md` read in full before the greps.
No sibling file edited, no git mutation, no network, no port bound
(`ss -ltn | grep -E "5328|8080"` → no match, rc 1). Frozen claims read first:
`plans/round-64-claims.md` (freeze `859ac24f`, base `5f517fe`).

> **Method correction (recorded because it changes a number).** The first grep
> pass filtered sibling hits with `grep -v "^kengaku/"` — a prefix that matches
> no sibling path (the lane dir is `kengaku-shokunin/`), so kengaku's own bytes
> were counted as sibling hits. `greps.py` excludes the lane by its exact
> directory name and re-scans all 20 lanes; every number below is from
> `greps.txt`.

## Verdict Q1 — offline grader replay / gRPC-kv-store building / corpus freshness sweeps

**No sibling owns benchmark-grader offline replay or execution.** Grep receipt
`greps.txt` (pattern A, `graders/executed|executed17|graders/SHA256SUMS|test_outputs\.py`):
**12 files in 4 lanes** (kama, souji, tabi, tsukuroi), every one a *citation or a
/tmp filename listing* — e.g.
`kama-shokunin/.ufo/waves/round-58/w1/out/X04ScratchHygiene/tmp-c1-before.txt:993`
and `tsukuroi-shokunin/.ufo/waves/round-48/w2/TExecCounterB/tmp-listing-pre-run.txt:1474`
both merely name `tb2_test_outputs.py`;
`souji-shokunin/.ufo/waves/round-52/w1/S52connector01/evidence/01-sibling-term-sweep.txt`
lists kengaku's TB2 grader digests. Pattern E (154 files, 11 lanes): every
corpus-level hit is a different subject (`kagi-shokunin/corpus/lessons/round-27.md:114`
release-anchor ordering; `kaidoku-shokunin/corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:46`
firmware transform; `kama-shokunin/corpus/knowledge/ollama-evidence-replay.md`
Ollama capture replay; `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md`
lane-scope census). **No sibling owns gRPC/kv-store building:** pattern C
(`grpcio|kv[._-]store|kv-store-grpc`) → **3 files in 1 lane**, all
`tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/{host,official,stable}-extra-pkglist.txt`,
a **pacman package-list mirror** naming `python-grpcio 1.84.0-1`; pattern D
(`127.0.0.1:5328|localhost:5328`) → **0 files, 0 lanes**.
**kama overlap, flagged:** kama owns the serving
plane (`kama-shokunin/PROVINCE.md:3` "**Domain:** local model serving & endpoint
health — local LLM endpoints, baseURL"; `:10` "producer discovery & read-only
service inspection of local serving ports") but its registry holds only
`:8080`/`:34113` (`registry/endpoint-consumers.tsv:35-37`) and its boundary rule
is model-specific (`:43-45` "kama answers *'is the thing at this baseURL the
model this config believes it is, right now'*"). The C1 lane-built gRPC
kv-store server on `127.0.0.1:5328` is a benchmark fixture, not a model
endpoint — **no overlap on the object**; contested scope C-2 below is about the
port plane only. kengaku already refuses the serving plane
(`kengaku-shokunin/PROVINCE.md:25-26`).

## Verdict Q2 — grader-class census ground / trio-sweep pattern

**No sibling holds the grader-class census:** pattern B
(`network-service|grader-class|class_survey|class-survey`) → **3 files in 1 lane**
(tabi), all quoting kengaku's own round-63 git log
(`tabi-shokunin/.ufo/waves/round-57/scout/receipts/07-meter-red-kengaku.txt:20,26`).
The census is kengaku-only (`corpus/evidence/round62/class-survey.txt`,
`PROVINCE.md:893-912`), matching the prior round's finding
(`.ufo/waves/round-63/w1/SiblingOverlap.md:6-9`).
**The trio-sweep PATTERN is held by four siblings with four different rules** —
kumitate `scripts/sources-check.mjs:381-383` (first 5 lines, presence-only);
tsukuroi `tools/check-knowledge-header.py:9-27` (column-0, last occurrence
operative); chousa `tools/research-gate.sh:3606-3622` (before first `## `);
kengaku (12-line window, before first `## `, **in order**). Measured on the same
65 kengaku entries (`measure_final.txt`): red **29 / 28 / 28 / 40**;
kengaku's red set equals the frozen 29-entry list entry-for-entry
(`SET equal: True`). tameshi owns only the *method*
(`tameshi-shokunin/PROVINCE.md:3`, `:14-17` "Never edits a sibling's gate code");
chousa owns research method (`:3`, `:5-9`), not the trio rule.

## Contested scope — for the L1 to route, not absorb

- **C-1 trio rule is fleet-ambiguous.** After the frozen C3 append-only addendum
  on all 29, **0/29** flip under kengaku's rule, 3/29 under tsukuroi's, 0/29
  under kumitate's (`measure_final.txt`). "Trio-green" is rule-relative; this
  round's `red=0` must not be read as a fleet-wide green.
- **C-2 port plane.** kama's L0 line "L0 must approve any endpoint outside the
  declared local model registry … any other unregistered endpoint still needs L0"
  (`kama-shokunin/PROVINCE.md:63-65`; `.ufo/l0-questions.md:58` `kama | round-16`).
  Decide once whether a lane-authored benchmark fixture on an unregistered
  loopback port needs the same L0 note.
- **C-3 stale cross-lane pointer (report-only).** `kama-shokunin/PROVINCE.md:144`
  cites `kengaku-shokunin/.ufo/waves/round-31/w1/out/ConnSibling/overlap.md` —
  **absent** (`find .ufo/waves/round-31 -name "*overlap*"` → 0 hits; the real
  artifact is `.ufo/waves/round-31/build/R31ConnSibling.md`). Substance still
  holds; route to kama, do not edit from here.
- **C-4 C2 `_resolves` repair.** Sibling root-containment prior art exists
  (chousa `tools/build-spans.py:107`, kotodama `tools/source-audit-inventory.py:119`,
  kaidoku `tools/round-40/ledger-status.py:105`, mado `tools/mado-assessment.py:65`;
  kotoba skips absolute pointer tokens by rule
  `verifiers/check_report_pointers.py:60-61`). The `ESCAPE` finding id and the
  fail-on-escape verdict are kengaku-local; a sibling citing "the escape rule"
  must not inherit them silently.
- **C-5 a kengaku entry contests kama's province, and kama's round-64 wave-b
  scan has already routed it (concurrent, this round).** kama's own seat
  (`kama-shokunin/.ufo/waves/round-64/b/CN02SiblingOverlap.md:56` §3c row C1, `:70` §4)
  records kengaku's `corpus/knowledge/served-endpoint-identity-pin.md` building
  its own served-endpoint pin from tokenised `/proc/<pid>/cmdline` — "the same
  identity fact kama's C1 binds" — and routes it: "kengaku (C1): cite kama's
  binding for the served-endpoint identity; kengaku keeps its battery and pin
  fields." The entry is real and pre-dates this round
  (`corpus/knowledge/served-endpoint-identity-pin.md:1-3`, header
  `source: S178 … verified-at: 2026-10-28`; "owning process" row =
  `/proc/<pid>/cmdline`, tokenised). **Not absorbed here, and it does not touch
  C1/C2/C3** — that entry is a *served model endpoint* identity pin; the C1
  probe's server is a gRPC kv-store fixture.
- **Reported, not edited (frozen claims):** `plans/round-64-claims.md:181-182`
  says "two entries carry `verified-at` but fail the gate's … rule". Measured at
  the base tip (`git show 5f517fe…:<file>`, receipt `base_tip.txt`): **two**
  carry the *string*, but only **one** carries a column-0 `verified-at:` **key**
  outside the window (`corpus/knowledge/tb2-grader-vacuity-triage.md:13`; the
  other, `tb2-cancel-async-tasks-grader.md:74`, carries it inside a `Round-61
  verified-at: …` prose line). The 29-entry frozen list itself is confirmed
  exact.
