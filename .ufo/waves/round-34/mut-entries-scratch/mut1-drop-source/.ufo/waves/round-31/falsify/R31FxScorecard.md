# R31FxScorecard — round-31 SCORECARD numbers vs committed bytes

Leaf reviewer. Target: verify the SCORECARD §Round 31 cells (SCORECARD.md:1045-1075) against
committed bytes. Verification ran at HEAD `97e69c7` (the L1 landed `d6aa66e` and `97e69c7` on top of
the referenced `dbb07364` during this assignment; every count below was re-derived from committed
blobs, and where a receipt differs between `dbb07364` and HEAD it is called out). No tools were
installed (no pacman transaction; scratch used was the existing python3/git). Scratch: /tmp/r31fx-scorecard (< 1 MB).

## 1. Count lines — re-derived from committed bytes

| Cell | Claim | Re-derivation | Verdict |
|---|---|---|---|
| Registry | 88 → 91 rows (S092, S093, S100) | `git show 0883e72:corpus/SOURCES.md \| grep -cE '^\s*\|[ \t]*S[0-9]{3,}[ \t]*\|'` → 88; same at `dbb07364`/HEAD → 91. Added-ids diff (`comm` on row ids): exactly S092, S093, S100; zero removed. | OK |
| Knowledge | 39 → 40 | `git ls-tree -r --name-only <c> -- corpus/knowledge \| grep -c '\.md$'` → 39 / 40; added file = `corpus/knowledge/benchmark-verifier-execution-model.md` only. | OK |
| Index | 40 → 40 | `git show <c>:corpus/README.md \| grep -cE '^\| `knowledge/.+\.md` \|'` → **39 at baseline, 40 at dbb07364/HEAD** (baseline readme has 39 rows; diff adds exactly one). **Cell does not re-derive: should be 39 → 40.** The frozen claims file itself says "39 index rows" baseline; lesson round-31.md §Census also says 39 → 40. | FELL |
| Census | exit 0; 15 W04 after, 14 before; 15th = S100↔S079 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → exit 0; W04 = 15 (S040,S048,S057,S058,S059,S064,S065,S066,S067,S068,S069,S071,S075,S076,S100); committed `census-before.txt` = 14 W04, `census-after.txt` = 15; S100 row and S079 row both cite `https://github.com/laude-institute/terminal-bench-2` (different scope cells). | OK |

## 2. The three counter lines (re-run from committed code)

All four commands were executed in the lane; outputs are byte-identical to the committed receipts.

- C1: `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census`
  → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0
  (matches committed `corpus/evidence/round31/adoption-after.txt`). Committed rows S092/S093/S100 each
  have 11 cells, `status=mined`, `opened=2026-10-25`, `used-by=corpus/knowledge/benchmark-verifier-execution-model.md`;
  entry has exactly three `source:` lines (S092/S093/S100) + `verified-at: 2026-10-25`; exactly one
  README index row. Control `claims/control-nothing.txt` (committed) shows `entries=0 … census=ok`,
  `exit=1`, `expect_sha256=a6a7631ce9ec5d932d6702e7090f5256e32806a37906012a05f8b66db424a5c8` =
  sha256 of the committed expect file. OK.
- C1 second receipt: `python3 plans/round31_c1_verify.py --lane .` → `checks=6 defects=0`, exit 0
  (matches committed `c1-verify-after.txt`); `--selftest` → `SELFTEST checks=6 failed=0`, exit 0. OK.
- C2: `python3 plans/round31_defects.py --lane .` → `checks=10 defects=0`, exit 0 (matches committed
  `defects-after.txt`). Before-state receipts all committed and show ten DEFECT lines + `checks=10
  defects=10` + `exit=1` (`claims/defects-before.txt`, `evidence/round31/defects-before-tightened.txt`,
  `defects-before-final.txt`). Individual repairs re-derived from blobs: R4 "reconciled truth" sentence
  2 → 1 occurrences; R5 `populated (not "unknown")` (emphasis-stripped) 2 → 1; R7 "tri-state" present
  at baseline, absent at HEAD while "Its values are not new" and "adds to the union table" are present;
  R8 baseline entry carries `CC0` (1), HEAD carries none (adjective dropped); R9 all five round-30 seat
  reports committed at HEAD with line counts ≥ baseline (e.g. R30DraftGate.md 199→243) and "Pass 9"
  present; R10 falsify registry `len(members)=33`. Append-only holds: `git diff --numstat 0883e72 HEAD
  -- LOG.md` = 26/0, `-- corpus/lessons/round-30.md` = 21/0. OK.
  - Note: lesson `corpus/lessons/round-31.md` §Mistakes describes post-tightening R6/R8 behavior that
    does not match committed counter bytes (committed R6 parses the counted form; committed R8 scans all
    cells). Stale prose only; the checks themselves pass and are substantive.
