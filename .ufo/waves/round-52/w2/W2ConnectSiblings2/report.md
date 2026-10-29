# W2ConnectSiblings2 — round 52, wave 2 (falsify) — sibling-overlap scan of the landed round

Seat: connector (leaf, read-only). Lane: kengaku (`/home/vgpnk/Projects/shokunin/kengaku-shokunin`).
Judged on: adjacency. Milestone: attack the landed grader-triage instrument (R52-C1) and the
gate-registry rows (R52-C2) — this seat scans *ownership*, it does not attack the counters.

## Verdict

No registered sibling lane owns any part of what round 52 landed:

- the whole-population Terminal-Bench 2.0 grader triage (R52-C1, including the per-test presence-only split);
- the R52-C2 registry rows (kengaku's own `SKILL.md` registry home, under the fleet §Gate standard);
- the presence-only-test finding as a *benchmark* finding.

Overlap is adjacency only: three sibling lanes already run a registry-completeness counter of the
same shape; two sibling lanes own adjacent methods (located-quote verification, the verification-fixture
craft); and the presence-only class is already recorded as a finding in three sibling lanes. Each of
these is a report-out, not a transfer of scope. The contested scope is listed in §3.

## 1. Landed state at scan time (read-only)

- Lane HEAD `87301ba` (`round-52: amendment A5 …`), branch as committed. The lane tree is dirty with
  uncommitted wave-2 artefacts (`.ufo/waves/round-52/w2/*`, `claims/c1-after.txt`, …). The wave-1
  connector observed HEAD `07ea208`; the tip has since moved. This scan is at `87301ba`.
- `git rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
- Frozen counters run read-only (`--lane .`; both write nothing outside `--work`/selftest temp dirs,
  verified by grepping their write calls):

| counter | measured at `87301ba` (working tree) | verdict |
|---|---|---|
| `plans/round52_c2_registry.py --lane .` | `ADVERTISED total=72` · `REGISTERED total=72 rows=74` · `MISSING 0` · `INCOMPLETE 0` · `ENTRY-MISSING 0` · `SELFTEST-UNBACKED 0` | `PREDICATE R52-C2 pass`, exit 0 (base was `REGISTERED 44`, `MISSING 28`) |
| `plans/round52_c1_grader_audit.py --lane .` | `TASKS total=89 records=89 classified=88` · `CAPTURES expected=184 present=183 mismatched=0` · `CLASS V1=2 V4=0 V2=53 V3=31 V0=3` · `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27` · `CANDIDATES total=29` · `CONFIRMED new=0 []` · `PRIOR-ART ok=False urls=0` · `LABELS agree=0 of 0` · `PREDICATE R52-C1 fail` · `A5 CAPTURES present+pinned_excluded=184 of 184` · `A5 TASKS classified+excluded=89 of 89` · `PREDICATE R52-C1-A5 fail` | literal R52-C1 fails at this instant: `CONFIRMED` and `PRIOR-ART` legs are not in the lane tree yet (`corpus/evidence/round52/confirmations.json` and `prior-art.md` absent; the W2 executors are still writing). The `183/184`, `88/89` figures are the expected A5 state. `presence_only_tests=33 / tasks=27` matches the A4 correction (not the retired 54/42). |

Receipts: `W2ConnectSiblings2/c1-landed.txt`, `W2ConnectSiblings2/c2-landed.txt` (next to this file).

## 2. Scan, question by question

### 2a. Grader-triage instrument (R52-C1) — who owns Terminal-Bench grader auditing?

No sibling claims whole-population TB2 grader triage or task-validity auditing.

- `kasegi-shokunin/PROVINCE.md:47-50` (`## Adjacent`) lists `kengaku — LLM evaluation and benchmarks` as reported-not-absorbed. Routes *to* kengaku.
- `kumitate-shokunin/PROVINCE.md:24` — its Terminal-Bench references are a topology study
  (`corpus/knowledge/multi-agent-coordinator-topologies.md`), and it says "kengaku evaluates agents, this lane arranges the seats". Not grader inspection.
- `souji-shokunin/census/round-31/waves/w2/SwarmConnector28.md:21` — souji's prior connector names the
  Terminal-Bench git-leak grader as kengaku-held ground ("a routing precedent, not a competing owner").
- `chousa-shokunin/PROVINCE.md:10-12` refuses model-quality and evaluation claims to kengaku.
- `tameshi-shokunin/PROVINCE.md:3-17` owns the *reusable verification-fixture craft* and explicitly refuses
  to own any sibling's gate code. Adjacent to C1's method, not to the TB2 population.

Adjacent method overlaps (report-out, not ownership change):

- **Located-quote verification.** chousa owns the claim-vs-source method (`chousa-shokunin/PROVINCE.md:5-8`),
  with `tools/quote-reopen.py` and `tools/capture-text.py --locate QUOTE`
  (`chousa-shokunin/SKILL.md:24,135,140`). R52-C1's A1 check is a plain substring test:
  `plans/round52_c1_grader_audit.py:316` — `quote not in grader.read_text(errors="replace")`. The method
  belongs to chousa; the TB2 application belongs to kengaku. chousa's locator normalises and reports
  offsets; kengaku's does not. Recorded as a method-level overlap; the frozen counter is not changed by this scan.

### 2b. Presence-only finding — is the class already owned?

The class (a test that passes on artefact presence alone) is recorded as a *finding* in three sibling lanes,
which meets tameshi's own admission rule for a general pattern (`tameshi-shokunin/PROVINCE.md:14-17`:
"admitted from evidence in TWO independent lanes before it is claimed general"):

