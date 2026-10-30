# R53ScribeQuality2 — round 53 wave 3, seat report (scribe)

Seat `R53ScribeQuality2`, role scribe, axes calibration + adjacency. Lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

**Lane tip I ran at:** `9ead4476bf55b1ea6490d0204b668195db4a4d1d`
("round-53: confirmations integrated (20 tasks, five wave-2 readers), wave-3 spec+dispatch
evidence"). The assignment named `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` as the build-time tip;
the lane advanced while I worked (that commit is its immediate parent), so I cloned fresh and
recorded the hash I actually ran at. The L1 reconciles.

---

## 1. What I did

Three drafting deliverables for the L1 to integrate, plus ten measured probes of the two round-53
counters and of the round-51 surfaces counter.

| deliverable | absolute path |
|---|---|
| Q43 criterion draft (QUALITY.md shape of Q42) | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/q43.md` |
| SKILL.md lines to add (decision table + error-pattern entry) | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/skill-notes.md` |
| PROVINCE.md note (one replacement line; the manifest decision) | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/province-note.md` |
| ten probe receipts (verbatim stdout) | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/` |

Nothing was written outside my seat directory. The lane tree was not edited (no `git add`,
`commit`, `checkout`, `reset`, `pull`, `stash` in the lane or the fleet repo); every mutation was in
a scratch clone under `/fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/`, which I removed before
yielding.

## 2. Exact commands

```sh
# clone (asserted top-level before anything else)
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  /fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/lane
git -C /fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/lane rev-parse --show-toplevel
#   -> /fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/lane
git -C .../lane rev-parse HEAD   # -> 9ead4476bf55b1ea6490d0204b668195db4a4d1d

# the two counters, at that tip
mkdir -p /fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/tmp
cd .../lane && TMPDIR=.../tmp python3 plans/round53_c1_triage.py --selftest
#   -> SELFTEST cases=47 failures=0
cd .../lane && TMPDIR=.../tmp python3 plans/round53_c2_tipstate.py --selftest
#   -> SELFTEST cases=52 failures=0
cd .../lane && TMPDIR=.../tmp python3 plans/round53_c1_triage.py --lane .
#   -> PINS ... ok / FREEZE clean=yes classifier_and_freeze_one_commit=yes /
#      ORACLE tests=305 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52
#      unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9) /
#      ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes /
#      CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 /
#      PRIOR-ART rows=0 / PREDICATE R53-C1 fail   (exit 1)
cd .../lane && TMPDIR=.../tmp python3 plans/round53_c1_triage.py --lane . --candidates
#   -> CANDIDATES never_read_tasks=28
cd .../lane && python3 plans/round53_c1_classify.py --selftest   # -> cases=83 failures=0
cd .../lane && python3 plans/round53_c1_classify.py \
    corpus/evidence/round52/graders/cobol-modernization/tests/test_outputs.py \
    corpus/evidence/round52/graders/pytorch-model-recovery/tests/test_outputs.py \
    corpus/evidence/round52/graders/torch-tensor-parallelism/tests/test_outputs.py
#   -> P1=2 P0=1 / P1=1 P0=4 / P1=1 P0=2 / TOTAL P1=4 P0=7

# the round-51 surfaces counter, at that tip
cd .../lane && python3 plans/round51_surfaces.py --lane .
#   -> REV 9ead4476… / MANIFEST … entries=20 sections=2 /
#      ROWS section="## Surfaces" rows=10 entries=10 uncovered=0 /
#      ROWS section="### Core" rows=10 entries=10 uncovered=0 /
#      PROBES run=20 present=13 absent=7 errors=0 / DRIFT 0 /
#      STALE 1 (SF20 http://127.0.0.1:1234/health -> Connection refused) /
#      NUMBER-DRIFT 1 (SF14 row claims 171, probe says SOURCES rows=186) /
#      UNCOVERED 0 / RESOLVE observed_present=13 floor=13 verdict=met /
#      PREDICATE R51-C1 fail   (exit 1)

# the two audits that a PROVINCE.md edit must not break (run in the edited clone)
cd .../provtest && python3 plans/round50_c2_audit.py --lane .
#   -> POINTERS total=299 paths=233 hashes=66 resolved=299 exists=221 superseded=3
#      never-landed=9 unresolved=0
cd .../provtest && python3 plans/state_check.py --summary
#   -> assertions=329 match=317 mismatch=1 superseded=6 offline_unverifiable=5
#      MISMATCH: P3c.box.4.pointer.1:12   (the pre-existing PROVINCE.md:129 pointer)

# the counts behind the PROVINCE replacement line
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md      # 186
grep -c '^| S[0-9]' corpus/SOURCES.md                                       # 186
git show 11e79380:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   # 171
git show 11e79380^:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  # 170
git show 11e79380:corpus/SOURCES.md | grep -oE '^\|[[:space:]]*S[0-9]+' | tail -1            # S178
git diff 11e79380..43438294 -- corpus/SOURCES.md | grep -oE '^\+\|[[:space:]]*S[0-9]+' \
  | tr -d ' |+' | sort -u | tr '\n' ' '        # S179 S180 … S193  (15 rows)

# the never-read / never-examined measurement
python3 -c "…"
#   candidates from .ufo/waves/round-53/claims/c1-candidates.txt : 28
#   of those, present in .ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json : 28
#   per-test records for those 28 tasks : 112

# scratch removal
rm -rf /fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2
```

Disk guard was consulted before the heavier passes (`sh scripts/hyaku/disk-guard.sh status` →
`/fast/scratch/hyaku` 42 % used, 466.0 G free — the same figure the wave-3 touch-run seat
reported). No ENOSPC was seen. Scratch removed at exit.

## 3. Measured numbers this seat established

| # | measurement | how | receipt |
|---|---|---|---|
| 1 | C1 `--selftest` = `cases=47 failures=0` at `9ead4476` | `python3 plans/round53_c1_triage.py --selftest` | (matches `.ufo/waves/round-53/claims/c1-selftest.txt`) |
| 2 | C2 `--selftest` = `cases=52 failures=0` at `9ead4476` | `python3 plans/round53_c2_tipstate.py --selftest` | (matches `.ufo/waves/round-53/claims/c2-selftest.txt`) |
| 3 | C1 at `9ead4476`: `PRIOR-ART rows=0`, `PREDICATE R53-C1 fail`, exit 1; `CONFIRM new_confirmed=20`; `ORACLE … disagree=0 per_label_agree=1.000` | `python3 plans/round53_c1_triage.py --lane .` | (the run in §2) |
| 4 | A red row declared with a **negative exit** (`exit=-9`, a signal death) is accepted as truthful: `mismatched=0 evidence_missing=0`, `declared_red=1 observed_red=1` | fixture: script `os.kill(os.getpid(), SIGKILL)`, ledger declares `exit:-9, state:"red"` | `probes/probe-A-negative-exit.txt` |
| 5 | A red row whose evidence is the **generic** `Traceback (most recent call last):` header passes the evidence leg: `mismatched=0 evidence_missing=0` | fixture: script prints that header and exits 1; ledger evidence = that header, reason 15 words | `probes/probe-B-generic-evidence.txt` |
| 6 | A **non-numeric `timeout_s`** in the ledger crashes the counter with an uncaught `ValueError` and **no `PREDICATE` line at all** | doctored ledger copy (`adoption-check.timeout_s = "2.5"`), `--only adoption-check` | `probes/probe-C-timeout-string.txt` |
| 7 | Editing the **PROVINCE.md prose alone** does not clear `NUMBER-DRIFT` (the counter compares the manifest's `count_claim`) | full `round51_surfaces.py` run in an edited clone | `probes/probe-F-province-prose-only.txt` |
| 8 | Editing the **manifest `count_claim` alone** clears `NUMBER-DRIFT` but leaves the PROVINCE prose at 171; the row still exits 1 on `STALE SF20` | same | `probes/probe-E-manifest-count-only.txt` |
| 9 | **Both** edits → `NUMBER-DRIFT 0`, `UNCOVERED 0`, still `PREDICATE R51-C1 fail` on `STALE SF20` | same | `probes/probe-D-both-edits-province-row-and-manifest-count.txt` |
| 10 | Adding one `### Core` row **without** a manifest entry → `UNCOVERED 1` (`### Core row line 113 has no manifest entry`), `ROWS section="### Core" rows=11 entries=10` | same | `probes/probe-H-core-row-no-manifest-entry.txt` |
| 11 | Adding the row **and** a manifest entry → `rows=11 entries=11 uncovered=0` | same | `probes/probe-G-core-row-plus-manifest-entry.txt` |
| 12 | A **committed** count fix makes the ledger row `round51-surfaces`'s declared evidence fragment vanish: `EVIDENCE-MISSING round51-surfaces fragment not in output`, `evidence_missing=1` | the fix committed in a scratch clone, then `--only round51-surfaces` | `probes/probe-J-ledger-evidence-after-committed-count-fix.txt` |
| 13 | The same fix **uncommitted** is not seen by the row (`clean=NO`, `evidence_missing=0`) | same, uncommitted | `probes/probe-I-ledger-evidence-after-count-fix.txt` |
| 14 | All **28** never-read candidates appear in round 52's machine receipt, with **112** per-test records | join of `c1-candidates.txt` against `.ufo/waves/round-52/w2/W2CritC1Reach/receipts/live_tests.json` | (script in §2) |

## 4. What each deliverable says

### `q43.md` — the Q43 criterion

Drafted in Q42's shape (`corpus/QUALITY.md:1133-1146`): one bolded requirement sentence, the
round's evidence, "Criterion for the next counter of either class" (a)/(b)/(c), `Limits`, `Lesson`,
`Supersedes`. It says:

* **against Q42(a)** — the forged-complete controls now live inside the counters (`cases=47`,
  `cases=52`), each case a complete-but-wrong world rather than a blank; the wave-1 attacks on the
  frozen counters all landed (C1's composite fixture printed `PREDICATE R53-C1 pass`; C2's route
  table has 29 rows of which 23 landed; the mutation seats killed 25/81 and 28/69);
* **against Q42(b)** — every trusted input is pinned by digest or by history, and the pin is
  *unreachable* (the classifier and its freeze file in one commit that is never touched; the eight
  label files and eight shards by sha256 in `plans/round53-c1-freeze.json`; C2's row set by the
  digest of the 75 frozen names `df38a8fc…d0a4` plus this round's rows, read from `--source`);
* **against Q42(c)** — the registry's truth is now an executed per-row fact (run 1:
  `mismatched=18 evidence_missing=1`; the wave-3 re-measure at `b1f79a5`: `mismatched=1`);
* **the three mandated limits** — independence of labellers is a protocol property (A1's own "Not
  changed" note; `per_label_agree=1.000` is a result to attack, not a proof); a green ledger row can
  be a gate that cannot fail (and my probe 5 shows the mirror: a red row whose evidence is a
  generic traceback header also passes); never-read is not never-examined (all 28 candidates and
  112 per-test records are in round 52's machine receipt, which the counter does not consult);
* **two further residuals I measured** — a negative/signal exit is accepted as a red verdict
  (probe 4), and a non-numeric `timeout_s` crashes the counter with no `PREDICATE` line (probe 6).

It claims nothing about round 53's admission: at `9ead4476` the C1 predicate is still `fail`
(`PRIOR-ART rows=0`) and the C2 predicate is still `fail` (one mismatch).

### `skill-notes.md` — the SKILL.md lines

Two proposals: a new `## Presence-only grader triage` section with two short decision tables (what a
grader's assertion reads → class → meaning; and what a triage result does *not* say → what to check
instead), to be appended at the end of the file after the round-44 section; and **item 20** in the
existing error-pattern list (`## Benchmark anti-patterns`, `SKILL.md:60`, items 1–19), covering the
three error classes round 53 named — classifier-vs-oracle, forged-complete controls, ledger
tip-state — in the list's own shape (bolded claim, the concrete failure, a parenthesised cite). The
note flags that the L1 may prefer three separate items 20/21/22 and that the text is written so each
clause lifts out on its own. Every command quoted exists in the tree and was run at `9ead4476`; no
registry row is added, because `round53-c1` / `round53-c2` are already registered at `SKILL.md:639-640`.

### `province-note.md` — the PROVINCE.md decision

**One change only**: `PROVINCE.md:113`, the "Public-literature registry" row, whose cell still
claims 171 SOURCES rows while the registry holds 186. The note prints the current row byte-for-byte
and the exact replacement line, with the provenance of every number in it (186 now; 171 at the
round-51 landing `11e79380`, 170 at its parent, last id `S178`; `S179–S193` added in round 52's
`43438294`).

It also states, with the grep, that **nothing else changes**: the classifier, the label files and
the ledger are not in PROVINCE.md, and adding a `### Core` row for them would make the round-51
counter report `UNCOVERED 1` (measured). The `STALE SF20` complaint (the round-51 successor endpoint
is down on this host) is explicitly **not** proposed for change this round — it is a host surface
this seat cannot re-verify and must not assert an `ABSENT` date for.

The note hands the L1 the decision it reserves: `plans/round51-surfaces.json` is a **frozen**
round-51 instrument (`plans/round-51-claims.md:24`), and `SF14.count_claim` is what the counter
actually reads — so the manifest edit is the L1's call. Measured: the PROVINCE prose edit alone
leaves `NUMBER-DRIFT 1`; the manifest edit alone clears it but leaves the prose lying.

**A scheduling consequence the note adds (probe 12/13):** landing a *committed* count fix makes the
tip-state ledger's `round51-surfaces` evidence fragment (`"NUMBER-DRIFT SF14 row claims 171, probe
says SOURCES rows=186"`) disappear from the row's output, and the C2 counter then reports
`EVIDENCE-MISSING round51-surfaces`. The ledger row must be re-declared **with** the count fix, not
after it.

**A second consequence, and the reason the replacement line is dated rather than final:** the lane's
working tree already carries **28 uncommitted SOURCES rows** from the wave-3 source seats
(`git status --porcelain corpus/SOURCES.md` → ` M corpus/SOURCES.md`;
`git diff corpus/SOURCES.md | grep -oE '^\+\|[[:space:]]*S[0-9]+'` → `S900 … S927`; the working-tree
count is **214** against HEAD's 186), and `.ufo/waves/round-53/facts.md` says the L1 assigns the real
ids from S194. So the number in the replacement line, and the manifest's `SF14.count_claim`, are the
count at the tip I measured — **the L1 must re-run the counting command at the landing tip and
substitute that number into both**. The row's own convention already demands it (the round-51
landing wrote "round 51: `grep -cE …` → 171", true at its own tip). The prose "171 at the round-51
base tip through S178, plus S179–S193" stays valid however many rows land after S193.

## 5. Out of scope / not done

* **Not landed.** I wrote drafts and receipts only; the L1 integrates. No `corpus/QUALITY.md`,
  `SKILL.md`, `PROVINCE.md`, `plans/round51-surfaces.json` or `plans/round53-tipstate.json` byte was
  changed by me.
* **The `STALE SF20` host surface** — not re-verified and not marked absent: the endpoint is the
  operator's, and this seat must not assert a host state nobody re-checked.
* **`STALE`/`ABSENT` marking policy for `PROVINCE.md:15`** — left to the L1/operator.
* **Prior-art pricing, the touch-run and the relabel seats** — other wave-3 seats; Q43 says
  `[pending]`-equivalent ("not shown able to fail until …") rather than asserting their results.
  The touch-run seat's own report (`C1TouchExecA.md`) records the run as blocked at bwrap mount
  setup, so no touch-run result exists to cite.
* **The `C1CritOracle2` / `C1MutCounter2` / `C2MutLedger2` wave-3 attacks** were still running when
  I wrote; Q43 states the wave-1 attacks and the amendments, and does not claim the wave-3
  re-attacks' outcomes.

## 6. Findings and conflicts for the canonical judge

* **Facts-file conflict (verbatim).** `.ufo/waves/round-53/facts.md:21` says
  "`C1CritCounterReach`: 13 routes"; the seat's own report enumerates **15** numbered routes
  (R1–R15), of which 11 were exercised on fixtures and 9 are marked `holds` (R12 is a negative,
  R13–R15 reading-only). My q43.md uses the report's own count and says so in a parenthesis. The
  L1 should reconcile the facts line.
* **Facts-file conflict (verbatim).** `.ufo/waves/round-53/facts.md:23` says
  "`C2CritLedgerReach`: 20+ routes"; the report's route table has **29 data rows**, of which **23**
  carry `**yes**` in the "Lands?" column. "20+" is consistent with 23 but understates the table.
* **`STALE SF20` was already stale before this round's landings** — the wave-3 surfaces scout
  attributes it to an operator-initiated stop of `lfm3-server.service` at 2026-10-29 07:58:02 -03,
  i.e. after round 53's wave-1/wave-2 measurements. My own runs at `9ead4476` reproduce the same
  `STALE SF20` line; I did not investigate the host cause (out of scope, and it is a host surface).
* **A C2 counter residual the wave-1 report flagged and A1 did not close**: route F1
  ("`timeout_s` as a string") — my probe 6 shows the ledger can still carry a non-numeric
  `timeout_s` and crash the counter with an uncaught `ValueError` and no `PREDICATE` line. The
  wave-1 seat had filed it as "fails, but noisily"; it is still noisy.
* **Two residuals the wave-1 report flagged as "the counter cannot close"** are now measured as
  *accepted*, not merely argued: the negative-exit route (E3) and the generic-evidence route (E1).
* **Concurrent working-tree growth (measured at write time).** `corpus/SOURCES.md` is modified in
  the lane working tree with 28 uncommitted rows (`S900 … S927`, placeholder ids for the wave-3
  source seats; the count is 214 against HEAD's 186). **Not my edit** — I never wrote to
  `corpus/SOURCES.md`; `git status --porcelain` shows ` M corpus/SOURCES.md` alongside the wave-3
  source seats' files (`.ufo/waves/round-53/integrate_sources.py`,
  `.ufo/waves/round-53/integrate_w3.py`). The consequence for my province note is that the
  `count_claim` and the row's stated count must both be re-derived **at the landing tip**, not
  copied from the 186 I measured.

## 7. Tooling

No tool was installed or upgraded; nothing was missing. No pacman transaction was attempted (the
orchestrator's pacman pause was respected). No `~/.local/bin` or other PATH directory was touched.
No credential-shaped string was written into any deliverable; the strings `TOKEN`/`KEY`/`SECRET`
appear in my notes only as the names of the environment variables the C2 counter scrubs
(`plans/round53_c2_tipstate.py:37`), not as values.

`tool:` the `read` tool truncates long single lines with a "…" and points at
`artifact://<id>:raw:<n>` for the full line; I used that path twice (to read the wave-1 q43 draft
and the C2 route table) and it returned the untruncated text as documented.

## 8. Files produced (absolute)

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2.md
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/q43.md
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/skill-notes.md
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/province-note.md
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-A-negative-exit.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-B-generic-evidence.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-C-timeout-string.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-D-both-edits-province-row-and-manifest-count.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-E-manifest-count-only.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-F-province-prose-only.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-G-core-row-plus-manifest-entry.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-H-core-row-no-manifest-entry.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-I-ledger-evidence-after-count-fix.txt
/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w3/R53ScribeQuality2/probes/probe-J-ledger-evidence-after-committed-count-fix.txt
```

Scratch `/fast/scratch/hyaku/kengaku-r53/R53ScribeQuality2/` was removed before this report landed.

Report: `.ufo/waves/round-53/w3/R53ScribeQuality2.md`
