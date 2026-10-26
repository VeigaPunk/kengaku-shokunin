# F40TipReceipts — attack on the landed `plans/tip_receipts.py`

Wave-2 falsify seat. Target: the landed derived-receipt rule (round-39 routing item R4 / `F39TipReceipts`),
attacked at the named tip `ec1005a2a28bc5cfdde7723374368ed4cc956eed`.

Lane clone: `S=/fast/scratch/hyaku/kengaku-r40/F40TipReceipts`, `git clone -q --no-local <lane> $S/lane`,
`git -C $S/lane checkout -q ec1005a…`; `git -C $S/lane rev-parse --show-toplevel` → `$S/lane`;
`git -C $S/lane status --porcelain --untracked-files=all | wc -l` → `0` at the end. Every counter invocation
ran under
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`.
No lane file, Git index or jj state was touched; scratch removed after the receipts were copied here.
No tool installed or upgraded (`pacman` untouched).

Committed tool bytes: `git show HEAD:plans/tip_receipts.py | sha256sum` →
`e4f49714299ca1f2a93303c59ac07e691cc45d6126ccf24e5eecab93733f88f3` (the wave-1 fixed copy).

---

## 1. Assigned checks — all four hold

### 1.1 Full run at the tip (`--work` on the clean clone)

```
$ cd $S/lane && python3 plans/tip_receipts.py --lane . --work "$S/w"          # rc=0
tip ec1005a2a28bc5cfdde7723374368ed4cc956eed
receipt corpus/evidence/round35/tb2-grader-probe.txt equal bytes=3399 exit=0 doc=corpus/README.md:262+SKILL.md:574
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking) doc=SKILL.md:576+corpus/README.md:470
receipt corpus/evidence/round36/regex-log-probe.txt equal bytes=5907 exit=0 doc=SKILL.md:576+SKILL.md:576
receipt corpus/evidence/round37/git-webserver-probe.txt equal bytes=8529 exit=0 doc=SKILL.md:577+SKILL.md:577
receipt corpus/evidence/round38/build-pmars-probe.txt equal bytes=5537 exit=0 doc=SKILL.md:582+SKILL.md:582
receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0 doc=SKILL.md:587+SKILL.md:590
receipt corpus/evidence/round40/db-wal-probe.txt equal bytes=8257 exit=0 doc=SKILL.md:593+SKILL.md:590
control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
note compared=6 declared_bounded=1 no_command=19
receipts=26 byte_equal=6 differ=0 skipped=20
```

`full.txt` and a second full run `full-run2.txt` (`--jobs 6`, 54 s) are **bit-identical**
(`a83d04382cbb466e6f7bb8300d0b2790b894b219c9c240b15f46aea88e5a0156` both, `sha256sum`). Deterministic.

**Freshness note on the routed measurement.** `integrate/measure-final.txt:575-581` prints
`tip ec17216844585d0fecde9f1d4c4be0b78a3bf76f` — one commit behind the named tip — but its seven result lines
are exactly the seven above. The inputs of this tool are unchanged between the two commits:
`git diff --name-only ec17216 ec1005a | grep -E '^(plans/|SKILL.md|README.md|corpus/README.md|corpus/knowledge/)'`
prints nothing (rc 1: no match), and `git diff --stat` names only `.ufo/`, `LOG.md`, `SCORECARD.md`,
`corpus/lessons/round-40.md`. So measure-final is stale in its TIP line only; my run at `ec1005a` is the tip
measurement and it lands on the same bytes.

### 1.2 `--list`: every `origin=derived` mapping is correct

`list.txt` — 7 mapped lines, 2 of them derived:

```
receipt corpus/evidence/round39/git-leak-probe.txt kind=byte script=plans/git_leak_probe.py origin=derived provenance=SKILL.md:587+SKILL.md:590
receipt corpus/evidence/round40/db-wal-probe.txt kind=byte script=plans/db_wal_probe.py origin=derived provenance=SKILL.md:593+SKILL.md:590
```

Independent audit (`audit_stems.py`, output `audit-stems.txt`) recomputes the rule from `git ls-tree` without
the tool's code: `plans_total=49 plans_stem_dup={}` → no two top-level `plans/*.py` share a stem;
`candidates=26`; exactly 6 `MATCH` lines, the 6 already-mapped receipts (4 `origin=table`, 2 derived); the 20
remaining candidates have no stem match. So the derived set is neither short nor over-broad at this tip, and
each derived mapping is corroborated the only way it can be — the named script reproduces the receipt byte for
byte (`equal bytes=5867` / `8257`). Provenance hits are real: `sed -n '590p' SKILL.md` contains both
`git-leak-probe.txt` and `db-wal-probe.txt`, `587p` contains `plans/git_leak_probe.py`, `593p` contains
`plans/db_wal_probe.py`.

### 1.3 Fixture repo: stem collision and `-first-run` sibling

Fixture `f1` (`fixtures-src.txt`): `plans/gamma_probe.py`, a collision pair `plans/alpha_probe.py` +
`plans/alpha-probe.py`, `plans/zeta_probe.py` (no command line), receipts `gamma-probe.txt`,
`gamma-probe-first-run.txt`, `alpha-probe.txt`, `probe-r19-legacy.log`.

```
receipt corpus/evidence/r41/gamma-probe.txt kind=byte script=plans/gamma_probe.py origin=derived provenance=command=SKILL.md:3,receipt=undocumented
receipt corpus/evidence/r41/zeta-probe.txt kind=byte script=plans/zeta_probe.py origin=derived provenance=undocumented
receipt corpus/evidence/r41/alpha-probe.txt skip reason=no-committed-re-run-command
receipt corpus/evidence/r41/gamma-probe-first-run.txt skip reason=no-committed-re-run-command
receipt corpus/evidence/r41/probe-r19-legacy.log skip reason=no-committed-re-run-command
--- run ---
receipt corpus/evidence/r41/gamma-probe.txt equal bytes=17 exit=0 doc=command=SKILL.md:3,receipt=undocumented
control receipt=corpus/evidence/r41/gamma-probe.txt flip=byte 8 0x63->0x62 verdict=differ
note compared=2 declared_bounded=0 no_command=4
receipts=5 byte_equal=1 differ=0 skipped=4
```

Collision resolves to nothing (rule is unique-match), the `-first-run` sibling does **not** inherit the mapping
(exact stem, no prefix match), a legacy log stays unmapped, an explicit `--tamper` on the derived receipt
answers `differ`, rc 0 — all as the docstring says. (The `compared=2` counter is wrong; that is D2 below.)

### 1.4 Tamper controls on every equal receipt

`--tamper` with all six equal receipts in one invocation (`tamper-all-six.txt`, rc 0):

```
control receipt=corpus/evidence/round35/tb2-grader-probe.txt flip=byte 1699 0x27->0x26 verdict=differ
control receipt=corpus/evidence/round36/regex-log-probe.txt flip=byte 2953 0x30->0x31 verdict=differ
control receipt=corpus/evidence/round37/git-webserver-probe.txt flip=byte 4264 0x54->0x55 verdict=differ
control receipt=corpus/evidence/round38/build-pmars-probe.txt flip=byte 2768 0x74->0x75 verdict=differ
control receipt=corpus/evidence/round39/git-leak-probe.txt flip=byte 2933 0x65->0x64 verdict=differ
control receipt=corpus/evidence/round40/db-wal-probe.txt flip=byte 4128 0x72->0x73 verdict=differ
```

6/6 `differ`, and the automatic control (no `--tamper`) picks the cheapest equal receipt
(`3399` B `round35/tb2-grader-probe.txt`), exactly as documented. The comparator is not vacuous on any of the
six, including both derived pairs.

### 1.5 Status change vs `integrate/measure-baseline.txt`

Baseline block extracted (`base-lines.txt`) vs this run (`now-lines.txt`), `doc=` stripped, sorted, diffed:

```
-note compared=4 declared_bounded=1 no_command=21
+note compared=6 declared_bounded=1 no_command=19
-receipt corpus/evidence/round39/git-leak-probe.txt skip reason=no-committed-re-run-command
-receipt corpus/evidence/round40/db-wal-probe.txt skip reason=no-committed-re-run-command
+receipt corpus/evidence/round39/git-leak-probe.txt equal bytes=5867 exit=0
+receipt corpus/evidence/round40/db-wal-probe.txt equal bytes=8257 exit=0
-receipts=26 byte_equal=4 differ=0 skipped=22
+receipts=26 byte_equal=6 differ=0 skipped=20
```

**No previously-equal receipt changed status**: the four `equal` lines keep their exact byte counts
(3399/5907/8529/5537), the `temp-paths` receipt keeps its declared-bounded skip, and the control line is
byte-identical (`flip=byte 1699 0x27->0x26`). Only the two new derived receipts move skip → equal, and only
the counters follow. (`measure-baseline.txt`'s `round35` line carries `doc=corpus/README.md:261+SKILL.md:574`,
now `:262` — a doc line index, not a receipt status.)

Also checked: cwd independence (`cd /tmp`, `--lane` absolute, `--only round39` → same `equal bytes=5867`,
control `differ`, rc 0; `TMPDIR`/`--work` stayed under `$S`, nothing written to `/tmp`).

---

## 2. Defects

Each is a receipt: command, observed output, code line. **None of them changes the round-40 frozen predicate,
the C2 counter or the §1.1 full-run line** — the shipped measurement is green and reproducible. They are
defects of the tool's own contract, found on fixtures, plus D1 which is reachable on the real lane through a
documented selector.

### D1 — a run can be green with **no tamper control at all** (S2, contract)

Attacks the docstring's exit-code line (`plans/tip_receipts.py:29`) "Exit codes: 0 every mapped receipt
reproduces … and the control reports `differ`" and the registry row `SKILL.md:586` "… and the tamper control
answers `differ`". When no mapped receipt is byte-equal, `equal` is empty and `controls` becomes empty while
`control_ok` stays `True` (`:340-343`):

```
$ python3 plans/tip_receipts.py --lane . --only corpus/evidence/round36/regex-log-probe-first-run.txt --work "$S/w-only"
receipt corpus/evidence/round36/regex-log-probe-first-run.txt skip reason=declared-nonreproducible-absolute-scratch-paths (equal after masking) ...
note compared=0 declared_bounded=1 no_command=0
receipts=1 byte_equal=0 differ=0 skipped=1
rc=0
```

No `control` line, rc 0. Same shape for `--only probe-r19`: `receipts=19 byte_equal=0 differ=0 skipped=19`,
rc 0, no control (`only-skip-runs.txt`). Generalises: any run whose mapped set is all declared-bounded /
dependency-missing / no-command exits 0 with zero tamper evidence — the instrument disappears exactly when
nothing was compared. Wave 1 fixed the "green having compared nothing" wording for unmapped receipts; the
control was left optional. The full measurement command has six equal receipts, so the round-40 line is
unaffected.

### D2 — `note compared=` counts receipts that were skipped (S3, counter)

`strict = [r for r in mapped if results[r]["kind"] == "byte"]` (`:374`) counts a mapped receipt even when it
was skipped for having no command. Fixture `f1` shows the same receipt in both totals:

```
receipt corpus/evidence/r41/zeta-probe.txt skip reason=no-committed-re-run-command:no-command doc=undocumented
note compared=2 declared_bounded=0 no_command=4
receipts=5 byte_equal=1 differ=0 skipped=4
```

Only `gamma-probe.txt` ran; `compared=2` includes `zeta-probe.txt`, which `no_command=4` counts in the same
breath. Reachable in the lane: `plans/attrib_probe.py` and `plans/catalog_probe.py` are probe-named and carry
no `python3 ` command line (`grep -c python3` → `1` each: the shebang only), so a future
`corpus/evidence/**/attrib-probe.txt` would be a derived mapping that inflates `compared`.

### D3 — the derived argv is the **first** matching prose line, and prose is split only on 2+ spaces (S1, false red)

`usage_argv` takes the first stripped line starting `python3 `/`uv run ` that contains the basename
(`:146`) and splits at `re.split(r"\s{2,}", s)[0]` (`:149`). The docstring claims this is "the same line
SKILL.md's gate/probe registry and corpus/README.md quote" (`:8`). Two shapes, both rc 1 on a **genuine**
receipt:

*f2* — `plans/epsilon_probe.py` documents `--smoke` on the line before the `--lane .` line that `SKILL.md:3`
quotes. The receipt is the exact output of the quoted command
(`cmp epsilon-documented-out.txt corpus/evidence/r41/epsilon-probe.txt` → equal):

```
receipt corpus/evidence/r41/epsilon-probe.txt differ first_diff=byte 0 (line 1) exit=0 ...
receipts=1 byte_equal=0 differ=1 skipped=0
rc=1
```

*f4* — one space between command and prose: `python3 plans/theta_probe.py --lane . run every frozen case …`
→ the prose becomes argv, the receipt (that same command's output) differs at byte 6, rc 1
(`f4-single-space.txt`). Live tip: all six mapped scripts happen to carry the full-run line first with 2+
spaces, so the landed measurement is clean — but the next probe written that way produces a false `differ`,
i.e. exactly the "false red" a re-run gate must not have.

### D4 — a zero-length committed receipt can never pass; the lane is reported red with `differ=0` (S1, false red)

`tamper_one_byte(b"")` returns `b""`, and the control guard `if "fresh" not in res or not res["blob"]`
(`:346`) treats an empty blob as "no control", while the same receipt is a legitimate `equal`. Fixture `f3`
(`delta_probe.py` prints nothing, receipt committed empty):

```
receipt corpus/evidence/r41/delta-probe.txt equal bytes=0 exit=0 ...
control receipt=corpus/evidence/r41/delta-probe.txt verdict=unavailable
receipts=1 byte_equal=1 differ=0 skipped=0
rc=1
```

Every mapped receipt reproduced; the exit code is 1 because the control could not run. The docstring's exit-1
list is "a `differ`, a failed control, or a probe that did not complete" — none happened. A probe that prints
nothing is a legal receipt, and this lane can never go green. No empty receipt exists at this tip.

### D5 — `provenance` reads the lane **worktree**, not committed text (S3, display)

Docstring `:161`: "Where the lane's **committed** text names both the script and this receipt". The search
reads `lane / name` (`:164-167`). Fixture `f1` with one uncommitted line appended to `SKILL.md`
(`git status --porcelain` → ` M SKILL.md`; `git show HEAD:SKILL.md` is 3 lines):

```
receipt corpus/evidence/r41/gamma-probe.txt kind=byte script=plans/gamma_probe.py origin=derived provenance=SKILL.md:3+SKILL.md:5
```

`SKILL.md:5` does not exist at HEAD. Only the `doc=` field is affected (no verdict), but `doc=` is quoted into
reports and receipts as evidence that the lane documents the receipt.

### D6 — `--tamper` excluded by `--only` is reported as "not a mapped receipt" (S3, diagnostic)

`unknown = [t for t in tamper if t not in results]` (`:335`) tests the **filtered** results. Real lane:

```
$ python3 plans/tip_receipts.py --lane . --only round39 --tamper corpus/evidence/round40/db-wal-probe.txt --work "$S/w-oo"
SETUP: --tamper corpus/evidence/round40/db-wal-probe.txt is not a mapped receipt
rc=2
```

That receipt *is* mapped at the tip (§1.2 line). Exit 2 (setup) is defensible; the sentence is false.

### Checked and cleared (not defects)

- Derivation is stem-exact and unique; `-first-run` is not inherited by prefix; legacy `probe-r19-*` logs stay
  unmapped; a `plans/sub/x.py` duplicate is out of the declared `plans/*.py` scope (fixture-invisible by
  declaration, not by accident).
- `temp-paths` masking applies only to the table-declared kind; derived mappings are strict `byte`; masking is
  applied to both sides and the tamper control compares the same way.
- Comparison is stdout-only, declared in the docstring; probe exit != 0 is a `differ`; a timeout is a `differ`.
- stderr noise only: cloning a lane whose HEAD is detached prints git's detached-HEAD advice into the tool's
  stderr (my clone is at `ec1005a`; `measure.sh`'s lane was on `master`, which is why its receipt has no such
  block). It is why `full.txt` / `full-run2.txt` carry the same 17-line advice header; both files are otherwise
  the tool's own lines and are bit-identical.
- Round-40 C1/C2 counters, the battery, `round_close.py` and the routed registry rows were outside this seat's
  scope and were not re-run.

---

## Evidence index (`.ufo/waves/round-40/falsify/F40TipReceipts/`, `sha256.txt`)

| file | sha256 | what |
|---|---|---|
| `full.txt`, `full-run2.txt` | `a83d0438…5a0156` (both) | two full runs at `ec1005a`, bit-identical |
| `list.txt` | `153183d6…2e4a43c` | `--list` at the tip (7 mapped, 2 derived) |
| `tamper-all-six.txt` | `8c39d1f0…a496` | explicit `--tamper` on all six equal receipts |
| `fixtures.txt` | `0b46e41e…eeac4` | f1 collision/`-first-run`/no-command; f2 first-match; f3 empty receipt |
| `f4-single-space.txt` | `047658a9…841a` | single-space padding → false `differ` |
| `epsilon-documented-out.txt` | `de14ba93…0243b` | f2 receipt proven equal to the documented command's output |
| `only-skip-runs.txt` | `a6ba7b27…049d` | `--only` on skip-only selections: rc 0, no control |
| `only-tamper-cwd.txt` | `36cd4d6f…bc11` | `--tamper` excluded by `--only`; cwd=/tmp run |
| `audit-stems.txt`, `audit_stems.py` | `9b8c7e04…`, `34418ade…` | independent stem/derivation audit |
| `base-lines.txt`, `now-lines.txt` | `1cb72ddd…`, `b964a421…` | baseline vs tip status lines |
| `fixtures-src.txt` | `9f379af6…ef2` | fixture layout description |

VERDICT: tip-receipts-attack-6-defects
