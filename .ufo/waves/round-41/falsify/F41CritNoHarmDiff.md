# F41CritNoHarmDiff — no-harm diff, kengaku round 41 wave 2

Seat: leaf critic. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`.
Clone used for every number: `/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff/lane`
(`git clone -q --shared <lane>`, `rev-parse --show-toplevel` = `.../lane`, read-only use, no commit).
Range under test: `e50c134556b4ba48e29dc7ff364e90d6ef07a3f3` (round-40 tip) → `3d0058fbde484c9d6c23fd997d9ee09a0663bcdb` (wave-1 tip).
Lane HEAD is `d7c77895752a2a5f317fa22f2362416ada50a04b` (wave-2 dispatch); `git merge-base --is-ancestor 3d0058fb HEAD` → exit 0, and `3d0058fb..d7c7789` is 2 files / 917 insertions / 0 deletions, both `.ufo/waves/round-41/{falsify-dispatch,falsify-spec}.json`.

## 1. Removed lines — none, anywhere

```
$ git -C <clone> diff --numstat e50c134 3d0058fb | awk '{a+=$1;d+=$2;n++} END {print "files="n, "insertions="a, "deletions="d}'
files=400 insertions=36552 deletions=0
$ git -C <clone> diff --numstat e50c134 3d0058fb | awk '$2>0 {print}'
(no rows)
$ git -C <clone> diff --summary e50c134 3d0058fb | grep -v '^ create mode'
(nothing: no delete mode, no rename, no mode change)
$ git -C <clone> diff --numstat e50c134 3d0058fb | awk '{a+=$1;d+=$2} END{print "ins="a" del="d}'   # 74513c0..3d0058fb
ins=30252 del=0
```

`git diff --stat` tail: `400 files changed, 36552 insertions(+)` — no `deletions(-)` clause.
Summary count: `393 create mode` + 7 modified = 400.

**Every removed line in lane files outside `.ufo/waves`: zero.** (Zero inside `.ufo/waves` too.)
`git diff --name-status e50c134 3d0058fb -- . ':!.ufo' | awk '$1!="A"'` → exactly seven `M` rows, each with `deletions=0`:

| file | + | − |
|---|---|---|
| `SKILL.md` | 110 | 0 |
| `SCORECARD.md` | 127 | 0 |
| `corpus/QUALITY.md` | 106 | 0 |
| `PROVINCE.md` | 61 | 0 |
| `LOG.md` | 36 | 0 |
| `corpus/README.md` | 19 | 0 |
| `corpus/SOURCES.md` | 3 | 0 |

Arithmetic proof that each is a pure insertion (new length = old length + insertions):

```
$ for f in LOG.md SCORECARD.md PROVINCE.md corpus/QUALITY.md SKILL.md corpus/README.md corpus/SOURCES.md; do
    echo "$f old=$(git show e50c134:$f | wc -l) new=$(wc -l < $f)"; done
LOG.md old=1229 new=1265            1229+36=1265
SCORECARD.md old=1527 new=1654      1527+127=1654
PROVINCE.md old=468 new=529          468+61=529
corpus/QUALITY.md old=569 new=675    569+106=675
SKILL.md old=1030 new=1140          1030+110=1140
corpus/README.md old=499 new=518     499+19=518
corpus/SOURCES.md old=168 new=171    168+3=171
```

So no earlier round's *text* was rewritten: every pre-existing line survives verbatim.

## 2. Where the 462 inserted lines in those seven files land

`git diff -U0` insertion coordinates, in old numbering:

| file | insertion after old line | lines |
|---|---|---|
| `SKILL.md` | 594 | +4 (registry rows `round41-c1-mutants`, `round41-c2`, `constraints-probe`, `round-close-check`) |
| `SKILL.md` | 644 | +23 (Round-41 registry addendum) |
| `SKILL.md` | 1030 (EOF) | +83 (`## Scheduling-constraint TB2 grader — round 41`) |
| `corpus/README.md` | 73 | +1 (index row for the new entry) |
| `corpus/README.md` | 267 | +1 (coverage bullet) |
| `corpus/README.md` | 340 | +17 (§Frontier nested sub-bullet) |
| `corpus/SOURCES.md` | 136 | +3 (S122, S123, S124) |
| `LOG.md` | 1229 (EOF) | +36 |
| `SCORECARD.md` | 1527 (EOF) | +127 |
| `PROVINCE.md` | 468 (EOF) | +61 |
| `corpus/QUALITY.md` | 569 (EOF) | +106 |

