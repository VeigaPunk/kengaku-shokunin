# R46ConnSibling — Sibling Overlap Scan

- **Seat:** `R46ConnSibling` (connector, leaf member)
- **Round:** kengaku round 46 (hyaku run 9, 2026-10-27), wave 1 (build / pre-data attacks)
- **Lane repo:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
- **Frozen claims:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-46-claims.md`
- **Axes:** Primary: **adjacency** (judged axis). Secondary: **calibration**, **depth**, **coverage**.
- **Receipts & Scan Table:** `.ufo/waves/round-46/w1/R46ConnSibling/sibling-scan-hits.tsv` (SHA-256 `25b9aa567b2b554e79a5e31160c5647235a255e32f9f391d5cc292b4c74e10e0`)

---

## 1. Scope and Method

This seat conducts a read-only sibling-overlap audit across all 20 sibling repositories in the fleet under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kengaku-shokunin` and typo clone artifact `kengaku-shokukin`).

The audit targets the three core surfaces of Round 46:
1. **Surface 1 (C1 Calibration):** Fixture fence / sandbox decision-procedure counter (`plans/fixture_fence.py`, contract `breach(d: pathlib.Path, argv: list[str], tool: str) -> str|None`, `plans/round46_c1_verify.py` with Q39 name hiding, bwrap isolation, strace log protection, and open/stat/readlink boundary auditing).
2. **Surface 2 (C2 Depth):** Anchor-line or quote-location check over `corpus/SOURCES.md` rows (`plans/anchor_line_check.py`, validating line `:N`, range `<file>:<a>-<b>`, word count `(<K> words)`, and capture sha256 binding under QUALITY Q34 supersede discipline).
3. **Surface 3 (C3 Coverage):** Terminal-Bench grader knowledge entry for `polyglot-c-py` or dual-runtime execution (`corpus/knowledge/tb2-polyglot-c-py-grader.md`, dual-toolchain execution via gcc and python3, pre-build directory listing check).

---

## 2. Findings by Surface

### Surface 1: Fixture Fence / Sandbox Decision-Procedure Counter

