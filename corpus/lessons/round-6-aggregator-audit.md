# Round 6 — kengaku-shokunin aggregator audit (round-6 aggregate review lesson)

**Provenance:** auditor = aggregator L1, non-author of every entry audited (the aggregator lane wrote
only `corpus/lessons/round-{1,4,5}-aggregator-audit.md`). Date 2026-09-28, local clock 18:2x -03,
`date -u` → `Mon 28 Sep 2026 09:28:19 PM UTC`. Repo HEAD audited `f147a27` (`round-7`), equal to
`origin/master`. Audited delta: the committed tree at `f147a27` (rounds 5–7) plus the untouched
round-3/4/6 reports. Method: re-executed every count in `corpus/README.md`, a 14-row citation sample
across `corpus/knowledge/` and `corpus/lessons/`, a full cited-hash ancestry sweep
(`git merge-base --is-ancestor`), a byte diff of `SHONEN.md` against the canonical seed, and a
`git status --porcelain` classification. No lane file was edited; this lesson is a new entry (rule 9).

## Verdict

**Not conformant.** Failed rules: **7** (index row is a claim — `corpus/README.md` lessons table has 6
rows for 8 files), **9** (corrections are new entries — `LOG.md:9` was rewritten in place by the
lane's own round-7 amendment), **4** (counts carry their command — `bench-arena-round7-noise-n25.md:24`
carries a 12-denominator on a 25-draw probe whose own table fixes the count at 17).

Correction of a standing claim in this audit chain: the lane's round-7 report cites commit `85b22e3`,
which the lane then amended away (`48ecc88 → 85b22e3 → f147a27`, all three stamped
`2026-09-28 16:55:52 -0300`). `git merge-base --is-ancestor 85b22e3 HEAD` → exit **1**;
`git fsck --lost-found` → *dangling commit*. The three round-8 defects the lane closed **are** closed
in content (`bench-arena-round7-scaffold-ablation.md:57` now reads `13/15 with empty content`,
`:58` persists the observed `skill(name="min_stack")` pointer, `:110-112` decomposes the class as
1 scaffold (13) / 1 strategy-bound (06) / 6 noise) — but the closure is unverifiable from the cited
hash, and one closure (`22 → 25`) was executed by rewriting `LOG.md:9`.

## Re-executed citations

| claim (file:line) | command | observed | pass/fail |
|---|---|---|---|
| knowledge table 18 rows ↔ 18 files | `grep -oE '^\| \`knowledge/[a-z0-9.-]+\`' corpus/README.md \| wc -l`; `ls corpus/knowledge \| wc -l`; `comm` both directions | 18 / 18; empty diffs | pass |
| lessons table ↔ disk | same shape for `lessons/` | rows **6**, files **8**; orphans `round-4-aggregator-audit.md`, `round-5-aggregator-audit.md` | **fail (rule 7)** |
| `ledger-route-telemetry.md:3` `7,218 lines` | `wc -l ~/Projects/bounties/ledger/telemetry.jsonl` | **7224** (live surface, +6) | pass-at-write, drift |
| `ledger-route-telemetry.md:8` `n=7,202 events` + taxonomy | python `Counter` over the first 7,218 lines | 7,202 non-null `event` rows; listed 15 sum 7,123 + 79 tail; `dispatcher_tick 3680 / mission_parked 1188 / mission_dispatched 1167 / fleet_synced 249`; `model` key 1243; top `xai-oauth/grok-4.6:low` 621 | pass (exact) |
| `bailian-cli-telemetry.md:3` `4,274 records` | `wc -l ~/.bailian/telemetry.jsonl` | 4274 | pass |
| `LOG.md` round-1 `413 models` | `wc -l …/models.jsonl` | 413 | pass |
| `eval-design-digest-2.md:109` `25 files` | `grep -oE '[A-Za-z0-9._-]+\.md' \| sort -u \| wc -l` → 30; −5 self-refs | 25 | pass |
| `bench-arena-round7-noise-n25.md:24` `0/12 PASSes (discordance 0/25)` | file's own table `:13` `PASS/25 = 17` | 8 FAIL + 12 PASS = 20 ≠ 25 draws; 0/**17** | **fail (rule 4)** |
| `noise-n25.md:13,17` `17 (p=0.68)`, `21/30 (0.70)` | arithmetic | 0.680 / 0.700 | pass |
| `bench-arena-round5-battery.md:17` vs `:36` flip taxonomy | read both lines | consistent post-r7 sweep | pass |
| `round-5-aggregator-audit.md:22` llm-wiki frozen `e66e614` | `git -C ~/…/llm-wiki rev-parse HEAD` | `e66e614372ee…` (== HEAD) | pass, scope it |
| `round-5-aggregator-audit.md:65,68,70` `c5abaac`, `097c75e` | `git merge-base --is-ancestor <h> HEAD` in the **main** repo | exit 0 both | pass |
| `SHONEN.md` box count | `grep -c '^- \[' SHONEN.md` | 3 vs seed 4 | **fail (seed drift)** |