Structural placement checked in the diff context, not assumed: the four SKILL rows are appended at the **end** of the registry table (last pre-existing row `db-wal-probe` stays at old and new line 594); the SOURCES rows follow S121 in id order; the README index row sits inside the `knowledge/` table; the §Frontier addition is a nested `  - *Partly discharged round 41 …*` bullet under the existing TB2 bullet, before `- **Contamination transparency cards**`. No table row, heading or sentence is split. `grep -nE '^## ' SKILL.md | sed 's/^[0-9]*://' | sort | uniq -d` → empty (no duplicate heading introduced).

## 3. Earlier instruments — untouched, and verdicts identical

**(a) No pre-existing instrument file was modified.**
```
$ git diff --name-status e50c134 3d0058fb -- 'plans/*.py' | awk '$1!="A"'
(empty)
```
Every round-41 plans/ file is an `A` (`battery41/{r_setup,r_run,r_ctl,r_map,s_usage,s_modes,s_exit}.py`, `constraints_probe.py`, `pkg-spec-r41.json`, `round-41-claims.md`, `round41_c1_verify.py`, `round41_c2_verify.py`, `routed_open.py`). `round_close.py`, `pkg_gate.py`, `order_check.py`, `ledger_tip.py`, `anchor_digest_check.py`, `tip_receipts.py`, `sources_adopt.py` and every `round3*`/`round4*_c*_verify.py` are byte-identical.

**(b) Frozen digests hold at the clone's HEAD (`d7c7789`), not just at the landing commit:**
```
$ for r in 41 40 39; do sha256sum -c .ufo/waves/round-$r/claims/frozen-digests.txt; done
round-41: plans/sources_adopt.py: OK … plans/order_check.py: OK            (11/11 OK, exit 0)
round-40: plans/ledger_tip.py: OK … plans/pkg_gate.py: OK                  (11/11 OK, exit 0)
round-39: plans/round37_c1_verify.py: OK … plans/round38_c2_verify.py: OK  (9/9 OK, exit 0)
```

**(c) Verdict-line diff `measure-baseline.txt` vs `measure-final.txt`** (24 `$ command` sections in both; verdict lines = `PREDICATE|checks=|MUTANTS total|MUTANTS-BY-TOOL|BATTERY fixtures|PINS|PINS-AFTER|ADVERTISED|ORDER RESULT|ROUND-CLOSE RESULT|receipts=|cases=`, paired section-by-section):

```
identical verdict blocks=21 changed=3
[0] round41_c1_verify   base PREDICATE C1 fail / survived=23 → final PREDICATE C1 pass / killed=23
[1] round41_c2_verify   base checks=8 defects=4 fail        → final checks=8 defects=0 pass
[23] round_close --round 41  base ROUND-CLOSE ERROR          → final ROUND-CLOSE PASS exit=0
```

Every **earlier-round** block is byte-identical, including the two reds that must not be mistaken for round-41 damage:
`round38 C1` `MUTANTS total=22 killed=21 survived=1` / `PREDICATE C1 fail` (pre-existing, both files) and `round38 order_check` `ORDER RESULT FAIL exit=1` (pre-existing, both files); `round40 C1 21/21 pass`, `round40 C2 defects=0`, `round39 C1/C2 pass`, `round37 C1 55/55 pass`, `round37/38/39/40 C2 defects=0`, `round36 C2 defects=0`, `anchor_digest_check rows=114 tokens=21 defects=0` → in the final run `rows=117 tokens=24 defects=0`, `census exit=0` in both, `tip_receipts receipts=27 byte_equal=7 differ=0 skipped=20` in both (baseline verdict lines at `measure-baseline.txt` 4, 28–33, 55–57, 66, 109–113, 133–135, 141–142, 148–149, 156–157, 159, 250, 258–260, 280–282, 371, 394–396, 416–418, 485, 541–543, 563–565, 573–575, 577, 681–682, 718–719, 723–725; final at `measure-final.txt` 4, 76–82, 103–105, 111–112, 114, 157–161, 181–183, 189–190, 196–197, 204–205, 207, 298, 306–308, 328–330, 419, 442–444, 464–466, 533, 589–591, 611–613, 621–623, 625, 729–730, 766–767, 778, 798–800).

