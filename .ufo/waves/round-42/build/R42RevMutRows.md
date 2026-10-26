# R42RevMutRows — review of the 14 frozen C1 mutant rows (round 42, wave 1)

Seat: reviewer (leaf). Date 2026-10-26. Scope: the `MUTANTS` table frozen in
`plans/round42_c1_verify.py` (14 rows), checked against `plans/anchor_digest_check.py` (pin
`11bb2cad…`) and `plans/order_check.py` (pin `948d5e1d…`), the frozen witness run
`.ufo/waves/round-42/claims/witness-run.txt`, the round-40 ledgers, and the direction-mislabel control.
Nothing frozen was edited; I wrote only my report dir and my scratch.

## 1. Method

- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`;
  `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r42/R42RevMutRows/lane` (verified before any write).
- Clone HEAD is `fda71ae` (wave-1 dispatch), two commits past the freeze `bc856d8`. Faithfulness check:
  `git -C "$S/lane" diff --stat bc856d803576e182b6c3c12afc6b23f392071c25..HEAD -- plans/ .ufo/waves/round-42/claims/`
  → **empty** (rc=0), and `sha256sum` of `witness-run.txt` is identical in lane and clone
  (`d47428cbaca977ca1d51e90da81f9f9282229d8bc5510ea377ed9cc7a8a2beb4`). The frozen bytes I reviewed are the freeze's bytes.
- Static row check: `verify_rows.py` (receipt copy in my report dir) ast-parses the frozen `MUTANTS`
  table, then per row: (a) locates the `adv` quote in the named tool as a contiguous run after stripping
  markdown backticks and `**` and collapsing whitespace (the quotes drop some decoration: X1 drops
  `**`/backticks, X13/X15/XO5/XO6 keep backticks; punctuation otherwise exact); `...` inside XO3's quote
  is treated as a truncation marker and the pre-ellipsis text is located; (b) counts the quote's words;
  (c) checks the found line span lies inside the cited line spec; (d) checks `old` occurs exactly once
  and notes its line; (e) compares the table's `direction` with the `MUTANT` line in `witness-run.txt`;
  (f) compares the witness run's `attributed=L<n>` with `old`'s line; (g) compares the run's truncated
  label echo with `adv[:90]`.
- Empirical check: the witness run re-executed in my clone inside the mandated seat envelope (§2).

## 2. Witness re-run inside the envelope (Q32)

Command (my `rerun.sh`, receipt copy in my report dir), cwd = my clone:

```
ENVELOPE bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 plans/round42_c1_verify.py --lane . --battery-dir .ufo/waves/round-42/claims/witness --work $S/w
ENVELOPE start 17:22:56 cwd=/fast/scratch/hyaku/kengaku-r42/R42RevMutRows/lane
ENVELOPE end 17:22:58 exit=0 local_bin_before=763032563d3739aa6513b8aa3f0852d1cd7e7e4ba0a21165a391fc4026d60a78 after=763032563d3739aa6513b8aa3f0852d1cd7e7e4ba0a21165a391fc4026d60a78
```

`ls -A /home/vgpnk/.local/bin | sha256sum` unchanged across the run; stderr empty. The frozen run's
ENVELOPE lines differ only as expected (L1 used `--ro-bind /home/vgpnk /home/vgpnk`, its own scratch
bind, cwd = the lane, times 17:03:50→17:03:53, and prints a 16-hex prefix `763032563d3739aa` of the same
listing digest). **Byte comparison, ENVELOPE lines aside: `diff -u` empty — the re-run is byte-identical
to the frozen `witness-run.txt`**, including every FIXTURE line, all 14 MUTANT lines with their
`killed by=`/`attributed=L<n>`/`hits=<n>`, `BATTERY fixtures=14 wrong=0 tampered=0 sidechannel=0`,
`MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`,
`MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `ADVERTISED direct=13 indirect=1 none=0`,
`PINS total=2 mismatched=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 n/a (non-default battery or mutant
subset)`, exit 0.

## 3. Per-mutant table

"found" = lines where the quoted words actually sit (my verifier); "old@L" = the `old` string's line in
the unmutated tool, which must equal the witness run's `attributed=L<n>` (every replacement preserves
line count: all single-line except X6's two-line `old`→two-line `new`). All 14 rows: `old` occurs
exactly once (`oldcount=1`), `label[:90]` echo matches the frozen run's MUTANT lines, and the
class/direction consistency rule holds (silence rows carry a class, the rest `-`).

