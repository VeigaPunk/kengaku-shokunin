# ProvenanceRederive — round 69, w1 (R69-C2, E3)

Axes: coverage and calibration. Scope: build the R69-C2 **E3 receipt-provenance erratum** from
committed bytes only, and show it closes E3 under the instrument the round froze
(`plans/round69_c2_routed_defects.py`). No predicate, case table, vector, kill rule, target,
gate, or tracked file was edited.

Artifacts written: `.ufo/waves/round-69/w1/provenance-erratum.txt` (this seat's named file) and
this report. Nothing else in the lane was written. Scratch: `/fast/scratch/hyaku/kengaku-r69/ProvenanceRederive`
(deleted at close; receipts are copied below).

## 1. Inputs read

- `plans/round-69-claims.md`, R69-C2 (E3) in full, plus the R69-C1 section for context.
- `.ufo/waves/round-68/w2/GateReverify/committed-bytes.txt` — six lines, verbatim:

```text
plans/round68_c2_correction_gate.py sha256=1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d HEAD-equals-working=True
plans/round-67-claims.md sha256=d465f601cc05cd4df777d1e7432d3327c517afbcf7436b6025538e61de4c9be4 HEAD-equals-working=True
corpus/evidence/round68/r67-probe-selftest.txt sha256=5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467 HEAD-equals-working=True
plans/round67_c1_pipeline_probe.py sha256=03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e HEAD-equals-working=True
SKILL.md sha256=3fe9a6d0efa60d0f26ff488f99ed73b400b4faa2d6c9318da801141acb8ed979 HEAD-equals-working=True
corpus/evidence/round67/pipe/a1-mutants.txt sha256=29a9ba11d8c79a9baecb8c87bcbf267a96f42d6eec9822b47d395b7a116e5880 HEAD-equals-working=True
```

- Container: `sha256sum .ufo/waves/round-68/w2/GateReverify/committed-bytes.txt` →
  `b45c9a1155a21b71be57cab68c3bd09e7d4708344c7057b716330945a264470e`; it is tracked, and
  `git log --oneline -1 -- <that path>` → `1ec2e60a round-68 attempt 2: re-derivation, …`.
- `corpus/lessons/round-68-verifier-spotcheck.md` §5 items 1–7 (item 3 is this defect) and
  `.ufo/waves/round-68/w2/GateReverify.md` (the receipt's own report).

## 2. Revisions (both exist)

```text
argv: git -C L cat-file -e 27f649f8^{commit}      rc=0
argv: git -C L cat-file -e 1ec2e60a^{commit}      rc=0
argv: git -C L rev-parse --verify 27f649f8^{commit}
27f649f874ae96d7cf7f4f3e6ea4d0810f0d2f91
argv: git -C L rev-parse --verify 1ec2e60a^{commit}
1ec2e60aefc407f5b244dae46026d120010a3895
argv: git -C L log -1 --format='%H %ad %s' --date=iso-strict 27f649f8
27f649f874ae96d7cf7f4f3e6ea4d0810f0d2f91 2026-11-03T20:30:43-03:00 round-68 attempt 2: freeze A3 (capability-table completeness gate + red receipt)
argv: git -C L log -1 --format='%H %ad %s' --date=iso-strict 1ec2e60a
1ec2e60aefc407f5b244dae46026d120010a3895 2026-11-03T20:42:04-03:00 round-68 attempt 2: re-derivation, report-contract + capability gates, corrections (A4-A7), wave w2 evidence
argv: git -C L merge-base --is-ancestor 27f649f8 1ec2e60a   rc=0
argv: git -C L rev-list --count 27f649f8..1ec2e60a          → 1
argv: git -C L rev-list --count 1ec2e60a..27f649f8          → 0
```

Revision offsets at read time: lane HEAD `b288e8e0` (round-69 freeze), which has
`1ec2e60a` and `a518980e` as ancestors.

## 3. Per-input re-derivation (exact argv and raw output)

Each side was produced with `git -C L show <rev>:<path> | sha256sum`; existence was also checked
per side with `git -C L cat-file -e <rev>:<path>` (rc 0 for all twelve checks — the full loop is in
§6, all `rc=0`). Blob ids were read with `git -C L rev-parse <rev>:<path>` as an independent
identity cross-check (equal sha256 ⇔ equal blob id).

```text
--- INPUT plans/round68_c2_correction_gate.py
git show 27f649f8:… | sha256sum → 1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d  rc=0 (9226 bytes)
git show 1ec2e60a:… | sha256sum → 1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d  rc=0 (9226 bytes)
blob 7356d43c7dcbe193ca0159c0989505082ca76ab9 both sides        SAME
--- INPUT plans/round-67-claims.md
git show 27f649f8:… → d465f601cc05cd4df777d1e7432d3327c517afbcf7436b6025538e61de4c9be4  rc=0 (15276 bytes)
git show 1ec2e60a:… → d465f601cc05cd4df777d1e7432d3327c517afbcf7436b6025538e61de4c9be4  rc=0 (15276 bytes)
blob 178cf276475ba629377506b4d73ba64f80bfe233 both sides        SAME
--- INPUT corpus/evidence/round68/r67-probe-selftest.txt
git show 27f649f8:… → 5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467  rc=0 (663 bytes)
git show 1ec2e60a:… → 5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467  rc=0 (663 bytes)
blob 0dd738befcdbe1b0a8149f24cb973e2f4245b2db both sides        SAME
--- INPUT plans/round67_c1_pipeline_probe.py
git show 27f649f8:… → 03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e  rc=0 (16130 bytes)
git show 1ec2e60a:… → 03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e  rc=0 (16130 bytes)
blob 5c7402f729f9a740b1164293033b5b3cfd748208 both sides        SAME
--- INPUT SKILL.md
git show 27f649f8:… → 3fe9a6d0efa60d0f26ff488f99ed73b400b4faa2d6c9318da801141acb8ed979  rc=0 (299445 bytes)
git show 1ec2e60a:… → 544ad892c46a500d68928f21b06a8a26d03506d7dd4732649c20f8f6c15883c5  rc=0 (300464 bytes)
blob 2f0f896610a2bae0ba326e51b911cd001171ca7e → ead8e1437352ba8ffd0a827278cccc721098e6cd   DIFF
--- INPUT corpus/evidence/round67/pipe/a1-mutants.txt
git show 27f649f8:… → 29a9ba11d8c79a9baecb8c87bcbf267a96f42d6eec9822b47d395b7a116e5880  rc=0 (1883 bytes)
git show 1ec2e60a:… → 29a9ba11d8c79a9baecb8c87bcbf267a96f42d6eec9822b47d395b7a116e5880  rc=0 (1883 bytes)
blob 7d17cd1b4bed4086a08497deb332a73586cf6c68 both sides        SAME
```

Independent confirmation of the differing set, without hashing:

```text
argv: git -C L diff --stat 27f649f8 1ec2e60a -- <the six paths>
 SKILL.md | 1 +
 1 file changed, 1 insertion(+)
argv: git -C L diff --numstat 27f649f8 1ec2e60a -- <the six paths>
1	0	SKILL.md
argv: git -C L diff 27f649f8 1ec2e60a -- SKILL.md
@@ -685,6 +685,7 @@
+| `round66_c1_tensor_probe` | probe | `python3 plans/round66_c1_tensor_probe.py --check-receipt …`
argv: git -C L diff --shortstat 27f649f8 1ec2e60a
 145 files changed, 11080 insertions(+), 42 deletions(-)
```

So: **five inputs are byte-identical across the two revisions; exactly one — `SKILL.md` — differs**,
`3fe9a6d0efa60d0f26ff488f99ed73b400b4faa2d6c9318da801141acb8ed979` at `27f649f8` versus
`544ad892c46a500d68928f21b06a8a26d03506d7dd4732649c20f8f6c15883c5` at `1ec2e60a`. The 145-file
whole-tree delta between the two revisions is why the bound set matters: `DIFFERS` is a statement
about the six named inputs only, not about the two trees.

## 4. The erratum file

`.ufo/waves/round-69/w1/provenance-erratum.txt` (9 lines, 1174 bytes, LF only, ASCII, no trailing
whitespace, no blank lines; sha256 `9261c8d73e939b7859746d8aae6a84b1611e21587cd2330202d14ba36341831c`):

```text
TREE 27f649f8
LANDING 1ec2e60a
INPUT plans/round68_c2_correction_gate.py at-tree=1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d at-landing=1d9fd08f11a10b30f7b504d13b803c3fbd1136157559407d55177de16bed879d
INPUT plans/round-67-claims.md at-tree=d465f601cc05cd4df777d1e7432d3327c517afbcf7436b6025538e61de4c9be4 at-landing=d465f601cc05cd4df777d1e7432d3327c517afbcf7436b6025538e61de4c9be4
INPUT corpus/evidence/round68/r67-probe-selftest.txt at-tree=5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467 at-landing=5a15dfd2ec8f2f114d49e344330c5b6ea06115ca95842e200c4e27c0387e7467
INPUT plans/round67_c1_pipeline_probe.py at-tree=03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e at-landing=03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e
INPUT SKILL.md at-tree=3fe9a6d0efa60d0f26ff488f99ed73b400b4faa2d6c9318da801141acb8ed979 at-landing=544ad892c46a500d68928f21b06a8a26d03506d7dd4732649c20f8f6c15883c5
INPUT corpus/evidence/round67/pipe/a1-mutants.txt at-tree=29a9ba11d8c79a9baecb8c87bcbf267a96f42d6eec9822b47d395b7a116e5880 at-landing=29a9ba11d8c79a9baecb8c87bcbf267a96f42d6eec9822b47d395b7a116e5880
DIFFERS SKILL.md
```

Cross-check against the round-68 receipt: all six `at-tree` values equal the six `sha256=` values
declared in `committed-bytes.txt` (0 mismatches, same order); the `HEAD-equals-working=True` flags
are consistent with the `at-tree` column because the receipt was taken at that tree.

Strict-format measurement:

```text
bytes=1174 sha256=9261c8d73e939b7859746d8aae6a84b1611e21587cd2330202d14ba36341831c
has_CR=False ends_with_LF=True line_count=9 ascii_only=True
any_trailing_whitespace=False any_blank=False
1: tokens=2 TREE value=27f649f8
2: tokens=2 LANDING value=1ec2e60a
3..8: tokens=4 INPUT path=… at_tree_len=64 at_land_len=64 at_tree_prefix_ok=True at_land_prefix_ok=True
9: tokens=2 DIFFERS value=SKILL.md
first_line_is_TREE=True last_line_is_DIFFERS=True
```

## 5. Gate compatibility — the committed E3 block, executed verbatim

The E3 block was extracted from the frozen instrument itself
(`plans/round69_c2_routed_defects.py`, source lines 183–225) and executed unmodified with
`PROVENANCE` pointed at the W file (the block's `ppath = root / PROVENANCE` yields the absolute
path, while `git_show` still runs against the real lane). Arms B–H are controls: each is a
deliberate corruption of the same bytes.

```text
[consts] TREE=27f649f8 LANDING=1ec2e60a PROVENANCE=corpus/evidence/round69/c2-receipts/provenance-erratum.txt
ARM A committed W file:                  E3 ok inputs=6 differs=['SKILL.md'] problems=[]
ARM B no DIFFERS line:                   E3 defect problems=["differs-set got=[] want=['SKILL.md']"]
ARM C extra DIFFERS:                     E3 defect problems=["differs-set got=['SKILL.md', 'plans/round-67-claims.md'] want=['SKILL.md']"]
ARM D flip one hex of SKILL at-landing:  E3 defect problems=['landing-sha:SKILL.md']
ARM E wrong TREE short rev:              E3 defect problems=['tree-line']
ARM F extra column on SKILL line:        E3 defect problems=['malformed:INPUT SKILL.md at-tree=3fe9a6d0efa60d0f26ff488f99ed73b400b4f', "differs-set got=['SKILL.md'] want=[]"]
ARM H no INPUT lines:                    E3 defect problems=['no-inputs']
REPLICA-SELFTEST all-controls-fail=True green-arm-ok=True
```

### Real instrument, scratch clone

A single `git clone --shared L /fast/scratch/.../laneclone` (toplevel asserted equal to the clone
dir before any write) at `b288e8e0`, with the erratum installed as an untracked file at E3's real
path. No other C2 correction is present in the clone.

```text
== erratum ABSENT (do-nothing control for this seat)
E1 defect rows=0/4 missing=['round68_c1_pypi_finish', 'round68_c2_correction_gate', 'round68_report_contract', 'round68_capability_table'] thin=[]
E2 defect headings=0 q50=False round68-lesson=False spotcheck=False
E3 defect corpus/evidence/round69/c2-receipts/provenance-erratum.txt missing
E4 defect verified-at-lines=1 last-names-landing=False
E5 defect strict-lines=0
E6 defect rerecord-lines=0
E7 defect problems=['corpus/evidence/round69/gates/depth-gate.txt:missing', 'corpus/evidence/round69/gates/trio.txt:missing']
DEFECTS n=7
PREDICATE R69-C2 fail
gate_rc=1

== erratum PRESENT (only this correction installed)
E3 ok inputs=6 differs=['SKILL.md'] problems=[]
DEFECTS n=6
PREDICATE R69-C2 fail
gate_rc=1
```

`diff` of the two runs: exactly two lines change — the E3 line and the `DEFECTS n=` line
(`7 → 6`). `diff` of the absent run against committed `.ufo/waves/round-69/c2-red-before.txt`
(minus its trailing `rc=1`): identical.

### A second, independent erratum already sits at the corpus path (not written by this seat)

At 21:07, after writing the W file, a re-read of the lane found
`corpus/evidence/round69/c2-receipts/provenance-erratum.txt` present and untracked (mtime 21:06:32,
i.e. earlier than this seat's write), sha256
`fad393d0709067d0e5a95fd4e080db6e362a8fe75ec369de0796cfa868b25652`, 9 lines, 1174 bytes. `diff -u`
against the W file shows **one difference: line order** — the corpus copy places `DIFFERS SKILL.md`
between the `SKILL.md` INPUT line and the `a1-mutants.txt` INPUT line; every `at-tree`/`at-landing`
value and the `TREE`/`LANDING` values are identical. Both files pass the committed E3 block verbatim:

```text
W      sha256=9261c8d73e939b7859746d8aae6a84b1611e21587cd2330202d14ba36341831c  E3 ok inputs=6 differs=['SKILL.md'] problems=[]
CORPUS sha256=fad393d0709067d0e5a95fd4e080db6e362a8fe75ec369de0796cfa868b25652  E3 ok inputs=6 differs=['SKILL.md'] problems=[]
```

E3 parses by line prefix and is order-insensitive, so layout does not matter to the gate. This is an
independent second derivation of the same six sha columns (agreement on all twelve digests), which
is stronger evidence than either file alone; the integrator should pick one as the receipt of record
and remove the other so the landed tree has one erratum. This seat did not write or edit the corpus
copy — it is outside the seat's named scope.

So this file closes **exactly one** of the seven defects and leaves the other six red for their
own seats. The green predicate is not claimed here: it needs E1/E2/E4/E5/E6/E7 landed.

## 6. Existence checks (all twelve)

```text
git -C L cat-file -e 27f649f8:<path>  rc=0   (six paths)
git -C L cat-file -e 1ec2e60a:<path>  rc=0   (six paths)
```

No path is missing on either side, so no `rev-missing:` branch is reachable.

## 7. Findings for this claim's attacker / critic

1. **E3 enforces accuracy of the lines it is given, not completeness of the bound set.** An erratum
   containing only the five *identical* inputs and no `DIFFERS` line passes the real gate:
   `E3 ok inputs=5 differs=[] problems=[]`, `DEFECTS n=6` (truncated-file sha
   `6868db1ff1be4544e405b756826b0098d782f5b164233f3b856e795d00f00f68`, 7 lines). `observed_differs`
   is computed only over the `INPUT` lines present, and no constant names the six bound paths; only
   `no-inputs` guards the empty case. The claim's clause "every bound input's sha256 at both
   revisions" is therefore **not** gate-enforced — a fabricated erratum that silently omits the one
   input that matters still turns E3 green. Fix would be a `BOUND_INPUTS` tuple in the instrument
   compared against the parsed set (schema change, so not made here; this round's file is complete,
   so the scored run is unaffected).
2. **The `TREE`/`LANDING` literals are hardcoded, and the receipt they reference never names a
   revision.** `committed-bytes.txt` records only `HEAD-equals-working=True`; the GateReverify
   report's prose says the lane HEAD was `7803bdd4` (A2 freeze) while the report-of-record
   `ReportGateVerify/provenance.txt` (20:30:49) says `27f649f8` (A3) — the wave straddled A3. This
   does not weaken the erratum: **all six shas are identical at `7803bdd4` and `27f649f8`** (A3
   changed only `plans/round68_capability_table.py`, `plans/round-68-claims.md`, and a red receipt),
   so the `at-tree` column is invariant under either candidate revision. It does mean the `TREE`
   line is not discriminating; what the erratum actually proves is the `SKILL.md` landing delta.
3. **Worktree-based re-derivation would have been wrong here.** At read time the live worktree held
   sibling edits (`git status --porcelain`: `M SKILL.md`, `M corpus/QUALITY.md`,
   `M corpus/knowledge/tb2-network-service-offline-grader.md`, `M corpus/lessons/round-68.md`, plus
   untracked wave/evidence dirs), and working `SKILL.md` hashed `ba596071c9053f309fc33fe62be0ad8eb1c426ffb527406447989d15a0ecf998`
   — neither revision, and neither the receipt's `3fe9a6d0…` nor the landing's `544ad892…`. E3's use
   of `git show` is load-bearing; a hash-of-file check would fail on any wave that is in flight.
4. **The `at-landing` value is stable at the dressed tip.** `SKILL.md` = `544ad892…` at `1ec2e60a`,
   at round-69 base `a518980e`, and at wave HEAD `b288e8e0` (`git diff --stat 1ec2e60a b288e8e0 -- SKILL.md`
   → empty), so a reader comparing the erratum against the round-69 tree sees a match on the landing
   side.
5. **Two gate-green erratum candidates now exist; land exactly one.** No wave seat is assigned
   `corpus/evidence/round69/c2-receipts/provenance-erratum.txt`, yet an untracked copy appeared
   there mid-wave (sha `fad393d0…`), and this seat's named artifact is the W file
   (sha `9261c8d7…`). Both pass E3 verbatim; they differ only in where the `DIFFERS` line sits
   (the W file follows this seat's format — `DIFFERS` last). The integrator must land one and
   remove/ignore the other, e.g. the seat format:

   ```text
   install -D -m 644 .ufo/waves/round-69/w1/provenance-erratum.txt corpus/evidence/round69/c2-receipts/provenance-erratum.txt
   ```

   (sha256 must then read
   `9261c8d73e939b7859746d8aae6a84b1611e21587cd2330202d14ba36341831c`; the gate reads it as
   `root / PROVENANCE`, `PROVENANCE` line 45, and compares only `git show` bytes, so the file's own
   git status is irrelevant.) Leaving both in place is harmless to E3 but leaves two receipts of
   record with different hashes — a provenance ambiguity this very defect class was routed to end.

## 8. Commands and checks NOT run

- Did not run `plans/round69_c2_routed_defects.py` against the real lane (`--root L`): four tracked
  files are mid-edit by sibling seats and the depth/trio receipts do not exist yet, so a real-lane
  number would measure in-flight work and belongs to the parent's post-integration gate.
- Did not run `--selftest` on the C2 gate (GateMutate's item; it also needs a work dir and mutates a
  fake lane, not mine to exercise).
- Did not run the R69-C1 nginx battery (not this seat; includes the port-8080 flock).
- Did not run any pacman/uv/npx install (none needed) and did not touch `~/.local/bin`.
- Did not run any git/jj write command anywhere (no commit, stage, stash, checkout, switch, branch);
  all git invocations were `-C L` read-only (`show`, `cat-file`, `rev-parse`, `log`, `diff`,
  `merge-base`, `rev-list`, `status`, `ls-files`) plus the one `git clone --shared` into scratch and
  the clone-local `git rev-parse --show-toplevel` assertion.
- Did not modify any tracked file; did not write the corpus erratum path (out of this seat's scope).

## 9. Scratch

`/fast/scratch/hyaku/kengaku-r69/ProvenanceRederive` held the raw transcripts (`rederive.raw.txt`,
`rederive2.raw.txt`, `ancestry.raw.txt`, `a2-vs-a3.raw.txt`, `final-checks.raw.txt`,
`e3-verify.raw.txt`, `fmt.raw.txt`, `gate-clone.raw.txt`, `gate-clone-absent.raw.txt`,
`gate-clone-truncated.raw.txt`), the harnesses `e3_verify.py`/`fmt_check.py`, and the
`laneclone` (659 MB). It was deleted, recreated for the two-file E3 check (`e3_two_files.py`), and
deleted again; the raw lines that carry every verdict are quoted above.
