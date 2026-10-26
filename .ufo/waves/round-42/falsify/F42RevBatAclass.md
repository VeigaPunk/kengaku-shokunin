# F42RevBatAclass — non-author honesty review of `plans/battery42/a_class.py`

Seat: `F42RevBatAclass` (reviewer, kengaku round 42 wave 2 FALSIFY, 2026-10-26). Target:
`plans/battery42/a_class.py` — the module that kills X6, X7, X14 in the landing run. Method: read the
module and the frozen mutant table in `plans/round42_c1_verify.py`; re-ran the counter on a clean
clone with `--battery-dir` holding only this module and `--only X6,X7,X14`; then built the six
fixtures with the counter's own `Ctx`/`load`, ran the unmodified tool on each with `--verbose`, and
traced executed lines — all inside the Q32 envelope. Report dir:
`.ufo/waves/round-42/falsify/F42RevBatAclass/` (receipts `counter-run.txt`, `inspect-run.txt`). No
lane file was edited; no git/jj mutation anywhere; no package installed (none needed).

## 0. Identity and envelope

- Clone: `git clone -q --no-local <lane> $S/lane && git -C $S/lane checkout -q 508434ad…`;
  `git -C $S/lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r42/F42RevBatAclass/lane`;
  HEAD `508434ad55c709337065611691c426f05875492d`.
- Module digest: `sha256sum` of `plans/battery42/a_class.py` =
  `eef02b5df0a8b5e7e558956eaf3d5fca6fa5701872f11632d5327717def8f1bb` — identical in the clone at
  `508434ad`, in the lane working tree, and equal to the artifact digest the author's wave-1 report
  `R42BatAncClass.md` §0 claims. The reviewed bytes are the landed bytes.
