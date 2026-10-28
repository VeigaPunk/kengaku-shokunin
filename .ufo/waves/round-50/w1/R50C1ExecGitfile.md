# R50C1ExecGitfile — gitfile / commondir leg proof (R50-C1, novelty)

Seat: `R50C1ExecGitfile` (executor, leaf). Item: prove the gitfile/commondir legs on their own against the
candidate fence, and emit a case table with exit/verdict.

**Axis named: novelty (R50-C1).** Coverage is not touched (operator cap). Nothing in the lane was edited.

---

## REV

    REV lane tip at measurement      c3372a9b24d3a200946a6b37dc0a31ed5c982cc1   (tip when the seat opened: 5c56819f)
    REV freeze                       3b02d573d58cc6d2e0d27ef92ac0815354912252   ancestor of both: verified
    REV tools measured from          git clone --shared of the lane, checked out at the freeze
    REV candidate measured (FINAL)  .ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py
                                     sha256 9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1
    REV candidate prior final       same path, sha256 6df6a2a331a66195cfeb963b457372596cd55ac1199d7d97027323a533a76ec2
    REV candidate intermediate       same path, sha256 ae47fc3e43aa9e98042c81dfd18a54b48bdaebf4763e25dbc067b99c99dc8d4b
    REV candidate first arrival      same path, sha256 2c4e40a057d7ed46c7b117c48e0890b91e5994e7aad9baea9198cfb9ab7e4e03
    REV base fence (control)         plans/fixture_fence.py @ freeze, sha256 05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
    REV git                          2.56.0

Ancestry check, verbatim:

    $ git merge-base --is-ancestor 3b02d57… HEAD && echo ok
    FROZEN_IS_ANCESTOR yes          # at 5c56819 (seat start) and again at c3372a9 (before the report)

The candidate is uncommitted work owned by sibling seat `R50C1ExecRepair`; it moved three times while I measured,
and **every digest was re-measured from a fresh clone and a fresh scratch tree rather than taken on the sibling's
word.** `2c4e40a0` is recorded in §4 because its defects are the ladder that found the four real gaps;
`ae47fc3e` fixed three of the four; `6df6a2a3` was identical to `ae47fc3e` (§2.1); **`9baedf13` is final and is
the digest this report's verdict names** (§2.2). The third pass also corrected a fixture defect of my own — see
§2.2 and §3/`f1`.

---

## VERDICT

**VERDICT — gitfile/commondir legs PROVEN on the final candidate `9baedf13` (§2.2): 15 of 16 cases decide as
required, each with a leg-specific reason. No escape is admitted and no honest class is refused. One row is a
declared-and-safety-neutral divergence (`f6`, no trailing newline: git accepts it, the fence admits it, git never
writes it) and one is a deliberate strict divergence (`f1`, CRLF: git tolerates it, the fence refuses it).**

* The two honest in-`d` shapes now admit: `n21` separate-gitdir (`gitdir: ../store`) and `n20` linked worktree
  (bare `gitdir` + `commondir` under `.git/worktrees/wt`, `repositoryformatversion = 1`).
* Every escape refuses with the leg's own reason, not a blanket rule: outside-`d` gitfile, gitfile→gitfile
  chain, `commondir` escaping `d`.
* The base fence `05d5fe03` scores 4 of 16 wrong (all over-refusals) and gets the refusals right only by
  refusing every `.git` FILE — zero discrimination between the legs.

---

## 1. Method

14 fixtures in the first pass, 16 in the final pass (§2.2), one per leg, each built by the same git invocations
git itself uses
(`git init --separate-git-dir`, `git worktree add --relative-paths`, `git worktree add`). Each fence is scored by
calling its `breach(d, argv, "anchor")` directly with the fixture dir and the argv tail the population module
would return (`["--lane", "wt"]` / `["--lane", "repo"]`). No fence is ever handed a dirty or live tree.

Two independent facts are recorded per case: what **git itself** does with the fixture, and what the **fence**
decides. The `git` column is the arbiter for "is this a state git writes", and it is measured with
`git -C <fixture> rev-parse --absolute-git-dir` plus, for every `.git` FILE in the fixture,
`git -C <worktree> rev-parse --path-format`-style `--git-path objects`.

