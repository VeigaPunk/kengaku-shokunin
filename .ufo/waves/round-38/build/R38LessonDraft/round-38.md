# Round 38 — a build arm executed offline, and the gate's advertised behaviours attributed (2026-10-26, hyaku run 8)

Baseline `fc1174f52b150999bef91f2e81da78732ca0eb9f` (the round-37 non-author verifier spot-check); frozen claims
`plans/round-38-claims.md` (freeze `e0a378539a45cc9388c66cfba22f44275131de23`; first recorded probe run
`e95cf5500b6c13305cc41b8532ae07fb2c9dcd7b`). Ancestry checked at drafting with `git merge-base --is-ancestor`:
baseline → freeze `rc=0`, freeze → probe run `rc=0`. The eight frozen digests in
`.ufo/waves/round-38/claims/frozen-digests.txt` all equal the bytes at the freeze commit — `git show
e0a37853:<path> | sha256sum`, 8/8 `MATCH` — so the round-36 number-drift class does not recur in this freeze.
Controls are red before any `plans/battery38` module exists in the lane (`ls plans/ | grep -c battery38` → `0`)
and before any entry, registry row or README bullet:

- `control-c1-nothing.txt`: `PINS total=14 mismatched=0`, `BATTERY fixtures=64 wrong=0 renamed_disagree=0
  sidechannel=0`, `MUTANTS total=22 killed=0 survived=22 invalid=0 null_detected=0`, `PREDICATE C1 fail`,
  exit 1 (48.5 s) — the round-36+37 battery kills none of the 22 under the ATTRIBUTED rule.
- `control-c1-gate-edited.txt`: `PINS total=14 mismatched=1 first=plans/pkg_gate.py`, `invalid=22`, exit 1 — a
  byte change to the frozen gate invalidates every mutant instead of scoring them.
- `control-c2-nothing.txt`: `checks=7 defects=4` (V2, V3, V4, V7 red; V1 `listed=5 bad=0 extra=0`, V5
  `dry_byte_equal=True`, V6 `census_exit=0`), `PREDICATE C2 fail`, exit 1.
- `control-c2-skip.txt`: a junk entry/rows/README with the *right* anchors and a receipt copied from `--dry` →
  `checks=7 defects=2` (V2 red on `P10 DEFECT fresh probe output is not byte-equal to the receipt`, V6 red),
  `V7 ok rows=7 tags=7`, exit 1. The claims' known-at-freeze note holds: V7 alone is satisfiable by a
  hand-typed receipt; P10's fresh-run byte compare is what makes it red.
- `census-before.txt`: 15 `W04` duplicate-URL warnings (the round-36/37 set, no new one), `kengaku ok`, exit 0.

C1 is measured by its counter, not by a Gate row. At drafting three reported wave-1 seats carry an attributed
kill for their own subset — `build/R38BatP1Run.md` (N01, N16), `build/R38BatP3.md` (N02), `build/R38BatMain.md`
(N17, N18) — each with `wrong=0 renamed_disagree=0 sidechannel=0` for its module alone; the aggregate predicate
(`MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`) and the no-harm re-run of
the round-37 counter are the L1's landing measurements: `<L1 fills>`.

## Gate

| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| `knowledge/tb2-build-pmars-grader.md` (C2) | **Admit on the frozen predicate only** (`<L1 fills>`) | Drafted in wave 1 (seats `build/R38PkgEntry`, `build/R38PkgProse`); at drafting the entry does not exist (`ls corpus/knowledge/ \| grep -ci pmars` → `0`), so the counter's V4/V7 read `receipt or entry absent` (`control-c2-nothing.txt`). The claim rests on the 22-case receipt `corpus/evidence/round38/build-pmars-probe.txt` (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`; predictions frozen in `build-pmars-dry-cases-freeze.txt` before the first recorded run) and on the seven checks of `plans/round38_c2_verify.py`, whose V7 now derives every requirement-map label from *all* violating cases. Derived from the frozen receipt at drafting: every one of the seven tags is `partly` — `from-source` 7 pass/15 fail, `no-x11` 1/2, `debian-source` 7/15, `extract-to-app` 7/15, `install-path` 1/3, `results-format` 1/4, `debugger-works` 7/15 — so an entry map labelled anything else is red. Landing: `checks=7 defects=0`, `PREDICATE C2 pass` `<L1 fills>`. Flip: any V check red at landing, or a capture digest off its pin. |
| S115 `tests/test_outputs.py` @ `2fd12b88` | **Admit (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py`; quote, line 53: “ldd_output = run_shell_command("ldd /usr/local/bin/pmars")” (4 words); also line 24 “assert binary.exists(), "pmars not installed at /usr/local/bin/pmars"” (7 words) and line 84 “c_files = list(src_dir.glob("*.c"))” (3 words); capture `corpus/evidence/round38/tb2-build-pmars/test_outputs.py`, sha256 `d9d2796ddc19cf8159670567e174ea377e2bce675bf3451d5951c045b01f4e85`, listed in `SHA256SUMS` (its own digest `3fd9de04b5c325061a08f8c145a7fce7c8d85fbb9f7a713d350310c2f2eac0bc`); upstream `main` byte-equal at drafting (`build/R38ScoutUpstream.md` §1: git blob `77b17303…`, `cmp` BYTE-EQUAL). Flip: the capture's digest leaves the pin. |
| S116 `instruction.md` @ `2fd12b88` | **Admit (mined)** | Opened 2026-10-26 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/instruction.md`; quote, line 3: “Extract the source to `/app` and build without X11 support. Install the binary to `/usr/local/bin/pmars`.” (15 words); line 7 “This should output "Results: X Y Z" where X, Y, Z are integers.” (13 words); capture sha256 `1606850579342a8b8f2189de0e499fae6be21198150d8dd1e4d18c2efbcf3b82`; upstream `main` byte-equal. The TB2.1 copy of this file differs on line 3 (`build/R38ScoutUpstream.md` §2: it says `/app/pmars-<version>/`, line count unchanged), so every `instruction.md:<L>` anchor in the entry is a **2.0** anchor and the map's line numbers survive the 2.1 text change. Flip: the pin moves, or the line numbering changes upstream. |
| `tests/test.sh`, `task.toml`, `solution/solve.sh` @ `2fd12b88` (captured) | **Captured, not rows** | `test.sh` is the pytest-exit → `/logs/verifier/reward.txt` mechanism the registry already holds as S109 (lines 18–28 run pytest through `uvx`, then write 1/0); `task.toml` is manifest metadata read only for declared limits — verifier and agent `timeout_sec = 900.0`, `docker_image = "alexgshaw/build-pmars:20251031"`, `cpus = 1`, `allow_internet = true` (lines 21–34); `solve.sh` is the oracle, never executed by the frozen probe (claims §C2 limits), so a row would dress it as evidence. Flip: a claim that needs one of them as its source. |
| Prior art: TB2 issue #59 and issue #38 (re-opened live 2026-10-26) | **Row recommended (tier B), capture owed** (`<L1 fills>`) | `gh api repos/harbor-framework/terminal-bench-2/issues/59` → open, created 2026-04-13 by sam571128, title “`build-pmars` failing with oracle solution”; body line 14: “E: Version '1.22.21' for 'dpkg-dev' was not found” (8 words) — about the oracle's pinned apt versions, not the grader. Bodies saved at `build/R38LessonDraft/tb2-issue-59-body.md` (sha256 `22936c6e52c9fd92a5fc807c6d7c4945e64d529622f696ccaf7e7e5ffbce464e`) and `tb2-issue-38-body.md` (`27ee1f27a9b66903c263b3e5394d8e6dbdc672d429e82d5ca876fce71bcdf713`). Issue #38 is the stronger prior art: open, 2026-02-13, dwahdany, line 2 “Made instructions explicit that source should be extracted to `/app/pmars-<version>/` (not flattened into `/app/`) and left in place after building” (20 words) — exactly the 2.1 line-3 revision `R38ScoutUpstream` §2 measured, and it predicts the grader's one-level `/app/pmars-*` glob. #53 is the open 2.1 demo PR. Neither is a report about the grader, so neither makes the grader case a replication; a row needs a committed capture outside the C2 capture dir (V1 lists exactly five files and rejects extras) and an id. Flip: `<L1 fills>`. |
| Assimilation: `considerthese/2026-10-25.md` proposal 2(c) (tip-receipt validator) | **Held — rejected for this round** | The proposal asks for a validator that re-runs every `corpus/evidence/**` receipt and byte-compares it, “which would have caught D3 mechanically” (`considerthese/2026-10-25.md:39-45`). No claim in this round's freeze names it and no wave-1 seat built it (`grep -rn "tip-receipt" .ufo/waves/round-38/build/` → no hit). Its narrow form exists as C2 V2 + V5 + P10 over this round's single receipt; the lane-wide form needs its own counter and a receipt census, which would be an unmeasured landing. Flip: a round that freezes the validator together with a control that is red on a fabricated receipt. (Round 37 landed 2(a) as `plans/ledger_tip.py`; 2(b) and 2(c) remain unbuilt.) |
| Assimilation: `merge/kengaku/` re-screen | **Pending (`R38MergeRescreen`)** (`<L1 fills>`) | Receipts at `build/R38MergeRescreen/`: `c2-ids` = S115, S116; `c2-collisions` = S115, S116; `collisions` = 31 registry ids (S077–S086, S090–S094, S097, S100–S114) that already occupy ids inside the staged range `staged-ids` S077–S251. So the two requested ids collide with the staged catalogue, not with a landed row; whether that admits, renumbers or refuses them is the seat's disposition. Registry count it moves: `rows=107` → `<L1 fills>`. Flip: an admitted package whose bytes have not changed since its last screening, or a duplicate of ground the registry already holds. |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| order-of-operations — **recurrence** of `corpus/lessons/round-37.md:42`: the C2 skip-control executed the frozen probe before the first recorded run | `plans/round-38-claims.md:8-13` (disclosure): “the gate's P10 executed the frozen probe once inside the scratch clone at control time”; `control-c2-skip.txt` keeps `P10 DEFECT fresh probe output is not byte-equal to the receipt`. Corroborated here, not taken on the write-up: `git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt` → `fatal: path … exists on disk, but not in 'e0a37853'` (rc 128), so at the freeze commit no receipt existed while a committed control proves the probe ran; `git log --diff-filter=A --format='%H %cI' -- corpus/evidence/round38/build-pmars-probe.txt` → `e95cf550… 2026-10-26T02:38:41-03:00` | the claims header itself, self-disclosed before the freeze commit; no seat's receipt records the discarded execution, and the run happened in a scratch clone that was removed | the round-37 fix (re-pin the probe, re-run and byte-compare the receipt every counter run) did not prevent the recurrence, so the fix has to be an ordering rule with a check that is red on this freeze. Lint: any committed control under `.ufo/waves/round-38/claims/` whose text contains `fresh probe` requires `corpus/evidence/round38/build-pmars-probe.txt` to exist at that commit. Run at `e0a37853`: `git cat-file -e` rc 128 and `grep -l "fresh probe" .ufo/waves/round-38/claims/*.txt` → `control-c2-skip.txt` alone → **RED**. So a receipt-bearing control may only be built after the first recorded run's commit (or must carry no receipt at all, leaving P2/P10 red without any probe execution), and the claims must cite that commit — `e95cf550` today, re-derivable with the `git log --diff-filter=A` command above. Escape named: a control that reruns the probe without leaving the clause in its text still passes the lint; the stricter form is a counter guard that refuses `--rerun` unless the receipt's add-commit is a descendant of the freeze and is not the freeze itself. |
| witness-picked label — a requirement-map label chosen from one convenient case (round-37 closure D2) | `corpus/knowledge/tb2-git-webserver-grader.md:107` labels `instruction.md:9` `enforced` with cases `capitalised`, `leading-space`, while the same entry's receipt carries `CASE token-in-body … observed=pass`; the round-37 counter printed `V7 ok rows=4 bad=0`, `checks=7 defects=0` (`falsify/F37CritC2Map.md:15`), and the critic calls the row “the landing defect” (`:112`) | `F37CritC2Map` (wave-2 critic); the round-37 counter could not see it — its V7 asked only that a cited case contradict the label, never that the cited case be the only violating state | repaired in the round-38 counter, not in the round-37 entry: `plans/round38_c2_verify.py:239-243` builds `violating` from every case whose `violates=` set carries the tag and takes `want = derive(set(violating.values()))` (`:205-210`), so one observed-pass violating case forces `partly`. Falsifiable today: a row labelled `enforced` against this receipt is red, because all seven tags derive `partly` (7/15, 1/2, 7/15, 7/15, 1/3, 1/4, 7/15). Owed at landing: a wave-2 control on a relabelled map `<L1 fills>`; an appended erratum on the round-37 entry (still absent — `grep -n "Errata" corpus/knowledge/tb2-git-webserver-grader.md` → no hit) and a QUALITY criterion. Residual limit: four of the seven tags (`from-source`, `debian-source`, `extract-to-app`, `debugger-works`) are carried by all 22 cases, so their derived label is the overall 7/15 split rather than a discriminating state — V7 is only as good as the `violates=` tags, and a mechanical seven-times-`partly` map is correct by construction. |

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (freeze): exit 0, `kengaku ok`, 15 W04 — duplicate-URL warnings on S040, S048, S057, S058, S059, S064,
S065, S066, S067, S068, S069, S071, S075, S076, S100 (`.ufo/waves/round-38/claims/census-before.txt`). The set
is the same as round 36's: no new duplicate.

At drafting (this seat, same command): exit 0, `kengaku ok`, the same 15 W04 and no new one. Counts at drafting:
registry rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `107`; knowledge
files `ls corpus/knowledge/*.md | wc -l` → `44`; README index rows `grep -cE '^\| `knowledge/[^`]+` \|'
corpus/README.md` → `44`. S115 and S116 add two rows and the entry one knowledge file, so at landing the counts
are `109/45/45` `<L1 fills>` — the state C1's genuine fixture is sensitive to (it copies `corpus/`), which makes
one commit for row + entry + index row the consistent landing.

After: `<L1 fills>` (expected: exit 0, the same 15 W04, no new one).

## Spot-check

Pending — the non-author closure for this round follows the report (LEARNING.md: a seat the lane dispatched is
still the lane). Cheapest failing check first:

1. `python3 plans/round38_c1_verify.py --lane .` on a **clean clone** of the landing tip (no untracked files) and
   record `PINS …`, `BATTERY …`, `MUTANTS …`, `PREDICATE C1 …` verbatim. One command; fails loudest.
2. `python3 plans/round37_c1_verify.py --lane .` on the same clone: the round-37 predicate must still pass
   (no-harm). Claims §C1 kill rule requires it.
3. `python3 plans/round38_c2_verify.py --lane .` and record `checks=7 …`, `PREDICATE C2 …`. V2's `P10` line is
   the receipt's authenticity: confirm it names a *fresh* run, not a cached one.
4. `grep -nE 'b1run-|p3m-|p4a-|p4b-|p6m-|p7m-|d4m-|d5m-|mainx-|build-pmars|pmars' plans/pkg_gate.py` → expect
   empty: no gate path may name a fixture, a battery module or this round's evidence. (The gate is frozen, so
   this is a check on the landing, not a suspicion.)
5. Hand-run one mutant outside the counter: apply one frozen `old → new` replacement to a scratch copy of
   `plans/pkg_gate.py`, run it by hand on that mutant's fixture, and confirm the clause set moves in the
   declared direction (silence) or the clause flips `ok` → `DEFECT` (mirror). Round 36's closure left this
   unexecuted; round 37's §2 audit stood in for it again — this round should execute it once.
6. Recompute the probe's prediction/observation join from committed bytes: parse the 22 `CASE` ids from
   `corpus/evidence/round38/build-pmars-dry-cases-freeze.txt` and `…/build-pmars-probe.txt`, require the same
   ids in the same order, 7 `predicted=pass` against 7 `observed=pass`, and 0 disagreements (drafting state:
   exactly that, `mismatches=0`). Then read every `match=NO` id and confirm the entry names it — there is none
   today, so the entry must not claim a mismatch section it does not need.
7. Re-open S115/S116 live at the pin: `curl -s <url> | sha256sum` equals the row anchor, and `sed -n <line>p`
   equals the row quote. Two rows, two digests — and check the quotes are the two the entry actually carries.
8. Re-derive the entry's requirement map: for each of the seven tags take every receipt case carrying it and
   require the row's label to equal the derivation (`partly` for all seven from this receipt). This is V7 done
   by hand; if the entry's map differs from V7's derivation in one row, V7 is the authority and the row is wrong.
9. Re-read the claims' disclosure (`plans/round-38-claims.md:8-13`) beside `control-c2-skip.txt` and run the
   order lint above: no `fresh probe` control text may predate the receipt's add-commit.
10. Confirm no `corpus/` or `plans/` copy, and no lane mirror, sits under `.ufo/waves/round-38/build/`
    (`find .ufo/waves/round-38/build -maxdepth 2 \( -name corpus -o -name plans \)`).

## Close

Wave 1 (build + first falsifiers) is dispatched against the freeze; wave 2 (falsify) follows once wave 1 settles.
Nothing above rests on a wave-2 finding except where the row names one. Landing obligations left to the L1:
commit the wave-1 battery modules into `plans/battery38/` (one module per fixture family, unique fid prefixes),
land the entry with registry rows S115/S116 and the README/PROVINCE sentences in one commit, run both predicates
and the no-harm round-37 predicate on a clean clone, and fill every `<L1 fills>` above with the measured line.
The two Mistakes rows are this round's own mining: the order-of-operations recurrence has a red lint at the
freeze commit, and the witness-picked label has a counter that derives instead of trusting — both are still
write-ups until the closure re-runs them.
