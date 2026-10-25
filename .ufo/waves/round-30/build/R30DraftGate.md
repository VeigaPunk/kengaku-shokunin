# R30DraftGate — the round-30 `## Gate` block, reconciled to the landed tree

Seat: scribe, leaf. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Access date 2026-10-25.
No production edits: the only lane-tree file I write is this report.

## Behavior

1. Read the frozen authority (`plans/round-30-claims.md`), the shape/voice sources
   (`corpus/lessons/round-29.md` §Attempt 2 Gate and §Rejected candidates, `corpus/QUALITY.md`
   Q1–Q13, `MERGE-REPORT.md`), and the six returned source receipts.
2. Measured the staged package myself: anchor-quote word counts, row well-formedness, `used-by`
   multiplicity, tier spread, duplicate-target hashes.
3. Drafted the block, then re-derived every pointer because the tree moved under the round: the
   admission landed in the working tree (entry, six registry rows, README index and discharge rows,
   `QUALITY.md` Q20, `plans/round30_defects.py`, `corpus/lessons/round-30.md` with a Gate of its own).
4. Read `plans/gate_timing_check.py` (940 lines) to settle Q13's mechanics from its source rather
   than from anyone's description, including the falsify wave's registry, which then decided the
   shape of the admit row.
5. Rewrote `/tmp/r30-DraftGate/gate.md` against the current tree and against Q9 for every reject
   reason. The ruled-on rows the earlier draft got wrong are listed under §Corrections.

## Gates I ran (commands and outcomes)

