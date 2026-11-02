# Round 62 claims freeze (kengaku, 2026-11-02; a retry session — a prior round-62 attempt landed no work: no round-62 commit exists in the history and no round-62 path exists in the base tree, controls receipt `.ufo/waves/round-62/recon/base-controls.txt`)

Base `c55a3f8868f352280538cf7d786135d34ac6542f` (the round-61 non-author closure tip, admitted).
The round-61 carry-in's three status-neutral findings (R61-D1 the amendment-prose undercount,
R61-D2 the S225 gloss pointer/byte swap, R61-D3 the idealized EOL counts) are ADDRESSED FIRST
this round, folded into R62-C2's landing. Freeze discipline unchanged: this freeze is written
and committed BEFORE the round's scored run; plumbing is proven only against toys — the survey's
`--selftest` is green at the round-62 worktree (receipt `.ufo/waves/round-62/recon/selftest-worktree.txt`:
3/3 ok, `SELFTEST pass (rc=0 want_rc=0)`, SELFTEST-EXIT=0; toy population, no TB2 capture touched).
Instrument self-pin: `plans/round62_c1_class_survey.py` sha256
`9414af9c50c36d55553577f889e82e5b76796cc0ab6d18016e8eeb77551e85d6` at freeze (recorded in
`.ufo/waves/round-62/recon/land-hygiene.txt`, with CR-COUNT=0 on every landed byte).

Environment: WSL Ubuntu-24.04 (python 3.12.3, bwrap 0.9.0, git 2.56.0; uv/pytest absent — the
canonical counter environment preserved; no environment mutation this round). Measured on clean
WSL-native-fs clones; every exit label in a receipt is captured inside the runner script (the
r60 harness rule). Sources opened live this round (both staged and adopted BEFORE the scored
run): **S226** (the pin's top-level task tree via the GitHub git-trees API, capture
`corpus/evidence/round62/tb2-tree-2fd12b88.json`, sha256 `dd64bfb3…f0cd1`; the census's
denominator grounding) and **S227** (the WHATWG windows-1252 index re-opened live, sha256
`2c5fa192…60795` byte-identical to the S225 capture; the corrected-pointer superseding row that
discharges R61-D2). Both adopted through `plans/sources_adopt.py` (leg 1: registry=218 staged=2
collisions=0 malformed=0 duplicates=0 defects=0, exit 0; leg 2: quotes 4/4 located+bound, exit 0;
pure byte append 274→276 lines, CR 0→0 — the r61 EOL rule honored; receipt
`.ufo/waves/round-62/recon/sources-adopt-run.txt`).

## R62-C1 / coverage (lowest owned axis, L0-capped) — the population's first grader-class census: the survey pass the planned round-62 section required before any eighteenth-grader claim

The planned round-62 text (SCORECARD): "an eighteenth grader only if a NEW grader class is found
in the 89-task population (the signal class was the last obviously-new mechanism in a first
sweep; remaining classes need a survey pass before any claim)". This round lands that survey
pass as a mechanized instrument and a receipt: the committed round-52 capture population is
byte-verified against its pinned SHA256SUMS, every committed `test_outputs.py` grader is
classified over a frozen detector table, and the census plus the executed-coverage cross-tab are
priced in a receipt the eighteenth-grader gate can read.