## Defects

**Major**

1. **Falsified count survivor (rule 4), owner kengaku.** Standing claim:
   `corpus/knowledge/bench-arena-round7-noise-n25.md:23-24` — "matches 8/8 FAILs and **0/12 PASSes**
   (discordance 0/25)". Falsified by the file's own table (`:13`: 09 → 17/25 PASS). Proof command:
   `sed -n '13p;23,24p' corpus/knowledge/bench-arena-round7-noise-n25.md`. Required correction form:
   an **appended** errata line in that entry (never an in-place number edit) stating `0/12 → 0/17`
   and naming the count source. Routed at round 9 as "`0/25` → `0/17`" — the on-disk falsified token
   is the PASS denominator `0/12`; the `0/25` discordance figure is consistent, so the routing line's
   wording should be corrected too.
2. **Append-only violation (rule 9), owner kengaku.** Standing claim:
   `LOG.md:9` (round-5 entry) reads "8/33 **status deltas** vs v2". The line was edited in place by the
   `85b22e3 → f147a27` amendment; proof: `git -C kengaku-shokunin diff 85b22e3 f147a27 -- LOG.md` →
   one `-`/`+` pair (`status flips` → `status deltas`), no annotation. The lane applied PROTOCOL's
   sweep-every-mention rule to an append-only file. Required correction form: an **appended** LOG
   entry naming the rewrite + the four in-tree count corrections it swept. Routed round 9 (protocol
   *D1 major*); still open.
3. **Orphaned citation (unresolvable closure), owner kengaku + protocol.** Standing claim:
   `.ufo/reports/round-7/kengaku.md:3` "Commit: `kengaku-shokunin@85b22e3`". Proof:
   `git -C kengaku-shokunin merge-base --is-ancestor 85b22e3 HEAD; echo $?` → **1**;
   `git rev-list HEAD | grep -c 85b22e3` → **0**; `git fsck --lost-found` → *dangling commit
   85b22e35f549…*. The main repo compounds it: `.ufo/reports/round-8/protocol.md:16,120` cites the
   even-earlier `48ecc88` (also dangling), so a **committed** main-repo artifact now points at a
   nonexistent ancestor. Required correction form: appended notes in the lane's next report/LOG
   naming `f147a27` as the live hash; the protocol lane records the retroactive-orphan rows.
