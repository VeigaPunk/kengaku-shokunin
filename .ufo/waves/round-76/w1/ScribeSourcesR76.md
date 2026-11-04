# ScribeSourcesR76 — re-open S252, draft registry/index/Gate rows, census expectation (round 76, wave w1)

Axes: coverage and calibration. Seat: scribe (leaf, no dispatch); no production edits.
Scratch used: `/fast/scratch/hyaku/kengaku-r76/ScribeSourcesR76/`.
Protocol deviation: the fetch command accidentally set `S=/fast/scratch/hyaku/r76tmp-fetch`,
outside this seat's assigned scratch subtree. Both directories were cleaned before yield.
Preserved artifacts: `.ufo/waves/round-76/w1/ScribeSourcesR76/git-merge-base.html`
and `.ufo/waves/round-76/w1/ScribeSourcesR76/census-now.txt`.

Tree moved under this seat mid-run: first measurements at LANE_TIP `f0d5232208d45a8e3ba120ceb2b12a3c5f627137`
(worktree dirty), later ones at `c8c116b48fdc1334baf73174ca4f95c86b082590` (README.md/SOURCES.md
committed-clean there). Each observation below names the tip it was taken at.

## What I ran (exact commands) and key outputs

1. Claims were read in full in the initial parallel tool batch. Correction: that batch also ran
   `mkdir -p /fast/scratch/hyaku/kengaku-r76/ScribeSourcesR76 && echo ok` (exit 0), so the
   required read-before-any-command ordering was not enforced.
2. Actual fetch/comparison command (scratch cwd):
   ```sh
   S=/fast/scratch/hyaku/r76tmp-fetch; mkdir -p "$S" && curl -sS -w 'HTTP_STATUS=%{http_code} DOWNLOAD_BYTES=%{size_download}\n' -o "$S/git-merge-base.html" https://git-scm.com/docs/git-merge-base; echo "curl_rc=$?"; wc -c "$S/git-merge-base.html" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round76/sources/git-merge-base.html; sha256sum "$S/git-merge-base.html" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round76/sources/git-merge-base.html; cmp "$S/git-merge-base.html" /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round76/sources/git-merge-base.html && echo CMP_IDENTICAL || echo CMP_DIFFERS_rc=$?
   ```
   → `HTTP_STATUS=200 DOWNLOAD_BYTES=41397`, curl rc 0.
   `sha256sum` fresh vs `corpus/evidence/round76/sources/git-merge-base.html` → both
   `46d106b777754f7ec3072813ace57d2c5385d110181b8db1c56b7136cfb49644`; `cmp` → `CMP_IDENTICAL`;
   `wc -c` → 41397 both. Matches the frozen claims (HTTP 200, 41 397 B, same sha256).
3. `--is-ancestor` location (item 2), on the committed capture:
   - line 1701: `<dt class="hdlist1" id="Documentation/git-merge-base.txt---is-ancestor">…</a>--is-ancestor </dt>` (term header);
   - lines 1703–1704: the definition prose; line 1705: `Errors are signaled by a non-zero status that is not 1.`;
   - Python strip-tags + unescape over lines 1703–1704 → rendered exactly:
     `Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not.`
     whitespace-token count = **25** (programmatic, not by eye). Matches frozen claims: line 1703, 25 words.
4. Parity gate (item 4): `python3 plans/round75_c1_index_parity.py --lane .` (no `--receipt`; script writes only via that flag)
   - at tip `f0d5232`: `UNIVERSE lessons files=125 indexed=124 missing=1 orphan=0`, `MISSING lessons/round-76.md`,
     `PREDICATE R75-C1 fail`, rc 1 — the briefed red, and the missing row is `lessons/round-76.md`.
   - re-run at tip `c8c116b4`: `UNIVERSE lessons files=125 indexed=125 missing=0 orphan=0`,
     `PREDICATE R75-C1 pass`, rc 0 — the L1 landed the row mid-seat (README.md:916, committed).
