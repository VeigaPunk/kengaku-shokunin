# R53ScribeEntry2 — round-53 knowledge entry `corpus/knowledge/tb2-presence-only-triage.md`

Seat: `R53ScribeEntry2` (scribe, wave 3 of 3, leaf member — no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. L1 `KengakuR53`.

## What I did

Drafted the round-53 knowledge entry for R53-C1 as
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeEntry2/entry.md`
(28 KB), in the shape of `corpus/knowledge/tb2-grader-vacuity-triage.md` (first lines `source:` …,
`verified-at:`, `recheck:`; then the finding).

I read in full: `.ufo/waves/round-53/facts.md`, `plans/round-53-claims.md` (including amendments A1–A3),
`.ufo/waves/round-53/p1-spec.md`, the round-52 entry `corpus/knowledge/tb2-grader-vacuity-triage.md`, the
round-52 lesson, `corpus/QUALITY.md` (Q1–Q11), the wave-1 reports I cite, all five wave-2 reader reports
`w2/C1ConfRead{A,B,C,D,G}.md`, the wave-3 peer reports that had landed when I wrote, the two source scribes'
`rows.md`/`gate.md`, and the C1 counter and both counters' source.

**I did not read any label file before the counter's own merge logic was understood** — the eight
`C1Label*/labels.json` files were read only for the per-seat `Y` counts and for the merge re-derivation in the
`## Re-run` section; no label file was read to decide any per-task class in the entry (all per-task classes
come from `corpus/evidence/round53/confirmations.json` and the wave-2 reader reports).

## Lane revision I worked at

The build-time tip named in the assignment was `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`. The lane had
advanced when I started; every counter run in this seat is at:

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r53/R53ScribeEntry2/lane
git -C /fast/scratch/hyaku/kengaku-r53/R53ScribeEntry2/lane rev-parse --show-toplevel
  → /fast/scratch/hyaku/kengaku-r53/R53ScribeEntry2/lane
git -C /fast/scratch/hyaku/kengaku-r53/R53ScribeEntry2/lane rev-parse HEAD
  → 9ead4476bf55b1ea6490d0204b668195db4a4d1d  ("round-53: confirmations integrated (20 tasks, five wave-2 readers), wave-3 spec+dispatch evidence")
```

`9ead4476` is the tip I ran at and the tip the entry's `verified-at:` names. The L1 reconciles against
`b1f79a54`; the only delta between them is wave-3 evidence, and the C1 counter's output is byte-identical
across the two (it depends on `plans/`, `corpus/evidence/round53/` and the label files, none of which moved).

## Exact commands I ran

```
S=/fast/scratch/hyaku/kengaku-r53/R53ScribeEntry2
mkdir -p "$S"; git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel
git -C "$S/lane" rev-parse HEAD
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status

cd "$S/lane" && TMPDIR="$S/tmp" python3 plans/round53_c1_triage.py --lane .            # the scored C1 counter
cd "$S/lane" && TMPDIR="$S/tmp" python3 plans/round53_c1_triage.py --lane . --candidates
cd "$S/lane" && TMPDIR="$S/tmp" python3 plans/round53_c1_triage.py --selftest
cd "$S/lane" && TMPDIR="$S/tmp" python3 plans/round53_c1_classify.py --selftest
cd "$S/lane" && TMPDIR="$S/tmp" python3 plans/round53_c2_tipstate.py --lane . --dry
cd "$S/lane" && TMPDIR="$S/tmp" python3 plans/round53_c2_tipstate.py --selftest

# read-only git history checks quoted in the entry
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -- plans/round53_c1_classify.py plans/round53-c1-freeze.json | wc -l
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -- .ufo/waves/round-53/w1/C1LabelRevB/labels.json
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin merge-base --is-ancestor d40b7055 db90a6b7   # → exit 0

