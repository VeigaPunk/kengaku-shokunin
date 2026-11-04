# Round 71 — kengaku (hyaku run 15)

Round 71 declared two claims (`plans/round-71-claims.md`, frozen at `d8a77d3f` on base
`1cb49cac`): **R71-C1** coverage — replay the `hf-model-inference` Terminal-Bench 2.0 grader
offline under an eight-case frozen table in which every one of its four legs is witnessed `P`
and `F` — and **R71-C2** calibration — close the round-70 non-author closure's two routed
defects R70-D1 (`Mistakes`-row count drift) and R70-D2 (the nginx entry's residual
`instruction.md:6-11` citation) with a re-deriving gate. R71-C1 is **admitted on its frozen
sentence** (all eight `VECTOR` lines `agree=True`, `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`,
`SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2`, `--check-receipt` rc 0, the do-nothing
control refused); R71-C2 is **admitted on its frozen predicate** (`DEFECTS n=6` → `n=0`,
selftest 4/4 all-fail, gate mutants 4/4). Both are admitted with the gaps below named rather
than smoothed: the covered unit is the *leg*, not each assert site (6 of 19 grader asserts have
a negative witness, `LegPricing` §4b); `E2a`'s membership test is a fragment, so the prose's
"verbatim" condition is carried by an appended erratum, not by the check; and the red-before is
a red-data run with the freeze instrument, because the gate did not exist at base.

## Gate

SOURCES contract v1 — rows opened this round, each with its access date and a located quote.

- **S245 — the task instruction at the pin. Admit** (tier A, docs). Opened live 2026-11-03 by
  `curl` at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/instruction.md`
  (HTTP 200, 1264 bytes, 28 lines, sha256
  `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1`), `cmp` byte-identical to
  the committed capture `corpus/evidence/round71/hf/instruction.md`; the row is
  `corpus/SOURCES.md:260`, status `mined`, used-by the round-71 entry. Located quote (16 words),
  line 3: `Download the "distilbert-base-uncased-finetuned-sst-2-english" sentiment analysis model from Hugging Face and save to the local directory '/app/model_cache/sentiment_model'.`
  The same file states the `POST /sentiment` request and response schema (`:11-24`), the
  `0.0.0.0:5000` binding (`:6`) and the 400 error body (`:25-28`); it never states the six texts
  the grader grades.
- **S246 — the grader at the pin. Admit** (tier A, code). The same pinned fetch (HTTP 200, 4239
  bytes, 107 lines, sha256
  `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`), `cmp` byte-identical to
  `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` and its
  `SHA256SUMS:76` line; the row is `corpus/SOURCES.md:261`. Located quote (8 words), lines 29-30:
  `requests.get("http://0.0.0.0:5000")` / `except requests.exceptions.ConnectionError:` — the
  liveness leg never inspects the status, so any HTTP answer passes it; the 400 leg is the
  unquoted `assert response.status_code == 400,` at `:103`.
- **`merge/kengaku` entry `grader-predicate-input-types.md`. Reject.** Opened at
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/grader-predicate-input-types.md`
  (3300 bytes). Three grounds, each on the entry's own bytes: (i) its triad is offset — line 1
  is blank, `source:` sits at `:2-3` and `recheck:` at `:5` (Q1); (ii) its cited `S143`/`S144`
  resolve in this lane to different sources — `corpus/SOURCES.md:160-161`, the
  `feal-linear-cryptanalysis` README and `solve.sh` — so the tier-A floor for its Toolathlon
  comparison-function claim is not met here (Q2, Q9); (iii) its own-work citation
  `lanes/kengaku/round7/toolathlon-grader-fixture-probe.md` (`:3`) is not held by this lane
  (`git ls-files | grep -c 'lanes/kengaku'` → 0), so its headline `16 of 16 separate the two`
  (`:20-23`) cannot be re-derived from lane bytes. **Flip:** stage the merge registry's two ids
  as fresh rows carrying the Toolathlon URL
  (`tasks/finalpool/yahoo-analysis/evaluation/main.py` at `9be8d8fe`) and carry the round-7
  probe artefact (or re-point the count at a held capture); the substance — a comparison
  function called with a bare string returns `None`, which a probe can misread as "no
  discrimination" — is worth carrying.
