# F37RevQuality — the round-37 QUALITY.md criteria (Q26, Q27) reviewed

Seat: reviewer, wave 2 (falsify), round 37 (hyaku run 8, 2026-10-26). Target: the criteria added to
`corpus/QUALITY.md` this round. Scope: `git -C <lane> diff 3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd
357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5 -- corpus/QUALITY.md` adds exactly two rows — **Q26** (`corpus/QUALITY.md:383-405`) and
**Q27** (`corpus/QUALITY.md:409-449`). No other row changed.

Measurement base: my clone of the landing tip (`/fast/scratch/hyaku/kengaku-r37/F37RevQuality/fx/lane`,
`git rev-parse HEAD` → `357deceb3b5ac8c3c5f9a3edb4d56139d8f8d9b5`, `git status --porcelain` → empty),
plus derivative clones of it at `3ea9a1d9` for red-before runs. The lane itself was never written.
Receipts: `.ufo/waves/round-37/falsify/F37RevQuality/01…08-*.txt` (each carries its command and output).
Scratch deleted at the end. No tools installed (none needed).

## 1. The four required properties, per criterion

| property | Q26 | Q27 |
|---|---|---|
| cites the lesson that produced it | yes — `corpus/lessons/round-37.md` §Mistakes (1), the anchor-drift row (`QUALITY.md:405`) | yes — §Mistakes (2), the vacuous-battery row (`QUALITY.md:447`) |
| names what it supersedes | yes — "Supersedes: none." (`:405`), accurate: no earlier row covers anchor digests | yes — supersedes Q24's middle clause, quoted verbatim (Q24 at `:300-301`: "every single-property junk mutant must be rejected"), and preserves Q24's ordering rule and `unevaluated` leg (`:448-449`) — consistent with the file's never-edit-in-place convention |
| testable | yes — green and red-before both reproduced (§2) | yes — predicate lines match the L1 receipt and all four controls (§2) |
| Limits honest | mostly — three unstated vectors (F4, F5, F6) | **no** — the gameability limit the round itself demonstrated is missing (F1), plus two text defects (F2, F3) |

## 2. Checks re-run (command → output)

- Q26 green at tip — `python3 plans/anchor_digest_check.py --lane .` on my clone →
  `rows=107 tokens=15 defects=0`, exit 0 (receipt 01). Matches Q26's stated output shape.
- Q26 red-before — the tip's checker against a clone at `3ea9a1d9` →
  `rows=103 tokens=11 defects=5`, exit 1, defects exactly S110 `digest-short` (63-hex) +
  S070/S072/S073/S074 `digest-unknown` (receipt 02). Matches Q26's quoted numbers exactly.
- Q27's pinned gate digest — `sha256sum plans/pkg_gate.py` on my clone →
  `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` = the digest Q27 pins.
