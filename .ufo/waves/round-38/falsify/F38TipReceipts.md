# F38TipReceipts — falsification: `plans/tip_receipts.py` at `8c7422d7`

**Seat:** F38TipReceipts (executor, leaf), kengaku round 38 wave 2 (falsify).
**Attacks:** the wave-1 assimilation `plans/tip_receipts.py` (considerthese/2026-10-25 proposal 2(c)) and the
`tip-receipts` gate row `SKILL.md:586` — the claim that "every committed `probe*` receipt with a committed
re-run command is byte-equal at the tip" and that the tamper control answers `differ`.
**Tip measured:** `8c7422d7a646515d80af44844e8ecc8a1fc1d30a` (`git -C "$S/lane" rev-parse HEAD`), detached in a
`--no-local` clone; `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`.
**Scratch:** `/fast/scratch/hyaku/kengaku-r38/F38TipReceipts` (`S` below), `TMPDIR` exported inside it, removed
before this report; receipts kept in `.ufo/waves/round-38/falsify/F38TipReceipts/`. Lane, clone, index, jj state:
untouched (0 write-opens into the lane, §3). Nothing installed; no pacman transaction attempted.
`plans/tip_receipts.py` sha256 `f2a35b47…` — byte-identical to the wave-1 draft in
`.ufo/waves/round-38/build/R38TipReceipts/tip_receipts.py` (both `f2a35b47d9e4d2ce3ec981dbb07a5c968d61d41c207ee32ecef4b9ea1932bcdd`).

---

## 1. Re-run at the tip — the claim reproduces

```
$ cd "$S/lane" && TMPDIR=$S/tmpdir python3 plans/tip_receipts.py --lane . --work "$S/w"
tip 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
… 19 × `receipt corpus/evidence/probe-r19-*.log skip reason=no-committed-re-run-command` …
receipt corpus/evidence/round35/tb2-grader-probe.txt equal bytes=3399 exit=0 doc=corpus/README.md:260+SKILL.md:574
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking) doc=SKILL.md:576+corpus/README.md:435
receipt corpus/evidence/round36/regex-log-probe.txt equal bytes=5907 exit=0 doc=SKILL.md:576+SKILL.md:576
receipt corpus/evidence/round37/git-webserver-probe.txt equal bytes=8529 exit=0 doc=SKILL.md:577+SKILL.md:577
receipt corpus/evidence/round38/build-pmars-probe.txt equal bytes=5537 exit=0 doc=SKILL.md:582+SKILL.md:582
control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
note compared=4 declared_bounded=1 no_command=19
receipts=24 byte_equal=4 differ=0 skipped=20
exit=0        # real 0m53.494s
```