| id | tool | class | dir (table) | dir (witness-run) | adv cite | quote found at | words | cite | old@L=attr | kind |
|----|------|-------|-------------|-------------------|----------|----------------|-------|------|-----------|------|
| X1 | anchor | - | rc-mirror | rc-mirror ✓ | :50-52 | 50-51 | 15 | OK | 318 ✓ | direct ✓ |
| X3 | anchor | - | rc-mirror | rc-mirror ✓ | :57-58 | **59-61** | 18 | **MISS** | 343 ✓ | direct ✓ |
| X6 | anchor | digest-wrong-capture | silence | silence ✓ | :89-92 | 89-90 | 14 | OK | 527 ✓ | direct ✓ |
| X7 | anchor | digest-unknown | silence | silence ✓ | :92-93 | **91-92** | 11 | **MISS** | 535 ✓ | direct ✓ |
| X9 | anchor | - | rc-silence | rc-silence ✓ | :34-35 | 34-35 | 17 | OK | 477 ✓ | direct ✓ |
| X12 | anchor | - | rc-mirror | rc-mirror ✓ | :55-56 | 55 | 11 | OK | 256 ✓ | direct ✓ |
| X13 | anchor | - | rc-silence | rc-silence ✓ | :73 | 73 | 12 | OK | 570 ✓ | direct ✓ |
| X14 | anchor | erratum-digest-unresolved | silence | silence ✓ | :111-113 | 112-113 | 22 | OK | 458 ✓ | direct ✓ |
| X15 | anchor | - | rc-silence | rc-silence ✓ | :108-110 | 109-110 | 19 | OK | 455 ✓ | direct ✓ |
| XO1 | order | - | rc-silence | rc-silence ✓ | :17,183 | 17 | 13 | OK | 183 ✓ | direct ✓ |
| XO3 | order | - | rc-silence | rc-silence ✓ | :18,188 | 18 (trunc `...`) | 10 | OK | 188 ✓ | direct ✓ |
| XO5 | order | - | rc-mirror | rc-mirror ✓ | :116-117 | 116 | 11 | OK | 117 ✓ | direct ✓ |
| XO6 | order | - | rc-mirror | rc-mirror ✓ | :52-53 | 52 | 14 | OK | 53 ✓ | indirect ✓ |
| XO7 | order | - | rc-silence | rc-silence ✓ | :54-55 | 54 | 9 | OK | 55 ✓ | direct ✓ |

**12/14 rows fully OK; 2 rows carry a wrong line citation (X3, X7).** Every declared direction matches
`witness-run.txt`; every `old` is unique and sits exactly at the attributed line; the re-run reproduces
the frozen run byte-for-byte.

## 4. The two cite misses (both carried unchanged from round 40)