1. **`souji-shokunin/PROVINCE.md:101-105`**
   - **Located Quote:** “The census must refuse credential-store roots, ancestor roots and known aliases before enumeration; this is a refusal fence” (`:101–103`, 19 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `souji` established the fleet precedent for a "refusal fence" in repository census operations, guarding credential roots, ancestor directories, and git metadata (symlinks, alternates, attributes). However, souji's fence protects against repository traversal into ambient credentials. Kengaku's `fixture_fence.py` evaluates an adversarial fixture's internal git store and tool invocation arguments to determine whether a declared test fixture stays contained inside its assigned directory `d`. Kengaku's `PROVINCE.md` previously cited souji's boundary; kengaku should continue to cite souji's refusal-fence precedent without absorbing souji's repository-cleanliness or credential domain. No report-out needed.

2. **`souji-shokunin/census/round-32/c2-counter.py:10-25` (documented in `souji-shokunin/SKILL.md:257-261`)**
   - **Located Quote:** “run inside `bwrap --dev-bind / / --ro-bind <empty> /tmp ...` so any attempt to create a path under /tmp ... fails” (`:13–15`, 20 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `souji`'s `r32-c2-counter` and `r33-c2-counter` evaluate tool compliance with the host scratch discipline by running tools inside bubblewrap (`bwrap`) containers while tracing file-creation syscalls via `strace -f` (`mkdir,creat,open,openat`). While both counters use `bwrap` and `strace -f`, souji's check is a conformance gate testing whether benign tools leak temporary files into `/tmp`. Kengaku's C1 counter `plans/round46_c1_verify.py` tests adversarial fixture discovery, verifying that `fixture_fence.py` detects hostile git structures (includeIf, symlinks, argv env, commondir) while preventing fence bypasses B1–B6 under Q39 randomized name tokens. Cite souji as bwrap/strace scratch-isolation precedent. No report-out needed.

3. **`tameshi-shokunin/tools/trace-inputs.py:1-55`**
   - **Located Quote:** “Runs ARGV under `strace -f` tracing only file-open/exec/chdir/dup syscalls, passes the command's stdout/stderr through, and writes a JSON receipt” (`:2–5`, 20 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `tameshi` owns generic command input tracing (`schema: tameshi-trace-inputs-v1`) using `strace -f` with seccomp-bpf, `strace -y` path resolution, and C-unescaped path handling, classifying opened files into tracked `inputs`, `untracked`, `external`, and `live_lane_reads`. Kengaku's C1 counter utilizes similar low-level syscall tracing mechanics (`strace -f -y`), but applies them specifically to verify whether `fixture_fence.py` breached containment by reading files outside `d`. Kengaku should cite `tameshi`'s syscall-tracing and receipt-recording craft while keeping the fence contract in-lane. No report-out needed.

4. **`tameshi-shokunin/PROVINCE.md:3-11,28-38`**
   - **Located Quote:** “Domain: verification-fixture craft — the reusable method of honest checks: hermetic suites, mutation testing, fail-closed arms, verdict-line discipline” (`:3–5`, 18 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `tameshi` owns the reusable verification method across the fleet (mutation testing, hermetic suites, fail-closed arms). Kengaku's battery of honest fixtures (`battery42`, `battery43`, `battery44`) and refusal modules (`refusals45`, `refusals46`) are Kengaku-local product surfaces evaluating model/tool containment, not a generic mutation framework. Kengaku's C1 counter docs should cite tameshi's methodology without claiming fleet-level method ownership. No report-out needed.

5. **`tsukuroi-shokunin/tools/score-selftest-mounts-r41.py:1-46`**
   - **Located Quote:** “one DECOY variant is the unmutated arm plus a dead here-document ... inside probe_storage_arm that carries every mutant's replacement text verbatim” (`:9–13`, 21 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `tsukuroi` confronted `R40-ANSWER-KEY`, where a selftest inspected its own source code via `declare -f` or `$0` rather than testing actual fixture behavior. Tsukuroi addressed this with dead here-document decoys. This directly parallels Kengaku's QUALITY Q39 anti-cheating mandate in C1: the round-45 counter was bypassed by fences keying on fixture directory names (`control-c1-fence-keyed_name.txt`), leading to Round 46's randomized `secrets` tokens and shuffled execution. Kengaku should cite tsukuroi's anti-cheating decoy precedent in its counter documentation. No report-out needed.

---

### Surface 2: Anchor-Line or Quote-Location Check Over SOURCES Rows

6. **`chousa-shokunin/tools/quote-reopen.py:1-34`**
   - **Located Quote:** “looks each `source_id` up in the lane registry ... fetches each registry URL once per run, extracts the page text ... reports one verdict” (`:8–12`, 22 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `chousa` implements `quote-reopen.py`, an automated verifier that reads `corpus/SOURCES.md`, performs HTTP GET requests to live source URLs, strips markup, and checks whether cited quotes appear verbatim within a 25-word bound (`MAX_WORDS = 25`). While both tools verify located quotes, chousa's tool tests live remote web pages over HTTP; it does not check git-tracked local capture files under `corpus/evidence/`, does not verify line numbers (`:N`), and does not validate line ranges (`<a>-<b>`). Kengaku's `anchor_line_check.py` is an offline gate tool verifying capture line placement and word counts. Cite chousa's verbatim quote checking as remote-source prior art. No report-out needed.

7. **`chousa-shokunin/tools/build-spans.py:1-31`**
   - **Located Quote:** “Input: TSV header `id url quote entry` ... Each written row prints `QUOTE <id> char <N> <span_file>`, N = offset + the quote's position” (`:19–24`, 22 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `chousa`'s `build-spans.py` derives span manifests from quote tables and enforces character offsets (`char N`) into defined capture text forms (`.raw` / `.txt`). Chousa's `corpus/SOURCES.md` anchor cells use these character offsets (e.g., `S130: cover block (char 11, char 103, char 129)`). Kengaku's convention uses 1-based physical line numbers (`:N`), line ranges (`<a>-<b>`), and word counts (`(<K> words)`). Both enforce mechanical anchoring, but on different coordinate systems (character offset vs line number). Cite chousa's span offset model as adjacent anchor verification. No report-out needed.

8. **`kumitate-shokunin/scripts/sources-check.mjs:1-45, 271-286`**
   - **Located Quote:** “sources-check.mjs — validate the lane's curated source registry and its knowledge-entry citations (contract `kumitate-sources-v1`). Reads only `corpus/SOURCES.md`” (`:3–7`, 20 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `kumitate`'s `sources-check.mjs` validates the structure and schema of `corpus/SOURCES.md` (11 columns, non-empty cells, tier/status/date enums, used-by links). However, for the `anchor` cell, it only verifies `ROW_FIELD_EMPTY` (`:286`). It does not parse the internal anchor syntax (`commit <sha>, <file>:<a>-<b>, :<N> "<quote>" (<K> words); sha256 <hash>`), does not read capture files, and does not test quote alignment on line N. Kengaku's `anchor_line_check.py` operates as an orthogonal, deeper content checker. Cite kumitate's tool as registry structural validation prior art. No report-out needed.

9. **`kumitate-shokunin/scripts/cite-check.mjs:1-86`**
   - **Located Quote:** “cite-check.mjs — mechanical citation re-verifier ... Re-resolves every path / line / symbol / pin citation written in `SKILL.md` and `corpus/**/*.md`” (`:3–7`, 21 words).
   - **Classification:** **adjacent**
   - **Disposition:** **cite**
   - **Analysis:** Sibling `kumitate`'s `cite-check.mjs` re-resolves in-text file and line citations (`:N`, `:N-M`, `«…»` quotes, symbol bindings) across markdown prose, checking `LINE_OOR` and `SYMBOL_OFF_LINE`. However, it does not inspect `corpus/SOURCES.md` table anchor cells or verify quote substrings against captured blobs. Cite as in-text markdown citation verification precedent. No report-out needed.

10. **`tameshi-shokunin/corpus/knowledge/r44-anchor-refresh-rule.md:1-43`**
    - **Located Quote:** “A stale `anchor` cell ... is therefore repaired by a **new supersede row**, never by editing the old row's anchor cell in place.” (`:11–13`, 22 words).
    - **Classification:** **adjacent**
    - **Disposition:** **cite**
    - **Analysis:** Sibling `tameshi` established the fleet's normative rule for anchor-cell drift: per `CORPUS.md` rule 2, the registry is append-only, so when an anchor cell's digest or location drifts, it must be superseded by a new row starting `supersedes S0NN —` under QUALITY Q34, preserving immutable history. Kengaku's C2 depth claim strictly follows this discipline: rather than editing round-45 defective rows S108 and S149–S156 in place, Kengaku mints superseding rows S157–S165. Kengaku should cite tameshi's entry as the governing authority for its Q34 supersession structure. No report-out needed.

11. **`tsukuroi-shokunin/tools/check-adjacency-anchors.py:1-40, 203-208`**
    - **Located Quote:** “quote_line = OWNERSHIP_PIN['quote_line'] ... or quote_line > len(source_lines) or OWNERSHIP_PIN['quote'] not in source_lines[quote_line - 1]” (`:204–208`, 18 words).
    - **Classification:** **adjacent**
    - **Disposition:** **cite**
    - **Analysis:** Sibling `tsukuroi`'s `check-adjacency-anchors.py` checks adjacency tables in `PROVINCE.md` (`OUT-###`, `IN-###`), verifying that `quote` is a verbatim substring of `source_lines[quote_line - 1]` in the pinned snapshot. This is the exact 1-based line-substring logic implemented by Kengaku's `anchor_line_check.py` (`line` leg), but tsukuroi applies it to `PROVINCE.md` adjacency tables rather than `corpus/SOURCES.md` registry rows. Cite tsukuroi's tool as the closest mechanical precedent for line-indexed quote substring verification. No report-out needed.

12. **`tsukuroi-shokunin/tools/check-exec-environment-r40.py:22-28, 305-318`**
    - **Located Quote:** “lo, hi = int(a1), int(a2 or a1) ... body = collapse(' '.join(srcl[want][lo - 1:hi])) ... if 4 <= len(qc.split()) <= 25 and qc in body: quote_ok = True” (`:309–314`, 24 words).
    - **Classification:** **adjacent**
    - **Disposition:** **cite**
    - **Analysis:** Sibling `tsukuroi`'s `check-exec-environment-r40.py` validates quotes in knowledge-entry table cells against line ranges `A..B` in frozen source snapshots. This mirrors `anchor_line_check.py`'s `range` leg (confirming that the cited line `:N` falls within the range `<a>-<b>`). Cite tsukuroi's tool as precedent for range-bounded quote verification. No report-out needed.

13. **`mado-shokunin/quality/check-locators.py:1-43`**
    - **Located Quote:** “finds every locator token `<name>:<N>[-<M>]` ... and decides whether the cited receipt lines actually carry the identifiers of the fragment” (`:4–8`, 21 words).
    - **Classification:** **adjacent**
    - **Disposition:** **cite**
    - **Analysis:** Sibling `mado`'s `check-locators.py` validates line-range tokens in prose markdown against receipt files in `--fetch DIR`. It confirms that cited line numbers carry the relevant code identifiers. Cite as receipt line-range checking prior art. No report-out needed.

14. **`scripts/sources-census.sh:610-675` (Fleet Root Script)**
    - **Located Quote:** “id=trim($2); source=trim($3); kind=trim($4); tier=trim($5); scope=trim($6); anchor=trim($7); teaches=trim($8); status=trim($9)” (`:627–628`, 16 words).
    - **Classification:** **adjacent**
    - **Disposition:** **cite**
    - **Analysis:** The authoritative fleet-wide validator `sources-census.sh validate` parses all 11 columns of `corpus/SOURCES.md` across every lane, enforcing E01–E12 and W01–W04. However, it treats the `anchor` cell as an opaque string (only checking for non-empty field, escaping, and pipe formatting). Kengaku's `anchor_line_check.py` does not compete with or replace `sources-census.sh`; it acts as an in-lane gate verifying the internal truth of the anchor cell against physical capture files. Cite `sources-census.sh` as the fleet schema baseline. No report-out needed.

---

### Surface 3: Terminal-Bench Grader Knowledge Entry (polyglot-c-py or Dual-Runtime)

15. **`kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29, 53, 83`**
    - **Located Quote:** “Terminal-Bench (2 tools): Independent +1.7% (0.350) vs SAS 0.344, Centralized −19.2% (0.278)” (`:29`, 14 words).
    - **Classification:** **different**
    - **Disposition:** **ignore**
    - **Analysis:** Sibling `kumitate`'s entry cites a published academic paper (Kim et al.) evaluating multi-agent orchestration topologies across benchmarks including a 20-instance subset of Terminal-Bench. Kumitate does not read, execute, probe, or audit Terminal-Bench task graders. This was already adjudicated in Round 37 as a coordinator-topology data citation (`kengaku-shokunin/PROVINCE.md:352–356`). No overlap with Kengaku's C3 grader audit.

16. **`audio-shokunin/reports/frontier/fa-sndfile.md:59`**
    - **Located Quote:** “labels the hcom-polyglot as WAV; no HCOM in build — no fork” (`:59`, 12 words).
    - **Classification:** **different**
    - **Disposition:** **ignore**
    - **Analysis:** Sibling `audio` uses the term "polyglot" to describe audio files containing dual-format container headers (e.g., RIFF/WAV and HCOM/ACT headers recognized by `libsndfile` and `sox`). This is domain-specific audio transcoding, entirely unrelated to software benchmark execution or dual-runtime source code grading.

17. **`game-dev-2d-shokunin/reports/round-102/r102-w1.md:68`**
    - **Located Quote:** “head-ELF polyglot script ... `/var/tmp/r102-w1/fhe_e0/embed.x86_64` (starts `\x7fELF;echo…`)" (`:68`, 11 words).
    - **Classification:** **different**
    - **Disposition:** **ignore**
    - **Analysis:** Sibling `game-dev-2d` discusses executable ELF / shell script polyglots in the context of engine binary embedding and asset smuggling. This is game engine binary packaging, having no connection to LLM benchmarks, dual-runtime execution verification, or Terminal-Bench graders.

---

## 3. Sibling Adjacency and Routing Summary

| Topic / Surface | Sibling Hit | Owner | Class | Kengaku Routing / Action |
|---|---|---|---|---|
| **C1 Fixture Fence** | `souji-shokunin/PROVINCE.md:101` | souji | adjacent | **cite**: souji owns git-metadata/credential refusal fence; kengaku's fixture fence is an adversarial git-fixture boundary decision procedure |
| **C1 Sandbox Verification** | `souji-shokunin/census/round-32/c2-counter.py:10` | souji | adjacent | **cite**: souji owns bwrap/strace scratch boundary auditing on tools; kengaku's C1 verifies adversarial fixture discovery |
| **C1 Syscall Input Tracing** | `tameshi-shokunin/tools/trace-inputs.py:1` | tameshi | adjacent | **cite**: tameshi owns reusable command input tracing via strace -f; kengaku's fence is a lane-local fixture containment decision procedure |
| **C1 Fixture Craft Method** | `tameshi-shokunin/PROVINCE.md:3` | tameshi | adjacent | **cite**: tameshi owns reusable fixture/mutation method; kengaku's fixture fence and battery are lane-local product surfaces |
| **C1 Counter Anti-Cheating** | `tsukuroi-shokunin/tools/score-selftest-mounts-r41.py:9` | tsukuroi | adjacent | **cite**: tsukuroi owns anti-cheating decoy precedent; adjacent to kengaku's Q39 per-run random name token hiding |
| **C2 Live Remote Quote Reopen** | `chousa-shokunin/tools/quote-reopen.py:7` | chousa | adjacent | **cite**: chousa checks live remote URLs; kengaku's `anchor_line_check.py` checks offline git-tracked capture lines and word counts |
| **C2 Character Offset Anchors** | `chousa-shokunin/tools/build-spans.py:19` | chousa | adjacent | **cite**: chousa verifies char offsets `char N`; kengaku verifies physical line `:N`, range `<a>-<b>`, and word counts |
| **C2 Registry Schema Gate** | `kumitate-shokunin/scripts/sources-check.mjs:3` | kumitate | adjacent | **cite**: kumitate validates SOURCES.md structure/fields; kengaku checks internal anchor quote placement against captures |
| **C2 Prose Citation Re-verifier** | `kumitate-shokunin/scripts/cite-check.mjs:3` | kumitate | adjacent | **cite**: kumitate checks prose line/symbol references; does not check SOURCES.md table anchor cells |
| **C2 Anchor Drift Supersession** | `tameshi-shokunin/corpus/knowledge/r44-anchor-refresh-rule.md:9` | tameshi | adjacent | **cite**: tameshi documents fleet rule for Q34 supersede rows on anchor drift; kengaku strictly implements it for S157–S165 |
| **C2 Adjacency Line Substring** | `tsukuroi-shokunin/tools/check-adjacency-anchors.py:204` | tsukuroi | adjacent | **cite**: tsukuroi checks line-quote placement in PROVINCE tables; mechanical equivalent to Kengaku's 1-based capture line check |
| **C2 Range-Bounded Quote Check** | `tsukuroi-shokunin/tools/check-exec-environment-r40.py:309` | tsukuroi | adjacent | **cite**: tsukuroi checks quotes in range A..B of snapshots; directly adjacent to `anchor_line_check.py`'s range inclusion check |
| **C2 Prose Locator Check** | `mado-shokunin/quality/check-locators.py:4` | mado | adjacent | **cite**: mado checks prose line-range locators against receipts; does not check SOURCES.md rows |
| **C2 Fleet Sources Validator** | `scripts/sources-census.sh:626` | fleet (mori) | adjacent | **cite**: fleet standard for SOURCES 11-column schema; kengaku's gate is an orthogonal content verifier |
| **C3 Multi-Agent TB Subset** | `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:29` | kumitate | different | **ignore**: academic citation of multi-agent benchmark scores, not benchmark grader code execution or auditing |
| **C3 Audio Polyglot** | `audio-shokunin/reports/frontier/fa-sndfile.md:59` | audio | different | **ignore**: audio file dual-header parsing, completely unrelated to benchmark evaluation |
| **C3 Binary Smuggling Polyglot** | `game-dev-2d-shokunin/reports/round-102/r102-w1.md:68` | game-dev-2d | different | **ignore**: game engine binary script embedding, completely unrelated to benchmark evaluation |

---

## 4. Second-Order Effects and Adjacency Governance

1. **Benchmark Grader Ownership is Solely Kengaku's:**
   No sibling lane claims or performs benchmark grader auditing, execution, or interpretation. Four sibling lanes explicitly route all model evaluation and benchmark claims to Kengaku:
   - `kasegi-shokunin/PROVINCE.md:50`: `kengaku — LLM evaluation and benchmarks`
   - `chousa-shokunin/PROVINCE.md:10-11`: `Refuses: … model-quality or evaluation claims (→ kengaku)`
   - `kumitate-shokunin/PROVINCE.md:24`: `adjacent, not absorbed: kengaku evaluates agents, this lane arranges the seats around that judgment`
   - `kotoba-shokunin/PROVINCE.md:65`: `kengaku owns measured capability effects of prompt format and hands reusable craft out`
   Therefore, Kengaku's C3 coverage claim over `tb2-polyglot-c-py-grader.md` has **zero sibling contention**. Furthermore, Kengaku's `PROVINCE.md` explicitly disclaims polyglot source construction as an agent technique ("Polyglot construction as a technique, and how an agent should build the file, stay the task's and the authors' business — not this lane's"). Because Kengaku does not claim polyglot authoring craft, there is no unowned domain to report out to an integrator.

2. **No Competitor for Offline Anchor-Line Gate Tools:**
   While multiple siblings validate citations (`sources-check.mjs`, `cite-check.mjs`, `quote-reopen.py`, `check-locators.py`, `check-adjacency-anchors.py`, `check-exec-environment-r40.py`), none performs automated line-level substring verification over `corpus/SOURCES.md` anchor cells against git-tracked evidence captures. Sibling checks validate table schema (`sources-census.sh`, `sources-check.mjs`), live HTTP text (`quote-reopen.py`), character offsets (`build-spans.py`), or PROVINCE adjacency tables (`check-adjacency-anchors.py`). Kengaku's `anchor_line_check.py` fills a distinct depth role in the fleet. It conforms to tameshi's `r44-anchor-refresh-rule.md` by requiring new superseding rows (S157–S165) under QUALITY Q34 rather than in-place mutation.

3. **Containment Boundary is Cleanly Separated:**
   Kengaku's fixture fence (`plans/fixture_fence.py`) tests adversarial git-fixture discovery. It does not encroach on souji's repository/credential refusal fence or tameshi's reusable mutation testing service. The bwrap and strace techniques used in `plans/round46_c1_verify.py` follow established fleet patterns from souji and tameshi without altering or importing sibling code.

4. **Zero Report-Outs Required:**
   No sibling lane owns work that Kengaku has encroached upon, and Kengaku does not claim authority over any sibling's domain. No contradictory rulings or active disputes were detected. All 14 identified sibling overlaps are harmonious adjacent precedents that Kengaku cites. The 3 non-overlapping hits are distinct domain coincidences correctly ignored.

---

VERDICT: sibling-overlaps-14-report-outs-0
