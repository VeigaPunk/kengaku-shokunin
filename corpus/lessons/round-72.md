# Round 72 — kengaku (hyaku run 15)

Round 72 declared two claims, frozen at `b6336136` (2026-11-03T23:02:34-03:00) on base `c6322972`
(`plans/round-72-claims.md`): **R72-C1** coverage — replay the `hf-model-inference` Terminal-Bench 2.0
grader (pin `2fd12b88`, sha256 `61a686d6…87857`) offline under a nine-case frozen table whose sandbox
is proven isolated (`bwrap --clearenv`, a nine-variable allowlist, the sandbox's own
`transformers.__file__`, a canary) and whose stub-injection control must be blind — and **R72-C2**
calibration — close round 71's routed defects R71-R1 (registry rows) and R71-R7 (freeze-doc
overclaim) with a re-deriving gate whose mutation metric is a fixture matrix. R72-C1 is **admitted on
its frozen sentence** and R72-C2 on its frozen predicate; the exact counters are in §Verdicts. The
round's new knowledge entry (`corpus/knowledge/tb2-hf-model-inference-provenance.md`) is **not
admitted**: `admission: hold`, and no second-wave seat exists this round to discharge Q13/Q14. What
the round found and did not close is in §Mistakes and §Limits — including that C2's registry check
closes the four reported rows and not the class (a fifth instrument still prints `DEFECTS n=0`), that
the four rows it appends are themselves defective in 9 of 32 cells, and that C1's `env_cleared=True`
is a hardcoded literal while the canary is the witness that carries the isolation claim.

## Gate

SOURCES contract v1 — rows opened this round, each with its access date and a located quote.

- **S247 — the `bwrap(1)` manual at bubblewrap 0.13.1. Admit** (tier A, docs). Row
  `corpus/SOURCES.md:263`, status `mined`, recheck 2027-05-02, `used-by`
  `corpus/knowledge/tb2-hf-model-inference-provenance.md`. URL
  `https://man.archlinux.org/man/bwrap.1.en`; the row records a live fetch on **2026-11-03** (HTTP
  200, 27981 bytes, HTML man page). The committed capture is
  `corpus/evidence/round72/sources/bwrap.1.html`; this seat re-derived it — `wc -c` → **27981** and
  `sha256sum` → `708f56eed930f9a0b524fd79b8d9db92c4c35eb246646c4b0fab0812d7e68de7`, both equal to
  the row (and to `KnowledgeIndexR72.md` §1). Located quote (15 words), capture `:184-186` (the
  `--clearenv` entry; the indented body is `:185`): `Unset all environment variables, except for PWD
  and any that are subsequently set by --setenv`. The same entry states `--setenv` and `--unsetenv`,
  which is why the probe's argv pairs `--clearenv` with an explicit `--setenv` list; the `PWD`
  exception is the one key the live `env_keys` carries that `ENV_ALLOW` does not name
  (`HfBatteryR72.md` §F1). **Admitted**: the claim this row bounds — `--clearenv` unsets everything
  except `PWD` and later `--setenv` assignments — is what the manual says, and the capture
  re-derives byte-for-byte. The fetch's HTTP status is the row's record, not this seat's
  observation; no live re-fetch was made.
- **S248 — the model card of the checkpoint the task names. Admit** (tier A, docs). Row
  `corpus/SOURCES.md:264`, status `mined`, recheck 2027-05-02, same `used-by`. URL
  `https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english/raw/main/README.md`; live
  fetch **2026-11-03** (HTTP 200, 10512 bytes). Capture
  `corpus/evidence/round72/sources/hf-model-card.md`; this seat re-derived **10512** bytes and
  sha256 `75f17282923fea5b541df92640e2d8646c4ff5e8e3e16ed0a7e4e50ee7588851`, both equal to the row.
  Located quote (3 whitespace tokens), capture `:145`: `model =
  DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")`.
  The card is what bounds the claim's limitation (iii): the staged object in the replay is a
  five-file synthetic fixture (`MODEL tree_sha256=c5c25767…8944 files=5`, 13,944 bytes), not this
  checkpoint, so the replay prices the grader's logic, not the model's accuracy. **Admitted** on the
  identity field it is cited for. One row field was corrected at landing, not silently: the freeze
  row (`git show b6336136:corpus/SOURCES.md`, line 264) read "172 lines" while the committed capture
  carries **197** newlines (165 non-empty); `KnowledgeIndexR72.md` §4.5 reported the mismatch, and
  the landing edit's `corpus/SOURCES.md` diff (`1 1`) now reads "197 lines". Bytes and sha256 were
  right throughout.
- **S245/S246 — re-derived, not re-fetched.** The round-71 instruction and grader rows
  (`corpus/SOURCES.md:260-261`) remain admitted; the round-72 entry and both batteries re-derive them
  from the committed captures `corpus/evidence/round71/hf/instruction.md` (`29151c5b…dcc1`) and
  `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` (`61a686d6…87857`), and
  the receipt of record pins both. No live re-fetch of either URL was made this round, so "HTTP 200"
  remains the round-71 fetch's claim, not this seat's observation.
