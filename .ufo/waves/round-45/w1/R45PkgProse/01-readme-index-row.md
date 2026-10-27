# Item 1 — `corpus/README.md` knowledge index row for the eleventh grader

**Surface:** `corpus/README.md` knowledge table (`| \`knowledge/…\` | … |`) — the row for
`knowledge/tb2-password-recovery-grader.md`, modelled on the round-44 row at `:77`.

**Anchor (byte-exact, must be read before editing):**

```
file: corpus/README.md
line: 77   (length 812 bytes; sha256 c629106eb51779429eabbe413f4260f4c110570ffe73fe6f4cb4426417516092)
      | `knowledge/tb2-feal-linear-cryptanalysis-grader.md` | … | Pinned at terminal-bench-2 `2fd12b88`: S138, S139, S140, S141, S142, S143, S144, S145, S146; captures + `SHA256SUMS` in `evidence/round44/tb2-feal-linear-cryptanalysis/` |
line: 78   | `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
```

**Edit:** insert exactly one new line between `:77` and `:78` (nothing else changes).

```diff
@@ corpus/README.md:77-78 @@
 | `knowledge/tb2-feal-linear-cryptanalysis-grader.md` | A tenth Terminal-Bench 2.0 task grader … | Pinned at terminal-bench-2 `2fd12b88`: S138, … captures + `SHA256SUMS` in `evidence/round44/tb2-feal-linear-cryptanalysis/` |
+| `knowledge/tb2-password-recovery-grader.md` | An eleventh Terminal-Bench 2.0 task grader read and executed, and a grader class distinct from round 44's: `password-recovery` grades an **agent-written guess list** — `test_outputs.py:14` reads `/app/recovered_passwords.txt` and splits it on `"\n"` after `.strip()`, and `:18` asserts that one embedded 23-character constant, `8XDP5Q2RT9ZK7VB3BV4WW54`, is a whole line of that list — so line order, guess count, duplicates and CRLF endings are invisible while a guess concatenated with decoys on one line fails (`constant-joined`) and the file's own `PASSWORD=` form fails (`password-eq`); the constant is printed by the task's own `README.md:31` and written into the image by `setup.sh:25`, so a 1001-line list of decoys (`decoys-1000`) and a bare copy of the published answer (`constant`) both pass, and the `len(guesses) > 0` assert at `:16` cannot fire on any input; the executable reading is in `## Predictor` | Pinned at terminal-bench-2 `2fd12b88`: S149, S150, S151, S152, S153, S154, S155, S156; captures + `SHA256SUMS` in `evidence/round45/tb2-password-recovery/` |
 | `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
```

**Checks this row is written against (read from the frozen gate, not guessed):**
`plans/pkg_gate.py:29` `INDEX_ROW = re.compile(r"^\|\s*`(knowledge/[^`]+\.md)`\s*\|")`; `c_readme`
(`plans/pkg_gate.py:232-256`) requires exactly one row for the entry name, that row to cite **every**
registry id (`S149`…`S156`), and `knowledge-files == index-rows` afterwards. The row above starts
`| \`knowledge/tb2-password-recovery-grader.md\` |`, cites all eight ids, and adds exactly one row for the one
new file.

**Paste preconditions:**
1. None of the eight ids may be renumbered by `R45PkgRows`; if that seat's registry rows differ in count, this
   row's id list is the thing to re-cut, not the prose.
2. The row names case outcomes (`constant` and `decoys-1000` pass, `constant-joined` and `password-eq` fail).
   Those are the **frozen predictions** (`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt:12,22,
   14,23`); paste only when `corpus/evidence/round45/password-recovery-probe.txt` reports `mismatches=0`, i.e.
   the observations match them. If any of the four disagrees, rewrite the row to the observed verdict — the
   receipt wins over this draft.
