# R37MutC2Counter — C2 counter mutation test (round 37, wave 1)

Seat: R37MutC2Counter (mutation-tester, leaf). Date: 2026-10-26. Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin (untouched; all work in a scratch clone).

## 1. Setup

- Scratch (operator directive 2026-10-25): `S=/fast/scratch/hyaku/kengaku-r37/R37MutC2Counter`; `TMPDIR="$S/work"` on every run; deleted at the end (§6).
- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"`; `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r37/R37MutC2Counter/lane` (verified before any write). No commit, no checkout; index-only `git add` only. Lane HEAD at clone time: `44b7298ae1e03791173097cef0e898285f238870` (lane tip had moved past the freeze commit; all frozen files verified at their freeze digests before use — see §2 digests).
- Environment found, nothing installed (no pacman, no uv, no downloads): `bwrap --version` → `bubblewrap 0.13.1`; `python3 -V` → `Python 3.14.8`.
- Passing package built in the clone from the R37PkgDraft drafts (present when I started):
  - `entry.md` → `corpus/knowledge/tb2-git-webserver-grader.md` (cp).
  - `sources-rows.md` (S111–S113) → appended to `corpus/SOURCES.md`.
  - `readme-additions.md` → index row inserted after the `knowledge/tb2-regex-log-grader.md` row (clone README line 69→70) and coverage bullet after the "second task" bullet (line 259→261), via exact-text edits.
  - Index-only `git add` of the three files; gate P9 (`git ls-files --others --exclude-standard`) then reports `untracked=0`, so `--require-clean-tree` is satisfiable without a commit.
- **Fixture defect found in the draft (for the L1/PkgDraft):** appending `sources-rows.md` at EOF puts S111–S113 under `## Leads (unopened)`, and the census rejects them: `sources-census.sh validate --file <clone>/corpus/SOURCES.md` → `file E12 S111 row outside Registry section` (same for S112, S113), exit 1; baseline counter run printed `V6 DEFECT census_exit=1`. Fix applied in the clone: rows moved inside `## Registry`, immediately after the S110 row (before `## Paths`). The `sources-rows.md` draft carries no placement instruction (unlike `readme-additions.md`, which does) — the integrator must insert after S110, not append. Receipts: `build/R37MutC2Counter/census-clone.txt` (E12 ×3), `census-clone2.txt` (exit 0).

## 2. Baseline (pristine package)

Command: `python3 plans/round37_c2_verify.py --lane "$S/lane" --work "$S/work"` (cwd = clone, `TMPDIR="$S/work"`), run twice (initial + final). Output (both runs identical):

```
V1 ok listed=6 bad=0 extra=0
    gate: P1..P10 all ok (P10 ok probe_rerun=byte-equal bytes=8443; gate: defects=0)
V2 ok gate_exit=0
V3 ok rows=3 bad=0
V4 ok cases=22 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
```

exit=0, 53 s per counter run (each run re-executes the 22-case probe via gate P10). Receipts: `baseline.txt`, `final-pristine.txt`.

Pristine digests recorded before mutation (`sha256sum`, clone cwd; receipt `pristine.sha256`):

```
e70bb662f74fe3271b16e95e694276ba8ef0fd468856ac3c1fae287a38a3531f  corpus/evidence/round37/tb2-git-webserver/SHA256SUMS
1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05  corpus/evidence/round37/tb2-git-webserver/verify.sh
835507129cb536ff6c927b5b05650dd4712891bd3ec218948659655597ec29f8  corpus/evidence/round37/git-webserver-probe.txt
0095e59121a70a5fa6ec8c02ae4a1b30cb2c2b0f335c5e6ad62c650dca4b66f3  corpus/evidence/round37/git-webserver-dry-cases-freeze.txt
63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf  plans/git_webserver_probe.py
948b19065ecaf2936754d799183d4e0566f4458cee13807a77b2071b324e61e4  corpus/SOURCES.md
63633abc95dff0dc78c20f4f1001299ea5b98dc9dcfc1a3db59ec74233364982  corpus/knowledge/tb2-git-webserver-grader.md
9f531ec2c603bf98269d86cd8ab9815cd59de041f8248c7d512c5f49016e1826  corpus/README.md
```

