# F37C2Rerun — C2 re-run on a clean clone of the landing tip

Seat: executor, kengaku round 37 wave 2 (falsify). Target: the C2 coverage landing
(`corpus/knowledge/tb2-git-webserver-grader.md`, SOURCES S111–S113, captures, probe) and the
counter that claims it.

## Setup

```
S=/fast/scratch/hyaku/kengaku-r37/F37C2Rerun; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/fx/lane"
git -C "$S/fx/lane" checkout -q 357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5
```
- `git -C $S/fx/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r37/F37C2Rerun/fx/lane`
- `git -C $S/fx/lane rev-parse HEAD` → `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`
- `git -C $S/fx/lane status --porcelain` → empty (clean tree before every run)
- host: `Python 3.14.8`, `bubblewrap 0.13.1`, `uv 0.13.0`; `import Bio` → `ModuleNotFoundError`
- the lane was never written to; no git-mutating command ran outside the clone.

## C2 predicate, run verbatim (`cd <clone>; python3 plans/round37_c2_verify.py --lane .`)

EXIT=0, WALL=53.037 s (`t0=$(date +%s.%N) … awk`). Full stdout:

```
V1 ok listed=6 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=32 distinct_quotes=32 distinct_lines=32 out_of_word_range=0
    gate: P4 ok checked=32 bad=0 first=0
    gate: P5 ok manifest_entries=6 bad=0 first=0
    gate: P6 ok rows=3 bad=0 first=0
    gate: P7 ok source_lines=4 bad=0 first=0
    gate: P8 ok index_rows=44 knowledge_files=44 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=8443
    gate: defects=0
V2 ok gate_exit=0
V3 ok rows=3 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
```

