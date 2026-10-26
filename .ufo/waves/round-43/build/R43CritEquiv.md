# R43CritEquiv — equivalents, incidental kills, and the denominator (round 43 wave 1, C1 calibration)

Seat: R43CritEquiv (critic, leaf). Lane `kengaku-shokunin` clone at `d33350fdb01ce27cbff47b04642fd2c1471e5c26`; frozen
tools pinned (`PINS total=2 mismatched=0` in every run below): `plans/anchor_digest_check.py`
`11bb2cad87be1c29…`, `plans/order_check.py` `948d5e1d2b3429d7…`. Read in full before judging: `plans/round-43-claims.md`,
`plans/round43_c1_verify.py` (MUTANTS 9, docstring), `plans/round42_c1_verify.py` (MUTANTS 14), `plans/round40_c1_verify.py`
(MUTANTS 21), `plans/anchor_digest_check.py`, `plans/order_check.py`, `.ufo/waves/round-43/claims/witness-run.txt`,
`.ufo/waves/round-43/claims/witness/w_near.py` (read for reachability only; not imported/copied),
`.ufo/waves/round-42/build/R42CritEquiv.md`.

Envelope (Q32): every run below ran under `claims/envelope.sh "$S/env" <cmd>`; in every run
`local_bin_content_before=after=328be01808ba022f unchanged` and the envelope exited 0. Envelope lines are pasted
verbatim in each receipt (`run-crit-battery3.txt`, `probe-muts.txt`, `probe-rest.txt`; sha256 in `COMMANDS.txt`).
Scratch `S=/fast/scratch/hyaku/kengaku-r43/R43CritEquiv`; no git mutation in the lane, no commit anywhere; fixture
repos are `git init` from nothing in scratch.

---

## 1. Equivalents: none of the 9 (`e = 0`)

Test applied to each frozen row: is there an input on which the mutant differs from the reference, **in the declared
direction, because of the span the `adv` cell quotes**? A mutant is an "equivalent" only if no such input exists. For
each row I re-derived a from-nothing fixture of a DIFFERENT shape than the freeze witness's, ran it through the frozen
counter in development mode (all nine killed, attributed, `value=differs`, on my own fixtures —
`run-crit-battery3.txt`: `BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=9 killed=9 survived=0
invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=6/6 order=3/3`), and additionally ran reference-vs-
mutant copies directly to capture the exact outputs (`probe-muts.txt`, `probe-rest.txt`). Advert-cause is checked
against the docstring line in the `adv` cell.

| id | isolating input (my shape) | ref → mutant (rc, classes) | declared direction | cause = quoted clause? |
|---|---|---|---|---|
| NA1 | a 13-cell row (witness used 12) | `1 [row-malformed]` → `0 []` | silence | yes — `anchor:34-35` (`!=`→`<`) |
| NA5 | `task.toml` `name = "corp/r43svc"`; URL task component `r43svc` | `0 []` → `1 [anchor-unbound]` | rc-mirror | yes — `anchor:54-56` (slug keeps `corp/` under mutant) |
| NA7 | green erratum lane: wrong anchor `W`, correction = real committed digest | `0 []` → `1 [erratum-digest-unresolved]` | rc-mirror | yes — `anchor:112-113` (the in-A correction token is flagged) |
| NA18 | row-path locator beside a pinned URL with a **5-hex** commit segment | `0 []` → `1 [digest-wrong-capture]` | rc-mirror | yes (indirect) — `anchor:53-54` (4-6-hex segment now binds) |
| NA20 | green erratum lane | `0 []` → `1 [digest-unknown]` | rc-mirror | yes — `anchor:108-110` (exemption never granted) |
| NA21 | green erratum lane | `0 []` → `1 [erratum-digest-unresolved, digest-unknown]` | rc-mirror | yes — `anchor:108-109` (cited_wrong keyed on row ids) |
| NO5 | a gate-P10 line added in a SECOND claims commit, before the receipt | `1` → `0` | rc-silence | yes — `order:14-16` (only the oldest claims commit scanned) |
| NO7 | claims blob `P10 DEFECT receipt unreadable: <path>` | `0` → `1` | rc-mirror | yes — `order:56-57` (echoed shape no longer excused) |
| NO22 | a gate-P10-only claims blob (second claims commit) | `1` → `0` | rc-silence | yes — `order:15-16` (gate-line branch disabled) |

