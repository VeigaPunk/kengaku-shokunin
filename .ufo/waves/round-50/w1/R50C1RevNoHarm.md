# R50C1RevNoHarm — reviewer: plausible harm from admitting R50-C1 (novelty)

REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78 (lane tip at measurement; `TREE dirty=0` in the clone)
FREEZE 3b02d573d58cc6d2e0d27ef92ac0815354912252 — `git merge-base --is-ancestor` → **yes**, an ancestor of the tip
FENCE under test `plans/fixture_fence.py` 57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1 (was 05d5fe03…, the base fence at the freeze)
COUNTER `plans/round50_c1_verify.py` d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2
MUTANTS `plans/mutants50/c1-mutants.json` e885f0a6e69e33af55519279c5efab5f8dd8950df95b1e08a41e39e3043f5ccb (15 rows); `plans/sealed50/` 18 modules
SEAT R50C1RevNoHarm · reviewer · read-only against a `git clone --shared` of the lane · scratch `/fast/scratch/hyaku/kengaku-r50/R50C1RevNoHarm` (removed before yield)

Axes named (my judgement rubric, one line each):
- **A1 refusal strength** — every module the base fence refused must still be refused, and for the *same reason class*, after the repair.
- **A2 isolation** — the repaired fence must still make **no outside-`d` syscall at decision time and start no git child** (the base fence's load-bearing property; r45/fence docstring).
- **A3 repo integrity** — the landed round-50 artifacts must not bloat the lane materially nor embed host-specific bytes that make the claim un-re-runnable.
- **A4 novelty attribution** — the novelty step must not re-credit round 48's already-measured honest leg or the 120 carried fixtures as new evidence.

---

## 0. What I measured, and the revision it was measured at

The lane moved twice while this seat ran: at seat start the tip was `c3372a9` (fence still the base `05d5fe03`); S2 landed as `6db0279` (fence repair to `57adce4a`), the mutant freeze as `d6f2fce`, the scored receipt + LOG as `d45c5bb`. **All numbers below are from a clean `git clone --shared` checked out at `d45c5bb`**, re-verified by my own run:

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE …/lane/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
```

Command: `cd <clone> && python3 plans/round50_c1_verify.py --lane . --work /fast/scratch/hyaku/kengaku-r50/R50C1RevNoHarm/work` (8.8 s). The committed receipt `corpus/evidence/round50/c1-receipt.txt` records the same lines at `d6f2fce`; my independent run at `d45c5bb` reproduces it line for line. **The claim's stated predicate is reachable and non-trivial** — that is the precondition for the harm analysis, not the analysis.

Non-triviality (saturation) check, run at the same revision with `--fence` pointed at the three committed controls:

| control | HONEST | REFUSALS | SEALED 46/50 | verdict |
|---|---|---|---|---|
| `admit_all` | 126 admitted | **0 clean, 34 leaked** | **0/0 clean, 15/22 leaked** | fail |
| `refuse_all` | **0 admitted, 126 refused** | 20/20 | 12/12 + 18/18 | fail |
| `keyed_names` | 123 admitted, **3 refused** | **7 clean, 25 leaked** | **6/8 clean, 9/10 leaked** | fail |

So `admitted=126 refused=0` is not saturation: every leg can fail. (Weak-control note, not a harm: `keyed_names` refuses only 3 of 126 honest fixtures, so its honest-leg coverage is thinner than its name suggests; its failure comes mostly from the hostile legs.)

---

## A0 — instrument drift observed at measurement time (finding, medium)

At `d45c5bb` the **committed** counter is `plans/round50_c1_verify.py` `d8787b34…` — the digest the S3 receipt and the claims file name, and the one my clone ran. The **live lane working tree** carried an uncommitted modification of that same file while this seat measured:

```
 M plans/round50_c1_verify.py      (sha256 850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999)
 59 insertions, 15 deletions: HARNESS subprocess per decision + FENCE_TIMEOUT=120, Q39 name hiding
 (random per-module parent token, PAD=8 decoy sibling dirs), secrets import
```

This is another seat's in-flight repair responding to `R50C1CritPredicate`'s measurement that a directory-name-keyed fence passes the `--skip-mutants` mode. It is a **good** change; the problem is procedural: the claim's open-window table closes instrument repairs at S2, and the scored receipt is S3. A counter change after the scored run means the tree no longer contains the instrument that produced `corpus/evidence/round50/c1-receipt.txt`.

Exact check: `git show <tip>:plans/round50_c1_verify.py | sha256sum` must equal the digest named by `corpus/evidence/round50/c1-receipt.txt` and by the claims file (`d8787b34…`), and `git status --porcelain -- plans/round50_c1_verify.py` must be empty. If the change lands, the receipt must be re-run on a clean clone of the commit that carries it, and the claims file's open-window table must record old→new digest with the measured defect (it already has one such row for `f9b9873e…`→`d8787b34…`, so the format exists). Until then the receipt evidences a counter that is not at the tip.

---

## A1/A2 — does the repaired fence weaken any refusal? **No frozen refusal weakens; three base-refused shapes are newly admitted, one with a path-bearing payload.**

### A1.1 Before/after verdict vector over every hostile fixture (the item's literal ask)

Method: one build of every fixture from the frozen population and from `plans/refusals46` / `plans/sealed46` / `plans/sealed50`, evaluated against **both** fences in the same process — `05d5fe03` (base, extracted from the freeze) and `57adce4a` (landed). Fixtures: 126 honest + 34 + 15 + 22 = 197.

Result: **71 hostile fixtures — 0 flipped `BREACH → ADMIT`. 34 refusal-fixture verdicts and all 15+22 sealed verdicts are unchanged.** The 20 refusal *modules* and the 12+18 sealed *modules* are therefore not weakened at the verdict level. The 13 changes are all honest `BREACH → ADMIT`:

```
HFLIP n03-detached-head  n07-reflog-gc  n08-tag-detached  n12-local-config-user  n13-remote-origin
HFLIP n14-stash-entry    n15-commit-graph  n16-notes-ref  n17-replace-ref  n18-shallow-fetch
HFLIP n20-linked-worktree  n21-separate-gitdir  n22-alternates-in-d
```

**Finding A1-1 (scope understatement, low).** The claim prose says the base fence refuses "the five honest classes" (`n17`,`n18`,`n20`,`n21`,`n22`); the measured refusal set is **13 fixtures / 12 classes** (`n03`,`n07`,`n08`,`n12`,`n13`,`n14`,`n15`,`n16`,`n17`,`n18`,`n20`,`n21`,`n22`). The repair therefore widens **twelve** allowlist decisions, not five (detached HEAD, `info/refs`, `objects/info/{commit-graph,packs}`, `[user]`/`[remote]` config, reflog namespaces, `refs/replace`, `FETCH_HEAD`+`shallow`, `.git`-file store, `commondir`, `worktrees/`, `[extensions] relativeWorktrees`+`repositoryformatversion=1`, alternates-inside-`d`). The claims file's `Before` line (113/13) is correct; only the *narrative* compression is wrong, and it matters because it understates what the review must check.

### A1.2 Which widening is guarded by what — measured ablation table

I re-implemented a plausible careful repair as a scratch candidate (`/fast/scratch/…/cand/repair_emul.py`, monkeypatch of the base fence, 10 widenings) to *attribute* guards; then removed one guard at a time (`ABLATE=<guard>`) and re-scored. Candidate reaches the target itself (`HONEST 126/126`, `REFUSALS 20/20`, `SEALED 12/12`, `PREDICATE pass`), i.e. **the target is attainable without weakening any frozen refusal — the harm is conditional on implementation, not inherent to the claim.**

| guard dropped (widening kept) | HONEST | REFUSALS | SEALED | leak caught by |
|---|---|---|---|---|
| `gitfile` (inside-`d` containment of a `.git` file) | 126 | 19 clean | 12 | `f1_gitfile` ADMIT |
| `wtdir` (`worktrees/<id>/gitdir` containment) | 126 | 19 clean | 12 | `f18_wtmeta_out` ADMIT |
| `alternates` (containment of alternates entries) | 126 | 19 clean | 12 | `f5_alternates` ADMIT |
| `config` (`[user]`/`[remote]` free text) | **122** | 20 | 12 | HONEST leg only |
| `head` (detached HEAD) | **124** | 20 | 12 | HONEST leg only |
| `commondir`, `objinfo`, `extensions`, `notes`, `replace`, `inforefs` | 126 | **20** | **12** | **nothing** |

Read: the three *containment* guards are pinned by frozen hostile modules; the *allowlist* widenings (commondir content, `objects/info` entries, `[extensions]` keys, reflog namespaces, `refs/replace` validation, `info/refs` content) were — at the time I ran this on the base fence — invisible to the counter. The landed repair answers this with `plans/sealed50/` (18 blind modules authored in this wave, including `b1_replace_ref_target_outside_store`, `s50_05_objinfo_unknown`, `s50_10_reflog_name`, `s50_alternates_dotdot_abs`, `s50_gitfile_symlink_chain`, `s6_second_store_mount`) — all 22 sealed50 fixtures refuse at the tip. The ablation table is still the derivation of *which* check each of them must be exercising, and my finding is that this mapping is now implicit: **no artifact states "guard G is pinned by module M"**, so a later refactor can keep 18/18 green while moving the decision to a different rule.

**Finding A2-1 (medium, claim-file gap).** The claim does not record the guard→module mapping that makes the sealed set load-bearing. Exact check (mechanical, cheap): for each guard in the repair, delete it in a scratch copy and require the counter to report `REFUSALS`/`SEALED ... clean < total`; any guard whose deletion leaves all legs green is unpinned and must get a module before S2 claims closure. My table above is that derivation for the base fence; it must be re-derived on `57adce4a` (the landed fence has 12 guard sites spread over ~420 added lines, so the base-derived table cannot simply be copied).

### A1.3 A2 — isolation: no git child, no outside syscall at decision time

`strace -f -e trace=execve,openat,newfstatat,lstat` around a driver that **only** imports `plans/fixture_fence.py` and calls `breach` on a hostile fixture whose `commondir` names an existing directory **outside** `d` (`p1-commondir-outside`, built in scratch):

```
RESULT=repo/.git/worktrees/wt/commondir names a common dir outside the fixture
execve: 1                       (the python interpreter; no git child)
outside-target syscalls: 6      (/etc/ld.so.cache, /etc/localtime — interpreter startup, before breach)
syscalls naming the outside commondir target: 0
```

The containment test is **lexical and ordered before any stat**, so refusal does not read the outside path. The base fence's central promise survives the repair. This is the one property I would have blocked the claim on; it holds.

### A1.4 Three base-refused shapes that the repair now admits (independent probes, live at `57adce4a`)

Each probe is a scratch fixture built with the round-44 builder contract and run through both fences:

| probe | base | repaired | harm |
|---|---|---|---|
| `p4` `.git/FETCH_HEAD` = `0000…\tnot-for-merge\tbranch 'x' of file:///etc` | BREACH "not a plain-init entry" | **ADMIT** (no reason) | **medium-low** |
| `p7` `worktrees/wt/commondir` = `.` (self-cycle) | BREACH (`.git` file) | **ADMIT** | low |
| `p8` `.git` FILE naming the primary store `repo/.git` (git writes `…/worktrees/<id>`) | BREACH (`.git` file) | **ADMIT** | low-medium |

- `p4` matters because `FETCH_HEAD` is **the one newly admitted file whose payload is a path/URL**, whereas the base fence's declared limit ("`index`, `COMMIT_EDITMSG`, `description`, `logs/*`, packs … the tool run behind this fence reads none of them for a path") was stated for files that carry no path. I checked the lane's tools: `git grep -l FETCH_HEAD` finds **no production reader** (only historical wave documents), so today the widening has no reachable consumer. Exact check to keep it that way: a lane test asserting `no tracked non-fixture file parses FETCH_HEAD` (or, stronger, validating each admitted `FETCH_HEAD` line as `40-hex <TAB> (not-for-merge|<branch…>) <TAB> …` with any path contained in `d`), plus the same test for `shallow` (40-hex lines only) and `objects/info/packs`.
- `p7`/`p8` matter because the fence's own scope is "states git itself writes": `commondir = .` and a `.git` file naming the primary store are states git does **not** write, and the repair admits them. Exact check: require the back-pointer pair to agree — the store named by a worktree `.git` file must live under `<common>/worktrees/<id>`, whose `gitdir` names that same file; and `commondir`, resolved, must be a store that (i) contains `objects`+`refs`+`HEAD` and (ii) is not the worktree store itself.

**Finding A1-2 (Verdict-relevant).** (a) is **not** weakened at the frozen-set level (0/71), and the repair is isolation-clean; the residual harm is exactly the three admitted shapes above, of which only `p4` has a path-bearing payload, and it has no production consumer today.

---

## B — does landing a 126-fixture population bloat the repo or encode host-specific bytes?

### B1 Bloat: negligible

| measure | value |
|---|---|
| `plans/honest50/` in the tip tree | 155 files, **361,227 bytes** (126 JSON receipts = 123,121 B; modules + population + builder + receipt = rest) |
| `plans/sealed50/` + `plans/mutants50/` | 19 files, 50,575 B |
| all files added by round 50 (`git diff --name-only --diff-filter=A 71f5f5f d45c5bb`) | 197 files, **1,010,868 bytes** added |
| whole tip tree | 18,047 files, 556,712,671 B |
| round-50 share of the tree | **0.18 %** |

The population is **not** stored as fixture bytes: no `.git` object of any fixture is committed; 126 rows of `HONEST <tree_sha256> …` are rebuilt from 44 modules at run time (~20 s). This is the right shape and I see no bloat harm. Repo-level check to keep it that way: `git ls-tree -r -l HEAD -- plans/honest50 | awk '{s+=$4} END{print s}'` must stay under ~1 MB, and no `.git/` path may ever appear in `plans/honest50/` (`git ls-tree -r --name-only HEAD -- plans/honest50 | grep -c '/\.git/'` = 0).

### B2 Host-specific bytes: **witnessed, and it is the stronger harm of axis (b)**

Every one of the 126 pinned trees embeds bytes copied from **this host's git installation**:

```
fixtures=126 with-hook-samples=126 with-info-exclude=126 with-info-packs=1
n10-empty-repo  hooks/pre-commit.sample         fixture=57185b7b9f05239d  template=57185b7b9f05239d  equal=True
n10-empty-repo  hooks/fsmonitor-watchman.sample fixture=9159720099ad5595  template=9159720099ad5595  equal=True
n10-empty-repo  info/exclude                    fixture=6671fe83b7a07c89  template=6671fe83b7a07c89  equal=True
```

(template dir `/usr/share/git-core/templates`, `git version 2.56.0`; `plans/round44_c1_verify.py` `Ctx.ENV` fixes `PATH`/`HOME`/`GIT_CONFIG_*` but sets **no** `GIT_TEMPLATE_DIR`, so `git init` copies the host install's samples and drops the comment header of `info/exclude`.)

Consequence: `tree_sha256` pins are a function of the host's git template bytes. On any host whose templates differ (a different git release, a distro-patched template, `init.templateDir`), `POPULATION mismatched>0` and the **frozen kill rule fires → the round is not admitted**, not "the host is different". The claim's `Named limits` paragraph states the host sensitivity ("hooks/*.sample, info/exclude, git worktree --relative-paths ≥ 2.48, git 2.56.0 here; identity pins make that visible rather than silent") — so this is disclosed, not hidden. But disclosure is not containment: the claim is **only re-runnable on a host with git 2.56.0 and unmodified Arch templates**, which no artifact pins as a precondition.

Exact checks:
1. `GIT_TEMPLATE_DIR` must be set by the builder to a lane-frozen template tree (or the two template files frozen under `plans/honest50/templates/`), and the population rebuilt; then `POPULATION mismatched=0` must hold on a host with a different `git --version`. Cheaper interim: record `git --version` **and** `sha256sum /usr/share/git-core/templates/hooks/*.sample /usr/share/git-core/templates/info/exclude` in `plans/honest50/builder-receipt.txt` (the receipt already has `HOST git=git version 2.56.0 …` but not the template digests) so a mismatch is diagnosable in one command instead of a 126-row diff.
2. `plans/honest50/builder-receipt.txt:289` records `MODULES dir=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/honest50/modules` — an **absolute host path** in a committed artifact. Low severity (a receipt, and the lane already carries absolute host paths in 183 tracked files under `plans/`/`corpus/`/`scripts/`, so this is the standing convention rather than a new class), but the round-50 rule for reports is that citable evidence lives in the lane tree; the receipt line should record `MODULES dir=plans/honest50/modules` (lane-relative) so the receipt is portable. Check: `git grep -c '/home/vgpnk' -- plans/honest50/builder-receipt.txt` → 1 (measured); expected 0 after the fix.
3. Hygiene observation (not a defect of this claim): running the counter against the **live checkout** writes `plans/honest50/modules/**/__pycache__/*.pyc` (24 files present in the working tree when I started; `.gitignore:2` covers them, `git status --porcelain` is unaffected). Seats are told to use a clone; the wave's own runs evidently did not. Check: `git status --ignored --porcelain | grep -c __pycache__` must be 0 on a lane that only ran the counter in a clone.

---

## C — does the novelty claim double-count round 48's honest leg?

Facts (from `SCORECARD.md`, cited, not restated from the claim):
- r48 row (`SCORECARD:2104`): "base fence on the 120-fixture candidate population: `HONEST fixtures=120 admitted=112 refused=8`; repair candidate: 120/120 admitted … **unverified / not admitted**".
- r49 row (`SCORECARD:2119`): "Base fence on r48 population: 120/112/8; variant-A candidate 120/120 … New population is 124 … **not admitted / unverified**".
- r50 claim text: "Round 48 measured, **for the first time**, that the landed fence also *over-refuses*" and "Round 49 built the population to 124 and a counter contract but never landed a repair or a scored run".

Provenance split of the 126 rows (`builder-receipt.txt` `COUNTS` line, matching the population file): `battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 novel49=4 novel50=2`. **120 of 126 rows (95.2 %) are carried fixtures from rounds 42–48**; the r50-new evidence is 2 fixtures (`n21`,`n22`), 18 blind sealed modules, a committed counter, and a landed repair.

**Finding C-1: the claim text does not double-count** — it explicitly credits r48's measurement and states r49's failure to land. The novelty being claimed is *the committed instrument + frozen denominator + blind sealed set + witnessed mutant floor + a landed repair*, which r48/r49 did not have. **No harm here.**

**Finding C-2 (low, prospective).** The double-count risk lives in the *scoring* step, not the claim text: `SCORECARD` "Round 50 — measured outcomes" (written at `d45c5bb`) states the capability is "first working round 50" and does not repeat r48's 8-refusal measurement, so a reader cannot see that the discovery predates this round; and `126` is presented as the instrument's denominator without the 120/6 split. Exact checks:
1. The novelty cell must contain the provenance split (`120 carried / 6 new`) or a pointer to the `COUNTS` line, so the volume of the population cannot be read as this round's evidence.
2. The novelty cell must keep r48's `admitted=112 refused=8` as the *prior* measurement of over-refusal (it is currently only in the r48 row, which is the right place — the check is that a later edit to the r50 row must not claim the discovery).
3. The 15-row mutant battery must be scored on **caught/floor**, not on rows: 7 carried rows were dropped as unwitnessed (that is the correct Q38 move) and `MUTANTS total=15 caught=15` meets the floor exactly — a claim of "23-mutant battery" would be a second overstatement of exactly the same kind.

---

## Residual risk (in priority order)

0. **Instrument drift** (A0): the tip's working tree carries a counter (`850ec790…`) that is not the counter the S3 receipt scored (`d8787b34…`). Medium — claim-integrity, cheapest to close (re-run the receipt or record the open-window row).
1. **Guard mapping not recorded** (A1.2): the sealed50 set probably pins the six allowlist widenings, but nothing states module→guard, and my base-fence ablation shows six of them are invisible without a dedicated module. Medium. Exact check given in A2-1.
2. **`FETCH_HEAD`/`shallow`/`objects/info/packs` admitted with unvalidated content** (A1.4 `p4`): no production reader today; becomes a real outside-`d` path the day a tool parses fetch metadata. Medium-low.
3. **Host-git-template pins** (B2): the claim is re-runnable only on a host matching this git installation. Medium; disclosed in `Named limits`, not contained. Exact checks given.
4. **States git does not write now admitted** (`p7`, `p8`): scope widening of "states git itself writes"; low-medium, no outside-`d` reach measured. Exact checks given.
5. **Narrative scope understatement** (A1-1: "five classes" vs 12): low, review-quality only.

## Verification gaps (what I could not observe)

- I could not run the counter on a host with a **different git version**, so B2's portability failure is proven by the byte-identity of the pinned template files and by the kill rule's `mismatched>0` clause, not by a second-host run.
- The landed fence's docstring mentions a **mount/device-boundary leg** added by its author; I did not test it (it needs a bind mount; a reviewer seat does not mutate the host mount table). Whether that leg is load-bearing for any frozen module is unverified.
- The 15 mutant rows' kill *directions* were not re-witnessed by me (that is the mutation seat's item); I only re-ran the counter and confirmed `caught=15 broken=0`.
- The r50 `SEALED50_MIN=6` literal is weaker than the shipped 18; a later deletion of 12 sealed modules would still pass the literal. Not a harm today, but the check should be `SEALED50_TOTAL >= 18` once 18 is the frozen set.

VERDICT: **admit with fixes — no refusal is weakened (0 of 71 hostile fixtures flip; no outside-`d` syscall at decision time; no git child), and no double count in the claim text.** The axis-(b) harm is real but disclosed (126/126 pinned trees embed host-git template bytes; the claim is re-runnable only on git 2.56.0 with unmodified templates); the axis-(a) harm is conditional on implementation and today amounts to three newly admitted shapes, one of them path-bearing (`FETCH_HEAD`). Ship-blocking: none. Must-record before the novelty step is scored: the guard→module mapping (A2-1), the 120-carried/6-new split and r48's prior measurement in the novelty cell (C-2 checks 1–2), and the template-digest line in `builder-receipt.txt` (B2 check 1, interim form).

Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C1RevNoHarm` removed before yield — **no defect of my own to report**; candidate `repair_emul.py`, `probes.py`, base-fence extraction and all ablation logs were copied into this report's evidence above before removal.
