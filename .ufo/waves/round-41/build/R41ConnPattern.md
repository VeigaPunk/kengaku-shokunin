# R41ConnPattern — cross-claim pattern finding (round 41 wave 1)

Seat: R41ConnPattern (connector, leaf). Claims read in full: `plans/round-41-claims.md`
(freeze 8ef8b4f). Instruments inspected (read-only, via `read`/`grep`; no counter/battery
run — none writes anything outside the report):
`plans/round41_c1_verify.py`, `plans/round41_c2_verify.py`, `plans/constraints_probe.py`,
`plans/pkg_gate.py`, `plans/order_check.py`, `plans/tip_receipts.py`,
`plans/sources_adopt.py`, `plans/round_close.py`.

Question: the TB2 `constraints-scheduling` grader's shapes are *first DTSTART wins*,
*case-sensitive SUMMARY/property tokens*, *folded-line refusal*, and *text-mode reads*
(claims §C2; `input-crlf-rewrite` passes 3/3 because integrity compares `read_text()`).
Do the lane's own instruments carry the same shapes — first-match-wins parsing, text-mode
digest, case-sensitive tokens? Yes: 15 sites, below. Each carries a one-line fixture that
exposes it. Sites are marked **silent** (verdict flips without a defect) or **fail-closed**
(a defect is raised — robustness, but the same shape-class).

## A. First-match-wins parsing (8 sites)

- **A1 — `plans/tip_receipts.py:144-147` (silent).** `usage_argv` scans the probe
  script's docstring lines and takes the **first** line starting `python3 `/`uv run `
  that contains the script basename; the real `Run as:` line later in the docstring is
  never seen. This is the TB2 first-DTSTART shape exactly.
  *Fixture:* add `python3 plans/x_probe.py --dry` as an example line above the script's
  real `Run as: python3 plans/x_probe.py --lane .`; the receipt re-run executes `--dry`,
  prints nothing, and the receipt flips `equal` → `differ` (or exit≠0).
- **A2 — `plans/tip_receipts.py:149` (silent).** `re.split(r"\s{2,}", s)[0]`
  truncates the command at the first run of 2+ spaces, assuming prose is padded with ≥2
  spaces. A `Run as:` line padded with exactly one space before the description swallows
  the prose into `shlex.split` argv → the probe runs with bogus args.
  *Fixture:* `Run as: python3 plans/x_probe.py --lane . (writes the receipt)` (one space)
  → argv gains `(writes`, `the`, `receipt)` → run fails → `differ`.
- **A3 — `plans/tip_receipts.py:174-180` (silent, cosmetic).** `provenance` records
  `script_hits[0]`/`receipt_hits[0]` — the first file:line where each name appears in
  the docs, not the naming claim.
  *Fixture:* mention the script basename once in `README.md`; the printed
  `doc=README.md:N+…` points at the wrong home.
- **A4 — `plans/round41_c2_verify.py:241` (silent).** V7 takes the **first**
  `## Requirement map` section (`re.search` to the next `##`). Any second same-named
  section in the entry is never parsed, so its rows cannot be checked and cannot trip
  the `missing`/`duplicated` tag tests.
  *Fixture:* append a second `## Requirement map` section labelling a frozen tag
  `unenforced` where the receipt derives `enforced` → V7 still passes.
- **A5 — `plans/pkg_gate.py:79,83-92` (silent).** P3/P4 parse only the **first**
  `## Located quotes` section; a second section's rows are never counted or verbatim-
  checked.
  *Fixture:* put a decoy `## Located quotes` table before the real one; the real quotes
  get no verbatim check (P4 skips them, P3 counts only the decoy).
- **A6 — `plans/pkg_gate.py:85` (silent).** `rows[1:]  # rows[0] is the header`
  assumes the first `|` row of the section is a header. A quote table **without** a
  header row silently drops its first data row from `self.quotes`.
  *Fixture:* a two-row quote table with no `|--|` header → the first quote is never
  verified and the quote count deflates.
- **A7 — `plans/pkg_gate.py:216` (silent).** P7's `re.match(r"^source:\s*(S\d{3,})\b.*?(https?://\S+)", line)` captures the **first** URL on each `source:`
  line (`.*?` is lazy). A second, trailing URL is invisible; `prov.get(sid) != [pinned]`
  still passes when the pinned URL comes first.
  *Fixture:* `source: S123 … https://raw/pinned https://other.invalid/x` → P7 OK
  although the row cites an unrelated document.
- **A8 — `plans/sources_adopt.py:43,101` (silent, population-regex).** `parse_rows`
  keeps only rows matching `ROW_RE` (0-3 leading spaces); any deeper-indented row
  (4+ spaces, or tab-indented) is silently invisible to every clause — collision,
  duplicate and defect checks all skip it. The selftest pins this boundary as a
  documented false-green (`four-space-not-a-row`, expected exit 0).
  *Fixture:* stage a row indented with 4 spaces carrying the same id as a registry row →
  no collision reported, exit 0.

## B. Text-mode digest / text-mode comparison (3 sites)