stderr empty. A second run with an absolute `--lane $S/fx/lane` printed the identical 722-byte
stdout (`cmp` → `SAME_OUTPUT`), WALL=53.066 s. The frozen predicate sentence is reproduced
exactly: `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0, on a clean clone of the tip.

## Probe re-run and byte comparison

`cd <clone>; python3 plans/git_webserver_probe.py --lane .` — run twice, independently:

| run | exit | wall | bytes | sha256 |
|---|---|---|---|---|
| 1 | 0 | 52.759 s | 8529 | `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8` |
| 2 | 0 | 52.773 s | 8529 | `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8` |
| committed `corpus/evidence/round37/git-webserver-probe.txt` | — | — | 8529 | `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8` |

- `cmp run1 receipt` → `CMP1=EQUAL`; `cmp run2 receipt` → `CMP2=EQUAL`; `cmp run1 run2` → `CMP12=EQUAL`.
- both runs: `cases=22 observed_pass=9 observed_fail=13 mismatches=0`; stderr empty both times.
- determinism holds across interpreters, not just across runs: the direct runs used host
  `python3` 3.14.8, while gate P10 inside the same predicate shells out to
  `uv run --no-project --with biopython==1.85 python3` (3.13.16) and also reported byte equality.

## Negative controls (does the counter bite?)

Single-input mutations applied to a scratch copy (`cp -a --reflink=auto` of the clone), each check
called in isolation; V2 is covered by the real predicate run above. Scripts and outputs are in
`F37C2Rerun/negctl{,2,3}.py` / `.out`.

| mutation | check | result |
|---|---|---|
| flip one byte of `verify.sh` capture | V1 | DEFECT `bad=['verify.sh']` |
| append stray manifest entry | V1 | DEFECT `extra=['stray.txt']` |
| S111 anchor digest last hex digit | V3 | DEFECT `S111:anchor_digest` |
| second `sha256` token in S112 anchor | V3 | DEFECT `S112:anchor_digest` |
| drop `sha256 ` prefix in S113 anchor | V3 | DEFECT `S113:anchor_digest` |
| truncate an S-row to 10 cells | V3 | DEFECT `row` |
| drop one `CASE` line from the receipt | V4 | DEFECT (ids differ + summary disagrees) |
| inflate `observed_pass` in the summary | V4 | DEFECT (summary disagrees) |
| duplicate S111 row (census E03) | V6 | `census_exit=1` → DEFECT |
| malformed row (census E01) | V6 | `census_exit=1` → DEFECT |
| dry-table byte flipped | V5 | DEFECT (not at freeze digest) |
| `unenforced` → `enforced` (line 1–6 row) | V7 | DEFECT `enforced without a failing case` |
| `enforced` → `unenforced` (line 9 row) | V7 | DEFECT `unenforced without a passing case` |
| delete a requirement-map row | V7 | DEFECT `instruction lines not mapped: [1,2,3,4,5,6]` |
| **`partly` → `enforced` (line 7 row)** | V7 | **ok, bad=0 — NOT caught (finding N2)** |
| forge one `grader-stdout` byte in the receipt | V1/V4/V7 | all ok (by design) → **P10 DEFECT**: `fresh probe output is not byte-equal to the receipt` |
| restore the receipt, re-run P10 | P10 | ok `probe_rerun=byte-equal bytes=8443` |

The last two lines are the important positive: a receipt forged in a byte that the seven V checks
never read is caught only by gate P10, and P10 does catch it (`wall=52.8s`). Authenticity of the
receipt therefore rests where the counter's docstring says it does.

## Findings

**N1 — gate P10's `bytes=` label reports a character count, not bytes; "byte-equal" is a
text-mode comparison.** `plans/pkg_gate.py:285` prints `f"probe_rerun=byte-equal bytes={len(want)}"`
where `want = read(...)` is `pathlib.read_text()` (`pkg_gate.py:38`), so 8443 is the code-point
count. Measured on the committed receipt: `wc -c` = 8529, `len(text)` = 8443, 43 non-ASCII chars
(`—`, `✅`, `❌`), 49 newlines. The equality itself is `r.stdout != want` with `text=True`
(`pkg_gate.py:283`), so universal-newline translation applies: a receipt rewritten with CRLF line
endings would compare equal to the probe's LF output while the files differ byte-for-byte. Severity:
wording/disclosure, not a C2 verdict change — the probe's own output and the committed receipt are
genuinely identical (same sha256). Suggested fix: `len(want.encode())` and compare `r.stdout`
against a bytes read, or relabel to `chars=`.

**N2 — V7 cannot see a `partly` label downgraded to `enforced`.** Relabelling the
`instruction.md:7` row from `partly` to `enforced` leaves V7 at `rows=4 bad=0`, because the row
cites `wrong-port-8081` (fail) and `static-file-no-git` (pass), and V7 only requires an `enforced`
row to cite *a* failing case (`round37_c2_verify.py:195-201`). The required-label relation is
one-directional, so the strongest form of the claim's evidence label can be dropped invisibly by
the counter's own criterion. A stricter equality version (enforced ≡ {fail}, unenforced ≡ {pass},
partly ≡ {pass, fail}) was evaluated against the landing and reports `bad=0 rows_checked=4`, and it
does flag the relabelled row (`7:enforced verdicts=['fail','pass']`) — so the tightening is free
for the current entry. Severity: low (narrow, and the landing satisfies the strict form); the
current entry's four rows are `1-6 unenforced{pass}`, `7 partly{fail,pass}`, `8 partly{fail,pass}`,
`9 enforced{fail}`.

**N3 — gate P10 depends on `uv` plus a warm biopython cache, for a probe that never imports Bio.**
Host python has no `Bio`, so P10 runs the probe through
`uv run --no-project --with biopython==1.85 python3` (`pkg_gate.py:276`), while
`plans/git_webserver_probe.py` contains no `Bio` reference at all (`grep -n Bio` matches only
`plans/pkg_gate.py:273`). Measured: `uv run --offline --no-project --with biopython==1.85 python3 -c
'import Bio'` → `BIO 1.85 PY 3.13.16`, 0.017 s (cache hit). On a cold or offline host without that
cache, P10 returns a non-zero probe exit and C2 flips to DEFECT for an environment reason unrelated
to the package. Severity: portability risk; the Bio indirection is unused by the probe, so pinning
`sys.executable` would remove the dependency. Not a defect of the landing — recorded because the
predicate claims reproducibility on "a clean clone", not on a warm package cache.

## What holds

- `PREDICATE C2 pass` reproduces on a clean clone of `357dece…`; predicate text, V-line set and gate
  line set match the frozen claim.
- The probe is byte-reproducible: three independently produced 8529-byte outputs (two direct runs
  under 3.14.8, one gate rerun under 3.13.16) share sha256
  `835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8` with the committed receipt.
- The counter is not vacuous: 14 of the 15 mutations aimed at a specific check were caught by that
  check (the exception is the `partly`→`enforced` relabel, finding N2), and the one class V1–V7 are
  blind to (a forged `grader-stdout` byte) is caught by P10.
- Timing on this host: C2 counter 53.0 s (of which ~52.8 s is P10's inner probe), standalone probe
  52.8 s.

## Risks / blockers

- No blocker. Nothing in the C2 landing failed; the three findings are label-precision and
  portability items, none of which changes the verdict under the frozen predicate.
- Residual risk inherited from N3: re-running this predicate in a cold `uv` environment will report
  `V2 DEFECT` for reasons unrelated to the package.
- Scratch `/fast/scratch/hyaku/kengaku-r37/F37C2Rerun` removed after copying receipts; the 539 MB
  clone and the mutation copy were never placed under the report directory.

## Artifacts (this directory)

`c2-verify-literal.out` (verbatim predicate stdout), `c2-verify.out` (absolute-lane repeat),
`c2-verify-literal.err` (empty), `probe-run1.err`, `probe-run2.err` (empty),
`negctl.out`, `negctl2.out`, `negctl3.out`, and the three harnesses `negctl.py`, `negctl2.py`,
`negctl3.py`.

VERDICT: c2-rerun-pass-probe-byte-equal-yes
