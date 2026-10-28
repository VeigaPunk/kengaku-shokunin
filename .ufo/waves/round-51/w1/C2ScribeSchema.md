# C2ScribeSchema — round 51 (hyaku run 11), ledger-schema note

Seat: `C2ScribeSchema` (scribe), round 51 C2 (`adjacency 8 → 9`), lane `kengaku-shokunin`.
Item: draft the ledger-schema note — a short `corpus/README.md` paragraph plus a lesson section
describing the routed-finding row contract (`owner`, `disposition` values with one-line
semantics, `next` for routed rows, and the `fixed-verified` / `fixed-historical` split and why
it exists), citing the counter and the claims doc. Read-only against the lane; nothing landed.

## 1. Axes named

| axis | move | what this seat contributes |
|---|---|---|
| **adjacency** (primary, 8 → 9) | the round's claimed move | the note is the human-readable half of the C2 signal: a routed finding is only "reported, not absorbed" if the row *names* its owner and *states* what this lane did with it. `AXES.md:16` — "Cross-domain awareness — evidence belonging to another domain reported, not absorbed". Without the note the new fields are undocumented schema; a reader cannot tell `routed` from `fixed-verified` and the axis reads as data entry. |
| **freshness** (not claimed, not harmed) | unchanged | the note describes the contract **as the frozen counter enforces it**, including the one behaviour the counter gets wrong for checks (F1/F2). Nothing here changes `PROVINCE.md` or C1's instrument. |

## 2. Commands run and observed output

All work in `/fast/scratch/hyaku/kengaku-r51/C2ScribeSchema` (NVMe; `TMPDIR` exported there).
One live shared clone, verified as its own toplevel before any write:

```sh
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane -q
cd lane && git rev-parse --show-toplevel      # /fast/scratch/hyaku/kengaku-r51/C2ScribeSchema/lane
git checkout -q e07f131cf7037e58a21db6e1f3986cf401ad257c
git rev-parse HEAD                            # e07f131cf7037e58a21db6e1f3986cf401ad257c
git status --porcelain | wc -l                # 0
```

### 2.1 The frozen counter at the frozen commit (reproduced, not copied)

```sh
cd $TMPDIR/lane && python3 plans/round51_routing.py --lane . --run-checks; echo "EXIT=$?"
```

```
LEDGER corpus/routed-findings.jsonl rows=71
FIELDS complete=0 incomplete=71
OWNERS attributed=0 unattributed=71
DISPOSITIONS set=0 bad=71
SOURCES resolved=71 missing=0
CHECKS present=61 absent=10
VERIFIED ran=0 passed=0 failed=0
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
  DETAIL FIELDS R39-R1 missing owner,disposition
  … (71 FIELDS lines, 71 OWNER lines, 71 DISPOSITION lines, 10 CHECK lines)
  DETAIL CHECK R40-R5 has no check command
  DETAIL CHECK R42-R3-09 has no check command
  DETAIL CHECK R42-R3-33 has no check command
  DETAIL CHECK R42-R3-34 has no check command
  DETAIL CHECK R42-R3-35 has no check command
  DETAIL CHECK R42-R3-37 has no check command
  DETAIL CHECK R45-S5-7b has no check command
  DETAIL CHECK R45-S5-7c has no check command
  DETAIL CHECK R45-S5-7d has no check command
  DETAIL CHECK R45-S5-7e has no check command
PREDICATE R51-C2 fail
EXIT=1
```

This is byte-for-byte the receipt `.ufo/waves/round-51/claims/c2-before.txt` (which carries no
`REV` line of its own — see F6).

### 2.2 Where the counter runs a `fixed-verified` check (A/B, same row, same predicate)

Row `R39-R1` copied into a scratch ledger, `owner=kengaku`, `disposition=fixed-verified`, check
unchanged; then the same row with the check addressed through `$LANE`.

```sh
python3 plans/round51_routing.py --lane . --ledger "$PWD/scratch-ledger-a.jsonl" --run-checks
```
```
VERIFIED ran=1 passed=0 failed=1
  DETAIL CHECK_FAILED R39-R1 fixed-verified but check exits nonzero
PREDICATE R51-C2 fail
```
```sh
python3 plans/round51_routing.py --lane . --ledger "$PWD/scratch-ledger-b.jsonl" --run-checks
```
```
VERIFIED ran=1 passed=1 failed=0
PREDICATE R51-C2 pass
EXIT=0
```