That second probe is not optional: `commondir` is consulted only when git starts at the *linked worktree*. Asking
the main repo `--git-common-dir` returns `.git` for every fixture, escape included — my first pass did exactly
that and produced a false "commondir inside d" for case `e`. The corrected probe is what witnesses the leg.

Fixture git environment is per-child (copied from `plans/round44_c1_verify.py` `Ctx.ENV`):
`HOME=/nonexistent`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, pinned author/committer identity
and dates. This is not cosmetic — see §5.

---

## 2. Case table (first pass, 14 cases)

**§2.2 is the authoritative table** — it is the last digest, it has 16 cases, and it corrects the encoding
fixtures I got wrong here. §2 is kept because the `2c4e40a0` column is the evidence for §4.

`OK` = the fence's verdict equals the required verdict; `XX` = mismatch.

| # | case | leg | git accepts | required | base `05d5fe03` | cand `2c4e40a0` | cand `ae47fc3e` (= `6df6a2a3`) | delta4 (my reference rung) |
|---|---|---|---|---|---|---|---|---|
| a | n21 separate-gitdir (honest) | gitfile → store inside `d` | yes | **admit** | **XX** refuse | OK admit | OK admit | OK admit |
| b | n20 linked-worktree (honest) | gitfile → per-worktree dir + `commondir` inside `d` | yes | **admit** | **XX** refuse | **XX** refuse | OK admit | OK admit |
| b2 | n20, config normalised to version 0 | gitfile + worktree metadata alone | yes | **admit** | **XX** refuse | **XX** refuse | OK admit | OK admit |
| c | gitfile → store **OUTSIDE `d`** | gitfile escape | yes | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| d | gitfile → a **second gitfile** | gitfile chain | no | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| e | `commondir` relative escaping `d` | commondir escape | lane yes / worktree **no** | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| e2 | `commondir` escaping `d`, config normalised | commondir escape alone | lane yes / worktree **no** | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| f1 | gitfile with `\r` (CRLF) | gitfile encoding | no | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| f2 | gitfile with UTF-8 BOM | gitfile encoding | no | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| f3 | gitfile with trailing junk line | gitfile encoding | no | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| f3b | gitfile with trailing spaces (target = working tree) | gitfile encoding | no | **refuse** | OK refuse | OK refuse | OK refuse | OK refuse |
| f4 | gitfile **absolute path INSIDE `d`** | gitfile form | yes | **admit** | **XX** refuse | OK admit | OK admit | OK admit |
| f5 | gitfile trailing spaces → target **is a valid store** | parser-vs-git | **no** | **refuse** | OK refuse | **XX** admit | **XX** admit | **XX** admit |
| h | plain init (control) | ordinary store | yes | **admit** | OK admit | OK admit | OK admit | OK admit |

Verbatim run summary (`ae47fc3e` ladder, `work-v2`):

    CASES total=14 mismatched=5 fixture_fence.py=4 candidate-snapshot.py=3 candidate-v2.py=1 delta4.py=1

`delta4` is my scratch reference rung (§4); it carries the same `f5` divergence as the candidate because it
inherits the candidate's pointer parser, which is the point of that case.

### Reasons observed on `ae47fc3e` (verbatim; identical at `6df6a2a3`, and superseded at `9baedf13` by §2.2)

    c   refuse : wt/.git names '../../c_outside/store', which resolves outside the fixture
    d   refuse : wt/.git names '../hop1', which is not a directory
    e   refuse : repo/.git/worktrees/wt/commondir names '../../../../../e_outside/store', which resolves outside the fixture
    e2  refuse : repo/.git/worktrees/wt/commondir names '../../../../../e2_outside/store', which resolves outside the fixture
    f1  refuse : wt/.git carries a bare CR
    f2  refuse : wt/.git carries a non-ASCII byte
    f3  refuse : wt/.git is not a single line
    f3b refuse : store (via wt/.git)/.git is not a plain-init entry
    a, b, b2, f4, h  admit