Two mechanism notes:

- **NA18**'s measured mechanism is subtler than a second binding: the widened `URL_RAW` lets the short-commit URL win
  `bind_row` (the first successful route returns), so the row binds `x.py` only, and the anchor (the notes.txt digest)
  becomes `digest-wrong-capture`. This is still exactly the advertised widening ("a 4-6 hex segment now binds").
- **NA1**'s `old -> new` is byte-identical to round-40 **A09** (`!=` → `<`, line 477), and both are killed by a
  12+-cell row. NA1 is a re-frozen duplicate of A09, not a new behaviour and not an equivalent (it differs from the
  reference on over-long rows). Flagged to the L1 as the one round-43 mutant that adds no calibration surface.

## 2. Incidental kills in `witness-run.txt`: none by the strict test (`i = 0`), two shared-evidence limits

Strict test: a kill is incidental if the reference/mutant difference in `witness-run.txt` is not produced by the
clause the `adv` cell quotes. Each variant is the reference with exactly one span replaced, and both run on the same
end state, so the difference is *causally* the span. I checked each of the six witness end states against the
reference source and rebuilt all six with different shapes (`r43crit.py`): the same nine kills reproduce, attributed,
with `value=differs` and identical line names (NA7→L458, NA20→L468, NA21→L456, NO5→L120, NO22→L105). No kill rides
on a different clause, an unhandled exception, or a fixture artefact.

Shared-fixture structure (not incidental, but evidence-sharing):

1. **`wit-green-erratum` kills NA7 + NA20 + NA21** — three distinct spans in the erratum handler, three distinct
   clauses, and the mutants are pairwise distinguishable on the same end state (measured, `probe-muts.txt`):
   `NA7 rc=1 classes=[erratum-digest-unresolved]`, `NA20 rc=1 classes=[digest-unknown]`,
   `NA21 rc=1 classes=[erratum-digest-unresolved, digest-unknown]`, reference `rc=0 classes=[]`.
2. **`wit-late-claims-edit` kills NO5 + NO22** — distinct spans, and NO5 ≠ NO22 (measured on two extra histories,
   `probe-muts.txt`): gate-P10 line in the OLDEST claims commit → `REF=1, NO5=1, NO22=0`; a CASE line added in a
   LATER claims commit → `REF=1, NO5=0, NO22=1`.

So no kill is incidental; but two fixtures carry 5 of the 9 kills. Same precedent as R42's X6/X7 note: legitimate
kills, but a wave-1 battery may reuse one end state for several mutants, halving the fixture count without adding
evidence. The kill rule only requires per-mutant attribution, which is met. Also note the counter's line attribution
(L456/L458/L468 for the trio) shows the spans are distinct even though the fixture is shared.

## 3. Denominator: advertised behaviours with no frozen mutant in rounds 40, 42 or 43 → `u = 18`

