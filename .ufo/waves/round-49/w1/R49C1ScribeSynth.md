# R49C1ScribeSynth — r45→r49 C1 history synthesis (scribe, kengaku round 49 w1)

Seat: `R49C1ScribeSynth` (scribe), serving **R49-C1** (calibration). One v2 build-and-attack wave, hyaku run 10.
Item executed: *draft a concise factual synthesis of the r45→r49 C1 history (keyed-control pass; kill-rule firing;
measured 8/120 base refusal; unreproducible r46 9/9; 2/13 mutants; round-48 no-landing) with evidence pointers only;
no new factual claims.*

## Axes named (godspeed step 1)

| axis | this seat moves | this seat must not move |
|---|---|---|
| **calibration** (primary) | nothing measured; this seat consolidates already-committed C1 evidence into one pointer table so the stage-2 counter author and the closure review do not re-derive it | no predicate line, control, kill rule, literal, or fence byte; no re-freeze; no admission claim |
| coverage / novelty / depth / operability / freshness / adjacency | none | no C2 surface touched; no score, SCORECARD row, or LOG entry written |

## Revision measured

- Clone of the lane at `/fast/scratch/hyaku/kengaku-r49/R49C1ScribeSynth/cl`, `git rev-parse --show-toplevel`
  printed `/fast/scratch/hyaku/kengaku-r49/R49C1ScribeSynth/cl` (asserted before any read).
- `REV af88aab193e6034cb9b386472064e3c18fa90128` — clone HEAD; the lane tip at report time is the same commit
  (`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD` → `af88aab193e6034cb9b386472064e3c18fa90128`).
- `TREE clean` (fresh clone, read-only; no file written inside it).
- Frozen base under test: `9d2900af41e4d1fc6022eff99010436fde6dbd93` (`round-49: stage-1 freeze of C1 … and C2 … claims`,
  authored `2026-10-28 09:14:40 -0300`).

## Stage-1 freeze verification (precondition for any scored run — none run, see Limits)

| check | command (in the clone) | observed | result |
|---|---|---|---|
| freeze commit exists | `git cat-file -t 9d2900af…` | `commit` | pass |
| freeze predates the wave | `git merge-base --is-ancestor 9d2900af af88aab` | exit 0 (`yes`) | pass |
| claims unamended after freeze | `git log --oneline 9d2900af..af88aab -- plans/round-49-claims.md` | empty | pass — no post-freeze edit of the claim file |
| no C1 counter landed at the base | `git ls-tree -r 9d2900af --name-only \| grep -c round49_c1_verify` | `0` | pass — predicate is still prospective at stage 1 |
| base fence byte-stability | `git show 9d2900af:plans/fixture_fence.py \| sha256sum` vs `git show 3a54833:plans/fixture_fence.py \| sha256sum` | both `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` | pass — the r49 "base fence" is the same r46 variant-A allowlist the r48 before-value measured |
| wave-1 report dir at the base | `git ls-tree -r 9d2900af --name-only \| grep '^.ufo/waves/round-49/w1/'` | empty | consistent with an in-progress wave |

The freeze's own wording binds the repair direction: `plans/round-49-claims.md:15` — “the routed repair now carries
the measured 8/120 base refusal, never the unreproducible r46 placeholder-argv”.

## History synthesis — six routed facts, pointers only

No fact below is new; each row quotes committed bytes and names the file, commit-relative path and line.

