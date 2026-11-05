# ReviewerR88b — claim/predicate consistency + Q66 extraction-engine attack (read-only)

Date 2026-11-05. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Frozen refs verified resolvable:
A `0220c2f9…`, instruments `1f267d4b…`, measured tip `7fcc680b…`, BASE `801b903a…`, R87 BASE `b9be6877…`.
Production files were only read; all writes are this seat dir plus scratch
`/fast/scratch/hyaku/kengaku-r88/ReviewerR88b/` (deleted before yield). No git mutation anywhere;
only `rev-parse`, `diff --stat`, `show`, `cat-file` in the lane. No tools installed (python3/git
already present; nothing was needed).

**Verdict: FINDINGS — 5 (1 frozen-text inconsistency, 1 wording/semantics gap, 3 engine findings).
Both headline claims' committed numbers reproduce exactly under independent re-run.**

---

## 1. Claims-file before/after numbers vs counter outputs (task 1)

Every number checked against `.ufo/waves/round-88/L1/base-runs.txt` and `tip-runs.txt`, and
independently re-run where feasible:

| Claim figure | Claims file | Evidence | Verdict |
|---|---|---|---|
| C1 before `TARGET executed_rows=31 member=fix-git located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R88-C1 fail`, exit 1 | `plans/round-88-claims.md:21-22` | `base-runs.txt:5-7` byte-identical | MATCH |
| C1 after `TARGET executed_rows=32 … defects=0`, `PREDICATE R88-C1 pass`, exit 0 | `:23-24` | `tip-runs.txt:2-4` byte-identical | MATCH |
| Ledger executed 31 → 32; `crypto-credential` 2 of 12 → 3 of 12; `file-artifact` 23 of 76 → 24 of 76 | `:24-25` | recomputed from `git show <rev>:plans/grader-population-ledger.json` at both revs: 31/32; 2/12→3/12; 23/76→24/76 (denominator = members carrying the class; `receipts/freeze-diffs.txt`) | MATCH |
| C2 before: instrument absent at BASE | `:52-53` | `base-runs.txt:10-11` (`fatal: path … exists on disk, but not in '801b903a…'`, rc=128) | MATCH |
| C2 after `RECORDS claims=17 files=8 records=56 checked=56 matched=55 mismatches=1 prose=0`, one `MISMATCH KNOWN R87-C1 kv:defects claimed==7 … measured 3`, `DEFECTS n=0`, `PREDICATE R88-C2 pass`, exit 0 | `:54-56` | my independent re-run at the tip reproduced every line exactly (`receipts/c2-tip-rerun.txt` = `tip-runs.txt:6-11`); `claims=17` = `len(CLAIMS)` table entries; `files=8` = `CLAIMS_FILES` rounds 80–87 (`plans/round88_claim_figures.py:114`) — the glob ambiguity (`round-8?` also matches round-88) does **not** apply, the list is range(80,88) | MATCH |
| C2 selftest "prints **four** `SELFTEST … pass` lines … exit 0" | `:56-57` | committed `base-runs.txt:14-18` shows **five** (`T1-doctored-extract`, `T1-doctored-mismatch`, `T2-marker-negatives`, `T3-atbase-backward`, `T4-dedupe`); my re-run: 5 lines, rc=0 (`receipts/c2-selftest-rerun.txt`); instrument emits two `check()` lines for T1 (`plans/round88_claim_figures.py:507-522`) | **DISAGREES — FINDING 1** |

Cosmetic: the claims quote at `:55` ("`MISMATCH KNOWN R87-C1 kv:defects claimed==7 measured 3`") is an
elided paraphrase — the emitted line is `… claimed==7 defects claimed =7 measured 3`
(`plans/round88_claim_figures.py:469`), so the quoted string is not a contiguous substring. Folded into
FINDING 2.

## 2. Extraction-engine attack (task 2)

Method: `python3 -c` importlib load of `plans/round88_claim_figures.py`; synthetic claims texts in
scratch only; `claim_spans`/`extract_records` executed on each, `check_record` simulated against a
canonical failing BASE output (`TARGET … defects=3`, `PREDICATE`, rc=1). Full transcript:
`receipts/attack-battery.txt`. Raw engine lines:

- **Evasions — figure that should yield a record but does not (4):**
  - **E1 prose-number form** `- **Before (BASE):** the ledger holds 31 executed rows with 3 defects, exit 1.` → `records=0 prose=0`. Span has `exit 1` (FAIL_RE, `:125`) but no `CONVO_RE` token (`:128-130`) → discarded at `:179`. "31 executed rows"/"3 defects" carry no `key=` shape and no counter token.
  - **E3 PREDICATE-first ordering** `- **Before (BASE):** \`PREDICATE R99-C3 fail\` — the counter printed \`TARGET executed_rows=31 defects=3\`, exit 1.` → `records=0`. `SPAN_END_RE` (`:123`) cuts at `PREDICATE` before the figures; span is one backtick; CONVO fails.
  - **E4 `**State at BASE:**` prefix style** → `records=0`. The only marker hit is backward (`at BASE`, `:182-193`); the backward span is the text *before* the marker and requires literal `exit 1` in it — `"- **State"` contains neither, and figures *after* the marker are never captured by any rule.
  - **E5 colon figures** `` `TARGET defects: 7 located: 0` `` → span kept (CONVO via `TARGET `) but `KV_RE` (`:131`) requires `=`, so `records=0 prose=1`. The prose count is printed in RECORDS (`:481-482`) but is **not a defect** — the span figure is invisible to the verdict.
  - **Downstream for all four:** `F6-norecords` (`:447-448`) fires only for a claim with **zero** records *and* (`rc == 0` or no `PREDICATE` in output). A normally failing BASE run prints `PREDICATE` and exits 1, so F6 stays silent — verified in the battery ("F6-norecords would fire: False" for E1/E3/E4; E5 keeps zero records too). **These are real blind spots, not caught downstream.** The frozen predicate sentence is scoped to "*every extracted* before-figure record", so an unextracted figure violates nothing observable — the completeness of extraction is convention-dependent and unproven. No current corpus figure is *proven* missed (`prose=0`), but E1/E3/E4 would also leave `prose=0` while silently dropping the figure.
- **False records — non-before figure extracted as a before-record (3):**
  - **F1 after-figure in forward span:** `- **Before (BASE):** \`TARGET defects=3\` and after the fix \`TARGET defects=0\`, fail, exit 1.` → two kv records `defects=3` and `defects=0`; the latter checks `mismatch` vs measured 3 → would emit `MISMATCH UNEXPECTED` → `F5-unexpected` (`:470-471`) → predicate **fail** (false alarm).
  - **F2 backward-span capture of after-figures:** sentence ending `… unlike \`TARGET executed_rows=32 defects=0\`, exit 1 at BASE.` → records `executed_rows=32`, `defects=0` — tip figures taken as before-records → both `mismatch` → false alarm.
  - **F3 hypothetical figure:** "a forged ledger would print `TARGET defects=9` — the real figure is `TARGET defects=3`" → record `defects=9` → `mismatch` → false alarm. The extractor cannot distinguish observed from narrated/hypothetical figures inside a span.
  - **Direction of failure:** these fail *safe* (a false record mismatches → `F5-unexpected` → predicate fail), **except** when the false figure's value coincides with the measured value — then it counts as `matched` silently (demonstrated in F1: `defects=3 → match`). The corpus today has `mismatches=1` equal to KNOWN exactly, so no live occurrence.
- **Anti-findings (honest negatives):** E2 `exit 1 at Base.` is **not** an escape — the leading `(?i)` at `:120` scopes the entire alternation, so `\bat BASE\b` is case-insensitive; the engine extracted both records. A TARGET string wrapped across lines in the claims text (F4) is also handled: `KV_RE` spans the newline and the counter's single-line TARGET parses both keys → both `match`, no false F4.

## 3. Frozen KNOWN set verification (task 3)