- **Assimilation: none.** One entry considered, rejected; no canonical knowledge row is claimed
  from `merge/kengaku`.
- **Census.** Before: `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  → rc 0, **236** data rows, 25 `W04` warnings (`.ufo/waves/round-71/census-before.txt`, sha256
  `5bbde4eee78cb5806484850cc0f00ac48e475f62226a9ddf57135ea0d989fcde`). After: the same command at
  the landed tree → rc 0, **238** data rows, the same 25 `W04` warnings; the stdout is
  byte-identical to the before capture because the two new URLs are fresh and the `ok` line is
  unchanged — only the row count moves.
- **Admission status (QUALITY Q13/Q14): HOLD.** The round-71 entry
  `corpus/knowledge/tb2-hf-model-inference-offline.md` (`writer: KnowledgeEntryDraft`) is landed
  and indexed but **not admitted**: Q13 requires a returned second-seat re-read cited by
  repo-relative path from a second-wave directory, and `plans/gate_timing_check.py:284-300` loads
  only `w2`/`falsify` registries. This round dispatched ONE v1 wave under the run-15 8–16 band, so
  no such seat exists; `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-71.md
  --commit <tip>` therefore prints `no admit rows … failed=1`. Round 72 dispatches the falsify
  wave that admits the entry; the S245/S246 rows and the class-row move do not depend on the
  entry's admission.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **dispatched counter written in Python repetition syntax** | the item's row count `grep -cE '^\|[[:space:]]*S[0-9](3,)[[:space:]]*\|' corpus/SOURCES.md` → `0`, rc 1, against 236 real rows; the intended `…S[0-9]{3,}…` → `236` (`.ufo/waves/round-71/w1/DepthGateRerun.md` §Census; both forms re-run by `Lesson71Draft`) | the `DepthGateRerun-2` seat, on its own item text | use `{3,}`; the lesson and the post-landing count use the corrected form (`→ 238`). The dispatch template is the L1's to fix, not a predicate. |
| **fragment membership accepted for a verbatim-quote condition** | the claims require the erratum to quote the superseded sentence verbatim (`plans/round-71-claims.md:91-93`); the gate defines `SUPERSEDED_SENTENCE = "states the same bodies"` (`plans/round71_c2_routed_defects.py:169`) and greps it anywhere (`:176,187`), so `E2a ok` printed over an erratum (`corpus/knowledge/tb2-nginx-request-logging-offline.md:92-95`) that quoted the fragment while the original sentence sat verbatim at `:14-15` (`.ufo/waves/round-71/w1/DefectGateReverify.md` §P2) | `DefectGateReverify-2`, reading the gate against its own bytes | `E-D2a` appended (`corpus/knowledge/tb2-nginx-request-logging-offline.md:96-99`) quoting the full sentence — "The instruction at the same pin states the same bodies, the rate-limit zone location and the log path (`instruction.md:6-11`)." — and the gate stays green on the fragment clause; the gate's contract is unchanged, the prose condition is now carried by the erratum |
| **red-before run with an instrument that did not exist at base** | `python3 $D/plans/round71_c2_routed_defects.py --lane $D` at `1cb49cac` exits 2: `python3: can't open file '/fast/scratch/hyaku/kengaku-r71/base.NFi4/plans/round71_c2_routed_defects.py': [Errno 2] No such file or directory`; the six-defect red (`.ufo/waves/round-71/c2-red-before.txt`: `DEFECTS n=6`, `PREDICATE R71-C2 fail`) was reproduced by the *freeze* gate reading base data (`.ufo/waves/round-71/w1/DefectGateReverify.md` §P3) | `DefectGateReverify-2` | label the receipt as red-data with the freeze instrument; the claims' "Red-before (committed at freeze)" (`plans/round-71-claims.md:116`) does not say which instrument ran, and a gate created in the freeze commit cannot have a base-instrument run. Reported, not edited. |
| **a control receipt named "committed at freeze" but absent from the freeze commit** | `git cat-file -e d8a77d3:.ufo/waves/round-71/c1-control.txt` → rc 128, `fatal: path '.ufo/waves/round-71/c1-control.txt' exists on disk, but not in 'd8a77d3'`; `git ls-tree -r --name-only d8a77d3 -- .ufo/waves/round-71/` lists `c2-red-before.txt` and `census-before.txt` but not `c1-control.txt`, which is `??` in the wave dir (mtime 22:21, after the 22:08 freeze commit) while `plans/round-71-claims.md:59` reads "**Do-nothing control (committed at freeze).**" | `Lesson71Draft`, reading the claims against the freeze tree | commit the control with the landing (then the sentence is true of the round, not of the freeze) or reword the heading to "produced before the scored battery"; the control's content is correct — every case `FFFF`, `seen_p=0`, `PREDICATE R71-C1 fail` — only its claimed commit is not. Reported, not edited. |
| **leg-level coverage read at assert-site granularity** | the claim and `LEG-COVERAGE legs=4 seen_p=4 seen_f=4` count *legs*; the assert-site tally is 6 priced of 19 — `:13`, `:22`, `:31`, `:77`, `:86`, `:103` (`.ufo/waves/round-71/w1/LegPricing.md` §4b) — and 13 unpriced, of which `test_outputs.py:107` `assert "error" in error_data` is unreachable under the frozen modes (K4 reds on `:103` first) and `:19-20` are practically dead (`.ufo/waves/round-71/w1/CaseTableAudit71.md` §What the table fails to distinguish item 2, and its ADD-ONE K9 `400-no-error-field` `PPPF`) | `CaseTableAudit71` and `LegPricing`, independently | the claim is honest at its stated unit; carry the assert-site gap as a limitation and freeze K9 in a successor table to price `:107`. The count in the new Q53 row (`corpus/QUALITY.md`) reads "six … without a negative witness", which inverts the seats' tally (six *have* a witness, thirteen do not); that one line is the L1's to reconcile — reported, not edited here. |
| **sandbox environment inherited, so a stubbed library reproduces the whole table** | `ClaimFalsify71` §C1-b: `bwrap_argv` never clears the environment (`plans/round71_c1_hf_probe.py:416-441`), so a designed `transformers` stub placed on `PYTHONPATH` derives 8/8 frozen vectors and a receipt byte-identical to the record; the `LIBRARIES` line is measured on the host (`:315-325`), not inside the sandbox (`.ufo/waves/round-71/w1/ClaimFalsify71.md:56-116`) | the `ClaimFalsify71` critic, running the probe's own staging with one env delta | named limitation: the model-load witness is an outcome check, not a provenance check; round 72's successor probe adds `--clearenv` plus an explicit env allowlist and records `transformers.__file__` from inside the sandbox |
| **a defect detector's count parser accepts only word numerals** | `plans/round71_c2_routed_defects.py:85-91` maps words only: `8 Mistakes rows` yields the string `"8"` (`"8" != 8`, a false red) and a backticked `` `eight` `` yields `None` (a false red) — measured as T9/T10 (`.ufo/waves/round-71/w1/GateMutate71.md` §T9/T10) | the `GateMutate71` mutation-tester | round 72: `parse_count` int-coerces digits and strips backticks; the frozen R71-C2 predicate and its receipt are untouched |
| **`--mutants` invariance read as arm-level necessity** | `MUTANTS total=4 killed=4 survived=0` reproduces under all six semantic mutants; at check level the same matrix is 2/6 killed and 4/6 survived, with M1 (E1c count-only) and M2 (E2a missing-range) passing the entire predicate on defective bytes (`.ufo/waves/round-71/w1/GateMutate71.md` §5.4) | the `GateMutate71` seat, reading the metric against its own fixture matrix | the round report cites the line only as the literal frozen predicate, never as arm-level evidence; round 72 adds an accept-the-red-lane arm to the mutation metric |

