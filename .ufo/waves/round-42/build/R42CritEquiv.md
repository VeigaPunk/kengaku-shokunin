# R42CritEquiv — equivalents, incidental kills, and the denominator (round 42 wave 1, C1 calibration)

Seat: critic (leaf). Lane `kengaku-shokunin` at `fda71ae033224e1d0ed5ddd0fdcb1b63a02f2473`. Frozen tools unchanged:
`sha256sum plans/anchor_digest_check.py plans/order_check.py` →
`11bb2cad87be1c29c2d5abe8313d487d73f71ba49a40d7d0dc80ec26c70fd4c2` and
`948d5e1d2b3429d76a598fd11c4b22856d9f43ec093efd2c6aa0025aa0fc6ecc`, equal to `PINS` in
`plans/round42_c1_verify.py` and to the digests in `plans/round-42-claims.md`. Nothing in the lane was written.

Read in full before judging: `plans/round-42-claims.md`; `plans/round42_c1_verify.py` (MUTANTS 14, `exhibits()`,
attribution span, main); `plans/round40_c1_verify.py` (frozen 21); `plans/anchor_digest_check.py` (whole file);
`plans/order_check.py` (whole file); `.ufo/waves/round-42/claims/witness-run.txt`; `.ufo/waves/round-42/claims/witness/w_anchor.py`
and `w_order.py`; `.ufo/waves/round-40/falsify/F40XMutAnchor/xmut_table.py`; `.ufo/waves/round-40/falsify/F40XMutLedgerOrder/xmut_driver.py`;
`plans/battery40/a_bind.py`; `.ufo/waves/round-41/build/R41PlanNext/near-variants-r40-counter.txt` and `near40_survivors_only.txt`.

Envelope (Q32) for every probe below — `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin
--tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>`; `date +%T` 17:21:22 / 17:23:10 /
17:23:26 / 17:23:40 / 17:24:21 and after each run; `ls -A /home/vgpnk/.local/bin | sha256sum` =
`436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` before and after, unchanged. Scratch
`/fast/scratch/hyaku/kengaku-r42/R42CritEquiv` (`trap rm -rf` on that dir only); no git mutation in the lane, no
commit anywhere; fixture repos are my own `git init` inside scratch.

---

## 1. Equivalents: none of the 14 (`e = 0`)

Test applied to each frozen row: is there an input on which the mutant differs from the reference, **in the declared
direction, because of the span the `adv` cell quotes**? A mutant is an "equivalent" only if no such input exists. Each
row below has a from-nothing input that isolates the quoted clause (the pre-freeze witness builds one; I re-derived the
mechanism from the reference source and ran the two hard cases myself). Advert-cause is checked against the docstring
line in the `adv` cell, not against the mutant's own prose.

