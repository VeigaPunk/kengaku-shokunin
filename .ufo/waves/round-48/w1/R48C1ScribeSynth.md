# R48C1ScribeSynth — r45→r48 C1 evidence-pointer synthesis (scribe, R48-C1)

Seat: `R48C1ScribeSynth`, role scribe, route `@m_flash` (as captured at spawn; no model passed).
Item served: R48-C1 (calibration). Scope: a concise factual synthesis of the r45→r48 C1 history with evidence
pointers only. No new factual claims, no scored counter/probe execution, no product edit, no commit.
Access date for every source below: **2026-10-27**. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

## Axes named

- **Primary: calibration** — the axis R48-C1 is charged to (`plans/round-48-claims.md` §C1; SCORECARD axis state
  carried at 8, "held — kill rule fired").
- Secondary axes named by the source receipts themselves (not measured by this seat): **evidence integrity** and
  **contract fidelity** (`w2/R46W2C1MutFence.md` line 3); **operability** appears only as a routed-defect pointer
  (`corpus/lessons/round-46-verifier-spotcheck.md` §Routed defects 1–4).
- This seat evaluated **no axis**. It re-read bytes; it did not score.

## Freeze gate (checked before anything else)

Commands (read-only):

```
git -C $L rev-parse --show-toplevel
git -C $L log --format='%H %ci %s' -3
git -C $L cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
git -C $L ls-tree a543d92083557dd9b33ee674e9b99b03411f80af -- plans/round-48-claims.md
git -C $L diff --stat a543d92083557dd9b33ee674e9b99b03411f80af -- plans/round-48-claims.md
git -C $L status --porcelain
ls -la plans/round48_c1_verify.py plans/round48_c2_verify.py
find .ufo/waves/round-48 -maxdepth 3
```

Observed (verbatim):

```
/home/vgpnk/Projects/shokunin/kengaku-shokunin
bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767 2026-10-27 08:29:33 -0300 round-48: w1 ready handoff marker
453ddfdb4e8f69068aaf25084756188012cfcb10 2026-10-27 08:29:18 -0300 round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
commit
100644 blob 3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5	plans/round-48-claims.md
(no output from git diff --stat)
?? .ufo/waves/round-48/claims/
?? .ufo/waves/round-48/w1.ready.partial
?? .ufo/waves/round-48/w1/
ls: cannot access 'plans/round48_c1_verify.py': No such file or directory
ls: cannot access 'plans/round48_c2_verify.py': No such file or directory
```

Gate result:

- **Stage-1 freeze present in the committed tree and predates all wave-1 activity.** `plans/round-48-claims.md` is
  blob `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5` at `a543d920` (06:53:29 -0300); sha256 of the same bytes =
  `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672` (recomputed read-only: `git show
  a543d920:plans/round-48-claims.md | sha256sum` and `sha256sum plans/round-48-claims.md` both print it, so blob id
  and sha256 agree on identical bytes — two hash functions, no conflict). The worktree copy is byte-identical to the
  freeze (`git diff --stat` empty); the dispatch commit is later (`453ddfdb`, 08:29:18 -0300).
- **Stage-2 freeze absent.** The counter files the claim pins at stage 2 (`plans/round48_c1_verify.py`,
  `plans/round48_c2_verify.py`), the literals `<P> <H> <S> <B> <M>`, and the pre-receipt control receipts do not
  exist in the committed tree or the worktree; `.ufo/waves/round-48/claims/` contains only `README.txt` and
  `freshness-r48.txt` (2 files, untracked, `prepared_by=L1 KengakuR48 2026-10-27T11:30:40Z`).
- Consequence: **no scored C1 run is permitted and none was made.** No round-48 C1 receipt exists on disk
  (`find .ufo/waves/round-48 -type f` shows no receipt beyond the two scaffold files). Blocker stated, not worked
  around. This seat's item did not require a scored run.

## Synthesis, r45 → r48 (pointers only)