Receipt: `F38TipReceipts/run-full.txt` (`c3184e3d…`). Population independently reproduced: 24 candidates
(`git ls-tree -r HEAD --name-only corpus/evidence` filtered by the tool's own predicate, §4 F2).
`--list` at the tip: `F38TipReceipts/list.txt` (`b4b76157…`), same 5 mappings, same 19 named skips, 0.081 s.
**Determinism:** two full passes differ only in their `control` line;
`diff <(grep -v '^control' run-full.txt) <(grep -v '^control' tamper-4.txt)` → empty, both
`md5 4d97f67ff5a0cc1c1f0f9d58f34d11f4`. The wave-1 claim `4/24` reproduces at a different tip (wave 1 measured
`2c5f4e0b`, this seat `8c7422d7`), and every `doc=` field still resolves to a committed line.

## 2. Tamper controls — every one is caught (this is the claim, and it holds)

| # | what it attacks | tamper | result |
|---|---|---|---|
| 2a | the in-tool comparator, all four byte receipts | one flipped byte each (`--tamper 4 rels`) | 4/4 `verdict=differ`, exit 0: `flip=byte 2768 0x74->0x75` (r38), `2953 0x30->0x31` (r36), `4264 0x54->0x55` (r37), `1699 0x27->0x26` (r35) — `tamper-4.txt` (`ac0b33ca…`) |
| 2b | end-to-end: a **committed** tampered receipt at a different tip | scratch clone `lane-tamper` @ `d3041bed`, `cases=22`→`cases=23` (byte 5489) | `receipt … differ first_diff=byte 5489 (line 26) exit=0`, `receipts=1 byte_equal=0 differ=1`, `exit=1` — `tamper-e2e.txt` (`d94ad57d…`); the report's offset matches the manual flip (byte 5489 = `'2'` in `cases=22`, line 26) |
| 2c | the `temp-paths` masking as a launderer | one byte **outside** both mask spans (offset 2964, line 13) in `regex-log-probe-first-run.txt` | `differ masked bytes differ: byte 2964 (line 13)`, `exit=1` — `tamper-masked.txt` (`d3990a68…`). Mask spans in that blob are 4976-4992 and 5182-5198; the auto flip lands at 2964, outside them |
| 2d | the tool measures output, not the script's mtime | probe's live summary line edited (`plans/build_pmars_probe.py:343` `cases=`→`kases=`, commit `e054809e`) | `differ first_diff=byte 5482 (line 26)`, `exit=1` — `tamper-script2.txt` (`5dd4611f…`) |
| 2e | a tamper that changes nothing observable (recorded, not a failure) | probe's `--dry`-only line edited (`:297`, dead on the receipt path), commit `8a5d8935` | `equal`, `exit=0` — `tamper-script.txt` (`42e96fd4…`). Correct: the receipt path never prints that line; the tool compares stdout, not code |

Masked-kind control at the top level: `--only regex-log-probe-first-run --tamper <that receipt>` →
`control … flip=byte 2964 0x32->0x33 verdict=differ`, `exit=0` (`tamper-temppaths.txt`, `acd90410…`).
An unknown id refuses: `--tamper corpus/evidence/probe-r19-P3.log` →
`SETUP: --tamper corpus/evidence/probe-r19-P3.log is not a mapped receipt`, `exit=2`.

## 3. `TMPDIR` / `--work` are honoured; the lane is read-only

`strace -f -qq -e trace=mkdir,mkdirat,openat,open,creat` around `--only build-pmars-probe`
(`strace-summary.txt`, `77d732ec…`; raw log not kept, scratch deleted):

```
absolute mkdir outside scratch: 0
mkdir under scratch (w2/tmpdir): 214
openat under lane with write flags: 0
openat /tmp with write flags: 0
tmp-before lines: 134; tmp-after: 134; diff: 0 lines
__pycache__ under lane: 0
lane status --porcelain lines: 0
```

`--work` names the parent: `mkdir("…/w2/tip-receipts-86s5fboy", 0700)` then `…/w2/…/tmp/corpus-evidence-round38-build-pmars-probe-txt`
with per-probe children `a036u8ng`, `k38-bpm-4t08qj_6`; the WS is removed (`ls -A "$S/w"` empty).
Without `--work`, `TMPDIR=$S/tmpdir/td2` is used: `mkdir("…/tmpdir/td2/tip-receipts-pavoecp9", 0700)`, and
`ls -A "$S/tmpdir/td2"` is empty afterwards (`tmpdir-only.txt`, same bytes as the `--only build-pmars` run).

## 4. Attacks that land (each named with what it breaks)

**F1 — a new runnable probe receipt is labelled `no-committed-re-run-command` and the gate exits 0.**
Attacks `SKILL.md:586`'s exit-0 predicate ("every committed `probe*` receipt **with a committed re-run
command** is byte-equal"). A runnable probe is one whose script carries the `Run as:` line the tool parses — not
one with a `RECEIPTS` row. Constructed in a scratch clone `lane-extra` @ `94bf1068`: `plans/extra_probe.py`
(with a `Run as:` docstring line) + `corpus/evidence/round38/extra-probe.txt`, both committed.

```
$ python3 plans/tip_receipts.py --lane "$S/lane-extra" --work "$S/w"
receipt corpus/evidence/round38/extra-probe.txt skip reason=no-committed-re-run-command
note compared=4 declared_bounded=1 no_command=20
receipts=25 byte_equal=4 differ=0 skipped=21
extra exit=0
$ python3 plans/extra_probe.py --lane . | cmp - corpus/evidence/round38/extra-probe.txt && echo BYTE-EQUAL
BYTE-EQUAL
```
(`population-extra.txt`, `4e645837…`.) The receipt **is** byte-equal and **does** have a committed re-run
command; the tool reports the opposite reason and passes. Population is closed-world over a 5-entry literal
table (docstring: "receipt -> (committed probe script, kind)"), so the gate's stated predicate is not what it
measures.

**F2 — 176 of the 200 committed `corpus/evidence/**/*.{txt,log}` receipts are outside the population and get no
line at all.** The docstring's "everything else is printed on one boundary line with its reason, so nothing is
dropped silently" holds only *inside* the candidate set, which is defined by the filename (basename must contain
`probe`). Measured at the tip:

```
evidence files 485 txt/log 200 candidates 24
txt/log excluded by predicate: 176
```
Among the 176: `corpus/evidence/round36/regex-log-dry-cases-freeze.txt`,
`round37/git-webserver-dry-cases-freeze.txt`, `round38/build-pmars-dry-cases-freeze.txt` — the frozen `--dry`
tables of three probes the tool *does* run (`--dry` is a documented, deterministic mode of each), plus
`round35/hardening-counterexamples.txt`, `round30/landing-receipt.txt`, `round26/…/grader-replay-final.txt`, and
the `census-*`/`state-check-*` receipt families. None of them can ever be reported, whatever their drift.

**F3 — an absent dependency turns a receipt into an unverified skip, still counted as `compared`, gate green.**
Attacks the "byte-equal at the tip" reading and the `note` line's honesty. `uv` lives in `~/.local/bin`:

```
$ PATH=/usr/bin:/bin python3 plans/tip_receipts.py --lane . --work "$S/w3" --only round35
receipt corpus/evidence/round35/tb2-grader-probe.txt skip reason=dependency-missing:uv doc=corpus/README.md:260+SKILL.md:574
note compared=1 declared_bounded=0 no_command=0
receipts=1 byte_equal=0 differ=0 skipped=1
exit=0
```
(`path-no-uv.txt`, `279be4db…`.) `compared=1` while `byte_equal=0 skipped=1`: the counter counts mapped
byte-kind receipts, not verified ones. On any host without `uv` (or `bwrap`: the same branch guards
`shutil.which(argv[0])`), the whole round-35 receipt silently leaves the evidence set with a green exit.

**F4 — a mistyped filter is a green gate that checked nothing.**

```
$ python3 plans/tip_receipts.py --lane . --work "$S/w3" --only zzz-nothing
tip 8c7422d7a646515d80af44844e8ecc8a1fc1d30a
note compared=0 declared_bounded=0 no_command=0
receipts=0 byte_equal=0 differ=0 skipped=0
exit=0
```
(`only-typo.txt`, `a1e27455…`.) With no `equal` receipt the auto-control list is empty (`controls = [... ] if
equal else []`), so `control_ok` stays `True` and no control runs. `SKILL.md:586` lists `--only SUBSTR` as part
of the gate's own command, so the documented invocation can be narrowed to "no receipts" and still exit 0.

**F5 — the gate's verdict depends on the filter, not on the tip.** On `lane-tamper` @ `d3041bed`, whose r38
receipt reads `cases=23` (a real `differ`, §2b):

```
$ python3 plans/tip_receipts.py --lane "$S/lane-tamper" --work "$S/w" --only round36/regex-log-probe.txt
tip d3041bed35aaf9d429dc60fb9b84aefbaf4d1174
receipt corpus/evidence/round36/regex-log-probe.txt equal bytes=5907 exit=0 …
receipts=1 byte_equal=1 differ=0 skipped=0
narrow exit=0
```
(`only-narrow-green.txt`, `2fccdb9e…`.) Same HEAD, opposite verdicts: `--only build-pmars-probe` on that clone
is `differ`/exit 1. A per-receipt green is not a tip green, and nothing in the output says so.

**F6 — an uncommitted edit of a receipt is invisible.** `git show HEAD:<rel>` is the blob of record, so a
worktree edit still reads `equal`:

```
$ python3 - <<'PY'   # lane-wt: byte 5489 of round38 receipt -> '9', not committed
$ git -C "$S/lane-wt" status --porcelain
 M corpus/evidence/round38/build-pmars-probe.txt
$ python3 plans/tip_receipts.py --lane "$S/lane-wt" --only build-pmars-probe
receipt corpus/evidence/round38/build-pmars-probe.txt equal bytes=5537 exit=0 …   # exit=0
```
(`worktree-tamper.txt`.) Consistent with "the blob of record", and worth stating because the gate is run *inside*
the lane (`--lane DIR`), where a stale worktree receipt is exactly the failure a reader would expect it to catch.