These are the leg's own reasons. Compare the base fence, which returns the identical string for all ten refusal
cases:

    wt/.git is a file (gitdir redirect), not a directory

### What git measured, per case

    a   gitdir=a/store                                wt: —                                  (separate-git-dir)
    b   gitdir=b/repo/.git                            wt: accepts=True  objects_inside=True
    c   gitdir=c_outside/store                        wt: accepts=True  objects_inside=False   <- git resolves the outside store
    d   gitfile does not point to a valid repository  (git refuses the chain itself)
    e   gitdir=e/repo/.git                            wt: accepts=False objects_inside=False
    e2  same as e                                     wt: accepts=False objects_inside=False
    f4  gitdir=f4/store/.git                          wt: accepts=True  objects_inside=True
    f5  gitfile does not point to a valid repository  (git refuses the trailing-space line)

`c` is the important one: an outside-`d` gitfile is a state git **fully accepts** and resolves to a store outside
the fixture. Admitting it is a genuine read escape, which is why the fence must refuse it on the pointer, not on
a blanket `.git`-FILE rule.

### 2.1 Intermediate re-measurement (`6df6a2a3`; superseded by §2.2)

The sibling published `fence_candidate.py` as final at `6df6a2a3` after my `ae47fc3e` run, so I rebuilt the whole
table from a fresh scratch tree and a fresh clone at the freeze and re-scored both the base fence and the final
candidate. Verbatim:

    case git  require  fixture_fence.py         cand-final.py
    ------------------------------------------------------------
    a    yes  admit    XX:refuse                OK:admit
    b    yes  admit    XX:refuse                OK:admit
    b2   yes  admit    XX:refuse                OK:admit
    c    yes  refuse   OK:refuse                OK:refuse
    d    no   refuse   OK:refuse                OK:refuse
    e    yes  refuse   OK:refuse                OK:refuse
    e2   yes  refuse   OK:refuse                OK:refuse
    f1   no   refuse   OK:refuse                OK:refuse
    f2   no   refuse   OK:refuse                OK:refuse
    f3   no   refuse   OK:refuse                OK:refuse
    f3b  no   refuse   OK:refuse                OK:refuse
    f4   yes  admit    XX:refuse                OK:admit
    f5   no   refuse   OK:refuse                XX:admit
    h    yes  admit    OK:admit                 OK:admit

    CASES total=14 fixture_fence.py=4 cand-final.py=1

Every verdict is identical to the `ae47fc3e` column, so the sibling's "verdicts identical" statement is confirmed
independently rather than taken on trust. Reasons at `6df6a2a3`, verbatim:

    a, b, b2, f4, h  admit
    c   refuse : wt/.git names '../../c_store/store', which resolves outside the fixture
    d   refuse : wt/.git names '../hop1', which is not a directory
    e   refuse : repo/.git/worktrees/wt/commondir names '../../../../../e_outside/store', which resolves outside the fixture
    e2  refuse : repo/.git/worktrees/wt/commondir names '../../../../../e2_outside/store', which resolves outside the fixture
    f1  refuse : wt/.git carries a bare CR
    f2  refuse : wt/.git carries a non-ASCII byte
    f3  refuse : wt/.git is not a single line
    f3b refuse : store (via wt/.git)/.git is not a plain-init entry
    f5  ADMIT

(`c`'s directory is named `c_store` in the rewritten harness — a fixture-naming difference between my two runs,
not a behaviour change.) **`f5` was still open at `6df6a2a3`; it is closed at the final `9baedf13` (§2.2).**

Two notes on the sibling's other claims, for the integrator's arithmetic rather than mine: `refs/replace` being
admitted by `_refs` rather than by absence, and the worktree entry `locked` being refused, are theirs to witness
— my 14 cases contain neither an `refs/replace` ref nor a `locked` worktree entry (case `b`/`b2`'s worktrees
carry only `HEAD`, `ORIG_HEAD`, `commondir`, `gitdir`, `index`, `logs`, `refs`).

### 2.2 FINAL re-measurement (`9baedf13`) — and a correction to my own §2/f1 fixture

The sibling closed `f5` at `9baedf13` (git's prefix is now `b"gitdir: "` with the space, and the pointer text is
taken verbatim instead of stripped). I re-measured a third time, from a fresh clone at the freeze.

