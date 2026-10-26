# F39CritOverclaim — overclaim hunt (round 39, wave 2 FALSIFY)

Seat: critic. Targets attacked as landed at lane tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c` (branch `master`):
`corpus/knowledge/tb2-git-leak-recovery-grader.md`, the round-39 lines of `corpus/README.md`, the round-39 paragraph of
`PROVINCE.md`, and `SKILL.md` §"Repository-history TB2 grader — round 39" (`:867-931`). The live lane HEAD is `acf4375`
(the wave-2 dispatch commit); the four target files hash identically in the live tree and in the clean clone at
`a6832f5` (`receipts/tip-identity.txt`), so line numbers below are valid for both.

Method: clean clone under `/fast/scratch/hyaku/kengaku-r39/F39CritOverclaim/`, `git rev-parse --show-toplevel` verified,
`sha256sum -c SHA256SUMS` 7/7 OK; the frozen probe re-run byte-equal; all 29 located quotes re-checked byte-exact; tag
counts and V7 labels re-derived from the receipt; every class/universal/"first" sentence tested against the captures and
against scratch fixtures under host `git version 2.56.0`. No lane file edited; no subagents; nothing installed. Receipts
are in `F39CritOverclaim/receipts/`; the `receipts/…` paths below are relative to the seat directory
`.ufo/waves/round-39/falsify/F39CritOverclaim/`.

## Findings (6)

### 1. "tag messages … are outside all four views" — a dangling tag's message is inside the fourth view

Claim (`corpus/knowledge/tb2-git-leak-recovery-grader.md:82-83`): "tag messages, stash merge commits and `.git/config`
are outside all four views." (13 words)

Counterexample (executed, `receipts/dangling-tag.txt`; object ids are per-fixture, wall-clock dependent — the entry's
own disclosure): create an annotated tag whose message is the literal, then delete the tag so the tag object is
unreferenced:

```
$ git tag -a keep -m 'secret[lost_and_found_in_git]' HEAD && git tag -d keep
Deleted tag 'keep' (was ae6bf3c)
$ git fsck --lost-found
dangling tag ae6bf3cb611523ee069eb35258119996996cbb47
$ T=$(git fsck --lost-found | awk "/dangling tag/{print \$3}") && git cat-file -p "$T"
object 5e4b87a08bca97401b8318e39f737f9028471aaf
type commit
tag keep
tagger T <t@e> 1793001149 -0300