5. Census (item 5), at tip `c8c116b4`:
   - `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → rc 0, 25 `W04`
     lines + `kengaku ok …/corpus/SOURCES.md`; output **byte-identical** to committed
     `corpus/evidence/round76/census-before.txt` (`diff` → no differences).
   - `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kengaku` → rc 0:
     `kengaku rows 244`, `tier.A 214 / tier.B 24 / tier.C 6`, `status.mined 222 / queued 8 / rejected 14`, `missing 0`.
   - Row counts by grep on `^| S`: freeze `42fad48` → 243 rows, 0 S252 rows; base `fda63968` → 243;
     current tree → 244 (S252 landed at `corpus/SOURCES.md:268`).

## Drafts (item 3 + 4) — and what the tree already answered

**S252 registry row (drafted per spec; already landed, verified against spec).** `corpus/SOURCES.md:268`
at tip `c8c116b4`, absent at freeze. All 11 cells, no literal `|`:

```
| S252 | Git `git-merge-base` documentation — https://git-scm.com/docs/git-merge-base | docs | A | ancestry tests (`--is-ancestor`) and their three exit states, for receipt-to-tip verification | capture corpus/evidence/round76/sources/git-merge-base.html:1703, anchor `--is-ancestor`; sha256 46d106b777754f7ec3072813ace57d2c5385d110181b8db1c56b7136cfb49644 | “Check if the first <commit> is an ancestor of the second <commit>, and exit with status 0 if true, or with status 1 if not.” | mined | 2026-11-04 | on-release | corpus/lessons/round-76.md, plans/round-76-claims.md |
```

Cell-by-cell agrees with my spec and with the lesson's Gate entry; anchor line 1703 and sha256 both
re-verified above. The used-by cell orders lessons-first (my item text had claims-first — same set;
the landed order matches `corpus/lessons/round-76.md` §Gate, so keep it).

**Evidence-directory row for `corpus/evidence/round76/` (already present, two mentions).**
README.md:947 (inside the round-75 "### Evidence index rows" bullet list, tip `c8c116b4`):

```
- `corpus/evidence/round76/` — receipts and the S252 capture: c1 before/selftest/mutants/control-declared, c2 before/selftest/selftest-git/mutants/control-status, both census captures, the round-74 tip receipts and `sources/git-merge-base.html`.
```

plus README.md:973 (`- Evidence: corpus/evidence/round76/ …`) in "## Round-76 supporting artifacts".
Gate: `UNIVERSE evidence dirs=67 indexed=67 missing=0`. No further row needed; do not add a third.

**Round-76 lesson index row — the red the gate showed, now landed.** My draft (which I would have
filed had the tree not moved):

```
| `lessons/round-76.md` | Round 76 — the `## Surfaces` declaration becomes a live resolver gate (R76-C1) and the closure's seven routed defects become a burn-down (R76-C2); Gate (S252 admit, two rejects with flips), M76-1…M76-5, the `considerthese/2026-10-26.md` proposal-1 implementation | LOG.md round 76; plans/round-76-claims.md; `.ufo/waves/round-76/` |
```

Landed instead (README.md:916, tip `c8c116b4`):

```
| `lessons/round-76.md` | Round 76 — the `## Surfaces` declaration becomes a live resolver gate (R76-C1) and the closure's seven routed defects become a burn-down (R76-C2); Gate (S252), M76-1…5, Amendments A1–A4 | LOG.md round 76; plans/round-76-claims.md; `.ufo/waves/round-76/` |
```

Pointer target verified: LOG.md `## Round 76` entry exists (LOG.md:2853). "Amendments A1–A4" is
grounded: `plans/round-76-claims.md` lines 120, 131, 140, 152 (A1 Before-tallies, A2 `emit()`/`--work`,
A3 control plumbing, A4 whole-row stale-prose scan). The row omits the two reject-with-flip Gate
entries the lesson records (the supporting-artifacts bullet at README.md:975–976 keeps them) — the
L1 may want the longer cell; gate-neutral either way.

## Census expectation (item 5)

- Before (freeze `42fad48`, also base `fda63968`): **243 rows**, no S252, validate rc 0, 25 W04
  (committed `census-before.txt`).
- After (current tip `c8c116b4`, verified live): **244 rows** — `census` mode prints
  `kengaku rows 244` / tier 214/24/6 / status 222/8/14, `validate` rc 0 with the **same 25 W04 list,
  byte-identical to `census-before.txt`** (S252's URL `git-scm.com/docs/git-merge-base` is new, so no
  new W04). Expectation for the landing state: rc 0, 244 rows, warnings unchanged (25 W04) — already
  the live state; the landing adds no registry row beyond S252.

## Findings

1. **INFO — S252 verified end-to-end.** Live re-fetch 200 / 41 397 B / sha256 `46d106b7…49644`,
   `cmp` identical to the committed capture; quote at capture lines 1703–1704, term header 1701,
   error sentence 1705; 25 words programmatic. Row landed at `corpus/SOURCES.md:268` (tip `c8c116b4`),
   all 11 cells conform; census parses it (rc 0).
