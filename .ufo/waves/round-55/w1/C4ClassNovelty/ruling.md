# C4ClassNovelty — ruling: is full-multiset equality a graded-artefact class new to this lane?

Seat: C4ClassNovelty (kengaku round 55, wave 1, attack/critic).
Question assigned: is order-insensitive full-multiset equality over whitespace-split tokens
REALLY a graded-artefact class new to this lane (the R55-C3 entry's claim), or a re-label of
r45's password-recovery membership?
Base: `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (round-55 freeze; claims at
`plans/round-55-claims.md`, commit `80afa613`).
Method: read the four named knowledge entries; verified the chess-best-move capture's bytes and
sha256 (`a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` — matches the frozen
pin in the claims file); ran a 13-shape semantics demonstration in host python3 (inline heredoc,
no files written); swept `corpus/evidence/**/test_outputs.py` for `sorted(`/`Counter(` equality
decisions. No clone needed; no scratch dir created; nothing installed.

## The r55 rule under test (verified against the capture)

`corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` (25 lines, sha256 as
pinned), the whole score:

```python
move_file = Path("/app/move.txt")
move = move_file.read_text().strip().split()
assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"
```

`sorted(a) == sorted(b)` is exactly full-multiset (Counter) equality: same elements, same
multiplicities, any order. `split()` with no argument splits on any whitespace run
(space/tab/newline), after `read_text()`'s universal-newline translation and one `.strip()`.

## Per-entry axis table

Axes chosen to expose where sorted-multiset equality could be a re-label: partial credit, order,
duplicates/extras, normalization, split granularity. Quotes are byte-exact from the entries/captures.

| Grader (round) | Decision rule (quote) | Partial credit | Order | Duplicates / extras | Normalization | Split granularity |
|---|---|---|---|---|---|---|
| password-recovery (r45) | `guesses = Path("/app/recovered_passwords.txt").read_text().strip().split("\n")` then `assert "8XDP5Q2RT9ZK7VB3BV4WW54" in guesses` (`test_outputs.py:14,18`) | None, but **extras free**: `decoys-1000` (answer + 1000 wrong lines, shuffled) observed **pass** | **Free** — `decoys-1000` is explicitly "shuffled" and passes | **Tolerated** — membership is set-like; a duplicated answer line cannot fail; 1000 decoys cannot fail | Universal newlines (`\r\n` and lone `\r` → `\n`), then `.strip()`, case-sensitive (`lower23` fails) | **Newline** — `constant-joined` (answer + decoys on ONE line) observed **fail** |
| regex-log (r36) | `assert matches == expected_dates` (`test_outputs.py:90`) — full-list equality, "count, order and type all matter" | None — "A partial compliance (23 of 24 style) is indistinguishable from producing nothing" | **Enforced** — list equality on `re.findall` output in order | **Exact multiplicity** — list equality | Input pattern `.strip()`ed (`:25`); match output compared raw | n/a (regex compiled and run, not split) |
| polyglot-c-py (r46) | `assert polyglot_files == ["main.py.c"]` (`test_outputs.py:18`) + `assert python_out == expected and c_out == expected` (`:44`) | None | **Enforced** for the listing (trivially — one element; "any two-element listing fails regardless of order"); per-runtime literal compare | **Exact** — `extra-file` and `leftover-cmain` observed **fail** | `stdout.strip()` at both ends (`:36`,`:43`); CRLF source accepted; case n/a | n/a (directory listing + subprocess stdout) |
| protein-assembly (r35) | `assert flag_idx < donor_idx < dhfr_idx < acceptor_idx < snap_idx` (`test_outputs.py:42`) + per-gap linker checks | None | **Enforced positionally** — first-occurrence `str.find` indices must ascend | Repeats fail incidentally (`donor-repeated` fails the length cap); extras fail | `.lower()` per line, per-line `.rstrip()`, exactly one line (`:16,19,21`) | Single line required |
| db-wal-recovery (r40) (nearest neighbour found by sweep) | `assert ids == sorted(ids)` (`test_outputs.py:44`); `assert len(ids) == len(set(ids))` (`:89`); `len(data) == 11` (`:53`) | None — "one bit, no partial credit" | **Enforced** — the export must arrive sorted ascending | **Exact** — "the one place the id multiset is checked exactly" (`truth-plus-duplicate-id11` fails) | JSON typed parse; `1.0` fails the `int` gate; extra keys free | n/a (JSON records) |
| **chess-best-move (r55 candidate)** | `move = move_file.read_text().strip().split()` then `assert sorted(move) == sorted(["g2g4", "e2e4"])` | **None — partial answers fail** (one token only → fail, demonstrated) | **FREE** (`reordered` → pass, demonstrated) | **Exact multiplicity — extras AND duplicates fail** (`both-plus-decoy` → fail, `duplicated-correct` → fail, demonstrated) | `.strip()` + universal newlines + any-whitespace split; **case-sensitive** (`G2G4` → fail, demonstrated); raw string compare, no digit-width coercion | **Any whitespace** — `one-per-line` (`g2g4\ne2e4`) and single-line (`g2g4 e2e4`) both pass |

## The decisive discriminator vs r45 (the re-label hypothesis)

The two rules genuinely cross — neither subsumes the other — and they disagree on real content:

1. **Extras/multiplicity (the strong counterexample to "re-label").** Content `g2g4 e2e4 h7h5`
   (both required tokens + one decoy): r45-style membership semantics → **PASS**; r55 sorted
   multiset → **FAIL** (demonstrated). Content `g2g4 e2e4 g2g4` (extra duplicate): membership →
   **PASS**; multiset → **FAIL**. r45's own receipt records the analogue passing:
   `decoys-1000` — "the answer plus 1000 wrong guesses, shuffled" — observed **pass**, with the
   entry's finding "a thousand decoys pass because the check is membership, not exactness or
   count". Under r55's rule that state fails. A grader class that flips r45's `decoys-1000`
   verdict from pass to fail is not a re-label of r45.
2. **Granularity.** r45 splits on `\n` only (`constant-joined` fails: "the answer concatenated
   with two decoys on ONE line"); r55 splits on any whitespace — `g2g4 e2e4` on one line passes.
   The converse also holds: a file whose only line is `g2g4 e2e4` passes r55 and would fail
   newline-membership of both tokens.
3. **Shared axis (honest concession).** Both are order-free and both normalize newlines before
   comparing. Order-freeness alone is therefore NOT new to the lane (r45 had it), and exact
   multiplicity alone is NOT new (r36 list equality, r46 listing equality, r40 uniqueness+count).
   What has not been executed before is the **combination**: order-free **and** multiplicity-exact
   **and** exact-count **and** any-whitespace-token split over a bare agent-written token file.
   The sweep of all captured `test_outputs.py` files confirms no prior grader decides by
   `sorted(…) == sorted(…)` or `Counter(…) == Counter(…)`; the only other `sorted(` equality in
   the corpus is db-wal-recovery's `ids == sorted(ids)`, which *enforces* ascending order rather
   than ignoring it, and grades a structured JSON export, not a token file. (schemelike and
   sparql-university `sorted(` hits are harness-side file listing / display joins, not graded-artefact
   equality.)

## Word-precision check of the claim's sub-claims (all verified true)

- "order-insensitive full-multiset equality over whitespace-split tokens" — byte-accurate
  description of the captured assert.
- "r45's password-recovery was line-split membership" — accurate (`split("\n")` + `in`).
- "partial answers fail" — verified (one-token-only → fail).
- "order is free" — verified (reordered → pass).
- "no normalization of case or digit width exists" — verified for case (`G2G4` → fail) and
  trivially for digit width (raw string equality, no coercion). One wording caution: unqualified
  "no normalization" would be false — `.strip()` and any-whitespace tokenization ARE
  normalization. The claim's qualified phrasing is correct and must stay qualified in the entry.

## Final ruling

**NOVEL — not a re-label.** Sorted-multiset equality over whitespace-split tokens differs from
every prior executed class on at least one axis each prior class treats differently: from r45
membership on multiplicity/extras (extras and duplicates fail vs tolerated) and split granularity
(any-whitespace vs newline); from r36/r46/r40 exact-equality classes on order (free vs enforced);
from r35 on being an equality at all (r35 is positional chain comparison). The R55-C3 class claim
stands.

**Cap on the claim (must ride with the entry, not be buried):** the novelty is *combinatorial*,
not per-axis. No single axis — order-freeness, exact count, multiplicity-sensitivity,
case-sensitivity — is new to the lane; each individually appears in r36/r40/r45/r46. The entry
must phrase the class as "order-free AND multiplicity-exact AND whitespace-token over a bare
token file", and must keep "no normalization" qualified to case/digit-width. If the entry claims
any single axis as new, that claim is falsifiable from r36/r40 receipts and should be rejected.

Smallest safe correction: none needed for admission; one wording guard for the entry author as
stated above.

## Evidence log

- `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` sha256
  `a540714e…8f286` = frozen pin; lines 22–25 read in full.
- Semantics demonstration (host python3, inline heredoc, 13 content shapes; exit 0):
  exact-both-tokens True; reordered True; one-token-only False; both-plus-decoy False;
  duplicated-correct False; one-per-line True; case-variant False; padded-ws True; and the r45
  rule on its own shapes: answer-alone True; answer+1000-decoys True; answer-duplicated True;
  joined-line False; crlf-line True.
- `grep -rn "sorted(\|Counter(" corpus/evidence --include=test_outputs.py`: only
  chess-best-move decides by sorted-equality; db-wal-recovery uses `ids == sorted(ids)`
  (order-enforcing) + `len(ids) == len(set(ids))`; schemelike/sparql uses are harness-side.
- Knowledge entries read in full: `tb2-password-recovery-grader.md` (r45),
  `tb2-regex-log-grader.md` (r36), `tb2-polyglot-c-py-grader.md` (r46),
  `tb2-protein-assembly-grader.md` (r35); `tb2-db-wal-recovery-grader.md` (r40) read for the
  nearest-neighbour check.