1. **r45 — the keyed-control pass (the freeze defect).** The r45 C1 predicate passed on a fence that never did the
   work: a 7-line fence refusing iff `"/refusals45-" in str(d)` printed the same pass. Receipt
   `.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt` ends `REFUSALS total=10 clean=10 leaked=0 read=0
   hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0`, `CALIBRATION advertised=10
   contradicted=0`, `PREDICATE C1 pass`, `exit=0`. Read by the non-author spot-check as
   `| keyed control | … | PREDICATE C1 pass, exit 0 | confirmed — the frozen predicate is reachable without the work |`
   (`corpus/lessons/round-45-verifier-spotcheck.md:63`), axis verdict line `| calibration | unprovable | C1 counter
   passed by keyed control; held-out 8/10 admitted |` (`:102`). Root-cause row: `corpus/lessons/round-45.md:93`
   ("A freeze whose controls never included a procedure that keys on the counter's own names"). Q39 (name-hiding)
   enters the counter contract here; `plans/round-48-claims.md` §C1(c) carries it forward.

2. **r46 — honest over-refusal (the calibration breach).** Nine novel honest classes were all refused:
   `w2/R46W2C1HoHonest.md:3` — "Thus **9/9 were refused**, with no outside touches." Classes named there: packed
   refs after `gc`/`pack-refs`, annotated tags, detached HEAD, a merge commit, `.gitignore`, a 30-commit linear
   history, reflog gc, annotated-tag-plus-detached-HEAD, an ignored untracked file. Restated at
   `corpus/lessons/round-46.md:91-92`. Note the scope split: the pinned HONEST leg is the 104 battery fixtures
   (`w2/R46W2C1MutFence/summary.txt` BASELINE: `HONEST fixtures=104 admitted=104 refused=0` at `420eec9f`), while
   the nine novel classes were run only through the `--sealed` override quoted above.

3. **r46 — the kill rule firing on 3 benign held-outs.** Frozen text (`git show a543d920:plans/round-46-claims.md`,
   §C1 Kill rule): "Wave-2 held-out modules (authored against the landed fence) are reported per module; two or
   more admitted or read → C1 not admitted even if the predicate passes". Observed admissions:
   `w2/R46W2C1HoArgv.md:17` `VERDICT: heldout-argv-2-admitted-2-read-0` (both `ADMIT touches=0`);
   `w2/R46W2C1HoPaths.md:14` `VERDICT: heldout-paths-1-admitted-1-read-0` (`LEAKED fixtures=4 admitted=1 hung=0
   touches=0`, `read=0`). Total 3 admitted, 0 read. The literal count fired; the authoring seats state no outside
   access was observed (`HoArgv.md:15`, `HoPaths.md:5`). Judge-facing restatement:
   `corpus/lessons/round-46-verifier-spotcheck.md:19` ("the literal rule says ≥2 rejects C1") and
   `corpus/lessons/round-46.md:86-89`. Verdict of that closure: `rejected-harmed`, calibration `harmed`.

4. **r46 — mutation sensitivity floor evidence (2/13).** `w2/R46W2C1MutFence.md` results line: "13 valid one-edit
   mutants run; 2 killed, 11 survived. Mutation setups #6 and #13 did not run and are not counted. Thus
   `VERDICT: fence-mutants-caught-2/13`." Companion counter-mutant seat: `w2/R46W2C1MutCounter.md:57`
   `VERDICT: c1-counter-mutants-killed-1/6`. Baseline in the same run: `PINS total=65 mismatched=0`; refusals
   20/20 clean; sealed 12/12 clean; honest 104/104; `CALIBRATION advertised=32 contradicted=0`; `PREDICATE C1
   pass` (`w2/R46W2C1MutFence/summary.txt`). This is the number `plans/round-48-claims.md` §C1 quotes as
   "round-46 observed 2/13" against which the round-48 floor `<M>/2`, `<M> ≥ 12` is frozen.

5. **r47 — nothing frozen, nothing landed.** `corpus/lessons/round-47-verifier-spotcheck.md:44` — "the round froze
   and landed no claim, so there is no axis-move to admit … Verdict: `rejected-honest-stop`." C1 carried forward
   with exactly the two r46 numbers: `:68` "9/9 novel honest refused; only 2/13 fence mutants caught".

