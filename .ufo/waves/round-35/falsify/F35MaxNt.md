# F35MaxNt — falsify finding 2 (max passing gBlock = 2766 nt)

Seat: F35MaxNt (executor, leaf; no subagents spawned). Wave 2 of 2 (FALSIFY). Item attacked: `corpus/knowledge/tb2-protein-assembly-grader.md` finding 2 (lines 73–76): *"With the literal lengths 8, 259, 158, 235 and 182 residues and four linkers of at most 20, the longest gBlock that passes every other assertion is 3 × (842 + 80) = 2766 nt (`max_passing_nt=2766` in the receipt)."*

## Verdict

**REFUTED — a passing gBlock of 2768 nt exists (2766 + 2 trailing nucleotides).** The entry's `3 × (842 + 80) = 2766` is the maximum length of a *fully translated* fusion (922 aa), but the grader's translator drops trailing partial codons, so 1–2 extra nucleotides can be appended after the last full codon without changing the translated protein. Every grader assertion still passes at 2767 and 2768 nt. 2768 is the true maximum: +3 nt (a complete extra codon) adds an amino acid and fails `snap_idx + len(snap_aa) == len(gblock_aa)`.

## Evidence

Environment: host Python 3.14.8 with `biopython==1.85` (the version `test.sh` pins) installed into a scratch venv `/tmp/k35f-U53V/venv` (channel: `python3 -m venv` + `pip`, since pacman transactions are paused; `uv 0.13.0` present but unnecessary). Grader capture `corpus/evidence/round35/tb2-eval/test_outputs.py` SHA-256 matches the pinned digest (probe refuses otherwise). Probe run in-lane reproduces the receipt summary exactly: `cases=18 observed_pass=5 observed_fail=13 mismatches=0` (exit 0).

### 1. Literal lengths (recount from the capture, byte-exact literals)

```
$ python3 - <<'EOF'
import re
src = open("corpus/evidence/round35/tb2-eval/test_outputs.py").read()
for n in ("flag_aa","donor_aa","dhfr_aa","acceptor_aa","snap_aa"):
    print(n, len(re.search(n + r' = "([^"]*)"', src).group(1)))
EOF
flag_aa 8
donor_aa 259
dhfr_aa 158
acceptor_aa 235
snap_aa 182
```
Sum = 842 aa; +4 × 20 = 922 aa = 2766 nt. (Matches the entry.)

### 2. The mechanism: Biopython 1.85 drops trailing partial codons

```
$ python3 - <<'EOF'
from Bio.Seq import Seq
import warnings
for n in (3,4,5,6,7):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        t = str(Seq("A"*n).translate())
    print(n, repr(t), len(t), [str(x.message)[:40] for x in w])
EOF
3 'K' 1 []
4 'K' 1 ['Partial codon, len(sequence) not a multiple']
5 'K' 1 ['Partial codon, len(sequence) not a multiple']
6 'KK' 2 []
7 'KK' 2 ['Partial codon, len(sequence) not a multiple']
```
`Seq.translate()` (defaults: `to_stop=False`, table 1) returns floor(n/3) amino acids; a trailing 1–2 nt partial codon is dropped with only a warning. So appending 1–2 nt to a length-3k gBlock leaves the translated protein byte-identical — the snap-end check (`snap_idx + len(snap_aa) == len(gblock_aa)`) still holds.

### 3. Constructed counters (the decisive run)

