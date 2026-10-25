# R31DefR10 — routed defect R10: the round-30 falsify seat count (34 → 33)

Seat: `R31DefR10` (round-31 build wave, role reviewer, axis calibration). Leaf: no subagent, no
background job, no `ask`, no model passed, no `agent://all`. Lane writes: this file only. Scratch:
`/tmp/r31-R31DefR10/` (copies of two lane files plus one re-derivation script; well under 60 MB).
Read-only git only (`rev-parse`, `show`, `diff`, `status`, `log`, `ls-tree`); no lane file was edited
by me, and the lane counter was executed read-only (it opens no file for writing —
`grep -n "write_text\|open(.*['\"]w\|mkdir\|unlink" plans/round31_defects.py` → no output).

**Tree I measured.** HEAD `0883e72ef8474ca42ac1a54eb0273079f1507035`; worktree 13 modified paths at
first read (other seats in flight). The worktree moved under me during the pass — see §5 — so every
number below names the revision it came from.

## VERDICT

VERDICT: R10 is real and the wrong number is the lesson's `34`; the true round-30 shape is 36 build + 33 falsify = 69 seats (falsify roles: 12 scout, 8 reviewer, 5 critic, 5 executor, 1 connector, 1 mutation-tester, 1 revenger; 16/33 attack under the lesson's own reviewer+critic+mutation-tester+revenger+connector reading, 48%), corroborated by five independent counts (registries 36/33, dispatch tasks 36/33, assignments 36/33, seat reports 36/33, `yield.tsv` 69) against a `34` that no round-30 artifact holds, and the append-only erratum that fixes it is the `corpus/lessons/round-30.md:205-208` block now in the worktree, which re-derives `check_r10` green but is UNCOMMITTED, so R10 is green only in the worktree and still red at HEAD — the repair completes when that block is committed.

## 1. Which number is wrong, and where

Exactly one byte-run in the lane says 34, and it is the one R10 names:

| location | text | re-derived value |
|---|---|---|
| `corpus/lessons/round-30.md:3` | "Round shape: two v1 waves (36 build, 34 falsify)." | **34 is wrong → 33** |
| `corpus/lessons/round-30.md:162` (same file, §Wave accounting) | "Wave 2 (falsify) 33 seats, 16/33 attack roles (48% …)" | 33 ✓ |
| `LOG.md:784` | "Round shape: v1 wave 1 build (36 seats) + v1 wave 2 falsify (33 seats) = 69 seats." | 33 ✓ |
| `SCORECARD.md:1018` | "Round shape: two v1 waves, 36 build + 33 falsify seats (69 total)." | 33 ✓ |
| `.ufo/reports/round-30/kengaku.md:6-7` | "**36 build + 33 falsify = 69 seats**" | 33 ✓ |
| `.ufo/reports/round-30/kengaku.md:117-119` | "wave 1 36 (…); wave 2 33 (12 scout, 8 reviewer, 5 critic, 5 executor, 1 mutation-tester, 1 connector, 1 revenger) — 16/33 attack roles" | 33 ✓, mix ✓ |
| `corpus/lessons/round-30-verifier-spotcheck.md:39-44` | "the committed registries say build `members` = 36 and falsify `members` = 33 … The lesson's `34` is the outlier." | 33 ✓ |
| `corpus/lessons/round-30-verifier-spotcheck.md:194-195` (§5 item 8) | "`corpus/lessons/round-30.md:3` says "34 falsify" seats; the registries and the report say 33 (16 attack roles, 48%)." | 33 ✓ |

So: **the lesson's `:3` is wrong; the round-30 report and the non-author spot-check are right.** The
lesson is also internally inconsistent — its own `:162` says 33 — which is why this reads as a
transcription slip at the header rather than a disagreement about what a seat is.

`34` has no derivation anywhere in round-30's bytes. Measured, over the four artifacts that could each
plausibly have produced it:

- registry members: falsify **33** (single commit `623c1fc`; the count never changed —
  `git show <each round-30 commit>:….falsify/swarm-registry.json` → 33 for all twelve commits
  `623c1fc9 706ed3f2 501d0707 6f6d6c98 d0253c52 5cd92295 baa53e70 bdcd7bed a6a9b57a caf1e2b4 9af639c9 2dcf06c5`);
- dispatched `taskCall.tasks` entries: **33**, zero duplicate names;
- assignment keys: **33** (the harness `-3` suffix does not add an entry);
- seat-report files `*.md`: **33** at tip, and 28 / 31 / 32 / 33 at earlier commits — 34 at none;
- `grep -rn "\b34\b" .ufo/waves/round-30/*.json` → no seat-count occurrence.

## 2. Re-derivation command and output

Command (`/tmp/r31-R31DefR10/rederive.sh`, run from the lane root; exits 0):