Candidate **not** written: the item's suggestion that a `port_free` bound without
`SO_REUSEADDR` scored five `SETUP` cases is not in this round's bytes. The frozen probe sets
`SO_REUSEADDR` before every bind (`plans/round71_c1_hf_probe.py:327-338`), every round-71
receipt line is `sandbox_rc=0`/`setup=0` (`corpus/evidence/round71/hf/receipt.txt:9-33`,
`.ufo/waves/round-71/c1-control.txt` `SUMMARY … setup=0`), and `grep -rn 'setup=[1-9]'` over
`corpus/evidence/round71` and `/fast/scratch/hyaku/kengaku-r71` finds no round-71 receipt with
a nonzero setup count (the `SETUP` hits under that scratch tree are historical text in sibling
copies and clones). A mistake row needs an observation; this one has none.

## Census

- Before: `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  → rc 0, 236 data rows, 25 `W04`; `.ufo/waves/round-71/census-before.txt` sha256
  `5bbde4ee…9fcde`.
- After: the same command → rc 0, 238 data rows, 25 `W04`; the stdout is byte-identical to the
  before capture. Corrected row counter:
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `238` (the item's
  `(3,)` form prints `0`; see Mistakes row 1).
- The evidence-dir capture `corpus/evidence/round71/census-after.txt` was first written mid-landing
  (25 `W04` + 2 `E11 S245/S246 missing used-by corpus/knowledge/tb2-hf-model-inference-offline.md`,
  rc 1) before the knowledge entry landed; it was re-captured at 22:28 after the entry landed and
  is now byte-identical to the before capture (sha256 `5bbde4ee…9fcde`, rc 0). The mid-landing
  state is named here because a row that cites a source the tree does not yet hold is what `E11`
  catches — the checker was right and the tree was early.
- Validator self-test: `sh scripts/sources-census.sh selftest` → rc 0, 96 `killed`, 0
  `survived` (`.ufo/waves/round-71/w1/DepthGateRerun.md` §Census).

## Verdicts

- **R71-C1**: admitted on the frozen sentence; coverage held at its L0 cap (7). Receipt of
  record `corpus/evidence/round71/hf/receipt.txt`: eight `VECTOR … agree=True` lines, all
  `derived` equal to the frozen table; `:34` `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`; `:35`
  `SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2`; `:36` `PREDICATE R71-C1 pass`. The five
  digest bindings (`:2-6`) re-derive from committed bytes at `REV d8a77d3f` — `PROBE_BLOB` is
  the blob of `plans/round71_c1_hf_probe.py` (`git show d8a77d3f:… | sha256sum` →
  `d5ce2fa5…a82e`), `PROBE` equals it, and `ReceiptReview71` §1 recomputed all five by hand. The
  checker prints `DEFECTS n=0` / `PREDICATE R71-C1 pass`, rc 0
  (`corpus/evidence/round71/hf/check.txt`; `.ufo/waves/round-71/w1/HfBatteryR71.md` §1
  `CHECK_RC=0`, re-run by `.ufo/waves/round-71/w1/ReceiptReview71.md` §2). The do-nothing control refuses
  (`.ufo/waves/round-71/c1-control.txt`: eight `derived=FFFF`, `seen_p=0`, `mismatches=8`,
  `PREDICATE R71-C1 fail`). A second battery reproduces the same eight vectors byte-for-byte
  (`corpus/evidence/round71/hf/receipt-replicate.txt`, `cmp` identical). The class row moves:
  `grep -c 'executed 3 of 8' SKILL.md` → `0`, `grep -c 'executed 4 of 8' SKILL.md` → `1`
  (`SKILL.md:78`). Calibration: coverage is at *leg* level — every leg has both witnesses from
  a genuine assertion at least once (`LegPricing` §5) and six of eight cases are single-red —
  but 13 of the grader's 19 assert sites have no negative witness (L3: 2 of 12; L4: 1 of 2),
  K6's L3/L4 `F` cells are escaped `ConnectionError`s recorded on the `EXC` line (not assertion
  reds), and K8's "corrupt" is a malformed `config.json`, not bad weights.
- **R71-C2**: admitted on the frozen predicate; calibration held at ceiling (10), exercised.
  At the tip `python3 plans/round71_c2_routed_defects.py --lane .` prints `E1a ok`, `E1b ok`,
  `E1c ok`, `E2a ok`, `DEFECTS n=0`, `PREDICATE R71-C2 pass`, rc 0
  (`corpus/evidence/round71/c2-green.txt`, reproduced by `DefectGateReverify-2`); the red before
  the correction is `DEFECTS n=6` / `PREDICATE R71-C2 fail`
  (`.ufo/waves/round-71/c2-red-before.txt`, a red-data run with the freeze instrument —
  Mistakes row 3); the selftest prints
  `SELFTEST defects-in-fake=4 want=4 all-fail=True append-only-arm=True ok=True` and the gate
  mutants print `MUTANTS total=4 killed=4 survived=0`
  (`corpus/evidence/round71/c2-controls.txt`). The corrections are present and re-derive:
  `LOG.md:2650` appends the dated R70-D1 correction quoting the superseded "five rows" and
  stating eight; both `corpus/README.md` round-70 mentions (at `d8a77d3f`: `:565`, `:799`) say
  eight and name all eight classes; `corpus/lessons/round-70.md:63` carries the appended erratum; the nginx
  entry keeps the superseded sentence at `:14-15` and carries `E-D2` (`:92-95`) plus `E-D2a`
  (`:96-99`). Named gap: `E2a`'s membership contract is the fragment `states the same bodies`,
  so the frozen prose's "quoting the superseded sentence verbatim" is established by `E-D2a`,
  not by the check (Mistakes row 2); and the red-before is red-data (Mistakes row 3).
- **No owned axis harmed.** C1 touches `SKILL.md`'s `network-service` row, adds S245/S246 and the
  entry; C2 appends to `LOG.md`, `corpus/README.md` and the nginx entry. The only replaced line
  is the class row itself (`git diff --numstat SKILL.md` → `1 1`, the `executed 3 of 8` cell at
  `:78`); every other touched file appends (`LOG.md`, `corpus/README.md`, the nginx entry and the
  round-70 lesson's `## Errata` block show insertions only). No other class row, earlier score or
  earlier lesson line is edited. The SCORECARD section is the L1's.