# python3 (stdlib only) — every derived number in the entry
#  · classifier histogram over classes-305.json  → P1 52 / P0 253; P1 tasks 41 of 88
#  · oracle merge from the eight labels.json      → 305 ids, two labels each, per-seat Y counts
#  · re-locate every confirmation quote in its own test span and on its stated line → 20/20 and 20/20
#  · candidate/confirmed set difference            → 28 candidates, 20 confirmed, 8 unconfirmed
#  · wave-3 relabel vs classes-305.json           → 80 ids (all 52 P1 + 28 P0), 0 disagreements
#  · shard coverage                                → every id in exactly 2 shards, one scout + one reviewer
```

**No `git commit`, `git add`, `git push`, `git stash`, `git checkout`, `git reset`, `git pull` or mutating `jj`
command was run in the lane or the fleet repo.** No fixture repository was created (nothing needed one). The
only `git` calls on the lane were `clone --shared` (read-only), `rev-parse`, `log`, `merge-base`, `ls-files`.

## Measured numbers (all re-derived by me, not copied)

| what | value | how |
|---|---|---|
| C1 predicate at `9ead4476` | `PREDICATE R53-C1 fail`, exit 1 | counter run in the clean clone |
| PINS leg | `captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184` | same run |
| FREEZE leg | `clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4` | same run |
| ORACLE leg | `tests=305 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)` | same run |
| ORACLE-CONTROL | `r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes` | same run |
| CONFIRM leg | `candidates_never_read=28 new_confirmed=20 rejected=0` | same run |
| PRIOR-ART leg | `rows=0 tasks_covered=0/20 known=0 new=0 urls=0 rejected=0` | same run |
| classifier histogram | `P1=52 P0=253` over 305 ids; `P1` in 41 of 88 tasks | python over `classes-305.json` |
| classifier selftest | `cases=83 failures=0` | `python3 plans/round53_c1_classify.py --selftest` |
| C1 counter selftest | `SELFTEST cases=47 failures=0` | `.ufo/waves/round-53/claims/c1-selftest.txt`; my run agrees |
| candidates | 28 never-read tasks (`CANDIDATES never_read_tasks=28`) | `--candidates` run + the committed receipt |
| confirmations | 20 objects, all `confirmed: true`, 5 reader seats × 4 tasks | `corpus/evidence/round53/confirmations.json` |
| confirmation quotes re-located | **20/20** inside their own test span; **20/20** on the stated line | my own script over the committed captures |
| unconfirmed candidates | 8 (`kv-store-grpc`, `large-scale-text-editing`, `mteb-retrieve`, `multi-source-data-merger`, `raman-fitting`, `rstan-to-pystan`, `video-processing`, `vulnerable-secret`) | set difference of the two committed files |
| label oracle shape | 305 ids, exactly 2 labels each, role mix 1 scout + 1 reviewer on **every** id; per-seat `Y` = 13, 11, 12, 16, 14, 15, 13, 10 (sum 104 = 2 × 52) | python over the eight `labels.json` + the eight shards |
| shard coverage | every one of the 305 ids is in exactly 2 of the 8 shards; each seat's file covers its shard exactly | python over the shards + the label files |
| freeze history | the classifier + freeze file have **1** commit each (`d40b7055`); the eight label files have **1** commit each (`db90a6b7`); `d40b7055` is an ancestor of `db90a6b7` | `git log` / `merge-base --is-ancestor` |
| wave-3 blind re-label | 80 ids (all 52 `P1` + 28 `P0`, 48 tasks), **80/80 agreement, 0 disagreements** with the frozen classes | python over `w3/C1RelabelRev{1..4}/labels.json` vs `classes-305.json` |
| C2 registry/ledger | `ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok`; `ARGV entry=74 selftest=4 help=0 help_limit=7.8` | `python3 plans/round53_c2_tipstate.py --lane . --dry` at `9ead4476` |
| C2 selftest | `SELFTEST cases=52 failures=0` | `.ufo/waves/round-53/claims/c2-selftest.txt`; my run agrees |

## The entry's content, section by section (and what it deliberately does not say)

- **`source:` lines** — 13 rows: the group-A source-scribe placeholders `T01`–`T12` (from
  `.ufo/waves/round-53/w3/C1ScribeSources2A/rows.md`, each with its URL, its located quote and its location,
  all re-opened by that scribe on 2026-10-30), the landed row `S184` (TB2 PR #53), the group-B placeholders
  `U15` (TB2.1 issue #242) and `U06` (TB2.1 issue #156) from
  `.ufo/waves/round-53/w3/C1ScribeSources2B/rows.md`, and one `[pending: S-id mapping — no SOURCES draft row yet]`
  for the Harbor reward-hacking page that the wave-3 literature scout `C1ScoutLitSrc` fetched but for which no
  SOURCES row exists yet. The entry carries the literal `[pending: S-id mapping]` markers the seat spec asked
  for; the L1 assigns the final `S…` ids from **S194**.
- **What the instrument now is** — a table: the written spec, the AST classifier (with its frozen sha256), the
  one-commit freeze and the strictly-later label commits, the eight-seat blind oracle over the eight shards, the
  digest pins, the counter and its selftest. Every row carries a located pointer (path + commit + printed counter
  line).
- **What the oracle measured (305/305, control 23) and what it cannot support** — the two counter lines
  verbatim; then five explicit "does not support" bullets: not a weak *grader*, only a weak *test function*; not
  end-to-end reward-hackability (no execution evidence exists); not a new *phenomenon* (the class is documented by
  the maintainers, by a benchmark-wide audit, by a filed-issue catalogue and by the maintainers' own 2.1
  test-change class); task-level novelty for only 6 of the 20 confirmed tasks; and the counter's inability to
  prove labeller independence.
- **The 28 never-read candidates** — the committed candidates file, the command that produces it, the
  `never_read_tasks=28` line, and the set difference (8 candidates still unconfirmed).
- **The 20 confirmations** — the five reader seats (naming `C1ConfReadE` as the seat that produced no report),
  the counter's CONFIRM line, my own re-location of all 20 quotes (20/20 in span, 20/20 on the stated line), and
  a 20-row table giving each task, the confirmed test and its line, the reader, **the sibling check that keeps
  that grader honest**, and the reader report. That column is the entry's own "a presence-only test beside a real
  content check is a weakness of that test" made concrete per task.
- **`[pending: prior-art verdicts]`** — used exactly where I have no number: the 12 confirmed tasks whose pricing
  seats (`C1PriceScoutA/B/E`) had not reported when I wrote. The 8 priced tasks are tabulated with their verdict,
  their deciding archive and the seat that priced them, and the two ratifications the L1 owes are named
  (`pytorch-model-cli`'s known/new reading, and `tune-mjcf`'s known-under-both-readings note).
- **The limits** — the three the seat spec named (presence-only beside a real content check; labellers are LLM
  seats sharing one written spec; the counter cannot prove labeller independence) plus five more I could locate:
  never-read ≠ never-examined (the round-52 `live_tests.json` receipt), no execution evidence, the one excluded
  capture, the prior-art leg being a negative claim, and the unmapped source ids.
- **`## Re-run`** — the frozen counting commands from the claims file for both claims, the counter selftests, and
  two runnable stdlib snippets that re-derive the classifier histogram + oracle merge and re-locate every
  confirmation quote. **I ran both snippets in the clean clone and they print `P1 52 P0 253` / `ids 305 two labels
  each True` and `quotes in own span 20 of 20`** — the commands in the entry are not aspirational.