- `kasegi-shokunin/LOG.md:1990` — round 44: the counter "was falsified … on presence-only predicates"
  (`wave2/R44W2Rev09.md`).
- `kasegi-shokunin/LOG.md:2008` — round 45 mined mistake M45 includes "presence-only counters".
- `kotoba-shokunin/LOG.md:2335` — round 47 falsify: "every OC rule is a whole-dump presence test … 25 of 42
  ids are witnessed by literal presence only" (`.ufo/waves/round-47/falsify/W2BlindArm.md`).
  Also `kotoba-shokunin/corpus/lessons/round-64.md:104` ("checks 2/3 presence-only").
- `chousa-shokunin/LOG.md:1707-1710` — round 45: a "citation-presence-only tool 1/3"; "the check proves
  presence, not entailment".

Not counted as a finding: `kake-shokunin/LOG.md:1089,1111` uses "presence-only" as a disclosed scope limit
of its own input and capability, not a finding about tests.

Ownership: the general craft is tameshi's to admit; the TB2 instance is kengaku's. The R52 instance
(per-test P1 split, `presence_only_tests=33` across `27` tasks at this tip) is evidence for tameshi,
not a general claim by kengaku.

### 2c. Gate-registry standard (R52-C2) — who owns "every advertised instrument has a registry row"?

- Fleet standard: `PROTOCOL.md:375-423` (`## Gate standard`). Its Registry bullet (`PROTOCOL.md:398-406`)
  says the schema is the section's and "a child lane's *registry home* is its own `SKILL.md`". R52-C2 fills
  kengaku's own `SKILL.md` registry and nothing else. Kengaku already routed a fleet-wide standard to
  protocol/integrator (`kengaku-shokunin/PROVINCE.md:140`).
- Three lanes now run a counter of the same shape, each its own implementation (duplicate concept, not
  duplicate ownership):
  - `kama-shokunin/tools/gate-registry-check.py` — occurrence + row-meaning grading over `tools/round<N>-*.py`
    and `.ufo/waves/round-*/count-*.py`; described as lane-internal in `kama-shokunin/PROVINCE.md:152-153`;
    registry home `kama-shokunin/SKILL.md:296`.
  - `kaidoku-shokunin/tools/round-45/c2-counter.py` — exact path equality over a frozen scope file
    (`tools/round-45/registry-scope.json`); a row for another tool does not satisfy a scope path.
  - `kengaku-shokunin/plans/round52_c2_registry.py` — advertised universe `plans/<name>.py` depth 1 plus evidence
    scripts cited as `python3 <path>`; four legs (missing, incomplete, entry-missing, selftest-unbacked).
- `kasegi-shokunin/SKILL.md:977-980` keeps its own 8-cell `Gates & probes registry`, with a row-presence limb
  in `corpus/instruments/r35-defect-closure.sh`. Same class, lane-local.
- Consequence: the fleet has no shared completeness counter. Whether one should exist is a protocol/integrator
  decision. Referral, not absorption.

### 2d. Clone and stray hazards observed (not sibling lanes; not acted on)

- `/home/vgpnk/Projects/shokunin/lane3` — not a sibling. `git -C lane3 remote -v` → `origin
  /home/vgpnk/Projects/shokunin/kengaku-shokunin`; `git -C lane3 rev-parse HEAD` → `297e17927ba9342a87ba27a48cc5270a001de7cb`
  (round 50). `grep -c lane3 MANIFEST.json` → `0`. The wave-1 connector also reports 12 `tb2-*-grader.md`
  copies there; I did not re-verify that count. Exclude from any sibling or population count; integrator to decide disposition.
- Fleet-root entries outside any lane, names only seen (`ls -la`): `D=` (dir, 2026-10-28 12:07), `ok` (dir),
  `o.bin`, `oldrep1.out`, `m-rev-vs-rev.py`. Contents not inspected; not kengaku's; flagged for integrator awareness.

## 3. Contested scope (recorded, not resolved)