Variant B differs only in the check text:
`grep -q '^| \`order-check\`' "$LANE/SKILL.md" && grep -q '^| \`round39-c1-audit\`' "$LANE/SKILL.md"`.

### 2.3 Every existing check, run both ways (61 non-empty checks, same 60 s timeout)

```sh
# for each of the 61 rows with a check: bash -lc <check> with cwd = counter scratch dir, then cwd = lane root
# env = {**os.environ, TMPDIR=<cwd>, LANE=<abs lane>}   (the counter's own env, :121-124)
checks=61
pass_in_counter_scratch_cwd=6 ['R39-R2','R39-R5','R42-R3-03','R42-R3-07','R42-R3-08','R42-R3-26']
pass_from_lane_root=43
fail_from_lane_root=18
['R39-R2','R39-R3','R39-R4','R42-R1','R42-R3','R42-R5','R42-R6','R42-R3-02','R42-R3-05',
 'R42-R3-06','R42-R3-07','R42-R3-08','R42-R3-18','R42-R3-19','R42-R3-26','R42-R3-27',
 'R42-R3-32','R42-R3-36']
```

Two of the six scratch-cwd passes are **negative greps that pass because the file is absent**:
`R42-R3-07` (`! grep -qF 'equal to the receipt row' SKILL.md`) and `R42-R3-08`
(`! grep -qF 'biopython==1.85' plans/pkg_gate.py`) exit 0 in the scratch cwd and 1 from the lane
root. `R42-R3-03` passes in both only because its first alternative succeeds.

Failure reasons from the lane root, first line each:
`R39-R4` / `R42-R5` `SETUP counter … is not a round-38-list counter`; `R42-R3-02` `grep -q ':238' SKILL.md` no match;
`R42-R3-05`/`R42-R3-06`/`R42-R3-32`/`R42-R3-36` no match; `R42-R3-18` missing `plans/carried_direction_diff.py`;
`R42-R3-27` `SELFTEST ok=` below 37; the rest nonzero from the same grep/test shape.

### 2.4 The owner vocabulary the counter actually uses

```sh
python3 - <<'EOF'   # in /home/vgpnk/Projects/shokunin
import re; conf=open('shokunin.conf').read()
pat=re.compile(r"\s{0,6}([a-z][a-z0-9-]{2,15}):\s*\{")
print(len([l for l in conf.split('\n') if pat.match(l)]))
EOF
```
```
conf_regex_matches=0
LANES ids=['protocol', 'aggregator']
kengaku_in_LANES=False
```
`plans/round51_routing.py:54` (`load_owners`) therefore contributes **nothing** from the conf and
the accepted owner set is the 17-name `FALLBACK_OWNERS` literal (`:44-47`):
`aggregator chousa kagi kaidoku kake kama kasegi kengaku kotoba kotodama kumitate mori protocol
souji tabi tameshi unowned:integrator`.

### 2.5 `--ledger` must live inside the lane

```sh
python3 plans/round51_routing.py --lane . --ledger scratch-ledger-a.jsonl --run-checks
# ValueError: 'scratch-ledger-a.jsonl' is not in the subpath of '…/lane'   (plans/round51_routing.py:77)
```

## 3. The row contract as the frozen counter enforces it

Read from `plans/round51_routing.py` at `e07f131` — each rule is a line I can point at, not an
inference.

