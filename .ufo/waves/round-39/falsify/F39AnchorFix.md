# F39AnchorFix — falsify the landed capture-per-token anchor check (wave 2)

Seat: `F39AnchorFix` (executor, kengaku round 39 / wave 2 FALSIFY). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
assigned tip `a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`. Object of attack: the landed
`plans/anchor_digest_check.py` (sha256 `11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2`) against its frozen
round-38 copy and against wave-1's multi-locator fixture (`R39AnchorUnion/`). Axes: **(1) calibration** (does the new
`capture-unanchored` leg red only what it claims, and is every round-38 class still live?), **(2) operability** (same argv/exit
contract, defect text that names the truth).

Result: **no lost round-38 behaviour and no false red at the tip**; two measured defects survive in the new leg — one
false-red class that the landed docstring explicitly promises stays green (**F1**), and a detail field that miscounts anchor
tokens (**F2**). Limits confirmed but not counted (erratum bypass, `url;` scanner, provenance-route precedence) are listed
separately in §5 with receipts.

## 0. Fixture and identity of the object

```
$ S=/fast/scratch/hyaku/kengaku-r39/F39AnchorFix; mkdir -p "$S"; export TMPDIR="$S"
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" &&
  git -C "$S/lane" checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
$ git -C "$S/lane" rev-parse --show-toplevel   -> /fast/scratch/hyaku/kengaku-r39/F39AnchorFix/lane
$ git -C "$S/lane" rev-parse HEAD              -> a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
$ sha256sum "$S/lane/corpus/SOURCES.md"        -> 63a2a3017b57a23b887ac868f700f8ae52e376c0182880bcfc308dfc2f01be8b
$ sha256sum "$S/lane/plans/anchor_digest_check.py"
  11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2
$ git -C "$S/lane" show 088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8:plans/anchor_digest_check.py > "$S/frozen_anchor.py"
$ sha256sum "$S/frozen_anchor.py"              -> 98847e8930304a23ab3e10dd27cfc3501738467b8871d8b725d24908e6c1f0b2
   (534 lines; the round-38 D3 copy wave-1 named)
```

The landed file is **exactly** the frozen file plus the wave-1 patch — no undeclared drift:

```
$ cp "$S/frozen_anchor.py" "$S/applied.py"
$ patch -s "$S/applied.py" < .ufo/waves/round-39/build/R39AnchorUnion/diff-vs-plans.patch
$ sha256sum "$S/applied.py"
  11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2   (== landed)
85 changed lines in 8 hunks; 591 lines vs 534.
```

Lane movement since the assignment: live `HEAD` is now `acf437542b00ae1723eba9dcc79d46af2e40d96e`; the single intervening
commit adds only `.ufo/waves/round-39/falsify-{dispatch,spec}.json`. `git diff --stat a6832f5..HEAD -- plans/anchor_digest_check.py corpus/SOURCES.md corpus/lessons/`
is empty, so the tip measurement below is the live-file measurement too.

## 1. Re-run at the tip — green, and the only verbose delta is the intended one

```
$ cd "$S/lane"
$ python3 plans/anchor_digest_check.py --lane .
  exit=0   rows=111 tokens=19 defects=0
$ python3 plans/anchor_digest_check.py --lane . --verbose | head -1
  EVIDENCE ref=head files=427 manifest_digests=36 rows=111 paths=495 bound_rows=21 unbound_rows=90
$ python3 plans/anchor_digest_check.py --lane . --evidence-ref index
  exit=0   rows=111 tokens=19 defects=0
$ python3 "$S/frozen_anchor.py" --lane .            -> exit=0  rows=111 tokens=19 defects=0
$ diff <(frozen --verbose) <(landed --verbose)      -> 1 changed line:
  24c24
  < ABBREV S036 prefix=afaae9dd matches=afaae9ddaf4deda… 
  > ABBREV S036 prefix=afaae9dd matches=afaae9ddaf4deda… capture=corpus/evidence/attrib-r23-stream.log
$ python3 .ufo/waves/round-39/build/R39AnchorUnion/probe_bind.py plans/anchor_digest_check.py .
  rows=111 rows_with_multi_capture=0 rows_with_multi_anchor_token=0
```

