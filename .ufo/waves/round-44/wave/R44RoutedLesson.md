# R44RoutedLesson — routed rows R42-R3-11..17 re-checked against the current `corpus/lessons/round-42.md`

Scribe seat, kengaku round 44 (hyaku run 9), 2026-10-26. Leaf: no subagents, no background jobs.
Read-only against the lane; every write is under `.ufo/waves/round-44/wave/R44RoutedLesson/` or `$S`.

## 0. What was measured, and against what

- Target file: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-42.md`,
  216 lines, `sha256=77ab977bc0a22bae159f4b83fb8d4c6cc134656747848cde58cb502e0124e2cc`, lane HEAD
  `5e3d3aa06c6b7000929ac3e62563a39159c4501f` (2026-10-26 20:27:30 -0300). Last commit touching the file:
  `77ea425` (round-43 landing).
- Comparison body: `git show d33350f:corpus/lessons/round-42.md` — the pre-errata 151-line body the round-43
  review re-checked against. `d33350f` = "round-43: wave-1 spec and dispatch (38 seats)", 18:59:51 -0300.
- Ledger: `corpus/routed-findings.jsonl` (60 rows; `open=38 blocked=1 closed=21 refused=0`).
- Tool: `python3 plans/routed_open.py --lane <clone> --list|--observe`, run on a `--shared` clone at
  `$S/lane` (toplevel verified `= $S/lane`), inside the Q32 envelope.

Envelope (Q32), `routed_open.py --list` / `--observe`:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/R44RoutedLesson/env … -- python3 plans/routed_open.py --lane …/lane --observe
ENVELOPE start 20:36:56 cwd=/fast/scratch/hyaku/kengaku-r44/R44RoutedLesson/lane
ENVELOPE end 20:36:58 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

```
OBSERVE R42-R3-11 rc=1 observed=fail self=open
OBSERVE R42-R3-12 rc=1 observed=fail self=open
OBSERVE R42-R3-13 rc=1 observed=fail self=open
OBSERVE R42-R3-14 rc=1 observed=fail self=open
OBSERVE R42-R3-15 rc=1 observed=fail self=open
OBSERVE R42-R3-16 rc=1 observed=fail self=open
OBSERVE R42-R3-17 self=open observed=n/a
OBSERVE rows=60 mismatched=0
```

(`--list` on the same clone: `ROWS total=60 open=38 blocked=1 closed=21 refused=0`,
`routed_open=39 oldest_round=39`, exit 0, digest unchanged. Both envelope runs recorded `exit=0` with
`local_bin_content_before=after=328be01808ba022f`.)

**Headline: all seven rows are still `open`, and every one of their checks is red — but for six of them the
red is stale bookkeeping, not an unfixed lesson defect.** Five defects were corrected by the round-43 errata
block (`E2`–`E6`); two were measured false by that block's own re-check paragraph; none is still-true and
uncorrected. What is left red is (a) six check strings that look for a token the correction never uses, and
(b) one new defect *in the correction layer itself* (§3): every errata line reference is 7 lines early.

## 1. Row-by-row disposition

| row | class | source | current state of the lesson | disposition |
|---|---|---|---|---|
| R42-R3-11 | lesson-unsupported-carry-claim | F42RevLesson.md:109 (D2) | body `:114` still says the F39 trio is "named carried again in the freeze"; `E2` (`:169-175`) retracts it | **fixed by errata (E2)** |
| R42-R3-12 | lesson-unpersisted-number | :118 (D3) | body `:158` still quotes `flash=14/33`; `E3` (`:176-181`) demotes both ratios to quoted stdout | **fixed by errata (E3)** |
| R42-R3-13 | lesson-wrong-pointer | :128 (D4) | body `:64` still cites `fibsqrt-probe.txt:6`; `E4` (`:182-185`) + closure-R1 block (`:206-210`) correct to `:11` | **fixed by errata (E4 + R1)** |
| R42-R3-14 | lesson-line-ref-off-by-one | :134 (D5) | `plans/round42_c2_verify.py:327` **is** the V9 entry; `:328` is `defects = 0` | **not a defect** (reviewer moved it) |
| R42-R3-15 | lesson-unreproducible-command | :137 (D6) | body `:129` still prints the BRE command; `E5` (`:186-188`) gives the `-E` form | **fixed by errata (E5)** |
| R42-R3-16 | lesson-line-ref-off-by-one | :142 (D7) | capture `Dockerfile` has `COPY tests/sim.c` at `:9`, `COPY gates.txt` at `:10`, comment at `:8` | **not a defect** (reviewer moved both) |
| R42-R3-17 | lesson-fix-without-receipt | :146 (D8) | body `:157` still has no failing receipt; `E6` (`:189-191`) states it | **fixed by errata (E6)** |

Net: **5 of 7 were real and are corrected; 2 of 7 were never defects.** Nothing is still-true-and-uncorrected.

## 2. Evidence per row

### R42-R3-11 — unsupported carry claim (D2)

The row's note is exact and still holds. `plans/round-42-claims.md` has no `§Limits` section:

```
$ grep -n '^#' plans/round-42-claims.md
1:# Round 42 — frozen claims (kengaku, hyaku run 9, 2026-10-26)
23:## C1 — calibration: …
65:## C2 — coverage: …
96:## Separability
102:## Frontier step (not a claim)