- Q27's predicate — cited from the L1's committed receipt
  (`.ufo/waves/round-37/integrate/measure-final.txt`): `BATTERY fixtures=64 wrong=0
  renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`,
  `PREDICATE C1 pass`, exit 0. Inputs verified unchanged since that measurement:
  `sha256sum plans/round37_c1_verify.py` → `dbc9f719…3413cc` (= the receipt's line), and
  `git diff 5c7d5d75 357dece --stat -- plans/` → only `plans/round37_c1_attribution.py` added (+89).
  The counter also executes on my clone (dev mode, receipt 07): `--battery r36 --only M01` →
  `BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANT M01 P1 killed by=r36-P5`,
  `MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 n/a`, exit 0.
- Q27's four controls, all quoted numbers confirmed by reading the committed files
  (`.ufo/waves/round-37/claims/`): `control-c1-nothing.txt` → `killed=5 survived=50`,
  `PREDICATE C1 fail`; `control-c1-gate-edited.txt` → `invalid=55`; `control-c1-mislabel.txt` →
  `wrong=1`; `control-c1-example.txt` → `killed=6`, M08 the extra kill.
- Q26's Limits, verified where testable: membership-not-binding — S111's anchor set to S112's
  digest in a scratch clone → `RESOLVED S111 … via=corpus/evidence/round37/tb2-git-webserver/SHA256SUMS`,
  `defects=0` (receipt 06); shared manifest basenames — `git ls-tree -r --name-only HEAD | grep
  SHA256SUMS` → 6 files under `corpus/evidence/`, all named `SHA256SUMS`; S037 not scanned — its
  anchor cell (`corpus/SOURCES.md:59`) reads "P1 receipts pinned by sha256 in the script", no hex
  token; laundered-manifest deflection — `plans/pkg_gate.py:167` re-derives every capture digest
  from bytes (`if sha256(capdir / name) != digest:`); uncommitted capture cannot launder — an
  untracked `SHA256SUMS` naming all five digests still leaves `defects=5`, exit 1 (receipt 04).
- Q27's Limits, verified where testable: the excluded-branches list matches
  `plans/round-37-claims.md` §C1 verbatim; kill-is-a-result-difference confirmed in code
  (`plans/round37_c1_verify.py:17`: "Exit codes other than 0/1 are kept as they are"); the
  co-occurrence example is real (`r36-P7` observed `P1,P3,P6,P9` in measure-final.txt); the eleven
  falsifier cases exist (`build/R37AnchorSweep.md` §5, 11 rows); `SCORECARD.md:564` is the
  `package-gate` capability row.

## 3. Findings

### F1 (major) — Q27 overstates its check: the Limits omit the counter-gameability/attribution limit the round itself demonstrated

Q27's only check is the counter run (`QUALITY.md:415-421`), and its Limits (`:440-446`) name
observationality, excluded branches, the mutant-list denominator, crash-kills, co-occurrence and
budget — but not what wave 1 and the L1's post-hoc audit established about that same counter:

- A hostile two-fixture battery reproduces the identical pass. Receipt
  `.ufo/waves/round-37/build/R37CritC1Battery/receipts/predicate3.txt`: `BATTERY fixtures=16
  wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`,
  `PREDICATE C1 pass` — with 49 of the kills attributed to `crit-p10-sidechannel`, a fixture whose
  reference DEFECT set is empty (`observed_defects=-`). The L1's rebuilt audit
  (`.ufo/waves/round-37/integrate/c1-attribution-hostile.txt`) reproduces it: `PREDICATE C1 pass`,
  then `ATTRIBUTED 6/55 UNATTRIBUTED=49`, exit 0; the landed battery scores `ATTRIBUTED 55/55
  UNATTRIBUTED=0` (`integrate/c1-attribution.txt`).
- The lane's own lesson states the consequence — `corpus/lessons/round-37.md:48`: "The landing
  therefore rests on that audit plus the code review of `plans/battery37/`, not on the counter
  alone" (19 words). SCORECARD records it too — `SCORECARD.md:1291`: "Wave 1 showed the counter
  alone is uninformative" (8 words).
- Q27's citation does not reach that record: it cites §Mistakes (2) only (`QUALITY.md:447`); the
  gameability/attribution record is §Mistakes row 7 (`round-37.md:48`). Its closest Limits
  sentence (`:442-443`) — "a kill records a result difference, not a reason — the result is the
  raw exit code" (16 words) — covers crash-kills, not side-channel forgeability, the single-sample
  null run, or fixture code running with the counter's privileges.

So the criterion presents `PREDICATE C1 pass` as the executable test of "a single-defect fixture
kills that class's silence mutant" while the round demonstrated the same line from a battery that
exercises none of the 50 classes. A reader applying Q27 alone over-trusts the pass; the honest
fix is one Limits sentence naming the gameability and pointing at the attribution audit
(`plans/round37_c1_attribution.py`) as load-bearing — which is exactly what SCORECARD already
says and Q27 does not.

### F2 (minor) — Q27 miscounts its own battery: "55 fixtures"

`QUALITY.md:445`: "55 fixtures is a budget, not a search for every reachable defect" (12 words).
The battery runs **64** fixtures (`measure-final.txt`: `BATTERY fixtures=64 wrong=0
renamed_disagree=0`); **55** is the mutant count (`plans/round37_c1_verify.py`, `TOTAL = 55`,
M01–M55). The count-without-unit slip is the exact class this round mined — lesson Mistakes row 5:
"a count is only meaningful with its unit named". Should read "55 mutants" (or "64 fixtures").

### F3 (minor) — Q27's `wrong=0` sentence overstates the check for 14 of the 64 fixtures, and "single-defect" is untestable by the counter

`QUALITY.md:426-427`: "each fixture must carry the reference's exact verdict and `DEFECT` set
(`wrong=0`)" (13 words). The counter enforces the DEFECT-set leg only where a fixture declares
one: `plans/round37_c1_verify.py:328` — `ok = res[0] == want_rc and (declared is None or res[1]
== frozenset(declared))` — and the 14 round-36 fixtures are built with `defects: None`
(`r36_fixtures`), shown as `declared=-` for all 14 in measure-final.txt. Those 14 are
verdict-checked only. Related: the counter has no notion of an edit count, so the criterion's own
term "single-defect fixture" is not what `wrong=0` tests — `build/R37CritC1Battery.md`'s attack
table records a two-edit fixture passing (`FIXTURE crit-multi-defect declared=P3,P8 … ok`,
"not caught").

### F4 (minor) — Q26's erratum rule only recognizes the literal "Erratum (round 37)"

`QUALITY.md:386`: corrections go "by an appended `Erratum (round 37): S<id> anchor sha256 …`
lesson line" (13 words). The checker's regex is hardcoded to that literal
(`plans/anchor_digest_check.py:80`: `ERRATUM = re.compile(r"^ {0,3}Erratum \(round 37\): (S\d{3,})
anchor sha256\b")`). Demonstrated (receipt 08): a wrong S111 token corrected by an uncommitted
`Erratum (round 38)` line carrying the wrong token and the resolving digest → `DEFECT S111 …
class=digest-unknown`, `defects=1`, exit 1; the identical correction written as `Erratum (round
37)` → `defects=0`, exit 0. Since criteria are never edited in place, the standing text sends a
round-38 fixer to a check that rejects the prescribed form. The Limits (`:399-402`) do not note
the instance-hardcoding.

### F5 (minor) — Q26's erratum exemption is read from the working tree: an uncommitted erratum launders a wrong anchor token, and no clean-tree condition is stated

Q26's parenthetical (`QUALITY.md:392-393`): "it reads committed blobs only, so an uncommitted
capture cannot launder a digest" (13 words) — true for captures (receipt 04: untracked manifest
naming all five digests → still `defects=5`, exit 1). But errata are read from the working tree
(`plans/anchor_digest_check.py:161`: "erratum lines in committed lessons, read from the working
tree"), as are the rows themselves (`parse_rows` reads the working-tree `corpus/SOURCES.md`).
Demonstrated (receipt 03): at `3ea9a1d9`, appending the S110 erratum line to the committed
`corpus/lessons/round-36.md` without committing → `defects=4` (S110 exempted), `git status
--porcelain` → `M corpus/lessons/round-36.md`. So an uncommitted lesson edit — not a capture —
clears a wrong anchor token. Q26's check command (`:388`) states no clean-clone condition, unlike
Q27's (`:421`); on a dirty lane the check mixes working-tree rows/errata with HEAD evidence.

### F6 (minor) — Q26 accepts a token shape it forbids: mid-ellipsis prefix+suffix, suffix never checked

`QUALITY.md:383-384` allows "64 lowercase hex (or a declared prefix ending in `…`)" (9 words).
The token regex treats `sha256 <hex>…<more>` as a prefix abbreviation and never inspects what
follows the `…`. Demonstrated (receipt 05): S111's anchor set to `sha256 526aee3d…ffffff` (false
suffix) → `ABBREV S111 prefix=526aee3d`, `defects=0`, exit 0. Latent today — the verbose run shows
the 15 tokens are 14 `RESOLVED` + S036's 8-hex prefix + S110 exempted; no row uses a mid-ellipsis
token — but the criterion states a stricter contract than the tool enforces.

