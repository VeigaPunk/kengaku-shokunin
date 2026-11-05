# ReviewerC186 — independent derivation and replay attack on R86-C1

Verdict: **R86-C1 claim stands at the measured tip** (`defects=0`, `PREDICATE R86-C1 pass`,
exit 0); BASE reproduces the frozen red state exactly. Three findings, none fatal to the
frozen contract; F1 is an empirical demonstration that the honest-limit sentence in the
frozen claims overstates what L2+L3 exclude.

Reviewed at lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Note: master moved twice
during this review (`f357e4c1` → `981d6f19` → `ab9da0d4`); all instrument blobs re-verified
unchanged after the moves (see §3), and the tip run was measured at `master=ab9da0d4`.

## 1. Derivation from grader bytes alone (before reading table or probe)

Inputs: `corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py` only, plus the
eight case-shape names from the claims/seat. `plans/round86-cases.json` and
`plans/round86_raman_probe.py` were NOT read until `derived.txt` was written.
Full derivation: `derived.txt` (this directory). Summary:

| case | derived (E,G,2D) | frozen | agree |
|---|---|---|---|
| exact | PASS PASS PASS | P/P/P | yes |
| missing-2D-key | PASS PASS FAIL(KeyError) | P/P/E | yes |
| g-amplitude-string | PASS FAIL(TypeError) PASS | P/E/P | yes |
| extra-schema-keys | PASS PASS PASS | P/P/P | yes |
| absent-file | FAIL(Assert) FAIL(FNFE) FAIL(FNFE) | F/F/F | yes |
| g-key-renamed | PASS FAIL(KeyError) PASS | P/E/P | yes |
| 2D-null-value | PASS PASS FAIL(TypeError) | P/P/E | yes |
| g-amplitude-just-outside | PASS FAIL(band) PASS | P/F/P | yes |

The frozen vocabulary refines my two-level PASS/FAIL exactly as the bytes require:
`P` = returned without raising; `F` = AssertionError **or FileNotFoundError**
S~F~ (`absent-file`: legs 2–3 raise FileNotFoundError → F, not E); `E` = any other
exception (KeyError/TypeError → E). Semantics relied on (derived §2): extra JSON keys are
inert; `str/float` and `None[...]` raise TypeError; strict `<` makes 1.0501× amplitude fail;
tests are independent. My predicted collapse classes (P/P/P ×2, P/P/E ×2, P/E/P ×2,
F/F/F ×1, P/F/P ×1) match the frozen table.

## 2. Comparison with the live probe

`python3 plans/round86_raman_probe.py --lane . --work <scratch>` (run twice, before and
after the master moves): 8/8 `observed == predicted`, `cases=8 legs=24 mismatches=0`,
`PREDICATE R86-PROBE pass`, exit 0. The observation block of the fresh run is byte-identical
to the committed receipt's block:
`sha256(fresh) = sha256(receipt) = 55d50eab515cd83239ba0af4921129effb243cf3e7e7c935b466d84d03fdd39a`.
No disagreement at probe level.

## 3. Counter runs and instrument freeze