| scope item | parties | status |
|---|---|---|
| TB2 grader population triage (R52-C1) | kengaku (owner); kasegi, kumitate, souji, chousa (route to kengaku) | uncontested |
| Located-quote method (A1 check) | chousa (method owner); kengaku (application) | method-level overlap; kengaku's counter unchanged |
| Presence-only test class | tameshi (general craft, two-lane rule met); kasegi, kotoba, chousa (own instances); kengaku (TB2 instance) | generalisation contested only; kengaku must not claim it general |
| Registry-completeness counter | protocol/integrator (fleet standard); kama, kaidoku, kengaku (lane instances) | duplicate concept; no ownership collision |
| kengaku's SKILL.md registry rows | kengaku | uncontested (`PROTOCOL.md:398-406`) |

## 4. Report-outs this lane must record in `PROVINCE.md` (append-only, dated; text for the L1 to adopt)

1. **R52 routing evidence — TB2 grader triage stays kengaku's.** Evidence: `kasegi-shokunin/PROVINCE.md:50`,
   `kumitate-shokunin/PROVINCE.md:24`, `souji-shokunin/census/round-31/waves/w2/SwarmConnector28.md:21`.
   Recorded, not absorbed.
2. **Located-quote method → chousa.** `chousa-shokunin/PROVINCE.md:5-8`; `chousa-shokunin/SKILL.md:24,135,140`.
   kengaku's A1 quote-in-bytes check is an application-level substring test (`plans/round52_c1_grader_audit.py:316`).
   Report-out to chousa; no change to the frozen counter.
3. **Presence-only test class → tameshi (craft admission).** Instances: `kasegi-shokunin/LOG.md:1990,2008`;
   `kotoba-shokunin/LOG.md:2335`; `chousa-shokunin/LOG.md:1707-1710`. kengaku supplies the TB2 instance
   (`presence_only_tests=33`, `tasks_with_presence_only=27` at `87301ba`) as evidence, not as a general claim.
   `tameshi-shokunin/PROVINCE.md:14-17`.
4. **Registry-completeness counters → protocol referral.** Three lane instances: `kama-shokunin/tools/gate-registry-check.py`,
   `kaidoku-shokunin/tools/round-45/c2-counter.py`, `kengaku-shokunin/plans/round52_c2_registry.py`. A fleet-shared
   completeness counter, if wanted, belongs to protocol (`PROTOCOL.md:398-406`). kengaku keeps its own registry home only.
5. **Stray clone and fleet-root entries → integrator awareness.** `lane3/` (origin kengaku, HEAD `297e179`, absent from
   `MANIFEST.json`); fleet-root `D=`, `ok`, `o.bin`, `oldrep1.out`, `m-rev-vs-rev.py`. Excluded from sibling and
   population counts.
6. **Landed-state note.** At `87301ba` the literal R52-C1 predicate still fails on the `CONFIRMED` and `PRIOR-ART` legs
   (confirmations/prior-art not yet in the tree). Recorded as in-progress, not as a finding about siblings.

## 5. Commands run (all read-only)

```sh
cd /home/vgpnk/Projects/shokunin
ls -d *-shokunin
grep -n -i 'terminal-bench|tb2|grader|…' <sibling PROVINCE/SKILL/AGENTS/MINT/SHONEN/README>
grep -n -i 'presence-only|literal presence|presence only' kasegi-shokunin/LOG.md kotoba-shokunin/LOG.md kake-shokunin/LOG.md
sed -n '1700,1710p' chousa-shokunin/LOG.md ; sed -n '43,52p' kasegi-shokunin/PROVINCE.md
sed -n '1,25p' kama-shokunin/tools/gate-registry-check.py ; sed -n '1,25p' kaidoku-shokunin/tools/round-45/c2-counter.py
sed -n '375,423p' PROTOCOL.md ; sed -n '14,17p' tameshi-shokunin/PROVINCE.md
git -C lane3 remote -v ; git -C lane3 rev-parse HEAD ; grep -c lane3 MANIFEST.json
cd kengaku-shokunin && git rev-parse --show-toplevel && git rev-parse --short HEAD
python3 plans/round52_c2_registry.py --lane .   # exit 0, PREDICATE R52-C2 pass
python3 plans/round52_c1_grader_audit.py --lane .   # exit 1, PREDICATE R52-C1 fail (CONFIRMED/PRIOR-ART legs pending)
```

Per-scan wall time: under two minutes for the counters and reads. No installs, no tools updated, no pacman.

## 6. Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ConnectSiblings2/report.md` — this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ConnectSiblings2.md` — the same report at the path the seat target names.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ConnectSiblings2/c1-landed.txt` — C1 counter receipt at `87301ba`.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ConnectSiblings2/c2-landed.txt` — C2 counter receipt at `87301ba`.
- Scratch `/fast/scratch/hyaku/kengaku-r52/w2-W2ConnectSiblings2/` — removed before yield (receipts copied above).

## 7. Attack outcome for this seat

Attack on the *ownership* of the landed round: **did not land**. No sibling owns the grader triage, the registry
standard for kengaku's rows, or the presence-only benchmark finding. Overlaps are real (§3) and each is routed as a
report-out in §4. The one live caveat is the in-progress literal C1 predicate, which is for the L1 and the critic seats
to rule on, not a sibling-ownership issue.