## Known limits of this deliverable

1. **It is a draft, not a landed entry.** It sits in my seat directory; the L1 owns
   `corpus/knowledge/tb2-presence-only-triage.md`, its `corpus/README.md` index row and its coverage-map row
   (QUALITY Q7 requires all three to land together — I did not write either, since `corpus/` is outside my write
   scope).
2. **The prior-art section is partial by necessity**: 12 of 20 tasks are `[pending: prior-art verdicts]`. The
   pricing seats were still running when I wrote. If `C1PriceScoutA/B/E` report before the L1 integrates, those
   12 rows must be filled in and the "6 of 20" novelty sentence recomputed.
3. **The `[pending: S-id mapping]` markers are real**: the `T…`/`U…` ids are the two source scribes' own
   placeholders, and the two scribes number **independently** (`T01…T18` for group A, `U01…U28` for group B), so
   the L1's renumbering from S194 must not merge the two sets silently. The entry names which scribe each `T…`
   belongs to for that reason.
4. **The entry quotes the counter's own output for the C1 leg** rather than re-deriving the ORACLE merge
   independently; the merge *shape* (305 ids, two labels each, one scout + one reviewer per id, shard coverage) is
   re-derived by me in the `## Re-run` snippet, but the 305/305 and control-23 figures are the counter's.
5. **No touch-run evidence exists** at this tip (`C1TouchExecA` blocked at the bwrap mount stage), so the entry
   says so rather than implying the confirmations were executed.

## Files produced (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeEntry2/entry.md` — the entry
  draft (28 KB; every file I want kept is here).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeEntry2.md` — this report.

No other lane file was created or modified. The lane's working tree is unchanged by this seat except for the two
files above (both inside `.ufo/waves/round-53/w3/R53ScribeEntry2{,.md}`).

## Scratch and tooling

- Scratch `/fast/scratch/hyaku/kengaku-r53/R53ScribeEntry2/` held one `--shared` clone of the lane and a `tmp/`
  dir; **removed before yield** (the entry and this report are the only kept artefacts).
- Disk guard before the pass: `/fast/scratch/hyaku` 45 % used, 449.5 G free. No ENOSPC.
- **No tool was installed or upgraded** (python3 stdlib, `git`, `bash` only; nothing was missing), so no
  tool/version/channel record is owed. No pacman transaction was attempted (pacman is paused host-wide by the
  orchestrator's 2026-10-20 ruling).

tool: `bash` returned `Ran in a temporary shell while the session shell is busy with another command: session
variables and functions were unavailable, and nothing set here persists.` on several calls — this is a harness
notice, not a failure of the command; every command in this report was re-run or verified in a later call and
produced the output quoted.

## For the L1

1. The entry draft is ready to land at `corpus/knowledge/tb2-presence-only-triage.md` **with** its
   `corpus/README.md` index row and its coverage-map row (Q7) — I wrote neither.
2. **Fill the 12 `[pending: prior-art verdicts]` rows** when `C1PriceScoutA/B/E` report, and recompute the
   "task-level novelty for 6 of 20" sentence.
3. **Renumber the source ids from S194** — remembering that the two source scribes numbered independently
   (`T01…T18` group A, `U01…U28` group B), and that three class-level archives cited by the `phenomenon-new`
   prior-art rows (arXiv:2511.21654, arXiv:2608.23616v3, TB2 issue #74) have **no** SOURCES row yet.
4. **The C1 predicate still fails** (`PRIOR-ART rows=0`) and the C2 predicate still fails
   (`MISMATCH round53-c1 declared exit=0 observed exit=1`, because the C1 counter exits 1 while the C2 ledger
   declares it green). Both are the L1's to re-declare once the prior-art leg lands.