$ grep -nE 'LedgerTip|MutDirection|OrderGateMut|fail-open|s_usage' plans/round-42-claims.md ; echo rc=$?
rc=1
```

The only "Limits named now" bullet is `:60` and it names XL1–XL6, `state_check.py`/`round_close.py` survivors and
the 34 unpriced `tip_receipts.py`/`sources_adopt.py` rows — not the F39 trio, not `s_usage-03`. `E2` states
exactly that. **The lesson defect is closed by E2.**

Caveat the L1 should keep: the row's green condition is "a later freeze or lesson names them", and no later
freeze does. `grep -nE 'F39LedgerTip|s_usage-03|F39MutDirection|F39OrderGateMut' plans/round-43-claims.md
plans/round-44-claims.md` → no match (rc=1); `corpus/lessons/round-43.md` → no match. So if the ledger wants the
*owner* tracked rather than the *claim retracted*, that is a second row, not this one.

### R42-R3-12 — unpersisted route-mix numbers (D3)

Re-measured, the substance is exactly as `E3` says:

```
$ python3 -c 'import json;s=json.load(open(".ufo/waves/round-42/falsify-spec.json"));print(len(s["items"]), sorted({k for i in s["items"] for k in i}))'
33 ['axes', 'milestone', 'name', 'prompt', 'role']
$ python3 -c 'import json;d=json.load(open(".ufo/waves/round-42/falsify-dispatch.json"));print(d["counts"])'
{'spawn': 33, 'resume': 0, 'total': 33}
$ grep -c 'flash=14/33' .ufo/waves/round-42/falsify-spec.json .ufo/waves/round-42/falsify-dispatch.json
.ufo/waves/round-42/falsify-spec.json:0
.ufo/waves/round-42/falsify-dispatch.json:0
```

Role mix in the spec: `reviewer 10, critic 9, executor 5, mutation-tester 3, scout 3, connector 3` — `E3`'s
"the row's role list also names two roles wave 2 did not have" is right and sharper than the review's "names
scribe": the row lists `executor/scribe/critic/sentinel`, and both *scribe* and *sentinel* are absent from the
spec. **Closed by E3.**

### R42-R3-13 — wrong receipt pointer (D4)

`E4` is accurate *against `d33350f`*, including its correction of the review:

```
$ git show d33350f:corpus/lessons/round-42.md | grep -n 'fibsqrt-probe.txt:6'
57:and 20000 and still passes 3/3 (receipt `fibsqrt-probe.txt:6`; `cases=16 …`)
```

One citation, not the review's two. The receipt itself:

```
corpus/evidence/round42/fibsqrt-probe.txt
  :6   # capture test_outputs.py sha256=6117b8ed…
  :11  CASE lookup-28 predicted=pass observed=pass tests=PPP … violates=example-208,example-20000
  :23  regrade cases=16 differ=0
  :24  cases=16 observed_pass=7 observed_fail=9 mismatches=0