| id | isolating input | ref → mutant | declared direction | cause = quoted clause? |
|---|---|---|---|---|
| X1 | row binds only through a `PROVENANCE.md` table line carrying its id (`w_anchor.py:52-61` shape) | rc 0 → 1, `anchor-unbound` | rc-mirror | yes — `anchor:50-52` |
| X3 | row URL resolves only via a `PROVENANCE.md` URL, no `task.toml` slug exists | 0 → 1, `anchor-unbound` | rc-mirror | yes — `anchor:57-61` |
| X6 | row binds capture A by lane path, anchor is sibling capture B's committed digest | `digest-wrong-capture` → `digest-unknown`, rc 1 → 1 | silence | yes — `anchor:89-92` (label swap only, §2) |
| X7 | anchor is a made-up 64-hex token | `digest-unknown` → `digest-wrong-capture`, rc 1 → 1 | silence | yes — `anchor:92-93` (label swap only, §2) |
| X9 | census-shaped row with 9 or 10 cells | `row-malformed`, rc 1 → 0 | rc-silence | yes — `anchor:34-35` |
| X12 | `task.toml` carries `name = "plain-slug"`; URL task component `plain-slug` | 0 → 1, `anchor-unbound` | rc-mirror | yes — `anchor:55-56` |
| X13 | capture rewritten and staged, row claims the staged digest, **argv omits `--evidence-ref`** | 1 (`digest-unknown`) → 0 | rc-silence | yes — `anchor:73` |
| X14 | erratum line carries an **uppercase** 64-hex token outside A, plus the row's real digest | 1 (`erratum-digest-unresolved`) → 0 | silence | yes — `anchor:111-113` |
| X15 | erratum cites a sibling capture's digest; row names a different capture | 1 (`digest-unknown`,`erratum-incomplete`) → 0 | rc-silence | yes — `anchor:108-112` |
| XO1 | one commit carries claims + receipt + the `P10 DEFECT receipt unreadable` excuse line | 1 → 0 | rc-silence | yes — `order:17,183` |
| XO3 | receipt added, removed, claims frozen, receipt re-added | 1 (`receipt-before-claims`) → 0 | rc-silence | yes — `order:18,188` (narrow, §2) |
| XO5 | honest freeze+receipt, then a `gate: P10 ok …` claims blob committed **after** the receipt | 0 → 1 (HIT) | rc-mirror | yes — `order:114-117` |
| XO6 | claims blob carrying `P10 PASS receipt unreadable` | 0 → 1 (HIT) | rc-mirror | adjacent, not the quoted sentence, §2 |
| XO7 | claims blob carrying `CASE c1 observed=timeout` | 1 (HIT) → 0 | rc-silence | yes — `order:54-55` |

Nothing here is equivalent. The three rows I would have expected to collapse — X6/X7 (inverse label swaps of one branch
pair) and XO3 (redundant with clause 1 on every natural history) — still differ on some input, see §2.

Two structural checks that rule out "hidden equivalence" for the rest: (i) every mutated span is inside a branch that the
reference reaches on the witness's end state (`witness-run.txt` `attributed=L… hits≥1`, and the counter rejects a span
that does not execute); (ii) the counter's `null_detected=0` on a second unmodified run shows the differences are not
flakes. The one row whose quoted sentence is *not* what its mutation changes is XO6, and the freeze already labels it
`indirect` (`plans/round-42-claims.md`, "13 `direct`, 1 `indirect`").

## 2. Incidental kills in `witness-run.txt`: none by the strict test (`i = 0`), three calibration limits

Strict test: a kill is incidental if the reference/mutant difference in `witness-run.txt` is not produced by the clause
the `adv` cell quotes. Because each variant is the reference with exactly one span replaced and both variants are run on
the same end state, the difference is *causally* the span; I checked each witness build against the reference source and
found no case where the kill rides on a different clause, an unhandled exception, or a fixture artefact. Three limits
must still be named, because they bound what the 14 kills calibrate.

