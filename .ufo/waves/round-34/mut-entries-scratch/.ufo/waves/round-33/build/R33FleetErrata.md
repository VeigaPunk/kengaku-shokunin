# R33FleetErrata — fleet-report errata drafts (routed defects N3, N4) + L0 decision-packet line

Seat: `R33FleetErrata` (scribe), round 33 / hyaku run 7, 2026-10-25. Access date for every source
opened: 2026-10-25.
Scope: DRAFT ONLY. Nothing under the lane tree was edited except this report; nothing under the fleet
repo was touched. The L1 applies these via fleet-commit.

Lane tip observed at start of work: `78955888542258ba369f5aa72c200c913b4c3c90` (the assignment named
`c227e486` as the post-freeze tip; `c227e486a622ff82aae780c6fc58f023dcc82430` is its prefix — the tip has
since advanced by one commit, `7895588`, "round-33: C2 routed-defect repairs …"). Read-only fact, not a
conflict: both pointers resolve, and `112091c2d9077e484b53512ca363d2fe6ba6fc5c` is the round-32 closure
the lane branched from (`f0b20ae` → `c227e48` → `7895588` sit on top of it).

## 1. As-found state — both appends already land in the fleet repo

This is the load-bearing observation of the seat, and it changes how the L1 should consume the drafts.

