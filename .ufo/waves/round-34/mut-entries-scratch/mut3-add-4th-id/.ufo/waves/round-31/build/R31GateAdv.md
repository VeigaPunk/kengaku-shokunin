# R31GateAdv — attack on the `--url-map` citation binding

Lane: kengaku-shokunin, round 31 (hyaku run 6), claim C3 (operability: bind the adoption gate's
capture to the row's cited URL). Seat: adversarial pre-landing attack on
`plans/sources_adopt.py`.

## What was attacked

Not a plan: the in-flight bytes. The lane file carried an uncommitted `+129/−5` working-tree
diff (the binding), so I took a byte snapshot and attacked that.

| artifact | sha256 | lines |
|---|---|---|
| lane `plans/sources_adopt.py` at attack time | `71a90ec072e3b5e3fefcc127ea3dd0cf57d234950e9b14422a1ddb0e1abd60d5` | 997 |
| `/tmp/r31-GateAdv/pristine.py` (the attacked copy, byte-identical to the lane file) | `71a90ec072e3b5e3fefcc127ea3dd0cf57d234950e9b14422a1ddb0e1abd60d5` | 997 |
| lane `plans/sources_adopt.py` at report time | `71a90ec072e3b5e3fefcc127ea3dd0cf57d234950e9b14422a1ddb0e1abd60d5` | 997 |
| `/tmp/r31-GateAdv/fix.py` (proposed 5-hunk patch, not applied to the lane) | `50c670f41fb8ff2814ec1a36c5c579714d14b865e066cb17c23968ac74c3486d` | 997 |

The binding as written (`pristine.py:344–415`, wired at `pristine.py:495`, precedence at
`pristine.py:528–531`) is: `mapped = url_map.get(artifact_name)` (`:406`) → `unmapped` if absent
(exit 9); `cited = cited_urls(row.cell(SOURCE_COLUMN))` (`:409`) → `cites-no-url` (exit 8) if the
row cites nothing; accept iff `normalize_url(mapped)` is in `{normalize_url(url) for url in cited}`.
`normalize_url` (`:349`) drops the fragment, lowercases scheme+host only, keeps path case, keeps the
subpath boundary, keeps the scheme distinct, and `rstrip("/")`s.

Lane `--selftest` at attack time: `SELFTEST cases=17 failed=0` (run against the lane file, read-only).

## Case table — the six mandated probes

`accept` = exit 0; `refuse` = exit 8 (mismatch) or 9 (unmapped). "Right?" compares the binding's
answer to the verdict the invariant needs.

| # | probe | binding's answer | right verdict | right? |
|---|---|---|---|---|
| 1 | artifact mapped to the cited URL + trailing slash (`…/spec.html/` vs `…/spec.html`), both directions | **accept** (0) | accept — formatting only; the registry's cited URLs are article paths, and the `rstrip("/")` at `:363` makes `…/spec.html/` and `…/spec.html` one key | yes |
| 2 | `http://` map value vs `https://` cited (both directions) | **refuse** (8) | refuse — a capture's provenance is the URL it was fetched from; the gate cannot prove the two origins serve the same bytes, and a looser rule (mutant N1) silently greens a different origin | yes (fail-closed; see U2) |
| 3 | map value is a prefix of the cited URL (`…/docs` vs `…/docs/spec.html`), reverse, and a string-prefix sibling (`…/spec.html.bak`) | **refuse** (8) for all three | refuse — a subpath is a different document; the `startswith` shortcut (mutant N2) accepts all three plus a query-string difference | yes |
| 4 | map value is a URL that 301s to the cited page; capture holds the target's bytes | **refuse** (8) | refuse is the only statically defensible verdict: the equivalence is a network fact, and the gate is offline by design. Repair is operator-side (record the resolved URL in the map, or cite the canonical). | yes, as a refusal — unsettleable as a semantic judgment (U1) |
| 5 | map keyed on a filename that also occurs in a directory artifact: `artifact-dir/{sub,other}/a.txt`, key `a.txt` | **refuse** (9 unmapped) | refuse — the receipt prints `sub/a.txt`, and a basename fallback (mutant N3) binds *both* files to one URL and accepts. `5b` (key `sub/a.txt`) accepts, `5c` (same file passed directly, receipt name `a.txt`, key `sub/a.txt`) refuses 9 — both right. | yes |
| 6 | row's `source` cell carries two URLs; capture is the second / the first / neither | **accept** (0) / **accept** (0) / **refuse** (8) | accept / accept / refuse — a two-document citation is satisfied by a capture of either. First-URL-only (mutant N4) refuses the second, i.e. a right map is refused. | yes |

## Extras (cheap probes, run in the same harness)

| # | probe | binding's answer | right verdict | right? |
|---|---|---|---|---|
| 7 | quote occurs in **two** captures (`alpha/cap.txt` bound elsewhere, `beta/cap.txt` bound to the cited URL) | **refuse** (8 mismatch) | accept — a capture of the cited document does contain the quote; the row's repair list would otherwise say "wrong document" when the right one is present | **NO — finding F1** |
| 8 | `source` cell carries no URL | **refuse** (8, `cites-no-url`) | refuse — otherwise dropping the URL is an escape hatch (mutant N5) | yes |
| 9a/9b | host case only (`EXAMPLE.com`) / path case only (`/Docs/Spec.html`) | accept / **refuse** (8) | accept / refuse — host is case-insensitive, GitHub-style paths are not (mutant N7 accepts the path case) | yes |
| 10 | map value carries `?utm_source=feed` | **refuse** (8) | refuse — a query string may select a different page (`?page=2`); tracking junk must be stripped at capture time, not guessed here (U3) | yes |
| 11 | `source` cell wraps the URL in angle brackets (`<https://…/spec.html>`) | **refuse** (8) | accept — `cited_urls` (`:344`) trims `.,;:)]}` but not `>`, so a formatting-only autolink becomes a mismatch | **NO — finding F2** |
| 12 | `source` cell is a markdown link `[spec](url)` | accept (0) | accept — the trailing `)` is already trimmed | yes |
| 13 | map value is not a URL at all (`"capture of spec.html"`) | **refuse** (8) | refuse — fail-closed on a map the gate cannot interpret | yes |

Totals: pristine **21/23** probes right; `fix.py` **23/23**.

## Findings (both are over-refusals, not wrong-map survivals)

- **F1 — the binding commits to the first locating artifact.** `locates` (`:387`) returns the first
  name in load order, and `:495` binds only that one. When a quote is present in two captures, a
  wrong-document capture sorted first refuses a row whose cited capture is also present. Blast
  radius: any run whose artifact directory holds a vendored copy, a README quote, or the same
  sentence in two pages — the gate reports `mismatch=1` for a correct citation.
- **F2 — `>` is not trimmed from cited URLs.** `cited_urls` (`:344`) strips `.,;:)]}` only. An
  autolink (`<URL>`) is a formatting difference of exactly the class case 1 accepts, yet it refuses.
  Low frequency in the live registry (which writes `title — URL`), but it is a false refusal that
  the operator cannot distinguish from a real mismatch.

No *wrong* map survived any of the six mandated probes on the in-flight bytes: the narrow
`normalize_url` is what buys that, and every loosening I tried lost it (table below).

## Proposed rule

Normalization (single `normalize_url`, applied to both sides):

1. strip whitespace and surrounding decoration — `<>`, `()`, `[]`, and the trailing `.,;:)]}>`;
2. drop the fragment (`#…`);
3. lowercase the scheme and the host **only** — never the path, never the query;
4. drop a default port (`:80` on http, `:443` on https) and nothing else;
5. collapse a trailing `/` on a non-empty path (`/a/` ≡ `/a`; `/` stays `/`);
6. keep the scheme significant (`http` ≠ `https`), keep every path segment (no prefix, no
   subpath), keep the query significant.

Binding (the pair rule):

> A row is bound when **any** artifact whose normalized text contains the quote is mapped to **any**
> URL the row's `source` cell cites. Exit 9 only when none of those artifacts has a map entry; exit
> 8 when they all have entries and none matches, or when the row cites no URL at all.

That is `fix.py`, five hunks on the in-flight bytes:

- `:344` `rstrip(".,;:)]}>")` (F2);
- new `locating()` next to `locates()` (`:387`) returning every containing artifact;
- `bind_failure` takes `artifact_names: list[str]` and tests `any(normalize_url(v) in wanted)`
  over all mapped names (F1);
- call site `:495` passes `locating(quote, loaded)`;
- no signature or exit-code change anywhere else.

Verified: `fix.py --selftest` → `SELFTEST cases=17 failed=0`; `attack.py fix.py` → `ATTACK
cases=23 diff=0`. Patch was **not** applied to the lane file.

## Mutants (does the rule bite?)

Ten single-point mutants of `fix.py`, each a plausible cheaper implementation, run through the same
23-case detector. All killed:

| mutant | change | killed by | verdict |
|---|---|---|---|
| N1 `a7207514cf89` | scheme dropped from the comparison key | 2a, 2b | KILLED |
| N2 `8ec780d767d7` | prefix/`startswith` comparison | 3a, 3b, 3c, 10 | KILLED |
| N3 `f49a811a7be6` | basename fallback for map lookup | 5a | KILLED |
| N4 `67029e0cf045` | first cited URL only | 6a | KILLED |
| N5 `d8fc95a75712` | a row citing no URL is accepted | 8 | KILLED |
| N6 `c8fd6f6bab07` | trailing slash significant | 1a, 1b | KILLED |
| N7 `e8c532536e58` | whole URL lowercased (path too) | 9b | KILLED |
| N8 `47529fbcac95` | bind only the first locating artifact (the in-flight behaviour) | 7 | KILLED |
| N9 `7456f8c7bbde` | `>` not trimmed (the in-flight `cited_urls`) | 11 | KILLED |
| N10 `8ac9ea977de9` | unmapped artifact accepted | 5a, 5c | KILLED |

The same seven mutants built on the in-flight bytes (M1 `b3364f284d98` scheme-blind, M2
`79bd7a9aa1bc` prefix, M3 `41aa46328480` basename, M4 `3ed09a3d3451` first-URL, M5 `ecce416e8ed1`
no-URL-accepted, M6 `31c31ee153e5` slash-significant, M7 `cbf48c236a6c` lowercase-all) are likewise
killed by the same detector — so the probes discriminate on the code that is about to land, not only
on the patch.

## No static check can settle these

- **U1 redirects.** Whether `…/old/page` resolves to `…/new/page` needs a fetch and a redirect
  chain; a static gate must refuse, and the repair is to record the URL after redirects in
  `--url-map` (or cite it). A redirect-following mode would turn the gate into a network client
  with an unpinnable result.
- **U2 `http` vs `https` equivalence.** Same class: whether the two origins serve identical bytes
  is a network fact. Refusal is correct by contract, but it is a false positive generator for hosts
  that force https — the operator fixes it in the map, not in `normalize_url`.
- **U3 query strings.** `?utm_source=…` may be tracking junk or may select content; no static rule
  distinguishes them. Keeping them significant (case 10) is fail-closed; strip at capture time.
- **U4 host aliasing** — `www.` vs bare, `example.com` vs `example.com:443`, CNAMEs. Resolvable only
  by DNS/HTTP.
- **U5 percent-encoding** — `%7E` vs `~`, `%2F` vs `/`, `%20` vs `+`: whether the origin decodes to
  the same resource is server-dependent. Left significant.
- **U6 trailing slash, strictly** — a static server may serve a directory listing at `/a` and an
  index at `/a/`. Case 1 is accepted on convention (the registry cites article paths), not on proof;
  that is a documented bet, not a fact the gate establishes.

Also outside the binding's reach by construction: that the capture's *bytes* came from the pinned
commit (`6099b8cf…` for Harbor, `66f9276…` for SWE-bench_Pro-os, `2fd12b8…` for terminal-bench-2).
The map records which document was fetched, never which revision; a commit-pin check is a separate
capability.

## Restoration evidence

- The lane file was never written: the only operations against it were `read`, `cp` (out),
  `grep`, read-only `git status/diff/log`, and `python3 plans/sources_adopt.py --selftest`.
- `sha256(plans/sources_adopt.py)` before the attack run and after the mutant sweep:
  `71a90ec0…bd26b2` both times, 997 lines both times — no drift, nothing to restore.
- Every mutant and probe lives under `/tmp/r31-GateAdv/` (17 mutant files + `attack.py` +
  `pristine.py` + `fix.py`, < 1 MB total); nothing under `/home/vgpnk/Projects/shokuknow` was
  touched and no network fetch was made.
- Tool installs: none (python3 stdlib only). No pacman transaction was attempted.

Reproduce:

```
cd /tmp/r31-GateAdv
python3 attack.py pristine.py     # 23 cases, 2 diff (cases 7, 11)
python3 attack.py fix.py          # 23 cases, 0 diff
python3 fix.py --selftest         # SELFTEST cases=17 failed=0
python3 attack.py N8-first-artifact-only.py   # KILLED by case 7
```

VERDICT: **The in-flight binding is sound on all six mandated probes — no wrong map survives
trailing slash, scheme, subpath, redirect, basename-collision or two-URL input — but it is too
strict in two places (F1 first-locating-artifact-only, F2 untrimmed `>`), so correct maps are
refused; land it with the five-hunk `fix.py` pair rule (any containing artifact × any cited URL,
`>` added to the trim set), which scores 23/23 and keeps all ten loosening mutants killed.**
