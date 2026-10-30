# S3GateQuotes — scoped findings (round 55 w1, 2026-10-30)

Deliverable: `.ufo/waves/round-55/w1/S3GateQuotes/gate-block.md` — the `## Gate` table rows
S201 + S202 (5 columns, lesson format) + flip-check line, ready for L1 splice into
`corpus/lessons/round-55.md`.

Verified before writing (read-only GETs at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`):
- S201 quote `assert sorted(move) == sorted(["g2g4", "e2e4"])` — verbatim prefix of `tests/test_outputs.py:25` (full line adds `, "File is wrong"`); sha256 `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` matches the frozen claim pin.
- S202 quote `If there are multiple winning moves, print them all, one per line.` — verbatim in `instruction.md:1`; sha256 `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` matches the lesson.
- Flip-check grounded: `chess-best-move/tests/test.sh` sha256 `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` is byte-identical to S109's `regex-log/tests/test.sh` (same hash, fetched both) — the runner row drop as duplicate is factual.

Observations (data only, not fixed): the lesson's drafted S201 row quotes the longer assertion
form; this block uses the seat spec's shorter exact quote — splice shortens the lesson's quote
cell. `corpus/SOURCES.md` has pre-existing format drift (`||` prefix, stray `*` on the S109
line). No defect in this seat's own output. Scratch removed; no installs; no product/judge/
git surface touched. Full detail: `.ufo/waves/round-55/w1/S3GateQuotes/report.md`.
