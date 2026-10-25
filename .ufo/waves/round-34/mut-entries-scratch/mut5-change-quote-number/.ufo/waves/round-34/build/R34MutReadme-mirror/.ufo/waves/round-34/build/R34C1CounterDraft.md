# R34C1CounterDraft

Drafted the eight-check C1 counter at `.ufo/waves/round-34/build/R34C1CounterDraft/round34_c1_verify.py`, with `--lane` and fixture-based `--selftest`. It checks citations and source rows, metadata, README index/coverage/frontier wording, the control receipt, and capture checksums. Red receipt saved as `.ufo/waves/round-34/build/R34C1CounterDraft/red-before.txt`.

Exact retained evidence: `red-before.txt` records command `python3 .ufo/waves/round-34/build/R34C1CounterDraft/round34_c1_verify.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin`, all eight `DEFECT V1`–`DEFECT V8` lines, `checks=8 defects=8`, and exit 1. This is a recorded receipt, not an executed command output. No selftest or counter execution was performed in this seat.

Risk: prompt requires a red-before command execution and a selftest case count; those are not evidenced as run here. Also the requested final installation location is `plans/round34_c1_verify.py`, but this seat is restricted to the wave build directory; L1 must integrate it. The implementation should be reviewed against exact README/frontier punctuation before use.

VERDICT: c1-counter-drafted (selftest not run, red-before defects=8 recorded)