Command run (read-only; work in scratch):
`python3 plans/round87_c1_replay.py --lane <lane> --rev b9be687774e6b559470f5b0d9b936315b51ff311 --work $S/r87work`
→ `TARGET executed_rows=30 member=mteb-retrieve located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R87-C1 fail`, rc=1 (`receipts/r87-base-rerun.txt`).
Measured value is **3** — matches the frozen KNOWN literal `("R87-C1", "defects"): (7, 3)`
(`plans/round88_claim_figures.py:111-113`) and the round-88 claims text (`:62-65`). The round-87 claims
file's quote is `plans/round-87-claims.md:18` (`… defects=7` inside the Before TARGET) and `:28`
(do-nothing control `defects=7`): every other R87-C1 before figure (30 / mteb-retrieve / 0 / 0 /
mismatches=0) matches the re-run; `defects` is the **only** disagreeing figure — exactly the corpus's one
documented mispredict (R87-V2). The `F5-known-value` guard (`:476-480`) additionally pins the measured
side at 3.

## 4. R88-C2 predicate three-way comparison (task 4)

1. **Claims file** (`plans/round-88-claims.md:58-61`), verbatim: "pass iff every extracted before-figure
record is checked, every claim's counter completes at its BASE, the mismatch set equals the frozen KNOWN
set `{(R87-C1, kv:defects): claimed 7, measured 3}` exactly — reported `MISMATCH KNOWN`, never
`UNEXPECTED` — and the selftest battery exits 0." Declared "identical in this file, the counter's
`PREDICATE R88-C2` line and the report".
2. **Counter semantics** (`plans/round88_claim_figures.py:376-490`): `PREDICATE R88-C2 pass|fail` at
`:489` is a bare verdict; pass ⇔ the defect list is empty, where defects are `F1-corpus` (claims file
absent at rev), `F2-claim/-mode` (claim without frozen table entry / unknown mode), `F3-prose/-timeout/
-nopredicate` (prose-mode absence check failed / counter timed out / no `PREDICATE` token in output),
`F4-unparsed` (extracted record not checkable), `F5-unexpected`, `F5-missing-known`,
`F5-known-value`. That implements conjuncts 1–3 of the sentence (checked ⇔ no F4; counters complete ⇔
no F3; mismatch set == KNOWN ⇔ no F5-*). The docstring's own predicate sentence (`:30-33`) reads: "pass
iff every extracted record is checked, every re-run completed, and the set of mismatched records equals
the frozen KNOWN set exactly…" — **three** conjuncts.
3. **Report requirement:** per `:58` the round report must carry the identical sentence, i.e. the full
four-way conjunction including "and the selftest battery exits 0"; the committed evidence must therefore
show both rc=0 runs (main + `--selftest`), which `base-runs.txt:13-21` and my re-runs do.

**Gap — FINDING 2:** the sentence is *not* identical across the three places: the docstring drops the
selftest conjunct, and the `PREDICATE R88-C2` line itself cannot attest it at all — `run_check` never
runs the battery; `--selftest` is a separate process (`:579-580`). Gating on the single `PREDICATE
R88-C2 pass` line alone tests only three of the four conjuncts. Operationally benign today (both runs
are committed and both exit 0), but the report and the L1 gate must check both exit codes, and the
report must not quote the docstring's three-conjunct variant as "the" predicate.

## 5. Freeze verification (task 5)

All three `git diff --stat` comparisons empty (exit 0) — quoted in full in
`receipts/freeze-diffs.txt`:
- `0220c2f9… → 7fcc680b…` over `plans/round-88-claims.md plans/round88-cases.json`: unchanged.
- same range over the eight claims files `plans/round-80-claims.md … round-87-claims.md`: unchanged
  (C2 kill-rule leg "any edit to a frozen claims file … after commit A" holds).
- `1f267d4b… → 7fcc680b…` over `plans/round88_c1_replay.py plans/round88_claim_figures.py
  plans/round88_fixgit_probe.py`: unchanged.

---

## Findings (severity-ordered)