`rows=111 tokens=19` (wave-1 measured `109/17` at `7504738`; S117/S118 are the two round-39 rows). **No row at the tip binds
more than one capture, so no false red is reachable at the tip** — `capture-unanchored` cannot fire. A read-only run against
the live lane (`python3 plans/anchor_digest_check.py --lane .` in `/home/vgpnk/Projects/shokunin/kengaku-shokunin`) prints the
same `rows=111 tokens=19 defects=0`, exit 0; that lane had 4 untracked round-39 paths and no modified tracked file.

## 2. Wave-1's multi-locator fixture, replayed at the assigned tip

Driver unchanged from wave 1 (`R39AnchorUnion/fixture_union.py`, sha256 `5ae644da4d7eba…`), both tools, all eight cases,
restore asserted per case. Receipt `F39AnchorFix/fixture_tip.txt`.

| case | edit to the S111 row | LANDED (tip, `11bb2cad`) | FROZEN (`088f7c36`, `98847e89`) |
|---|---|---|---|
| CONTROL | none | `rows=111 tokens=19 defects=0` exit 0 | same |
| D | +regex-log URL in scope cell, anchor ← its digest | `defects=1` `capture-unanchored` exit 1 | `defects=0` exit 0 |
| F | same URL in the anchor cell, anchor ← its digest | `defects=1` `capture-unanchored` exit 1 | `defects=0` exit 0 |
| D2 | both locators, one token each | `tokens=20 defects=0` exit 0 | same — no false red |
| DUP | both locators, both tokens the row's own digest | `defects=1` `capture-unanchored` exit 1 | `defects=0` exit 0 |
| A | anchor ← S108's digest, no second locator | `defects=1` `digest-wrong-capture` | byte-identical defect line |
| L | anchor token deleted (single-capture row) | `tokens=18 defects=0` exit 0 | same |
| M | A + working-tree `Erratum (round 37): S111 …` | `defects=2` (`erratum-incomplete` + `digest-wrong-capture`) | byte-identical |

```
==== CASE D ====
LANDED exit=1
LANDED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
LANDED | rows=111 tokens=19 defects=1
FROZEN exit=0
FROZEN | rows=111 tokens=19 defects=0
RESTORED corpus/SOURCES.md sha256=63a2a301… status-lines=0
```

Wave-1's claims hold at the new tip row count (they were measured at `109/17`): D/F/DUP red only under the landed copy,
D2 green, A and M byte-identical, every case restores `status-lines=0`.

## 3. Diff review — what the change can move, and that none of it is lost round-38 behaviour

Behavioural surface of the 8 hunks, read against the code: the *only* new decision is the coverage leg
(`plans/anchor_digest_check.py:547-556`); `claimed` bookkeeping (`:484`, `:539`, `:507-513`) feeds it and changes no verdict;
`BIND+`/`CAPTURES`/`capture=` are verbose-only additions. Everything else is docstring. Differential cases run on the same
clone (`F39AnchorFix/probe_extra.txt`, both tools, 17 cases, restore asserted): cases in which the two tools disagree are
only the additive-locator shapes.