4. **Index row regression (rule 7), owner kengaku (aggregator-authored files).** Standing claim:
   `corpus/README.md` lessons table enumerates the corpus. `round-4-aggregator-audit.md` and
   `round-5-aggregator-audit.md` exist on disk with **no row**; proof:
   `comm -13 <(grep -oE '^\| \`lessons/[a-z0-9.-]+\`' corpus/README.md | sed 's/.*lessons\///;s/`.*//' | sort)
   <(ls corpus/lessons | sort)`. Required correction form: two appended README rows in the existing
   column shape. Note both files are aggregator-owned *content* while the index is lane-owned — the
   lane is the writer, the aggregator supplies the row text.
5. **Missing axis artifact / unmet MISSION axis, owner kengaku (+ protocol for the AXES.md
   definition).** Standing claim: `MISSION.md:14` assigns kengaku `novelty + calibration`, and
   AXES.md says a lane's round is one axis-move recorded in `SCORECARD.md`. Proof:
   `ls kengaku-shokunin/SCORECARD.md` → *No such file*; `git ls-files SCORECARD.md | wc -l` → 0;
   `grep -n 'novelty' AXES.md` → **0 hits** while `MISSION.md:14` names it. The lane is in fact
   working that axis right now — `corpus/evidence/round9-fleet/prior-art.md:1` says "kengaku lane
   round 9 (**novelty axis**)" — with no place to score it. Required correction form: the lane creates
   `SCORECARD.md` (axes + evidence pointer + last-change round, `planned`, `retired`) declaring
   **calibration** (defined in AXES.md) and, for the second axis, one of: `novelty` added to AXES.md
   by the protocol lane, or an explicit sub-axis mapping recorded in the repo. A score for an
   undefined axis is not re-derivable.

**Minor**

6. Flip/delta taxonomy half-swept: survivors at `corpus/README.md:22`, `corpus/lessons/round-5.md:8`,
   `SKILL.md:168,311` vs "deltas" at `bench-arena-round5-battery.md:17,36` and `LOG.md:9`.
   Proof: `grep -rn 'status flips\|flipped status' corpus/ SKILL.md LOG.md`.
7. `ledger-route-telemetry.md:3` + `corpus/README.md:17` carry `7,218 lines` with a method, not a
   re-runnable command, and the live surface has drifted (7,224).
8. Evidence durability: 14 committed file-lines / 23 distinct `/tmp/...` tokens
   (`git grep -c '/tmp/' -- corpus SKILL.md LOG.md`; `git grep -ho '/tmp/[A-Za-z0-9_./-]*' … | sort -u | wc -l`).
   All seven `/tmp/bench-r*` dirs still resolve today, and the decisive numbers are pasted into the
   knowledge entries — so this is acceptable-as-labelled past debt, and a hard blocker for rounds 8–9
   (see below) once the r9 clause requires closure-resolvable pointers.
9. `SHONEN.md` non-canonical: 3 boxes vs the seed's 4 (the
   "Instructions executable by an agent without oral context" box is absent — this is the box the
   aggregator's refresh-3 promotion verdict flagged as unmet), prose appended inline to each box line,
   and all three `[x]` marks carry no named non-author verifier → **0/3 verified**, effectively `[~]`.
   Proof: `cmp` against a regenerated seed; `grep -c '^- \['` → 3.
10. Commit identity: 5/5 recent commits and `git config --local user.name/email` are the operator's
    personal identity (`Joao Pedro Veiga <jpveigao10@gmail.com>`), against PROTOCOL's
    `<lane>-shokunin` / `<lane>@shokunin.local` invariant that ROADMAP claims "kagi/kake/kumitate/
    kengaku already do". Fleet-wide, `git config --local user.name` is unset/wrong in all six repos;
    the invariant's assertion is false as written.
11. Round-8 material is uncommitted, unlogged, unreported: `.ufo/reports/round-8/kengaku.md` is a
    3-line stub ("Fleet-1 lane retired mid-round; work pushed") with no hash and no `SHONEN` heading;
    the actual round-8 work (78-cell planning-horizon harness) sits untracked in
    `corpus/evidence/round8-horizon/`; `LOG.md` has no round-8 entry (`tail -4 LOG.md` → round 7
    last). "Landed means committed" therefore fails for round 8 — and the round-8 report's claim
    "work pushed" is not supported by `git status --porcelain` today (`?? corpus/evidence/`).
12. Live round-9 provenance staleness (report in progress, not a committed defect): the round-9 probes
    recorded `md5sum corpus/evidence/round8-horizon/results.jsonl` → `01547cfaa8b5b0a28d27559e8be63bb0`,
    97,023 B vs `/tmp` `df154cb5…`, 125,577 B, and called the repo copy a different execution
    (`round9-fleet/probeA.md:11-12`, `probeB.md:7,130`, `probeC.md:29`). Re-executed 18:29 local:
    both copies now hash `df154cb524bf210782fb0f4a46fd1bdc`, 268 lines each, repo mtime `18:08:50`
    — the repo copy was replaced after the probes were written, so the recorded defect no longer
    reproduces while three probe docs still assert it. The round-9 closeout must reconcile (appended
    note or re-run) or the first committed copy of this material will carry a self-falsified claim.

## Fleet-2 axis-framework state (this repo)

- `SCORECARD.md`: **absent on disk and untracked** (`ls` → No such file; `git ls-files` → 0 lines).
  Same for the other three repos without any axis artifact; `kasegi` and `kake` have an *untracked*
  `SCORECARD.md`, so the fleet's axis ledger is currently **zero committed artifacts**.
- Contract fields present: none. `planned`/`retired`: none. Before→after record: none — no round in
  `LOG.md` frames itself as an axis-move (`grep -rn 'SCORECARD\|axis-move\|axis move' LOG.md SKILL.md
  corpus/README.md corpus/lessons/` → 0 hits).
- Declared axes: none; `matches_mission_axes` = false; the MISSION name `novelty` has no AXES.md
  definition, and the lane's round-9 evidence already uses that name (`prior-art.md:1`).
- Recommendation to declare: `calibration` (AXES-defined) + one second axis with an explicit
  evidence-backed definition; `novelty` needs a protocol-lane AXES.md amendment before it can be
  scored. The round-7 calibration move (ex-ante predictions vs observed: predicted ≥5/8 noisy,
  observed 2/8; over-trusted decode-parameter hypothesis) is recordable retroactively with the
  report/entry pointer.

## Routed-defect rows for the ledger

```
kengaku | 85b22e3 cited in round-7 report is orphaned (amended twice: 48ecc88→85b22e3→f147a27) | r6 | open | git -C kengaku-shokunin merge-base --is-ancestor 85b22e3 HEAD; echo $?  → 1
kengaku | 48ecc88 cited by main round-8 protocol report is dangling (round-8 report cites a pre-amend id) | r6 | open | git -C kengaku-shokunin fsck --lost-found | grep 48ecc88 ; grep -n 48ecc88 .ufo/reports/round-8/protocol.md → :16,:120
kengaku | corpus/README.md lessons table 6 rows vs 8 files (round-4/round-5 aggregator-audit rows missing) | r6 | open | comm -13 <(grep -oE '^\| `lessons/[a-z0-9.-]+`' kengaku-shokunin/corpus/README.md | sed 's/.*lessons\///;s/`.*//' | sort) <(ls kengaku-shokunin/corpus/lessons | sort)
kengaku | rule 9: LOG.md:9 round-5 entry rewritten in place by the r7 amendment, no correction entry | r9 | open | git -C kengaku-shokunin diff 85b22e3 f147a27 -- LOG.md
kengaku | noise-n25.md:24 "0/12 PASSes" on a 25-draw probe (own table: PASS/25=17) | r9 | open | sed -n '13p;23,24p' kengaku-shokunin/corpus/knowledge/bench-arena-round7-noise-n25.md
kengaku | flip/delta taxonomy: 4 survivor spots (README:22, lessons/round-5:8, SKILL:168,311) | r9 | partly | grep -rn 'status flips\|flipped status' kengaku-shokunin/corpus kengaku-shokunin/SKILL.md kengaku-shokunin/LOG.md
kengaku | no corpus/lessons/round-6.md for the round-6 landing | r9 | open | ls kengaku-shokunin/corpus/lessons
kengaku | SHONEN.md stale 3-box + inline prose + no non-author verifier (0/3 verified) | r8/r9 | open | grep -c '^- \[' kengaku-shokunin/SHONEN.md → 3 (canonical seed in PROTOCOL.md "The canonical `SHONEN.md` seed" block has 4 boxes; regenerate the seed with `<name>`=kengaku-shokunin and `cmp`)
kengaku | SCORECARD.md absent; no axis scores, no planned/retired, no before→after | r6 | open | ls kengaku-shokunin/SCORECARD.md ; git -C kengaku-shokunin ls-files SCORECARD.md | wc -l → 0
protocol | MISSION.md:14 assigns "novelty" but AXES.md defines six axes without it | r6 | open | grep -n novelty /home/vgpnk/projects/shokunin/AXES.md → 0 hits (exit 1); MISSION.md:14
kengaku | round-8 harness uncommitted/unlogged/unreported; r8 report is a 3-line stub | r6 | open | git -C kengaku-shokunin status --porcelain → ?? corpus/evidence/ ; cat .ufo/reports/round-8/kengaku.md → 3 lines ; tail -4 kengaku-shokunin/LOG.md → round 7 last
kengaku | commit identity = operator personal (JP Veiga) not kengaku-shokunin | r6 | open | git -C kengaku-shokunin log -5 --format='%an <%ae>' | sort -u ; git -C kengaku-shokunin config --local user.name
kengaku | 14 committed lines / 23 distinct /tmp tokens (durability clause; all /tmp/bench-r* still present) | r9 | open | git -C kengaku-shokunin grep -c '/tmp/' -- corpus SKILL.md LOG.md
kengaku | no report carries a SHONEN heading (r3–r8) — assessment disqualified as promotion evidence | r8 | open | grep -LE '^#{1,6} *SHONEN' .ufo/reports/round-*/kengaku.md
kengaku | r9 live: repo copy hashes df154cb5 (== /tmp) while probeA/B/C still assert 01547cfa | r6 | open | md5sum kengaku-shokunin/corpus/evidence/round8-horizon/results.jsonl /tmp/bench-r8/results.jsonl ; grep -n 01547cfa kengaku-shokunin/corpus/evidence/round9-fleet/probe{A,B,C}.md
```

## Absence sweeps

- No committed artifact cites `corpus/evidence/`: `git grep -n 'corpus/evidence'` in kengaku (exit 1)
  and in the main repo (exit 1); `grep -rn 'corpus/evidence' .ufo/` → no hits. The closure rule is not
  violated yet — the risk is latent (the untracked round-9 docs cite the untracked round-8 tree).
- No `SHONEN` heading in any kengaku report: `grep -LE '^#{1,6} *SHONEN' .ufo/reports/round-*/kengaku.md`
  → all six existing reports; fleet-wide `| wc -l` → 50 of 59 report files.
- No `LOG.md` entry for rounds 8–9: `grep -n 'round 8\|round 9' LOG.md` → 0 hits (exit 1).
- No axis-move framing anywhere in the lane's committed files:
  `grep -rn 'SCORECARD\|axis-move\|axis move' LOG.md SKILL.md corpus/README.md` → 0 hits.
- No `.gitignore` in the repo: `ls -la .gitignore` → No such file; `git check-ignore -v corpus/evidence/`
  → exit 1.