1. **[Minor] Frozen After bullet misstates the selftest output — "four" lines, observed five.**
   `plans/round-88-claims.md:56-57` vs `.ufo/waves/round-88/L1/base-runs.txt:14-18` and
   `receipts/c2-selftest-rerun.txt` (`grep -c '^SELFTEST'` = 5; rc=0, `PREDICATE R88-C2-SELFTEST pass`).
   Root cause: `selftest()` makes two `check()` calls for T1 (`plans/round88_claim_figures.py:507-522`),
   the frozen text was written against a four-test plan. Frozen element — reported, not repaired. The
   round report must not repeat "four"; the substantive criterion (battery exits 0) holds.
2. **[Minor] Predicate-sentence identity does not hold across its three declared homes.**
   `plans/round-88-claims.md:58-61` (4 conjuncts, incl. "and the selftest battery exits 0") vs
   `plans/round88_claim_figures.py:30-33` (3 conjuncts, selftest leg absent) and the bare
   `PREDICATE R88-C2` verdict line (`:489`) that cannot attest the battery. Also `:55` quotes the
   MISMATCH line in elided form (not a contiguous substring of the emitted line, `:469`).
   Operationally safe because both runs are committed; report and gate must consume both rc=0s.
3. **[Minor] Extraction recall is convention-dependent; evaded before-figures are silent end-to-end.**
   Demonstrated escapes E1/E3/E4/E5 (§2): figures in prose-number form, after a `PREDICATE` token,
   after an `at BASE` marker, or colon-delimited yield no record; `F6-norecords`
   (`plans/round88_claim_figures.py:447-448`) only guards the zero-record *counter-pass* case, and a
   prose span is counted (`:481-482`) but is not a defect. No live corpus figure is proven missed, but
   Q66's intent ("every frozen before-figure re-derivable") is only as complete as the
   marker/vocabulary net; a future claims file phrased outside it sails through `PREDICATE R88-C2 pass`.
4. **[Minor] Over-capture: after-figures, tip figures and hypotheticals become before-records (F1/F2/F3).**
   They usually fail safe (`MISMATCH UNEXPECTED` → `F5-unexpected` → predicate fail, a false alarm), but
   a false figure whose value coincides with the measured one is silently `matched` (shown in F1).
   No live occurrence (`mismatches=1` == KNOWN exactly). The instrument relies on corpus style to
   distinguish observed figures from narration.
5. **[Low] KNOWN-set matching is record-representation-sensitive.** `known_pairs =
   {(c, f"kv:{k}")…}` (`plans/round88_claim_figures.py:464`) hardcodes kind `kv`; the same documented
   mispredict phrased `DEFECTS n=7` would extract as `deftotal` and its mismatch key
   `deftotal:defects` would fall outside KNOWN → `F5-unexpected` → predicate fail despite being the
   known mispredict. Frozen-correct for the current corpus (the figure is kv form at
   `plans/round-87-claims.md:18`); a fragility to note for any future KNOWN entry.

## Residual risk and verification gaps

- I did not re-run the R88-C1 counter/probe/legs at the tip — C1's runtime legs are the executor/L1
  seats' scope; my check is that the claims numbers equal the committed counter outputs (they do).
- "checked=56" counts every record fed to `check_record`, including any `unparsed` verdict (`:451`);
  the predicate still fails on `F4`, so the headline is sound, but "checked" is not "matched or
  mismatched" in that rare case.
- Extraction completeness is unprovable from the instrument alone (finding 3 is the demonstration);
  the only corpus-level assurance is `prose=0` plus 56/56 checked on today's phrasing.
- `run_rev` executes counters with `env={"PATH": "/usr/bin", …}` (`:299`) — worked here (Arch keeps
  `python3` at `/usr/bin/python3`); a counter needing anything else on PATH would timeout → `F3`.
- Tooling record (operator 2026-10-19): no installs or upgrades performed — none needed.

Receipts in this directory: `receipts/c2-tip-rerun.txt`, `receipts/c2-selftest-rerun.txt`,
`receipts/r87-base-rerun.txt`, `receipts/attack-battery.txt`, `receipts/freeze-diffs.txt`.
Scratch `/fast/scratch/hyaku/kengaku-r88/ReviewerR88b/` deleted before yield.