**That pass also caught an error of mine, and it is worth stating plainly.** My `f1`/`f2`/`f3`/`f3b` fixtures in
§1–§2 pointed at a plain `git init` repo — a *working tree* — rather than at a store. git therefore refused them
for the target, not necessarily for the encoding, so my §2 line "Measured: git 2.56 refuses CRLF" was
**over-determined and unsound**. The sibling's independent measurement disagreed (CRLF accepted), and they were
right. In the third pass those four cases are built with `git init --separate-git-dir` so the **only** difference
from honest case `a` is the bytes of the `.git` file; three more probes were added (`f6` no trailing newline,
`f7` no space after the colon, `f8` two spaces).

    case git  require  fixture_fence.py       cand-final.py
    --------------------------------------------------------
    a    yes  admit    XX:refuse              OK:admit
    b    yes  admit    XX:refuse              OK:admit
    b2   yes  admit    XX:refuse              OK:admit
    c    yes  refuse   OK:refuse              OK:refuse
    d    no   refuse   OK:refuse              OK:refuse
    e    yes  refuse   OK:refuse              OK:refuse
    e2   yes  refuse   OK:refuse              OK:refuse
    f1   yes  refuse   OK:refuse              OK:refuse
    f2   no   refuse   OK:refuse              OK:refuse
    f3   no   refuse   OK:refuse              OK:refuse
    f3b  no   refuse   OK:refuse              OK:refuse
    f6   yes  ADMIT?   OK:refuse              XX:admit
    f7   no   refuse   OK:refuse              OK:refuse
    f8   no   refuse   OK:refuse              OK:refuse
    f4   yes  admit    XX:refuse              OK:admit
    h    yes  admit    OK:admit               OK:admit

    CASES total=16 fixture_fence.py=4 cand-final.py=1

Reasons at `9baedf13`, verbatim:

    a, b, b2, f4, h, f6   admit
    c    refuse : wt/.git names '../../c_store/store', which resolves outside the fixture
    d    refuse : wt/.git names '../hop1', which is not a directory
    e    refuse : repo/.git/worktrees/wt/commondir names '../../../../../e_outside/store', which resolves outside the fixture
    e2   refuse : repo/.git/worktrees/wt/commondir names '../../../../../e2_outside/store', which resolves outside the fixture
    f1   refuse : wt/.git carries a bare CR
    f2   refuse : wt/.git carries a non-ASCII byte
    f3   refuse : wt/.git is not a single line
    f3b  refuse : wt/.git names '../store   ', which does not exist
    f7   refuse : wt/.git is not a `gitdir: ` redirect
    f8   refuse : wt/.git names ' ../store', which does not exist

Three things changed for the better between `6df6a2a3` and `9baedf13`, all witnessed here:

* **`f5`/`f3b` are closed and now refuse at the right layer.** `f3b` no longer reaches the store classification;
  the verbatim pointer `'../store   '` simply does not exist, which is git's own reason.
* **`f7`/`f8` refuse**, so the prefix is now git's literal `gitdir: ` including the single space. My earlier
  report did not test either; the sibling's tightening measured out.
* **`f1` (CRLF) now refuses a state git accepts.** See §3 — this is the deliberate strict divergence they
  declared, not a defect, and my previous justification for it was wrong.

`f6` is the one row that still disagrees with my required column, and it is a **judgment call, not a defect**:
git accepts `gitdir: ../store` with no final newline, the fence admits it, and admitting it is *safety-sound* —
the resolved store is inside `d`, so the fence's actual question is answered yes. It is only a divergence from
the strict "states git itself writes" reading, since git always writes the newline. The sibling declared this
choice deliberately; the integrator should record it as declared rather than have it discovered later. I have
left the required column at `refuse` (the strict reading) and marked the row `ADMIT?` so the disagreement is
visible instead of silently resolved in my favour.

---

## 3. Decisions and justification, per ambiguous case

The item asks me to decide the `\r`, BOM, trailing-junk and absolute-inside cases rather than read them off; I
added `f5`-`f8` because a verdict that matches the requirement for the wrong reason is not evidence (`f3b`/`f5`
were exactly that at `6df6a2a3`).