secret[lost_and_found_in_git]
```

Test 4 loops every line containing `dangling` (`test_outputs.py:76-77`), takes `parts[-1]` as the hash (`:80`), calls
`cat-file -p` (`:84`) and asserts `secret[` absent (`:90`) — so this state **fails test 4**. The frozen
`tag-message-secret` case passes only because its tag stays referenced (probe `plans/git_leak_probe.py`: `git tag -a keep
-m ... HEAD`), not because "tag messages" are outside the views. The entry's own uncovered list already excludes "a tag
object dereferenced by `--all`" from the claim (`:283-284`); a dangling tag is a different, uncovered shape.

Axes: depth (grader semantics), coverage (edge class), calibration (the "four views" list is a class claim).

Smallest safe correction: "…; the message of a **referenced** annotated tag, stash merge commits and `.git/config` are
outside all four views. A **dangling** tag object's message *is* read by `fsck --lost-found` + `cat-file -p` and fails
test 4 (not among the 25 cases)."

### 2. SKILL's "only a dangling blob … or a dangling commit … is caught" — a dangling tree is read too

Claim (`SKILL.md:896`): "only a dangling blob (`dangling-secret-blob`, PPPFP) or a dangling commit whose message carries
the secret (`dangling-secret-commit`, PPPFP) is caught" (19 words as quoted).

Counterexample (executed, `receipts/dangling-tree.txt`): write a blob holding the literal and a tree whose entry name
carries it, without committing:

```
$ B=$(printf 'secret[lost_and_found_in_git]\n' | git hash-object -w --stdin) && printf '100644 blob %s\tsecret[lost_and_found_in_git].txt\n' "$B" | git mktree
d0b3d1a2bbfdf4f46dddd1e8dfe00196c5a3b5b1
$ git fsck --lost-found
dangling tree d0b3d1a2bbfdf4f46dddd1e8dfe00196c5a3b5b1
$ git cat-file -p d0b3d1a2bbfdf4f46dddd1e8dfe00196c5a3b5b1
100644 blob 52d18a091cd9755bacb8eaccab2882a24b080dc7	secret[lost_and_found_in_git].txt
```

The tree's `cat-file -p` text contains `secret[`, so `test_outputs.py:90` fires: test 4 fails. The tree is one of the
three object kinds the test's own docstring names (`test_outputs.py:67`), and a dangling tag (finding 1) is a third caught
shape. The entry is careful about this limit ("a secret in a tree object … are not covered and are not claimed",
`:283-284`); the SKILL row is not. If the sentence is meant to be scoped to the 25 cases it must say so.

Axes: depth, operability (decision table), coverage.

Smallest safe correction: "of the 25 frozen cases, only a dangling blob or a dangling commit whose message carries the
secret is caught; the loop asserts over **every** `dangling` object's `cat-file -p` text, so a dangling tree whose entry
name carries `secret[`, or a dangling tag object carrying it in its message, also fails test 4 (neither is in the 25)."

### 3. "any non-dot work-tree change … fails test 5" — a mode-only change passes

Claim (`corpus/knowledge/tb2-git-leak-recovery-grader.md:86-88`): "*any* non-dot work-tree change — an edited file, an
added file, a removed file, a renamed file — fails test 5" (19 words).

Counterexample (executed in a probe-style sandbox, `receipts/checksum-mode.txt`): build the task's own initial state from
the captured `challenge-setup.sh`, compute the grader's exact checksum, then `chmod 755` the tracked, non-dot
`README.md`:

```
D1=2c3d6389133b6f9fffae5d3428ec1250c3b1cab5573c716d580dc1d4fa2f4adb  -
D2=2c3d6389133b6f9fffae5d3428ec1250c3b1cab5573c716d580dc1d4fa2f4adb  -
MODE_BLIND
755 /app/repo/README.md
 M README.md          <- git itself reports the change (old mode 100644 / new mode 100755)
```

D1 is the pinned literal of `test_outputs.py:110`, so the pre-change state satisfies test 5; D2 equals D1, so the
post-change state satisfies it too. `sha256sum` hashes contents and paths only; `git status`/`git diff` see the mode
change (`core.filemode=true`). A work-tree change git reports as a repository change is therefore invisible to the
"strict side".

Axes: depth, coverage (an "irrelevant files untouched" violation that passes), calibration.

Smallest safe correction: "any change to the **paths or contents** of the non-dot work tree fails test 5; file modes and
timestamps are not hashed, so a `chmod` on a tracked non-dot file passes."

### 4. "The two cases that show the checksum firing" — the receipt shows three

Claim (`corpus/knowledge/tb2-git-leak-recovery-grader.md:234-236`): "The two cases that show the checksum firing are
`untracked-file-secret` … and `readme-edited`" (13 words as quoted).

Counterexample (receipt, `receipts/labels.txt`): the frozen receipt's own letters make `flag-in-repo-only` the third
digest-moving case:

```
$ python3 labels.py <lane>        # parses corpus/evidence/round39/git-leak-probe.txt
test5-failing cases [('empty-app', 'FFFFF'), ('untracked-file-secret', 'PPPPF'), ('readme-edited', 'PPPPF'), ('flag-in-repo-only', 'FPPPF')]
```

Four cases carry a `F` in test 5. `empty-app` fails because `find /app/repo` errors on the missing directory
(`test_outputs.py:107`), not because a work-tree change moved the digest; of the three that do move the pinned digest,
`flag-in-repo-only` is the third, and the entry names only two. The same entry says so two findings later: "the new
non-dot file changes the pinned work-tree digest" (`:237-238`). The statement is false as an enumeration over the receipt; it is true only of the two cases tagged
`files-untouched`.

Axes: calibration, depth.

Smallest safe correction: "The two `files-untouched` witnesses are `untracked-file-secret` and `readme-edited`; the
checksum also fires on `flag-in-repo-only` (`FPPPF`, finding 6)."

### 5. "first probed instance for TB2 `git-leak-recovery`" — the round-38 pilot probed it first

Claim (`corpus/knowledge/tb2-git-leak-recovery-grader.md:312-314`): "The claim this entry makes is **\"first probed
instance for TB2 `git-leak-recovery`\"**" (7 words as quoted).

Counterexample (lane's own record, `receipts/pilot-and-logcount.txt`): the round-38 wave-1 pilot **executed the same
grader** on eight states on this host with git 2.56.0 before this entry existed —
`.ufo/waves/round-38/build/R38PlanNext.md:70` "Measured controls (executed; … grader `test_*` called after import … git
2.56.0)", with `A = untouched FPPPP`, `C = echo-only PPPPP`, `B = oracle PPPPP`, `E/F/G/H` also `PPPPP`. The entry
itself copies eight predictions from that pilot (`:61-62`: "eight predictions copy the round-38 pilot's observations on
this host"). The unqualified "first probed instance" is therefore false for this lane; only the first *recorded, frozen
25-case* probe is round 39's.

Axes: novelty, calibration (provenance/priority).

Smallest safe correction: "first **recorded, frozen 25-case** probe for TB2 `git-leak-recovery`; eight of the 25
verdicts were first observed by the round-38 pilot (`R38PlanNext.md` §2.3, controls A–H)."

### 6. README: "'recover the literal' … [is] enforced" — only the literal is; recovery is never checked

Claim (`corpus/README.md:265`): "\"irrelevant files untouched\" (the checksum) and \"recover the literal\" are enforced"
(12 words).

Counterexample (receipt:8 + probe): `echo-only` writes the literal and passes test 1 while the reset-away secret commit
and blob stay in the object store — no recovery happened (`receipts/labels.txt`; probe `FLAG = printf … > /app/secret.txt`
with no history read). The entry itself draws the line: "The label is `enforced` for the literal's *presence and exact
text*, not for recovery" (`:151`), and the expected value is a grader literal (`test_outputs.py:16`). The same README
clause also inherits finding 3: "irrelevant files untouched" is enforced only for non-dot **contents/paths**.

Axes: coverage, calibration (summary layer is broader than the entry it summarises).

Smallest safe correction: "the literal's presence and exact text at `/app/secret.txt` is enforced; recovery/provenance is
not (a planted literal passes), and 'irrelevant files untouched' is enforced only over non-dot paths and contents."

## Checked and cleared (calibration ledger)

Each was attacked and survived; numbers carry their commands.

- **Probe re-run** on the clean clone at `a6832f5`: `python3 plans/git_leak_probe.py --lane . --work $S/work` → exit 0,
  `cases=25 observed_pass=13 observed_fail=12 mismatches=0`; `diff` against the committed receipt empty
  (`receipts/probe-rerun.txt`, `receipts/probe-diff.txt`) — supports "reproduced every prediction" as to the frozen
  `predicted=` column and "the second run's receipt was byte-equal".
- **Captures**: `sha256sum -c SHA256SUMS` → 7× `OK` (`receipts/labels.txt`).
- **Located quotes**: 29 rows parsed from the entry's table; every quote occurs verbatim on its cited line/range and is
  3–25 words → `quotes_checked 29 bad 0` (`receipts/quotes-check.txt`).
- **Tag counts and labels** re-derived: `secret-gone` 16, `recover-secret` 5, `messages-untouched` 3, `files-untouched` 2;
  22 tagged, 3 untagged (`oracle-solve-sh`, `clean-echo`, `flag-padded-crlf`); labels `enforced/partly/enforced/partly`
  (`receipts/labels.txt`) — matches the entry and `PREDICATE C2`'s V7.
- **Instrument**: host `git version 2.56.0` matches the entry's stated instrument.
- **Finding 9 mechanism** (`receipts/fsck-split.txt`): on a reset-away initial state `git fsck` and
  `git fsck --unreachable` print nothing; `git fsck --no-reflogs --unreachable` prints
  `unreachable commit e4265715…`, `unreachable tree aa7dfd0c…`, `unreachable blob 52d18a09…`; `git fsck --lost-found`
  prints only `dangling commit e4265715…` — the tree/blob/commit split the entry describes.
- **Stash mechanism** (SKILL `:895`, `receipts/stash-mechanism.txt`): `git log --all --grep 'secret\['` and
  `git log --all -p -S 'secret['` are both empty; `git log --all -m -p -S 'secret['` produces 769 bytes containing the
  literal — merge-diff suppression, as stated.
- **Prior art** (`:299-308`, `:315-316`): the quoted sources are backed by opened fetches in
  `.ufo/waves/round-39/build/R39ScoutPriorArt.md` §1.1/§3 (TASK_REVIEW_AUTOMATION:244; Evan-Kim cert row 33; laion
  README:107; sha256 `dc7b01c1…` across TB2/TB2.1/fork). I did not re-fetch; no overclaim found in the entry's use.
- **Ubuntu 24.04 / git 2.43.0** (`:266-272`): backed by `R39CritFsckReflog.md` §6 (container run, same letters). Not
  re-run here.
- **PROVINCE round-39 paragraph** (`:372-408`): attacked and cleared — "object store and refs", "reading the literal
  alone passes 5/5 while the secret commit stays in the reflog", "fails exactly test 4", "84 remaining TB2 task graders",
  and the "never pulled / read, not run" limits all match the receipts and captures. No overclaim in this paragraph.
- **Entry limits** ("What the probe does not show", `:262-284`): the uncovered list already excludes trees, dangling
  tags, packed-refs, alternates, replace refs, etc.; findings 1–2 correct text that contradicts that list.

## Precision defects (measured, not counted as overclaims)

- `:42-43` "read by two `git log` invocations" — the captures contain **three** `git log` invocations
  (`test_outputs.py:26`, `:41`, `:54`; `receipts/pilot-and-logcount.txt`), and `PROVINCE.md:378-379` itself lists three.
  An undercount of the reads, not an inflated claim; narrower: "three `git log` invocations (two searches, one
  `--oneline` for the substring test)".
- `:89` and `:195` "the init message to appear once" — the assertion is substring containment (`:61`) and the setup
  writes that message on two commits (`challenge-setup.sh:12`, `:22`), so the test passes with two occurrences; narrower:
  "appear **at least** once".
- `:257` "reported only under `--unreachable`" — true of fsck's classification, but on the initial state `git fsck
  --unreachable` alone prints nothing (reflogs are heads; `receipts/fsck-split.txt`); `--no-reflogs` is required to see
  the tree and blob. A command-level reader would be misled by the bare flag name.
- `:304` "the audit executed no case" — the opened source supports "LLM prose, not a reproduction"
  (`R39ScoutPriorArt.md` §3.D); the stronger negative is an inference, not a fetched fact.

## Hygiene

Scratch `/fast/scratch/hyaku/kengaku-r39/F39CritOverclaim` removed before yield (receipts copied into this directory
first). Writes: this directory only. No lane file, Git index/jj state, or fleet-root file touched; no `git add/commit/
stash/checkout/reset/push/pull`, no mutating jj. No tools installed or upgraded (host `git 2.56.0`, `python3`, `bwrap`
sufficed). No process left running.

VERDICT: overclaims-6