| # | fact (as routed) | evidence pointer | located quote (≤25 words) |
|---|---|---|---|
| 1 | **r45: the frozen C1 predicate was passed by a keyed do-nothing control** — the pass was reachable without the fence work | `.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt:1` (fence `claims/fences/keyed_name.py`, post-landing, lane clone `fbad1c56`); same file, verdict lines | `:1` “fence = fences/keyed_name.py (inspects nothing; keys on the counter-chosen fixture path)” (15 words); receipt prints `PREDICATE C1 pass`, `exit=0` |
| | non-author confirmation of the same fact | `corpus/lessons/round-45-verifier-spotcheck.md:63` | “confirmed — the frozen predicate is reachable without the work” (9 words) |
| | the critic reading of that receipt | `.ufo/waves/round-45/a3w1/R45CritC1Overclaim.md:9` | “A no-inspection fence keyed to the counter's fixture path was already measured by the L1” (16 words) |
| 2 | **r46: the frozen held-out kill rule fired although the predicate printed pass** — 3 admitted held-outs vs the “≥2 rejects” threshold | `corpus/lessons/round-46-verifier-spotcheck.md:19` | “the frozen kill rule is met: wave-2 reports count 3 admitted held-outs (2 argv, 1 paths), and the literal rule says ≥2 rejects C1” (24 words) |
| | the lane's own statement of the firing | `corpus/lessons/round-46.md:86-88` | “The frozen kill rule … fires on its literal count: 3 admitted” (11 words, §C1 bullet) |
| | r46 disposition | `corpus/lessons/round-48-verifier-spotcheck.md:51` (provenance line) | “r46 `a5ed97f1` (rejected-harmed)” |
| 3 | **measured base refusal is 8 of 120 honest fixtures** (the r49 `<H>` population basis) | `.ufo/waves/round-48/w1/R48C1ExecCounter.md:94` (REV), `:99` (HONEST line), `:104` (verdict) | `:99` “HONEST fixtures=120 admitted=112 refused=8 read=0 hung=0 build_errors=0” (7 words) at `REV abb08e283a0eba0eb469fbc8d2f4d7cb2f49c359`, then `PREDICATE R48-C1 fail` |
| | restated in the r48 lesson | `corpus/lessons/round-48.md:28` | “the candidate counter measured the base fence as `HONEST fixtures=120 admitted=112 refused=8`” (13 words) |
| | carried into the r49 freeze | `plans/round-49-claims.md:158` | “(measured 8/120 refusals on the frozen population by round-48; the stage-2 receipt re-measures…)” |
| 4 | **the r46 “9/9 refused” figure does not reproduce** — it was a `{WORK}` placeholder-argv artifact, not repository-state over-refusal | `.ufo/waves/round-48/w1/R48C1ExecControls.md:16-18` (§1) | “The round-46 "9/9 refused" was a `{WORK}` placeholder-argv artifact, not a repository-state over-refusal.” (15 words) |
| | the controlled re-measure on the frozen population | same file, §1 | “the base fence refuses **8 of 16** novel honest classes, and only **3 of the 9** round-46 classes” (19 words) |
| | the original 9/9 statement being superseded (r46 routed defect) | `corpus/lessons/round-46-verifier-spotcheck.md:45` | “repair over-refusal (9/9 novel honest controls refused)” (7 words) |
| | the r49 freeze's binding use | `plans/round-49-claims.md:47-48` | “the r46 "9/9" figure does not reproduce (all nine r46 override modules used `{WORK}` placeholder argv” (18 words) |
| 5 | **mutation evidence was 2 of 13 fence mutants caught** — the gap the r49 MUTANTS leg and `<M>` floor answer | `corpus/lessons/round-46.md:92` | “2 of 13 fence mutants caught (`R46W2C1MutFence`: the refusal/sealed sets do not” (14 words) |
| | independent restatement | `corpus/lessons/round-46-verifier-spotcheck.md:45` | “mutation evidence is only 2/13 fence mutants and 1/6 counter mutants caught” (13 words) |
| | the r49 freeze's floor rule cites this history | `plans/round-49-claims.md:91` | “(round-46 observed 2/13; the floor and receipts are committed, never asserted)” (13 words) |
| 6 | **round 48 landed nothing for C1** — counter and population stayed seat-scratch; the fence source was unchanged | `corpus/lessons/round-48-verifier-spotcheck.md:31` | “`git ls-tree -r d4eacdfb… --name-only \| grep round48_c1_verify` → **absent**” (7 words) |
| | the fence byte-identity | `corpus/lessons/round-48-verifier-spotcheck.md:32` | “`plans/fixture_fence.py` byte-identical to the pre-round version (temporary L1 candidate removed, as reported)” (15 words) |
| | the lesson's own verdict | `corpus/lessons/round-48.md:28` | “unverified / not admitted; score 8→8 held” (7 words) |
| | the repair candidate existed only in scratch | `.ufo/waves/round-48/w1/R48C1ExecFenceA.md:70,1071-1072` | `:1071` “variant A candidate complete and measured — 34/34 novel honest fixtures … admitted with `touches=0`” |

### Intervening round 47 (context for the “r45→r49” span)

Listing-observed only, no interpretation: `.ufo/waves/round-47/` contains `build_spec.py` and `w1-spec.json` and no
`w1/` directory; `corpus/lessons/` holds `round-45.md`, `round-46.md`, `round-48.md` and **no** `round-47.md`. The
r47 closure is recorded as a commit at `corpus/lessons/round-48-verifier-spotcheck.md:51`: “r47 `98a0cb51`”. The
r47 C1 direction is visible in `.ufo/waves/round-47/build_spec.py:53,62` (kill-rule and 2/13 synthesis items) and in
`corpus/lessons/round-47-verifier-spotcheck.md:26,68`, which carries the same four C1 facts forward.

### Where the r49 claim stands against that history (pointer, not a verdict)

`plans/round-49-claims.md:41-48,52-58` state the four repairs the routed defects require: honest population frozen at
stage 2 with per-module digests, the MUTANTS leg with a `<M>/2` floor and per-mutant receipts (:79-84), the round-45
keyed fence demoted to a **control that must fail** (:87), and the base fence at `3a548330` kept as the do-nothing
control (:158). None of these is executed in this report.

## Sources opened (URL / access date / located quote duty)

No external URL was opened by this seat: every source above is a committed lane file read from the clone at
`REV af88aab1…`. The URL/access-date/quote duty is therefore discharged as **(path, commit-relative, line, quote)**
rows in the table above; no `http(s)` row exists for this report. The r49 C2 sourced basis (S166, reopened by the L1)
is out of this seat's scope and is not restated here.

## Commands run (exact)

```
mkdir -p /fast/scratch/hyaku/kengaku-r49/R49C1ScribeSynth
cd /fast/scratch/hyaku/kengaku-r49/R49C1ScribeSynth && git clone --shared -q /home/vgpnk/Projects/shokunin/kengaku-shokunin cl
cd cl && git rev-parse --show-toplevel && git log --oneline -6
git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93
git log -1 --format='%H %ci %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
git log --oneline 9d2900af..af88aab -- plans/round-49-claims.md
git merge-base --is-ancestor 9d2900af af88aab
git ls-tree -r 9d2900af --name-only | grep -c round49_c1_verify
git show 9d2900af:plans/fixture_fence.py | sha256sum ; git show 3a54833:plans/fixture_fence.py | sha256sum
grep -rn -i "keyed" .ufo/waves/round-45/
cat .ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt
sed -n '1,35p' .ufo/waves/round-45/a3w1/R45CritC1Overclaim.md
sed -n '10,22p' corpus/lessons/round-45-verifier-spotcheck.md
sed -n '15,50p' corpus/lessons/round-46-verifier-spotcheck.md
sed -n '43,48p' corpus/lessons/round-46-verifier-spotcheck.md
sed -n '86,90p' corpus/lessons/round-46.md
sed -n '88,108p' .ufo/waves/round-48/w1/R48C1ExecCounter.md
sed -n '10,26p' .ufo/waves/round-48/w1/R48C1ExecControls.md
grep -n "120/120\|104/104\|20/20\|12/12\|VERDICT" .ufo/waves/round-48/w1/R48C1ExecFenceA.md
grep -n "round48_c1_verify\|byte-identical\|R48-C1" corpus/lessons/round-48-verifier-spotcheck.md
grep -n "73540ccc\|a5ed97f1\|98a0cb51" corpus/lessons/round-48-verifier-spotcheck.md corpus/lessons/round-48.md
grep -n "mutant\|2/13" corpus/lessons/round-46.md
ls .ufo/waves/round-47/ ; ls corpus/lessons/round-4[5-8].md
ls -d /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-49/w1/
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
```

No mutating git/jj command was run at any point (clone creation excepted; it wrote only inside the seat scratch).
No pacman, `uv`, `npx` or other install was run; nothing was installed, upgraded or removed.

## Limits

- **No scored counter or probe execution.** No `plans/round49_c1_verify.py` exists at the base
  (`grep -c` → `0`), and the stage-2 pins/literals are not committed, so the frozen predicate cannot be run. This seat
  makes no measurement of its own; every number quoted is a committed third-party receipt with its own `REV`.
- **No admission claim.** R49-C1 and R49-C2 are not asserted admitted, admitted-pending, or refuted here.
- Quotes are single-line extracts; two rows quote a fragment ending mid-clause and are marked by the ellipsis-free
  cut (word counts stay ≤25). The `R48C1ExecFenceA` figures were read from that report, not re-executed.
- The r47 row is a directory/lesson listing observation plus the spotcheck's provenance line, not a re-audit of r47.
- Lane tree: read-only clone only. The only file this seat wrote outside scratch is this report.

## Scratch

`S=/fast/scratch/hyaku/kengaku-r49/R49C1ScribeSynth` (`TMPDIR` exported there), holding one `git clone --shared` of the
lane at `af88aab1…`. **Deleted before yield** (`rm -rf "$S"`, then `ls` → `No such file or directory`); no receipt in
this report depends on a scratch path as citable evidence, and no report artifact was left in `/tmp`.

VERDICT: history-synthesis-delivered (6/6 routed C1 facts pointer-keyed; 0 scored runs; 0 new factual claims; freeze
`9d2900af` verified present, unamended and predating the wave; C1 not admitted by this seat)