**f1 — `gitdir: ../store\r\n` → REFUSE, against git.** Corrected measurement (§2.2): with a valid store target,
**git 2.56 ACCEPTS the CRLF form**. My first pass reported the opposite and was wrong: that fixture pointed at a
working tree, so git's rejection was attributable to the target and not to the CR. The honest statement is
therefore: *git tolerates a bare CR on Linux (it trims trailing whitespace from the `gitdir:` line); the fence
refuses it.*

  * Decision: **REFUSE, as a declared strict divergence.** No git invocation writes a CRLF gitfile — git writes
    `\n` on every platform — so no honest fixture can carry one, and a refusal here can only ever over-refuse.
    The fence is deliberately *stricter* than git on a shape git never produces.
  * Why that is the right direction: the fence's contract is "states git itself writes". Refusing a state git
    merely tolerates costs nothing; admitting one would widen the allowlist for a shape no honest fixture needs.
  * Consequence for the claim: this must be **recorded as a divergence** in whoever lands the repair, the same way
    the population records host-sensitive entries — a critic looking for "fence agrees with git everywhere" would
    otherwise score this as a defect.

**f2 — UTF-8 BOM → REFUSE, with git.** Measured with a valid store target: git refuses with `invalid gitfile
format`, because the BOM breaks the literal `gitdir: ` prefix. Not a git-producible state. Refusing on
`any byte >= 0x80` (the candidate's rule) also covers UTF-16 and every other encoding that could smuggle a second
spelling of the prefix past the parser.

**f3 — trailing junk (a second line) → REFUSE, with git.** Measured with a valid store target: git refuses.
Independently of git, a second line is the only shape in which a single `.git` file could name two stores, so
"one line" is a structural bound, not just an encoding preference. `is not a single line` is the right reason.

**f3b / f5 — trailing spaces → REFUSE, with git, and now for git's own reason.** Measured with a valid store
target: git refuses `gitdir: ../store   `. At `6df6a2a3` the fence's `_pointer` stripped `' '`/`'\t'` before
resolving, so it admitted this (my `f5`) and refused only by accident when the stripped target happened to be a
working tree (my `f3b`, via `store (via wt/.git)/.git is not a plain-init entry` — right verdict, wrong layer).
**At `9baedf13` this is closed:** the prefix is git's literal `gitdir: ` including its single space and the
pointer text is taken verbatim, so the fence reports `names '../store   ', which does not exist` — the same
reason git gives. My `f5` handoff is discharged and I verified it rather than taking the fix on trust.

**f7 — no space after the colon (`gitdir:../store`) → REFUSE.** git refuses it; the fence reports
`is not a `gitdir: ` redirect`. This is the case that proves the prefix is git's *literal* 8 bytes and not a
tolerant variant; I had not tested it before the tightening.

**f8 — two spaces after the colon (`gitdir:  ../store`) → REFUSE.** git refuses it; the fence reports
`names ' ../store', which does not exist` (one leading space survives into the path). Correct, and correct at the
pointer layer rather than by falling through to the store classification.

**f6 — no trailing newline (`gitdir: ../store`) → ADMIT (the fence), with git; my required column says refuse.**
This is the one open judgment call and I am not going to resolve it unilaterally in either direction.
git accepts it. The fence admits it. Admitting is **safety-sound**: the pointer resolves to a store inside `d`,
which is the fence's actual question, so no read-escape is possible. It diverges only from the strict
"states git itself writes" reading, since git always terminates the line. The sibling declared the choice
deliberately; the integrator should either record it as declared or tighten to the written form. Either is
defensible; what is not defensible is leaving it unrecorded.

**f4 — absolute path inside `d` → ADMIT.** Measured: git accepts it, and the store it names is inside `d`. The
fence's question is "is the store provably inside `d`?", and an absolute path inside `d` answers it yes. Refusing
it would be an over-refusal of a state git accepts — the same over-refusal class the round is repairing. The
`2c4e40a0` candidate already admits it.

  * **Consequence, stated so it is not mistaken for a fence requirement:** this fixture is **not eligible for the
    frozen population**. The absolute path embeds the build root, so the identity pin of
    `plans/honest50/population.txt` cannot be reproduced across two builds; the population builder therefore
    rewrites `wt/.git` to a relative pointer before the first commit (that is exactly what
    `modules/novel50/n21_separate_gitdir.py` does). Admit-by-fence, exclude-by-builder: two separate constraints,
    both correct. I did not test whether the builder would in fact reproduce such a fixture; the statement is
    about the shape, and the population already excludes it by construction.

---

## 4. Defects found in the intermediate candidate `2c4e40a0` (ladder)

`2c4e40a0` refused both honest worktree classes. Rather than report "n20 refuses", I isolated each cause with a
delta fence in scratch, each adding exactly one fix. All four are one-file, few-line changes; `ae47fc3e` fixes
1–3 and 4's consequence, which is why it now scores 13/14.

| rung | change | case that exposes it | reason before → after |
|---|---|---|---|
| delta1 | `worktrees` added to `GIT_DIRS` | b2 | `repo/.git/worktrees is not a regular file` → next gap |
| delta2 | `[extensions] relativeWorktrees` + `repositoryformatversion 1` accepted | b | `core.repositoryformatversion must be 0` → next gap |
| delta3 | `worktrees/<name>/gitdir` parsed **bare** | b | `…/gitdir is not a 'gitdir:' redirect` → **admits b, b2** |
| delta4 | `_worktree` unpacks its `(target, reason)` helpers | e, e2 | delta3 **admits both commondir escapes** → refuses with the commondir reason |

**4a. `worktrees` is in `GIT_TOP` but not in `GIT_DIRS`.** `_store`'s entry loop therefore falls through to
`if not stat.S_ISREG(mode): return f"{label}/{name} is not a regular file"` and rejects the directory before the
`if "worktrees" in have:` hook at the bottom of `_store` ever runs — the hook is unreachable for every real
linked worktree.

**4b. `core.repositoryformatversion` pinned to `0`, `CFG_SECTIONS = {"core"}`.** `git worktree add
--relative-paths` writes, into the **main** repo's config:

    [core]      repositoryformatversion = 1
    [extensions] relativeWorktrees = true

So a real n20 is refused on its own main-repo config, before any pointer is read. Measured on both forms
(§`git worktree add` without `--relative-paths` leaves version 0 and writes absolute pointers). A tight repair
accepts version 1 only when the sole extension is `relativeWorktrees = true` — which is what delta2/delta3/delta4
do, and what `ae47fc3e` now does.

**4c. `worktrees/<name>/gitdir` is a BARE path; the candidate parses it as `gitdir:`-prefixed.** Measured with
`od -c` on both worktree forms:

    git worktree add --relative-paths
      wt/.git                              = "gitdir: ../repo/.git/worktrees/wt\n"     (prefixed, relative)
      repo/.git/worktrees/wt/gitdir        = "../../../../wt/.git\n"                    (BARE)
      repo/.git/worktrees/wt/commondir     = "../..\n"                                   (BARE)
    git worktree add
      wt/.git                              = "gitdir: /abs/…/repo/.git/worktrees/wt\n"   (prefixed, absolute)
      repo/.git/worktrees/wt/gitdir        = "/abs/…/wt/.git\n"                         (BARE)
      repo/.git/worktrees/wt/commondir     = "../..\n"                                   (BARE)

`gitdir` is bare in **both** modes, so `_file_ref(..., prefixed=True)` is wrong for every linked worktree git
writes, not only the relative one. Only a `.git` FILE is prefixed.

**4d. The short-circuit that hides the commondir leg.** `_worktree` does

    why = _file_ref(p / "gitdir", f"{label}/gitdir", p, d, True)
    if why:
        return why
    common, why = _dir_ref(p / "commondir", ...)

but `_file_ref` returns `(target, reason)`, so on **success** it returns `(PosixPath(...), None)` — truthy.
`_worktree` returns that tuple early and `commondir` is never evaluated; `breach()` passes the tuple up as its
reason. Witnessed directly against the loaded module:

    _dir_ref(commondir)  -> (None, "commondir names '…/e2_outside/store', which resolves outside the fixture")
    _worktree(wt)        -> (PosixPath('…/wt/.git'), None)      # returns the gitdir target, never reaches commondir
    breach(fixture)      -> None                                # i.e. ADMIT

This is the reason delta3 admits both escape fixtures. It also means the fence's stated reason contract ("refuse
(one-line reason)") is violated whenever an error path in `_worktree` fires: the caller receives a 2-tuple.
`ae47fc3e` unpacks both helpers and refuses `e`/`e2` with the commondir reason, so this is fixed at the digest I
report — recorded here because the fix is invisible unless the leg is exercised with a *reachable* worktree.

Minor, non-blocking, in the same region: `_store` ends with a duplicated `_objects(gd / "objects", …)` call
(two identical consecutive calls), and `_pointer` strips trailing whitespace that git keeps (`f5`).

---

## 5. Environment note that nearly invalidated the table

The host's global git config carries `rerere.enabled = true` and `rerere.autoupdate = true`. Under it **every**
`git commit` writes an empty `.git/MERGE_RR` and an `rr-cache/` directory into the repo. My first pass built
fixtures with the ambient environment and the base fence refused every one of them with

    repo/.git/MERGE_RR is not a plain-init entry

i.e. the unrelated host setting, not the leg under test. Measured both ways:

    rerere=host:  COMMIT_EDITMSG HEAD MERGE_RR config description hooks index info logs objects refs rr-cache
    rerere=off :  COMMIT_EDITMSG HEAD config description hooks index info logs objects refs

Two consequences:

1. My harness sets `HOME=/nonexistent`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` per child (the
   lane's own `Ctx.ENV`), and nothing is exported into a shared shell.
2. The frozen population cannot contain `MERGE_RR` — otherwise the base fence would refuse 126/126, not 113 —
   which is consistent with the builder using the same per-child isolation. Worth a critic's eye if any future
   fixture is ever built outside `Ctx`.

This is a host-shape observation, not a fence defect: `MERGE_RR`/`rr-cache` are not states `git init` writes.

---

## 6. Exact commands run

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C1ExecGitfile`, `TMPDIR` exported there, one `git clone
--shared` of the lane.

    # freeze ancestry, before any measurement
    git -C <lane> merge-base --is-ancestor 3b02d57… HEAD && echo FROZEN_IS_ANCESTOR yes

    # tools measured from a shared clone pinned at the freeze
    git clone -q --shared <lane> lane && git -C lane checkout -q 3b02d57…
    sha256sum lane/plans/fixture_fence.py        # 05d5fe03…

    # candidate arrival + pinning (it moved twice: 2c4e40a0 -> ae47fc3e -> final 6df6a2a3)
    sha256sum <lane>/.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py
    cp <candidate> candidate-v2.py

    # the case table: 14 fixtures, each fence scored through breach(d, argv, "anchor")
    python3 leg.py --work $S/work-v2 \
        --fence $S/lane/plans/fixture_fence.py \
        --fence $S/candidate-snapshot.py \
        --fence $S/candidate-v2.py \
        --fence $S/delta4.py --json $S/v2-rows.json

    # same 14 cases, rebuilt from a fresh clone against the FINAL candidate (§2.1)
    git clone -q --shared <lane> lane && git -C lane checkout -q 3b02d57…
    cp <candidate> cand-final.py && sha256sum cand-final.py    # 6df6a2a3…
    python3 leg2.py --work $S/wfinal --fence $S/lane/plans/fixture_fence.py \
        --fence $S/cand-final.py --json $S/final-rows.json

    # third pass, 16 cases, valid-store targets for the encoding cases (the f1 correction, §2.2)
    python3 leg3.py --work $S/w3 --fence $S/lane/plans/fixture_fence.py \
        --fence $S/cand-final3.py --json $S/rows3.json

    # git's own verdict per case, from the linked worktree (not the main repo)
    git -C <fixture>/<worktree> rev-parse --show-toplevel
    git -C <fixture>/<worktree> rev-parse --git-path objects

    # the two worktree pointer forms, byte level
    od -c <fixture>/wt/.git  <fixture>/repo/.git/worktrees/wt/gitdir  …/commondir
    grep -E 'repositoryformatversion|relativeWorktrees' <fixture>/repo/.git/config

Nothing was run against the live checkout; every fixture git call used `git -C "$D"` with `D` under scratch.

---

## 7. Limits

* **The candidate is a sibling's uncommitted file, not a lane artifact.** I report the final `9baedf13`
  (re-measured from a fresh clone and a fresh scratch tree, §2.2), with `6df6a2a3`, `ae47fc3e` and `2c4e40a0`
  scored too. It may still move. My clone is pinned at the freeze and the lane tree was never written.
* **The lane's `plans/fixture_fence.py` is a different repair** (another seat's uncommitted edit) and none of
  these numbers are about it. Everything here was measured against the base fence `05d5fe03` in a clone at
  `3b02d57`, so the two repairs are not comparable and must not be stacked on my evidence.