The first five equal the frozen pins in `plans/round37_c2_verify.py` (probe `63cb75cf…5eedf`, dry `0095e591…66f3`) and the capture digests in `SHA256SUMS`/`pkg-spec-r37.json`.

## 3. Mutants (one at a time; each run `python3 plans/round37_c2_verify.py --lane <clone> --work "$S/work"`)

Every run: mutate → run counter → restore from pristine copy → `sha256sum` the restored file. Verdicts: killed = counter exits 1 with ≥1 `DEFECT` line attributable to the mutation; survived = `defects=0`.

| # | Mutant (exact change) | Checks red — DEFECT lines | Verdict | Restored digest |
|---|---|---|---|---|
| M1 | SHA256SUMS: delete the `1dc44c92…  verify.sh` line (6→5 lines) | `V1 DEFECT listed=5 bad=['verify.sh'] extra=0`; `V2 DEFECT gate_exit=1` (gate `P5 DEFECT manifest_entries=5 bad=3 first=S112: capture verify.sh is not pinned in the manifest`) | killed | `e70bb662…` OK |
| M2 | verify.sh capture, 1 byte: line 2 `tests`→`testz` | `V1 DEFECT listed=6 bad=['verify.sh']`; `V2 DEFECT gate_exit=1` (gate `P5 DEFECT … first=verify.sh: manifest digest does not match the bytes`; `P10 DEFECT fresh probe exit=2 stderr='SETUP capture verify.sh missing or not at its pinned digest'`) | killed | `1dc44c92…` OK |
| M3 | receipt, 1 byte: no-server case's stdout record `'…HTTP 000'`→`'…HTTP 001'` (invisible to V4's parsers) | `V2 DEFECT gate_exit=1` (gate `P10 DEFECT fresh probe output is not byte-equal to the receipt`); V1/V3/V4/V5/V6/V7 all ok | killed | `83550712…` OK |
| M4 | receipt: delete the `CASE no-server …` line (orphan `grader-stdout` line left) | `V2 DEFECT gate_exit=1` (P10 not byte-equal); `V4 DEFECT cases=21 … bad=['case ids differ from the frozen table', 'summary disagrees with the CASE lines']` | killed | `83550712…` OK |
| M5 | receipt summary off by one: `observed_pass=9`→`8` | `V2 DEFECT gate_exit=1` (P10 not byte-equal); `V4 DEFECT cases=22 … bad=['summary disagrees with the CASE lines']` | killed | `83550712…` OK |
| M6 | a `match=NO` line not named: receipt `CASE empty-200 … match=yes`→`match=NO` (2 bytes) + `empty-200` removed from its only entry mention (line 134) | `V2 DEFECT gate_exit=1` (P10 not byte-equal); `V4 DEFECT cases=22 mismatches_named=0/1 bad=['summary disagrees with the CASE lines', "mismatch cases not named in the entry: ['empty-200']"]` | killed | receipt `83550712…`, entry `63633abc…` OK |
| M7 | probe, 1 byte: shebang `python3`→`python4` | `V2 DEFECT gate_exit=1` (gate `P1 DEFECT pinned=2 mismatched=['plans/git_webserver_probe.py']`); `V5 DEFECT probe or dry table not at freeze digest` | killed | `63cb75cf…` OK |
| M8 | dry table, 1 byte: `CASE exact-no-newline … predicted=pass`→`predicted=fail` (case ids untouched) | `V5 DEFECT probe or dry table not at freeze digest`; V1–V4, V6, V7 all ok (gate `defects=0`) | killed | `0095e591…` OK |
| M9 | SOURCES S112 anchor digest truncated to 63 hex (`…f53d05`→`…f53d0`) | `V3 DEFECT rows=3 bad=['S112:anchor_digest']`; all other checks ok — including the gate (`P6 ok rows=3 bad=0`) | killed | `948b1906…` OK |
| M10 | SOURCES S112 row carries two sha256 tokens (appended `; sha256 000…000` in the anchor cell) | `V3 DEFECT rows=3 bad=['S112:anchor_digest']`; all other checks ok — gate `P6 ok rows=3 bad=0` again | killed | `948b1906…` OK |
| M11 | requirement map: row `instruction.md:1-6` label `unenforced`→`enforced` (cites only the passing `static-file-no-git`) | `V7 DEFECT rows=4 bad=['instruction.md:1: enforced without a failing case']`; all others ok | killed | `63633abc…` OK |
| M12 | requirement map: delete the `instruction.md:7` row | `V7 DEFECT rows=3 bad=['instruction lines not mapped: [7]']`; all others ok | killed | `63633abc…` OK |
| M13 | requirement map: row 8 cites `no-such-case-000` (unknown id) instead of `not-found` | `V7 DEFECT rows=4 bad=['instruction.md:8: cites no case or an unknown case']`; all others ok | killed | `63633abc…` OK |
| M14 | quote off by one line: Located-quotes row `verify.sh:62`→`verify.sh:61` (line 61 is `echo "Web server test successful (HTTP 200)"`) | `V2 DEFECT gate_exit=1` (gate `P4 DEFECT checked=32 bad=1 first=verify.sh:61: quote not verbatim there`); all others ok | killed | `63633abc…` OK |