- C3: `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=17 failed=0`, exit 0 (matches
  committed `gate-selftest-after.txt`). From committed code, CLI reproduction (fixtures in
  /tmp/r31fx-scorecard/gate): url-map correct → exit 0 (bound=cap.txt->…), mismatch → exit 8,
  unmapped → exit 9, no map → exit 0, `--url-map` alone → exit 2 (`--url-map needs --quote-file and
  --artifact`). Neutered `bind_failure` (return `"",""`) reproduces `cases=17 failed=2` exit 1,
  byte-identical to `gate-binding-neutered.txt`. Baseline gate: `git show 0883e72:plans/sources_adopt.py`
  has zero `url-map` matches; baseline selftest runs `cases=14 failed=0`; baseline CLI with `--url-map`
  → argparse `unrecognized arguments` exit 2. OK.

## 3. Capability rows

- citation-bound adoption gate: `python3 plans/sources_adopt.py --selftest` (17 cases, exit 0) ✓;
  `--quote-file <rows> --artifact <capture> --url-map <map.json>` ✓ (exits 0/8/9 reproduced above).
- adoption second receipt: `python3 plans/round31_c1_verify.py --lane .` → `checks=6 defects=0` ✓;
  `--selftest` → checks=6 failed=0 ✓. Both capability rows re-derive.

## 4. The two corrections to earlier rows (SCORECARD.md:1077-1082)

- (a) Round-30 C3 row quote "does not bind the artifact to the cited URL" exists verbatim
  (SCORECARD.md:1024). Closed by `--url-map`: verified — a capture mapped to its own cited URL is
  accepted; mapped elsewhere refused (exit 8); unmapped refused (exit 9). Residual limits as stated in
  the C3 row match code behavior (membership against *a URL the row cites*, caller-authored map, no
  fetch provenance; the tally being reachable by vacuous `case(..., True)` lines is disclosed and the
  failure-capability receipt is load-bearing). Accurate.
- (b) Round-30 C1 row quote "S2's tri-state flag is the only surviving field delta" exists verbatim
  (SCORECARD.md:1022). The committed entry (`corpus/knowledge/contamination-transparency-card.md:72-75`)
  documents a four-valued vocabulary: `controlled` / `not_controlled` / `unknown` / `n/a`; "tri-state"
  appears nowhere in the entry; the surviving delta is the card-level *field*, not its vocabulary.
  Accurate.

## 5. Cells that do NOT re-derive

1. C1 cell "index 40 → 40" — committed bytes give 39 → 40 (baseline README 39 index rows; +1 added).
2. Round-shape cell "two v1 waves, 36 build + 32 falsify seats (68 total)" — committed registries hold
   36 build + 36 falsify = 72 members (`.ufo/waves/round-31/build/swarm-registry.json`,
   `.ufo/waves/round-31/falsify/swarm-registry.json`); LOG.md and lesson round-31.md both state 72.
   "32 falsify / 68 total" does not re-derive from any committed byte.
3. C3 cell citation "gate-cli-exits.txt: 0 / 8 / 9 / 2" — at `dbb07364` the committed receipt contained
   all four exits (including the exit-2 guard demo); at HEAD the receipt contains only 0/8/9 (the 2 was
   dropped when the file was rewritten in `d6aa66e`). The exit-2 behavior itself exists and was
   reproduced from committed code; this is a receipt drift, not a behavioral loss.

VERDICT: All three counter lines and the underlying counts (registry 88→91, knowledge 39→40, census
exit 0/15 W04 with S100↔S079 as the 15th) survived, and both corrections to earlier rows are accurate;
three SCORECARD cells do not re-derive from committed bytes — "index 40 → 40" (was 39 → 40),
"36 build + 32 falsify = 68" (registries say 36 + 36 = 72), and the "gate-cli-exits.txt: 0/8/9/2"
citation (HEAD receipt carries 0/8/9 only).
