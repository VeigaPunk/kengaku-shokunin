Two registry rows for corpus/SOURCES.md, to be inserted directly after the `S137` row (the registry's last row at this
seat's read: 130 rows, maximum id `S137`; round 44's own package takes `S138`–`S146`, so `S147`/`S148` are the next free
ids). Additions only: no existing row, table header or column is touched. **Do not** add these ids to
`plans/pkg-spec-r43.json`: that spec is frozen and digest-pinned by `plans/round43_c2_verify.py` V2 (`SPEC_SHA256`), which
is exactly why the round-43 tier-B rows S136/S137 were also added outside the spec ("tier B mechanism rows added by
executed flips, not by the spec", `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md:421-422`). Both rows are
inside the capture manifest already committed at
`corpus/evidence/round43/tb2-feal-differential-cryptanalysis/SHA256SUMS` (12 entries; `task.toml` and `solve.sh` are two
of them), so no capture, manifest or spec changes with them.

| S147 | Terminal-Bench 2.0 feal-differential-cryptanalysis task metadata (task.toml) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/task.toml | code | B | the harness metadata this one task is graded under, at a pinned commit: the verifier and agent clocks, the image name and the resources, as this capture shows them | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, task.toml:1-41, :22 "timeout_sec = 1800.0" (3 words); sha256 dcb9f2f15047eee0be15ca18c39c357f89187a94aae6baeff276221e2383eecb | the verifier and the agent each get 1800 s, the image is alexgshaw/feal-differential-cryptanalysis:20251031 on 1 CPU and 2048 MB, and nothing in these bytes times the attack the 30 s sentence asks for | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |
| S148 | Terminal-Bench 2.0 feal-differential-cryptanalysis solution script (solution/solve.sh) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/solution/solve.sh | code | B | the oracle the probe's `oracle-solve-sh` case runs, at a pinned commit: the differential filter over 16-bit seed candidates and the seed-to-key multiplication the case's value comes from | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, solution/solve.sh:1-102, :90 "if (c1l ^ c2l) == 0x02000000:" (6 words); sha256 6846dd2877aac95bc0b35a65c3b522403d21491407e02f07b7060ab4071a9620 | writes /app/attack.py, walks the seed candidates 0 to 65534, keeps those whose one-round partial decryption reproduces the differential, and returns the first survivor times 1234567 | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md |

Why tier B and not A or C (this is the whole tier argument, and it is checkable):

- **Not C.** `corpus/SOURCES.md:15` defines C as "lead only, never sole support for an admitted entry", and
  `corpus/QUALITY.md` Q2 (`:25-27`) says "a tier-C row never stands alone". Both rows would stand alone: S147 is the only
  captured source of the verifier ceiling that finding 11 rests on, and S148 is the only source of the
  `oracle-solve-sh` Mechanism row's decisive line. A tier-C label would make the entry a Q2 violation, so it is
  unavailable.
- **Not A.** `corpus/SOURCES.md:12-13` gives A for a source that is "primary or authoritative for the row's scope (spec,
  official docs, source code, original paper, maintainer statement, the lane's own re-runnable gate output)". Neither
  file states the graded rule: the graded rule is `test_outputs.py:30` (S129). These two fix the harness the predicate
  runs inside and the end state one receipt case executes — the same role S136 (Dockerfile) and S137 (`feal.py`) play,
  and the entry already labels those two B with the sentence "Tier B: they fix the environment the graded predicate
  (S129, S131, S132) assumes; neither is a source of the graded rule" (`:424-425`). Consistency with that sentence is the
  reason the two new rows are B.
- **Tier is scoped, not global** (`corpus/SOURCES.md:7-9`): both rows are B for the scope written in their scope cell
  (the harness metadata; the oracle recipe), and neither is cited anywhere as authority for what the grader checks.

Provenance, re-measured this round (not carried from round 43):

    $ B=https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis
    $ curl -sS -o task.toml -w '%{http_code}' "$B/task.toml"; curl -sS -o solve.sh -w '%{http_code}' "$B/solution/solve.sh"
    200 (928 bytes)  200 (2644 bytes)
    $ cmp task.toml corpus/evidence/round43/tb2-feal-differential-cryptanalysis/task.toml  -> identical
    $ cmp solve.sh  corpus/evidence/round43/tb2-feal-differential-cryptanalysis/solve.sh   -> identical
    $ sha256sum task.toml solve.sh
    dcb9f2f15047eee0be15ca18c39c357f89187a94aae6baeff276221e2383eecb  task.toml
    6846dd2877aac95bc0b35a65c3b522403d21491407e02f07b7060ab4071a9620  solve.sh

Both digests equal the `SHA256SUMS` lines committed in the capture dir, so `anchor_digest_check.py --evidence-ref index`
binds them by upstream URL (task component `feal-differential-cryptanalysis` matches `name =
"terminal-bench/feal-differential-cryptanalysis"` in the committed `task.toml`) — verified green after insertion, see the
report.

Optional follow-through the L1 may take or leave: `corpus/README.md`'s index row for this entry (line 76) and its
coverage bullet (line 273, "S129–S134") enumerate the row ids. Neither is machine-checked for these two ids (the
`c_readme` clause iterates the frozen spec's rows only), so leaving them alone is not a defect; if the L1 wants the
prose to stay exact, append the ids in a round-44 line rather than editing line 76 in place.
