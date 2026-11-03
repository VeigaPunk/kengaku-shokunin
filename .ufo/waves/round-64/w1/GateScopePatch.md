# GateScopePatch — R64-C2 depth-gate path-token scope repair (routed defect L-1)

Seat: `GateScopePatch` (kengaku r64 w1). Claim worked: **R64-C2** (operability). Frozen
rules: `plans/round-64-claims.md` @ `859ac24f41061bffde588b9ed5d5adfea5ca8e27`.
Work was done on a clean `--shared` clone of the lane at that commit; nothing was committed,
nothing outside this seat dir and its scratch dir was written.

## Verdict on the frozen R64-C2 predicate

| clause | requirement | observed | verdict |
|---|---|---|---|
| (a) | escape fixture under the PATCHED gate fails with `DETAIL escape=` and rc 1 | `DETAIL escape=/home/vgpnk/.config/uv/uv-receipt.json`, `PREDICATE R63-C2 fail`, rc 1 (`receipts/escape-after.txt`) | **PASS** |
| (b) | selftest exit 0 with FOUR cases, each asserting verdict + a stable finding line | `SELFTEST GOOD/BAD-COUNT/NO-SECTION/BAD-ESCAPE … finding=ok ok`, `SELFTEST pass`, rc 0 (`receipts/selftest-after.txt`) | **PASS** |
| (c) | real SKILL section unchanged | `ROWS n=16 class_match=True count_mismatch=0 paths total=24 resolved=24 share=1.00`, `PREDICATE R63-C2 pass`, rc 0 (`receipts/real-section-after.txt`) | **PASS** |

Red-before reproduced on the unpatched freeze gate, byte-identical to the committed capture
(`.ufo/waves/round-64/claims/escape-before.txt`): `ROWS n=16 class_match=True
count_mismatch=0 paths total=2 resolved=2 share=1.00`, `PREDICATE R63-C2 pass`,
`FIXTURE absolute-token=/home/vgpnk/.config/uv/uv-receipt.json inside_root=False`, rc 0
(`receipts/escape-red-repro.txt`).

## Patch (authoritative bytes: `gate-scope.patch`, sha256 `2b3282cc69515493313b6bc35320a65df6e351799bb83eaf9783e29cec0c54b7`)

Base blob `HEAD:plans/round63_gate_checks.py` sha256
`797085c242a63d0b38f875b6f67550848ddac34dd7f5dbd20861ad3849e7a18a` (= lane tree at read time);
patched file sha256 `a98d9c0f75600ea4f99573d2ca291b1ffd97cffc18a53a3a65dce7b7941dfe17`
(`receipts/patch-sha.txt`). `git -C clone-head apply --check gate-scope.patch` → rc 0. Applying the
patch to a fresh clone of the freeze tip reproduces the patched file byte-exact
(sha256 `a98d9c0f…`) and that landed tree passes the four-case selftest and the real-section
run (`receipts/landing-check.txt`). The diff carries the host git config's mnemonic prefixes
(`i/`…`w/`); `git apply` (proven above) and `patch -p1` both accept them, and the in-file
headers name `plans/round63_gate_checks.py` for both sides.

Behavioural delta, confined to the depth gate:

1. `_escape_reason(root, token)` (new helper) rejects a token that is absolute, that has a
   `..` segment, or whose `os.path.normpath(root/token)` is not `is_relative_to(root)`; reasons
   are `absolute` / `dotdot` / `outside-root`.
2. `_resolves()` keeps its signature and returns False for any such token before the
   existence test, so the share, `resolved == total` and every row-pointer price the same
   tokens as before for in-root paths.
3. `depth_measure()` builds `escapes = [tok for tok in tokens if _escape_reason(...)]`, adds
   `not escapes` to the predicate conjuncts, and prints `DETAIL escape=<tokens>` (comma list,
   `_short`-limited) as the first DETAIL line on failure. The escape set is over the section's
   path tokens, the same population the share prices.
4. `--selftest` grew from three to four legs; each leg now also asserts one stable finding line
   (`PREDICATE R63-C2 pass`, `DETAIL count-mismatch=class-02:got=8,want=7`,
   `DETAIL section-absent heading='## Decision table — grader class → offline replay recipe'`,
   `DETAIL escape=/usr/bin/,../escapee.json`). `BAD-ESCAPE` puts an existing absolute host
   path (`/usr/bin/`) in row 0's receipt-pointer cell plus a `../escapee.json` token in the
   section prose, so the unpatched gate resolved the absolute token and printed no escape line;
   the patched gate resolves neither (`receipts/discrimination.txt`).
