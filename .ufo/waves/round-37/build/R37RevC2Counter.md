# R37RevC2Counter — review of `plans/round37_c2_verify.py` (C2 counter) vs `plans/round-37-claims.md`

Seat: R37RevC2Counter (reviewer, leaf). Round 37 wave 1, 2026-10-26. Scope: the C2 counter only —
V1–V7: what each reads (committed bytes vs working tree), what it cannot see, false-green and false-red
paths. No lane file was edited; no scratch dir was needed (all commands were read-only: `read`, `grep`,
read-only `git rev-parse/status/check-ignore`, `sha256sum`, `wc`, `awk`, and python snippets that only
printed). No `lsp` device exists in this session's toolset, so caller/definition checks are from direct
file reads plus runtime demos of the cited expressions; this unavailability is recorded here.

Lane state at review: HEAD `44b7298ae1e03791173097cef0e898285f238870`; `git status --porcelain` = 8
untracked paths (`.ufo/waves/round-37/**`, `corpus/evidence/round37/prior-art/`), no modified tracked
files; `git check-ignore .ufo` → not ignored. Working-tree digests match the pins: `pkg_gate.py`
`ea638822…edd41`, `git_webserver_probe.py` `63cb75cf…eedf`, dry table `0095e591…66f3` (`sha256sum`).
Live check states (module harness: import `round37_c2_verify`, run v1/v3/v4/v5/v6/v7):
`V1 (True, 'listed=6 bad=0 extra=0')`, `V3 (False, "rows=3 bad=['S111:row','S112:row','S113:row']")`,
`V4 (False, 'receipt or entry absent')`, `V5 (True, 'probe=frozen dry_byte_equal=True')`,
`V6 (True, 'census_exit=0')`, `V7 (False, 'receipt or entry absent')` — the S111–S113 rows, entry and
map are not landed yet; V2 was not executed end-to-end (it re-runs the 22-case sandboxed probe via gate
P10); its analysis is from code plus the recorded controls.