```sh
python3 - <<'PY'
import json, collections, csv, glob
ATTACK = ("reviewer","critic","mutation-tester","revenger","connector")
for w in ("build","falsify"):
    reg  = json.load(open(f".ufo/waves/round-30/{w}/swarm-registry.json"))
    disp = json.load(open(f".ufo/waves/round-30/{w}-dispatch.json"))["taskCall"]["tasks"]
    asg  = json.load(open(f".ufo/waves/round-30/{w}-assignments.json"))
    roles = collections.Counter(m["role"] for m in reg["members"].values())
    attack = sum(roles[r] for r in ATTACK)
    print(f"{w}: members={len(reg['members'])} dispatch_tasks={len(disp)} assignments={len(asg)} "
          f"files={sum(1 for _ in glob.glob(f'.ufo/waves/round-30/{w}/*.md'))}")
    print("  roles: " + ", ".join(f"{r} {c}" for r,c in sorted(roles.items(), key=lambda kv:(-kv[1],kv[0]))))
    print(f"  attack(fleet {len(ATTACK)} roles)={attack}/{len(reg['members'])}={100*attack/len(reg['members']):.1f}%"
          f"  reviewer-only={roles['reviewer']}/{len(reg['members'])}={100*roles['reviewer']/len(reg['members']):.1f}%")
rows = [r for r in csv.DictReader(open(".ufo/waves/yield.tsv"), delimiter="\t")
        if "round-30" in "\t".join(r.values()).lower()]
b = sum(1 for r in rows if not r["seat"].startswith("R30Fx")); f = len(rows)-b
print(f"yield.tsv round-30 rows: build={b} falsify={f} total={b+f}")
PY
```

Output (verbatim):

```
build: members=36 dispatch_tasks=36 assignments=36 files=36
  roles: scout 10, reviewer 7, executor 6, scribe 4, critic 3, connector 2, mutation-tester 2, revenger 1, simplifier 1
  attack(fleet 5 roles)=15/36=41.7%  reviewer-only=7/36=19.4%
falsify: members=33 dispatch_tasks=33 assignments=33 files=33
  roles: scout 12, reviewer 8, critic 5, executor 5, connector 1, mutation-tester 1, revenger 1
  attack(fleet 5 roles)=16/33=48.5%  reviewer-only=8/33=24.2%
yield.tsv round-30 rows: build=36 falsify=33 total=69
```

Five independent sources agree on 36 / 33 / 69: the two registries, the two dispatch files, the two
assignment files, the 69 `*.md` seat reports (36 + 33, one per registry member, no orphan in either
direction), and `.ufo/waves/yield.tsv`'s 69 round-30 rows. `yield.tsv` also reproduces the registry's
falsify role histogram exactly (`scout 12, reviewer 8, executor 5, critic 5, mutation-tester 1,
revenger 1, connector 1`). Both waves sit inside the policy band (`scripts/hyaku/ufo-wave-policy.json:88`
"wave band … 32-64", `:89` `"waveMinLanes": 32`).

## 3. Role mix — the shape round 31's report should cite

Round-30 shape, canonical: **36 build + 33 falsify = 69 seats**.

| wave | scout | reviewer | executor | scribe | critic | connector | mutation-tester | revenger | simplifier | total |
|---|---|---|---|---|---|---|---|---|---|---|
| build | 10 | 7 | 6 | 4 | 3 | 2 | 2 | 1 | 1 | **36** |
| falsify | 12 | 8 | 5 | — | 5 | 1 | 1 | 1 | — | **33** |

**Attack-role share is convention-dependent, and round 31 must name the convention it cites.** Four
readings, all re-derived from the same registry:

| reading | roles counted | falsify | build |
|---|---|---|---|
| fleet reading used by the round-30 lesson (`:162`) | reviewer + critic + mutation-tester + revenger + connector | **16/33 = 48.5 %** (lesson's "48%" ✓) | 15/36 = 41.7 % |
| `R30FxDeadSeats.md:206`, labelled "reviewer+critic+mutation-tester+**sentinel**" | reviewer + critic + mutation-tester | 14/33 = 42.4 % | 12/36 = 33.3 % |
| `R30FxDeadSeats.md:206`, "narrower" reading | critic + mutation-tester + revenger | 7/33 = 21.2 % | 6/36 = 16.7 % |
| reviewer-only | reviewer | 8/33 = 24.2 % | 7/36 = 19.4 % |

Cite the first row if the round-31 report restates "16/33 attack (48%)": that is the only reading under
which the number is true, and it is the reading the lesson's own §Wave accounting declares.

## 4. The append-only erratum

`corpus/lessons/round-30.md` is treated as append-only by the frozen predicate (`plans/round31_defects.py:31`,
`:239-253`): `check_r10` refuses if `"34 falsify"` has *disappeared* from the file (`:248`
`retracted = text.rfind("34 falsify")` → `retracted < 0` is a defect), and then requires the literal
`"33 falsify"` to appear **after** the last occurrence (`:252`). Two mechanical consequences a rewrite
would violate and an append satisfies:

1. never edit line 3 — the retracted bigram must survive;
2. the erratum must contain the literal two-word run `33 falsify` *after* the last `34 falsify`, so an
   erratum that quotes the superseded header ("36 build, 34 falsify") must place its correction later
   in the same block. Wrapping the number as `**33**` alone is not enough.

**State at my first read (T1).** `python3 plans/round31_defects.py --lane .` →
`DEFECT R1 … R2 … R3 … R6 … R9 … R10 lesson-round-shape: no appended erratum corrects the falsify seat
count to 33` / `checks=10 defects=6` / `exit=1`. R10 was open.

**State at my second read (T2), after another seat appended `## Errata` at `:189-208`.** Same command →
`DEFECT R9 round30-seat-reports-committed …` only / `checks=10 defects=1` / `exit=1`; R10 is green.
The landed erratum item is `corpus/lessons/round-30.md:205-208`:

> "**Round shape (supersedes `:3`).** The header says "36 build, 34 falsify". The committed falsify
> registry holds **33** members (`.ufo/waves/round-30/falsify/swarm-registry.json` → `len(members) = 33`),
> the build registry holds 36, and the round report says 33; 33 falsify seats of 69 is the shape, with
> 16 of the 33 in attack roles. The `34` was a transcription slip, not a dispatch difference."

I checked that item against my own re-derivation rather than against the counter's verdict: 33 members ✓,
build 36 ✓, report 33 ✓, "33 falsify seats of 69" ✓, "16 of the 33 in attack roles" ✓ under the
lesson's own convention. It satisfies `check_r10` (I also confirmed the ordering mechanically on the
live file: `rfind("34 falsify") = 20121 < rfind("33 falsify") = 20324`). Its last clause mixes a
measured claim ("not a dispatch difference" — dispatch 33, assignments 33, files 33, no artifact holds
34: measured) with an inferred cause ("a transcription slip"): `[INFERENCE]`, harmless, but it is not a
measurement and should not be cited as one.