Union of frozen lists: 28 mutants in rounds 40+42 (11 anchor + 3 order in `round40_c1_verify.py`; 9 anchor + 5 order
in `round42_c1_verify.py`; ledger rows out of this surface) + 9 in round 43 (6 anchor + 3 order). A docstring sentence
that names an observable outcome for some input the tool accepts is *covered* if some frozen mutant alters exactly
that observable in a declared direction. Round-43 additions: NA5 (55-56 slashed-name half; location already covered by
X12), NA7 (112-113 A-membership; X14 covered only the hex-case half), NA18 (53-54 URL formats — uncovered but not in
R42's 18), NA20/NA21 (108-110 exemption grant / cited_wrong keying; X15 covered only the `supported` predicate),
NO5 (14-16 "any file" half), NO7 (56-57 echo shape — not in R42's 18), NO22 (15-16 → now alters R42 row k's
observable: a gate-P10 line with the `gate: ` prefix trips; NO22's disabled branch removes that too).

**Unlisted advertised behaviours (u = 18: 10 anchor + 8 order):**

| # | file:line | advertised behaviour | why no mutant |
|---|---|---|---|
| 1 | `anchor:24` | read-only; stdlib only; writes no file | none (no side-effect mutant) |
| 2 | `anchor:26-27` | exit 2 usage error (bad args / missing lane / absent SOURCES.md / no git) | no anchor `error`-direction row |
| 3 | `anchor:62-64` | explicit lane-path route: a `corpus/evidence/…` path in the row binds that committed file only; a directory or uncommitted path is `anchor-unbound` | no mutant touches `LANE_PATH`/the row-path branch (R42 listed 62-64 as covered; **no mutant in 40/42/43 maps to it** — correction) |
| 4 | `anchor:76` | `--verbose` prints the mode, bindings and resolutions | no mutant; no counter reads verbose output |
| 5 | `anchor:88` | `digest-short` class (non-ellipsis hex run shorter than 64) | no mutant emits or suppresses it |
| 6 | `anchor:88` | `digest-long` class (hex run longer than 64) | no mutant emits or suppresses it |
| 7 | `anchor:99-100` | a token resolving to several of the row's captures is **not** a defect (byte-identical captures) | `A27` covers only the `capture-unanchored` half |
| 8 | `anchor:102-103` | a row with no anchor token raises nothing | no mutant |
| 9 | `anchor:106-108` | lessons are read from the working tree for paths committed at HEAD (an uncommitted erratum counts) | no mutant changes the read source |
| 10 | `anchor:114-115` | an erratum whose row was since repaired stays valid (no stale-erratum defect) | none |
| 11 | `order:12` | commits only — working tree and index are ignored | none; `O12`/`XO5` change the read set, not worktree-vs-commit |
| 12 | `order:26-27` | exit 2 when the lane is not a git work tree | none |
| 13 | `order:26-27` | exit 2 when claims or receipt were never committed | none |
| 14 | `order:26-27` | exit 2 on bad arguments | none (`O14` covers only the claims-name pattern) |
| 15 | `order:29-31` | read-only: six named read commands, writes nothing, touches no network, imports no probe/gate/counter, never runs the probe | none |
| 16 | `order:37-38` | every blob under `claims/` is read, so only the pattern matters, not the file name | `O12` covers the blob-type half only; a filename filter is unmutated |
| 17 | `order:41` | an uncommitted receipt is a setup error (2), not a pass (HEAD check) | none |
| 18 | `order:14` | the scanned directory is derived from the claimed round number (`.ufo/waves/round-NN/claims/`) | `O14` covers the name→error path, not the name→dir mapping |

Composition delta vs R42's 18: R42's row k (`order:52-53`, gate `P10` line with/without the `gate: ` echo prefix)
falls — NO22's disabled gate-line branch now changes the with-prefix observable in the declared direction; one new
anchor row (62-64, explicit lane path) is added because R42 mislabeled it covered. Net count: 18 again. R42's
inventory also omitted `anchor:53-54` and `order:56-57`, uncovered then but now covered by NA18/NO7, so they do not
enter u. The narrowest defensible reading (dropping the five setup/exit-2 rows 2/12/13/14/17 and the two read-only
invariants 1/15) is **11**, as in R42.

## 4. Limits of this review

- I did not run the frozen counter in production mode; development mode with my own battery plus direct tool runs is
  the evidence (the freeze's own controls are other seats' objects). `PREDICATE C1 n/a` is expected in dev mode.
- `u = 18` is a sentence-granularity judgment; the raw list is in §3 so another granularity can be recomputed.
- The NA1/A09 duplication (§1) is a limit note: NA1 is killable and non-equivalent, but it calibrates nothing new.

Receipts (all under `build/R43CritEquiv/`, each < 1 MiB, sha256 in `COMMANDS.txt`):
`run-crit-battery3.txt` (counter run, envelope `19:09:35→19:09:40`, exit 0, `local_bin_content_before=after=328be01808ba022f`),
`probe-muts.txt` (direct trio/pair probe, envelope `19:10:49→19:10:51`, exit 0),
`probe-rest.txt` (NA1/NA5/NA18 probe, envelope `19:11:18→19:11:20`, exit 0);
plus the sources `r43crit.py`, `probe_muts.py`, `probe_rest.py`.

VERDICT: equivalents-0-incidental-0-unlisted-advertised-18