```

So `:6` is a capture header and the content lives at `:23-24` (`:11` for the `lookup-28` case) — the row is
right and the correction is right. **Closed by E4 + closure R1**, with the line-ref caveat in §3.

### R42-R3-14 — `round42_c2_verify.py:327` (D5) — NOT a defect

The counter is unchanged since the round-42 freeze (`git log -- plans/round42_c2_verify.py` → one commit,
`bc856d8`), so today's bytes are the cited bytes:

```
$ sed -n '327,328p' plans/round42_c2_verify.py
                  ("V7", lambda: v7(lane)), ("V8", lambda: v8(lane)), ("V9", lambda: v9(lane))]
        defects = 0
```

`:327` is the checks-list entry that contains V9 and `:328` is `defects = 0`. The lesson's `:327` at `:97` is
**exact**; the review's D5 moved it one line early. The lesson already records this at `:198`. No correction is
owed. Ledger row should close as `refused` (its class is "line-ref-off-by-one" but there is no off-by-one).

### R42-R3-15 — census command without `-E` (D6) — real, corrected

Reproduced at both commits, on the `SOURCES.md` blob from each:

```
$ for c in bc856d8 508434a; do git show $c:corpus/SOURCES.md > /tmp/s.txt
    printf '%s wc=%s BRE=%s ERE=%s\n' $c "$(wc -l < /tmp/s.txt)" \
      "$(grep -c  '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /tmp/s.txt)" \
      "$(grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /tmp/s.txt)"; done
