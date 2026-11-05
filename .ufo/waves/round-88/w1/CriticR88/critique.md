# CriticR88 — adversarial review of the frozen round-88 claims (read-only)

Scope: `plans/round-88-claims.md` (frozen at 0220c2f9), `plans/round88_c1_replay.py`, `plans/round88_claim_figures.py`,
`corpus/lessons/round-88.md`, `corpus/QUALITY.md` Q66. Measured tip 7fcc680b. Transcript and fixture recipes:
`evidence.txt` in this directory. Nothing in the frozen set was edited; defects are reported, not repaired.

## Bottom line

- The measured numbers reproduce at the tip. C1: BASE `defects=3` / exit 1; tip `executed_rows=32 ... defects=0` / pass.
  C2: `records=56 checked=56 matched=55 mismatches=1 prose=0`, one `MISMATCH KNOWN R87-C1 kv:defects claimed==7 measured 3`,
  `PREDICATE R88-C2 pass`; selftest passes. The two claims are separable (section 3).
- Both predicates can be satisfied without the work they name. C1 passes with a probe that never runs the grader (F1).
  C2 passes with a false before-figure added (F3, F4) and with before-figures removed (F5). Its kill rule is not enforced (F6).
- The C1 coverage move is a count move on a keyword label, not a new surface (F2).
- Recommendation: report C1 as a count move, not a frontier move. Do not cite the R88-C2 green as proof that the
  Q66 before-figures are measured (F10) until F3–F6 are fixed in a later round.

## Findings

Severity: BLOCKER = the claim as frozen is unmet at the tip; MAJOR = a predicate or control can pass with the failure it names;
MINOR = wording, dead code or a small unchecked figure; FINDING = a gap or inconsistency that does not change a verdict.

### F1 — MAJOR — R88-C1 passes with a probe that never runs the grader (do-nothing control missing)
- Evidence: fixture commit `1173ac8d` (on top of 7fcc680b) replaces the sandbox call in `plans/round88_fixgit_probe.py`
  `payload = run_case(staged, work, case["result"])` with an echo of `case["predicted"]`, and rewrites the `TOOL_SHA` line of
  the receipt to the new probe sha. `python3 plans/round88_c1_replay.py --rev 1173ac8d` -> `TARGET executed_rows=32 member=fix-git
  located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R88-C1 pass`, rc 0.
- Why it passes: the counter pins SUBJECT_SHA (L8) and the table (L4), but never pins the probe bytes to the frozen
  `50ae36d6…` (`round88_c1_replay.py` L2 compares TOOL_SHA to the measured tree, not to a constant). L6 re-runs the probe, so
  it reproduces an echo. The predicate as frozen ("the probe re-run from the measured tree reproduces the receipt observation
  block") is satisfied by the echo.
- Controls: the L1 controls (`.ufo/waves/round-88/L1/controls.txt`) are ledger-only and forged-LANE_TIP only. No probe control.
- The honest limit (claims lines 39–41) covers authorship of the receipt, not execution of the grader.
- Falsifier: if `round88_fixgit_probe.py`'s SHA were pinned in a frozen element I did not find (grep of
  `plans/round88_c1_replay.py` shows only `SUBJECT_SHA` and `TOOL` path), or if L6's re-run were compared to predicted vectors
  independently of the echo, the fixture would fail. Neither holds.
- Impact on the measured tip: none (the committed probe is the real one; L6 at tip ran real bwrap runs). It is a control gap.

### F2 — MAJOR — R88-C1 coverage move is a count move on a keyword label, not a frontier move
- The ledger count moves 31→32 executed, `crypto-credential` 2→3 of 12, `file-artifact` 23→24 of 76 (verified from the ledger
  at BASE and tip).
- `crypto-credential` is assigned by regex, `plans/round62_c1_class_survey.py:92`:
  `\bhashlib\b|\bsha1\b|\bsha256\b|\bmd5\b|\bopenssl\b|\bgpg\b|\bhmac\b`. fix-git matches on `import hashlib` and
  `hashlib.md5(file.read().strip())`. No key, certificate, credential artefact or openssl call is staged or exercised.
