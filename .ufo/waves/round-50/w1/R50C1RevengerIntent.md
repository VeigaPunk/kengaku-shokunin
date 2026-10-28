# R50C1RevengerIntent — the base fence's intent for the five refused honest classes

seat: R50C1RevengerIntent (revenger, novelty) · round kengaku 50, hyaku run 11, wave w1 (v2) · 2026-10-28
claim served: R50-C1 (novelty; instrument + fence repair). **This seat claims no C1/C2 admission and edits no
production file.**
**Axes named:** noveltY — the axis is *reconstructed intent*: for each of the five documented git states the base
fence refuses, was the refusal a deliberate security boundary or a shape heuristic, quoted from the frozen text;
and second, *which of the five can be reopened without weakening a named refusal*, decided by measurement, not by
reading.

REV `3b02d573d58cc6d2e0d27ef92ac0815354912252` (stage-1 freeze) — every byte measured below is verified identical
at this revision and in a `git clone --shared` of the lane (`HEAD c3372a9b24d3a200946a6b37dc0a31ed5c982cc1`).

## 0. Freeze precondition (before any measurement)

```text
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git rev-parse HEAD                                          → c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD ; echo $?
FREEZE_IS_ANCESTOR

$ git clone --shared --quiet /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
$ test "$(git -C lane rev-parse --show-toplevel)" = "$PWD/lane" && echo TOPLEVEL-OK
TOPLEVEL-OK
$ git -C lane status --porcelain | wc -l                       → 0
```

Per-file freeze-check (freeze blob digest vs clone working-tree digest, all `SAME`):

```text
SAME plans/fixture_fence.py                        05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
SAME plans/honest50/build_honest_population.py     35e3de6059e4676133291c615fdac7b04342e7c43827ec1e70ac09f83267a70b
SAME plans/round44_c1_verify.py                    6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
SAME plans/round46_c1_verify.py                    ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508
SAME plans/round45_c1_verify.py                    7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d
SAME plans/honest50/modules/novel49/n17_replace_ref.py    9f38f07a016d711cffa0276186550c022640528dba3f9d84656a223213f46578
SAME plans/honest50/modules/novel49/n18_shallow_fetch.py  64ecb769c08075a89a68e3916a21606044acab041d74d5d589624a4c397d37ae
SAME plans/honest50/modules/novel49/n20_linked_worktree.py 75cc4fff53e68e5810c380b101ac333c79a48d633a96f43c205e70fa91ce577a
SAME plans/honest50/modules/novel50/n21_separate_gitdir.py fe248d925ce014a293024e62a3a1bf2005089d7705293420b4eff291450ef478
SAME plans/honest50/modules/novel50/n22_alternates_in_d.py 8a71b8759f39e31b3bfb810e1216505fb51c303ec83390ec00ba12f30486dda6
SAME plans/refusals46/f1_gitfile.py                bac0df8aa55e35de2964f0e98a8c461aa6eeeba9daa2f18ca113a383f24a4c8d
SAME plans/refusals46/f5_alternates.py             8d56f2f7d4c1e8dd5951d87e1d5e5443fa45721fc1da1a61abcd11320061eab4
SAME plans/refusals46/f7_commondir.py              c828c1010e38e17812374e8d5383d4fb04e8e37d0ad38915f46723b726eaa0f3
```

The fence under test is the frozen base fence `05d5fe03…`, byte-identical to `plans/fixture_fence.py` at the
freeze. Nothing measured here is the lane's newer fence.

## 1. The fence's stated intent — quoted, not paraphrased

All quotes are from `plans/fixture_fence.py` @ `05d5fe03…` unless named otherwise.

**(a) The boundary sentence is containment, and the allowlist is only its proof:**

> `"""Fixture fence (round-46 C1, variant A: allowlist): admit only a fixture whose git store is provably the`
> `shape a plain `git init` + commits writes inside `d`, and whose argv names nothing else.`

> `Round 45's fence named attack classes (commondir, alternates, `[include]` text) and was passed by nine held-out`
> `modules that spelled the same escapes differently: … Variant A inverts the burden: nothing is admitted until`
> `every byte the decision depends on has been classified against a small allowlist, and anything unclassified is`
> `refused.`