bc856d8 wc=171 BRE=171 ERE=117
508434a wc=175 BRE=175 ERE=121
```

Exactly `E5`'s numbers: as printed the command is `wc -l`, with `-E` it is the quoted 117/121. (HEAD today is
`wc=184 ERE=130` — the registry has grown since, which is why the check must key on the *correction*, not on the
count.) **Closed by E5**, with the line-ref caveat in §3.

### R42-R3-16 — `Dockerfile:9-10` (D7) — NOT a defect

```
$ sed -n '6,10p' corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile
6  RUN apt-get install -y gcc
7
8  # Copying tests/sim.c is allowed for the agent to check its work
9  COPY tests/sim.c /app
10 COPY gates.txt /app
```

The two COPY lines are `:9` and `:10`, the comment is `:8` — so the lesson's `Dockerfile:9-10` is right and the
review's D7 moved both pins one line late. Recorded by the lesson at `:200-202`. Close as `refused`.

### R42-R3-17 — fix without a failing receipt (D8) — real, corrected

`E6`'s two facts verify:

```
$ grep -n 'fc58bf3f' .ufo/waves/round-42/claims/frozen-digests.txt
4:fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3  plans/fibsqrt_probe.py
$ sha256sum plans/fibsqrt_probe.py
fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3  plans/fibsqrt_probe.py
```

The pin proves the frozen probe is the corrected file; it does not demonstrate the failure. No artifact under
`.ufo/waves/round-42/` stores the editor's syntax warning. **Closed by E6**; the row's `check` is `null` by
design (`routed_open.py --observe` prints `observed=n/a`), so a check must be added if the row is to be closed
by observation rather than by hand.

## 3. New defect found in the correction layer (needs an appended correction)

**E8 (minor) — every errata line reference is 7 lines early.** The errata block opens with "Line numbers are
this file's", but its references resolve only against `d33350f`. The round-43 addendum (`:62`) and the errata
block landed in the same commit (`77ea425`), so the refs point 7 lines above their targets at HEAD. Measured:

```
d33350f:57  -> HEAD:64  | and 20000 and still passes 3/3 (receipt `fibsqrt-probe.txt:6`; …
d33350f:98  -> HEAD:105 | round.* `git diff bc856d8..HEAD -- corpus/SOURCES.md` → empty (measured); …
d33350f:106 -> HEAD:113 | - *14 `round_close.py`/`tip_receipts.py` residual mutants* and *`F39LedgerTip` D1, …
d33350f:122 -> HEAD:129 | (`grep -c '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`) …
d33350f:150 -> HEAD:157 | | **A seat-tooling slip by the L1** — two `edit` calls on the freshly written probe …
d33350f:151 -> HEAD:158 | | **A wave dispatched under the m_flash floor** — wave 2 carries 14/33 …
```

The mapping is uniform `+7` for all six refs, and the same applies to the closure-R1 block, which names `:57`
twice (`:206`, `:207`) for a citation now at `:64`. Four of the seven rows in this seat's scope are affected
(R42-R3-11 via E2 `:106-108`, -12 via E3 `:151`, -13 via E4 `:57`, -15 via E5 `:122`, -17 via E6 `:150`).

Draft appended correction (paste at the end of `corpus/lessons/round-42.md`; nothing above edited, per R1):

```markdown
### Errata (round 44 — errata line references re-pointed; nothing above is edited)

- **E8 — every `E1`–`E6` and closure-R1 line reference is 7 lines early.** The errata block says "Line numbers
  are this file's", but its references resolve against `d33350f` (151 lines): the round-43 addendum and the
  errata block landed in the same commit (`77ea425`), which inserted 7 lines above them. At HEAD (216 lines,
  `sha256 77ab977b…`) the targets are: R4's measurement `:98` → **`:105`**; R5's freeze sentence `:106-108` →
  **`:113-115`** (sentence at `:114`); the route-mix row `:151` → **`:158`**; the `fibsqrt-probe.txt:6`
  citation `:57` → **`:64`** (both places, including the closure-R1 block); the census command `:122` →
  **`:129`**; row 3's fix `:150` → **`:157`**. The content of E1–E6 is unaffected — verified at HEAD: the freeze
  still has no `§Limits` (`grep -nE 'LedgerTip|MutDirection|OrderGateMut|fail-open|s_usage'
  plans/round-42-claims.md` → rc=1), the spec/dispatch still carry no route field, the receipt still reads
  `:6`/`:11`/`:23`/`:24`, the BRE/ERE counts are still 171/175 and 117/121, and the frozen probe still hashes
  `fc58bf3f…`.
```

## 4. Proposed `check` commands for the seven ledger rows

Each was run twice — against HEAD (must pass) and against the pre-errata `d33350f` body (must fail), so none is
green by accident and each is green only because a correction exists. Envelope receipt:
`.ufo/waves/round-44/wave/R44RoutedLesson/checks.txt`.

```
ENVELOPE /usr/bin/bwrap … -- bash /fast/scratch/hyaku/kengaku-r44/R44RoutedLesson/run_checks.sh
ENVELOPE start 20:38:31 cwd=/home/vgpnk/Projects/shokunin
R42-R3-11 HEAD=pass d33350f=fail(expected)
R42-R3-12 HEAD=pass d33350f=fail(expected)
R42-R3-13 HEAD=pass d33350f=fail(expected)
R42-R3-14 HEAD=pass d33350f=fail(expected)
R42-R3-15 HEAD=pass d33350f=fail(expected)
R42-R3-16 HEAD=pass d33350f=fail(expected)
R42-R3-17 HEAD=pass d33350f=fail(expected)
ENVELOPE end 20:38:33 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

| row | proposed status | proposed `check` |
|---|---|---|
| R42-R3-11 | `closed` (claim retracted) | `grep -qF 'are **not** "named carried again in the freeze"' corpus/lessons/round-42.md` |
| R42-R3-12 | `closed` | `grep -qF 'quoted stdout, not persisted data' corpus/lessons/round-42.md` |
| R42-R3-13 | `closed` | `grep -qF 'pointer corrected' corpus/lessons/round-42.md` |
| R42-R3-14 | `refused` (not a defect) | `grep -qF 'Re-checked and **not** defects' corpus/lessons/round-42.md` |
| R42-R3-15 | `closed` | `grep -qF 'The quoted numbers come from the' corpus/lessons/round-42.md` |
| R42-R3-16 | `refused` (not a defect) | `grep -qF 'moved both pins' corpus/lessons/round-42.md` |
| R42-R3-17 | `closed` | `grep -qF 'falsifier exists only in its own sentence' corpus/lessons/round-42.md` |

`routed_open.py --observe` wants `pass` for `closed` and `refused` alike (`want = "pass" if status in
("closed","refused")`), so these strings satisfy the tool as written. Two notes for the L1:

- These checks assert *the correction exists*, not *the underlying fact is re-verified*. That is the right
  predicate for a lesson-defect row (R1 forbids in-place edits, so the body sentence can never be the thing that
  turns green), but it must not be read as a fresh measurement of the freeze/receipt — §2 carries those.
- If the ledger prefers the row's original green condition for R42-R3-11 ("a later freeze or lesson names the F39
  trio"), keep it `open` with the existing check; I verified it is still red for a real reason (no later freeze
  names them). That would make the tally 4 corrected / 1 open / 2 refused.

