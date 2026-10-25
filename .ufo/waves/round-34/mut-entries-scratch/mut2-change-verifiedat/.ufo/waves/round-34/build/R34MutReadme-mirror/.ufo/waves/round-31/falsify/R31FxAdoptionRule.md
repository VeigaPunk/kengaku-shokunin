# R31FxAdoptionRule — assimilation-contract compliance attack (kengaku round 31, wave 2)

Seat: critic, leaf (no subagent dispatch, no production edits). Target: `kengaku-round-31.md` §6 item
10 (assimilation contract) checked clause-by-clause against what wave 1 produced and the L1 landed at
`dbb0736459e0540a169a6d421ec6231734547378` (helper commit, 2026-10-25T06:01:14-03:00).
Scratch: `/tmp/r31fx-adoprule/` (archived landed tree, reruns — well under 60 MB). No tools installed.

---

## Clause-by-clause verdicts

### 1. One theme — MET
Evidence: `corpus/lessons/round-31.md:10` "One theme — *how a benchmark's verifier actually runs*".
Only the verifier-execution entry is admitted; the two other themed staged entries are refused this round:
`terminal-bench-release-identity.md` ("a second theme … release identity") and
`benchmark-grader-semantics.md` ("third theme") at `round-31.md:19-20`.

### 2. 1–3 entries — MET
Exactly one package entry admitted:
`corpus/knowledge/benchmark-verifier-execution-model.md` (committed at `dbb07364`). Package staged 65
entries (`/home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md` "proposed knowledge entries: 65").

### 3. Rows only for admitted entries' citations; never bulk-append — MET
Registry delta 88 → 91 = exactly S092/S093/S100 (`git show dbb07364:corpus/SOURCES.md` row count 91).
Re-run on baseline `0883e72` registry with the 0–3-space extraction reproduces the saved 12-collision set
and adopted ids are disjoint (see clause 5). No staged row beyond the three adopted was appended
(S094–S099, S101+ absent; S087–S089 stay unused). The wholesale-append path was rejected in simulation
(`.ufo/waves/round-31/build/R31ReconRegistry.md:284-296`: Sim A → `EXIT=1`, `E03`-class id conflict on
staged S091, `E01` S093 fields=12, `E09` prose recheck, `E11` dangling used-by). Adopted rows carry
`status=mined`, `opened=2026-10-25`, `recheck=180d`, `used-by` = exactly the one admitted entry
(`git show dbb07364:corpus/SOURCES.md | python3` parse: S092/S093/S100 cols 8-11).

### 4. Per-entry PROVINCE and QUALITY gates — MET (with a disclosed Q2 bound)
- PROVINCE: `.ufo/waves/round-31/build/R31EntryScope.md` ran the surface + sibling-ownership check;
  it found the claims file's "runtime task validity" label is refused by `corpus/PROVINCE.md`, and the
  landing carries that correction: README frontier bullet "Not runtime task validity (PROVINCE refuses it)"
  (`git show dbb07364:corpus/README.md:253`).