6. **r48 — the claim under test (stage 1 only).** `plans/round-48-claims.md` §C1 replaces the admission-keyed
   detector semantics: LEAK only on traced outside access (touches>0 or READ), `BENIGN-ADMIT` counted separately,
   honest population frozen at stage 2, control set must include the base fence `@0f77f9b` (before value: "the 9
   round-46 novel honest classes refused — `HONEST … refused=9` minimum") and the round-45 keyed fence. Stage-2
   literals `<P> <H> <S> <B> <M>` are **not yet committed** (see gate above), so no r48 C1 measurement can exist
   yet, and this seat made none.

## Exact commands run (all read-only; no scored execution)

```
mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C1ScribeSynth ; export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1ScribeSynth ; df -h /fast
git -C $L rev-parse --show-toplevel
git -C $L log --format='%H %ci %s' -3
git -C $L cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
git -C $L log --format='%H %ci %s' -1 a543d92083557dd9b33ee674e9b99b03411f80af
git -C $L status --porcelain | wc -l
git -C $L ls-tree a543d92083557dd9b33ee674e9b99b03411f80af -- plans/round-48-claims.md
git -C $L diff --stat a543d92083557dd9b33ee674e9b99b03411f80af -- plans/round-48-claims.md
git -C $L ls-tree -r --name-only a543d92083557dd9b33ee674e9b99b03411f80af | grep -E 'round48|fixture_fence|polyglot_c_py_probe|round46_c1|round46_c3'
git -C $L ls-tree -r --name-only a543d920 | grep -E '^\.ufo/waves/round-46/(w2|integrate)/'
git -C $L ls-tree -r --name-only a543d920 | grep -E '^\.ufo/waves/round-45/' | grep -iE 'c1|fence|mutat|keyed|control'
git -C $L ls-tree -r --name-only a543d920 | grep -E '^\.ufo/waves/round-48/'
cat .ufo/waves/round-46/w2/R46W2C1MutFence/summary.txt
cat .ufo/waves/round-46/integrate/c1-landing.txt
cat .ufo/waves/round-46/w2/R46W2C1MutFence.md
sed -n '1,60p' .ufo/waves/round-46/w2/R46W2C1HoHonest.md
grep -nE 'VERDICT|touches=0|admitted|LEAK|revision|REV' .ufo/waves/round-46/w2/R46W2C1HoArgv.md
grep -nE 'VERDICT|touches=0|admitted|LEAK|revision|REV' .ufo/waves/round-46/w2/R46W2C1HoPaths.md
grep -nE 'VERDICT|caught|survived' .ufo/waves/round-46/w2/R46W2C1MutCounter.md
head -6 .ufo/waves/round-46/integrate/final-tip.txt
git -C $L show a543d920:plans/round-46-claims.md | sed -n '55,62p'
git -C $L show a543d920:.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt | tail -12
grep -rniE 'keyed|path-keyed' corpus/lessons/round-45*.md corpus/lessons/round-46*.md
sed -n '63p;100,104p' corpus/lessons/round-45-verifier-spotcheck.md
sed -n '86,92p' corpus/lessons/round-46.md
grep -nE 'C1|rejected-honest-stop|never dispatched' corpus/lessons/round-47-verifier-spotcheck.md
sed -n '1,40p' corpus/lessons/round-48.md          # 14 lines; Gate/Mistakes say "(filled at integration)"
grep -nE 'C1|round-45|round-46|keyed' SCORECARD.md
ls -la plans/round48_c1_verify.py plans/round48_c2_verify.py
find .ufo/waves/round-48 -maxdepth 3 ; find .ufo/waves/round-48/claims -type f | wc -l
cat .ufo/waves/round-48/claims/README.txt ; cat .ufo/waves/round-48/claims/freshness-r48.txt
```

No write command touched the lane tree, no git/jj mutating command ran anywhere, no fixture Git call was made (no
fixture was built; `git -C` was used only against `$L` with `rev-parse --show-toplevel` printed first).

## Revision measured

- Lane HEAD at read time: `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; stage-1 freeze: `a543d92083557dd9b33ee674e9b99b03411f80af`.
- **REV** for each receipt quoted above, as the source states it (r46 predates the Q22 `REV` prefix form):
  - `.ufo/waves/round-46/integrate/c1-landing.txt:1` — `# C1 frozen counter at lane commit 420eec9f7bc59130277629028b504a6212c2c364`
  - `.ufo/waves/round-46/integrate/final-tip.txt:1` — `== C1 at 264b7757f7815fe31bb5c1b1abf3299dab4e4caf`
  - `w2/R46W2C1HoHonest.md:6`, `w2/R46W2C1HoArgv.md:3`, `w2/R46W2C1HoPaths.md:7`, `w2/R46W2C1MutFence.md:5` — clone
    HEAD `42d5043afac952fcb43bf4798757785dd258cf85`
  - round-45 keyed control receipt: clone of `fbad1c5` (`corpus/lessons/round-45.md:93`); the receipt itself carries
    no `REV` line, only `ENVELOPE end 00:21:34 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`.
- This seat measured **no** revision of C1 behaviour; the REV lines above are the revisions its sources claim.

## Conflicts and limits (verbatim, for the canonical judge)

1. **Receipt-header form vs Q22.** `plans/round-48-claims.md` §Receipt discipline says "Every receipt this round
   prepends `REV <40-hex>`". The r45/r46 receipts quoted here do not: `c1-landing.txt` opens
   `# C1 frozen counter at lane commit 420eec9f…` and `final-tip.txt` opens `== C1 at 264b7757…`.
   No round-48 receipt exists yet to satisfy or violate Q22. Recorded, not resolved, by this seat.
2. **The 9/9 measurement is an override probe, by its own words.** `w2/R46W2C1HoHonest.md:8`: "The fail is expected
   for this override because adding nine modules violates the counter's frozen exact SEALED total of 12.
   Consequently this is a direct fence behavior probe, not a passing/frozen C1 run; do not interpret the override
   predicate as the pinned result." The 9/9 refusal count is therefore probe evidence, not a pinned counter verdict;
   the spot-check and the round-48 claim both cite it as the over-refusal number.
3. **Admission-vs-leak semantics conflict was already live in r46.** `HoArgv.md:3`: "rollup `LEAKED` is the
   detector classification for admission, not a claim that an outside path was observed." `HoPaths.md:11` states the
   one module is "below the threshold of two" alone, while `HoArgv` supplies the other two. R48-C1(b) is the frozen
   repair of exactly this semantics; it is not yet measurable (stage 2 absent).
4. **Limit of this seat's reading.** `corpus/lessons/round-46-verifier-spotcheck.md:19` is a long single cell; it was
   re-read with `:19:raw` in full, but other long cells in `SCORECARD.md` were truncated in the default read and were
   not re-read raw — no SCORECARD cell is quoted as evidence here; the SCORECARD is cited only by location.
5. **No external sources were opened.** This item required none; the only network-bearing requirement in
   `plans/round-48-claims.md` (§C2, S166 reopen with URL/date/≤25-word quote) belongs to a C2 seat, not to this one.
   Source table below is local-path only.
6. **Frozen-text gap: how `BENIGN-ADMIT` maps onto the SEALED leg (textual only, unscored).** Delta (b) is worded
   per fixture — "a fixture result is `LEAK` only if traced opens/reads outside `d` are observed … a fixture admitted
   with `touches=0` is reported as `BENIGN-ADMIT` and counted separately, never as a leak"
   (`plans/round-48-claims.md:51-53`) — while the predicate still demands `SEALED total=<S> clean=<S> leaked=0
   read=0 hung=0 build_errors=0` (`:61`). A SEALED module admitted with `touches=0` would be `BENIGN-ADMIT` and not
   `clean`, so the SEALED line would be off and the kill rule ("Any predicate line off at the landing tip → C1 not
   admitted") applies. The frozen text does not say which reading governs; resolving it inside the v3 counter without
   editing a predicate line or a kill rule is the stage-2/wave-1 executor's problem. Pointed at, not adjudicated, by
   this seat (raised by sibling seat `R48C1ScribeLimit` and confirmed against the quoted lines above).
7. **Companion limits ledger (pointer, not verified by this seat).** A sibling scribe seat reports its named-limits
   list at `.ufo/waves/round-48/w1/R48C1ScribeLimit.md` (`REV a543d920`), including that the honest population is
   finite, that the nine novel classes are re-authored from `w2` descriptions, and that no score exists because
   `plans/round48_c1_verify.py` is absent. This seat did not open or re-derive that file; it is cited as the
   companion pointer only, and its content does not modify anything above.
7. **Observed lane change not authored by this seat.** At the gate check `git status --porcelain` printed 3 untracked
   entries (`claims/`, `w1.ready.partial`, `w1/`); at the closing check it printed a fourth, `?? corpus/lessons/round-48.md`.
   This seat wrote only `.ufo/waves/round-48/w1/R48C1ScribeSynth.md`; the lesson file is another seat's/L1's work and is
   reported as observed, not attributed.

## Sources opened (path @ revision, access 2026-10-27, ≤25-word located quote)

| # | source | located quote (≤25 words) |
|---|---|---|
| 1 | `plans/round-48-claims.md` @ `a543d920` (blob `3a9c71f3…`) | "a fixture admitted with `touches=0` is reported as `BENIGN-ADMIT` and counted separately, never as a leak" |
| 2 | `corpus/lessons/round-46-verifier-spotcheck.md` @ `a543d920` | "the literal rule says ≥2 rejects C1" (line 19); "9/9 novel honest fixtures refused and fence mutants 2/13 caught" |
| 3 | `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` @ `a543d920` | "Thus **9/9 were refused**, with no outside touches." |
| 4 | `.ufo/waves/round-46/w2/R46W2C1HoArgv.md` @ `a543d920` | "`VERDICT: heldout-argv-2-admitted-2-read-0`" |
| 5 | `.ufo/waves/round-46/w2/R46W2C1HoPaths.md` @ `a543d920` | "`VERDICT: heldout-paths-1-admitted-1-read-0`" |
| 6 | `.ufo/waves/round-46/w2/R46W2C1MutFence.md` + `summary.txt` @ `a543d920` | "13 valid one-edit mutants run; 2 killed, 11 survived." |
| 7 | `.ufo/waves/round-46/w2/R46W2C1MutCounter.md` @ `a543d920` | "`VERDICT: c1-counter-mutants-killed-1/6`" |
| 8 | `.ufo/waves/round-46/integrate/c1-landing.txt`, `final-tip.txt` @ `a543d920` | "`PINS total=65 mismatched=0`" … "`PREDICATE C1 pass`" |
| 9 | `git show a543d920:plans/round-46-claims.md` | "two or more admitted or read → C1 not admitted even if the predicate passes" |
| 10 | `.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt` @ `a543d920` | "`CALIBRATION advertised=10 contradicted=0`" / "`PREDICATE C1 pass`" |
| 11 | `corpus/lessons/round-45.md:93`, `round-45-verifier-spotcheck.md:63,102` @ `a543d920` | "A one-line keyed fence passes the frozen predicate."; "C1 counter passed by keyed control; held-out 8/10 admitted" |
| 12 | `corpus/lessons/round-46.md:86-92` @ `a543d920` | "The frozen kill rule … fires on its literal count: 3 admitted" |
| 13 | `corpus/lessons/round-47-verifier-spotcheck.md:44,68` @ `a543d920` | "Verdict: `rejected-honest-stop`."; "only 2/13 fence mutants caught" |
| 14 | `corpus/lessons/round-48.md` (14 lines, Gate/Mistakes unfilled) @ `a543d920` | "(filled at integration)" |
| 15 | `.ufo/waves/round-48/claims/README.txt`, `freshness-r48.txt` (untracked) | "round-48 claims receipts dir; every receipt names REV" |

## Scratch

Scratch `/fast/scratch/hyaku/kengaku-r48/R48C1ScribeSynth` was created, `TMPDIR` exported to it, and **removed**
before this report was finalized (`rm -rf`; no receipt needed to be copied out — every quoted byte is committed
lane content, so nothing in the report points at scratch or `/tmp`). No fixture Git repository was created.

## VERDICT

`VERDICT: synthesis-complete-no-scored-run` — r45 keyed-control pass, r46 9/9 honest refusals and 2/13 fence mutants,
r46 kill rule fired on 3 benign held-outs, r47 honest stop, r48 stage-1 freeze only; every statement above is a
pointer to committed bytes at `a543d920`/`bf783c1e`. Stage-2 freeze absent from the committed tree → no scored C1
execution was permitted or made; no R48-C1/C2 admission is claimed.