- **Tip**: `python3 plans/round86_c1_replay.py --lane . --rev master --work <scratch>` →
  `TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0` /
  `PREDICATE R86-C1 pass`, EXIT=0, measured `master=ab9da0d47ad9b2cce58438282a0606fd547b99b6`.
  `--rev master` measures a committed `git archive` extraction (`rev_tree`), so the dirty
  worktree files (SKILL.md, corpus/*.md — modified by other seats) cannot enter the measured
  tree; the kill rule's "measured committed revision" is honored even mid-flight.
- **BASE (official)**: `--rev 88651a72ef112ed9f5361e1c8c197babec691f96` →
  `DEFECT L1-receipt/L2-stamp/L3-tip/L4-table/L5-vectors/L6-reproduce/L7-ledger` (one line
  each; L8-subject the only green leg), `TARGET ... located=0 executed=0 defects=7`,
  `PREDICATE R86-C1 fail`, EXIT=1 — exactly the frozen BASE target.
- **BASE (my own scratch extraction)**, fixture mode (`--lane <extraction> --repo <lane>`,
  no `--rev`): identical 7-line defect pattern, EXIT=1. My extraction confirms at 88651a72:
  `plans/round86-cases.json` ABSENT, `plans/round86_c1_replay.py` ABSENT,
  `corpus/evidence/round86/raman-fitting-probe.txt` ABSENT,
  `plans/grader-population-ledger.json` present with raman row `status=unexecuted,
  reason=unattempted`.
- **Ledger delta verified by hand**: BASE row `{status: unexecuted, reason: unattempted}` →
  master row `{status: executed, round: 86, receipt: corpus/evidence/round86/raman-fitting-probe.txt,
  subject: tb2-header, verdict: cases, classes: [file-artifact, numeric-band,
  serialization-schema]}` — matches the claim sentence (claims:15-18) field for field.
- **Instrument freeze**: blob IDs of `plans/round86_c1_replay.py`, `plans/round86_c2_repin.py`,
  `plans/round86_raman_probe.py`, `plans/round86-cases.json` are identical at
  `316811fa`, at `f357e4c1`, and at current master `ab9da0d4`; `git status --porcelain` on
  those paths (and the round86 evidence dir) is empty. No instrument byte changed after the
  tip run — nothing voids the claims on this axis.
- Independently hashed: `SUBJECT_SHA 171fae77…` (capture), `CASE_TABLE_SHA f8aa21f3…`,
  `TOOL_SHA 09731b3e…` — all three match the receipt stamp and the counter's
  `TRUSTED_TOOL_SHA` (my own `sha256sum`, not the tool's self-report).

## 4. Predicate identity (item 4)

Frozen claims `plans/round-86-claims.md:24-26`:

```python
ok = (not defects and stats["members"] == 1 and stats["cases"] == 8
      and stats["legs"] == 24 and stats["mismatches"] == 0
      and stats["located"] == 1 and stats["executed"] == 1)
```

Counter `plans/round86_c1_replay.py:386-388` (`result_code`):

```python
ok = (not defects and stats["members"] == 1 and stats["cases"] == 8
      and stats["legs"] == 24 and stats["mismatches"] == 0
      and stats["located"] == 1 and stats["executed"] == 1)
```

**Byte-identical sentence.** The label: `plans/round86_c1_replay.py:399` prints
`PREDICATE R86-C1 {'pass' if code == 0 else 'fail'}` → at the tip it printed exactly
`PREDICATE R86-C1 pass`, the same label the claims' Target section (and therefore the round
report) carries. The probe's inner label `PREDICATE R86-PROBE pass` (`PRED_RE`, counter:60)
is the L5 input, also observed verbatim. Printed order (defects, then TARGET, then
PREDICATE) matches the claims' "TARGET … followed by PREDICATE R86-C1 pass".

## 5. Attacks

### L6 — whole observation block, not just the summary line

`plans/round86_c1_replay.py:366-367` (the comparison, quoted):

```python
        fresh_stamp, fresh_block, problem = parse_receipt(proc.stdout)
        if proc.returncode != 0 or problem or fresh_block != block:
```

`check()` reproduces the pinned tool from the measured tree (counter:358-361:
`[sys.executable, "-I", "-B", tree.root / TOOL, "--lane", tree.root, "--work", out]`) and
compares the **entire 12-line observation block** (8 CASE lines + `cases=8 legs=24
mismatches=0` + `PREDICATE R86-PROBE pass`) via `fresh_block != block`. It does NOT compare
the fresh run's **stamp**: `fresh_stamp` is parsed and then discarded. Consequences:

- Stronger than a summary-only compare (an edited CASE line, summary, or inner predicate is
  caught) — this is load-bearing (the `no-vectors-no-reproduce` mutant removes it).
- But the block contains **no revision-derived line**: the tip lives only in the stamp,
  which L6 never compares. I demonstrated block invariance across tips: the committed
  receipt was produced at `LANE_TIP bfda0472…` (receipt line 10), my fresh probe runat
  master `f357e4c1`→`ab9da0d4` produced the byte-identical block (sha `55d50eab…`).
  L6 therefore authenticates the observation *shape*, not the observation's *origin* —
  consistent with the claims' own honest-limit concession (claims:53-55).

### L3 — what receipt satisfies it without being minted at this tip

`plans/round86_c1_replay.py:318-324` (the whole L3 test, quoted):

```python
        declared = stamp.get("LANE_TIP") or ""
        anchor = (tree.tip if tree.tip != "fixture"
                  else git(repo(), "rev-parse", "master").stdout.decode().strip())
        resolvable = (re.fullmatch(r"[0-9a-f]{40}", declared) is not None
                      and git(repo(), "cat-file", "-e", f"{declared}^{{commit}}").returncode == 0)
        ancestor = resolvable and git(repo(), "merge-base", "--is-ancestor", declared,
                                      anchor).returncode == 0
```

Answer: **any receipt whose `LANE_TIP` names any resolvable ancestor of the measured
revision.** L2 pins digests (`SUBJECT_SHA`/`CASE_TABLE_SHA`/`TOOL_SHA`) but not the tip;
L5/L6 check only the (tip-free) block. So L3's ancestry test is the *only* tip binding, and
it accepts ancestors, not the measured tip. Two demonstrations:

1. The delivered receipt itself: `LANE_TIP bfda0472d5c163b2b5d2bbf22557f60a940de180`
   (ancestor, dated 2026-11-04 22:26:29 -0300) while master at measurement time was
   `ab9da0d4…`; `git merge-base --is-ancestor bfda0472… master` → yes; counter says pass.
2. **Empirical forgery**: I copied the measured tree into my scratch, changed ONLY the
   receipt's `LANE_TIP` line to the round-85 BASE `88651a72…` (a tree that never contained
   the receipt, the case table or the instruments), and ran the counter:
   `TARGET members=1 cases=8 legs=24 mismatches=0 located=1 executed=1 defects=0` /
   `PREDICATE R86-C1 pass`, EXIT=0. Full target reached by a receipt declaring a tip from
   the previous round.

This does not violate the frozen leg list — the claims define L3 as "resolves and is an
ancestor of the measured revision" and the code implements exactly that — but it falsifies
the strength implied by claims:55.

## Findings (3)

- **F1 (moderate — frozen prose overstates the receipt authentication).**
  `plans/round-86-claims.md:55`: "`L2` and `L3` are what a receipt copied in from elsewhere
  cannot satisfy." L3 as implemented (counter:318-324) accepts ANY resolvable ancestor tip,
  and no other leg binds the receipt to the revision it was minted at (L6 compares the
  tip-free block, counter:366-367, and discards the fresh stamp). Demonstrated: a
  BASE-tipped receipt reaches the full target in my scratch fixture. L3 does exclude
  cross-repo copies (unresolvable tips) and non-ancestor/future tips — that is all it
  excludes. The claim's target and legs are met as frozen; the round report should carry the
  honest limit in this narrower form ("L3 excludes receipts whose declared tip does not
  resolve in this repo's history or is not an ancestor — not receipts minted at an earlier
  ancestor of the same repo"). No edit made (frozen file).
- **F2 (minor — the `members=1` stat is hardcoded, not counted).**
  `plans/round86_c1_replay.py:209`: `stats = {"members": 1, "cases": 0, ...}` — `members`
  is never recomputed from the ledger, so the predicate leg `stats["members"] == 1`
  (counter:386) is vacuously true and the "grows by exactly one member" clause
  (claims:15-16) is not machine-verified against the population (e.g. no count of
  `status=executed` rows or diff vs the BASE ledger). L7 does verify *this* row's fields, so
  the delivered verdict stands; the counter merely cannot detect a second member flipping to
  `executed`. Suggest a future instrument revision counts the ledger population.
- **F3 (trivial — frozen case-table `why` names the wrong failing line).**
  `plans/round86-cases.json:68` (`2D-null-value`): "a present key carries null;
  `abs(1 - None/2670.08)` raises TypeError". With `data["2D"] = null`, the first failure is
  `G_peak["x0"]` (TypeError: 'NoneType' object is not subscriptable) in
  `test_outputs.py:46`, before any arithmetic — the cited expression is never evaluated.
  Predicted vector `P/P/E` is unaffected (observed confirms); prose only. Frozen file, not
  edited; flagging for the record.

## Residual risk and verification gaps

- Controls (`--control-*`), mutants and selftest were NOT re-run by this seat (not in my
  item list); their pre-data state is committed at `.ufo/waves/round-86/L1/freeze-battery.txt`
  and `base-runs.txt` and the instrument bytes are unchanged since, so those committed
  results remain valid for the current tip run I performed.
- The upstream byte-comparison behind S274 (pinned `2fd12b88` fetch) was not re-verified —
  my item names no network fetch; I used zero network. The capture's SHA-256 matches the
  frozen `SUBJECT_SHA` everywhere it is pinned.
- `bfda0472` being an ancestor of master resolves the "inherited unlanded work" tension for
  L3, but the provenance of how those earlier-attempt commits entered master's history was
  not audited by this seat (out of scope).
- Scratch (`/fast/scratch/hyaku/kengaku-r86/ReviewerC186/`) is deleted before yield; raw
  outputs quoted above were copied into this directory first. No production file was
  written; no network used; no mutating git command anywhere.
