# R31 C3 — design review: binding the capture to the row's cited URL

Seat: UFO-FSD critic, leaf. No production edit was made; the only lane file this seat wrote is this one.
Scratch: `/tmp/r31-gatedesign/`. Nothing installed or upgraded (no package manager transaction ran).

## 0. State reviewed, and why the state matters

`plans/sources_adopt.py` changed three times while this review ran. Each observation below is tagged with the
body it was taken on.

| md5 | mtime | quote-mode CLI | `--selftest` |
|---|---|---|---|
| `fcd357da78658fa26a463810cb5a319f` | 05:55:10 | **unreachable** — the `elif args.url_map:` guard swallowed the quote-mode body; `--quote-file … --artifact …` exited 2 `--registry and --package are required` | `cases=17 failed=0`, exit 0 |
| `50793383c1c3d0d11ba3720f07df6dfb` | 05:57:16 | reachable; receipt prints `urlmap=none` / `urlmap=entries=N` | `cases=17 failed=0`, exit 0, **argparse usage on stderr** |
| `90603c3f20dc226f53931b27d9a0ba63` | last seen | reachable; receipt prints the binding fields **only when a map was supplied** | `cases=17 failed=0`, exit 0, stderr clean |

The transient body is worth recording rather than ignoring: it shows the claim's counting command
(`--selftest`) is **blind to `main`**. `selftest()` calls `quote_check`/`load_url_map` directly and never drives
the CLI, so the frozen predicate `SELFTEST cases=17 failed=0` can be green while the tool it certifies cannot be
invoked. That is an operability hole in the *predicate*, not only in the body; §9 C6 closes it cheaply.

The design as it now stands (body `90603c3f`, `bind_failure` at :411-432, the binding check at :509, the refusal
precedence at :544-546, `print_quote_report` at :550-578, the provenance comment at :341, help at :969, guard at
:1007):

- map shape: flat JSON `{"<artifact name>": "<url>"}` (:367-389), keyed by the name `load_artifact` prints;
- binding: **existential** — `cited` = every http(s) URL in cell 1; `mapped` = map values of *every* artifact
  that contains the quote; green iff some mapped value normalises into `cited`; else `url-mismatch`, and
  `unmapped` only when no containing artifact has an entry;
- exit codes 8/9 added; 6/7 keep precedence;
- the receipt appends `mismatch=… unmapped=… urlmap=entries=N` **only when `--url-map` was given** (:556), so
  the field's *absence* is the unbound signal and round-30's `QUOTE …` prefix stays byte-stable.

## 1. The decision that actually has to be made: provenance or citation membership?

The flag's name and the section comment (:341, "naming the document each artifact was fetched from") promise
**provenance**. The implementation (:411-432) tests **membership in the row's cited set**. Those two contracts
disagree for exactly the captures this round exists to admit, and the disagreement is not academic — every C1
row cites a repository root and quotes a file at a pinned commit:

```
S092 source cell : https://github.com/laude-institute/harbor
S092 anchor cell : commit 6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5, src/harbor/models/task/config.py: "…"
(staged package, /home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md, rows S092, S093, S100)
```

Live counterexample, both directions, one fixture row shaped like S092 (the quoted sentence in the fixture is
**synthetic**, written by this seat; the row shape, cells and pin are copied from the staged row):

```
$ python3 plans/sources_adopt.py --quote-file rows.md --artifact capture.txt --url-map map-root.json
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=capture.txt mismatch=0 unmapped=0 urlmap=entries=1
  ok S092 words=11 at capture.txt quote="…"                                              EXIT=0
  map-root.json = {"capture.txt": "https://github.com/laude-institute/harbor"}

$ … --url-map map-pin.json
QUOTE rows=1 spans=1 located=0 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=capture.txt mismatch=1 unmapped=0 urlmap=entries=1
  REFUSED S092 url-mismatch words=11 at capture.txt quote="…"                            EXIT=8
  map-pin.json  = {"capture.txt": "https://raw.githubusercontent.com/laude-institute/harbor/6099b8cf…/src/harbor/models/task/config.py"}

$ … (no --url-map)
QUOTE rows=1 spans=1 located=1 found=1 overlong=0 absent=0 malformed=0 cap=25 artifacts=capture.txt
  ok S092 words=11 at capture.txt quote="…"                                              EXIT=0
```

