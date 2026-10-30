# E5ChessProbe — scoped findings (R55-C3 instrument)

**Deliverable:** `plans/round55_c3_chess_probe.py` — NEW, sole lane file written by this seat.

**Contract honoured:** 12 frozen cases embedded with predictions written before any run;
per-case bubblewrap sandbox (private namespaces, /tests ro byte-copy of the captured grader,
case-owned writable /app); observed P = rc 0, F = nonzero + AssertionError, else per-case
SETUP → exit 2; `CASE`/`cases=12`/`PREDICATE R55-C3` output lines; exit 0 pass / 1 fail /
2 setup; `--lane`/`--receipt`/`--selftest` CLI; no network; scratch under `--work`/TMPDIR
and self-deleted.

**Acceptance:** `python3 plans/round55_c3_chess_probe.py --selftest` → exit 0,
`SELFTEST cases=2 failures=0` (toy pass + toy fail both verdict-correct through the real
bwrap pipeline).

**One-time battery verification (disclosed per seat spec; official run is a sibling's):**
all 12 observed verdicts equal the frozen predictions — `cases=12 observed_pass=5
observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`, exit 0. Full output kept at
`.ufo/waves/round-55/w1/E5ChessProbe/battery-verify.txt`. The frozen receipt path
`corpus/evidence/round55/chess-best-move-probe.txt` was NOT written by this seat.

**Guards verified:** captured grader sha256 equals the frozen pin `a540714e…`; missing
capture → SETUP exit 2; tampered capture (sha mismatch) → SETUP exit 2; `--receipt` output
byte-identical to stdout across runs.

**Defects found:** none in claims or capture. Two spec ambiguities (bwrap SRC/DEST order in
the frozen sketch; unbound interpreter tree) resolved in the only functional reading and
documented in the module docstring.

**Installs:** none. **Scratch:** `/fast/scratch/hyaku/kengaku-r55/E5ChessProbe/` deleted.
**Dead ends:** none.

Full detail: `.ufo/waves/round-55/w1/E5ChessProbe/report.md`.
