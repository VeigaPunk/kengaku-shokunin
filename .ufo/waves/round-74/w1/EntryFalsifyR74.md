# EntryFalsifyR74 — admission audit of held knowledge entries in `corpus/knowledge/` (round 74, wave w1)

Seat: reviewer (leaf member, no subagent dispatch). Axes judged: coverage, calibration (admission-status
audit, not a claim score). Lane tip at audit: `cea7ebf37df3e3e7ecf3d9e375f4e35d35c0cd30`; all four audited
files are tracked and byte-clean at that tip (`git status --porcelain` and `git diff --stat` over
`corpus/knowledge/` are empty), so working-tree reads equal committed bytes. Read-only: no git/jj mutation,
no clone, no scratch created (nothing to clean under `/fast/scratch/hyaku/kengaku-r74/EntryFalsifyR74/`).

## Primary finding — all four entries carry `admission: hold`, and the hold is current

1. **`corpus/knowledge/tb2-hf-model-inference-offline.md:6`** —
   `admission: hold — the QUALITY Q13/Q14 second-seat re-read is not yet on record; see corpus/lessons/round-71.md ## Gate (Admission status).`
   Corroborated current: `corpus/lessons/round-71.md:63-67` (`**Admission status (QUALITY Q13/Q14): HOLD.** …
   landed and indexed but **not admitted**`); `corpus/lessons/round-71-verifier-spotcheck.md:159-161`
   ("stays at `admission: hold`"); `corpus/lessons/round-73.md:33-36` ("Earlier HF candidates remain held …
   not newly admitted here"); `corpus/lessons/round-74.md:23` (round-71/72 candidate remains held);
   `LOG.md:2673` ("landed, `admission: hold` pending Q13/Q14"). No later admission found.

2. **`corpus/knowledge/tb2-hf-model-inference-provenance.md:6`** —
   `admission: hold — the QUALITY Q13/Q14 second-seat re-read is not yet on record from a w2/falsify registry; see corpus/lessons/round-72.md ## Gate (Admission status).`
   Corroborated current: `corpus/lessons/round-72.md:11-12` ("**not admitted**: `admission: hold`") and
   `:102-107` (`**Admission status (QUALITY Q13/Q14): HOLD.**`); `round-72-verifier-spotcheck.md:166-169`
   ("stays `admission: hold`"); `round-73.md:33-36` names it explicitly as still held.

3. **`corpus/knowledge/instrument-registry-derivation.md:5`** —
   `admission: hold — requires a qualifying second-seat reread satisfying corpus/QUALITY.md Q10/Q13/Q14; no admission is inferred from structural audit output.`
   Corroborated current: `corpus/lessons/round-73.md:29-32` ("Admission remains hold pending a qualifying
   complete Q10/Q13/Q14 reread; source admission is not entry admission"); `round-74.md:23` (round-73
   candidate remains held).

4. **`corpus/knowledge/registry-argv-and-flag-audit.md:8`** — frontmatter `admission: hold`, with the
   hold reason in body §3 (Admission boundary): "complete runtime certification requires an outside
   non-author spot-check and execution verification per Q13/Q14." Corroborated current:
   `corpus/lessons/round-74.md:22` ("**Held knowledge candidate:** … (admission: hold)"). Grounding is on
   record: `corpus/SOURCES.md:266` — S250, argparse docs, tier A, kind docs, capture
   `corpus/evidence/round74/sources/argparse-docs.html`, sha256 `ad9095cd…`, `used-by` names this entry —
   matching the claims file's frontier step.

Rule source confirmed: `corpus/QUALITY.md:97` (Q13 — admit lands only after its second-seat re-read is on
record in the admitting commit's tree, cited by repo-relative path, non-writer seat, no generic
references) and `:111` (Q14 — qualifying roles are exactly reviewer/scout/critic/sentinel/revenger;
identity authority). No entry claims admission anywhere in the four files; the only `admit` token in the
argv candidate is the hold boundary itself.

## Findings (severity-ordered; none contradicts the hold)

- **LOW — the round-74 candidate lacks the Q1 line triad its held peers carry.**
  `registry-argv-and-flag-audit.md` has frontmatter `source_ids: [S250]`, a body `source:` line, and
  `admission: hold`, but **no `verified-at:` line, no `recheck:` line, and no `writer:` line** (grep for
  `^verified-at:|^recheck:|^writer:` → 0 hits). Q1 (`corpus/QUALITY.md`, Admission bar) requires
  `source:`/`verified-at:`/`recheck:` as the first three lines; the three older entries all carry them
  (offline :1-3, provenance :1-3, derivation :1-3). Q13's checker also reads a candidate `writer:`
  different from the re-read seat at admission time. [INFERENCE] This blocks nothing while held, but the
  entry cannot pass Q1/Q13 as byte-written today; fix before any admission motion.
- **LOW — same-shape gap on `instrument-registry-derivation.md`:** Q1 triad present (:1-3), but no
  `writer:` line (0 hits for `^writer:`). The round-73 lesson names the draft writer
  (`KnowledgeEntryR73`, L1 integration) in prose only; Q13 wants it on the candidate.
- **INFO — index state of the two newer held candidates diverges from the r71/r72 precedent.**
  `corpus/README.md` has zero occurrences of `registry-argv-and-flag-audit` (no "What's here" row, and no
  Round-74 supporting-artifacts section yet), and `instrument-registry-derivation` appears only in the
  Round-73 artifacts section (`README.md:832-833`), not the "What's here" table — whereas the two HF
  entries are indexed at `README.md:95-96` while held. Q7 binds the index row to the *admitting* commit,
  so this is precedent divergence, not a rule break at hold time.
- **INFO — `corpus/lessons/round-74.md:23`'s "earlier held" line names the offline and derivation entries
  but not `tb2-hf-model-inference-provenance.md`.** Its hold remains on record via its own :6 line,
  `round-72.md:102-107` and `round-73.md:33-36`; the omission is cosmetic.

## Residual risk and verification gaps

- Status is a property of bytes at a revision: the hold verdicts above bind tip `cea7ebf3`; any later
  commit can change an entry's frontmatter, and this audit does not pin the future.
- I did not run `plans/gate_timing_check.py` (Q13's own instrument): confirming absence of any admitting
  commit is a tree/lesson read, and running admission machinery is outside this seat's read-only audit
  scope. The lessons' own recorded checker outcomes (`no admit rows … failed=1`, spot-check receipts) are
  cited as records, not re-executed here.
- No LSP server applies to markdown corpus prose; all evidence is direct file/line reads at a clean tip,
  not grep-as-semantic-proof.