1. **X6 and X7 change only the printed class; the exit code stays 1 in both directions.** Measured (one repo, two rows —
   `S930` anchored on a sibling capture's digest, `S931` on a made-up token):
   `REF rc=1 classes=[digest-wrong-capture, digest-unknown]`, `X6 rc=1 classes=[digest-unknown, digest-unknown]`,
   `X7 rc=1 classes=[digest-wrong-capture, digest-wrong-capture]` (receipt `R42CritEquiv/probe_lbl.txt`, script
   `probe_lbl.py`). The `silence` direction is defined on class sets (`exhibits()` in `plans/round42_c1_verify.py`), so
   these are legitimate kills, but an operator reading only rc sees no difference; and **one** fixture carrying both rows
   kills both mutants at once. A wave-1 battery that reuses one wrong-capture row for X6 and one made-up-token row for X7
   is safe (each kills only its own mutant), but the pair should not be described as two independent behaviours.
2. **XO3's unique input is an artificial history.** Clause 2 is not observable on the natural inversion: in a repo where
   the receipt is committed before the claims and is still present at the freeze, the reference fails **both** clauses and
   the XO3 mutant still exits 1 through clause 1 — measured `REF rc=1 ['ORDER FAIL freeze-contains-receipt …',
   'ORDER FAIL receipt-before-claims …']`, `XO3 rc=1 ['ORDER FAIL freeze-contains-receipt …']`. Only the
   delete-then-freeze-then-re-add shape separates them: `REF rc=1 ['ORDER FAIL receipt-before-claims 1148ca9… is an
   ancestor of 76f5ba5…']`, `XO3 rc=0` (receipt `R42CritEquiv/probe_xo3.txt`). The kill is real and is the advertised
   clause; the clause's *coverage* is one history shape, and clause 1 already covers the common one.
3. **XO6's mutation changes a verdict the gate never prints.** Its quoted sentence (`order:52-53`) is about the `gate: `
   echo prefix; the mutation widens the verdict alternation with `PASS`. The reference gate prints
   `f"{name} {'ok' if ok else 'DEFECT'} {note}"` (`plans/pkg_gate.py:301`), so `P10 PASS` cannot occur in a real
   claims blob and the fixture must forge it. The kill is a genuine strictness difference (the gate stays strict about
   `PASS`) and the freeze discloses it as the one `indirect` cell; it should not be counted as demonstrating `order:52-53`,
   which stays unmutated (§3, row k).

## 3. Denominator: advertised behaviours with no mutant in the 35

Union of the frozen lists over the two tools of this round: 28 mutants — 11 anchor + 3 order in
`plans/round40_c1_verify.py` (A01 A02 A03 A06 A08 A09 A15 A17 A21 A22 A27; O04 O12 O14) and 9 + 5 in
`plans/round42_c1_verify.py` (X1 X3 X6 X7 X9 X12 X13 X14 X15; XO1 XO3 XO5 XO6 XO7). The other 7 rows of the frozen 21
are `ledger_tip.py` (L01 L05 L06 L11 L14 L15 L21) and out of this surface. The 28 cover 19 distinct docstring locations:
anchor `31`, `34-35`, `37-39`, `44-46`, `50-52`, `55-56`, `57-61`, `62-64`, `73-76`, `81-83`, `84-87`, `88-92`, `96-98`,
`108-113`; order `14-16`, `17`, `18-19`, `26-27` (round number), `37` (blob type), `52-55`, `114-117`.

Rule for counting an *unlisted advertised behaviour*: a docstring sentence (file:line) that names an observable outcome
for some input the tool accepts, with no frozen mutant altering exactly that observable; where two sentences share one
observable, one mutant covers both. Under that rule, **u = 18** (9 anchor + 9 order).

| # | file:line | advertised behaviour | why no mutant |
|---|---|---|---|
| a | `anchor_digest_check.py:27` | exit 2 usage error (bad args / missing lane / absent `SOURCES.md` / no git) | no anchor `error`-direction row; `O14` is order's, `L01` ledger's |
| b | `anchor:76` | `--verbose` prints the mode, bindings and resolutions | no mutant; no counter reads verbose output |
| c | `anchor:88` | `digest-short` class (non-ellipsis hex run shorter than 64) | `A03` moves the ellipsis bound only; `X16` relabels the uppercase branch only |
| d | `anchor:88` | `digest-long` class (hex run longer than 64) | no mutant emits or suppresses it |
| e | `anchor:99-100` | a token resolving to several of the row's captures is **not** a defect (byte-identical captures) | `A27` covers only the `capture-unanchored` half |
| f | `anchor:102-103` | a row with no anchor token raises nothing | no mutant (named as a presence limit, stated as behaviour) |
| g | `anchor:106-108` | lessons are read from the working tree for paths committed at HEAD (an uncommitted erratum counts) | `X5` changes the round-number regex, not the read source |
| h | `anchor:114-115` | an erratum whose row was since repaired stays valid (no stale-erratum defect) | none |
| i | `anchor:24` | read-only; stdlib only; writes no file | none (no side-effect mutant) |
| j | `order_check.py:12` | commits only — working tree and index are ignored | none; `O12`/`XO5` change the read set, not worktree-vs-commit |
| k | `order:14-15` | a gate `P10` line with or without the `gate: ` echo prefix | `O04` changes the excuse, `XO6` the verdict; the prefix itself is unmutated |
| l | `order:26` | exit 2 when the lane is not a git work tree | none |
| m | `order:26` | exit 2 when claims or receipt were never committed | none |
| n | `order:26` | exit 2 on bad arguments | none |
| o | `order:41` | an uncommitted receipt is a setup error (2), not a pass (HEAD check) | none |
| p | `order:29-31` | read-only: six named read commands, writes nothing, imports no probe/gate/counter, never runs the probe | none |
| q | `order:37-38` | every blob under `claims/` is read, so only the pattern matters, not the file name | `O12` covers the blob-type half only; a filename filter is unmutated |
| r | `order:14` | the scanned directory is derived from the claimed round number (`.ufo/waves/round-NN/claims/`) | `O14` covers the name→error path, not the name→dir mapping |

If the L1 prefers the narrower denominator that drops the five setup/exit-2 rows (a, l, m, n, o) and the two read-only
invariants (i, p), the count is **11**. I report 18 because those rows are advertised behaviour with an observable
(an exit code, a write, a read set) that a from-nothing fixture can exercise.

Two things the 18 say about the round: the calibration surface is *wider than the 14 rows assume* — the biggest gaps are
the whole setup/exit-2 path on both tools and the `--verbose`/read-only contracts — and the gaps are cheap to price
(fourteen of the eighteen are a single exit-2 or read-set fixture away).

## 4. The round-40 near-variants left out: 5 honest, 4 honest-in-substance but mis-recorded, 7 correctly out

Source of the kill column: `.ufo/waves/round-41/build/R41PlanNext/near-variants-r40-counter.txt`
(`MUTANTS total=30 killed=10 survived=20`), reproduced from `plans/round40_c1_verify.py`'s unedited machinery.

| id | round-40 record | verdict |
|---|---|---|
| X8 | killed by `a_row-token-in-teaches`, declared `token-outside-anchor` | honest direct kill (`anchor:81-83`) |
| X10 | killed by `a_tok-upper-anchor`, declared `digest-uppercase` | honest direct kill (`anchor:37-39`) |
| X16 | killed by `a_tok-upper-anchor`, declared `digest-uppercase` | honest direct kill, label-only shape like X6/X7 |
| XO2 | killed by `o_gate-claims-gitlink` (only accept fixture) | honest direct kill — inverted comparison rejects every honest repo |
| XO4 | killed by `o_gate-claims-gitlink` | honest direct kill, same shape |
| X2 X4 X5 X11 | all four "killed by=`a_bind-a17-index-bytes`" | **kill provenance is the cloned lane, not the fixture** — correct the record |
| XL1–XL6 | "text-only" (survivors of battery40) | accurate *and* off-surface: they are `plans/ledger_tip.py` output-label rows, not anchor/order; `R41PlanNext.md:59` names why `classes()` cannot read them |
| XL7 | killed by `l_rows-open-row` | honest kill (the harness's positive control) |

Evidence for the four: `plans/battery40/a_bind.py:83-105` builds `a17` as `ctx.clone(d / "lane")` — a clone of the whole
lane — with one added row `S903` and `--evidence-ref index`. I rebuilt that fixture exactly and ran the reference plus the
near-variants (`R42CritEquiv/probe_a17.txt`):

```
REF  rc=0 defects=0 []
X1   rc=0 defects=0 []
X2   rc=1 defects=3 [('S036', 'anchor-unbound'), ('S114', 'anchor-unbound'), ('S124', 'anchor-unbound')]
X3   rc=0 defects=0 []
X4   rc=1 defects=1 [('S110', 'digest-short')]
X5   rc=1 defects=1 [('S110', 'digest-short')]
X6   rc=0 defects=0 []
X11  rc=1 defects=2 [('S036', 'anchor-unbound'), ('S124', 'anchor-unbound')]
X12  rc=0 defects=0 []
```

Every defect lands on a lane row (`S036`, `S114`, `S124` bind by explicit lane path; `S110` is the live
`corpus/lessons/round-37.md:32` erratum); **none on `S903`, the row the fixture adds**. The fixture's own end state — the
index-vs-HEAD byte view — contributes nothing to these four kills. The round-40 counter had no attribution rule, so a
broad `rc 0→1` on a lane clone counted.

Are they nevertheless honestly excluded? Yes, on substance — all four are non-equivalent **and** killable from nothing,
which I measured with a two-row repo built by `git init` with no lane clone (`R42CritEquiv/probe_none.txt`):

```
REF  rc=0 defects=[] 
X2   rc=1 defects=[('S920', 'anchor-unbound'), ('S921', 'anchor-unbound')] 
X3   rc=0 defects=[] 
X4   rc=1 defects=[('S921', 'digest-short')] 
X5   rc=1 defects=[('S921', 'digest-short')] 
X11  rc=1 defects=[('S920', 'anchor-unbound')] 
X1   rc=0 defects=[] 
```

(Reading: `X2` loses the row-path route, so both rows unbind; `X4`/`X5` lose the erratum exemption, so `S921`'s 32-hex
anchor is `digest-short`; `X11` loses the committed-bytes view, so the manifest-less `S920` capture unbinds; `X1`/`X3` are
unaffected controls.)

So the exclusion is sound; only its stated provenance is wrong. Smallest safe correction: in the wave-1 record (and any
lesson note), say "X2 X4 X5 X11 were killed by a clone-broad battery40 fixture on lane rows S036/S114/S124/S110; they are
non-equivalent and killable from nothing (see this report §4)", instead of "killed by battery40".

## 5. Consequences for wave 1 (C1 executors), no lane edit implied

1. **X13's fixture must omit `--evidence-ref`.** Passing the flag explicitly makes the mutant and the reference identical;
   the kill then silently becomes an `attributed` survivor.
2. **XO6/XO7 need a forged claims blob** (`P10 PASS …`, `CASE … observed=timeout`); keep `defects: []` and expect
   `accept`/`reject` respectively — the class channel is not used for order.
3. **X9 needs a short row (9–10 cells), not a 12-cell row** — a 12-cell row is `A09`'s mutant, and a battery that reuses
   one row for both would leave X9 alive (`>` vs `!=` are the two halves).
4. **Do not reuse one repo for X6 and X7** unless the intent is a shared fixture: one repo with both a sibling-digest row
   and a made-up-token row kills both (measured, §2 limit 1) — legitimate, but it halves the fixture count without adding
   evidence.
5. **XO3 needs the delete-then-freeze-then-re-add history**; the natural inversion is killed by clause 1 in both variants.
6. The four `a17` clones are not a precedent: round-42 fixtures must be built from nothing, so `S036/S114/S110`-style lane
   content cannot be relied on as a kill source.

## 6. Limits of this review

- I did not rerun the frozen counter itself (the witness receipt is other seats' object); I reconstructed each witness
  end state from source and ran the three probes above on my own fixtures.
- `u = 18` is a judgement about sentence granularity; the raw list of docstring sentences is in §3 so a different
  granularity can be recomputed. The narrowest defensible reading is 11.
- The claims' `ADVERTISED direct=13 indirect=1` counts adv *kinds* over the 14 rows, not coverage; it is not evidence
  about the 18 gaps.

Receipts (scripts + outputs, sha256 in `R42CritEquiv/COMMANDS.txt`): `R42CritEquiv/probe_a17.py`, `probe_a17.txt`,
`probe_none.py`, `probe_none.txt`, `probe_xo3.py`, `probe_xo3.txt`, `probe_lbl.py`, `probe_lbl.txt`.

VERDICT: equivalents-0-incidental-0-unlisted-advertised-18