5. Module docstring: `depth` resolution sentence and the `--selftest` description updated; a
   dated `(2026-11-03, r64-C2)` ambiguity note records the escape rule. No other code path
   changed; `trio` is untouched (`receipts/trio-sanity.txt`: green entry `TRIO pass` rc 0, first
   frozen trio-red entry still `TRIO fail missing=source,verified-at,recheck` rc 1).

## Receipts (all in `receipts/`; each file carries the exact command that produced it)

| receipt | command (abridged) | key observed line | rc |
|---|---|---|---|
| `clone-head.txt` | `git clone --shared <lane> <scratch>/clone`; `rev-parse HEAD`; `sha256sum` base/patched | `859ac24f…`; base `797085c2…`; patched `a98d9c0f…` | 0 |
| `escape-red-repro.txt` | committed driver retargeted (LANE only) at pristine clone `clone-head` | `PREDICATE R63-C2 pass`, `resolved=2`, absolute token counted resolved | 0 |
| `escape-after.txt` | same fixture against patched clone | `DETAIL escape=/home/vgpnk/.config/uv/uv-receipt.json`, `PREDICATE R63-C2 fail` | 1 |
| `selftest-after.txt` | `plans/round63_gate_checks.py --selftest --work <scratch>` | `SELFTEST pass` (4 legs, `finding=ok` each) | 0 |
| `real-section-after.txt` | `depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root .` | `ROWS n=16 … total=24 resolved=24 share=1.00`, `PREDICATE R63-C2 pass` | 0 |
| `discrimination.txt` | `red/discriminate_escape_fixture.py <patched> <work>` | unpatched: `resolved=18`, no escape line; patched: `DETAIL escape=/usr/bin/,../escapee.json` | 0 |
| `trio-sanity.txt` | `trio` on one green + one frozen-red entry | `TRIO pass` / `TRIO fail missing=source,verified-at,recheck` | 0 / 1 |
| `patch-sha.txt` | `sha256sum gate-scope.patch`; `git diff --stat/--numstat` | `97 insertions(+), 17 deletions(-)`, one file | 0 |

Supporting, re-runnable artifacts in this seat dir: `red/escape_red_repro_head.py` (committed
driver, LANE → pristine clone), `red/escape_red_repro.py` (LANE → patched clone),
`red/discriminate_escape_fixture.py` (materialises the freeze-tip gate with
`git show 859ac24f…:plans/round63_gate_checks.py` and compares both gates on the same fixture),
`patched-round63_gate_checks.py` (convenience copy, sha256 above; the patch is authoritative).

## Risks and named limitations (reported, not repaired)

- **Section-wide escape set.** One absolute/`..` token anywhere in the decision-table section
  fails the gate, not only in a pointer cell. That follows the frozen sentence ("collect the
  escape set … FAIL the predicate when the escape set is nonempty") and the share's existing
  token population; the real section carries none, so nothing regresses today.
- **`..` is rejected syntactically**, even for a token like `corpus/../corpus/x` that would
  normalize back inside the root. The frozen rule says "no `..` segment"; the docstring note
  records it.
- **Lexical only.** A symlink inside the root that points outside still counts as resolved
  (`normpath`/`is_relative_to` never resolve links). Out of the claim's scope; named here so a
  later closure does not read the gate as a sandbox.
- **Selftest output shape changed additively**: a fourth leg plus a `finding=ok|BAD` field. Round-63
  selftest receipts (three lines) stay historical, not comparable line-for-line.
- **Patch base is the freeze blob** `797085c2…`. If `plans/round63_gate_checks.py` differs when
  the L1 lands it, `git apply` fails rather than applying partially; `patched-round63_gate_checks.py`
  is the byte-exact target (sha256 `a98d9c0f…`) if the L1 prefers a copy.
- The `BAD-ESCAPE` fixture's absolute token is `/usr/bin/`, which exists on this host, which is
  what makes the unpatched-vs-patched contrast observable; the leg's assertion is on the
  `DETAIL escape=` line, which does not depend on that path existing.

## Tooling, network, host discipline

No tool was installed or upgraded; no network call was made; no pacman invocation; no server or
port bind (5328/8080 verified free and left alone, `ss -ltn` at start). Git was read-only
(`clone`, `rev-parse`, `show`, `diff`, `status`, `apply --check` — the last writes nothing).
Scratch `/fast/scratch/hyaku/kengaku-r64/GateScopePatch` was removed after these receipts were
copied here.

## Files written (absolute paths)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/gate-scope.patch`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/patched-round63_gate_checks.py`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/red/escape_red_repro_head.py`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/red/escape_red_repro.py`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/red/discriminate_escape_fixture.py`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/receipts/{clone-head,escape-red-repro,escape-after,selftest-after,real-section-after,discrimination,trio-sanity,patch-sha,landing-check}.txt`
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/GateScopePatch/receipts/gate-scope.patch`