| # | command | outcome |
|---|---|---|
| G1 | cell-split each staged row of `SOURCES.append.md` on the pipe character | 175 rows; **S093 = 12 cells, S101 = 15 cells**, both with an escaped pipe — round 29's malformed-row record reproduces |
| G2 | quoted-segment word count per staged anchor cell | S081 **30** (over Q3's 25), S082 11 + 17, S083 14 + 19, S084 3 + 1, S085 1-word runs, S086 1 + 1 |
| G3 | `used-by` split per staged row | S081, S084, S085, S086 each named a second entry **before the append**; the landed rows (G8) name the card alone, so the objection is resolved, not carried |
| G4 | `sha256` of both copies of `benchmark-task-validity-checklist.md` | staged 7 239 B `7b73f175…`; lane 12 643 B `2cd9dca5…` — the package copy is the superseded draft |
| G5 | tier scan of staged rows | two tier-C rows only: S145 (→`disclosure-vocabulary-bilingual.md`), S167 (→`card-publication-contracts.md`), and S167 mirrors staged S126 at `arxiv.org/abs/2606.09809` |
| G6 | grep the staged `judge-calibration-thresholds.md` for kappa and for kappa inside its three anchor cells | figures at `:40-42` (0.46 vs ceiling 0.84); **no kappa text in any anchor cell** |
| G7 | read the six source receipts `.ufo/waves/round-30/build/R30SrcS08{1..6}.md` | all targets located; S085 `http=200` after round 29's `HTTP 000`; S081's 30-word staged quote occurs **0** times in both HTML fetches, 22-word span at `:46`; S086 independently counted 0 S081–S086 rows pre-append |
| G8 | current working tree: `grep -c '^\| S' corpus/SOURCES.md`; registry cell dump for S081–S086 | **88 rows**; S081–S086 at `:107-112`, each `mined`, `opened 2026-10-25`, 11 cells, `used-by` = the card alone |
| G9 | read `plans/gate_timing_check.py` | Q13 mechanics, all four verified in source: candidate resolved as a path (`:314-317`); **only an admit row's reason cell is scanned** (`:330`); second wave = `falsify` or `wave-2` only (`:241-243`); each cited report needs existence, mode `100644`, a registry seat with an allowed role, an anchored `^VERDICT:` line (`:56`, `:360`) and the candidate path in its body (`:358`); the strings "falsify reports/seats/wave" in a reason cell are a generic reference and void the row (`:45`) |
| G10 | `ls .ufo/waves/round-30/falsify/` and per-file `grep -m1 '^VERDICT:'` | **`swarm-registry.json` only — no report files**, so no `VERDICT:` line exists anywhere in that wave |
| G11 | members of `falsify/swarm-registry.json` | 33 seats; the six cited reviewer/scout seats (`R30FxEntryCompleteSet`, `R30FxEntryQ1Q3`, `R30FxEntryQ4Q6`, `R30FxEntryQ7Q9`, `R30FxQuotes`, `R30FxRowsCensus`) are present with allowed roles; every `agentId` is `null`, which is not the entry's `writer: KengakuR30` |
| G12 | current tree markers | entry `corpus/knowledge/contamination-transparency-card.md` 15 779 B, triad `:1-9`, `writer: KengakuR30`, CG1–CG8 at `:73`; README index row `:65`, card frontier bullet `:274`, discharge `:275`; `QUALITY.md:198` Q20 landed; `corpus/lessons/round-30.md` exists with its own `## Gate` at `:6` |
| G13 | URL comparison, staged S120 against lane S001 | same document: stash S120 = `aclanthology.org/2026.gem-main.50.pdf`, lane S001 = `aclanthology.org/2026.gem-main.50/` |
| G14 | `test -d .github`; `grep -n author-observed LOG.md` | absent; `372: Receipts are author-observed, never non-author closure.` |

## Findings

1. **The round's admission is in the working tree, not in the staged package.** The entry, six
   `mined` rows, the README index row and discharge line, `QUALITY.md` Q20 and a round-30 lesson all
   exist as uncommitted changes. My block therefore reads the landed bytes and cites them; a Gate
   written against the staged package would have mis-stated Q1 (dates), the anchor quotes and the
   `used-by` cells.
2. **Q13's four mechanics, from the checker's own source** (G9), now govern the table's shape: the
   candidate cell holds the path and nothing else; citations live in the admit row's reason cell;
   only `falsify/` and `wave-2` count as a second wave, so a `build/` path is a reading pointer and
   never evidence; and each cited report needs an anchored `VERDICT:` line plus the candidate path in
   its body.
3. **The falsify wave has a registry and no reports** (G10). Every falsify path cited in the round-30
   lesson's admit row therefore fails `audit_admission` with "absent from commit tree", and the check
   prints "no cited, existing, returned second-seat report". My block keeps those citations —
   they are the correct paths and the registry backs their seats — and puts the obligation in a
   paragraph *below* the table, because the reason cell cannot say "falsify reports" without being
   read as a generic reference (`:45`).
4. **Q9 corrections applied (each a reviewer-raised or self-found wrong reason).**
   - The staged `used-by` collision on S081 was being argued as Q6. It is not: lane S005's cell names
     three paths, so multi-entry `used-by` is normal in this registry. The objection is dropped, and
     the landed append already corrected the cells (G8).
   - The 12/15-cell split of S093/S101 was filed under Q3. It is a row-schema property (11 cells,
     no escaped pipe), and it is now filed as such in the deferred row.
   - The README pointer moved: the card's frontier bullet is `:274`, not `:272`, and the discharge
     line is `:275`.
   - The entry's gate is **CG1–CG8**, relabelled precisely so it cannot be read as `QUALITY.md`
     Q1–Q8; my earlier row said "Q1–Q8 gate".
   - The round-6 union table is a *staged* file, so its pointer now carries the `staged` prefix; the
     entry itself records the same fact at `:136-137`.
   - The fleet report path for the register S105 verdict is marked "fleet path, not lane-relative" in
     its own cell instead of being passed off as in-tree evidence.
5. **A duplicate-source reject that the package's own duplicate table misses.** Staged S120 is the
   PDF of the paper the lane already holds as S001; the mitigation entry's second source S121 was not
   opened this round. Reject reason: Q6 on one document, two rows; Q2 on a one-source argument.
6. **Counts are now stated so they can be re-derived**: 175 staged rows less the six admitted = 169;
   65 staged entries less one admitted and four rejected = 60 deferred. The lesson's "63" is not
   reproducible from MERGE-REPORT's own numbers.
7. **The register slice is released, with the numbering hazard named.** The register's S091 is the
   NEC 技報 page under staged numbering, while lane `S091` is the ABC paper — the two must never be
   read against each other. S105's verdict is quote-present in the archived 200 snapshot per the
   fleet report, and the surviving defect is that round 29's lesson deferred the verdict instead of
   recording it.

## Corrections I recommend for the existing `corpus/lessons/round-30.md` Gate

I do not edit the lesson. Four cells disagree with the bytes:

| lesson cell | current lesson text | what the bytes show |
|---|---|---|
| register `kengaku round3 S105` (`corpus/lessons/round-30.md:23`) | "unverifiable, not a fabrication" | the fleet report records **quote-present**, with the hold-out quote in the 200 snapshot (`.ufo/reports/round-29/kengaku.md:60-62`); round 29's lesson deferred it — see §Conflicts |
| remaining entries row (`corpus/lessons/round-30.md:21`) | "63 staged entries" | MERGE-REPORT states 65; 65 − 1 admitted − 4 rejected = 60 |
| three reject rows' `read` column | cites only `.ufo/waves/round-30/build/R30DraftGate.md` | the primary evidence is the staged bytes (file:line) and the lane's criteria; a report about the block is not evidence for a reject |
| register `kengaku round2 S091` | "re-opened in round 29 and re-read this round" | round 29 opened it; this round's evidence is the fleet report's byte-43351 hand-check plus the quarantine slice. No round-30 fetch of the NEC page appears in the wave receipts |

## Conflicts — verbatim, for the canonical Rust judge

- `corpus/lessons/round-29.md:183`:
  "`| register \`kengaku round3 S105\` (\`payload-absent\`) | see the second hand-check verdict in the round report | the quoted Japanese text reads like a fetch-failure page; confirming it is the campaign register's unchecked family rather than a claim in this lane's corpus | a re-fetch that renders the article rather than an error page |`"
- `.ufo/reports/round-29/kengaku.md:60-62`:
  "`kengaku round3 S105` → **quote-present**; the quoted Japanese text is METI's WAF error shell returned to a bare client, and the row's hold-out quote is present in the 200 snapshot."
- `corpus/lessons/round-30.md:23`:
  "`|register \`kengaku round3 S105\` (payload-absent) | unverifiable, not a fabrication | …`"
- `corpus/lessons/round-29.md:228-230` against staged `judge-calibration-thresholds.md:75`:
  lesson: "it claims the pre-registered threshold is missing inward" / staged: "It does not claim that any specific kappa threshold is".
- Reviewer message of this seat's draft, `/tmp/r30-R30DraftGate/` reported empty while my own
  `ls` shows `gate.md` 13 443 B and an identical sha256 to `/tmp/r30-DraftGate/gate.md`; recorded as
  an environment observation, not a finding about the reviewer's work.

## Touched surfaces

- Written: `.ufo/waves/round-30/build/R30DraftGate.md`; `/tmp/r30-DraftGate/gate.md`;
  `/tmp/r30-R30DraftGate/gate.md`.
- Read-only: `plans/round-30-claims.md`; `plans/gate_timing_check.py:28-58,160-395`; `corpus/QUALITY.md`;
  `corpus/SOURCES.md:1-30,23,106-112`; `corpus/README.md:65,241,270-278`;
  `corpus/knowledge/contamination-transparency-card.md:1-9,13-166`;
  `corpus/knowledge/contamination-detection-and-transparency.md:1-100`;
  `corpus/knowledge/benchmark-task-validity-checklist.md` (bytes only, for the hash);
  `corpus/lessons/round-29.md:175-190,218-244`; `corpus/lessons/round-29-verifier-spotcheck.md:108-139`;
  `corpus/lessons/round-30.md:1-63`; `considerthese/2026-10-24.md:1-40`; `LOG.md:372`;
  `.ufo/waves/round-30/assimilation/{quarantine-slice,collisions,reg-ids,staged-ids}`;
  `.ufo/waves/round-30/falsify/swarm-registry.json`; `.ufo/waves/round-30/build-spec.json`;
  `.ufo/waves/round-30/build/R30SrcS081.md` … `R30SrcS086.md`, `R30CritC2.md`, `R30CritC3.md`, `R30ConnSibling.md`, `R30Considerthese.md` where read;
  `MERGE-REPORT.md`; `SOURCES.append.md`; `knowledge/corpus/knowledge/*` (staged entries);
  `lanes/kengaku/round6/DOMAIN.md:40-50`; `.ufo/reports/round-29/kengaku.md:56-70`.

## Out of scope / not claimed

- I fetched none of S081–S086; every source-level statement cites a seat receipt.
- I ran none of `plans/round30_defects.py`, `plans/sources_adopt.py --selftest`,
  `plans/adoption_check.py` or `plans/gate_timing_check.py`. My Q13 statements are read from the
  checker's source, not from a run.
- I did not create the falsify reports, the lesson, or any registry row; the block states those as
  landing obligations.
- No tool was installed or upgraded, so there is no tool row to record.

## Artifact paths

- `/tmp/r30-DraftGate/gate.md` — the reconciled block (sha256 `a4f60e21…e174`).
- `/tmp/r30-R30DraftGate/gate.md` — byte-identical copy under my scratch name.
- `.ufo/waves/round-30/build/R30DraftGate.md` — this report.