- The class description in SKILL.md ("credential and certificate artefacts are staged... openssl calls") does not describe fix-git.
- Overlap with executed members: `constraints-scheduling` (executed round 41) already hashes an app file with
  `hashlib.sha256(app_text.encode())` (tip grader line 95, class crypto-credential). `mteb-retrieve-probe.txt` (round 87)
  already has `CASE result-is-directory predicted=P/E observed=P/E`, the same directory-at-path edge as fix-git's `layout-old-is-dir`.
- What is new: the md5 pair predicate with the `strip()` normalisation (exercised by `trailing-whitespace-tolerance`), and the
  FileNotFoundError leg. I did not verify that strip() normalisation is absent from every other executed grader.
- Verdict on the question asked: the count moves; the frontier (credential or certificate surface) does not. The claim's
  framing "first crypto-credential movement" is accurate about the ledger and overstated about coverage.
- Falsifier: if the frontier is defined by ledger class counts (the ledger's own definition), this is a count move as
  claimed. If a reviewer defines it by surface, my reading holds. If another executed grader stages a key or certificate,
  it is not new either way.

### F3 — MAJOR — R88-C2: the extraction gate drops a false before-figure silently (weakest point)
- Weakest point: `CONVO_RE` (case-sensitive token list, `round88_claim_figures.py:128–130`) plus the FAIL gate. A before-span
  without a listed token (`TARGET`, `DEFECTS`, `PREDICATE`, `located=`, `executed=`, ...) is discarded with no record and no
  prose count. `prose=0` therefore cannot see it.
- Evasion (fixture `a9d2468d`): add to R86-C1 the line `- Before (BASE \`88651a72\`): \`defects=9\`, exit 1.` (false: BASE
  measures `defects=7`). Output is byte-identical to the tip run: `records=56 checked=56 matched=55 mismatches=1 prose=0`,
  `PREDICATE R88-C2 pass`. (`diff out-E1.txt c2-tip.out` empty.)
- The predicate says "every extracted before-figure record is checked". For a dropped span, nothing is extracted, so the
  predicate is vacuously satisfied.
- Real drops in the frozen corpus (not fixtures): R83-C2 "before eight unregistered ids plus missing index, fail" (no
  token; R83-C2 contributes zero records); R81-C1 "`RECEIPT-UNTRACKED` ×2" (count-after-code form matches neither CODE_RE nor
  CODE2_RE); R82-C3 "Before (BASE_REV): the gate, the map and the receipt are absent" (gated out; prose-mode).
- Falsifier: if the claim text were required to contain a counter token, the drop would be a defect of the claim, not the
  instrument. The claim text (lines 48–50) says only counter-output vocabulary yields records, which discloses the gate, but
  the predicate does not.

### F4 — MAJOR — R88-C2: the F5 set-equality is per (claim, key), not per record
- Evidence: `round88_claim_figures.py:463–466` builds `measured_pairs = {(cid, key) ...}` and `known_pairs = {(c, f"kv:{k}") ...}`.
  A second wrong figure on the same pair is classified KNOWN.
- Evasion (fixture `66f41fa3`): add to R87-C1 `- **Before (BASE \`b9be6877\`, restated):** \`TARGET defects=9\`, ...`.
  Output: two lines `MISMATCH KNOWN R87-C1 kv:defects claimed==7` and `... claimed==9 ... measured 3`,
  `RECORDS ... mismatches=2`, `DEFECTS n=0`, `PREDICATE R88-C2 pass`.
- Predicate says "the set of mismatched records equals the frozen KNOWN set exactly". It does not; the counter says pass.
- The value check (F5-known-value) only checks that the measured number is 3, so it cannot catch a second claimed figure.
- Falsifier: the instrument's own `mismatches=2` line contradicts the predicate's "exactly one" reading; that is the falsifier
  the reader can check with `grep MISMATCH`.

### F5 — MAJOR — R88-C2: the record set is not pinned; removing matched evidence passes ("narrowing after landing")
- Evidence (fixture `1f76c074`): delete `\`defects=3\`, \`state_mismatches=1\`,` from the R86-C2 before-figure. Output:
  `records=54 checked=54 matched=53 mismatches=1 prose=1`, `DEFECTS n=0`, `PREDICATE R88-C2 pass`.
- The `RECORDS` count (56) is correct at tip (I reproduced 56 exactly) but nothing pins it. `prose` is printed and never
  enters the predicate, so a before-figure converted to prose passes.
- Against the sizing rule as briefed (no narrowing after landing): a deletion that reduces checked records is a narrowing, and
  the instrument reports it as green.
- Falsifier: a frozen expected record count or a per-claim record hash in the counter would catch E6. None exists (grep of
  the counter: no hash or count constant).

### F6 — MAJOR — R88-C2: the kill rule ("any edit to a frozen claims file, counter or this instrument ... makes the claim unmet") is not enforced
- No SHA pins exist in `round88_claim_figures.py` (grep `sha` returns nothing). Claims 80–87 are read from the measured rev.
  Child counters run from the working tree (`cmd = [sys.executable, str(lane / counter)]`, line 270), not from the measured rev
  or from commit A.
- E1, E2, E5 and E6 are all edits to frozen claims files (round-86 and round-87) and all but E5 pass.
- At the tip the claims files and counters are byte-identical to 801b903a / 1f267d4b (verified: `git diff` empty). So the
  measured tip is clean; the instrument just cannot tell if that stops being true.

### F7 — MINOR — Real before-figures are unchecked, and the prose path contradicts the docstring
- The docstring (`round88_claim_figures.py:17–18`) says a before-span with no machine-checkable figure is "reported, never
  silently dropped". R82-C3's before-span is dropped by the gate (no token, no FAIL in window) and `prose=0` is printed.
- The three dropped figures are listed in F3 (R83-C2, R81-C1, R82-C3).
- Falsifier: if the gate were documented as the definition of a before-span, the docstring would be wrong, not the claim.

### F8 — FINDING — F6-norecords only fires for claims with zero extracted records
- `round88_claim_figures.py:445–449`: `if not recs:` is the only place the counter's own BEFORE-state (exit 1 / PREDICATE fail)
  is checked. A claim with records is never checked for before-state failure, so "exit 1" and "PREDICATE R… fail" in the claim
  are not compared to BASE output. Only numbers are compared.
- Falsifier: a counter that passes at BASE with the claimed numbers would be the failing case; I did not construct one (the
  numbers would then appear as UNEXPECTED if they differ).

### F9 — FINDING — The instrument does not scan this round's claims file
- `CLAIMS_FILES = [f"plans/round-{n}-claims.md" for n in range(80, 88)]` (line 114). `plans/round-88-claims.md` is not in scope, so
  R88-C1's own before-figures (`executed_rows=31`, `defects=3`, `crypto 2 of 12`) are not checked by the Q66 check.
- Falsifier: the frozen table was written against rounds 80–87 by design ("the eight claims files this instrument was written
  against"); this is a scope note, not a bug, but Q66's text ("every claim") reads wider.

### F10 — FINDING — QUALITY.md Q66 overclaims the instrument
- Q66 (`corpus/QUALITY.md` lines 1355–1363): "A claim's before-figure is now evidence only while this counter stays green."
  E1 (false figure) and E6 (figure removed) are green. Q66's executable half does not guarantee the statement.
- Falsifier: the statement is true only if "evidence" means "figure re-derived at BASE for the numbers the extractor sees".

### F11 — FINDING — Selftest battery does not exercise the holes the predicate depends on
- `--selftest` T1 tests one doctored figure in one known location (R87-C1 `defects=7`→`9`). T2–T4 pin marker negatives, the
  backward direction and dedupe. None tests F5 pair-scoping, the CONVO gate for lowercase keys, or record-count pinning.
- Falsifier: a T5 that doctors a second same-pair figure (as E2 does) would have to observe `verdict=mismatch` to catch F4. On the current instrument it observes PASS, so the battery cannot detect F4. The falsifier is the E2 transcript in `evidence.txt`.

### F12 — FINDING — R88-C1 states four count moves against a one-count-per-claim sizing rule
- The claim reports `executed_rows 31→32`, `crypto-credential 2→3 of 12`, `file-artifact 23→24 of 76` and `defects 3→0`.
  Under the sizing rule as briefed ("one count per claim"), this is four. The first is the one count; the rest are its
  consequences and are derivable from it.
- Falsifier: if the sizing rule counts consequences separately, this is not a defect.

### F13 — MINOR — R88-C1 counter: `legs` is arithmetic, not a measurement; `LEGS` is dead
- `legs = 2 * cases` (`round88_c1_replay.py:259`). The `LEGS` tuple (line 59) is defined and never used. "legs" means case-legs
  in the TARGET line and L1–L8 in the predicate; the claim uses both (claims lines 14–18, 23).
- Falsifier: none needed; this is a naming and dead-code point.

### F14 — MINOR — "first crypto-credential movement since round 41/80" is ambiguous
- Ledger history: constraints-scheduling executed at round 41 (commit 5d684313 is the round-79 freeze, receipt round41);
  openssl-selfsigned-cert executed at round 80 (commit 6669fe72). The most recent prior movement was round 80, not 41.
  The claim text (lines 18–19) says "no recent round has moved crypto-credential" and the lesson (line 11) says "since round 41/80".
- Falsifier: if "41/80" is read as "the last two movements", the phrase is accurate; a reader will not read it that way.

### F15 — MINOR — The file-artifact figure hides a SKILL.md change this round did not disclose
- SKILL.md at BASE said "executed 22 of 76"; the ledger at BASE counts 23. The tip SKILL cell says "24 of 76". The claim's
  "23 → 24" follows the ledger. SKILL.md moved 22→24 in this round, which includes round 87's `mteb-retrieve` that SKILL.md
  had not recorded.
- Falsifier: if SKILL.md is not a before-figure source, the point is cosmetic.

## Answers to the four questions

1. Can C2 pass while missing a real new mispredict? Yes. Weakest point: the CONVO_RE gate plus the per-pair F5 comparison.
   Constructions: E1 (silent drop, output byte-identical to tip; F3) and E2 (second wrong figure on the KNOWN pair; F4).
   The F6-norecords leg does not help: it only fires for zero-record claims, and R83-C2 has zero records but its counter
   fails at BASE, so F6 is silent by design.
2. Is a sixth member replay a real coverage move? The count moves and the arithmetic reproduces. The frontier moves by a
   keyword label (F2). The ledger history confirms the last crypto-credential movement was round 80 (F14).
3. Separability. Both directions hold: removing every R88-C1 file from the tip worktree leaves C2's output identical
   (`records=56 ... PREDICATE R88-C2 pass`), and removing `round88_claim_figures.py` leaves C1 passing
   (`PREDICATE R88-C1 pass`). C2 does not scan round-88 claims (F9). Caveat: C2's child counters are read from the worktree
   (F6).
4. Frozen-text imprecision besides R87-C1: (a) claims lines 60–61 "mismatch set equals the frozen KNOWN set exactly" vs
   F5 pair-scope (F4); (b) claims lines 66–67 kill rule not enforced (F6); (c) claims lines 58–61 "every extracted record is
   checked" vs the gate (F3); (d) claims lines 26–29 predicate, which the fix-git fake probe satisfies (F1); (e) claims lines 39–41
   honest limit covers receipts, not the probe (F1); (f) claims line 23 "legs=16" is 2×cases (F13); (g) claims lines 18–19 and
   lesson line 11 "since round 41/80" (F14); (h) "56 records" is correct at tip but not pinned (F5). The "section 9 sizing rules"
   are not present in repo files at tip or HEAD (grep); I evaluated against the three criteria in the seat brief.

## What would falsify this critique as a whole

- If the frozen predicates were meant as a lower bound on the claim (nothing narrower than the named checks), F4–F5 become
  non-defects. The claim text does not say so.
- If the probe bytes were frozen by an element outside the repo (none found), F1 would be a control gap in the instrument only.
- If the counter's bytes at the tip are the only ones ever used (CI runs at tip only), F6's practical risk drops; the kill
  rule as written still says otherwise.

SEAT CriticR88 VERDICT FINDINGS findings=15