- QUALITY: entry-level Q1–Q19 record in `round-31.md:70-85`. The staged entry initially failed 7 bar
  rows (Q1/Q2/Q3/Q4/Q5/Q6/Q7, `R31EntryScope.md` VERDICT NOT-ADMISSIBLE-AS-STAGED); the re-grounded
  landed entry fixes the triad, ≤25-word located quotes, falsifier, source labels, named extended entry,
  and the "partly observable" quote of an unlanded document. Self-disclosed residual: Q2's stronger
  reading (the 731-manifest sweep is a seat's measurement) — `round-31.md:84-85`.
- Gate records ≥1 admit and ≥1 reject with flips: `round-31.md:14-23` (admit: verifier-execution; rejects:
  judge-calibration-thresholds, card-publication-contracts — carried from round 30 — plus the two this
  round, each with a flip).

### 5. Collision check with the 0–3-space guard — MET
- Guard proof committed: `.ufo/waves/round-31/assimilation/guard/` — fixture `reg-indented.md` (indented
  `  | S002 |` row) + `staged.md`; column-zero pattern returns 0 collisions (`collisions-col0` empty,
  false green), 0–3-space pattern returns `S002` (`collisions-sp0-3`). Exactly the contract's guard.
- Real run: `reg-ids` (88) ∩ `staged-ids` (175) = `collisions` (12: S077–S086, S090, S091). I re-ran
  the extraction with the contract regex on the baseline registry: identical 12 (matches saved file), and
  S092/S093/S100 ∉ collision set → no renumbering needed, ids continue the registry append-only.

### 6. Scratch validation before append — MET (evidence at an alternate scratch path)
`R31ReconRegistry.md:274-343` documents a pre-append scratch lane
(`/tmp/r31-registry/simroot/kengaku-shokunin/` — real registry copy + rows inserted + entries stub):
Sim A (staged rows verbatim) → `sources-census.sh validate --file …` `EXIT=1` (E01/E09/E11); Sim B
(corrected rows: pipe-free, `opened=2026-10-25`, `recheck=180d`, used-by trimmed) → `EXIT=0`, 91 rows,
15 W04, before any append. I re-ran `validate --file` on the archived landed registry: exit 0, 15 W04,
`ok`. Round-end `validate --root` on the current tree also exit 0 (15 W04). Note: the contract's literal
mirror path `$A/validate/corpus/SOURCES.md` does not exist — the lane used `/tmp/r31-registry/simroot`.
Functional equivalent, documented; minor path deviation.

### 7. Quarantine of the register slice — MET
Re-derived the lane slice with the §10 awk from
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (read-only):
`S091 payload-absent`, `S105 payload-absent` — byte-matches the saved `.ufo/waves/round-31/assimilation/quarantine-slice`.
Verdicts per row recorded in `round-31.md:99-103` (neither appendable, neither cited this round,
`unreachable` ≠ fabrication, flip = a round that fetches payload and locates a quote).

### 8. considerthese — at most one unimplemented proposal — MET
Proposal 2 of `considerthese/2026-10-24.md` §Self-improvement suggestions 2 grounded as **QUALITY Q21**
(an entry whose source is a pinned revision names the pin in its `recheck:` line), with measured absence
5/40 (both greps) at `corpus/QUALITY.md:237-249` and `round-31.md:104-109`. Proposal 1 of the same file
was mined in round 30 (Q20), not this round. No other proposal was implemented this round.

### 9. Never write the source repo — MET (no contrary evidence)
`find /home/vgpnk/Projects/shokuknow/merge/kengaku -newermt 2026-10-24T23:35` → nothing (package untouched
since its build). No campaign-tool invocation (`renumber-staged.py`/`merge-plan.py`/`quote-lint.py`/
`absent-defect-register.py`) appears anywhere in the lane's plans/evidence. Shokuknow's recent commit log
shows only campaign-team/other-lane work. All round writes are inside the lane; the landing went through
the §4 helper (commit author/committer `kengaku-shokunin <kengaku@shokunin.local>`).

---

## What fell — findings

**F1 — the landed commit lacks its own round evidence (strongest finding).** `dbb07364` does NOT contain:
`.ufo/waves/round-31/assimilation/captures/` (six captured files + `SHA256SUMS.txt`),
`assimilation/adopted-rows.txt`, `assimilation/capture-url-map.json`, `assimilation/quarantine-slice`,
`corpus/evidence/round31/census-after.txt`, `corpus/evidence/round31/quote-mode-adopted-rows.txt`,
`corpus/evidence/round31/quote-mode-bound.txt`, `corpus/evidence/round31/defects-after.txt`,
`.ufo/waves/round-31/gate-receipt.txt`, and the falsify wave evidence (`falsify/`). All exist only as
uncommitted working-tree bytes created 06:00–06:05, *after* the 06:01:14 landing
(`git status --porcelain`, `git ls-tree -r --name-only dbb07364 -- corpus/evidence/round31/` shows 7 of
11 files committed). The lesson asserts these as committed evidence — "the captures are committed with their
digests at `.ufo/waves/round-31/assimilation/captures/`" (`round-31.md:11-12`) — and the quote-mode
re-derivation depends on the untracked captures. As landed, the claim "stored evidence fully re-derives
offline" (gate-receipt.txt:5) is not yet true of the commit. If the round ends without a follow-up helper
commit carrying these files, C1's evidential base and the Q20 receipt are partially unlanded. (Round is
mid-flight; a final commit may repair this — as of the landed commit, it is an open gap.)

**F2 — C1's frozen counter is not reproducible from committed bytes.** `plans/adoption_check.py --expect …
--census` run in the archived landed tree prints `entries=1 indexed=1 cited_rows=3 rows_present=3
rows_mined=3 usedby_ok=1 census=fail` and exits 1 (only the lane-cwd run prints `census=ok`). This is the
known path-derivation bug (`round-29.md` M93; Q20's own text) — not a contract breach, but it means the
claim's counting command cannot be independently re-run offline; the git-free second receipt
`plans/round31_c1_verify.py` does re-derive green (`checks=6 defects=0`, exit 0, archived tree).

**F3 — S100's count claim lacks a byte capture.** The committed capture set has no contents-API listing for
the 92 top-level entries; the count's provenance is `R31SrcS100a.md` (committed; observed 301→200 response,
ETag = pin's tree sha `ec7c02c7…`, 92 = 89 dirs + 3 files). The claim checks out, but unlike the other six
quotes it is not reproducible from committed capture bytes.

**F4 — minor path deviation (clause 6).** The contract-mandated mirror `$A/validate/corpus/SOURCES.md` is
absent; the lane's documented equivalent lived at `/tmp/r31-registry/simroot`. Same gate, different path.

---

## Survived under attack
- The 0–3-space collision guard (proven on an indented fixture; real run reproduced at 12 collisions on the
  baseline, adopted ids disjoint).
- The three adopted rows' consensus state (mined/2026-10-25/180d/used-by → exactly the one entry), quote
  spans (7/7 located in pinned captures; digests match `SHA256SUMS.txt`), and census validity (exit 0,
  archive and live; 15th W04 S100↔S079 disclosed in lesson and in the S100 row's scope cell).
- Quarantine slice (S091/S105 payload-absent, verdicts recorded), considerthese one-proposal rule (Q21),
  and no-writes-to-source-repo (no contrary evidence).

## VERDICT:
Every contract clause (one theme, 1–3 entries, citation-bound rows only, per-entry PROVINCE/QUALITY gates,
0–3-space collision guard, scratch validation before append, quarantine slice, considerthese one-proposal,
source-repo read-only) **survived**; the **landed commit `dbb07364` fell** on evidence completeness — its
captures, quote-mode receipts, census-after receipt, quarantine-slice, and Q20 gate receipt exist only as
uncommitted post-landing bytes, so the landed state does not yet carry the evidence the lesson cites, and
C1's frozen counter is not re-runnable from the commit (known path bug; covered by the git-free second
receipt).