All paths below are under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/`. Counter line numbers are
from `plans/round37_c2_verify.py` (232 lines); gate numbers from `plans/pkg_gate.py` (398 lines).

## What each check reads, in one line each

- V1 `:71-84`: working-tree `SHA256SUMS` + capture bytes vs `CAPTURES` pins `:45-52`.
- V2 `:87-96`: working-tree `pkg-spec-r37.json` `:88` (mutated `:89`), runs the gate `--rerun
  --require-clean-tree` with `--root <lane>`; trusts exit code only (`:95`).
- V3 `:108-117`: working-tree `corpus/SOURCES.md` (hardcoded `:99-101`), spec rows only.
- V4 `:122-149`: working-tree receipt + entry + frozen dry table; arithmetic consistency + substring naming.
- V5 `:152-157`: digest pins on probe and dry table, then runs `probe --dry` and compares stdout to the file.
- V6 `:161-163`: fleet-absolute census script, `validate --file <lane>/corpus/SOURCES.md`, exit code only.
- V7 `:167-203`: working-tree receipt + entry; requirement-map section only.

## Findings — false-green (a wrong PASS is reachable)

**F1 (HIGH) The "frozen" spec template is pinned nowhere.** V2/V3/V4/V7 all do
`json.loads((lane / SPEC_REL).read_text())` (`:88, :109, :123, :168`) and no check pins
`pkg-spec-r37.json`'s digest (the only digest constants are `PROBE_SHA256 :55` and `DRY_SHA256 :56`;
gate P1 pins what the spec itself lists, `pkg_gate.py:112-115`). The claims call it "the frozen
template" (counter docstring `:9-10`), but relaxing `entry_rules` (`min_quotes`, `quote_words`,
`row_tier`, `row_status`, `min_teaches_words`), swapping `rows`/`entry`/`receipt`/`capture_dir`, or
editing the S111–S113 `sha256` pins re-bars V2/V3/V4/V7 silently and C2 still prints
`PREDICATE C2 pass`. Only deleting `frozen_instruments` outright is caught (`c_instruments` returns
False on empty pins, `pkg_gate.py:113-115`). The freeze exists only as prose.

**F2 (HIGH) V4's "named in the entry" is a bare substring test over real colliding ids.** `unnamed =
[c for c in no if c not in entry]` (`:146`). The frozen dry table contains both `token-in-body` and
`wget-token-in-body`; demo: entry text "…(`wget-token-in-body`)…" → `[c for c in ["token-in-body"] if
c not in entry]` → `[]`, i.e. a receipt line `CASE token-in-body … match=NO` counts as named although
the entry never mentions the curl case. Same prefix-embedding risk for any future id pair. A
backtick/token-boundary match would close it.

**F3 (HIGH) V7 ties labels to verdict polarity only, never to relevance.** `:192-200`: the cited set
needs ≥1 case with observed `fail` (enforced) / `pass` (unenforced) / both (`partly`); nothing links
the cited case to the content of the instruction line. A map that cites `static-file-no-git` (pass)
for every unenforced row and `no-server` (fail) for every enforced row is polarity-consistent whatever
it claims. The curl/wget twins (`token-in-body`, `wget-token-in-body`, both observed=pass in the
receipt) are interchangeable as evidence. The docstring's parenthetical (`:25-27`, "whose claims are
not tied to the executed verdicts fails here") overstates: only the verdict counts are tied.

**F4 (HIGH) Committed-vs-working-tree: the counter measures uncommitted bytes and cannot know it.**
Every V reads the working tree; nothing pins lane HEAD or compares it to the landing tip. The only tree
constraint anywhere is V2→P9, and P9 is `git ls-files --others --exclude-standard` — untracked files
only (`pkg_gate.py:259-265`). Modified tracked files (`corpus/SOURCES.md` rows, `corpus/README.md`
bullet, a tracked receipt) are invisible to P9, so a tree with hand-edited registry rows and no commit
can print `PREDICATE C2 pass`. The predicate sentence says "measured on a clean clone" (claims, C2
predicate), so the protocol covers this — but the counter enforces none of it.

**F5 V4 never cross-checks the per-case `match=` flag against that line's own `predicted`/`observed`.**
`:132-133` parse only `observed=` and the literal `" match=NO "`; a receipt line
`predicted=pass observed=fail match=yes` passes V4's arithmetic. Consistency rests entirely on V5's
digest pin and P10's fresh-run byte-compare (`pkg_gate.py:267-290`).

**F6 V3's scope excludes the routed defect class it was meant to close.** V3 iterates `spec["rows"]`
only (`:109-116`) = S111–S113. The round-36 routed item was S110's anchor digest losing a hex digit;
S110's current anchor (`corpus/SOURCES.md:125`) now carries `sha256 4f7ac05e…e96f9c`, which no C2 check
verifies against any capture (that file is not in the r37 capture set). The class survives outside the
three checked rows. Also `rows()` hardcodes `corpus/SOURCES.md` (`:101`) while the gate parses
`spec["sources"]` (`pkg_gate.py:198`) — a spec edit can point them at different files.

**F7 V1 tolerates duplicate/contradictory manifest lines and dot-captures.** `listed[m.group(2)] =
m.group(1)` (`:81`) — a second line for the same name overwrites silently; gate P5 has the identical
overwrite (`pkg_gate.py:166`). Dot-prefixed capture files escape both V1 (only listed names checked,
`:82-83`) and P5 (dotfiles skipped, `pkg_gate.py:177-180`).

**F8 V7 and V4 disagree on duplicate CASE ids.** V4 counts every CASE line (`:132-133`); V7's
`observed[m.group(1)] = m.group(2)` (`:176-177`) is last-wins. A receipt with a duplicated id (one
pass, one fail) can satisfy V4's summary arithmetic while V7 judges polarity by whichever line is last.

**F9 V5's "byte_equal" is newline-normalized on both sides.** `text=True` subprocess output
(`:156-157`) and `Path.read_text()` both apply universal newlines, so a CRLF dry table compares equal
to LF stdout; the `dry_byte_equal=True` label overstates byte equality (the raw-bytes digest pin at
`:56` is what actually binds the file).

## Findings — false-red (a wrong FAIL, or a structurally blocked green)

**F10 V7's citation grammar is brittle in both directions.** `` `([a-z0-9-]+)` `` (`:192`) extracts
only when the entire backtick content is lowercase/hyphen: demo — `` `git push` `` and `` `curl -L` ``
extract nothing (`cited=[]` → "cites no case"), while a lone `` `curl` `` extracts `curl` →
`observed.get` → None → "unknown case" defect. Prose mention of a case id outside backticks — the
hinted path — is likewise invisible and defects the row. The section header must match
`^## Requirement map\n` exactly (`:179`): `## Requirement Map` or a trailing space reads as "no
section".

**F11 V3 requires exactly one sha256 token, byte-identical.** `toks != [row["sha256"]]` (`:116`): an
anchor whose prose cites a second digest reds (demo: two `sha256 <hex>` tokens → list of 2 ≠ [pin]);
an uppercase-hex digest also reds. Strict by docstring design (`:19-20`, "no other sha256 token") but
honest anchors citing e.g. an upstream tree digest cannot be written.