> `4. each collected store is classified entry by entry against a plain-init allowlist: … `info/exclude` only`
> `   (so no `alternates`), … This is what closes the CR/BOM/includeIf/attributesFile/worktree family.`

> `6. no git child is started at all: … The store classification is the proof instead.`

**(b) The proof argument, stated in `breach()` itself:**

> `The store classification below is the proof: a store that matches the plain-init allowlist cannot have its`
> `config, refs or objects anywhere but under `d`, so `rev-parse --show-toplevel`/`--git-common-dir` have nothing`
> `left to add.`

**(c) The helpers are lexical on purpose:**

> `# ---------- small path helpers (lexical only: no resolve, no follow) ----------`
> `def _linked(mode, nlink):"""A regular file with another name somewhere is not provably inside `d`: refuse it."""`

**(d) What the counters call the property (the contract, not the mechanism):**

- `plans/round45_c1_verify.py` docstring: *"a module is CLEAN only if every fixture it builds is refused AND the
  fence's whole process tree opens no path outside the fixture directory while deciding"*; a fixture that is
  refused while opening outside `d` is `READ`, not clean — *"An outside open is a successful
  open/openat/openat2/creat whose resolved path … lies under the build scratch … but not under `d`"*.
- `plans/round46_c1_verify.py` rules (f)/(g): *"B3 WHOLE SCRATCH ROOT: a touch is any path under the scratch root
  that is neither `d` nor under the harness directory"*; *"B5 STAT CHANNEL: stat, lstat, newfstatat, statx, access,
  faccessat(2), readlink(at), getxattr … are traced and count like opens."*

So the counters and the fence agree on one named property: **no path outside `d` is named, and no git child runs.**
The allowlist is an implementation strategy for that property, chosen because its completeness is checkable
byte by byte. Two different things are being conflated in the r50 population: *admission shape* (plain-init only)
and *containment* (nothing outside `d`). The five refused classes are all refusals of the first kind.

## 2. Per-class reconstruction

Gate = the exact rule that fires. "Named refusal sharing the gate" = a frozen hostile module whose refusal
depends on the same rule (i.e. what a reopen can weaken).

### n17-replace-ref

- Witnessed base reason: `repo/.git/refs/replace is not refs/heads or refs/tags`
- Gate: `_refs()` — `if name not in ("heads", "tags"): return f"{label}/{name} is not refs/heads or refs/tags"`.
- Stated intent: the allowlist sentence `refs/heads|tags (40-hex refs)` (docstring §4). Nothing in the docstring,
  the r45/r46 contracts or the r49 critic reports claims a security property about the ref *namespace*; the
  namespace set is a shape list.
- Named refusal sharing the gate: **none.** `grep -rln 'refs/replace\|replace' plans/refusals46 plans/sealed46`
  hits only `f15_objects_symlink_out.py` (plus its `__pycache__` copy), and only the English word in its docstring (*"…is renamed out of `d`
  … and replaced by a symlink"*); no fixture builds a replace ref, and no hit at all for `refs/replace` or
  `shallow`.
- **Verdict: shape heuristic.** One additive namespace entry; no pointer, no outside-`d` question.

### n18-shallow-fetch

- Witnessed base reason: `repo/.git/FETCH_HEAD is not a plain-init entry` — i.e. the fence refuses on
  `FETCH_HEAD`, **not** on `.git/shallow`. The class is a conjunction of four independent shape gates; the
  ablation below witnesses each: (1) `FETCH_HEAD`, (2) `.git/shallow`, (3) `[remote "origin"]` in config,
  (4) `refs/remotes` + its reflog directory.
- Gate: `_store()` — `if name not in GIT_TOP: return f"{label}/{name} is not a plain-init entry"`; `_config()`
  section allowlist; `_refs()` namespace list; `_logs()` `_log_name_ok()`.
- Stated intent: allowlist `HEAD, ORIG_HEAD, COMMIT_EDITMSG, config, description, hooks/, index, info/exclude …
  refs/heads|tags`. No boundary sentence names `FETCH_HEAD` or `shallow`; `FETCH_HEAD` is not even in `GIT_TOP`,
  so the refusal is an unclassified-entry side effect.
- Named refusal sharing the gate: **none** (`grep 'shallow'` over the 32 frozen hostile modules: 0 hits).
- **Verdict: shape heuristic, four times over.** The frozen class description ("`FETCH_HEAD`") understates it:
  allowlisting `FETCH_HEAD` alone leaves the class refused three more times (measured, V4/V5/V3/V8 below).

### n20-linked-worktree

- Witnessed base reason: `wt/.git is a file (gitdir redirect), not a directory`
- Gate: `_tree()` — `if name == ".git": return None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"`;
  next gate `_store()` `worktrees` (not in `GIT_TOP`); then `_config()` (`[extensions] relativeWorktrees = true`,
  `repositoryformatversion = 1`).
- Stated intent: docstring §3 — *"one walk of `d` proves the tree has no symlink and no special file anywhere, and
  collects every directory holding a real `.git` directory (a `.git` file is refused)"*, and §4 *"This is what
  closes the CR/BOM/includeIf/attributesFile/worktree family"* — the worktree family was named as an attack
  family, so this gate is deliberate at the *mechanism* level.
- Named refusals that die with the gate: `f1_gitfile.py` (`.git` FILE, store BESIDE `d`), `f7_commondir.py`
  (hand-written `commondir` → store beside `d`), `f18_wtmeta_out.py` (`git worktree add` metadata whose checkout is
  outside `d`). Quote, `f7_commondir.py`: *"the round-45 fence refuses any `.git/commondir` outright (no
  module-built repo needs one)"* — a rule justified by *population*, i.e. a heuristic that later became a named
  refusal.