| element | rule | counter |
|---|---|---|
| field set | all of `id, class, source, opened_round, status, owner, disposition, close, blocker, check, note` must be **present as keys** (a `null` value counts as present) | `:38-39`, `:90-93` |
| `status` | one of `open`, `closed`, `refused`, `blocked`; failures are reported under the `DISPOSITION` key | `:40`, `:105-106` |
| `owner` | non-empty and a member of the counter's lane vocabulary | `:95-99` |
| `disposition` | one of `fixed-verified`, `fixed-historical`, `routed`, `referral`, `accepted-risk`, `refused-out-of-scope` | `:41-42`, `:101-104` |
| `source` | the substring **before the first `:`** must exist as a path inside the lane (`corpus/lessons/x.md:132` → `corpus/lessons/x.md`) | `:107-109` |
| `check` | non-empty for **every** row, whatever the disposition; only `fixed-verified` rows are executed | `:111-112`, `:120` |
| `next` | required (non-empty) for `routed` and `referral`; not part of the field-set tuple | `:113-118`, `:38-39` |
| `fixed-verified` execution | `bash -lc <check>`, **cwd = a fresh scratch dir**, `timeout=60`, env `TMPDIR=<that dir>`, `LANE=<abs lane>`; exit 0 = pass, timeout = fail | `:120-131` |
| `fixed-historical` `close` | first whitespace token (trailing comma stripped): a 7–40 hex commit that `git -C <lane> cat-file -e` resolves, **or** a path that exists in the lane | `:132-145` |
| routed/referral owner | must not be `kengaku` ("absorbed, not routed") | `:114-115` |

### Why the split exists

`fixed-verified` is a claim about **this run**, not about the commit: the counter re-executes the
check every time it is called. `fixed-historical` is the weaker, honest claim for a finding whose
evidence cannot re-execute — a one-time census, a check that needs a network or a live model
(`plans/round-51-claims.md` §Limits: such a check counts as failed), or a fix whose target text
has since been legitimately rewritten. Without the split the lane would have to mark those rows
`fixed-verified` and watch `CHECK_FAILED` climb, or delete them — and the kill rule forbids
deleting rows (`rows=71` floor). The measured basis: **18 of the 61 non-empty checks fail at
`e07f131` even from the lane root** (§2.3). Those rows cannot be `fixed-verified` as they stand.

## 4. Draft — `corpus/README.md` paragraph

Insertion point: immediately after the "Supporting corpus files" table, i.e. after current
`corpus/README.md:161` (the `SOURCES.md` row) and before `### \`evidence/\`` at `:163`. Optional
companion: add a row to that table, `| \`routed-findings.jsonl\` | Cross-domain ledger: one row
per routed finding, with owner and disposition (see the paragraph below) |` — the table currently
documents `QUALITY.md` and `SOURCES.md` only, and the ledger is documented nowhere in this file
(F4).

> **Routed findings — `routed-findings.jsonl`.** One JSON object per line for every finding that
> crossed a domain boundary in either direction. A row carries `id`, `class`, `source` (a lane
> path, `:line` allowed, which must resolve), `opened_round`, `status`, `owner`, `disposition`,
> `close`, `blocker`, `check`, `note`, and `next` for rows that leave the lane. `owner` names the
> lane the finding belongs to — `kengaku` only when this lane keeps it — and `disposition` says
> what happened to it: `fixed-verified` (fixed here, and `check` exits 0 when the counter runs
> today), `fixed-historical` (fixed here at a revision that no longer re-executes; `close` names
> the commit or path instead), `routed` (another lane owns the fix), `referral` (handed on as a
> lead, never absorbed), `accepted-risk` (real, knowingly unfixed), `refused-out-of-scope`
> (outside `PROVINCE.md`). `next` states where a `routed` or `referral` row goes. The split
> between `fixed-verified` and `fixed-historical` is deliberate: only a check that can be
> re-executed may be called verified, so a finding whose evidence is historical carries a
> resolvable pointer rather than a command that would fail. Counter:
> `python3 plans/round51_routing.py --lane . --run-checks`. It runs each `fixed-verified` check
> with `bash -lc` from a scratch working directory with `LANE` set to the lane root, so checks
> address the lane through `$LANE` and never through a relative path. Row contract frozen in
> `plans/round-51-claims.md` §C2.

Length: 16 lines, one paragraph; every clause is a counter rule from §3 or a claims-doc clause.

## 5. Draft — lesson section for `corpus/lessons/round-51.md`

Sits after `## Mistakes`, before `## Gate` (the `## Gate` section keeps its own spot-check line —
see F5; this section does not discharge round-50 D7).

