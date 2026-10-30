# R55-W1 M1RegistryMutants — scoped findings

Mutation probe of the frozen r52-C2 production counter `plans/round52_c2_registry.py`
(sha256 `9e6f41a4…`, lane HEAD == freeze commit `80afa613…`, worktree clean; bytes copied to
scratch, never edited in place). Detector: `python3 <counter-copy> --lane <fixture>` on seven
scratch fixtures (one focused per leg + one combined), identical on pristine/mutated/restored
bytes; baseline matched frozen expectations on all seven (conclusive).

**Verdict: 6/6 single-defect mutants killed — every advertised leg of the R52-C2 counter is
demonstrated; no coverage gap in the counter's verdict path.**

| mutant | leg | kill evidence |
|---|---|---|
| M1 `missing = []` always | MISSING | focused exit 1→0; combined `MISSING 2→0`, all 4 other families unchanged |
| M2 `not all(r)` → `not any(r)` (blank cells ignored; separator guard drops fully-empty rows so INCOMPLETE goes dead) | INCOMPLETE | focused exit 1→0; combined `INCOMPLETE 1→0`, others unchanged |
| M3 `entry_missing = []` | ENTRY-MISSING | focused exit 1→0; combined `ENTRY-MISSING 1→0`, others unchanged |
| M4 `selftest_unbacked()` → `return False` | SELFTEST-UNBACKED | focused exit 1→0; combined `SELFTEST-UNBACKED 1→0`, others unchanged |
| M5 `duplicate = []` | DUPLICATE | focused exit 1→0; combined `DUPLICATE 1→0`, others unchanged |
| M6 knowledge glob → `pass` (advertised universe drops `corpus/knowledge/*.md`) | universe | focused exit 1→0; combined MISSING line `plans/kb_tool.py` vanishes (2→1, orphan still caught), others unchanged |

Kill rule applied: focused exit flip 1→0 with the family →0 AND combined loses exactly its own
family (orthogonality). Mutant sha256s and full stdout details:
`.ufo/waves/round-55/w1/M1RegistryMutants/mutants.md` + `receipts.json`.

Restoration: production sha256 identical before/after probe; restored-bytes run reproduces the
pristine combined fingerprint byte-for-byte (exit 1, `PREDICATE R52-C2 fail`).

**Coverage finding (finding, not a fix):** the counter's shipped `--selftest` battery catches
only M1/M2 and is blind to M3/M4/M5/M6 — the ENTRY-MISSING, SELFTEST-UNBACKED, DUPLICATE and
knowledge-file legs have no fixture inside the tool's own battery. For R55-C1 this means the
frozen after-predicate's `--selftest` leg demonstrates 2 of the 6 printed families; the other
four are demonstrated only by external fixtures (as here). Production bytes untouched; no
contract change implied or made.

Receipts: `mutants.md`, `receipts.json`, `harness.py`, `report.md` under
`.ufo/waves/round-55/w1/M1RegistryMutants/`; scratch `/fast/scratch/hyaku/kengaku-r55/M1RegistryMutants/` deleted.