- **Verdict: deliberate boundary at the mechanism level, over-broad at the state level.** Reopening it is a
  renegotiation: the same bytes that make n20 honest are the escape vector of f1/f7/f18, and only a containment
  test separates them (measured below).

### n21-separate-gitdir

- Witnessed base reason: `wt/.git is a file (gitdir redirect), not a directory` — the *same* rule and the *same*
  string as `f1_gitfile.py`'s refusal (`.git is a file (gitdir redirect), not a directory`).
- Gate: `_tree()` `.git`-file blanket rule. Second obligation (not a refusal, a hole): `store/` carries no `.git`
  entry, so `_tree()` never collects it and `_store()` never classifies it. A reopened n21 must add store
  classification — otherwise the store the fence is supposed to prove is simply unread.
- Stated intent: docstring §3 as above (`n21` docstring calls the rule out: *"The base fence refuses this class
  because any `.git` file is refused as a 'gitdir redirect'; the resolved target is inside the fixture, so that
  refusal is over-refusal."* — written by the class author, not by the fence).
- Named refusal sharing the gate: **`f1_gitfile.py` exactly** (same rule, target outside `d`).
- **Verdict: deliberate boundary (mechanism-level), and it is the *one* gate that cannot be relaxed by name.**

### n22-alternates-in-d

- Witnessed base reason: `lane/.git/objects/info/alternates present (object-store redirect)`
- Gate: `_objects()` — the `info` branch refuses *any* entry: `if inner: return f"{label}/info/{inner[0][0]}
  present (object-store redirect)"`.
- Stated intent: docstring §4 *"`info/exclude` only (so no `alternates`)"*; and the docstring's own history:
  *"Round 45's fence named attack classes (commondir, alternates, `[include]` text)"* — alternates is a named
  attack class, so the mechanism-level refusal is deliberate.
- Named refusal sharing the gate: `f5_alternates.py` (alternates naming a store outside `d`), and `sealed46/p_info_redirect.py`
  (objects/info symlinked outside) shares the `_objects` walk.
- **Verdict: deliberate boundary at the mechanism level, over-broad at the state level** — same structure as n20.

### Summary table

| class | rule that fires | rule's origin | named refusal on the same rule | reopen class |
|---|---|---|---|---|
| n17-replace-ref | `_refs` namespace list | allowlist omission | none | **pure shape** |
| n18-shallow-fetch | `GIT_TOP` / config / refs / logs (4 gates) | allowlist omission | none | **pure shape** |
| n20-linked-worktree | `.git`-file blanket, `worktrees`, `[extensions]` | named attack family (round 45) | f1, f7, f18 | **boundary-bearing** |
| n21-separate-gitdir | `.git`-file blanket (identical to f1) | named attack family | f1 | **boundary-bearing** |
| n22-alternates-in-d | `objects/info` refuses any entry | named attack class ("alternates") | f5, p_info_redirect | **boundary-bearing** |

## 3. Measurement: can each be reopened, and at what cost?

Instrument: two scratch candidate fences generated from the frozen fence by asserted, one-hit textual deltas
(`mkcand.py`, both `ast.parse` clean, both derived from `05d5fe03…` and nothing else):

- `cand_strict.py` — the relaxed allowlist **plus** a containment test (`STRICT = True`): a `.git` gitfile,
  `commondir`, worktree `gitdir` and every `objects/info/alternates` line is resolved lexically and must land inside
  `d`; the resolved store/objects dir is then classified by the fence's own classifiers (cycles guarded).
- `cand_loose.py` — byte-identical except `STRICT = False`: the *same* allowlist, containment test removed.

Fixtures are the frozen modules, built by the frozen builder (`build_honest_population.build_once`) at the freeze,
each handed to `breach(d, argv, tool)`.

```text
$ python3 driver.py lane WORK cand_strict.py extras/s50_03_refs_namespace.py,extras/s50_05_objinfo_unknown.py
cand_strict:
n17-replace-ref   anchor ADMIT
n18-shallow-fetch anchor ADMIT
n20-linked-worktree anchor ADMIT
n21-separate-gitdir anchor ADMIT
n22-alternates-in-d anchor ADMIT
f1-gitdir-outside order REFUSE .git gitdir target escapes the fixture
f5-alternates-outside order REFUSE lane/.git/objects/alternates names a store outside the fixture
f7-cd-accept order REFUSE lane/.git/commondir target escapes the fixture
f7-cd-reject order REFUSE lane/.git/commondir target escapes the fixture
f7-cd-anchor anchor REFUSE lane/.git/commondir target escapes the fixture
g3-wtmeta-out order REFUSE …/repo/.git/worktrees/g3-wt/gitdir target escapes the fixture
g4-cd-hidden order REFUSE repo/.git/modules is not a plain-init entry
s50-03-unknown-ref-namespace anchor REFUSE repo/.git/refs/weird is not refs/heads or refs/tags
s50-05-objinfo-unknown anchor REFUSE repo/.git/objects/info/packsets present (object-store redirect)

cand_loose (same allowlist, containment removed): the five ADMIT, and
f1-gitdir-outside ADMIT
f5-alternates-outside ADMIT
f7-cd-accept/reject/anchor ADMIT
g3-wtmeta-out ADMIT          ← four named refusals, six fixture instances, leaked
s50-03 / s50-05 REFUSE (unchanged — the namespace set still polices them)
```

**This is the discriminator.** Dropping the containment test changes *nothing* about the five honest classes and
everything about the hostile ones: it leaks f1, f5, f7 and f18. So for n20/n21/n22 the reopenable thing is not the
name but the *resolution*; for n17/n18 there is no resolution to do.

### Ablation matrix — which delta each class needs (measured on the same on-disk fixtures)

`V0` = `cand_strict`; `Vn` = the same source with exactly one delta reverted.

| variant (one delta reverted) | n17 | n18 | n20 | n21 | n22 | f1 | f5 | f7×3 | f18 |
|---|---|---|---|---|---|---|---|---|---|
| V0 strict | admit | admit | admit | admit | admit | ref | ref | ref | ref |
| V1 no gitfile resolution | admit | admit | **ref** `wt/.git is a file…` | **ref** `wt/.git is a file…` | admit | ref | ref | ref | ref |
| V2 no `refs/replace` | **ref** `repo/.git/refs/replace is not refs/heads or refs/tags` | admit | admit | admit | admit | ref | ref | ref | ref |
| V3 no `refs/remotes` | admit | **ref** `repo/.git/refs/remotes is not refs/heads or refs/tags` | admit | admit | admit | ref | ref | ref | ref |
| V4 no `FETCH_HEAD` | admit | **ref** `repo/.git/FETCH_HEAD is not a plain-init entry` | admit | admit | admit | ref | ref | ref | ref |
| V5 no `shallow` | admit | **ref** `repo/.git/shallow is not a plain-init entry` | admit | admit | admit | ref | ref | ref | ref |
| V6 no `worktrees` | admit | admit | **ref** `repo/.git/worktrees is not a plain-init entry` | admit | admit | ref | ref | ref | ref |
| V7 no alternates resolution | admit | admit | admit | admit | **ref** `…/objects/info/alternates present (object-store redirect)` | ref | ref | ref | ref |
| V8 no `[remote]`/`[extensions]` | admit | **ref** `…config section [remote] is not allowlisted` | **ref** `…config section [extensions] is not allowlisted` | admit | admit | ref | ref | ref | ref |
| V9 containment removed | admit | admit | admit | admit | admit | **LEAK** | **LEAK** | **LEAK ×3** | **LEAK** |

Two results matter for the r50 claim:

1. **n18 is four gates, not one.** The frozen description names `FETCH_HEAD`; V4/V5/V3/V8 show that allowlisting
   only that entry still refuses the class. A repair that reports "FETCH_HEAD reopened" without the other three is
   unmeasured, not repaired.
2. **V2 is the anti-"passes by absence" probe** a sibling seat asked for after finding a dropped `_refs` call: with
   `refs/replace` reverted, n17 refuses again — the allowlist entry, not a missing call, admits it. (Raised by
   `R50C1ExecRepair` in-flight; the probe here is independent.)

### Containment keeps the fence's own "no outside-`d`" property

`strace -f -y -e trace=file` on `breach()` of `cand_strict.py` over n20/n21/n22 (the three pointer classes):

```text
n20_linked_worktree: distinct paths outside d under the scratch root: 4
   33  <scratch>           (cwd: getcwd/import machinery)
    5  <scratch>/probe.py
    1  <scratch>/cand_strict.py
    1  <scratch>/__pycache__/cand_strict.cpython-314.pyc
n21_separate_gitdir: 4 (same four)
n22_alternates_in_d: 4 (same four)
```

No fixture parent, no sibling fixture, no resolved store outside `d` — the residue is exactly the harness and
module the frozen docstring names: *"the measured residue is only the interpreter importing the harness and this
module, before `breach` runs"*. (This is a file-op trace, not the r46 B3/B5 counter; that counter is supplementary
evidence under R50-C1, not this seat's predicate.)

## 4. Answer to the item

**Which of the five can be reopened without weakening a named refusal.**

- **Without a named-refusal cost (pure shape heuristics, no pointer semantics): `n17-replace-ref` and
  `n18-shallow-fetch`.** They are additive allowlist entries — a ref namespace (`refs/replace`, 40-hex file names
  already enforced by `_ref_tree`) and content-shaped files (`.git/shallow` 40-hex lines; `FETCH_HEAD`; `[remote
  "<n>"] url/fetch`; `refs/remotes` + its reflog dir). No frozen hostile module uses either shape, both stay
  refused in every ablation, and the namespace police still holds: `refs/weird` is refused under every variant
  (V0–V9).
- **Only with a containment resolution (deliberate mechanism-level boundaries): `n20-linked-worktree`,
  `n21-separate-gitdir`, `n22-alternates-in-d`.** Each shares its gate byte for byte with a named refusal — n21 with
  `f1_gitfile` (same `.git`-file rule), n22 with `f5_alternates`/`p_info_redirect`, n20 with `f1`+`f7`+`f18`. The
  reopen is admissible **iff** the fence gains an explicit resolve-and-contain step (lexical normalisation, target
  must be inside `d`, target then classified by the fence's own store/objects classifier, cycles guarded) and
  **iff** the proof sentence changes with it: "a store matching the plain-init allowlist cannot have its config,
  refs or objects anywhere but under `d`" no longer holds when the store may be named by pointer; the new sentence
  must be "every pointer is resolved, contained, and its target classified". Measured: with that step, f1/f5/f7/f18
  all refuse on containment (V0); without it, all four leak (V9).
- **Nothing here requires a *git child***. The containment step is lexical resolution + `lstat`, so the "no git
  child" claim (§6 of the docstring) and the r46 B3/B5 property survive — witnessed above by the trace.

Two corollaries the integrator can use before S2:

1. Any repair must keep a **positive** probe per reopened class (V2/V7 style: revert the allowance, require the
   class to refuse again). The frozen 32 hostile modules do not cover the "admitted by absence" failure mode.
2. The in-flight blind modules `plans/sealed50/s50_03_refs_namespace.py` and `s50_05_objinfo_unknown.py`
   (untracked working-tree files at report time — **not frozen**, read-only observation) already police exactly
   the two namespace reopenings: both stay refused under every candidate above. They are the right police for
   n17 (namespace) and n22 (objects/info) and should be kept as-is.

## 5. Divergences and risks (routed, not acted on here)

- **The lane's fence is no longer the frozen fence in the working tree.** At report time
  `sha256sum plans/fixture_fence.py` → `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`
  (533+/117− vs `05d5fe03…`, uncommitted). My clone is clean at the freeze bytes and **nothing here measures or
  endorses that file**. A sibling seat (`R50C1ExecRepair`) reports a textually incompatible candidate
  (sha256 `9baedf13…`); two repairs must not be stacked. `[Peer-reported: not re-measured by me.]`
- **The r50 claims' class descriptions undercount n18's gates** (`FETCH_HEAD` only; measured: four).
- **The fence's refs message is a literal**: after widening `REF_DIRS` the refusal text still prints "is not
  refs/heads or refs/tags" — a repair must update the message, or a receipt reader will mis-attribute a refusal.
- **A reopened n21 leaves a store that `_tree()` does not collect** (`store/` holds no `.git`). Resolution must
  feed that store into `_store()`; my candidate does, and the trace shows no outside access, but a repair that
  only relaxes the `.git`-file rule would leave an unvalidated store inside `d`.
- **Config grammar widening is a real (small) cost**: n18 needs `[remote "<n>"]` and n20 needs
  `[extensions] relativeWorktrees = true` + `repositoryformatversion = 1`, which requires the value charset to
  admit `/ + * :` (refspecs). Every config *escape* stays refused in the measured matrix (`[include]`,
  `includeIf`, `core.attributesFile` are different sections/keys), but the widened grammar is a larger surface
  than the frozen one and should be the mutant battery's business, not assumed.
- Peer-reported (not my measurement): on the sibling candidate the carried r49 mutant battery reads
  `total=23 caught=1 broken=15` — the mutant floor is still unmet and needs witnessed re-derivation.

## 6. Limits

1. This is an intent reconstruction plus a nine-variant scratch ablation. **No scored counter run** (`round50_c1_verify.py`),
   no 20-module REFUSALS leg, no 12-module SEALED leg, no C2 audit. The four leaked named refusals under V9 are
   the four modules I built (f1, f5, f7×3, f18), not a claim about the other 16.
2. `s50_03`/`s50_05` are untracked working-tree files (S2 in-flight); the evidence they supply is their *text*,
   labelled not-frozen. They were built from copies in my scratch; the lane has no committed copy to pin.
3. The ablation table is about *necessity per delta*, not a minimal repair: my candidate is a demonstration, not a
   landing patch, and it deliberately does not touch host/mount paths, detached-HEAD config, `commit-graph`, or
   `info/refs` (classes outside my item; a sibling seat covers them).
4. `_objects` recursion for alternates chains is cycle-guarded by a per-call `_OBJ_SEEN` set; depth is otherwise
   unbounded — acceptable for the demonstration, not assessed for pathological chains.
5. Host git 2.56.0, Python 3.14.8; fixture semantics are "states git writes here", not cross-version.
6. No tools installed or upgraded; no pacman transaction attempted.

## 7. Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1RevengerIntent` (one `git clone --shared`, `status --porcelain` empty;
`mkcand.py`, `driver.py`, `ablate.py`, `cand_strict.py`, `cand_loose.py`, the built fixture trees and the strace
logs) is removed before this seat yields. Every command and every observed line needed as evidence is embedded
verbatim above; no scratch path is cited as evidence.

**VERDICT: intent reconstructed and measured. n17 (refs/replace) and n18 (FETCH_HEAD + shallow + remote config +
refs/remotes — four gates, not one) are allowlist shape heuristics and reopen at zero named-refusal cost; n20, n21
and n22 are deliberate mechanism-level boundaries that share their exact rules with f1/f5/f7/f18 and reopen only
under an explicit resolve-and-contain step (witnessed: strict = 5 admitted, 6 named-refusal instances still
refused; containment removed = same 5 admitted, f1/f5/f7/f18 all leaked). No C1/C2 admission claimed; no production
file touched; REV 3b02d573d58cc6d2e0d27ef92ac0815354912252.**