- Fleet repo HEAD is `22d28422f051195b336967dfc4da547281419912` ("round-33: kengaku l0 question —
  coverage-cap decision packet").
- Fleet commit `3d3ca566055112e9a3736218e77a7c79abb613f7` ("round-33: kengaku erratum appends for routed
  defects N3 (phantom hash a44b5a8 -> ae95fe0) and N4 (closure tip 112091c)", author
  `kengaku-shokunin <kengaku@shokunin.local>`, 2026-10-25 14:14:59 -0300) already appends to **both**
  reports: `git show --stat 3d3ca566` → `.ufo/reports/round-31/kengaku.md | 7 +++++++` and
  `.ufo/reports/round-32/kengaku.md | 7 +++++++`, 2 files changed, 14 insertions(+). It is an ancestor of
  HEAD (`git merge-base --is-ancestor 3d3ca566 HEAD` → success).
- Both files are clean in `git status --porcelain` at HEAD.
- The L0 line is already in the queue: fleet `.ufo/l0-questions.md:163` (403 characters), committed at
  `22d28422`; `git log --oneline -2 -- .ufo/l0-questions.md` shows `22d28422` then `02a92297`.

Consequence: **do not re-append the blocks below verbatim.** They are the canonical wording this item
asked for, they are what the frozen counters accept (verified in §3), and they differ from the applied
bytes only in the respects named in §2 F1–F3. If the L1 wants the round-31 block under the exact `##`
heading this item specified (the applied form is a bold inline header), the correct move is one short
distinct note, never a duplicate of an already-present block.

Applied bytes, quoted with line numbers (fleet paths relative to `/home/vgpnk/Projects/shokunin`):

`.ufo/reports/round-31/kengaku.md:241-246`
```
241|**Erratum addendum 3 (round 33, appended by the kengaku lane — the filed bytes above stand as written).**
242|The "Erratum addendum (trend-verdict seat)" above names lane tip ``a44b5a8`` as the locator-fix commit;
243|``git cat-file -t a44b5a8`` fails in both the fleet repo and the lane repo — the token is a phantom hash
244|(no such object). The real commit is ``ae95fe0`` — `round-31: entry locator corrections
245|(verifier_mode.py:18-21, :39-40) and final falsify evidence`, an ancestor of the round-31 lane tip.
246|This citation is superseded, not rewritten.
```

`.ufo/reports/round-32/kengaku.md:64-69`
```
64|## Addendum (round 33, appended by the kengaku lane — the filed bytes above stand as written)
65|
66|The lane tip cited above (`bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d0`) is the pre-closure tip. The
67|round-32 non-author closure commit `112091c2d9077e484b53512ca363d2fe6ba6fc5c` (verifier spot-check,
68|`corpus/lessons/round-32-verifier-spotcheck.md`) landed after this report was filed; this addendum
69|records that closure tip so the report names the final round-32 lane state.
```

The filed bytes these repair (unchanged, append-only):
- `.ufo/reports/round-31/kengaku.md:226` — `fixed at lane tip `a44b5a8`-class commits (`verifier_mode.py:22-23` → **`:18-21`** for the "Returns the`.
- `.ufo/reports/round-32/kengaku.md:54` — `Respawn-per-round lane. Lane tip `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d` is pushed; remote tip matched at the gate.` (that token is 39 characters; the full hash is `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d0`).

## 2. Findings

**F1 — `near()` is line-local, so the N3 window is a *same-line* window.** `plans/round33_defects.py:59-66`
builds `re.escape(a) + r".{0," + str(width) + r"}" + re.escape(b)` and passes `flags=re.I` only — no
`re.S`, so `.` never crosses a newline. A block whose `a44b5a8` and `superseded`/`erratum` fall on
different physical lines fails even at 20 characters of separation. I hit this for real: an intermediate
draft that wrapped `Erratum addendum (trend-verdict seat)` onto the line *above* the token returned
`N3: 'no appended erratum supersedes the a44b5a8 citation'` while the absolute byte distance was 123.
The applied block survives only because its line 242 carries the words `Erratum addendum` and the token
`a44b5a8` together. Draft 1 below is deliberately wrapped so one physical line holds both.

**F2 — frozen text says 400 characters, the instrument uses 300.** `plans/round33-claims.md` N3 reads
"within 400 characters of `superseded` or `erratum`"; `check_n3` calls `near(...)` with no `width`, so the
default `width: int = 300` (`plans/round33_defects.py:59`) binds. The instrument is the stricter of the
two, so a block green at 300 is green at 400 — no false green, but the claim text overstates the tolerance.
Recorded, not repaired (the seat may not edit the frozen instrument or the product code).

**F3 — two cosmetic/fidelity gaps in the already-applied bytes** (counter-neutral; both files still return
`defects=0`):
1. `.ufo/reports/round-31/kengaku.md:242-244` contains three double-backtick sequences (`` ``a44b5a8`` ``,
   `` ``git cat-file -t a44b5a8`` ``, `` ``ae95fe0`` ``). In Markdown a doubled delimiter renders as a code
   span containing literal backticks, not the intended single-backtick code span.
2. `.ufo/reports/round-32/kengaku.md:66` presents `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d0` (40 chars) as
   "the lane tip cited above", while the bytes cited above (`:54`) carry the 39-character truncation
   `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d`. Both resolve to the same commit
   (`git rev-parse --verify 'bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d^{commit}'` →
   `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d0`), so the sentence is not false — but it silently
   "corrects" a quotation. Draft 2 below states both spellings instead.

**F4 — the phantom hash really is absent from both repos.**
`git cat-file -t a44b5a8` → `fatal: Not a valid object name a44b5a8` in
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` **and** in `/home/vgpnk/Projects/shokunin`.
`git cat-file -t ae95fe0` → `commit`; `git show -s --format='%H %s' ae95fe0` →
`ae95fe03269c958e3a6d2e4c0099cb32d615fc54 round-31: entry locator corrections (verifier_mode.py:18-21, :39-40) and final falsify evidence`,
committed `2026-10-25 06:07:26 -0300`. Its diff moves exactly the two locators
(`verifier_mode.py:22-23` → `:18-21`; `:35-38` → `:39-40`), so the erratum's content is grounded in the
commit it names.

## 3. Gate receipts (only what I actually ran)

- **G1 — frozen counter at the observed lane tip.** From `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
  at `7895588`: `python3 plans/round33_defects.py --lane . ; echo EXIT=$?` →
  `checks=6 defects=0` / `EXIT=0`. N3 and N4 are therefore already green on the committed tree; the
  instrument file itself is unmodified (`git status --porcelain` lists no `plans/round33_defects.py`).
- **G2 — my drafts against the counter, on pre-append bytes.** Extracted the reports as they stood before
  the append (`git -C /home/vgpnk/Projects/shokunin show 3d3ca566^:.ufo/reports/round-31/kengaku.md` →
  239 lines; `…round-32/kengaku.md` → 62 lines), appended the drafts in `/tmp/r33-R33FleetErrata/`, then
  imported the committed counter module and called its own predicates:
  `check_n3(L, tmp_r31)` → `''` (green); `check_n4(L, tmp_r32)` → `''` (green).
  Same-line distances measured on the drafted text: `a44b5a8` vs `superseded` = 74 chars on one line.
  Red control from the same harness: the line-wrapped intermediate draft returned
  `'no appended erratum supersedes the a44b5a8 citation'` (see F1).
- **G3 — L0 filing check, red/green.** Wrote a probe report holding only `## L0 questions` + Draft 3, then
  `sh plans/l0_filed_check.sh <probe> /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
  → `FILED   report:5 queue:163 kengaku | round-33 | decision packet: what committed evidence lifts the round-25`,
  `l0_filed_check: sections=1 questions=1 filed=1 unfiled=0`, exit 0.
  Same command against a copy of the queue with the `kengaku | round-33 |` row stripped →
  `UNFILED …`, `filed=0 unfiled=1`, exit 1. The drafting-key match is real, not incidental: both the
  drafted wording and the filed row normalise to the same 60-character key
  `decision packet: what committed evidence lifts the round-25` (59 chars after the trailing-space strip),
  the divergence between the two texts starting only at character 61 (`coverage cap` vs `L0 coverage cap`).
- **G4 — phantom-hash control.** Both `git cat-file -t a44b5a8` invocations fail (F4); `ae95fe0` and
  `112091c` both resolve to commits.
- **G5 — closure-tip identity.** `git rev-parse --verify '112091c^{commit}'` →
  `112091c2d9077e484b53512ca363d2fe6ba6fc5c`; `git log --oneline -1 bcd2a6c` →
  `bcd2a6c round-32: record rejected assimilation and C3 probe`.

Not run (and not claimed): the C1 adoption counter, the C3 `catalog_probe.py --verify` counter, the
census, any wave/seat process. Nothing in this report rests on them.

## 4. Draft 1 — append to `/home/vgpnk/Projects/shokunin/.ufo/reports/round-31/kengaku.md` (verbatim)

Byte-identical to `/tmp/r33-R33FleetErrata/draft-r31-append.md` (the file G2 verified). Begins with a
blank line, i.e. append as-is after the current last line (fleet `:246`).

```markdown

## Erratum (round 33, appended by the kengaku lane)

The "Erratum addendum (trend-verdict seat)" above records the locator fix as having landed "at lane tip
`a44b5a8`-class commits". That token is a phantom hash and the citation is superseded: `git cat-file -t
a44b5a8` fails in both the fleet repo and the lane repo — no such object exists.
The real locator-fix commit is `ae95fe0` ("round-31: entry locator corrections
(verifier_mode.py:18-21, :39-40) and final falsify evidence"), which moved the "Returns the explicit
mode when set" docstring citation from `verifier_mode.py:22-23` to `:18-21` and the step-precedence
docstring from `:35-38` to `:39-40`. This erratum is appended; the filed bytes above stand as written.
```

Window compliance (F1/F2): line 3 of the block holds `a44b5a8`, `superseded` and a second `a44b5a8`
within 74 characters on one physical line; `ae95fe0` appears in the block; `a44b5a8` is never removed.
Wrapping is therefore part of the contract — do not re-flow this block.

## 5. Draft 2 — append to `/home/vgpnk/Projects/shokunin/.ufo/reports/round-32/kengaku.md` (verbatim)

Byte-identical to `/tmp/r33-R33FleetErrata/draft-r32-append.md`. Begins with a blank line; append after
fleet `:69`.

```markdown

## Addendum (round 33, appended by the kengaku lane)

The round-32 closure verifier commit `112091c2d9077e484b53512ca363d2fe6ba6fc5c` (non-author
verifier spot-check, `corpus/lessons/round-32-verifier-spotcheck.md`) landed after this report was
filed. The lane tip cited under "Stale-lane" above (`bcd2a6c`, filed there as the 39-character
truncation `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d`) is therefore the pre-closure tip, not the
round-32 final state; its full hash is `bcd2a6c0d49e6c7d3c30307cf0cd43be6d9660d0`.
```

N4 compliance: contains `112091c` literally (inside the full 40-character hash), names the closure tip,
and labels the cited `bcd2a6c…` tip as pre-closure.

## 6. Draft 3 — append to `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (verbatim, one line)

One physical line, 274 characters, no wrapping (the filing checker reads the queue as one normalised
stream, and a single line keeps the row greppable):

```
kengaku | round-33 | decision packet: what committed evidence lifts the round-25 coverage cap on coverage (7) — candidates: PROVINCE coverage-surfaces section with N new resolving surfaces, N rounds of net-new admitted entries, or a rubric change? SCORECARD records the cap.
```

Provenance: `considerthese/2026-10-25.md` proposal 3 ("A decision packet for the round-25 L0 coverage
cap"), whose own words name the same three candidate classes plus a fourth ("the cap stays until the
absent surfaces return"). The row already at fleet `.ufo/l0-questions.md:163` carries the fourth class;
the line above is the wording this item specified and it files clean (G3). Either is acceptable to the
checker; the L1 should not append both.

## 7. Touched surfaces

- Written: this file only —
  `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-33/build/R33FleetErrata.md`.
- Scratch: `/tmp/r33-R33FleetErrata/` (`r31-pre.md`, `r32-pre.md`, `r31-verify.md`, `r32-verify.md`,
  `draft-r31-append.md`, `draft-r32-append.md`, `l0-report-probe.md`, `l0-queue-red.md`; ~50 KB total).
- Read-only, no writes: fleet `.ufo/reports/round-31/kengaku.md`, `.ufo/reports/round-32/kengaku.md`,
  `.ufo/l0-questions.md`; lane `plans/round33_defects.py`, `plans/round33-claims.md`,
  `plans/l0_filed_check.sh`, `corpus/lessons/round-33.md`, `considerthese/2026-10-25.md`; git
  log/show/diff/status/cat-file/rev-parse in both repos. No lane production file, no lane Git index, no
  `.ufo/state`, no `watchdog.log`, no `MANIFEST.json`, no sibling lane, nothing under `/home/vgpnk/Projects/shokuknow`.

## 8. Out of scope / open

- Applying anything to the fleet repo (the L1's fleet-commit), and any C1/C3 work.
- F2 (400-vs-300 in the frozen N3 text) is reported, not repaired: changing the claim text or the
  instrument after freeze is outside a leaf's write scope.
- F3's double-backtick markup in the already-committed round-31 block stays; append-only forbids rewriting
  it, and the counter is indifferent. If the L1 judges it worth a note, it must be a new one-line append.
- Tool installs this seat: **none**, so no channel/version table applies.

VERDICT: fleet-errata-drafted