> ## The routed-finding row contract (C2, adjacency)
>
> Adjacency's signal in `AXES.md:16` is "cross-domain evidence is named with its owner and routed,
> not absorbed". Until round 51 a `routed-findings.jsonl` row recorded what was found and whether
> it closed, but not **who owns it** nor **what this lane did with it** — so an absorbed finding
> and a routed one read the same. The round added `owner`, `disposition` and `next`, and
> `plans/round51_routing.py` now enforces them (`plans/round-51-claims.md` §C2).
>
> | field | contract |
> |---|---|
> | `owner` | the lane the finding belongs to; `kengaku` means this lane keeps it, anything else means it left |
> | `disposition` | `fixed-verified` — fixed here and the `check` exits 0 in the counter's run; `fixed-historical` — fixed here, evidence is a commit or path in `close`, not a runnable command; `routed` — another lane owns the fix; `referral` — handed on as a lead, not absorbed; `accepted-risk` — real and knowingly unfixed; `refused-out-of-scope` — outside `PROVINCE.md` |
> | `next` | required on `routed` and `referral` rows; names where the finding goes |
> | `check` | non-empty on every row; executed only for `fixed-verified`, with `bash -lc` from a scratch cwd, `LANE` set, 60 s timeout |
> | `close` | for `fixed-historical`, its first token must be a commit that resolves in the lane or a path that exists |
>
> **Why `fixed-verified` and `fixed-historical` are separate.** `fixed-verified` is a claim about
> the current run: the counter re-executes the check every time. Some fixes cannot re-execute — a
> one-time census, a check that needs a network or a live model (a failed check by the claims'
> own §Limits), a target text legitimately rewritten since. The split gives those rows an honest
> claim and a resolvable pointer instead of a green that would not reproduce. It is not
> cosmetic: at the freeze commit `e07f131`, 18 of the 61 non-empty checks already failed from the
> lane root, so those rows cannot be `fixed-verified` as they stand, and the kill rule forbids
> deleting them.
>
> **Where the checks run.** The counter executes a `fixed-verified` check with
> `bash -lc` from a fresh scratch directory and exports `LANE=<lane>`
> (`plans/round51_routing.py:120-131`). A check written against lane-relative paths therefore
> fails there — and a *negative* grep written that way passes vacuously, because the file it
> names is absent. Both directions were observed on the freeze commit: `R39-R1`'s literal check
> failed under the counter and passed once addressed through `$LANE`, while `R42-R3-07` and
> `R42-R3-08` passed in the scratch cwd and failed from the lane root. Every `fixed-verified`
> check must therefore address the lane through `$LANE`, and a green from the scratch cwd alone
> is not verification.
>
> Numbers at landing (fill from the landing-tip run, not from this draft): `rows=<N>`,
> `unattributed=0`, `bad=0`, `CHECKS absent=0`, `CHECK_FAILED 0`, `NEXT violations=0`,
> `PREDICATE R51-C2 pass`.

## 6. Findings for the L1 (not landed by this seat)

1. **F1 — `fixed-verified` checks run from a scratch cwd, so lane-relative checks cannot pass.**
   `plans/round51_routing.py:121` passes `cwd=str(tmp)`, a fresh scratch dir, while 61 of the 61
   existing checks address the lane relatively. Measured at `e07f131`: 6 pass in that cwd, 43
   pass from the lane root, 18 fail from the lane root. Landing either (a) rewrites every
   `fixed-verified` check as `$LANE`-addressed (proven sufficient, §2.2 B) or (b) runs checks
   with `cwd=lane` — but (b) changes the frozen instrument and needs a claims amendment. The note
   drafts above state the rule as the counter actually behaves (a).
2. **F2 — vacuous green.** Two of the six scratch-cwd passes (`R42-R3-07`, `R42-R3-08`) are
   negative greps that succeed only because the file is missing. Granting `fixed-verified` on a
   scratch-cwd green can certify the opposite of the truth. If F1 is fixed by `cwd=lane`, this
   disappears; if not, those checks must be positive-form and `$LANE`-addressed.