| case (row, edit) | LANDED | FROZEN | verdict |
|---|---|---|---|
| S111 ← S108 digest, no second locator (round-38 cross-row) | `digest-wrong-capture` | byte-identical | preserved |
| S114 ← S108 digest | `digest-wrong-capture` | byte-identical | preserved |
| S111 token truncated to 63 hex | `digest-short` | byte-identical | preserved |
| S110's 63-hex anchor with the erratum removed from the working-tree lesson | `digest-short` | byte-identical | preserved (S110 shape) |
| S110 ← S111 digest (erratum's cited wrong token no longer matches → no exemption) | `digest-wrong-capture` | byte-identical | preserved |
| S111 token uppercased | `digest-uppercase` | byte-identical | preserved |
| S111 token deleted (single capture) | green, `tokens=18` | same | preserved |
| S036 `sha256 afaae9dd…` (abbrev) | green | same | preserved |
| D2 with the second capture anchored by an 8-hex abbreviation | green | green | new leg does not false-red abbreviations |
| D3 (two extra locators, one token) | 2 × `capture-unanchored` | exit 0 | intended strictness |
| GLUE-OWN (`url;` second locator, no token for it) | green | green | limit, §5 |

No false red at the tip; no round-38 class dropped, renamed, or re-scoped; A/M defect text byte-identical.

## 4. Defects found

### F1 — calibration: a multi-locator row with **no anchor token at all** is reddened, contrary to the tool's own contract

The landed docstring states the presence limit twice:

```
plans/anchor_digest_check.py:102-103  "Rows that carry no anchor token raise nothing (see the presence limit below), so a
                                       multi-locator row with no claim stays green."        (22 words)
plans/anchor_digest_check.py:132-133  "Presence: a row that carries no anchor token makes no claim and raises nothing"
```

Wave-1's report says the same (`R39AnchorUnion.md` §7: "The coverage leg only applies to a row that carries at least one
token"). The code does not implement it — the leg's only guard is `if per and not ex and len(per) > 1:`
(`plans/anchor_digest_check.py:547`); there is no `r["atoks"]` test. Fixture: S111 keeps its configure-git-webserver URL,
gains the regex-log URL (two captures), and its anchor token is deleted — the row makes no digest claim.

```
$ python3 - <mutate clone>            # F39AnchorFix/probe_no_token.txt
LANE …/F39AnchorFix/lane HEAD a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
PRISTINE corpus/SOURCES.md sha256=63a2a3017b57…
LANDED exit=1
LANDED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-0-anchor-token-none-resolves-capture-corpus/evidence/round36/tb2-regex-log/test_outputs.py loc=corpus/SOURCES.md:126
LANDED | DEFECT S111 anchor token=- class=capture-unanchored detail=row-names-2-captures-0-anchor-token-none-resolves-capture-corpus/evidence/round37/tb2-git-webserver/test_outputs.py loc=corpus/SOURCES.md:126
LANDED | rows=111 tokens=18 defects=2
FROZEN exit=0
FROZEN | rows=111 tokens=18 defects=0
RESTORED sha256=63a2a301… status-lines=0
```

This is a false red of exactly the shape the docstring promises is green: exit 1 on a row that asserts no digest (frozen:
exit 0). It is unreachable at the tip only because no row binds two captures, and it becomes reachable the moment an author
cross-references a second capture in prose. The same missing guard is why a misplaced token also produces coverage defects
(below). Repair is one condition, e.g. `if r["atoks"] and per and not ex and len(per) > 1:`.

### F2 — operability: the `capture-unanchored` detail counts tokens from **every** cell while calling them anchor tokens

```
plans/anchor_digest_check.py:551   ntok = sum(1 for _, _, _ in r["rtoks"])
plans/anchor_digest_check.py:554-556  "detail=row-names-{len(per)}-captures-{ntok}-anchor-token-…"
```

`r["rtoks"]` is every `sha256` token in the row; only `r["atoks"]` (cell index 5) are anchor tokens. Two receipts:

```
# F39AnchorFix/probe_limits.txt, L3: two locators, token moved into the scope cell (anchor cell empty)
LANDED | DEFECT S111 … class=token-outside-anchor detail=sha256-claim-in-cell-5-of-11
LANDED | DEFECT S111 … class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-…/round36/tb2-regex-log/test_outputs.py
LANDED | DEFECT S111 … class=capture-unanchored detail=row-names-2-captures-1-anchor-token-none-resolves-capture-…/round37/tb2-git-webserver/test_outputs.py
LANDED | rows=111 tokens=19 defects=3          (FROZEN: defects=1 — only token-outside-anchor)

# F39AnchorFix/probe_ntok.txt: two locators, ONE anchor token (S111) + one stray token in the teaches cell
LANDED | DEFECT S111 … class=capture-unanchored detail=row-names-2-captures-2-anchor-token-none-resolves-capture-…/round36/tb2-regex-log/test_outputs.py
LANDED | rows=111 tokens=20 defects=2          (FROZEN: defects=1)
```

So the message tells an author "2 anchor-token" for a row with one, and "1 anchor-token" for a row with none in the anchor
cell. A reader chasing `capture-unanchored` is pointed at a capture when the real fault is a misplaced token. Fix:
`ntok = len(r["atoks"])` (and, with F1's guard, the misplaced-token row emits only `token-outside-anchor`).

## 5. Limits confirmed by measurement (not defects: disclosed in wave-1 §6/§7 or inherent to the repair workflow)

- **Erratum bypasses the coverage leg.** Fixture D plus one append-only line
  `Erratum (round 37): S111 anchor sha256 <S108 digest> is wrong; the correction is sha256 <S111 digest>` →
  `LANDED exit=0 rows=111 tokens=19 defects=0` (`probe_limits.txt` L1b; FROZEN also 0). The round-38 cross-row shape A plus
  the same line is likewise `defects=0` (L1c). Wave-1 §7 states the erratum "bypasses every anchor class including
  coverage"; the landed limits paragraph (`:132-135`) lists only presence and provenance, so a reader can over-trust the
  leg. Naming it in the limits list would cost one sentence.
- **`url;` locator is never bound.** A row that writes the second URL glued to a semicolon is green with one token
  (`GLUE-OWN`: `LANDED exit=0`, `FROZEN exit=0`) — `URL_RAW`'s `([^\s|`)\]]+)` swallows the `;`, so the second capture is
  not even in `per`. Acceptance stays closed (wave-1's GLUE receipt reproduced: the second digest still reds
  `digest-wrong-capture`), but the "every named capture is anchored" guarantee is syntax-dependent.
- **Provenance-route precedence.** `bind_row` returns provenance-row captures *instead of* URL captures
  (`plans/anchor_digest_check.py:318-319`), so a row that gains a `PROVENANCE.md` line for another capture has its own URL
  capture dropped from `per`. Measured corollary: an uncommitted `PROVENANCE.md` edit is invisible under the default
  `--evidence-ref head` (`probe_limits.txt` L2: BIND still `by=url-task`), so this route needs a staged capture to exercise
  (`--evidence-ref index`, not fixtured here). Pre-existing, unchanged by this diff; the round-39 sentence "the row's
  locator set is treated as a set of claims of equal standing" (`:94-95`) is true only within one binding route.
- **Presence.** 19 rows carry an anchor token at the tip (`rows_with_atoks=19`, via `parse_rows`), 92 carry none; the
  docstring's "92 of 109 rows carry none at `7504738`" is historical and accurate for that tip.
- **Manifest branch cannot be spoofed today.** 38 `SHA256SUMS` entries across `corpus/evidence/`, 0 whose digest differs
  from the committed file's bytes, 0 naming a file that is not committed — so a token accepted through
  `capture_digests`' manifest label is the capture's real digest at the tip.

## 6. Operability, no-harm, tooling

- Invocation/exit contract unchanged: `python3 <tool> [--lane DIR] [--evidence-ref head|index] [--verbose]`, exit 0/1/2,
  final line `rows=… tokens=… defects=…`; stdlib only; writes no file; `--evidence-ref index` on the clean clone prints the
  same `rows=111 tokens=19 defects=0`. All new output is additive (one class, `BIND+`, `CAPTURES`, `capture=`).
- Writes by this seat: `.ufo/waves/round-39/falsify/F39AnchorFix.md` and
  `.ufo/waves/round-39/falsify/F39AnchorFix/` (`fixture_tip.txt`, `probe_extra.{py,txt}`, `probe_limits.{py,txt}`,
  `probe_no_token.txt`, `probe_ntok.txt`). No lane file, index or jj state touched: every fixture mutated only
  `$S/lane`'s working tree and every case ends `RESTORED … status-lines=0`; `$S` removed before filing.
- Tooling: nothing installed or upgraded; `python3 3.14.8`, `git 2.56.0`; `pacman` not run.
- Not covered: the "byte-identical captures share one token" branch (needs two captures of identical bytes in one row —
  code-inspected at `:507-513`/`:539`, no fixture); `--evidence-ref index` with staged-only captures; a row bound through
  multiple `PROVENANCE.md` lines.

VERDICT: anchor-fix-2-defects