**F12 V6 couples C2 to whole-registry hygiene.** census `validate` exits 1 on any E-finding on any row
of the lane's registry (script header, `sources-census.sh:24-30`; selftest `validate-findings-exit-1`,
`:141`), so an unrelated S001–S110 defect fails C2. Today `census_exit=0` (harness output above).

**F13 V6 depends on a hardcoded, unpinned fleet-absolute script.** `CENSUS =
"/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` (`:58`, used `:162`). On a clean clone of
the landing tip without this fleet checkout — the predicate's stated measurement environment —
`subprocess.run` raises FileNotFoundError, caught in main (`:221-222`) as a V6 DEFECT: C2 cannot pass
anywhere the script is absent, and on this host the verdict can change when the unpinned script
changes, with zero lane change. The `--file` flag itself is lane-correct: `resolve_targets` resolves
used-by paths against the file's own lane dir (`sources-census.sh`, `resolve_targets`:
`dir_abs=$(realpath "$(dirname "$file_abs")/..")`, consumed by `usedby_findings`), so this is a
reproducibility defect, not a wrong-tree defect.

**F14 V2 is structurally red in the working lane mid-wave, with no distinguishing diagnostic.** `.ufo/`
is untracked and not gitignored (`git check-ignore -q .ufo` → not ignored), and wave artifacts land
there (`git status --porcelain`: `.ufo/waves/round-37/build/`, `claims/`, `integrate/`,
`corpus/evidence/round37/prior-art/`). P9 counts them (`pkg_gate.py:259-265`) → gate exit 1 → V2
DEFECT even for a perfect package. Correct on a clean clone (the predicate's setting); the gate's
stdout lines printed by v2 (`:94`) do let an operator see `P9 DEFECT`, but the V2 note itself is just
`gate_exit=N`.

## Limits / cannot-see (named, not counted as defects)

- L1 V7 coverage is hardcoded lines 1–9 (`:202`); the capture has 10 lines (`wc -l` = 10), line 10
  being "I'll setup login with the server…". Matches the claims wording ("cover instruction.md lines
  1-9"), but a changed upstream instruction.md with a requirement on line 10 would pass V7.
- L2 V4's naming check counts any occurrence anywhere in the entry, including inside verbatim quotes
  (`:146` passes the whole entry text).
- L3 Receipt authenticity rests on V5's digest plus P10's fresh run compared byte-wise to the receipt
  (`pkg_gate.py:267-290`; cwd is the lane so `--lane .` in `probe_cmd` resolves correctly; the gate
  exits 0 only on zero defects, `:387`). V4 alone is satisfiable by a hand-typed receipt — exactly what
  `control-c2-skip.txt` demonstrates being caught one layer up.
- L4 P2 is presence-only by construction: v2 overwrites `receipt_sha256` with the digest of whatever
  file it finds (`:89`, docstring `:9-11`).

## Verified-good (calibration positives)

- All seven checks exist, run in order, and a crashing check becomes a DEFECT, never a pass
  (`:218-224`); the printed predicate matches the claims sentence (`checks=7 defects=0`, `PREDICATE C2
  pass`, exit 0 iff defects=0, `:225-227`).
- V1 green today with the manifest exactly the six pinned files; V5 green with probe and dry table at
  their freeze digests and `--dry` stdout byte-equal (harness outputs above).
- V3's exactly-one-token rule would have caught the S110-class lost digit for any row it covers; V7's
  unknown-case rule does anchor citations to real receipt ids; the gate's P10 byte-compare and P5's
  extra-file sweep (`pkg_gate.py:171-180`) cover gaps V1/V4 leave (extra unlisted capture files are
  caught by P5, not V1).
- V2's trust of exit code only is sound: gate exits 1 on any defect, 2 on setup/crash (`:387`, `:391-393`).

## Residual risk and verification gaps

- V2 was analyzed, not executed (it re-runs the 22-case bubblewrap probe through the gate; two prior
  runs are on record in the receipt). The five non-V2 live states above are executed evidence.
- Capture bytes were checked only for internal consistency (manifest vs bytes vs spec pins via V1), not
  re-fetched against the pinned upstream URLs.
- F1's exploit (a relaxed spec passing C2) is reasoned from code, not demonstrated end-to-end, to keep
  the frozen tree untouched; the mechanism (`:88-89`, unpinned template) is the evidence.
- Highest-value fixes, in order: pin `pkg-spec-r37.json` by digest (F1); make V4's naming a
  backtick/token-boundary match (F2); make V6 resolve the census script from the lane or pin its
  digest (F13); state in the report that P9 sees untracked files only (F4/F14).

VERDICT: c2-counter-review-14-false-green-9-false-red-5
