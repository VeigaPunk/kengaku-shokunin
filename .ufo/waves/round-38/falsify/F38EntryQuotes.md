# F38EntryQuotes — falsify: located quotes + receipt-backed findings, `tb2-build-pmars-grader.md`

Round 38 wave 2 (FALSIFY), 2026-10-26. Scope: every `## Located quotes` row of
`corpus/knowledge/tb2-build-pmars-grader.md` (verbatim at its cited capture line via `sed -n`,
3–25 words) and every sentence in that doc backed by a receipt case
(`corpus/evidence/round38/build-pmars-probe.txt`: observed verdict + tests letters).
Receipts: `.ufo/waves/round-38/falsify/F38EntryQuotes/` (R1–R7, referenced below).
No lane file, index, or sibling lane was touched; scratch was `/fast/scratch/hyaku/kengaku-r38/F38EntryQuotes`
(deleted at the end). No tools installed or upgraded (bwrap/gcc/python3/curl/diff already present).

## 1. Located quotes: 28/28 supported (R2, R1)

`sha256sum -c SHA256SUMS` → all five captures `OK`; live re-fetch of the two pinned URLs at
`2fd12b88` digests to exactly the capture digests (falsifier clause (a) survives, R1). Mechanical
check of all 28 rows — quote read at its cited `sed -n '<n>p'` line, verbatim-substring test, word
count: `TOTAL=28 OK=28 BAD=0`. Every quote is byte-exact at its cited line; word counts span 3
(`test_outputs.py:23`, `:31`, `:62`, `:84`) to 17 (`instruction.md:9`), all inside 3–25.

One nit, not counted as unsupported (the document states the condition precisely elsewhere):

- **N1 — `corpus/knowledge/tb2-build-pmars-grader.md:107`** (claim column of row
  `test_outputs.py:13`): "a failed command's output is returned, not raised". The quoted bare
  `except subprocess.CalledProcessError as e:` line shows only that a handler exists; the
  return-not-raise behaviour lives at `test_outputs.py:14-15` and holds only when the captured
  output is non-empty. The doc gives the exact condition at lines 52-53 and 248, so the document is
  correct — the single-row compression alone under-determines its claim.

## 2. Receipt-backed sentences: 2 misstatements (R3–R5)

Coverage: all 63 doc lines naming a receipt case (26-34, 143-149, 156-175, 183-191, 219-229,
233-264, 303, 336-340) were swept and checked against the receipt, the frozen instrument, the
captures, and the cited wave-1/upstream artifacts. The frozen receipt was re-executed before
judging: `plans/build_pmars_probe.py --lane .` in scratch printed a receipt **byte-equal** to the
frozen file (`diff` empty), tail `cases=22 observed_pass=7 observed_fail=15 mismatches=0` (R3) —
falsifier clause (b) survives, and every number below rests on a reproduced receipt.

All 22 per-case (observed, tests) citations match (R5); all seven requirement-map labels re-derive
`partly` under V7 over all violating cases; all 14 cited (tag, case, direction) pairs are correct;
the narrow-tag carrier counts 3/4/5 are correct; the `canned-x11-dlopen` load-bearing claim
reproduces (dropping it flips `no-x11` to `enforced`); the four "no label moves" drop-checks hold
(R4). Two sentences are misstated:

- **F1 (misstated, medium) — `corpus/knowledge/tb2-build-pmars-grader.md:237-238`**, Findings §1,
  final sentence: "it is the case that **fixes** four of the seven map labels at `partly`."
  Per the doc's own V7 rule (computed over *all* violating cases), each of `from-source`,
  `debian-source`, `extract-to-app`, `debugger-works` has seven passing carriers; dropping
  `canned-shape` leaves six pass carriers per tag and every label stays `partly` (R4). No label is
  fixed by `canned-shape`. The doc itself applies the stricter standard one section earlier
  (§Contestable: only `canned-x11-dlopen` is load-bearing, with the arithmetic shown), so this
  sentence overstates uniqueness its own method contradicts. True statement: `canned-shape` is the
  single strongest *witness* (violates all four fabricated-state tags while passing `PPPP`).

- **F2 (misstated, low) — `corpus/knowledge/tb2-build-pmars-grader.md:92-93`**, structural
  consequence 5: "every passing case's output comes from a program that **ignores its `argv`**."
  The canned C program branches on argv — `for (int i = 1; i < argc; i++) if (strcmp(argv[i],
  "-b") == 0) battle = 1;` (`plans/build_pmars_probe.py`, `C_SRC`) — and the script variant does
  the same (`for a in "$@"; do if [ "$a" = "-b" ]`). What the passing programs ignore is the
  warrior-*file* arguments (no file is ever opened); the instrument's own docstring says "for any
  argv without `-b`". The sentence's point (output is fabricated and independent of the named
  warriors) survives; the word `argv` is wrong — it should be "the warrior arguments".

## 3. Checked and held (no finding)

- Summary case list (doc 26-34): all seven pass cases `PPPP`, descriptions match staged states
  (21-line `C_SRC`, exit 3, sbin script, zero-byte `debian` file, `sim.c` directory, `Results: 12
  34 78 forged`) — R5, R6.
- Static-reading table and mechanisms (`test.sh:18-29`, `:23-24`, `:9-16`, `:27-40`, `:43-46`,
  `:53-57`, `:62-70`, `:75-85`) — all verified against the captures.
- Group table (doc 219-229): every observed/letters cell matches the receipt, including
  `CalledProcessError` on `canned-script`/`canned-static` and the PPFP/PPPF/PPFF shapes.
- Instrument claims (doc 204-217): bwrap namespaces, `/usr` ro, tmpfs `/tmp`, three ro-binds,
  `/tests` holding only the capture, cwd `/app`, Debian-default `PATH`, verdict mapping, zero-byte
  staging, no warrior files in any case, probe digest `32f0771c…25c24a` — all verified in source
  (R6).
- §What the probe does not show: `solve.sh` deb-src/installs/`apt-get source`/`-DXWINGRAPHX`/`LIB =
  -lncurses`/mode 0755 at the cited lines; `task.toml` `:22`/`:25`/`:29`/`:34`; host `sh -> bash` —
  all verified (R7).
- §Contestable tags: `R38CritProbe.md` §3 lists exactly the five tags the doc names, `dlopen`
  load-bearing, with the strace `openat …/libX11.so.6` evidence (R7).
- Falsifier §(c)-(d): consistent with the code (no provenance read anywhere; `re.match` start
  anchor; one-level globs).

## 4. Residual risk / verification gaps

- Prior-art quotations (JonathanGabor audit lines 249/255, TB2 issues #59/#631, TB2 2.1 grader
  byte-equality) are cited to wave-1 reports and were not re-verified here — outside this seat's
  receipt scope.
- The doc's historical "second run's receipt was byte-equal to the first" is not independently
  re-checkable; this seat's fresh third run is byte-equal to the frozen file (R3).
- Findings rest on the host toolchain (host `gcc`/`ldd`/`bash`), as the doc itself discloses; the
  task image's toolchain remains unexercised.

Every quoted number above carries its command in R1–R7.

VERDICT: entry-quotes-28/28-claims-unsupported-2