**Instrument** `plans/round62_c1_class_survey.py` (new file; stdlib-only, deterministic — every
output line sorted, a built-in determinism leg re-runs the census and requires byte-identical
output; read-only over the lane except its optional `--receipt` path). Population of record: the
committed `corpus/evidence/round52/graders/` tree (SHA256SUMS 184 pinned rows; EXCLUDED.md's one
pinned-but-absent capture; all_tasks.lst the 89-task roster; executed17.lst the 17 executed
tasks) plus the committed round-62 pin-tree capture `corpus/evidence/round62/tb2-tree-2fd12b88.json`
(S226). Invariants (each printed when it fails): sha-mismatch=0 over all committed captures;
captures-unpinned=0; the only pinned-but-absent row is exactly the EXCLUDED path; roster==tree
(the 89-task roster equals S226's live-opened dir set name-for-name); every roster task has a
grader dir; executed17 ⊆ roster; every executed grader classified; the roster holds 89 tasks;
the sentinel: `signal-delivery` count=1 member=`cancel-async-tasks` (the r59/r61 prose negatives
re-derived mechanically from committed bytes). Exit map: 0 pass (all invariants + determinism) |
1 fail (INVARIANT-FAIL lines printed) | 2 setup (missing population — never a vacuous pass).

**The detector table is frozen here, before the scored run (16 classes, each named by what its
regex literally matches, multi-label):** signal-delivery (`send_signal(`); subprocess-exec
(`subprocess.run|Popen|check_output|check_call|call(`); shell-exec (`os.popen(|os.system(|commands.getoutput(`);
candidate-import (`import attack|solution` at line start / `sys.path.append(`); file-artifact
(`.exists()|.read_text(|.read_bytes(|.is_file()|.is_dir()|open(`); stdout-inspection (`.stdout`);
numeric-band (`pytest.approx|math.isclose|np.allclose|abs(...)</>`); crypto-credential
(`hashlib|sha1|sha256|md5|openssl|gpg|hmac`); network-service (`socket.|requests.get/post|urllib|
http.client|urlopen|localhost:N|127.0.0.1`); timing-wall (`time.monotonic|time.perf_counter|elapsed|time.time(`);
filesystem-metadata (`os.stat|st_mode|os.chmod|os.geteuid|is_symlink|getsize|getmtime`);
process-environment (`os.environ|/proc/`); git-plumbing (quoted `git`); db-state (`sqlite3|postgres|mysql`);
serialization-schema (`json.load(s)|yaml.safe_load|tomllib|xml.etree`); container-image
(`docker|podman`).

**The table's own pre-freeze catch (the survey machinery working):** take 1 of the pre-freeze
dry run (receipt `.ufo/waves/round-62/recon/census-dryrun-worktree.txt`, kept AS-IS with take 2
beside it) priced the first table RED — the executed `feal-differential-cryptanalysis` grader
was UNCLASSIFIED (its mechanism is grader-imports-candidate plus an `os.popen` build step; the
first table had no detector for either; `INVARIANT-FAIL every-executed-grader-classified`,
PREDICATE R62-C1 fail, exit 1). The table was amended BEFORE the freeze (shell-exec and
candidate-import added; `.read_bytes(` added to file-artifact), the selftest re-proven green,
and take 2 of the dry run is all-green. The frozen table is the take-2 table; the frozen
instrument is sha `9414af9c…85d6`.

**Survey numbers fixed by the take-2 dry run at the worktree (the scored run re-derives them at
the freeze tip):** roster=89 == tree-dirs=89; sha256sums-rows=184; captures-committed=183;
captures-unpinned=0; sha-mismatch=0; absent-pinned=1 (exactly the excluded capture);
graders-classified=93; unclassified=0; classes=16. Census: file-artifact 76, subprocess-exec 45,
stdout-inspection 29, crypto-credential 12, numeric-band 10, filesystem-metadata 10,
serialization-schema 10, timing-wall 9, network-service 8, shell-exec 6, candidate-import 6,
process-environment 3, git-plumbing 3, db-state 2, signal-delivery 1, container-image 0.
SENTINEL signal-delivery count=1 member=cancel-async-tasks. EXECUTED-COVERAGE executed=17
classified=17 classes-covered=12 classes-uncovered=network-service,process-environment,
db-state,container-image — the eighteenth-grader gate's survey input: the only uncovered classes
with population members are network-service (8 graders), process-environment (3) and db-state
(2); container-image has no members in the population.

- BEFORE (base `c55a3f88`, measured controls in `.ufo/waves/round-62/recon/base-controls.txt`):
  the instrument, the tree capture, the re-open capture and the knowledge entry are ALL absent
  (`git cat-file -e` rc=128 ×4); the PROVINCE frontier anchor `^## Round 62` counts 0 at base and
  `CLASS-CENSUS` counts 0 in PROVINCE at base; SOURCES rows = 218; the census cannot run at base
  (its own file absent — the do-nothing control's red).
- AFTER (the freeze tip and the scored run): the census runs on a fresh clean WSL-native-fs
  clone at the freeze tip — every capture byte sha-verified, all 93 graders classified, every
  invariant green: `PREDICATE R62-C1 pass`, exit 0 (receipt of record
  `corpus/evidence/round62/class-survey.txt`, written OUTSIDE the measured clone); PROVINCE
  gains the round-62 section (`^## Round 62` 0→1); the knowledge entry
  `corpus/knowledge/tb2-grader-class-census.md` + its README index row land; the SKILL registry
  row `round62-c1-class-survey` + the entrytruth ledger row + the capability row
  `grader-class-census-survey` register the instrument (registration in the same commit as the
  SCORECARD section, the r58 lesson-3 rule); SOURCES 218→220 (S226+S227, both opened live this
  round).
- Score: **coverage HELD at 7** — the standing unanswered L0 cap `kengaku | round-25/33/51`
  (nothing assumed answered); the ground moves (the population's mechanism-class structure is
  now a mechanized, receipt-priced surface, and the class-line claims of r59/r61 are
  command-re-derivable instead of prose-negative), the capped number does not (the r56–r61 held
  shape).

Claim-sizing (§9): a do-nothing control cannot reach this — the instrument and every C1 artifact
are absent at base (rc=128 ×4); the census requires the instrument to run with sha-verification
green over all 183 committed captures, the roster==tree identity against the live-opened pin
capture, and the sentinel invariant met; the do-nothing round leaves the class structure
unpriced and the eighteenth-grader gate without its required survey pass.

## R62-C2 / calibration (held at ceiling 10, exercised) — the three round-61 closure findings land as dated corrections with re-deriving receipts

The round-61 non-author verifier spot-check (§6) routed three status-neutral findings; all three
land this round, addressed first:

- **R61-D1** — Amendment 1's defect-3 prose (and the round-61 lesson's freeze-transcription row)
  said ONE hand-transcribed row while the cited receipt's own diff shows THREE differing lines
  (the separator row 8-vs-9 cells, sequential-sync, no-max-enforcement; both data rows already
  wrong at the freeze; no scored run affected). Landed: the dated correction section appended to
  `plans/round-61-claims.md` (heading carries "dated correction", so
  `plans/correction_command_check.py` prices its commands at every future tip) and the dated
  erratum appended to `corpus/lessons/round-61.md`; the receipt stays as captured (R1). The
  corrected count re-derives: `grep -cE '^[0-9]+c[0-9]+$' .ufo/waves/round-61/recon/table-identity.txt`
  → 3.
- **R61-D3** — the lesson's EOL counts were idealized narrations. Measured this round from the
  git objects (receipt `.ufo/waves/round-62/recon/carryin-facts.txt`, runner-captured): base
  272 lines / 0 CR; freeze 274 lines / 274 CR (+274/−272 numstat = 546 changed lines — the
  row's "546" matches the numstat total, its "273-line" idealized 272→274); repair pure LF 0 CR,
  net +2/−0. The spot-check's variant fragment ("+274/−237 = 511") could not be re-derived by
  this round's numstat and is superseded by the measured numbers. Landed in the same two dated
  appends.
- **R61-D2** — the S225 gloss swapped pointer and byte for the 0xE2 mapping. Landed as the
  superseding registry row **S227** (teaches opens `supersedes S225 —`, per Q34 — S225's own
  cells stay byte-identical), adopted through the gate with a live re-open (sha `2c5fa192…60795`,
  byte-identical to the S225 capture; the re-open capture committed at
  `corpus/evidence/round62/whatwg-windows1252-reopen/index-windows-1252.txt`). Counters:
  `grep -c 'supersedes S225' corpus/SOURCES.md` → 1 (0 at base) and
  `grep -c 'R61-LESSON-ERRATUM-62' corpus/lessons/round-61.md` → 1 (0 at base).

- BEFORE (base `c55a3f88`, measured controls in `recon/base-controls.txt`): `supersedes S225`
  counts 0 in SOURCES; `R61-LESSON-ERRATUM-62` counts 0 in the lesson; no dated-correction
  section exists in `plans/round-61-claims.md`; the wrong gloss token `pointer 226 byte 0xE2`
  counts 1 in SOURCES (it STAYS 1 after the correction — S225 is immutable under Q34; the
  corrected state is the superseding row, not an edit).
- AFTER (the freeze tip): all three counters at 1; `plans/correction_command_check.py` prices
  the claims doc's dated-correction section green at the tip (exit 0); the receipt gate
  (`plans/receipt_consistency_check.py`) stays green over the round's receipts; the registry's
  byte hygiene holds (CR=0 through the append).
- Score: **calibration HELD at 10, exercised** — external catches are owned and corrected where
  the evidence demands, by dated appends whose commands keep re-deriving (R12), with the
  defective original text preserved as history (R1/Q34), not papered over or silently rewritten.

Claim-sizing (§9): a do-nothing control cannot reach this — at base all three correction
counters read 0 and the wrong gloss stands uncorrected; the do-nothing round leaves the routed
carry-in unaddressed and the gates unpriced.

## Separability, sources, L0, exploratory

- R13 separability: C1 and C2 share no artifact but this claims doc — C1's artifacts are the
  instrument, the tree capture, the census receipt and the knowledge/PROVINCE/registry landing;
  C2's are the two dated errata appends and the superseding registry row. Either verifies
  without the other having landed.
- Sourced claims: C1 rests on **S226** (the pin-tree roster, opened live this round — the
  census denominator grounding; roster==tree is priced by the instrument); C2 rests on **S227**
  (the re-opened windows-1252 index — the pointer-98 line grounds the corrected gloss).
- Exploratory claims: none this round; both claims carry counting commands in receipts.
- L0: the coverage cap trio `kengaku | round-25/33/51` and the `kengaku | round-56` pair stay
  open; routed around; nothing assumed answered (the cap is why C1's score is HELD, not raised).
