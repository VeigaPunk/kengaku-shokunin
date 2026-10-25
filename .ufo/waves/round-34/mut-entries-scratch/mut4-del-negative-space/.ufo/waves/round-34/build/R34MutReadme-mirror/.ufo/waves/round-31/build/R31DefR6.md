# R31DefR6 — re-derivation of the staged-source count (defect R6)

Reviewer: `L1Kengaku31.R31DefR6` (leaf; no dispatch). Access date 2026-10-25. Lane tip `0883e72`.
No production edits: the only file written under the lane is this report. Scratch in `/tmp/r31-R6/`
(one 47 KB HTML capture, no clones). No tool installs or upgrades were needed.

The entry under review is `corpus/knowledge/contamination-transparency-card.md`. It was
worktree-modified (`M`) and **being edited while I reviewed it**: it was 193 lines at my first read
and 196 lines at my last, so every location below is given by quoted text, with the line numbers I
observed at the stated state.

## (a) The three source URLs

Staged file `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-card-field-schema-2026-10-23.md`,
sha256 `66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9` (identical to the hash the
entry cites at its :38), `source:` lines 2–4:

| staged id | line | URL |
|---|---|---|
| S122 | 2 | `https://the-ai-alliance.github.io/trust-safety-evals/evaluations/benchmark-card-template/` |
| S123 | 3 | `https://github.com/Jangulo7/contamination-disclosure-paper/blob/4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6/templates/disclosure.yaml` |
| S124 | 4 | `https://aclanthology.org/2026.gem-main.50.pdf` |

Three `source:` lines, no more (the regex the counter uses returns exactly 3).

## (b) The one source with a registry row: S124, under id **S001**

`corpus/SOURCES.md:23` (tier cell `A`, status `mined`, opened `2026-10-19`):

> `| S001 | Are LLM Benchmarks Already Contaminated? A Systematic Review of Contamination Detection Methods — https://aclanthology.org/2026.gem-main.50/ | paper | A | … | Abstract, GEM 2026 (July 2026), pp.518-539, Outstanding Paper | … | mined | 2026-10-19 | 2027-01-17 | corpus/knowledge/contamination-detection-and-transparency.md |`

The registry cites the **landing page** `…/2026.gem-main.50/`; the staged file cites the **PDF**
`…/2026.gem-main.50.pdf`. They are the same ACL Anthology item — proved from bytes I fetched, not
inferred: the landing page links the PDF itself.

`curl -sS -m 40 -o gem50.html "https://aclanthology.org/2026.gem-main.50/" -w "http=%{http_code} bytes=%{size_download}\n"`
→ `http=200 bytes=47522`; then in `gem50.html`:

- line 1 `<title>`: `Are LLM Benchmarks Already Contaminated? A Systematic Review of Contamination Detection Methods - ACL Anthology` — byte-identical title to S001's.
- line 6: `<h2 id=title><a href=https://aclanthology.org/2026.gem-main.50.pdf>Are <span class=acl-fixed-case>LLM</span> Benchmarks Already Contaminated? …`
- line 40: `<dt>PDF:</dt><dd><a href=https://aclanthology.org/2026.gem-main.50.pdf>https://aclanthology.org/2026.gem-main.50.pdf</a></dd>`

S122 and S123 have no row under any locator: token counts over the whole registry —
`the-ai-alliance` 0, `card-template` 0, `Jangulo7` 0, `disclosure.yaml` 0, `gem-main.50` 1.
`grep -n -i "alliance"` → no output. No `S122`/`S123`/`S124` ids exist either (registry ids are 88
unique ids, `S001`…`S091`, no duplicates).

## (c) Re-derived unregistered count: **2**

One registered (S124 → S001), two unregistered (S122, S123). The entry's own arithmetic agrees:
its parenthetical names exactly one exception, so "three … not in this lane's registry" cannot be
true of the same sentence.

## (d) The two entry locations, and which one was wrong

Both statements are about the same staged file; both were quoted at my first read (193-line state):

- **Wrong — the amendment section, :41:** "its / three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the one / exception: this lane registers that review at tier A)". It asserts three unregistered and then names one registered exception in the same breath, and it contradicts the re-derivation (2).
- **Right — §Extends, :160:** "two of its three source rows are staged and not in this / lane's registry, while the GEM 2026 review it tabulates is already registered here at tier A, so that / one column is lane-checkable". This matches the re-derivation exactly, and "tier A" is correct (S001).