- Envelope (both runs): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`. Counter run 18:06:13 →
  18:06:14; inspection run 18:07:19 → 18:07:20; `ls -A /home/vgpnk/.local/bin | sha256sum` =
  `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` before and after both runs
  (receipt files carry every line).

## 1. What the three mutants advertise

From `plans/round42_c1_verify.py` MUTANTS (id, tool, class, direction, adv, old → new):

| id | class | direction | advertised sentence (tool docstring) | old → new (span) |
|---|---|---|---|---|
| X6 | `digest-wrong-capture` | silence | "A 64-hex token that is a committed capture but not this row's is digest-wrong-capture" (`plans/anchor_digest_check.py:89-92`) | `elif tok not in row_scope:` + `if tok in allowed:` → `if False:` (L527-528) |
| X7 | `digest-unknown` | silence | "a token that is no committed capture at all is digest-unknown" (`:92-93`) | `class=digest-unknown` → `class=digest-wrong-capture` in the append at L535 |
| X14 | `erratum-digest-unresolved` | silence | "no 64-hex token on it may be outside A unless it is the cited wrong token of the row it names (erratum-digest-unresolved)" (`:111-113`) | `HEX64_ANY.fullmatch(t)` → `HEX64.fullmatch(t)` at L458 |

Silence means: the reference prints the declared class and exits 1; the mutant must not print it.

**Why the observed class certifies the branch.** In the unmodified tool each class has exactly one
append site (grep over `plans/anchor_digest_check.py`): `class=digest-wrong-capture` only at :530,
inside the `if tok in allowed:` (L528) that X6 disables; `class=digest-unknown` only at :535, the
`else` of that same test; `class=erratum-digest-unresolved` only at :459, inside the L458 condition
X14 narrows. So a reference run that prints the declared class proves the mutated branch's condition
held for the advertised reason — a substitute that reached the direction another way could not print
that class at all.

## 2. Counter re-run (clone @ `508434ad`, battery dir = only this module)

Command (inside the envelope):
`/usr/bin/python3 $S/lane/plans/round42_c1_verify.py --lane $S/lane --battery-dir $S/batonly --only X6,X7,X14 --work $S/w`

```
PINS total=2 mismatched=0
FIXTURE a_class-x6-sibling-digest tool=anchor expect=reject declared=digest-wrong-capture observed_rc=1 observed=digest-wrong-capture ok
FIXTURE a_class-x6-stale-manifest tool=anchor expect=reject declared=digest-wrong-capture observed_rc=1 observed=digest-wrong-capture ok
FIXTURE a_class-x7-fabricated-token tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_class-x7-provenance-row tool=anchor expect=reject declared=digest-unknown observed_rc=1 observed=digest-unknown ok
FIXTURE a_class-x14-uppercase-token tool=anchor expect=reject declared=erratum-digest-unresolved observed_rc=1 observed=erratum-digest-unresolved ok
FIXTURE a_class-x14-two-errata tool=anchor expect=reject declared=erratum-digest-unresolved observed_rc=1 observed=erratum-digest-unresolved ok
MUTANT X6 anchor silence killed by=a_class-x6-sibling-digest attributed=L527 hits=2 -- plans/anchor_digest_check.py:89-92 'A 64-hex token that is a committed capture but not thi
MUTANT X7 anchor silence killed by=a_class-x7-fabricated-token attributed=L535 hits=2 -- plans/anchor_digest_check.py:92-93 'a token that is no committed capture at all is digest-
MUTANT X14 anchor silence killed by=a_class-x14-uppercase-token attributed=L458 hits=2 -- plans/anchor_digest_check.py:111-113 'no 64-hex token on it may be outside A unless it is
BATTERY fixtures=6 wrong=0 tampered=0 sidechannel=0
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0 unattributed=0
MUTANTS-BY-TOOL anchor=3/3 order=0/0
ADVERTISED direct=3 indirect=0 none=0
PINS-AFTER mismatched=0
PREDICATE C1 n/a (non-default battery or mutant subset)
rc=0
```

Matches the landing (`measure-final.txt:39,40,44`): same killing fids, same attributed lines. The
landing's X7 shows `hits=6` because the full 29-fixture battery has four more `digest-unknown`-
declaring fixtures (`a_row-x13-staged-capture`, `a_row-x13-url-staged`, `a_row-x15-sibling-digest`,
`a_row-x15-manifest-sibling` — grep over `plans/battery42/`); the killing fixture and span are
identical.

## 3. Per-fixture evidence (verbose reference runs + line trace)

Fixtures built with the counter's own `Ctx`/`load` (driver `kc_inspect.py` in scratch; receipt
`inspect-run.txt`), then the unmodified tool with `--verbose`, then a `sys.settrace` run recording
executed lines (spans: X6 {527,528}, X7 {535}, X14 {458}).

| fixture | reference verbose (the tool's own words) | trace span hits | honesty |
|---|---|---|---|
| `x6-sibling-digest` | `BIND S301 … by=row-path`; `DEFECT S301 … class=digest-wrong-capture detail=committed-capture-belonging-to-another-capture-corpus/evidence/round42/a-class/x6-b/notes.txt-not-the-capture-this-row-names-…` | X6: L527+L528 | honest |
| `x6-stale-manifest` | `BIND S310/S312 … by=url-task`, `BIND S311 … by=row-path`; `DEFECT S312 … detail=committed-capture-belonging-to-another-capture-corpus/evidence/round42/a-class/x6-side/SHA256SUMS-not-the-capture-this-row-names-…` | X6: L527+L528 | honest (manifest-view nuance, §5) |
| `x7-fabricated-token` | `BIND S320 … by=row-path`; `DEFECT S320 … class=digest-unknown detail=not-committed-evidence-and-not-in-a-SHA256SUMS` | X7: L535 | honest |
| `x7-provenance-row` | `BIND S330/S331 … by=provenance-row`, `BIND S332 … by=row-path`; `ABBREV S332 prefix=624ec1420921 matches=624ec14209215a3838133beacfe4c4a3671270b85cf7097c37ce6faf3e00a066` (green); `DEFECT S331 … class=digest-unknown` | X7: L535 | honest |
| `x14-uppercase-token` | `EXEMPT S340 anchor=c32e12b8…` (row green); `DEFECT S340 erratum token=F2046559EF710033AF5D8362FE506CBBCABA0C96AA4A29E2EA593B804D7B5606 class=erratum-digest-unresolved` | X14: L458 | honest |
| `x14-two-errata` | `EXEMPT S350 anchor=fb9bb61c… correction=41919a88…` (clean erratum works); `DEFECT S351 erratum token=91969E9F4E6271547661EFC9E24F452C240DBDD95E36485FA1658E5FFC9114C6 class=erratum-digest-unresolved` | X14: L458 | honest |

Reading of each, against the advertised sentence:

1. **`x6-sibling-digest` — honest, the direct shape.** Row S301 names capture A by explicit path; the
   anchor token is capture B's committed **file** digest; the tool's own detail names `x6-b/notes.txt`
   as the other capture. This is the round-37 M4b/M5 shape the docstring itself cites at :90.
2. **`x6-stale-manifest` — honest second trigger, one nuance.** S312 binds through the task.toml URL
   route (`by=url-task`); its token is the stale digest the sibling directory's `SHA256SUMS` still
   lists for a recaptured file. The tool's capture definition admits that view: "the digest that entry
   lists, and the digest of the committed file bytes, are both accepted views of that one capture"
   (`anchor_digest_check.py:43-46`), so `tok in allowed` is true for a documented reason and the
   defect detail names `x6-side/SHA256SUMS`. The author disclosed the shape in the module docstring
   ("for X6 a manifest-listed digest instead of a file digest", `a_class.py:9-10`). Nuance: the
   fixture tree contains a manifest that disagrees with the committed bytes — a state the real lane
   never has (the same docstring sentence records the two views "verified equal in every task
   directory of this lane at `2c5f4e0`"). The fixture therefore demonstrates ownership of a manifest
   view, not of a byte digest; that is within the advertised definition, not a substitute.
3. **`x7-fabricated-token` — honest, direct.** The token is `sha256(b"no capture anywhere carries
   this: a-class x7\n")`; the tool's detail says `not-committed-evidence-and-not-in-a-SHA256SUMS`;
   the else branch (:535) is the only site that prints the class.
4. **`x7-provenance-row` — honest; the shape difference is the binding route, not the defect
   mechanism.** S331 binds by `provenance-row` (route 1) instead of an explicit path; its token is
   made up, so the same `tok not in allowed` condition holds and :535 prints. The third row's 12-hex
   abbreviation resolves green (`ABBREV … matches=624ec142…`), so the declared set stays exactly
   `{digest-unknown}`.
5. **`x14-uppercase-token` — honest, direct.** The defecting token is the UPPERCASE uncommitted one
   (`F2046559…B5606`); the row's own token is green and exempted. Matches the round-40 source shape
   ("erratum line with an uppercase uncommitted token") and the witness `w14` structure (green row +
   erratum citing an uppercase token).
6. **`x14-two-errata` — honest.** The clean erratum exempts the stale-token row (`EXEMPT S350
   anchor=fb9bb61c…`), so the exemption path and the line check coexist; the second erratum's
   uppercase token (`91969E9F…114C6`) is outside A and is not the anchor token of the row it names →
   the only defect. The defecting token triggers precisely the HEX64_ANY-vs-HEX64 difference X14
   removes.

**Trace.** Both x6 fixtures execute L527 **and L528**; both x7 fixtures execute L535; both x14
fixtures execute L458. No kill in this module rests on the counter's weakest attribution line: X6's
printed `attributed=L527` is the always-executed `elif`, but the semantically loaded L528 also
executes, and the reference's printed class proves its condition was true (§1). The trace also shows
L527-528 executing on the x7 fixtures without an X6 direction — the general weakness wave-1
`R42CritAttribution` named; it carries none of this module's kills.

## 4. Witness modules: not read, not copied

- Frozen rule: "The battery may not import, copy or read the freeze modules (`claims/witness/`); the
  token scan flags `witness`" (`plans/round-42-claims.md:55-56`). The module imports `hashlib` only
  (the single `import` line is :27); it contains no `witness`, `.ufo`, `claims`, `open(`, `read_`,
  `subprocess`, `os.`, `sys.` token; it never calls `ctx.sh`; every write goes through `ctx.write`,
  every git call through `ctx.git`. Measured `sidechannel=0` in both runs.
- Structure vs `w_anchor.py`: `difflib.SequenceMatcher(None, a_class, w_anchor).ratio()` = **0.0733**;
  the only non-blank lines longer than 12 chars present in both are seven contract-boilerplate lines
  (`import hashlib`, `r = ctx.init(d / "repo")`, `ctx.write(r / "corpus/SOURCES.md",`,
  `ctx.write(r / "corpus/lessons/round-37.md",`, `return ["--lane", str(r)]`, the SOURCES header and
  separator, the PROVENANCE table header). No fixture-specific line is shared. The first fixture of
  each mutant is a same-shape re-derivation with different helpers (`capture()` writes no
  `SHA256SUMS`; the witness's `cap()` does), different row schema (`kind capture`/`scope
  fixture-scalar` vs `code`/`fixture`), different ids, paths and bodies; the second fixture of each
  mutant is a new shape. Not a renamed copy. `w_order.py` is order-tool and structurally unrelated
  (claims/receipt histories).

## 5. Repo-local git config, symlinks, `core.worktree`, gpg: none

Walked every built fixture tree: **zero symlinks**; every `repo/.git/config` is the vanilla four-line
`[core]` block `git init` writes (`repositoryformatversion`/`filemode`/`bare`/`logallrefupdates`) —
no `core.worktree`, no includes, no fsmonitor/hooks/external/textconv/sshCommand/pager/filter keys,
no gpg or signature anything. The module writes no config (no `.git/…` path in its source); during
builds `Ctx` pins `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`, and `ctx.git` refuses
any repo that is not its own toplevel; during tool runs the counter pins `core.fsmonitor=false` and
`core.hooksPath=/dev/null`. Every fixture argv is `["--lane", <d>/repo]` — inside `d` (`path_ok`
passed; no contract error in any run).

## 6. Verdict table

| fixture | mutant(s) killed | verdict | reason |
|---|---|---|---|
| `a_class-x6-sibling-digest` | X6 | **honest** | token is capture B's committed file digest; tool detail names x6-b; L528 condition true (class's only append site :530) |
| `a_class-x6-stale-manifest` | X6 | **honest** (manifest-view nuance) | token is the sibling capture's SHA256SUMS view — an accepted view per `anchor_digest_check.py:43-46`; detail names x6-side/SHA256SUMS; disclosed by the author |
| `a_class-x7-fabricated-token` | X7 | **honest** | made-up 64-hex token; detail `not-committed-evidence-and-not-in-a-SHA256SUMS`; else branch :535 |
| `a_class-x7-provenance-row` | X7 | **honest** | same made-up-token mechanism; row bound by provenance-row; abbreviation row green keeps the set exact |
| `a_class-x14-uppercase-token` | X14 | **honest** | defecting token is the uppercase uncommitted one; row's own token green |
| `a_class-x14-two-errata` | X14 | **honest** | clean erratum exempts the stale-token row; second erratum's uppercase token is the only defect |

6/6 honest, 0 substitutes, 0 incidental. The wave-1 substitute patterns (a receipt that is a
directory, an emptied directory, a staged manifest only — `R42CritC1Counter.md` §1) have no analogue
here: every fixture's declared class is printed by the mutated branch's own append site, for the
advertised reason, on a tree built from nothing.

## 7. Residual risks (not defects in this module)

1. The counter's attribution leg prints `attributed=L527` for X6 — the minimum span line, which
   executes on every fixture with an out-of-scope token (my trace shows it executing on the x7
   fixtures too). For THIS module the kills stand on L528 plus the unique append site, but the
   counter's leg f alone cannot distinguish an X6 fixture that never reaches L528; wave-1
   `R42CritAttribution`'s point stands for the counter in general.
2. `sidechannel=0` is scan-only evidence; the module-source read (§4) is the stronger evidence. The
   author's disclosed scan calibration (a capture renamed `run.txt` → `notes.txt` because the path
   contained `/run`, `R42BatAncClass.md` §6) changed no fixture shape.
3. `x7-provenance-row` and `x14-two-errata` pin neighbouring green branches (abbreviation resolution,
   erratum exemption) — a future tool change to those branches moves their declared sets. Intended
   and disclosed by the author (`R42BatAncClass.md` §7.4).
4. This review covers only `a_class.py` (X6, X7, X14). The other battery42 modules (`a_route`,
   `a_row`, `o_clause`, `o_scan`) and the counter's own vectors are other seats' scope.

## Receipts

| file | sha256 |
|---|---|
| `.ufo/waves/round-42/falsify/F42RevBatAclass/counter-run.txt` | `f9aec47a055ebe0dd9b5a1c2344b2c517b2287eaacb95691a2acadccf44278b3` |
| `.ufo/waves/round-42/falsify/F42RevBatAclass/inspect-run.txt` | `bfa73e31944a8da0488dfe7510c0a8e86afb0879b95e6c6c10256c85ee56bce9` |

Scratch `/fast/scratch/hyaku/kengaku-r42/F42RevBatAclass` (clone, battery dir, built fixtures,
driver) deleted after this report was written.

VERDICT: battery42-a_class-honest-6/6-substitute-0
