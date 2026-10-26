# R43FlipCheck — a conditional Gate refusal must be resolved by a recorded flip check

Round 43, wave 1 (build + first falsifiers), executor seat. Mined mistake: round-42 **D3** — a Gate
reject's flip condition fired at landing and was not executed
(`corpus/lessons/round-42-verifier-spotcheck.md:37`, "D3 Gate flip condition fired and was not executed
(Dockerfile)."; routed as closure R2 at `:125-128`). Axes worked: **calibration** (does the check catch the
real defect and not only its spelling) and **operability** (one command, stable exit codes, a selftest that
shows both halves red and green).

Nothing frozen was touched. No lane file under `corpus/`, `plans/`, `SKILL.md`, `QUALITY.md` or
`PROVINCE.md` was edited; the tracked files `git status --porcelain` reports as modified (`PROVINCE.md`,
`SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, the fibsqrt entry) are other seats' round-43 work, and
my writes are only the untracked `.ufo/waves/round-43/build/R43FlipCheck*` tree.

## 1. What landed

| path (under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/`) | what |
|---|---|
| `.ufo/waves/round-43/build/R43FlipCheck/gate_flip_check.py` | the checker, stdlib only, 504 lines, sha256 `d849250da6b3815dba421d5a5763c6cff20662a80f7fcf95c1e2912dfd44bf1d`. Must land as `plans/gate_flip_check.py` for the commands below to run as written. |
| `.ufo/waves/round-43/build/R43FlipCheck/QUALITY-Q35-draft.md` | the next free criterion, **Q35** (QUALITY.md's last landed number is Q34, `corpus/QUALITY.md:759-822`). |
| `.ufo/waves/round-43/build/R43FlipCheck/SKILL-registry-row.md` | registry row `gate-flip-check` + a round-43 addendum paragraph, in the §Gate/probe registry's 8-column shape. |
| `.ufo/waves/round-43/build/R43FlipCheck/{selftest,runs,sweep,final}.txt` | receipts quoted below (all < 8 KiB). |

**Rule implemented** (the script's docstring is the contract, `:1-71`). `--lesson <path>` reads one lesson,
takes its `## Gate` section (level-2 heading, ended by the next level-1/2 heading), keeps the refusals —
table rows whose *verdict cell* says REJECT/REJECTED/REFUSE/REFUSED, and `- **Rejected:**` bullets — and
for each refusal takes its flip condition from either its own text (`Flip:`, `flips when`, `if … admit`) or
a companion line of the same section that names the refused candidate (round 30's "Flip conditions (one per
rejected candidate)" bullet list — the only place `flips when` actually occurs). Each obligation must be
resolved by a **later** line

    Flip check (round N): <item> — fired|not fired — <evidence>

where `<item>` is the refusal's id token (`S042`, `XO5`), else its first code span (`Dockerfile`), else its
leading words; the state is exactly `fired`/`not fired`; the evidence must be ≥2 words and not a
placeholder (`none`, `n/a`, `todo`, `-`, …); and N must not be smaller than the round in the file name.
`--` is accepted as the separator when the em dash is absent. Output: one
`FLIP line=<n> flip_line=<n> item=<item> shapes=<…> resolution=<line-state-round|unresolved:reason>` line
per obligation, one `FLIP-DETAIL lesson=<path> lesson_round=<n> refused_rows=<n> malformed_resolutions=<n>`
line, then `FLIPS total=<n> unresolved=<u>`. Exit 0 when `u=0`, **1 when `u>0`**, 2 on setup (unreadable
lesson, no `## Gate` section, argparse). `--selftest` builds 19 fixtures in a temp dir and runs the script
on each as a subprocess (red/green/setup each compared to its expected code).

## 2. Evidence

All runs use the round-43 envelope; every envelope line below ends `local_bin_content_before=328be01808ba022f
after=328be01808ba022f unchanged`, i.e. no `INVALID`, no PATH-dir content change while it ran.

### 2.1 `--selftest` — red and green on built fixtures

```
$ ENVELOPE ... -- python3 .../R43FlipCheck/gate_flip_check.py --selftest
ENVELOPE start 19:18:18 cwd=/home/vgpnk/Projects/shokunin
SELFTEST case=reject-flip-unresolved expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=reject-flip-resolved expect=green got=green total=1 unresolved=0 rc=0 ok
SELFTEST case=reject-flips-when-resolved expect=green got=green total=1 unresolved=0 rc=0 ok
SELFTEST case=reject-flips-when-unresolved expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=resolution-before-row expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=resolution-wrong-item expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=resolution-placeholder-evidence expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=resolution-thin-evidence expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=resolution-round-before-lesson expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=resolution-ascii-separator expect=green got=green total=1 unresolved=0 rc=0 ok
SELFTEST case=resolution-malformed-shape expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=admitted-row-with-flip-not-counted expect=green got=green total=0 unresolved=0 rc=0 ok
SELFTEST case=plain-reject-without-flip expect=green got=green total=1 unresolved=0 rc=0 ok
SELFTEST case=bullet-reject-flip-unresolved expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=bullet-reject-flip-resolved expect=green got=green total=1 unresolved=0 rc=0 ok
SELFTEST case=companion-flip-unresolved expect=red got=red total=1 unresolved=1 rc=1 ok
SELFTEST case=companion-flip-resolved expect=green got=green total=1 unresolved=0 rc=0 ok
SELFTEST case=companion-flip-unmatched-candidate expect=green got=green total=0 unresolved=0 rc=0 ok
SELFTEST case=no-gate-section expect=setup got=setup total=None unresolved=None rc=2 ok
SELFTEST ok=19/19
ENVELOPE end 19:18:20 exit=0 ...
```

10 red, 8 green, 1 setup. The reds are the discriminations the criterion needs: no resolution line; a
`flips when` refusal with none; a resolution placed *before* its flip statement; a resolution naming another
candidate; evidence `none`; evidence of one word; `(round 4)` in a `round-42.md`; a malformed state; a
rejected bullet with none; a companion flip with none. (The first run of the selftest, before the item
token and companion-pairing fixes, printed `SELFTEST ok=13/16` with three real failures — that run is why
the item derivation and the fixture table were changed; it is not the delivered evidence.)

### 2.2 RED on the landed round-42 lesson (the Dockerfile row)

```
$ ENVELOPE ... -- python3 .../gate_flip_check.py --lesson /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-42.md
ENVELOPE start 19:18:22 cwd=/home/vgpnk/Projects/shokunin
FLIP line=43 flip_line=43 item=README.md shapes=flip: resolution=unresolved:no-line
FLIP line=44 flip_line=44 item=Dockerfile shapes=flip:,if-admit resolution=unresolved:no-line
FLIP-DETAIL lesson=.../corpus/lessons/round-42.md lesson_round=42 refused_rows=2 malformed_resolutions=0
FLIPS total=2 unresolved=2
ENVELOPE end 19:18:23 exit=1 ...
rc=1
```

`refused_rows=2` is the two explicit REJECT rows; the two "Captured, not rows" rows (`:45`, `:46`) also
carry `Flip:` text but are not refusals and are deliberately not counted (named in the docstring).

### 2.3 GREEN on a scratch copy with the resolution lines appended

The scratch copy is `round-42.md` + a blank line + exactly these two lines:

```
Flip check (round 43): Dockerfile — fired — entry tb2-circuit-fibsqrt-grader.md:435-438 keeps the WORKDIR sentence; no S### row opened (round-42 D3)
Flip check (round 43): README.md — not fired — the entry cites no README-only sentence and no README sentence the tests contradict (round-42 D3)
```

```
$ ENVELOPE ... -- python3 .../gate_flip_check.py --lesson /fast/scratch/hyaku/kengaku-r43/R43FlipCheck/green/round-42.md
ENVELOPE start 19:16:30 cwd=/home/vgpnk/Projects/shokunin
FLIP line=43 flip_line=43 item=README.md shapes=flip: resolution=line:154:not fired:round=43
FLIP line=44 flip_line=44 item=Dockerfile shapes=flip:,if-admit resolution=line:153:fired:round=43
FLIP-DETAIL lesson=/fast/scratch/hyaku/kengaku-r43/R43FlipCheck/green/round-42.md lesson_round=42 refused_rows=2 malformed_resolutions=0
FLIPS total=2 unresolved=0
ENVELOPE end 19:16:32 exit=0 ...
```

### 2.4 The two copies differ by exactly the lines appended — per-obligation, not all-or-nothing

Only the `Dockerfile` line appended (`partial/round-42.md`):

```
ENVELOPE start 19:16:33 cwd=/home/vgpnk/Projects/shokunin
FLIP line=43 flip_line=43 item=README.md shapes=flip: resolution=unresolved:no-line
FLIP line=44 flip_line=44 item=Dockerfile shapes=flip:,if-admit resolution=line:153:fired:round=43
FLIP-DETAIL lesson=.../partial/round-42.md lesson_round=42 refused_rows=2 malformed_resolutions=0
FLIPS total=2 unresolved=1
ENVELOPE end 19:16:38 exit=1 ...
```

### 2.5 The round-30 shape (flip conditions in a companion bullet list)

```
$ ENVELOPE ... -- python3 .../gate_flip_check.py --lesson .../corpus/lessons/round-30.md
ENVELOPE start 19:16:39 cwd=/home/vgpnk/Projects/shokunin
FLIP line=18 flip_line=28 item=judge-calibration-thresholds.md shapes=flips-when resolution=unresolved:no-line
FLIP line=19 flip_line=30 item=contamination-mitigation-comparative-evidence-2026-10-23.md shapes=flips-when resolution=unresolved:no-line
FLIP line=20 flip_line=32 item=card-publication-contracts.md shapes=flips-when resolution=unresolved:no-line
FLIP-DETAIL lesson=.../corpus/lessons/round-30.md lesson_round=30 refused_rows=5 malformed_resolutions=0
FLIPS total=3 unresolved=3
ENVELOPE end 19:16:40 exit=1 ...
```

Round 30's fourth flip bullet (`round-30.md:34`) is phrased imperatively — "flip one entry at a time under
CORPUS rule 4" — not conditionally, so it is not counted; that is named as a limit, not silently dropped.

### 2.6 The class is 45 obligations wide and every one is unresolved

`for f in corpus/lessons/round-*.md; do gate_flip_check.py --lesson "$f"; done` (one envelope,
`ENVELOPE start 19:16:52 … end 19:16:55 exit=0 … unchanged`, full output in
`build/R43FlipCheck/sweep.txt`):

```
lessons=55 red=18 green=2 setup=35 unresolved_sum=45
```

The 18 red lessons and their counts: round-24 2, round-25 4, round-26 3, round-27 5, round-28 4, round-29 2,
round-30 3, round-32 1, round-33 1, round-34 1, round-35 2, round-36 4, round-37 2, round-38 2, round-39 3,
round-40 3, round-41 1, round-42 2. The 2 green lessons (round-13-coverage, round-31) have a `## Gate`
section and zero obligations, so their green demonstrates nothing; the 35 `SETUP` files have no `## Gate`
section and are exit 2, never a pass.

## 3. QUALITY criterion draft (next free number: Q35)

`build/R43FlipCheck/QUALITY-Q35-draft.md`, in the landed sections' shape
(`## Round43 criterion — …`, `- **Q35 — …**`, Check / Shown able to fail / Limits / Lesson / Supersedes).
The normative sentence:

> **Q35 — every Gate refusal whose reason states a flip condition is resolved, in the same lesson and on a
> line after the flip statement, by `Flip check (round N): <item> — fired|not fired — <evidence>`; a
> condition that fires at landing must not be representable as silence, because the lane's only record
> that a flip was examined at all is the sentence that says so.**

Grounded numbers in the draft: 20 lessons carry `^## Gate$`, 18 carry obligations, 45 obligations total,
0 resolved; no line in `corpus/` or `plans/` says `Flip check` (grep → no matches), and the only `flip:`
string in `plans/*.py` is a fixture literal (`plans/round33_c1_verify.py:215`), so nothing has ever read
this class. Limits named there: the verdict is a recorded sentence, not an executed consequence (a `fired`
line with wrong evidence passes); the class is red on history so it binds from round 43 forward and does not
re-adjudicate the older 43; no `## Gate` section is exit 2, never a pass; the imperative "flip one entry at
a time" phrasing is not counted; a companion bullet attaches to every candidate it names and to none it does
not; the two-word state vocabulary rejects a third state; and the working tree only — a resolution line in
another file or a deleted line is invisible.

## 4. SKILL registry row draft

`build/R43FlipCheck/SKILL-registry-row.md`: name `gate-flip-check`, kind `gate`, entry
`python3 plans/gate_flip_check.py --lesson <path>`, verdict map `0` resolved / `1` `FLIPS total=<n>
unresolved=<u>` with u>0 / `2` setup, self-test `--selftest` (19 fixtures, `ok=19/19`), pinned values `none
in the script; the lesson it reads is the input` with the red control (`round-42.md` → `total=2
unresolved=2`) and the green control (scratch copy → `total=2 unresolved=0`), write scope `none — reads the
named lesson, writes nothing; --selftest writes only its own mkdtemp tree`, owner `kengaku`; plus an
addendum paragraph saying the row is red on the landing tip by construction and must be wired as a forward
gate.

## 5. Risks, limits, blockers

- **The tool must land as `plans/gate_flip_check.py`.** Every command in the draft criterion and the
  registry row is written against that path; at `build/R43FlipCheck/gate_flip_check.py` it runs, but the
  criterion's own check line does not.
- **Red by construction.** Landing the criterion makes 18 lessons and 45 obligations red. The L1 has to
  decide whether that is a forward gate (my draft's framing) or whether the first round to land it must
  also append the resolutions it can defend. Appending is the shape R1 requires — the round-42 lesson is not
  edited, a resolution line is added after it — but only for flips someone can actually settle; the other 43
  are older rounds' business.
- **A `fired` record is not the execution.** The check proves a sentence exists, not that its consequence
  landed. This is the criterion's own named limit, and it is why the check is cheap enough to run per round
  (55 lessons in ~3 s) but cannot by itself close D3 — closing D3 needs the `S###` row (closure R2).
- **Shape coverage is deliberately narrow.** A flip phrased imperatively, a candidate named only in prose, a
  resolution line missing the colon after `(round N)`, or a `### Gate` heading all fail closed (unresolved
  or exit 2) rather than passing silently; each is named in the docstring's Limits and in Q35's.
- **`--selftest` re-invokes itself** (`sys.executable` + `sys.argv[0]`) inside a `mkdtemp` tree and deletes
  it; it needs no network, no git, no lane and no writable PATH directory, and it ran inside the round-43
  envelope with the PATH-dir digest unchanged.
- **No tool was installed** (nothing needed beyond python3 stdlib), no pacman/jj/git mutation was run in the
  lane, and the scratch dir `/fast/scratch/hyaku/kengaku-r43/R43FlipCheck` was removed with
  `plans/scratch_guard.py safe-rm` (`DELETE … bytes=63250`, rc=0); the receipts are copied into
  `build/R43FlipCheck/`.

VERDICT: flip-check-red-on-r42-yes-selftest-19/19