So **:41 (the amendment section) was the wrong location; §Extends was right.** By my last read the
author had edited the :41 location to "and two / of its three source rows are not in this lane's
registry (the GEM 2026 review it tabulates is the / registered one: this lane carries that review at
tier A as S001)" — semantically correct, and the added `S001` makes it checkable. Line numbers had
drifted to :41 / :159 by then.

## (e) Minimal repair sentence

Minimal change to the amendment-section sentence, stating the re-derived count:

> before: `its three source rows are not in this lane's registry (the GEM 2026 review it tabulates is the one exception: this lane registers that review at tier A)`
>
> after: **`two of the three source rows it names are not in this lane's registry (the GEM 2026 review it tabulates is the one exception: this lane registers that review at tier A, S001)`**

Two constraints make this wording, not the obvious one, the minimal *passing* one — both proved below.

## Findings

### F1 — HIGH — the natural minimal repair does not clear R6: the negative predicate forbids its own target wording

`check_r6` rejects the entry when `flat(text)` contains `"three source rows are not in this lane's registry"`
(`plans/round31_defects.py:165`). Any repair of the form "two of **its** three source rows are not in
this lane's registry" still contains that substring ("…its **three source rows are not in this lane's
registry**"). Proof, on a copy of the *current* (196-line) entry:

```
CURRENT   : 'the entry still says three staged source rows are unregistered'
```
and
```
python3 -c "... print(repr(m.check_r6(lane)))"
'the entry still says three staged source rows are unregistered'
forbidden substring present: True
positive phrase present: True
```