## 4. Answer to the seat question

Does any criterion overstate what the round-37 tools check? **Yes — Q27** (F1: the pass line is
forgeable by the battery it runs and the load-bearing attribution audit is absent from the
criterion; F2/F3: smaller overstatements of the same check). **Q26 does not overstate** what its
tool checks — its three defects (F4–F6) are unstated strictness limits and an instance-hardcoded
correction form, i.e. places where the tool is narrower or differently-shaped than the criterion's
text. Both criteria otherwise cite the right lesson rows, name their supersession correctly, and
are executable as written (green and red states reproduced).

## 5. Not covered / residual risk

- The full C1 predicate (55 mutants × 64 fixtures) was not re-run end-to-end by this seat; its
  numbers are cited from the L1's committed receipt with input digests verified unchanged at
  `357dece`. The dedicated rerun seat covers the full run.
- The 50 `battery37` fixture builders were not audited line-by-line; the landed battery's
  attribute-cleanliness rests on the L1's audit receipts (`ATTRIBUTED 55/55 UNATTRIBUTED=0`),
  which I read but did not re-derive.
- C2's counter (V1–V7) and the probe are out of this seat's scope (other seats own them).
- Reproducing Q26's red-before needs the tip's checker pointed at the old tree (the script does
  not exist at `3ea9a1d9` and has no `--commit` flag); the criterion's red-before sentence gives
  no command shape. Noted for whoever fixes F4/F5; not counted as a defect.

VERDICT: quality-6-defects