* **14 fixtures.** Thin by design — one per leg plus the controls that keep a leg from being masked. Not a
  population; it says nothing about the other 111 honest classes.
* **`commondir` is only witnessed from the linked worktree.** A main repo's `--git-common-dir` is trivially
  `.git`; treating it as evidence produced a false clean in my first pass.
* **`e`/`e2`/`f5` are states git fails on.** Their refusal cannot be derived from "git accepts it"; it rests on
  the unbounded pointer and on git's own rejection of the line. Stated so the cases are not read as escapes that
  git would honour.
* **`f4` admitted but population-ineligible** (absolute path embeds the build root). I did not test whether
  `build_honest_population.py` reproduces such a fixture; the population excludes the shape by construction.
* Host-sensitive where git output is: `relativeWorktrees` needs git ≥ 2.48 (2.56.0 here). The `gitdir`/`commondir`
  byte forms are a property of that version, and the table is pinned to it.
* Not observed: io_uring, host paths outside the scratch root, `--lane` values other than the two shapes used.
* The `delta1`–`delta4` fences are **scratch only** and are not deliverables; they exist to attribute a refusal
  to one cause at a time.

---

## 8. Files changed / scratch

* **Lane: no writes.** The only file this seat created under the lane is this report,
  `.ufo/waves/round-50/w1/R50C1ExecGitfile.md`.
* Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ExecGitfile` (clone at the freeze, three harness passes, 14+16
  fixtures, four delta fences, row JSON, table text) was removed before yield; nothing citable lives there.
* No tool installs or upgrades were needed (none performed).
* No commit, push, stash, checkout of the lane, or mutating git command anywhere.

**Handoff to `R50C1ExecRepair` / the integrator:** my `f5` handoff is discharged at `9baedf13` and verified
(`f3b`/`f5` now refuse with git's own reason). Two items remain, both *recording* rather than repair: (a) `f1`,
the fence refuses a CRLF gitfile that git tolerates — deliberate strict direction, must be written down as a
divergence or a critic will score it as a fence defect; (b) `f6`, the fence admits a newline-less gitfile that git
accepts but never writes — safety-neutral, needs a declared decision. Everything else in the 16-case table
matches with a leg-specific reason.

---

VERDICT: gitfile/commondir legs proven on the final candidate `9baedf13` (re-measured independently at each
digest: `2c4e40a0` -> `ae47fc3e` -> `6df6a2a3` -> `9baedf13`) — 15/16 cases correct with leg-specific reasons
(honest `n21` and `n20` admit; outside-`d` gitfile, gitfile chain and escaped `commondir` each refuse for their
own measured cause; BOM, second line, trailing spaces, no-space and two-space gitdir lines all refuse with git).
The two remaining divergences are declared, not latent: `f1` refuses a CRLF gitfile that git tolerates (strict
direction, only ever over-refuses) and `f6` admits a newline-less gitfile that git accepts but never writes
(safety-neutral, needs recording). My own `f5` handoff is closed and verified, and my first pass's "git refuses
CRLF" claim is retracted — it was measured against a working tree, not a store. Base fence `05d5fe03` is wrong
on 4/16, all over-refusals, and discriminates none of the legs.