Before the block landed I verified the predicate was failure-capable and that a compliant erratum
passes, on copies outside the lane (`/tmp/r31-R31DefR10/lane-*`, each holding only `corpus/lessons/round-30.md`
and the falsify registry, `check_r10` called directly):

| fixture | `check_r10` |
|---|---|
| worktree lesson as of T1, no erratum | `'no appended erratum corrects the falsify seat count to 33'` (defect) |
| + my appended erratum, non-quoting form | `''` (pass) |
| + my appended erratum, **quoting** form ("The header line reads "two v1 waves (36 build, 34 falsify)" … the wave held **33 falsify** seats") | `''` (pass) |
| `git show HEAD:corpus/lessons/round-30.md` (committed bytes) | `'no appended erratum corrects the falsify seat count to 33'` (defect) |

**The one open thing in R10's scope is the commit, not the text.** The erratum is worktree-only at HEAD
`0883e72` (last row of the table above), so a reader grading the committed tree still sees R10 red. R10
closes when that `## Errata` block is committed with the round-31 landing; the frozen predicate is a
worktree read, so the counter alone cannot prove the commit happened — the committed blob is the proof.

## 5. Adjacent residues R10 does not cover (for the round-31 report, not claimed as fixed)

1. **`corpus/lessons/round-30.md:162` mislabels the narrower reading it points at.** The cell says "a
   narrower reviewer-only reading is reported in `.ufo/waves/round-30/falsify/R30FxDeadSeats.md`". That
   report's narrower reading is critic+mutation-tester+revenger = **7/33 = 21.2 %** (`R30FxDeadSeats.md:206`);
   reviewer-only is **8/33 = 24.2 %** and appears nowhere in it. The same line calls 14/33
   "reviewer+critic+mutation-tester+**sentinel**" — the falsify registry holds no sentinel seat, so the
   label overstates the roster (the arithmetic 14 is right: 8+5+1).
2. **`.ufo/reports/round-30/kengaku.md:35` says "33 seats produced 28 reports".** 28 was the file count
   at `623c1fc` (measured: `git ls-tree -r --name-only 623c1fc .ufo/waves/round-30/falsify | grep -c '\.md$'`
   → 28) and the wave ended at 33 files (`2dcf06c5` → 33). It is a snapshot, not a seat count, and the
   report's appended errata do not refresh it. Round 31 must not cite 28 as round-30's report count.
3. `R30FxDeadSeats.md:135` independently prints the same 33-seat falsify mix, so the registry is
   corroborated by a seat that audited it — no third-party count disputes 33.

## 6. Residual risk and verification gaps

- I did not land the erratum (lane write scope is this report only); the fix in §4 is verified as text
  and as predicate input, not as a commit. Until it is committed, R10 is red on committed bytes.
- `check_r10` cannot see a *second* wrong seat count elsewhere in the lesson or in the round-31 report —
  it is a bigram-ordering check over one file. My `grep -rn "34 falsify"` sweep covers the lane's
  markdown/JSON/TSV today, but a future restatement is invisible to the counter.
- The counter reads the **worktree** (`read(lane, LESSON)`), so any R10 green it prints before the
  round-31 commit is uncommitted evidence; this is the same class as R9's worktree read and is why both
  need a committed-blob test to be closure-grade.
- Attack-share percentages are exact ratios over registry `role` cells; they are only as good as the
  registry's role assignment, which no seat re-derived independently of the dispatch prompts.

## 7. Tool installs

None. `python3` 3.14.8, `git`, `awk`, `grep` were already present; no pacman transaction was attempted
(host-wide pause), no `uv tool`, no binary installed.