**F7 — the "clean clone" is a `--shared` clone.** `git clone -q --shared LANE <ws>/tip` makes the clone's object
store an alternate of the lane's, so a probe that reads history reads the lane's objects; the isolation the
docstring claims ("clones the lane at HEAD into a scratch directory") is HEAD-pinning plus a separate worktree,
not an independent object copy. Read-only in practice (§3: 0 write-opens into the lane), so this is a wording
risk, not an observed defect.

**F8 — `doc=` provenance is a cross-file substring join.** `provenance()` collects `script_hits` and
`receipt_hits` independently over `DOC_SOURCES + DOC_GLOBS` and returns `script_hits[0]+receipt_hits[0]`; receipt
matching is by **basename** only. A script named in `plans/x.py` and a receipt named in `corpus/README.md` pair
up as if one line named both. At this tip the r38 pair happens to resolve on one line — `SKILL.md:582` contains
both `build_pmars_probe.py` and `build-pmars-probe.txt` (verified by `grep -c` on that line = 1 and 1) — so the
wave-1 finding 2 (no line naming both) is genuinely closed, but the field is weaker evidence than it reads.

**Control robustness note (fails closed).** A one-byte flip *inside* a masked `…/tmpXXXXXXXX` span would be
masked away, so the control would answer `equal` and the tool would exit 1 (`control_ok = control_ok and not
same`). That is loud, not a silent pass; the auto flip for that receipt (2964) is outside both spans.

## 5. What this tool does not reach (scope of the verdict)

- **It is not the C1 or C2 measurement.** `tip_receipts` re-runs 4 probe scripts and compares their stdout; it
  never executes `plans/round38_c1_verify.py` or `plans/round38_c2_verify.py`. The `killed=21 survived=1` /
  `checks=7` numbers and the N21 mirror explanation are untouched by anything here — this report says nothing
  about them, in either direction.
- **Its population is `corpus/evidence/**` only.** 2030 `.txt`/`.log` files are tracked under `.ufo/` — including
  this round's landing receipts, which *are* tracked at the tip
  (`git cat-file -e HEAD:.ufo/waves/round-38/integrate/measure-final.txt` → present; likewise
  `claims/control-c1-nothing.txt`, `claims/control-c2-nothing.txt`) and which no `tip_receipts` run will ever
  re-run.
- **The proposal's "would have caught D3 mechanically" is not testable by this tool.** Round-38's routed D3 is
  `anchor check binds to any committed digest` (`plans/round-38-claims.md:93`), closed by
  `plans/anchor_digest_check.py`. `tip_receipts` reads knowledge/`plans` text only to build the `doc=` string
  (`DOC_GLOBS` feeds `provenance()`, never a comparison), so no anchor row can be checked by it. Its measured
  reach is the 4 receipts in §1.
- **Self-test.** The `SKILL.md:586` self-test receipt exists at the tip
  (`.ufo/waves/round-38/build/R38TipReceipts/tip-receipts-tamper-control.txt`, `note compared=1 … differ=1`) and
  is consistent with §2b/§2d/§2c re-measured here.

## 6. Limits of this falsification

All tampers were made in scratch clones under `/fast/scratch/hyaku/kengaku-r38/F38TipReceipts` (`lane-tamper`,
`lane-extra`, `lane-mask`, `lane-script`, `lane-script2`, `lane-wt`); the lane was never written, indexed or
committed, and `git -C "$S/lane" status --porcelain` stayed empty throughout. §4 F1's "receipt with a committed
re-run command" is my construction (`plans/extra_probe.py` + its receipt), because the tip has no such unmapped
case; the construction is byte-equal, so the skip is provably a label and not a divergence. F2's list is the
tool's own predicate re-implemented in one `python3 -` pass over `git ls-tree`. F3's PATH surgery removes `uv`
from the environment, not from the host. No finding here depends on network access; every probe ran offline
except `uv`'s cached environment resolution.

Axes: (a) operability — the tool runs from one command, honours `--work`/`$TMPDIR`, leaves no residue, is
deterministic and read-only: kept as good. (b) freshness — the tip claim `4/24 byte_equal, 0 differ` reproduces,
and the tamper control answers `differ` in five independent shapes: kept as good; but the *population* is a
closed 5-entry table with three ways to go green without verifying (F1, F3, F4) and one way to go green over a
known differ (F5). Those are the moves a wave-3 tightening should take; they are named here, not implemented.

VERDICT: tip-receipts-4/24-tamper-caught
