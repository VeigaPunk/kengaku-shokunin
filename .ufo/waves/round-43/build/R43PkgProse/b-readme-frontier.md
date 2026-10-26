# block b — corpus/README.md `## Frontier`, insert after the round-42 sub-bullet (`:378`), before `- **Contamination transparency cards**` (`:379`)

Names `feal-differential-cryptanalysis` inside `## Frontier` (C2 V9(d)); narrows the TB2 clause to **9 of 89 read**;
keeps the three open clauses in the round-37..42 form (remaining TB2 graders, SWE-bench Pro V2 beyond round 31,
runtime task validity that `PROVINCE.md` refuses).

  - *Partly discharged round 43 (2026-10-26):* `knowledge/tb2-feal-differential-cryptanalysis-grader.md` reads and
    executes a ninth Terminal-Bench 2.0 task's scoring code (`feal-differential-cryptanalysis/tests/test_outputs.py`
    with `tests/feal_module.c`, `tests/feal.c` and `tests/test.sh` @ `2fd12b88`; S129–S134) against its
    `instruction.md`, probe `plans/feal_probe.py`, receipt `corpus/evidence/round43/feal-probe.txt`. The graded state
    is a class the lane had not executed before: an agent-authored **Python module imported into the grader's own
    interpreter and called** (`test_outputs.py:22-24`), beside the reference C extension `feal_in_c` that the grader
    builds first (`:20`) and whose public `get_keys()` holds the answer (`feal_module.c:51`), with pytest's exit
    status as the whole verdict (`test.sh:17-25`). Six of the eight observed passes never recover a key — the
    reference `get_keys()[5]`, an object whose `__eq__` is always True, a fake `feal_in_c` in `sys.modules`, a
    rebound `get_keys`, `os._exit(0)` before the assertion, and a libc replay of `srand(time(NULL))` over the 16-bit
    per-key seed (`feal.c:56-67`) — and a 45 s oracle passes (`slow-oracle-45s`) although `instruction.md:3` asks
    under 30 s and `README.md:35` says the test confirms that limit, while nothing times the call (receipt:15-21).
    `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`. The "Terminal-Bench 2.0's"
    clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (9 of 89 read),
    for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md`
    refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent
    behaviour.