- **X3** cites `plans/anchor_digest_check.py:57-58`, but the quoted sentence sits at **:59-61**: line 59
  ends "…`test_outputs.py`. A", line 60 reads "provenance URL (an evidence markdown naming the same
  `<repo>/<subpath>`) is consulted when the", line 61 reads "`task.toml` route finds nothing, which
  covers captures that are not whole task directories." Lines 57-58 instead hold the S111/S108 example
  ("`configure-git-webserver/tests/test_outputs.py` binds" / "…tb2-git-webserver/test_outputs.py` and
  nothing else, while S108's") — **0 of the quote's 18 words** lie at the cite. The wording itself is
  verbatim in the tool; only the line range is wrong, two lines early. Origin: `F40XMutAnchor.md` §5
  cites the same sentence at "(:57-58)" — carried verbatim into the frozen table.
- **X7** cites `plans/anchor_digest_check.py:92-93`, but the quoted sentence spans **:91-92**: line 91
  ends "…a token that is no committed capture at all is", line 92 is "`digest-unknown`."; line 93 is
  blank. **10 of the quote's 11 words** (all but `digest-unknown`) lie outside the cited range. The
  wording is verbatim in the tool; the range is one line late at its start. Origin: `F40XMutAnchor.md`
  §5 cites "(:92-93)" identically — carried.

Materiality: the `adv` cell is display-only in the counter — `main()` prints it truncated
(`label[:90]`) and never parses it; the predicate consumes only id/tool/class/direction/adv_kind/old/new.
So neither miss can flip C1, but both are defects **inside a frozen artifact** (the counter may not
change this round): they must be carried as named limits, not fixed in place.

## 5. `adv_kind` — all 14 right (13 direct, 1 indirect)

Round-41 convention (`plans/round41_c1_verify.py:22-23`): "`direct` when a quoted sentence states the
behaviour, `indirect` when it follows from a quoted sentence plus the code, `none` when nothing
advertises it".

- X1/X3 (binding routes), X6/X7 (class names), X9 (row-malformed rule), X13 (default-ref rule),
  X14/X15 (erratum checks), XO1/XO3 (docstring FAIL clauses), XO5 (the scan window "up to and including
  `upto`"), XO7 (the regex matches "a probe receipt line (the probe's per-case verdict record)" — an
  `observed=timeout` line is still one, and the mutant stops matching it): each quoted sentence states
  the behaviour the mutant breaks → **direct**.
- X12: the sentence states exact matching against `name = "<org>/<task>"`; the mutant removes the
  slash-less fallback the reference still performs, i.e. it enforces the advertised exactness — the
  sentence states the behaviour → **direct**.
- XO6: the quoted comment states what the regex matches ("a gate output line, with or without the C2
  counter's `gate: ` echo prefix", `order_check.py:52`); that a `P10 PASS` line is *not* such a line
  follows from the sentence **plus the code** — the gate prints only `ok`/`DEFECT` verdicts
  (`pkg_gate.py:301` `print(f"{name} {'ok' if ok else 'DEFECT'} {note}")`), so it never prints PASS;
  the widened alternation matches a line the sentence never affirms or denies → **indirect**, exactly
  as the claims file states.

Recount from the frozen table (my verifier, and printed by both the frozen run and my re-run):
**`ADVERTISED direct=13 indirect=1 none=0`** — confirmed.

## 6. XO5/XO6 relabel rc-silence → rc-mirror: right

- The counter's definitions (`round42_c1_verify.py`, `exhibits()`): `rc-silence` = fixture
  `expect=reject`, reference rc 1 → mutant rc 0; `rc-mirror` = fixture `expect=accept`, reference rc 0 →
  mutant rc 1.
- Round-40 witnesses (receipts in `.ufo/waves/round-40/falsify/F40XMutLedgerOrder/`):
  `wit-xo5-xo5.diff` — reference `ORDER ok … ORDER RESULT PASS`, mutant `ORDER HIT
  …post-receipt-p10.txt… ORDER FAIL probe-executed-before-receipt … ORDER RESULT FAIL` (rc 0→1 on an
  order-holds input; the ledger itself calls the mutant "stricter"); `wit-xo6-xo6.diff` — reference
  PASS, mutant `ORDER HIT … 'P10 PASS receipt unreadable' … ORDER RESULT FAIL` (rc 0→1). Both are
  accept-shaped inputs where the mutant rejects → **rc-mirror**, not rc-silence.
- `control-c1-direction-mislabel.txt` (frozen): with the round-40 labels declared, both print
  `SURVIVED exhibits=0>1,rc-mirror` — the counter itself detects the rc-mirror direction and refuses
  the rc-silence claim; with `rc-mirror` declared (`witness-run.txt`) both are killed. The relabel is
  what makes the rows honest, and the round-40 witness text already recorded it
  (`F40XMutLedgerOrder.md` §2: XO5 "the mutant is *stricter*"; XO6 "invisible to the reference and a
  HIT to the mutant").

## 7. Residual risk and gaps

- Quote matching is normalized (backticks/`**` stripped, whitespace collapsed). I stripped nothing
  else; punctuation (em-dashes, `<…>`, quotes) matched exactly. Low false-positive risk: each found
  span coincides with the visibly intended sentence.
- I did not re-derive the mislabel control by re-running a direction-patched counter — that would
  require editing the frozen counter; the frozen control receipt, the two round-40 diffs and the
  counter's `exhibits()` code settle it.
- X7's `hits=3` is consistent with the three witness fixtures declaring `digest-unknown`
  (w-x7-unknown, w-x13-staged-index, w-x15-erratum-sibling) — read off the frozen FIXTURE lines.
- Out of my scope: battery42 modules (none exist at the freeze), the counter's sandbox/build machinery
  details, C2.

## 8. Receipts (paths relative to the lane root)

- `.ufo/waves/round-42/build/R42RevMutRows.md` — this report.
- `.ufo/waves/round-42/build/R42RevMutRows/witness-rerun.txt` — my re-run output (sha256
  `97e03ebbe5c89da770098e4fcd1d8c002046c9b65780e9d085767966aecdef13`).
- `.ufo/waves/round-42/build/R42RevMutRows/verify-out.txt` — static verifier output (sha256
  `3cfe97d69e1a794af8925c11f3e7d38181e0fe505fc1373f426bbac88bc2fdaa`).
- `.ufo/waves/round-42/build/R42RevMutRows/rerun.sh`, `verify_rows.py` — the two scripts (sha256
  `e001a99d…`, `c6a66efb…`).
- Scratch `/fast/scratch/hyaku/kengaku-r42/R42RevMutRows` removed after this report; no installs (none
  needed); nothing outside my report dir and scratch was written.

VERDICT: mutant-rows-ok-12/14-adv-misquoted-2