3. **F3 — the claims doc and the instrument disagree on where `owner` comes from.** §C2 says "every
   `owner` names a fleet lane from `../shokunin.conf`"; `load_owners` (`:54`) matches
   `id: {` and the conf's lane block is `LANES="id|repo|axes"`, so it matches **0** lines and the
   accepted set is the 17-name `FALLBACK_OWNERS` literal (§2.4). The conf names only `protocol`
   and `aggregator`, and `kengaku` is not in it. Either teach `load_owners` to parse `LANES`, or
   amend the claims wording to "the counter's lane vocabulary". As written, the predicate is
   satisfiable by names no conf declares.
4. **F4 — the ledger is undocumented in `corpus/README.md`.** `grep -n "routed-findings"`
   returns nothing there; the "Supporting corpus files" table has two rows (`QUALITY.md`,
   `SOURCES.md`); `defects.jsonl` is described only inside the round-35 evidence bullet
   (`:570`). Draft §4 is the drop-in fix, and the optional table row closes the discovery gap.
5. **F5 — round-50 D7 is still open.** `LEARNING.md:70` requires a round lesson's `## Gate` to
   carry the spot-check result; my lesson draft is schema-only and deliberately does not write
   that line, because no spot-check has happened yet at this seat.
6. **F6 — the C2 before receipt carries no `REV`.** `.ufo/waves/round-51/claims/c2-before.txt`
   has no revision line; I reproduced it exactly at `e07f131` (§2.1), so the revision is
   established here, but the receipt should name it (round-50 D4 was the same class).
7. **F7 — `referral` and `routed` are indistinguishable to the counter.** Both require a
   non-`kengaku` owner and a `next`; nothing else separates them. The semantics in the drafts
   (`routed` = another lane owns the fix, `referral` = handed on as a lead) are a documentation
   decision, not an enforced one — the L1 should confirm or replace them before landing.
8. **F8 — `next` is not in the field-set tuple** (`:38-39`), so its absence is invisible on any
   row that is not `routed`/`referral`, and `--ledger` crashes (`ValueError`) when the path is
   outside the lane (`:77`). Both are minor; recorded so the L1 does not read the field table as
   "`next` is a completeness field".

## 7. Limits

- I measured at `e07f131` only. The landing tip will have a different ledger (71 rows with
  `owner`/`disposition`), so §2.3's 43/18 split describes the **pre-landing** checks; the drafts
  say so and leave landing-tip numbers as placeholders.
- §2.3 ran the ledger's own shell commands in my scratch clone with a 60 s timeout, mirroring the
  counter's env. Two of them (`R39-R2`, `R42-R3-26`) `mktemp`/`chmod` inside `$TMPDIR`; all ran
  in the scratch clone or my `TMPDIR`, none in the lane tree.
- `git_leak_probe.py`, `scratch_guard.py`, `mutant_direction_check.py`, `sources_appendonly.py`,
  `anchor_line_check.py` were executed as the ledger's checks require, read-only against the
  clone.
- The `prose` of the README paragraph is my reading of the counter, not a landing; the L1 may
  reword. Nothing in this report edits a production file.
- No tool was installed or upgraded this seat; no pacman transaction was attempted.
- Scratch: `/fast/scratch/hyaku/kengaku-r51/C2ScribeSchema` was removed after this report was
  written (free space seen: `/dev/nvme1n1p2 804G 250G used 555G avail 32%`).

## 8. Provenance

```
REV e07f131cf7037e58a21db6e1f3986cf401ad257c
COUNTER plans/round51_routing.py sha256 = 7bf2d00ccf35ce3ca9a62f1f72aaf2bb0ecb7ea7880b093a05bb927cae6e9b03
LEDGER  corpus/routed-findings.jsonl rows=71 at REV
```

Lane tip read for the README/lesson context: `4090c3db79d11279ab5e5121ba25e74aa316e6e7`
(read-only; no file in that tree was modified).

VERDICT: drafted — README paragraph and lesson section delivered against the frozen counter, with the contract's check-cwd behaviour measured in both directions; 8 findings routed to the L1 (F1 check cwd, F2 vacuous green, F3 owner source, F4 README gap, F5 D7 still open, F6 receipt REV, F7 routed/referral semantics, F8 next/ledger path); nothing landed, no production file touched.