The repair the author landed mid-review ("and two of its three source rows are not in this lane's
registry …") is therefore **still a DEFECT by the counter**, even though its content is now correct.
The counter also prints `DEFECT R6 … the entry still says three staged source rows are unregistered`
against a sentence that no longer says three — a false diagnostic. Fix: make the negative predicate
match the assertion, not the substring, e.g. reject on `re.search(r"(?<!two of its )\bthree source rows are not in this lane's registry", entry)`,
or (simpler and honest) reject on `"its three source rows are not in this lane's registry"` — the
phrase that was actually wrong — and keep the positive count check as the real test.

### F2 — HIGH — R6 is unsatisfiable as coded: the URL test never credits S124

`check_r6` counts a staged URL as registered only by exact string containment
(`url.rstrip("/") in registry`, `plans/round31_defects.py:170`). The staged file cites
`…2026.gem-main.50.pdf`; the registry carries `…2026.gem-main.50/`. Direct measurement of that
predicate over the three URLs:

```
'https://the-ai-alliance.github.io/trust-safety-evals/evaluations/benchmark-card-template/' | rstrip-in-registry: False | bare-doc-token: False
'https://github.com/Jangulo7/contamination-disclosure-paper/blob/4dba1ed9b2ace8b71a2edcd5fa6ce0337cf08ba6/templates/disclosure.yaml' | rstrip-in-registry: False | bare-doc-token: False
'https://aclanthology.org/2026.gem-main.50.pdf' | rstrip-in-registry: False | bare-doc-token: True
```

So the check re-derives 3 unregistered and refuses the repair that assumes 2 — with a
substring-free, semantically correct wording in place:

```
CURRENT   : 'the entry still says three staged source rows are unregistered'
SUBSTRING-FREE WORDING: 're-derived 3 unregistered staged sources, the repair assumes 2'
```

R6 therefore cannot reach 0 for any entry text; C2's frozen predicate (`defects=0`, exit 0) is
unreachable through R6 until the check resolves the locator form. Minimal counter fix:

```python
def _registered(url: str, registry: str) -> bool:
    cands = {url, url.rstrip("/")}
    if url.endswith(".pdf"):
        cands.add(url[:-4].rstrip("/") + "/")   # ACL item landing page (S124 -> S001)
    return any(c in registry for c in cands)
```

with a one-line comment naming S124 → S001 so the normalization is not silent. (Adding a registry row
for the `.pdf` is *not* the fix: adopting those rows is the entry's declared open work, and R6 is a
copyedit item.)

### F3 — MEDIUM — R6's positive predicate is vacuous

`"two of its three source rows" not in entry` (`:172`) is already satisfied by §Extends at :159/:160
before any repair, so after F1/F2 are fixed that clause tests nothing. The check's only real content
is the count re-derivation (F2), which is broken. Either scope the positive test to the amendment
section or drop it and rely on the re-derivation plus the corrected negative predicate.

### F4 — LOW — the defect's line citations drift

R6's own docstring and the round-31 claim cite `:41` and `:160`; the entry is worktree-modified and
was edited during review (193 → 196 lines, `:160` → `:159`). Cite by quoted text. Not a scoring
issue, but a re-run at a different moment will not reproduce those numbers.

## Residual risk and verification gaps

- I did **not** open the S124 PDF body: the §7 heading "Towards a Contamination Transparency Card"
  is the staged file's label and the entry's claim, not my observation. Identity of S124 with S001
  rests on the landing page's own PDF link and byte-identical title (quoted above), which is enough
  for "same registry row", not for "§7 says X".
- I did not fetch the AI Alliance template page or the CTC `disclosure.yaml`; their unregistered
  status is a registry-side fact (0 token hits), which is all R6 needs.
- The registry contains 88 unique ids spanning `S001`…`S091` (3 gaps); row count and id space are
  consistent with the lane facts, but I did not audit the gaps.
- `python3 plans/round31_defects.py --lane .` at my first run: `checks=10 defects=10`, exit 1
  (matches the frozen control `.ufo/waves/round-31/claims/defects-before.txt`, `checks=10 defects=10`);
  at my last run: `checks=10 defects=6`, with R6 still among the six. The counter has no write
  surface (only `subprocess.run` for read-only git), so running it does not perturb the tree.

## Commands run (verbatim, with the outputs that carry the finding)

```
ls /home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/ /home/vgpnk/Projects/shokuknow/merge/kengaku/
grep -rn "three source rows are not in this lane" corpus/ plans/ .ufo/waves/round-31/
  -> corpus/knowledge/contamination-transparency-card.md:41 / plans/round31_defects.py:21,165
grep -n "^source:\|^  *source:\|source:" benchmark-card-field-schema-2026-10-23.md
  -> 2,3,4 (S122, S123, S124)
sha256sum benchmark-card-field-schema-2026-10-23.md
  -> 66651007989a7fb5df4671f5f86e69ab1436517025a821afe8c451641a3533b9
for u in <three tokens>; do grep -n "$u" corpus/SOURCES.md || echo "NO ROW"; done
  -> NO ROW / NO ROW / NO ROW      (literal locators)
grep -n -i "gem" corpus/SOURCES.md
  -> 23: | S001 | … https://aclanthology.org/2026.gem-main.50/ … | A | … | mined | 2026-10-19 | …
for p in the-ai-alliance card-template Jangulo7 disclosure.yaml gem-main.50; do grep -c "$p" corpus/SOURCES.md; done
  -> 0 0 0 0 1
grep -n -i "alliance" corpus/SOURCES.md   -> (no output)
grep -o "^| S[0-9]\{3\}" corpus/SOURCES.md | sort | uniq | wc -l  -> 88
  first/last -> | S001 / | S091 ; uniq -d -> (none) ; "^| S12[234] " -> none
python3 plans/round31_defects.py --lane .   -> checks=10 defects=10, exit 1  (first run)
python3 plans/round31_defects.py --lane .   -> checks=10 defects=6           (last run, mid-repair)
python3 -c "import round31_defects as m; print(repr(m.check_r6(Path('.'))))"
  -> 'the entry still says three staged source rows are unregistered'
python3 -c "… 'three source rows are not in this lane\'s registry' in m.flat(...) …"
  -> forbidden substring present: True ; positive phrase present: True
python3 <copy of lane: entry + SOURCES.md> check_r6 on candidate repairs
  -> A minimal substring-keeping : 'the entry still says three staged source rows are unregistered'
  -> B rewording (substring-free): 're-derived 3 unregistered staged sources, the repair assumes 2'
python3 - <<EOF … re.findall(r"^source:[ \t]*S[0-9]+ [—-] (https?://\S+)", staged) … EOF
  -> urls: 3 ; rstrip-in-registry False/False/False ; bare-doc-token False/False/True
curl -sS -m 40 -o gem50.html "https://aclanthology.org/2026.gem-main.50/" -w "http=%{http_code} bytes=%{size_download}\n"
  -> http=200 bytes=47522
grep -n '2026\.gem-main\.50\.pdf' gem50.html ; grep -o '<title>[^<]*</title>' gem50.html
  -> lines 1, 6, 40 ; title = "Are LLM Benchmarks Already Contaminated? A Systematic Review of Contamination Detection Methods - ACL Anthology"
cat .ufo/waves/round-31/claims/defects-before.txt   -> checks=10 defects=10
```

VERDICT: R6 CONTENT REPAIRABLE — re-derived count is 2 (registered: S124 under S001; unregistered: S122, S123), the amendment section at :41 was the wrong location and §Extends at :160 the right one, but the check as coded rejects every repair (F1 substring trap, F2 `.pdf` vs `.50/` locator) so C2 cannot print defects=0 until `check_r6` is corrected.