- **`merge/kengaku` entry `card-provenance-and-preregistration.md`. Refuse.** Considered as the
  package's closest match to this round's subject — a record frozen before the data it governs, which
  is the shape of C1's freeze-before-battery sanction. The package report
  (`/home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md`) stages 175 rows and 65 knowledge
  entries and lists this one at `:50` as a round-9 new file; the entry was read at
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/card-provenance-and-preregistration.md`
  (4576 bytes). Three grounds, each on the entry's own bytes:
  (i) **Q1 triad offset** — line 1 is blank; `source:` occupies `:2-7`, `verified-at:` `:8`,
  `recheck:` `:9`, `ground:` `:10`. The triad does not open the entry.
  (ii) **Q2/Q9 tier floor** — every id it cites resolves in this lane to a different document.
  `S159`–`S164` are the Terminal-Bench 2.0 `password-recovery` `instruction.md`,
  `environment/setup.sh`, `environment/Dockerfile`, `tests/test.sh`, `README.md` and
  `solution/solve.sh` at pin `2fd12b88` (`corpus/SOURCES.md:174-179`), while the entry cites arXiv
  `2608.29463`, arXiv `2512.09577`, the `auto-benchmarkcard` README, the HF evaluation-cards blog, a
  HF dataset commit and an `audit/PRE-REGISTRATION.md`. The one URL the lane does hold under another
  id — `2608.29463`, which is `S081` at `:105`, a tier-B contamination-taxonomy paper held for a
  different claim — cannot stand in without misattributing the claim (Q9). None of the entry's six
  URLs has a row of its own here, and none of its cited bytes is captured in this lane.
  (iii) **grounds not in the lane** — `ground: N14 and N20` (`:10`) names two ground ids this lane
  holds nowhere (`grep -rn 'N14\b\|N20\b' corpus plans` → no rows), and the entry's load-bearing
  numbers (per-variable linear-weighted kappa 0.00–0.35, median 0.21 over 29 main-pass documents,
  `:25-29`) are not re-derivable from any lane byte, so its headline cannot be checked here.
  **Flip:** stage six fresh rows carrying the entry's real URLs, with `audit/PRE-REGISTRATION.md`
  pinned at `4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6` and captured; then admit it as its own entry
  and re-derive the kappa figures from the captured paper. The substance is worth carrying: a
  pre-registration frozen "2026-08-12, before any document in the frame was coded" is the sanction
  this lane's own freezes imitate, and a protocol whose measured coder agreement is median 0.21
  cannot arbitrate another programme's card design.
- **Assimilation: none.** One entry considered, refused; no canonical knowledge row is claimed from
  `merge/kengaku` this round.
- **Census.** Before: `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`
  → rc 0, **25** `W04` warnings and `ok` on `corpus/SOURCES.md`; capture
  `.ufo/waves/round-72/census-before.txt` (3285 bytes, mtime 23:01:27, sha256
  `5bbde4eee78cb5806484850cc0f00ac48e475f62226a9ddf57135ea0d989fcde`). The validator's stdout carries
  no row count, so the before count is the lane's own
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` on the pre-freeze tree: **238**, corroborated
  from committed bytes (`git show c6322972:corpus/SOURCES.md` through the same counter → `238`), with
  the two new rows landing in the freeze (`git diff --numstat c6322972 b6336136 -- corpus/SOURCES.md`
  → `2 0`). After: the same command at the freeze tip (`b6336136`) → rc 0, **240** rows (same
  counter), the same 25 `W04`, stdout **byte-identical** to the before capture (`cmp` rc 0, same
  sha256 `5bbde4ee…fcde`). No wave seat appends a row; the landing commit is the L1's and a re-run at
  that tip is owed (see Limits).
- **Admission status (QUALITY Q13/Q14): HOLD.** The entry
  `corpus/knowledge/tb2-hf-model-inference-provenance.md` (6849 bytes, 78 lines, sha256
  `e384eb34a1df54c09be2a3f80074130be8b98bfb5ec66fb81323b6cbb6a4b53e`) carries `admission: hold` and
  cites this lesson's `## Gate` as its record — at `KnowledgeIndexR72`'s audit that file did not
  exist (`ls` rc 2), so the citation was dangling until this draft, and this draft existing does not
  change the status. Q13 admits an entry only after a returned second-seat re-read cited by
  repo-relative path from a second-wave directory, and `plans/gate_timing_check.py:241-243` accepts
  only a directory named `falsify` or `wave[-_ ]?0*2`. `.ufo/waves/round-72/` held `w1` only at
  draft time, so no such seat exists; `python3 plans/gate_timing_check.py --lesson
  corpus/lessons/round-72.md --commit <tip>` is owed at the landing tip; round 71's precedent is
  `no admit rows … failed=1` when no second-wave report exists, and this round has none. The entry
  is landed and indexed (`corpus/README.md:96`; reciprocal row↔file check in `KnowledgeIndexR72.md`
  §3; the file is one of 72 knowledge files against 71 index rows, the one unindexed file being the
  pre-existing `tb2-torch-tensor-parallel-offline.md`).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **a control run invoked without `--control` produced a passing battery** | the L1's receipt at `/fast/scratch/hyaku/kengaku-r72/l1/c1-control.txt` (3494 B, mtime 23:03:21, sha256 `fa060b7f…4087`) is a full battery, not a control staging: nine `VECTOR … agree=True`, `:39` `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2`, `:40` `PREDICATE R72-C1 pass`, no `CONTROL` line; its bytes are **identical** to the receipt of record (`cmp` rc 0; `corpus/evidence/round72/hf/receipt.txt` sha256 `fa060b7f…4087`). The corrected control, `.ufo/waves/round-72/c1-control.txt` (3976 B, sha256 `16d78eae…93e7`), carries nine `derived=FFFF`, `SUMMARY … mismatches=9 setup=0 exc=18`, `LEG-COVERAGE legs=4 seen_p=0 seen_f=4`, `PREDICATE R72-C1 fail` | the `--control` flag's own requirement — `run_control` passes only when `derived_set == ["FFFF"]` and the last line ends `fail` (`plans/round72_c1_hf_probe.py:671-691`) — and the receipt's `SUMMARY` line, which a control cannot print with `mismatches=0` | re-run with `--control`; the claims' do-nothing paragraph (`plans/round-72-claims.md:70`) names the artifact. The `CONTROL cases=9 derived_set=FFFF predicate=fail counter_refuses_do_nothing=True` line is **stdout-only** (`:687`) and is not written into the receipt, so the file of record carries the nine `FFFF` vectors and `fail`; `C2ControlsR72.md` quotes the stronger run and its replicate is byte-identical to the wave file (`diff` rc 0) |