Per-mutant full outputs: `build/R37MutC2Counter/m01.txt` … `m14.txt`.

**Result: 14/14 killed, 0 survived, 0 inconclusive** (baseline passed before and after; `final-pristine.txt` = `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0).

## 4. Which check carries which mutant (coverage map of the counter)

- V1 alone kills M1/M2 at the manifest level; the gate's P5 independently catches both (V2 red).
- V2 (gate P10 fresh-run byte-compare) is the **only** guard against arbitrary receipt tampering: M3's single byte inside a stdout record is invisible to every parse-level check (V4 stayed ok) and was caught solely by `fresh probe output is not byte-equal to the receipt`. M4/M5/M6 are additionally caught by V4's structural checks.
- V3 is the **only** guard for anchor-digest shape: in M9 and M10 the gate accepted the row (`P6 ok rows=3 bad=0` both runs) — the gate's own source check does not verify the anchor digest against the spec pin; only the counter's V3 does. This is a real asymmetry worth the L1's attention: a lane-side gate re-run alone would not catch a 63-hex or double-token anchor.
- V5 alone kills M8 (dry-table byte); for M7 (probe byte) V5 and the gate's P1 (frozen-instruments digest) both fire. Note M7's gate P10 still printed `probe_rerun=byte-equal` — the shebang byte is inert when the gate invokes the probe under `sys.executable`, so the fresh-run check did not contribute to that kill.
- V7 alone kills M11/M12/M13 (requirement-map semantics) and the gate's P4 (via V2) alone kills M14 (quote line anchor).

## 5. Notes and limits

- M6 is synthetic by necessity: the pristine receipt has **zero** `match=NO` lines (`mismatches=0`, and V4 requires `m == len(no)`), so "a match=NO line not named" was realized as flip `match=yes`→`match=NO` on `empty-200` plus removal of its only entry mention. V4 caught both the summary disagreement and the unnamed id; V2's byte-compare also fired. The "unnamed mismatch" clause of V4 is exercised by the mutant but has no natural occurrence in this receipt.
- M3's mutation site (a stdout record byte) was chosen to isolate the fresh-run check; a byte in a parsed field would also trip V4. The class demonstrated: any receipt byte change is caught, and parse-invisible changes are caught *only* by P10's byte-compare.
- Restoration evidence: after the last mutant, `sha256sum -c pristine.sha256` (clone cwd) printed `OK` for all 8 files (`final-digest-check.txt`), and the final pristine counter run printed `checks=7 defects=0` / `PREDICATE C2 pass`.
- No lane file was edited; no git mutating command ran anywhere (index-only `git add` inside the clone only); the source repo /home/vgpnk/Projects/shokuknow was not touched; no tools were installed (bwrap 0.13.1 and Python 3.14.8 already present).
- Runtime: 16 counter runs × ~53 s ≈ 14 min total.

## 6. Scratch cleanup

`rm -rf -- /fast/scratch/hyaku/kengaku-r37/R37MutC2Counter` executed after copying all receipts (§1–§3 files) into `build/R37MutC2Counter/`; deletion confirmed by the post-cleanup `ls` in the transcript.

Receipts in `build/R37MutC2Counter/`: `baseline.txt`, `census-clone.txt`, `census-clone2.txt`, `census-pristine.txt`, `final-pristine.txt`, `final-digest-check.txt`, `pristine.sha256`, `m01.txt`–`m14.txt`.

VERDICT: c2-mutants-14/14