## Limits (named, not scored)

- **The receipt is untracked until the L1 commit.** At the seats' write time
  `corpus/evidence/round71/hf/receipt.txt` and the sandbox captures are untracked; the four
  digest bindings already re-derive from `d8a77d3f`, and the receipt becomes committed bytes
  only with the landing commit (Q22 re-run owed at the tip).
- **`--check-receipt` is a consistency check, not run provenance.** A hand-written,
  self-consistent receipt that drops `EXC`, sets `SUMMARY … exc=0` and changes `server_pid`
  passes it (rc 0, `DEFECTS n=0`; `ReceiptReview71` §3 F2(d)) — `server_pid` is unchecked decoration
  and `EXC` is optional. The live witness is `corpus/evidence/round71/hf/sandbox/`; no receipt
  digest binds those captures.
- **Host-state coupling.** The `LIBRARIES` line is re-derived against `/fast/ComfyUI/.venv` at
  every check (`plans/round71_c1_hf_probe.py:655-657`); a future venv upgrade would retroactively
  fail a genuine receipt with `library-drift`. Current:
  `python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2`.
- **The staged model is a five-file synthetic fixture** (`MODEL tree_sha256=c5c25767…8944`); the
  replay prices the grader's logic, not distilbert accuracy.
- **The depth gate does not read the executed-counter cell.** A row whose evidence cell is
  `zzz-no-counter` still prints `PREDICATE R63-C2 pass` (`.ufo/waves/round-71/w1/DepthGateRerun.md`
  §p2), so the `3 of 8` → `4 of 8` move is witnessed by the grep pair plus the hf receipt, not
  by that gate; the pre-entry depth receipt
  (`corpus/evidence/round71/gates/depth-gate.txt`, `paths total=34`) must be re-run at the landed
  tip so the new row tokens resolve.
- **K6's L3/L4 reds are exceptions, not assertion failures** — the frozen predicate counts them
  `F` (pytest scores an exception as a failed test) and no leg depends on K6 for its only red;
  the `EXC` line now separates them, which discharges round 70's named limitation (iii) in the
  direction it asked for, without changing the `P`/`F` unit.
- **`test_flask_api_running` accepts any HTTP answer** (grader `:29`); K5 prices the only
  failing mode a live listener can have.