| **a green arm whose receipt was produced before the freeze** | `/fast/scratch/hyaku/kengaku-r72/l1/receipt.txt` (3494 B, mtime 22:57:20, sha256 `18ff2ec8…bf08`), `REV c6322972…` and `:6` `PROBE_BLOB sha256=unknown rev=c6322972…`: nine `VECTOR … agree=True`, `:39` `SUMMARY … mismatches=0`, and yet `:40` `PREDICATE R72-C1 fail`, because `battery_lines` requires `blob == probe_sha` (`plans/round72_c1_hf_probe.py:643`) and the probe was not yet committed at `HEAD`; the receipt of record prints `PROBE_BLOB sha256=99867c7f… rev=b6336136…`. Checked at the tip, the pre-freeze receipt draws `DEFECT probe-blob receipt={'sha256': 'unknown', …} want sha256=99867c7f…` from `check_receipt` (`:751-752`) — the item's record of that first check; this seat re-read the clause in source and did not re-run the check | `check_receipt`'s `PROBE_BLOB` and `probe-blob-rev` clauses (`plans/round72_c1_hf_probe.py:751-754`) and the receipt's own `PREDICATE` line | batteries run after the freeze commit; a receipt whose `PROBE_BLOB` is `unknown` is red even when its vectors are green. The frozen predicate's "at the round tip" is what makes this correct, not what makes the receipt usable |
| **a frozen kill-rule clause the checker never reads** | the claim fails on "a `PROVENANCE` line that is absent/duplicated" (`plans/round-72-claims.md:64-66`), but `check_receipt` reads only `prov_lines[0]` (`plans/round72_c1_hf_probe.py:768`) and never counts the lines; the receipt of record plus a second `PROVENANCE … env_cleared=False` line prints `DEFECTS n=0`, rc 0 (`ReceiptReviewR72.md` §2 attempt d, §4 F3) | `ReceiptReviewR72`, on the source read and a constructed receipt | successor probe refuses on `len(prov_lines) != 1`; the battery cannot emit two, so this round's evidence is unaffected. A rule a seat thinks is wrong is a finding, not an edit |
| **a set-equality name over a superset test** | `PROVENANCE … allowlist_seen=9/9` is computed as `set(env_keys) >= set(allow_names)` (`plans/round72_c1_hf_probe.py:611-613`) and cannot fall below 9/9 on an extra key; the live captures carry **11** keys — the nine allowlisted, plus `PWD` (bwrap's `--chdir`) and `TORCHINDUCTOR_CACHE_DIR` (created inside the sandbox during `from_pretrained`, value `/tmp/torchinductor_vgpnk`, which also names the host account through the read-only `/etc` bind). The numerator is one boolean, so it prints 9/9 or 0/9 and never a partial count (`C2ControlsR72.md` §F5) | `HfBatteryR72.md` §F1 (measured `env_keys` plus an import-attribution probe), reproduced independently by `HfReplicateR72.md` §F2, `SurfaceScoutR72.md` §F3.1, `ReceiptReviewR72.md` §4 F2 and `StubBeforeAfterR72.md` §F5 | successor prints `env_count=`/`extra_keys=` and renames the field `allowlist_present=9/9`; the isolation claim rests on `canary_seen=0`, which the extras do not weaken |
| **a round-72 knowledge entry written before the data it describes** | `corpus/knowledge/tb2-hf-model-inference-provenance.md` (mtime 23:01:58, before the 23:10 battery) **carried** three statements its own receipts contradict: `:34` "the sandbox's environment is exactly the `--setenv` list" (11 keys: `PWD` + `TORCHINDUCTOR_CACHE_DIR`), `:67` "five-file 19 KB fixture" (5 files, **13,944 bytes** = 13.6 KiB), and `:33-38` `env_cleared=True` listed under "why it is not self-report" while the emitter hardcodes the literal (`plans/round72_c1_hf_probe.py:614`) and `--check-receipt` only matches the literal (`:774-776`) | `SurfaceScoutR72.md` §F3.2 (the "exactly" sentence) and `KnowledgeIndexR72.md` §2.8, §2.11 (the witness framing, the 19 KB number); `C2ControlsR72.md` §F3 reaches the same conclusion from the instrument | the landing edit rewrote all three (entry diff `9 8` at draft close): the environment paragraph now says nine-plus-two, eleven keys, superset test; the fixture paragraph says 13,944 bytes; the witness table is re-headed "what backs it" with `env_cleared` no longer sold as sandbox-computed. The mechanism claims hold — the canary and the `/venv/` path are inside-sandbox observations |
| **a presence check read as an attribution check** | `E1b` passes when both revision tokens occur in the erratum, not when each is attached to the right artefact: an erratum with `c80fcdb3`/`d8a77d3f` **swapped** still prints `E1b ok`, `E2 ok`, `DEFECTS n=0`, rc 0 (`C2RedBeforeR72.md` §F1, probe P4). `E1a` is first-row-wins and duplicate-blind (`registry_rows`/`setdefault`): a second, 3-cell row for the same name appended **after** the valid row prints `E1a problems: []`, rc 0 (`:F2`, probes P1/P1b), and the check reads only the column count, entry cell, kind and owner of a row — the verdict-map, self-test, pinned-values and write-scope cells can be `GARBAGE` and `E1a` stays ok (`:F3`, probe P7). Independently, five junk erratum lanes (hollow, **opposite attribution**, code-only, original sentences deleted, non-git) and four wrong-row lanes (kind swapped, entry naming no command, duplicate rows, shadow rows) all print `DEFECTS n=0`, rc 0 (`ClaimFalsifyR72` §C2-d/§C2-e) | `C2RedBeforeR72`, constructed erratum and registry copies in scratch; `ClaimFalsifyR72`, five erratum fixtures and four row fixtures, the lane's gate run from the lane against byte copies | the predicate as frozen is still satisfied and the live erratum is factually correct (`c80fcdb3` control, `d8a77d3f` red-before, both re-checked with `git cat-file -e`), so this is calibration, not a claim failure. A successor gate binds revision↔artefact and refuses on a duplicate name |
| **registry rows that misstate the instrument's own exit contract** | of the four rows appended this round (`SKILL.md:695-698`), the audit finds **9 of 32 cells defective and no row conformant**: all four map a usage error to `2` while every script's `raise SystemExit("<message>")` exits **1** (`--selftest`/`--mutants`/`--control` without `--work` measured rc 1); both c1 rows' `0` cell says "mismatches … never the exit code" while the battery returns `0 if lines[-1].endswith("pass") else 1` (`plans/round72_c1_hf_probe.py:668`); both c1 rows' write scope omits `--receipt`, `--evidence-dir` and the fact that the sandbox runs `--share-net`; `round71-c1-hf-probe`'s self-test cell says "none declared" while the same row's entry cell lists `--selftest` and `run_selftest` exists (`:733`); the c1 `kind=probe` label rests on the false `0`-cell premise (`PROTOCOL.md:377-379` defines kind by failability) | `RegistryAuditR72.md` §3-§7 (flag sets match exactly; the cells that describe behaviour do not), corroborated by the live rc measurements in its §2 | the rows are rewritten against the scripts' real exit paths and write scope; the four flag-set cells are already correct and stay. This does not touch the frozen predicate, which checks presence/kind/owner only — and that gap is the calibration finding |
| **a registry-conformance gate bounded to a frozen list, closing an instance and not a class** | `E1a` iterates `INSTRUMENTS` = the four round-71/72 instruments (`plans/round72_c2_routed_defects.py:56-61`); a fifth kengaku instrument registered nowhere still prints `DEFECTS n=0` (`SiblingOverlapR72.md` §F1, `RegistryAuditR72.md` §F8). The mechanism of R71-R1 is measurable: `git show d8a77d3f:SKILL.md \| grep -c 'round71_c1_hf_probe'` → `0`, and the lane's older `plans/round52_c2_registry.py:29` advertises only `SCORECARD.md, SKILL.md, LOG.md, corpus/README.md`, so an instrument advertised only in a claims doc never enters `ADVERTISED`. At the tip that gate still prints `MISSING 5` and `PREDICATE R52-C2 fail` (`corpus/evidence/round72/registry-debt.txt`), including a five-column `round66_c1_tensor_probe` row at `SKILL.md:688` that the parser drops | `SiblingOverlapR72.md` §F1 and `RegistryAuditR72.md` §F7-F8, independently | the round report states R71-R1 as *this instance closed, class still open on the fifth instrument*; a successor derives the instrument set from `plans/*.py` entry points and repairs the five-column row. The two fleet instruments that already do this (tabi's `check-gate-registry.mjs`, tsukuroi's `check-registry-coverage.py`) are named by `SiblingOverlapR72` and uncited by the claim |
| **a mutation metric whose `null` conflates a deliberate no-op with a fixture-invisible weakening** | six fresh semantic mutants (one-label positional, kind whitelist, supersedes-wording, E1c word numeral, erratum length floor, row absence) were built and run: five are scored **`null`**, and on each bespoke fixture the mutated gate prints `DEFECTS n=0 / PREDICATE R72-C2 pass` on bytes the pristine gate reds (`GateMutateR72.md` §2, §3). Replacing the shipped comment-only `M7` with the one-label mutant reproduces the exact frozen line `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1` at rc 0 (`§4.1`). The verdict is also a function of the author-declared `target`: the same `M5` edit declared `target=E2` is `killed`, declared `target=E1a` is `survived` (`§5.1`, probe P1), and `escapes` does not require the pristine gate to refuse the fixture (`§5.2`, probes S1/S2) | `GateMutateR72`, against throwaway copies of the gate | the shipped six kills are real and the frozen line is satisfied; successor adds the five missing red fixtures, builds fixtures with the mutant's own builder, requires `pristine_vec[fx] != 0`, and derives `target` from the edited line. `null_detected=1` certifies "exactly one row flipped nothing", not "the null row is inert". The matrix is also template-closed — its green and red fixtures are the gate's own `claims_fixture()`/`registry_row()` templates — so it has no false-accept arm, which is why every junk lane above passes it (`ClaimFalsifyR72` §C2-f) |
| **a checker conjunct that no mutation can make decide** | two of the eight assigned clauses are `SURVIVED`, not killed: `M6` (K9 dropped from the case-set check) leaves every tested K9-less receipt refused anyway by `case-digest-unique`, the `--work` `case-digest` arm and the per-case vector loop; `M8` (`PROBE_BLOB`/`PROBE` equality ignored) is implied by the two independent bindings `probe-blob` and `probe-working-tree` (9/9 identical rc and defect codes in the enumeration). The matrix's own summary calls both "redundant, not load-bearing" (`corpus/evidence/round72/c1-counter-mutants.txt` §clause verdicts/§findings F1-F2) | `CounterMutateR72`, eight clause mutants plus attribution probes against a scratch copy of the instrument (`CounterMutateR72.md` §Result matrix, §F1/F2; raw in `corpus/evidence/round72/c1-counter-mutants.txt`) | a successor drops the two redundant conjuncts or gives each a fixture that can red only through it. The frozen predicate needs neither: it names `DEFECTS n=0` and the printed lines, not the clause inventory |
| **a freeze-doc count that is right only under an unstated exclusion** | claim limitation (vi) says "five assert groups remain red-unreachable"; the 12 unpriced asserts fall in **6** groups, of which 5 (10 sites) are priceable by server-mode cases and 1 (2 sites, `:19`, `:20`) is priceable only by the stub that the provenance witness exists to exclude. "Five" is right iff G1 is excluded, and the claim does not say so (`SurfaceScoutR72.md` §4a) | `SurfaceScoutR72`, re-deriving the 19-assert inventory from the pinned grader | the round report carries the exclusion; a successor's erratum says "five server-priceable groups plus one stub-only group". The claim is frozen and no seat edits it |

## Census

- Before: `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0,
  25 `W04` warnings, `ok …/corpus/SOURCES.md`; capture `.ufo/waves/round-72/census-before.txt`
  (3285 bytes, sha256 `5bbde4ee…fcde`). The validator's stdout carries **no row count**; the
  before-state row count is the lane's own
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` run in the same minute,
  **238** (the two round-72 rows S247/S248 did not exist yet; they were appended after this capture
  and land with the freeze).
- After: the same command at the freeze tip `b6336136` → rc 0, the same 25 `W04`, stdout
  `cmp`-identical to the before capture (both new URLs are fresh, so no new warning); the same
  `grep -cE` → **240**. A re-run at the landing tip is owed and is part of the L1's closing checks,
  not this seat's.
- Validator self-test: **not measured this round**. No seat ran `sh scripts/sources-census.sh
  selftest`; round 71's 96-`killed`/0-`survived` receipt stands as the last one.

## Verdicts

- **R72-C1: admitted, coverage held at its L0 cap (7), evidence-carried.** Receipt of record
  `corpus/evidence/round72/hf/receipt.txt` (40 lines, 3494 bytes, sha256 `fa060b7f…4087`): nine
  `VECTOR` lines, all `agree=True` (K1 `PPPP`, K2 `PPFP`, K3 `PPFP`, K4 `PPPF`, K5 `PFPP`, K6
  `PFFF`, K7 `FPPP`, K8 `FPPP`, K9 `PPPF`); `:38` `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`; `:39`
  `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2`; `:9` `PROVENANCE env_cleared=True allowlist=…
  nine names … allowlist_seen=9/9 cases=9 distinct=1 canary_seen=0
  transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py`; `:40`
  `PREDICATE R72-C1 pass`. The frozen checker prints `DEFECTS n=0` / `PREDICATE R72-C1 pass`, rc 0
  (`corpus/evidence/round72/hf/check.txt`, sha256 `0e63c73f…afe2`). The checker's trust boundary is
  measured, not merely declared: a hand-written receipt built from committed bytes with **no battery**
  passes (rc 0, ~5 s of staging), and so do five mutations of it — a `REV` and `PROBE_BLOB rev` at
  the base tip, a `PROBE_BLOB` naming a rev that does not contain the probe, a dropped `SANDBOX`
  line, a `transformers_file=/venv/DOES-NOT-EXIST/…` path, and a receipt whose `EXC K9 …=E` declares
  the L4 red an exception rather than the `:107` assert (`ClaimFalsifyR72` §C1-a). "At the round tip"
  is not a checked clause: `git_is_ancestor` accepts any ancestor. K9's mechanism is nonetheless
  unique among the frozen modes — only `400-no-error-field` returns a 400 whose body lacks `error`,
  and the real `run_case` reds `:107` while K4 reds `:103` (`§C1-b`; `HfBatteryR72` §K9) — and every
  leg's `F` has a genuine assertion witness, K6's two exceptions being extra (`§C1-c`). The
  replicate battery reproduces
  the receipt byte-for-byte (`diff` empty, both sha256 `fa060b7f…4087`; `HfReplicateR72` §3), and all
  nine `case_sha256` values re-derive from the committed fixture and grader through the probe's own
  `stage_case` and through an independently written tree hash (`HfReplicateR72` §4). The do-nothing
  control refuses: nine `derived=FFFF`, `seen_p=0`, `mismatches=9`, `PREDICATE R72-C1 fail`
  (`.ufo/waves/round-72/c1-control.txt`; stderr-free replicate by `C2ControlsR72`, `CONTROL cases=9
  derived_set=FFFF predicate=fail counter_refuses_do_nothing=True`, `diff` rc 0 against the wave
  file). The stub before→after is measured on one stub and one driver: the round-71 probe imports it
  (`test_model_downloaded` raises `RuntimeError: stub transformers` in all eight cases, six of eight
  derived vectors move, `SUMMARY cases=8 legs=32 mismatches=6`, `PREDICATE R71-C1 fail`), while the
  round-72 probe is blind (all nine `case_sha256` values change — the stub is present in every staged
  tree — yet 9/9 vectors equal the frozen table, `PROVENANCE … /venv/…`, `PREDICATE R72-C1 pass`)
  (`corpus/evidence/round72/hf/stub-before-v1.txt`, `stub-after-v2.txt`, `StubBeforeAfterR72` §"two
  tables"). The shipped control prints `STUB-CONTROL exposed=False vectors_unchanged=True`
  (`stub-control.txt:41`). The instrument's own selftest prints `SELFTEST red_refused=8/8 accept_ok=1
  state_sensitive=1 path_independent=1 ok=True`, with eight substantive refusal arms
  (`vector_flip`, `legs_flip`, `coverage_flip`, `drop_case`, `case_digest`, `drop_k9`,
  `provenance_env`, `provenance_path`; defect counts 4/1/1/5/1/5/2/2) and the genuine receipt accepted
  (`corpus/evidence/round72/c1-selftest.txt`, sha256 `e24edb70…f69b`). The checker's per-clause
  matrix kills 6 of 8 assigned clauses and finds `M6` (K9 in the case-set check) and `M8`
  (`PROBE_BLOB`/`PROBE` equality) redundant rather than load-bearing, and its receipt-side probes
  accept forged header digests and a duplicated `PROVENANCE` line
  (`corpus/evidence/round72/c1-counter-mutants.txt` §clause verdicts, §residual probes). No provenance attack
  succeeded: caller `PYTHONPATH`, an `/app` shadow, `BASH_ENV`/`PYTHONSTARTUP`/`PYTHONHOME`, and a
  write into the venv bind all fail, the last with `OSError: [Errno 30] Read-only file system`
  (`ProvenanceAttackR72`). K9 prices `tests/test_outputs.py:107` — `assert "error" in error_data` —
  which K4 (`:103`) cannot reach; the K9 manifest records `AssertionError: Error response should
  contain 'error' field` (`HfBatteryR72` §K9). Calibration: the ledger is at *leg* level and
  saturated (`legs=4 seen_p=4 seen_f=4` is byte-identical to round 71); the ninth case's advance
  exists only in per-case `detail` text and in the entry's 7-of-19 assert-site count, not in any
  receipt counter (`SurfaceScoutR72` §F2.2/F2.3); 7 of 19 assert sites are now priced (up from 6),
  12 unpriced in six groups, one group stub-only by design; K6's two `F` cells are escaped
  `ConnectionError`s recorded on `EXC`, so 36 leg-witnesses are 34 assertion-witnesses plus 2
  exception-witnesses; and `env_cleared=True` is a literal, so the isolation claim is carried by
  `canary_seen=0`, the `/venv/` path and the read-only bind, not by that field.
- **R72-C2: admitted, calibration held at ceiling (10), exercised — with the predicate's limits
  measured.** At the tip `python3 plans/round72_c2_routed_defects.py --lane .` prints `E1a ok`,
  `E1b ok`, `E1c ok`, `E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2 pass`, `EXIT=0` at `LANE_TIP
  b6336136` (`corpus/evidence/round72/c2-green.txt`, `RUN_AT 2026-11-04T02:09:18Z`; re-run by
  `C2RedBeforeR72` and by `KnowledgeIndexR72` §1 arm 3). The red before the correction is
  `DEFECTS n=6` — four `E1a row-absent` (both round-71 and both round-72 instruments) plus `E1b
  no-errata-section` and `E2 no-errata-section` — `PREDICATE R72-C2 fail`, `EXIT=1` at base
  `c6322972` (`corpus/evidence/round72/c2-red-before.txt`; a red-*data* run with the freeze
  instrument, since the gate script does not exist at base — rc 128). The corrections are strictly
  append-only: `git diff --numstat c6322972 master -- SKILL.md plans/round-71-claims.md` → `5 0` and
  `20 0`, 25 insertions, 0 deletions; the four eight-column rows sit at `SKILL.md:695-698`, and
  `plans/round-71-claims.md` keeps both superseded labels at `:59` and `:116` above `## Errata —
  round 72 (2026-11-03)` at `:137`, the file's last `##` section (`C2RedBeforeR72` §7-8). The
  selftest prints `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True
  positional-arm=True parser-arm=True ok=True`; the shipped matrix prints `MUTANTS total=7 killed=6
  survived=0 invalid=0 null_detected=1` and `ARM accept-green=ok refuse-red=ok attribution=ok`
  (`corpus/evidence/round72/c2-controls.txt`, sha256 `f8e7fa37…1bcd`; `--selftest` rc 0, `--mutants`
  rc 0). Read as discrimination rather than presence, the gate accepts a hollow erratum that quotes
  both labels and both revisions while saying "Nothing above is superseded … this block fixes
  nothing"; an erratum that states the *opposite* attribution; a lane where both original sentences
  are deleted; a non-git lane; and four rows whose kind, entry, verdict map and write scope are
  fabricated (`ClaimFalsifyR72` §C2-d/§C2-e, all rc 0 with `DEFECTS n=0`). Its mutant matrix is
  template-closed — the green and red fixtures are the gate's own templates — so it has no
  false-accept arm (`§C2-f`). The committed bytes are true and the two routed defects are closed
  *on the bytes*; "closed by a re-deriving gate" is the part the evidence does not carry.
  Calibration is bounded by measurement, not by the line. `E1b` is presence-only (a
  swapped-revision erratum passes) and `E1a` prices 3 of the 6 fields its sentence names and is
  duplicate-blind (`C2RedBeforeR72` §F1-F3). Five of six fresh semantic mutants are `null`, not
  `survived`, and `null_detected=1` is reproducible with a semantic weakening in place of the
  comment no-op (`GateMutateR72` §2-§4.1). The `ARM` line prints `accept-green=ok` and
  `attribution=ok` as literals, enforced only through `invalid=0` (`C2ControlsR72` §F1). The four
  rows that close R71-R1 are themselves defective in 9 of 32 cells and no row is conformant
  (`RegistryAuditR72` §4-§7), and the check is list-bounded: a fifth instrument still passes
  (`SiblingOverlapR72` §F1). Non-claim debt measured at the same tip: `python3
  plans/round52_c2_registry.py --lane .` prints `ADVERTISED total=110 REGISTERED total=105 rows=107
  MISSING 5` and `PREDICATE R52-C2 fail`, `EXIT=1` (`corpus/evidence/round72/registry-debt.txt`) —
  five pre-existing `plans/` instruments from rounds 66/69/70, identical at base and tip, outside
  this claim.
- **Axes.** Coverage: before 7, held at the L0 cap after — the move is evidence-carried (the
  provenance witness and K9), not a class-row move; `grep -c 'executed 4 of 8' SKILL.md` → `1` and
  `grep -c 'executed 3 of 8' SKILL.md` → `0` at the tip (`DepthGateR72.md`). Calibration: before 10,
  held at ceiling, exercised — the gate's own weaknesses are named above rather than scored as
  strength. Structural gates at the tip: depth `ROWS n=16 class_match=True count_mismatch=0 paths
  total=36 resolved=36 share=1.00`, `PREDICATE R63-C2 pass`; trio `SWEEP files=72 trio_open=43
  addendum=29 red=0`, `PREDICATE R64-C3 pass` (`corpus/evidence/round72/gates/depth-gate.txt`,
  `trio.txt`). The tracked modifications visible at draft close — `LOG.md`, `SCORECARD.md`,
  `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md` and the entry — are the integrator's landing
  edits (the same editor amended this lesson's `## Census` while it was being written); no wave
  seat's report claims a tracked write, every one naming only untracked evidence plus its report.

## Limits (named, not scored)

- **The C1 checker's clause matrix has two non-load-bearing clauses and three unbound digest lines.**
  `CounterMutateR72` (§"Result matrix"; evidence `corpus/evidence/round72/c1-counter-mutants.txt`)
  kills 6 of the 8 assigned clauses — `M1` provenance-absent, `M2` env_cleared, `M3`/`M3a`/`M3b`
  distinct and the `/venv/` path, `M4` canary_seen, `M5` allowlist_seen, `M7` library drift — and
  reports `M6` (K9 dropped from the case-set check) and `M8` (`PROBE_BLOB`/`PROBE` equality)
  **SURVIVED**: `M6` is a duplicate detector (`cases_ok` carries the same conjunct into the predicate,
  and `case-digest-unique`, the `--work` `case-digest` arm and the per-case vector loop each refuse a
  K9-less receipt), and `M8` is implied by `probe-blob` + `probe-working-tree` (9/9 enumeration pairs
  identical rc and defect codes). Its residual probes also accept a receipt whose `GRADER`,
  `INSTRUCTION`, `MODEL` and `SANDBOX` lines are forged (`P1`, rc 0 — three of the five printed
  digests are unbound, carried from round 71) and one carrying a duplicated `PROVENANCE` line
  (`P2`/`P3`, rc 0). Five further clauses (`M6c`, `M9`–`M12`) were built but `UNRUN` at wave
  wrap-up; the eight assigned clauses are fully measured and must not be read as more than that.
- **`corpus/evidence/round72/hf/check.txt` is an assigned receipt, not a stray.** `ReceiptReviewR72`
  §F4 calls it "a redirect slip by the battery/receipt seat"; the wave spec's `HfBatteryR72` item
  step 3 names that exact path for the check's stdout, so the 34-byte file is the check receipt of
  record and its sha256 is cited in §Verdicts. Reported here so the mislabel is not carried forward.
- **The receipts are untracked until the L1 commit.** At draft time `corpus/evidence/round72/` and
  `.ufo/waves/round-72/` are untracked; the digest bindings re-derive from `b6336136`, but the bytes
  become committed only with the landing commit (Q22 re-run owed at that tip).
- **`--check-receipt` is a consistency check, not run provenance.** A from-scratch forgery over the
  frozen table passes `DEFECTS n=0`, rc 0, and the `transformers_file` clause is a `/venv/`
  **prefix** test: `/venv/etc/does-not-exist.so` is accepted (`ReceiptReviewR72` §2 attempts b/b3,
  §4 F1; `ClaimFalsifyR72` §C1-a). Six further variants pass: a `REV`/`PROBE_BLOB rev` at the base
  tip ("at the round tip" is not a checked clause — `git_is_ancestor` accepts any ancestor), a
  `PROBE_BLOB` naming a rev that does not contain the probe, a dropped `SANDBOX` line, an
  unresolvable `/venv/DOES-NOT-EXIST/…` path, and an `EXC K9 …=E` that declares the `:107` red an
  exception. Run on a receipt produced **under an active stub injection**, the text-only arm passes
  it and only the `--work` arm fails, on all nine `case-digest` checks (`StubBeforeAfterR72` §F7),
  so the re-staged digests are the live witness against staged-tree tampering and nothing else in
  the text arm distinguishes a blind sandbox from a compromised one. Invoked without `--work`, the
  checker skips the nine digest re-stagings entirely (`ReceiptReviewR72` §4 F5).
- **The isolation claim rests on the canary, not on `env_cleared`.** `env_cleared=True` is a literal
  in the writer (`plans/round72_c1_hf_probe.py:614`); `canary_seen=0`, `distinct=1` and the `/venv/`
  path are computed from the in-sandbox harness's report — but that harness is the process under
  test self-reporting, so the witness is inside-out, not an outside observation of the child
  (`SiblingOverlapR72` §F2(ii); `C2ControlsR72` §F3 notes that dropping `--clearenv` *and*
  `canary_env()` would still print `env_cleared=True`). kama's `KAMA_R50_CANARY` arm reads
  `/proc/<pid>/environ` from outside for this reason.
- **`--clearenv` is a restoration, not a novelty.** The lane's round-64…67 probes already ran under
  `--clearenv` (`SiblingOverlapR72` §T5); round 71's probe dropped it and round 72 restores it. The
  round's new artefact is the provenance line, not the mechanism.
- **Host-state coupling.** `LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0
  requests=2.34.2` is re-derived against `/fast/ComfyUI/.venv` at every check; a venv upgrade would
  retroactively print `library-drift` on a genuine receipt.
- **The staged model is a five-file synthetic fixture** (`MODEL tree_sha256=c5c25767…8944`, 13,944
  bytes), not `distilbert-base-uncased-finetuned-sst-2-english`; the replay prices the grader's
  logic, not model accuracy.
- **`test_flask_api_running` accepts any HTTP answer** (grader `:29`); K5 prices the only failing
  mode a live listener can have.
- **K9 prices one assert site, not the leg.** 12 of 19 asserts are unpriced; five server-priceable
  groups (10 sites) and one stub-only group (`:19`, `:20`) — the claim's "five groups" is right only
  with the stub-only group excluded, which it does not state (`SurfaceScoutR72` §4a). The cheapest
  successor cases are specified there with their ordering guards; none is in this table.
- **The receipt cannot express the coverage move.** `LEG-COVERAGE` is saturated and identical to
  round 71; the receipt has no assert-site field, so `:107` is auditable only from
  `sandbox/K9/manifest.json` / `sandbox-stdout.txt` (`SurfaceScoutR72` §F2.3).
- **`SUMMARY` is prefix-matched, so `exc=` is unconstrained.** `check_receipt` requires
  `SUMMARY cases=9 legs=36 mismatches=0 setup=0` as a substring and never counts `exc`
  (`C2ControlsR72` §F4); the green battery's `exc=2` rides along, as the claim's own quotation does.
- **The server process is outside the import witness.** The staged server runs as `/app/server.py`,
  so its `sys.path[0]` is `/app`; a staged server that imported `transformers` would take
  `/app/transformers`. No leg prices server internals — a named residue of the isolation claim, not
  a falsification (`StubBeforeAfterR72` §F4).
- **Shared port 5000 is a one-case margin.** The `flock` is taken per case and `wait_port_free` caps
  at 20 s; a foreign listener holding the port turns a case into `SETUP`, which the kill rule scores
  as failure, not retry (`HfBatteryR72` §F5, `HfReplicateR72` §F6). Both batteries ran `setup=0`; the
  port was observed held by sibling sandboxes at 23:08-23:12.
- **Replicate identity is corroboration, not independent variation.** Staged digests are
  path-independent by design; two sequential runs at one tip are expected to be byte-identical
  (`HfBatteryR72` §F6, `HfReplicateR72` §F1). The control replicate is likewise byte-identical to the
  L1's file, so the receipt alone cannot distinguish a second execution from a copy
  (`C2ControlsR72` §F7).
- **R72-C2's gate binds no self-digest.** Unlike C1's `PROBE_BLOB`, `round72_c2_routed_defects.py`
  never digests itself against the commit, and `--mutants` mutates its own working-tree text; the
  runs here were sound because the tree was clean (`C2ControlsR72` §F6).
- **R72-C2's registry closure is list-bounded and its rows are defective.** `E1a` checks the four
  `INSTRUMENTS`; a fifth instrument registered nowhere still passes, the four rows carry 9/32
  defective cells, and the lane's older `round52_c2_registry.py` fails on five pre-existing misses
  (`registry-debt.txt`). The round report says *this instance closed*, not *class closed*
  (`SiblingOverlapR72` §F1, `RegistryAuditR72` §F7-F8).
- **"fixture matrix" is a label this lane has used since round 37.** Fleet-wide it has zero tier-A
  hits; the owned vocabulary is "mutant matrix". What R72-C2's variant adds is the counted,
  attributed no-op (`null_detected`), and `GateMutateR72` shows that token is weaker than its name
  (`SiblingOverlapR72` §F3).
- **The knowledge entry's admission is `hold`, not `admit`.** No `w2`/`falsify` directory exists at
  draft time; the Q13 second-seat re-read is not on record, and this lesson is not one.
- **Out of scope, as declared before data.** No model behaviour was measured; no live model endpoint
  was contacted; no sibling lane was written (`SiblingOverlapR72` is read-only across 21 lane trees);
  `merge/kengaku` assimilation is `none`.