Builder: max-size fusion `flag + G20 + donor + G20 + dhfr + G20 + acceptor + G20 + snap` (922 aa), deterministic GC-balanced back-translation (codons per residue chosen to keep every 50-nt window's G/C count near 25), verified `windows_ok` on the raw 2766-nt string before testing. Then 0/1/2/3 `A` nucleotides appended (trailing; no newline). Run through the captured grader function via the probe's `run_grader` (same code path as `plans/tb2_grader_probe.py`):

```
$ python3 repro_maxnt.py
append=0 nt=2766 observed=pass assertion='-' gcwin_ok=True
append=1 nt=2767 observed=pass assertion='-' gcwin_ok=True
append=2 nt=2768 observed=pass assertion='-' gcwin_ok=True
append=3 nt=2769 observed=fail assertion='End of gBlock must match snap protein.' gcwin_ok=True
```
- 2766 nt: pass (the entry's own max).
- **2767 nt: pass — already exceeds the claimed max.**
- **2768 nt: pass — the counterexample; > 2766 and ≤ 3000; `GC content` windows still within 15–35.**
- 2769 nt: fail — the 3rd appended nucleotide completes a codon, adding one amino acid after SNAP; `snap_idx + len(snap_aa) == len(gblock_aa)` fails first. This pins the ceiling at 2768.

Cross-check with independent constructions (different linker amino-acid patterns and GC targets — G-only, S-only, alternating GS; targets 0.40/0.42/0.50): every baseline 2766-nt build passes and every +2-nt build passes (`base=pass +2nt=pass (-)` in all three). The result is not an artifact of one builder.

### 4. Why nothing else can lengthen a passing gBlock

Walked every hiding place in the grader's assertions (`test_outputs.py`):
- **Before FLAG** — `flag_idx == 0` pins the protein start at the first residue; any leading content fails (entry lines 57, 120).
- **After SNAP** — `snap_idx + len(snap_aa) == len(gblock_aa)` pins the end to the first occurrence of SNAP; any translated content after it fails (entry lines 58, 123). Only *untranslated* trailing nucleotides survive (mechanism above), and only 1–2 of them (a 3rd completes a codon and translates).
- **Inside the four gaps** — each gap must `fullmatch(r"[GS]+")` with length 5–20 (entry lines 59, 121–122); any inserted residue there counts against the 20 cap, cannot exceed it, and must be G/S (subproteins contain non-GS residues, so no literal can hide in a gap).
- **Inside a subprotein** — literals are located by contiguous `str.find`; a single inserted residue breaks the exact match (observed: `donor-one-substitution` fails), and a *second full copy* of any literal can only sit before/after the canonical first occurrence, which the boundary/linker checks above forbid.
- **Frame tricks / middle insertions** — translation starts at nt 0; inserting 1–2 nt in the middle shifts every downstream codon (literals break); inserting a full codon at the end adds an amino acid (fails snap-end). The `lower()`/`rstrip()`/single-line checks do not change length. Alphabet `[atcg]+` and the 3000-nt cap are never binding for any candidate that reaches the structure (2768 ≪ 3000).

So the maximum passing length is 2768 nt, not 2766. Note the entry's second sentence (*"The cap only changes which assertion fails first … never the reward"*) survives — no passing candidate reaches 3000 — but the headline number in finding 2 is wrong by 2 nt, and the receipt's `max_passing_nt=2766` is not the true maximum.

## What could not run / not checked

- Re-fetch of the three pinned URLs against `SHA256SUMS` (the entry's recheck gate) was out of scope; the local capture digest was verified by the probe and matches the pinned `44a05a24…`.
- No changes were made to any lane file; all writes were under `/tmp/k35f-U53V/` (scratch) and the report path. No git/jj commands were run. `rm -rf /tmp/k35f-U53V` (scratch venv + scripts) is safe to run; the repro script below recreates everything.

## Repro (self-contained)

```
$ D=$(mktemp -d /tmp/k35f-XXXX) && python3 -m venv "$D/v" \
    && "$D/v/bin/pip" install -q biopython==1.85 && cat > "$D/r.py" <<'EOF'
import importlib.util, pathlib
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GPATH = LANE / "corpus/evidence/round35/tb2-eval/test_outputs.py"
PPATH = LANE / "plans/tb2_grader_probe.py"
spec = importlib.util.spec_from_file_location("probe", PPATH)
probe = importlib.util.module_from_spec(spec); spec.loader.exec_module(probe)
CODONS = probe.CODONS
def build(aa, target=0.45):
    out = ""
    for res in aa:
        opts = CODONS[res]
        if len(opts) == 1: out += opts[0]; continue
        best = None
        for c in opts:
            w = (out + c)[-50:]
            dev = abs(sum(x in "gc" for x in w)/len(w) - target)
            if best is None or dev < best[0]: best = (dev, c)
        out += best[1]
    return out
src = GPATH.read_text(); parts = probe.components(src)
aa = probe.fusion(parts, ["G"*20]*4)
nt = build(aa); assert len(nt) == 2766 and probe.windows_ok(nt)
for delta in (0, 1, 2, 3):
    obs, msg = probe.run_grader(GPATH, nt + "A"*delta)
    print(delta, len(nt)+delta, obs, msg)
EOF
    && "$D/v/bin/python" "$D/r.py"
0 2766 pass -
1 2767 pass -
2 2768 pass -
3 2769 fail End of gBlock must match snap protein.
```

VERDICT: maxnt-refuted