- **B1 — `plans/sources_adopt.py:284-286,325-329,404-412` (silent, deliberate).**
  `load_artifact` decodes artifact bytes to text and runs `normalize_text` (CRLF/CR →
  LF) on both sides before the quote substring search; `locates` compares normalized
  strings. A quote that differs from the capture only in line-ending style or in where
  the line break falls **locates**. This is the same universal-newlines shape as the
  TB2 `input-crlf-rewrite` claim (read_text vs bytes).
  *Fixture:* capture `...intro\r\nquote...` (CRLF) + quote cell `"intro\nquote"` (LF)
  → exit 0; a byte-substring comparator would refuse.
- **B2 — `plans/pkg_gate.py:106-107,148` (silent).** P4 reads captures via
  `read_text()` → `splitlines()` (universal newlines), rejoins with `"\n"`, and tests
  `q.text not in "\n".join(...)`. A quote spanning a line break passes against a CRLF
  capture.
  *Fixture:* capture line `alpha\r\nbeta`; quote `“alpha\nbeta”` → verbatim OK.
- **B3 — `plans/round41_c2_verify.py:214` (latent).** V5 compares probe dry-run stdout
  to the committed dry table as **text** (`r.stdout == …read_text()`), so CRLF/LF
  differences would compare equal. This is shadowed by the byte-digest pin of the dry
  table (line 210), so it is not currently exploitable — recorded as the same
  shape-class.
  *Fixture (illustrative only):* commit the dry table with CRLF and keep its digest
  un-pinned → V5 still sees byte-equal text; the digest check is what actually blocks it.

## C. Case-sensitive tokens (4 sites)

- **C1 — `plans/round41_c1_verify.py:362-378` (silent, classifier).** `classes()` maps
  tool stdout on exact-case tokens: `receipt`, `kind=`, `script=`, `origin=`,
  `skip reason=`, `equal|differ`, `control receipt=`, `verdict=`. A re-cased token is not
  misread — it is simply *not read*, so the defect class is lost and a silence-direction
  kill silently degrades (reference class absent → fixture `WRONG`, or a mutant survives).
  *Fixture:* have a reference run print `Receipt …` once → `observed_rc=0
  observed=-` vs declared defect → `FIXTURE … WRONG`.
- **C2 — `plans/tip_receipts.py:52,81-85` (silent, deliberate fold).** The inverse
  case shape: `CANDIDATE_RE` is `re.IGNORECASE` and `stem()` case-folds, so any
  `*probe*.txt|log` candidate in any case joins the receipt census (`FOO-PROBE.TXT`
  == `foo_probe.py`). Population-broadening by design.
  *Fixture:* commit `corpus/evidence/r/FOO-PROBE.TXT` → it is counted in
  `receipts=n` (skip/unmapped) instead of being inert.
- **C3 — `plans/round41_c2_verify.py:84-85,173,187-191` (fail-closed).** Exact-case
  token grammar: `SUMMARY` requires lowercase `observed_pass=`; `receipt_cases` anchors
  `^CASE … predicted=(pass|fail)`; V4 filters lines by literal `"CASE "`; `MAP_ROW`
  tag charset is `[a-z0-9-]+`. Every deviation raises a defect rather than silently
  passing — robust, but the same exact-token dependence.
  *Fixture:* a receipt summary line `observed_PASS=6` → no `SUMMARY` match → V4
  `summary line count != 1` defect.
- **C4 — `plans/sources_adopt.py:46-47,114,167` and `plans/pkg_gate.py:198-201`
  (fail-closed).** Statuses/tiers are exact-case set memberships (`status not in
  STATUSES`, `cells[7] != "mined"`, `cells[3] != rules["row_tier"]`), so a case
  variant is refused loudly, never silently accepted.
  *Fixture:* staged row status `Mined` → defect `status=Mined`.

## Second-order notes (surface trace)

- **C1 admission surface:** the battery contract's defect classes are the *exact*
  output tokens of the frozen tools; C1's `classes()` parser (C1) and the fixtures'
  declared `defects` must agree case-for-case. The first-match sites A1/A2 sit on the
  same critical path: `tip_receipts` re-runs receipts using the parsed `Run as:` argv,
  so a docstring tweak in any future probe script (this round's `constraints_probe.py`
  is itself a `*probe*` candidate) silently changes what the C1 fixture observes.
- **C2 admission surface:** A4/A5/A6/A7 sit inside V7/P3/P4/P7 — the gates that admit
  the S122/S123 entry. A second section or an extra source URL (A6/A7) is a
  false-green vector; B2 lets a CRLF capture pass verbatim, the same leniency the C2
  claim documents for the grader.
- **Order gate (V8/`order_check.py`) is clean of all three shapes:** all blob lines
  are scanned (no first-hit), comparisons are token-exact and fail closed.
- **No instrument unfolds RFC 5545 folded lines** — the grader's third shape has no
  instrument analogue (no continuation-line handling anywhere in the eight files).

VERDICT: pattern-15-sites
