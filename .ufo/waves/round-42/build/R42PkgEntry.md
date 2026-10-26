# R42PkgEntry — C2 knowledge entry drafted (round 42, wave 1, scribe seat)

## Behavior

Drafted the pinned TB2 `circuit-fibsqrt` grader entry at
`.ufo/waves/round-42/build/R42PkgEntry/tb2-circuit-fibsqrt-grader.md` — 416 lines, sha256
`f499f6c34ea841eb72d057e76b8101f6d8efd6ed12abfb557d049c16014a3a47` — modelled on
`corpus/knowledge/tb2-constraints-scheduling-grader.md`. It carries the three `source:` header lines (S125
`tests/test_outputs.py`, S126 `instruction.md`, S127 `tests/sim.c`, each with the pinned raw URL at
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`), `verified-at: 2026-10-26`, a `recheck:` line, and the eleven required
sections: Summary, Source labels, What is graded (static reading of `test_outputs.py` **and** `sim.c`), Located
quotes, Requirement map, Case table, Findings (each tied to receipt case ids), Regrade, What the probe does not
show, Prior art, Negative space with a four-part falsifier.

Contents, counted: **24 quotes at 24 distinct locations** (5 `instruction.md`, 8 `test_outputs.py`, 11 `sim.c`), all
3-25 words, all verbatim on the cited line; **7 requirement-map rows for the 7 frozen TAGs** with labels derived by
the counter's rule (not chosen) — `line-form` unenforced, `last-32-lines` unenforced, `gates-file` enforced,
`line-limit` enforced, `output-function` partly, `example-208` partly, `example-20000` partly; **16/16 case rows**
in receipt order with the receipt's letters and verdicts (`8` PPF/PPP/PFP/PFF shapes reproduced exactly); 10
findings; 5 "what the probe does not show" limits; 4 prior-art items; nothing claimed as novel.

Also drafted the four integration surfaces the counter needs, as text only, in
`.ufo/waves/round-42/build/R42PkgEntry/integration-drafts.md`: SOURCES rows S125-S127 (11 cells, tier A, `mined`,
`2026-10-26`, `180d`, anchor cell carrying exactly one `sha256 <pin>`, teaches ≥31 words each, used-by
`corpus/knowledge/tb2-circuit-fibsqrt-grader.md`), the README knowledge index row, the README coverage bullet, the
README §Frontier round-42 sub-bullet, and the PROVINCE round-42 paragraph. None of these were written to the lane.

## Gates — what was run, with output

Scratch `S=/fast/scratch/hyaku/kengaku-r42/R42PkgEntry`; clone
`git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`, toplevel verified
`/fast/scratch/hyaku/kengaku-r42/R42PkgEntry/lane`, HEAD `fda71ae033224e1d0ed5ddd0fdc1b63a02f2473` (identical to the
lane's own HEAD). Drafts were copied into the clone and **staged only** (`git add`, never committed).

1. **Quote/map/case self-check** (`$S/qcheck.py`, replicating the gate's `QUOTE_SECTION`/`QUOTE_ROW` and the
   counter's `MAP_ROW`/`CASE_ROW`):

   ```
   rows 24 bad []
   out_of_range []
   distinct_quotes 24 distinct_lines 24
   case rows 16
   ```

   No `NOT VERBATIM` line was printed for any of the 24 quotes.

2. **SOURCES census** — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file
   "$S/lane/corpus/SOURCES.md"` → `file	ok	…/lane/corpus/SOURCES.md`, `census_exit=0`, with 15 pre-existing `W04`
   duplicate-URL warnings on rows S040-S100 and no `E`-code (an `E11` would have fired had the used-by path been
   missing; none did).

3. **Frozen package gate, final entry bytes** (the run the numbers below come from):

   ```
   envelope: bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>
   date_before=17:28:25
   localbin_before=436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
   P1 ok pinned=2 mismatched=0
   P2 ok receipt_sha256=pinned
   P3 ok rows=24 distinct_quotes=24 distinct_lines=24 out_of_word_range=0
   P4 ok checked=24 bad=0 first=0
   P5 ok manifest_entries=9 bad=0 first=0
   P6 ok rows=3 bad=0 first=0
   P7 ok source_lines=3 bad=0 first=0
   P8 ok index_rows=49 knowledge_files=49 bad=0 first=0
   P9 ok untracked=0 first=0
   P10 ok probe_rerun=byte-equal bytes=4212
   defects=0
   gate_exit=0
   V4 ok cases=16 mismatches_named=0/0 bad=0
   V7 ok rows=7 tags=7 bad=0
   V9 ok case_rows=16/16 bad=0
   date_after=17:29:25
   localbin_after=436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
   ```

   Command: `bwrap … /usr/bin/python3 "$S/lane/plans/pkg_gate.py" package --root "$S/lane" --spec
   "$S/pkg-spec-r42-effective.json" --rerun --require-clean-tree` with `receipt_sha256` filled to
   `2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a` (the receipt's own digest). V4/V7/V9 are the
   frozen counter's functions, imported from `"$S/lane/plans/round42_c2_verify.py"` and called as
   `v4(lane); v7(lane); v9(lane)` inside the same envelope.

4. **Full frozen C2 counter** on the same clone, earlier run over the pre-correction entry bytes (only `task.toml`
   line cites + two sentences changed since; no clause reads them):

   ```
   V1 ok listed=9 bad=0 extra=0
   V2 ok spec=frozen gate=frozen gate_exit=0
   V3 ok rows=3 bad=0
   V4 ok cases=16 mismatches_named=0/0 bad=0
   V5 ok probe=frozen dry_byte_equal=True
   V6 ok census_exit=0
   V7 ok rows=7 tags=7 bad=0
   V8 ok order_exit=0 result=PASS
   V9 ok case_rows=16/16 bad=0
   checks=9 defects=0
   PREDICATE C2 pass
   counter_exit=0
   ```

   Wall time 71.21 s (17:26:36 → 17:27:47), same envelope. Note the nesting: the counter's V2 spawns the gate,
   whose P10 spawns the probe, which spawns one sandbox per case — all inside the outer `bwrap`, no failure.

5. **Independent re-fetch of the three pinned raw URLs** (curl, 2026-10-26):

   ```
   tests/test_outputs.py raw=6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438
   instruction.md raw=a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea
   tests/sim.c raw=700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173
   ```

   All three equal the spec pins and the capture digests, so the entry's "identical to the pinned raw files"
   sentence is measured, not assumed.

**Host-safety receipt (QUALITY Q32).** Envelope used for every gate/counter/probe run:
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc
--unshare-pid --die-with-parent <command>`. `date +%T` before/after each run is quoted above (17:24:50/17:25:49,
17:26:36/17:27:47, 17:28:25/17:29:25). `ls -A /home/vgpnk/.local/bin | sha256sum` was
`436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` before the first run and identical after the
last; no shim was created. No write outside `$S` and the two report-dir artifacts; `TMPDIR="$S"` throughout.

## Touched surfaces

- Written (report dir only): `.ufo/waves/round-42/build/R42PkgEntry/tb2-circuit-fibsqrt-grader.md` (the deliverable),
  `.ufo/waves/round-42/build/R42PkgEntry/integration-drafts.md` (SOURCES/README/PROVINCE text for the L1), this
  report.
- Scratch: `$S/lane` (a `--shared` clone at `fda71ae`; index-only `git add` of the four draft surfaces so the gate's
  P9 could run clean; **no commit, no push, no mutation of the lane**), `$S/qcheck.py`, `$S/integrate.py`,
  `$S/pkg-spec-r42-effective.json` (spec copy with `receipt_sha256` filled).
- Untouched: the lane's `corpus/`, `plans/`, `PROVINCE.md`, `README.md`, `SOURCE` set, `SCORECARD.md`, `LOG.md`,
  `SHONEN`, the Git index and every jj ref; every frozen artifact under `plans/` and
  `corpus/evidence/round42/`; the fleet root; other seats.

## Findings (seat-level)

1. **The entry is gate-clean on the first integrated run, and every clause is doing real work.** P1 (`pinned=2`),
   P2, P5 (`manifest_entries=9`), P6 (`rows=3`), P7 (`source_lines=3`) are provenance; P3/P4 are the 24 quotes; P8
   is the README index set-equality (49 files / 49 rows after the draft row); P9 the clean tree; P10 re-ran the frozen
   probe and got 4212 bytes byte-equal to the receipt. Nothing needed an exemption.
2. **The requirement-map labels are forced by the receipt.** Computed by hand from the 16 `violates=` sets and then
   confirmed by `V7`: `output-function` has 15 violating cases (9 fail, 6 pass → `partly`), `example-208` and
   `example-20000` have 14 each (the same set minus `lookup-28-plus-examples` → `partly`), `gates-file` has 2 (both
   fail → `enforced`), `line-limit` 1 (fail → `enforced`), and the two single-witness tags `line-form` and
   `last-32-lines` are `unenforced` because their only violating case passes. The three `partly` labels *are* the
   coverage gap: a lookup table passes while violating the sentences the tags name.
3. **Four defects in my own draft, found and fixed before the validating run** (all in the final bytes; none in a
   quote, so no `P4` risk): (a) `task.toml` cites were shifted — `difficulty` is `:15` not `:16`, expert/junior
   estimates `:18`/`:19` not `:21`/`:22`, the two 3600 s timeouts `:22`/`:25` not `:25`/`:29`, `docker_image` `:29`
   not `:33`, `allow_internet` `:34` not `:37`; (b) two places said the grader "raises" on `int("")` — it does not,
   the `except ValueError` at `test_outputs.py:128-131` catches it and clears `all_passed`, and the receipt's silence
   about an error on `empty-gates-file` is what exposed the mistake; (c) the gate-forms row cited `sim.c:122-176`,
   corrected to `:122-182` (the binary branch's second dependency block runs to 181); (d) the two truths I had to
   *narrow* rather than assert: the CRLF pass does not show that constant lines survive a CR (measured: L28 has 0
   constant lines among its 1195), and the `./sim` vs `/app/sim` binding holds only because the harness cwd is `/app`
   (no receipt case separates the two). Both are marked `[INFERENCE]` in the entry.
4. **The receipt's `lookup-28` composition, measured for the entry, not assumed.** Importing the frozen probe's
   builder and counting: `lookup(GRADED)` = 1195 lines = 32 self-copies + 32 NOTs + 1099 binary gates + 32 final
   copies, **0** `outX = 0`/`outX = 1` lines; `GRADED` = 28 values, max `48401`, and neither `208` nor `20000` is in
   it. This is what makes the CRLF scope note and the "28 points, not a function" finding honest rather than
   plausible.
5. **Integration prerequisites the L1 must land, or the counter fails at landing.** `P6`/`V3` need S125-S127 as
   11-cell registry rows inside `## Registry` with the exact pinned URL, tier `A`, status `mined`, ≥8 teaches words
   and the anchor `sha256` equal to the spec pin; census `E11` needs the used-by path to exist on disk at the same
   moment; `P8` needs the README index row (citing all three rows) **and** a column-0 coverage bullet naming both the
   entry file and `evidence/round42/fibsqrt-probe.txt`, and the knowledge-file set must equal the index set; `P7`
   needs the three `source:` lines to be the pinned URLs; `V9(c)/(d)` need the PROVINCE line and the §Frontier
   mention. All five are drafted verbatim in `integration-drafts.md` and were accepted by the frozen gate/counter in
   the clone.
6. **The receipt is re-runnable cheaply and deterministically.** `P10`'s fresh probe run took ~59 s wall inside the
   envelope and produced bytes identical to `corpus/evidence/round42/fibsqrt-probe.txt`
   (`2a54ca8a…`, 4212 bytes), so the entry's `recheck:` instruction (digests + `fibsqrt_probe.py --lane .`) is
   affordable at any later tip.
7. **Prior art is recorded as prior art, not as a claim.** The only public statement found is the contrary one
   (`JonathanGabor/terminal-bench-2-audit`, run `20260120_125158`: “28 distinct test cases with varied inputs make
   hardcoding impractical”), located by the round-41 seat (`R41PlanNext` §3.2) and **not re-fetched by me**; the
   entry cites it as tier C, claims **no** novelty, and says so in §Prior art and §Negative space. I ran no tracker
   search of my own and the entry says that too.

## Out of scope (not done, by contract)

- No image pull, no agent run, no trajectory, no task-validity/difficulty/solvability verdict; no claim that an
  agent would build a lookup circuit.
- No lane file edited, nothing committed or pushed, no jj command, no C1 work, no probe/spec/gate/counter change,
  no capture or receipt touched.
- The 16 frozen cases remain the entry's whole measured surface; the unexercised shapes are named in §What the probe
  does not show (index ≥ `MAX_SIGNALS`, a CR-bearing constant line, symlinks, an agent trajectory).

## Artifact paths

| Path | Note |
|---|---|
| `.ufo/waves/round-42/build/R42PkgEntry/tb2-circuit-fibsqrt-grader.md` | the entry draft, 416 lines, sha256 `f499f6c34ea841eb72d057e76b8101f6d8efd6ed12abfb557d049c16014a3a47` |
| `.ufo/waves/round-42/build/R42PkgEntry/integration-drafts.md` | SOURCES S125-S127 rows, README index row + coverage bullet + §Frontier sub-bullet, PROVINCE paragraph — text for the L1 |
| `.ufo/waves/round-42/build/R42PkgEntry.md` | this report |
| lane clone (scratch, discarded) | `/fast/scratch/hyaku/kengaku-r42/R42PkgEntry/lane` @ `fda71ae`, four surfaces staged, never committed |

VERDICT: entry-drafted-quotes-24-tags-7/7-case-rows-16/16