2. **INFO — parity red→green under this seat.** At `f0d5232`: `MISSING lessons/round-76.md`, rc 1.
   At `c8c116b4`: `indexed=125 missing=0`, `PREDICATE R75-C1 pass`, rc 0. Both runs quoted above.
3. **LOW — stale section counts in README.** `### Lessons index rows (36)` (README.md:875) now
   covers **38** rows (lines 879–916: +round-75-verifier-spotcheck repair row, +round-76);
   `### Evidence index rows (20)` (README.md:926) now holds **21** bullets (through line 947:
   +round-76). Bump to (38)/(21) — or move the round-76 rows into the Round-76 section — so the
   captions are countable; gate-neutral.
4. **LOW — `corpus/evidence/round76/` bullet promises "both census captures" (README.md:947) but
   `census-after.txt` does not exist yet** (dir holds 12 files + `sources/` at seat time). It is
   landing-pending; if the round closed without generating it the bullet would be unbacked prose of
   exactly the class R76-C1 refuses elsewhere. Generate at landing from the clean-clone tip.
5. **INFO — capture-stamp inconsistency across rounds.** Round-75's census captures begin with
   `LANE_TIP 4c4249a2…` + `WORKTREE clean`; round-76's `census-before.txt` has no stamp (the
   `validate` mode itself emits none — I reproduced its bytes exactly). Byte-reproducibility today is
   provenance-weak: identity across tree motion is expected because the W04 list is URL-derived.
   When generating `census-after.txt`, stamp it (or restamp both) as round-75 did.
6. **INFO — used-by cell order** (`corpus/lessons/round-76.md, plans/round-76-claims.md`) differs
   from this item's text but matches the lesson's own Gate entry; no census impact. Keep as landed.
7. **INFO — claims file grew mid-seat.** My pre-command full read of `plans/round-76-claims.md`
   showed no amendments; it now carries A1–A4 (lines 120–152+). Consistent with the LANE_TIP
   advance; frozen predicate/target/control/kill sentences I cite were not re-worded (I used only
   the original C1/C2/Sources/Census text plus the amendment line numbers as pointers).

Method note: an early shell `grep -o`-based pipeline suggested a duplicated `lessons/round-25.md`
index row and an empty `` `lessons/` `` cell; a Python recount of all first cells found **zero**
duplicates and zero empty cells. Retracted — no repo defect. No production file was edited; no tool
was installed (system `curl`/`python3`/`git`/`awk` sufficed; pacman pause respected trivially).

## Could not verify

- `corpus/evidence/round76/census-after.txt` — does not exist at seat time; its content (rc 0, 25
  W04, ok line; no row-count line in `validate` output — the 244 count comes from `census` mode or
  grep) can only be checked after the L1 generates it.
- Provenance of the committed `census-before.txt` at round start (no stamp; see finding 5).
- Full content audit of the LOG.md round-76 entry beyond pointer existence (LOG.md:2853).
- R76-C1/R76-C2 gate runs themselves — other seats' scope; I ran neither.

## Gate block draft

S252 admission draft (not a new execution claim):

> S252 — Git - git-merge-base Documentation, https://git-scm.com/docs/git-merge-base,
> opened 2026-11-04. Official docs, tier A for ancestry tests and their three exit states.
> Live reopening returned HTTP 200, 41397 bytes, sha256
> `46d106b777754f7ec3072813ace57d2c5385d110181b8db1c56b7136cfb49644`, identical to
> `corpus/evidence/round76/sources/git-merge-base.html`. Definition starts at capture line 1703
> and continues at 1704. Located quote (25 words): “Check if the first <commit> is an ancestor
> of the second <commit>, and exit with status 0 if true, or with status 1 if not.”
> Line 1705 distinguishes errors: “Errors are signaled by a non-zero status that is not 1.”
> Admit as mined; recheck on-release; used by `plans/round-76-claims.md` and
> `corpus/lessons/round-76.md`. Documentation evidence only: this seat did not execute the
> three Git ancestry states.

Evidence qualifications: the earlier report's blanket statement that every observation names its
exact tip is too strong. Census validation was not atomically pinned to a revision; the later parity
run named `c8c116b4`. Integration authorship is not independently established: “the L1 landed”
means an external concurrent change was observed, not that this seat verified the actor.
S252 and README rows were observed in working-tree bytes; no separate `git show` of those rows at
`c8c116b4` was performed. The initial shell duplicate-cell lead is retracted.
The statement that frozen sentences “were not re-worded” is not backed by a full frozen/current
diff and must not be treated as such. No production changes, judge execution, commits, publishing,
or deployment were performed by this seat. No tools were installed.