I re-ran the census instrument myself against the clone to confirm the count change is a clean 114→117 / 47→48, not a duplicate:
```
$ python3 plans/anchor_digest_check.py --lane .
rows=117 tokens=24 defects=0        (rc=0)
```

## 4. The one thing that does move: line-number drift, and why it is not harm

Mid-file insertions shift later lines in `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`. I enumerated every `(SKILL|SOURCES|README).md:<line>` citation in the **old** tree outside `.ufo` and compared the cited line's content old vs new:

```
old-tree citation occurrences = 138   (git grep -nE '<pat>' e50c134 -- ':!.ufo')
affected (old content ≠ new content at the same literal line) = 47
  10  sibling-lane / third-party targets  (not this lane's file)
  27  frozen receipts and pinned fixtures (append-only history; no gate re-resolves them)
  10  live lane prose / comment           (every one already stale at e50c134)
  0   correct at e50c134 and wrong at 3d0058fb
```

**Sibling/third-party (10)** — the PROVINCE instrument table cites *other lanes'* SKILL.md, and two knowledge entries cite other repositories:
`PROVINCE.md:318`→`SKILL.md:1929` and `:319`→`:1975` (tameshi: `sed -n 1929p tameshi-shokunin/SKILL.md` = `| .ufo/evidence/round-18/defect-probes.py | probe |`; `1975p` = env-diff row), `:321`→`:618`/`:322`→`:623`/`:323`→`:622`/`:324`→`:616` (kumitate: 616 = `| gate-mutants | gate |`, 622 = `| bind-oracle | gate |`, 623 = `| cap-spawn | helper |`), `:332`→`:606`, `:357`→`mado-shokunin/SKILL.md:610` (prefix elided by the regex), `corpus/knowledge/tb2-git-leak-recovery-grader.md:299`→`laion/terminal-bench-2-1-apptainer-v1 README.md:107`, `corpus/lessons/round-31-verifier-spotcheck.md:67`→`v2/README.md:75-76`. The out-of-range pair is itself the proof that table means sibling rows.

