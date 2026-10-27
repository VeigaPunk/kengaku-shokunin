## R46W2C3Rerun — C3 rerun

Revision: 42d5043afac952fcb43bf4798757785dd258cf85 (clean --no-local clone; verified TOP=/fast/scratch/hyaku/kengaku-r46/R46W2C3Rerun/lane, HEAD=42d5043afac952fcb43bf4798757785dd258cf85).

Axes: coverage (counter predicate and probe repeatability/equality).

### Counter
Command, twice: `envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round46_c3_verify.py --lane "$S/lane"`.

Both runs emitted identical predicate-relevant output; both exit 1. ENVELOPE start/end succeeded and local_bin_content_before/after were equal (`7747d38e2042d398`); neither returned exit 4 / INVALID. Evidence: counter1.txt and counter2.txt.

Each rerun V7 DEFECT: unparsed instruction.md rows for both-print and toolchain, tags missing. V8 DEFECT order_exit=1. Result `checks=13 defects=2`, `PREDICATE C3 fail`. Available landing receipt `integrate/c3-landing.txt` records the same defects and predicate. Requested `integrate/tip-c3.txt` does not exist (diff said No such file); c3-landing.txt is the available receipt and matches substantive output.

### Probe
Command: `envelope.sh "$S/env" python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/polyglot_c_py_probe.py --lane "$S/lane"`; exit 0. Output: cases=18, observed_pass=7, observed_fail=11, mismatches=0. Receipt probe.txt. Raw diff with corpus/evidence/round46/polyglot-c-py-probe.txt differs only by the wrapper ENVELOPE lines (command/start/end); after excluding these wrapper lines, probe payload is byte-equal. Raw DIFF_EXIT=1 due to wrapper lines.

No tools installed/updated.

VERDICT: c3-rerun-predicate-fail-probe-equal-yes