(All three receipts are body `90603c3f`; the sentence in the fixture is synthetic, the map files are quoted
verbatim. Note the third line: with no map the receipt is round 30's exact prefix and says nothing about
binding — see §7.1.)

**The honest map is refused; the coarse map is accepted.** The operator who declares the URL actually fetched is
punished, the operator who declares the repo root is rewarded. Any design that leaves this inversion in place
teaches the lane to write the weaker claim, which is the opposite of what C3 is for.

Therefore the only contract this gate can *truthfully* implement is **citation membership**: the map declares
*which cited URL this capture answers*, not *where the bytes came from*. The gate cannot verify a fetch (no
network, no hash, no provenance store), so a provenance-shaped contract would be an overclaim by construction.
That reframing is not a retreat: membership still catches the realistic laundering modes — a capture built for
row A reused for row B, a blog post or another project's README that happens to carry the sentence, a quote read
in a mirror of a different document. It cannot catch a deliberate false declaration, and §6 says so.

The help text at :969 already states the membership reading ("a URL that row cites — for a capture of a pinned
file this is the citation … not the raw fetch URL"). The section comment at :341 still states provenance. One of
the two authorities has to go; the comment is the one a future maintainer reads first.

## 2. Recommended contract (smallest, seven clauses)

1. **Key = artifact name**, exactly as `load_artifact` names it (basename for a file artifact, relative path for
   a directory artifact), i.e. the same string `locates`/`locating_artifacts` return and the receipt prints.
   *Not row id.* Row-id keying duplicates a fact the row already carries (its cited URL) and says nothing about
   *which* capture answered, so a five-file directory would pass on a row-keyed entry regardless of which file
   holds the quote; it also creates a second authority for "what this row cites", which is the identity
   duplication the lane's own lessons warn about. Artifact keying keeps one authority per fact: the row says
   what it cites, the map says which capture answers it, the gate compares.
2. **Value = one URL the row cites**, in any of the forms §3 accepts. Not "the URL you fetched".
3. **Comparison = set membership** over *all* http(s) URLs in cell 1, after §3 normalisation. Rows S041 and S045
   cite two URLs each (evidence §5), so membership over the set is required, not a first-match.
4. **Binding is existential over locators**: green iff some artifact that contains the quote is mapped to a
   cited URL. Universal ("every locator must be bound") is *wrong* here, because capture directories are per
   round, not per row: two rows citing two repos that share a sentence would make each other's capture an
   "uncited document" and refuse a correct map. Existential is right; it is also unauditable unless the binder
   is printed (§9 C4).
5. **The map is opt-in**, and the receipt must distinguish a bound run from an unbound one. Body `90603c3f`
   appends `mismatch=… unmapped=… urlmap=entries=N` only when `--url-map` was given (:556), so the *absence* of
   `urlmap=` is the unbound signal while round 30's `QUOTE …` prefix stays byte-stable. That is a weaker signal
   than an explicit `urlmap=none` (§7.1) but it is not silent, provided the contract says so and no round cites a
   `QUOTE` line without `urlmap=` as evidence of binding. Making the flag mandatory is the worse failure mode: a
   gate that cannot be run without a map is a gate that will be run with a fabricated one.
6. **Map-shape problems are caller errors (exit 2)**, never citation verdicts.
7. **The map file is round evidence**: the receipt must name it (path or digest), so the claim "the capture was
   bound" is auditable byte-for-byte by a non-author (§9 C3).

## 3. Normalisation: what is defensible and what must not be added

| form | decision | why |
|---|---|---|
| fragment `#L120`, `#section` | **drop** | the server never receives it; same bytes. The *line claim* in the anchor is then unbound — disclose (§6 R6) |
| trailing slash `/a/` vs `/a` | **drop** | same resource on nearly every origin (GitHub 301s). It is a redirect assumption; disclose |
| scheme case, host case | **lower** | RFC 3986 makes both case-insensitive; no two documents collide |
| path case | **preserve** | GitHub paths are case-sensitive; lowering would alias two different files |
| `http` vs `https` | **distinct** | different origin, may serve different bytes; a refusal here is correct |
| `www.` prefix | **do not touch** | a different host string; some origins do differ |
| default port `:443` | **do not touch** | rare; a mismatch refuses, which is the safe direction |
| empty query `?` / percent-encoding | **do not touch** | rare, and either rewrite is a guess about the server |
| query string `?a=1` vs `?a=2` | **distinct** | may serve different bytes |
| `<url>` / backtick decoration in the cell | **trim** (`.,;:)]}>`, :345) | cell formatting, not URL syntax. Note the trim set is still a guess: a backticked URL yields `https://…`` today, and the live registry has **0** such tails (§5), so this is latent, not live |
| `github.com/<o>/<r>/blob/<sha>/<p>` vs `raw.githubusercontent.com/<o>/<r>/<sha>/<p>` | **reject this round** | it is the one rewrite that would let a provenance-shaped map pass for pinned captures, and it is a two-host identity claim (`blob` is HTML-wrapped, `raw` is not — same object id, different bytes) that needs its own test surface. Adding it plus prefix-containment would let a *cited* repo root absorb a *fetched* file URL, but it buys file-granularity only when the row cites a file URL, which none of C1's rows do. Cost/benefit is wrong for this round; name it as a follow-on instead |
| prefix / containment (`capture under the cited path`) | **reject** | it admits every descendant document of a cited URL (issues, wiki, other files) as "the cited document", i.e. it widens the gap instead of closing it, and it is exactly the rule the coarse repo-root map already exploits (§5 case 3) |

## 4. Decision table of refusals

Precedence is the landed order 2 → 4 → 6 → 7 → 8 → 9 (`quote_check`, :541-546). Every refused row is still named,
so one run surfaces all of them.

| # | condition | exit | reason printed | precedence / repair | must NOT become |
|---|---|---|---|---|---|
| 1 | `--url-map` unreadable, not JSON, not a flat `string→string` object | **2** | `--url-map is unreadable: …` / `--url-map must be …` (:378-385, main :995-997) | before anything; repair = fix the map file | never 8/9: a typo'd map must not read as a fabricated citation |
| 2 | `--url-map` without `--quote-file`/`--artifact`, or with `--registry`/`--package` | **2** | argparse usage (`--url-map needs --quote-file and --artifact`, :1007) | usage; repair = pair the flags | never silently ignored (this was live on `fcd357da`, and the guard's placement then broke quote mode; both fixed on `50793383`) |
| 3 | `--artifact` unreadable / holds no UTF-8 text | **2** | `--artifact names no file …` / `--artifact holds no UTF-8 text` | unchanged from round 30 | — |
| 4 | row unparsable, anchor cell with no span, unbalanced span | **4** | `<id>:columns=N` / `no-quote` / `unbalanced-quote` / `escaped-pipe` | unchanged; no span ⇒ no citation to compare, so 8/9 are undefined | must **not** absorb `cites-no-url` (row 9) |
| 5 | span longer than the 25-word cap | **6** | `overlong words=N cap=25 at …` | outranks 8/9: a length defect is computable without a map | — |
| 6 | span absent from every artifact | **7** | `absent words=N` | outranks 8/9: there is no locator to bind | — |
| 7 | no artifact containing the quote has a map entry | **9** | `<id> unmapped` | after 7; repair = add the entry (caller gap) | must not collapse into 8: an incomplete map is not a bad citation |
| 8 | every containing artifact is mapped, none to a cited URL | **8** | `<id> url-mismatch` | after 7; repair = fix the capture or the row's citation | — |
| 9 | row's cell 1 carries no http(s) URL, while a map is supplied | **8** | `<id> cites-no-url` (:419) | folded into 8; repair = cite a URL or run without the map | must **not** become 4: `row_defects` never required a URL, and **6 live registry rows** cite lane-local paths (S024, S025, S036, S037, S047, S056), so 4 would retroactively invalidate them |
| 10 | both 8 and 9 present across rows | **8** | both rows named | deterministic: mismatch outranks unmapped | — |

Two qualifiers the SCORECARD must carry if it cites these codes: **8 covers two reasons** (`url-mismatch`,
`cites-no-url`), so "exit 8 = a capture of a different document" is an overstatement; and **9 is only reachable
when *no* containing artifact is mapped** (existential rule), so 9 is not "some artifact unmapped".

## 5. Evidence matrix (body `90603c3f`; the same ten exits were measured on `50793383`)

Ten direct `quote_check` cases on one S092-shaped fixture row (synthetic sentence), plus three registry facts:

| # | case | exit | verdict |
|---|---|---|---|
| 1 | repo-root map, the real capture | 0 | accepted |
| 2 | map = the URL actually fetched (pinned raw file) | **8** | **refused — the inversion** |
| 3 | repo-root map, a **different file** of the same repo | 0 | **accepted — the gap, at repo granularity** |
| 4 | repo-root map, a **whole-repo dump** (many files concatenated) | 0 | **accepted — `grep`-the-repo passes** |
| 5 | dir: real capture mapped elsewhere, an uncited `b-readme.md` mapped to the root | 0 | **accepted, and the binder is the README; the receipt prints `at a-real-config.py`** |
| 6 | dir: decoy unmapped, real capture mapped to the cited root | 0 | accepted (the intended existential fix) |
| 7 | dir: every containing artifact mapped elsewhere | **8** | refused |
| 8 | row cites no URL, artifact mapped | **8** | refused, reason `cites-no-url` |
| 9 | empty map `{}` | **9** | refused |
| 10 | no map at all | 0 | accepted (unchanged default) |

Registry facts (`corpus/SOURCES.md`, 88 rows, body `90603c3f`): **12** rows carry an ASCII-quoted anchor span (only those can ever
reach the binding); **6** carry no http(s) URL (rows 9 above); **2** cite two URLs (S041, S045 — membership over
the set is required); **0** have a URL with a non-alphanumeric tail (so the trim-set defect is latent);
**0** carry `\|`. Staged package: 173 rows, **S093 refused `escaped-pipe`**, **S100 refused `no-quote`**.

## 6. What a wrong or lazy map still passes — residual limits

- **R1 — granularity.** A repo-root (or directory) citation binds at repository granularity: any file, at any
  revision, that contains the sentence passes (cases 3, 4). The anchor's `commit <sha>` and file path are never
  bound, because they live in prose, not in the URL.
- **R2 — attestation, not verification.** The map is a caller declaration. Nothing ties it to the bytes; a
  deliberate false declaration passes. The gate converts an unverified silence into a *reviewable claim*, and no
  more. (Case 2 shows it also refuses the one claim that would have been stronger.)
- **R3 — content-blind keys.** A name-keyed map is reusable: `{"capture.txt": "<cited root>"}` authored for one
  fetch applies to any later `capture.txt`. Optional per-entry `sha256` is the obvious follow-on; it changes the
  map shape and the selftest surface, so it is out of scope for this claim and must be disclosed instead.
- **R4 — existential binder.** The artifact that satisfies the binding need not be the artifact the receipt names,
  nor the file the anchor names (case 5). Today this is invisible; §9 C4 makes it visible.
- **R5 — coarsest cited URL wins.** For a row citing several URLs, the coarsest one suffices (S041, S045).
- **R6 — anchor facts unbound.** The pinned commit, the file path, the line/field, and the fragment are all
  unverified by the URL check; dropping the fragment (§3) makes the line claim unbound by construction.
- **R7 — assertion vs quotation.** Byte containment cannot distinguish a sentence a document asserts from one it
  attributes to a critic. Unchanged from round 30.
- **R8 — reach.** The binding only runs for rows whose anchor carries an ASCII-quoted span: 12/88 live registry
  rows, 1/3 of C1's staged rows. A row quoting in the lane's own CJK convention (`「…」`, staged S100) is refused
  **4 `no-quote`**, and a row with an escaped pipe (staged S093) is refused **4 `escaped-pipe`** — the gate cannot
  even reach those rows' quotes, so the binding's coverage is bounded by the span extractor, not by the map.

## 7. Where this design is weak — the case against it

1. **The unbound case is now signalled by a missing field, not a present one.** Body `90603c3f` drops the binding
   fields entirely when no map is supplied, to keep round 30's `QUOTE …` prefix byte-stable (the comment at :551
   records a regression seat measuring the prefix break). The trade is real and it cuts against the gate: a round
   that greps `QUOTE rows=… located=1` cannot tell a bound receipt from an unbound one, and the *absence* of
   `mismatch=`/`unmapped=` is exactly what a reader will interpret as "no mismatches" rather than "not checked".
   The prefix constraint is legitimate; the remedy is that the contract must state "a receipt without `urlmap=`
   is unbound, never a binding pass", and the round's evidence must be the bound receipt. If the lane cannot
   guarantee that reading, an explicit `urlmap=none` is worth the prefix change — a receipt whose meaning depends
   on a field nobody prints is how the round-30 gap gets re-opened by paperwork.
2. **The inversion (case 2) is documented, not fixed.** Rewording the help text converts a trap into a rule, but
   the rule is "declare the coarser claim", which is a strange thing for a verification gate to teach. The
   alternative — alias + containment (§3, rejected) — is genuinely worse for this round, so the honest resolution
   is to state in the SCORECARD that the binding is *citation membership at the granularity the row cites*, and
   that a row citing a repo root cannot be bound below the repo.
3. **The existential rule widens "the row's document" to "any capture in the set"** (case 5). It is the right
   tradeoff against universal binding (per-round capture directories), but it means the gate's green says
   "somewhere in this directory there is a capture of a cited document containing the sentence", not "the row's
   quote was read in the document the row names". Printed without the binder, that difference is invisible.
4. **Two functions compute the same predicate.** `locates` (:400) is `next(iter(locating_artifacts(...)))`
   (:389) — one authority duplicated, and the duplicate is the one printed in the receipt while the other is the
   one that decides. Collapse to one and let the binder name come back from `bind_failure`.
5. **The map's identity is not in the receipt.** `urlmap=entries=N` cannot be tied to a file; two different maps
   of the same size produce identical receipts. For a claim whose entire value is "the caller declared X", the
   declaration must be nameable.

## 8. Adjacent defects that bound C3's claim (not C3's to fix, but C3's to disclose)

- **Staged S093 is refused `escaped-pipe` by the gate** (`fail_to_pass \| pass_to_pass`). The gate is *right*:
  the live registry has 0 escaped pipes, so the convention is "no `\|` inside a cell", and the staged row is the
  defect. Impacted: **C1** — one of three admitted rows cannot be parsed by the round's own instrument until the
  row is rewritten. Same for staged S101.
- **Staged S100 is refused `no-quote`** because its anchor quotes in `「…」`. Here the gate is wrong about the
  lane's convention (S091/S095/S096/S099 in the staged package use the same brackets), so CJK rows are
  structurally refused rather than merely cap-inert (round 30 disclosed only the cap). Impacted: **C1** (the
  quote check cannot validate S100) and **C3's R8**.
- **`--selftest` printed an argparse usage error on stderr** on `50793383` (the guard case calls `main` and lets
  `parser.error` write to stderr). Fixed on `90603c3f` — stderr is clean and the tally is unchanged. Kept in the
  record because a green tally that emits an error line is the shape of a predicate that has stopped measuring
  what it claims (see the next bullet).
- **The frozen predicate cannot see an unreachable CLI** (§0). Impacted: **C3** directly — `cases=17` was green
  on a body whose quote mode exited 2 for every invocation.

## 9. Smallest safe corrections, in order (all inside the frozen predicate)

- **C1 — kill the provenance wording that survives at :341** ("naming the document each artifact was fetched
  from"). The help text (:969) already says membership; make the comment agree. One line, no behaviour change.
- **C2 — pin the C1-shaped case inside case 15/16** (the tally must stay `cases=17`): a row citing a repo root,
  the capture mapped to that root → accepted; the same capture mapped to the pinned raw file URL → 8 with
  `url-mismatch`. This turns the inversion into a documented, tested rule instead of a surprise for the first
  operator who maps provenance.
- **C3 — put the map's identity in the receipt**: `urlmap=<basename> entries=N` (or a short digest) instead of
  `entries=N` (:556), and require the round's evidence file to be the *bound* receipt, since an unbound one now
  carries no binding field at all. Then a round's evidence file names the declaration it is citing.
- **C4 — return the binder**: `bind_failure` returns `""` today; return `(refusal, binder, binder_url)` so the
  `ok` line can print `bound=<artifact>-><url>` and the receipt can count the other locators (`extra=N`). This is
  the one correction that makes the existential rule auditable (case 5).
- **C5 — collapse `locates` into `locating_artifacts`** (:389-410) so the printed locator and the deciding
  locator cannot diverge by construction.
- **C6 — one assertion that the CLI is reachable**, inside case 17: `main(["--quote-file",…, "--artifact",…,
  "--url-map",…])` returns 0. This is what `cases=17` lacked when quote mode was dead.
- **C7 — disclose R1-R8 in the SCORECARD row**, in round 30's own style: the gate proves *the capture the caller
  declares answers a URL the row cites, at the granularity the row cites*; it does not verify a fetch, does not
  bind the pinned commit, path, line or fragment, and its reach is rows with an ASCII-quoted anchor span.

Rejected for this round, with reasons: blob↔raw aliasing, prefix containment, row-id keying, mandatory map,
`sha256`-pinned entries. Each is defensible later; each widens the surface the claim has to defend now.

## 10. Verification Main should run

```
python3 plans/sources_adopt.py --selftest                       # expect SELFTEST cases=17 failed=0, exit 0, no stderr
python3 plans/sources_adopt.py --quote-file X --artifact Y      # expect NO urlmap field (unbound), exit 0
python3 plans/sources_adopt.py --quote-file X --artifact Y --url-map M   # expect urlmap=entries=N present, exit 0/8/9 as the map dictates
python3 plans/sources_adopt.py --registry corpus/SOURCES.md --package P --url-map M   # expect exit 2
git show 0883e72:plans/sources_adopt.py … --url-map M           # control: exit 2, cases=14 (verified: 2 and 14)
```

Control verified this seat on the baseline body: `--selftest` → `SELFTEST cases=14 failed=0`; the same invocation
with `--url-map` → `error: unrecognized arguments: --url-map`, exit **2**.

---

VERDICT: ACCEPT WITH CORRECTIONS — the map keyed by artifact name, compared as set membership against the row's cited URLs under the narrow normalisation of §3, is the smallest contract this gate can *truthfully* implement; it must not be extended with blob↔raw aliasing, prefix containment or row-id keying, its provenance wording must be removed (:341) and its receipt must name the map and the binding artifact (C3/C4), and the SCORECARD must state that the binding is citation membership at the row's own citation granularity — repo-level for all three C1 rows — because a wrong or lazy map still passes R1-R8 and the frozen predicate `cases=17` cannot see any of it.