## 5. Adjacent finding, outside the seven rows (for the L1, not counted)

`R42-R3-10` (D1, `lesson-false-measurement`) is `closed` on `grep -qE 'only additions|four added lines'`. It is
green, but `E1`'s quoted command no longer produces its quoted output:

```
$ git diff --numstat bc856d8..HEAD -- corpus/SOURCES.md
13	0	corpus/SOURCES.md
$ git diff --numstat bc856d8..508434a -- corpus/SOURCES.md
4	0	corpus/SOURCES.md
```

`E1` says "`git diff --numstat bc856d8..HEAD -- corpus/SOURCES.md` → `4 0`". That is true at `508434a` (where
S125–S128 were the only additions) and false at `77ea425`/HEAD, where round 43 added nine more rows. The class
is the lesson's own recurring one — a quoted command whose output it does not produce — so if E8 is appended, a
one-line `E9` fixing the commit (`bc856d8..508434a`, or "13 additions at HEAD") is cheap. Not routed, not in
this seat's scope, flagged only.

## 6. Touched surfaces

- Written: `.ufo/waves/round-44/wave/R44RoutedLesson.md` (this report),
  `.ufo/waves/round-44/wave/R44RoutedLesson/checks.txt` (receipt, 1.5 KB, quoted in full above).
- Read only: `corpus/lessons/round-42.md`, `corpus/lessons/round-43.md`, `corpus/routed-findings.jsonl`,
  `plans/round-42-claims.md`, `plans/round-43-claims.md`, `plans/round-44-claims.md`,
  `plans/round42_c2_verify.py`, `plans/fibsqrt_probe.py`, `plans/routed_open.py`,
  `.ufo/waves/round-42/falsify-spec.json`, `.ufo/waves/round-42/falsify-dispatch.json`,
  `.ufo/waves/round-42/claims/frozen-digests.txt`, `.ufo/waves/round-42/falsify/F42RevLesson.md`,
  `corpus/evidence/round42/fibsqrt-probe.txt`, `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile`,
  git objects at `bc856d8`/`508434a`/`d33350f`/`77ea425`/`5e3d3aa`.
- Nothing in the lane was edited; no `git add/commit/stash/checkout/reset/push/pull`, no jj mutation. The clone
  at `$S/lane` was `--shared` and never committed to.
- Scratch `$S=/fast/scratch/hyaku/kengaku-r44/R44RoutedLesson` removed with `scratch_guard.py safe-rm` after
  the receipt was copied out.

## 7. Limits of this re-check

- I did not re-run the round-42 C1 battery, the C2 counter or the fibsqrt probe; the landing measurements are
  the L1's and the lesson scopes them to wave-1 receipts. Every number above is either a byte-level read of a
  stored artifact or a fresh `grep`/`git show` over one.
- `E2`'s claim about `plans/round-42-claims.md` was verified by header list and one `grep -nE`; I did not read
  the whole freeze.
- I did not verify `E7` (the two C1 `adv` cites) — outside R42-R3-11..17.
- The two `refused` recommendations rest on the current capture bytes (`Dockerfile` `:8-10`) and the current
  counter (`:327-328`); both artifacts are pinned/unchanged (`plans/round42_c2_verify.py` has a single commit,
  `bc856d8`), so they cannot drift under the verdict.
- The `+7` mapping is measured at HEAD `5e3d3aa`; a later edit above the errata block will move it again. That
  is exactly why the draft E8 quotes the target *text* beside each new line number.

VERDICT: lesson-defects-fixed-5-of-7