**Frozen receipts/fixtures (27)** — `corpus/evidence/round10-fleet/*`, `round13-coverage/*`, `round14-fleet/*`, `round26-calibration/p3-oracle*.txt` (3×4), `round27-calibration/{final-suite.json,p4-final-mutants.txt}`, `plans/fixtures/r26/*`, `plans/fixtures/r27/p4_mutants/P4b.json`. These are captured outputs and pinned fixtures: they record the tree at their own round, no gate re-resolves them (`plans/pkg_gate.py` parses only its spec's captures; `tip_receipts` skips them as `no-committed-re-run-command`, `receipts=27 … skipped=20`).

**Live lane prose (10), each already stale before round 41** — a citation is "already stale" if the text it quotes stood at a different line at `e50c134`:

| cite | quoted text | actually at (old tree) |
|---|---|---|
| `plans/round-27-claims.md:23,:69` → `README.md:260` | "a separately designed parser-policy comparison remain[s] open" | old `README.md:346` |
| `plans/round-31-claims.md:23` → `README.md:250` | "Not deployment config, not runtime task validity…" | old `README.md:259` |
| `plans/round-32-claims.md:20` → `README.md:276` | "stays open for the other benchmarks' scoring code" | old `README.md:288` |
| `corpus/knowledge/benchmark-grader-semantics.md:16` → `README.md:276` | "the primary specs and scoring code for Terminal-Bench 2.0…" | old `README.md:288` |
| `corpus/knowledge/benchmark-grader-semantics.md:18` → `README.md:278` | "and for Toolathlon" | old `README.md:261,290,291` |
| `corpus/knowledge/webarena-config-projection.md:10` → `README.md:338` | "generated eval-time configs … remain open" | old `README.md:421` |
| `corpus/lessons/round-24.md:160` → `README.md:166` | — | the sentence *is* an erratum saying `:166` pointed at the wrong row |
| `corpus/lessons/round-16-recensus.md:38` → `README.md:117` | — | an audit sentence listing stale durable identities, not a pointer |
| `plans/state_check.py:377` → `README.md:283-285` | — | old `:283` = `## Frontier`; the erratum text is not there |

Command behind the "actually at" column: `git show e50c134:corpus/README.md | grep -nF "<quoted text>"`.

**Nothing that was correct became wrong.** The strongest counterexample I could construct is the round-35 receipt's doc pointer, which *was* right at `e50c134` (`doc=corpus/README.md:262` → "Terminal-Bench 2.0 task grader (one task)"). It is not damage because `plans/tip_receipts.py` **derives** that pointer at run time (`DOC_SOURCES = ("SKILL.md", "README.md", "corpus/README.md")`, line 75), and the measurement shows it re-derived cleanly:

```
baseline: receipt corpus/evidence/round35/tb2-grader-probe.txt … doc=corpus/README.md:262+SKILL.md:574
final:    receipt corpus/evidence/round35/tb2-grader-probe.txt … doc=corpus/README.md:263+SKILL.md:574
final:    receipt corpus/evidence/round41/constraints-probe.txt … doc=SKILL.md:596+SKILL.md:667
```

The two line numbers the round's own instruments cite are also untouched: `SKILL.md:573` (`sources-adopt` row, used by `round41_c1_verify.py:121 SK = "SKILL.md:573"` and `battery41/s_usage.py`) and `SKILL.md:581` (`ledger-tip` row, used by `ledger_tip.py:23` and `round40_c1_verify.py:173`). Verified line-by-line old vs new: 573, 581, 590, 591, 592, 593, 594 all `SAME`; first drift is at old 595. `grep -rhoE 'SKILL\.md:[0-9]+' plans/` in instruments yields only 573 and 581 (plus 611 inside the round-26 pinned fixture, which is anchored to `90a5ce8` and carries a whole-file pointer).

Atomicity: `git diff` reports only additions, so a quoting gate that byte-compares (`pkg_gate` P3/P4/P10, `round4*_c*_verify` V-checks) is structurally unaffected — and the final measurement confirms `defects=0` for rounds 36–41.

## 5. What holds, what breaks

Holds: zero deletions and zero rewrites in the round; seven modified docs grow only by appending/inserting rows and bullets at correct boundaries; the seven earlier-round counter blocks and every earlier predicate line are byte-identical between baseline and final; no pre-existing instrument file changed; all three frozen digest manifests verify at the clone's HEAD; the registry rows instruments cite by line are unmoved; the census/anchor counts move exactly 114→117 and 47→48 with `defects=0`.

Breaks (bounded, and I state it rather than round it to zero): the landing **does** shift line numbers past old 594 (`SKILL.md`), 73/267/340 (`corpus/README.md`) and 136 (`corpus/SOURCES.md`), which moves the literal target of **47** existing `doc:line` citations. All 47 are in classes that do not resolve at HEAD: 27 frozen receipts/fixtures, 10 sibling-lane or third-party paths, 10 live lane citations that were already off by 9–86 lines at `e50c134` (measured where their quoted text relocates; two are staleness audits rather than pointers). No gate reads them; the one derived pointer that is read (`tip_receipts` `doc=`) re-derives itself. So the drift is real, visible, and harmless — but it is *not* "no movement", and a future seat re-verifying a quoted `README.md:262` from the round-35 receipt will now land one line off unless it reads the final measurement instead of the baseline.

Not attributable to this round (checked so it is not misread as damage): `round38 C1 survived=1 (N21)` and `round38 order_check FAIL` are identical in baseline and final. The lane work-tree also carries untracked `.ufo/waves/round-41/falsify.ready*` files (wave-2 dispatch), which the P9 untracked check would flag only if a counter ran in the live tree; the final measurement's P9 ran in a clean clone (`untracked_in_clone=0`) and passed.

Smallest safe correction: none required for admission. If the L1 wants the drift retired rather than accepted, the lane's own idiom already exists — `state_check.py` resolves `SKILL.md` by heading text (`(1, "SKILL.md", None, "## Decision table — benchmark selection", 1)`) and `tip_receipts` re-derives — so the fix would be to convert the 10 live `README.md:NNN` refs to quoted-phrase or heading anchors, not to move lines back.

Scratch: `/fast/scratch/hyaku/kengaku-r41/F41CritNoHarmDiff` removed after copying `enum.txt` and the five scripts into `.ufo/waves/round-41/falsify/F41CritNoHarmDiff/`. No write outside that directory and scratch; no git mutation in the lane or the clone.

VERDICT: removed-lines-0-harm-0
