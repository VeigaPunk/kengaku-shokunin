# R31FxRowIdentity — V2 cited-row identity

Scope: `plans/round31_c1_verify.py`, `check_v2` lines 68–88 (especially URL extraction at 77–80 and line matching at 81–87). Fixtures and all mutations were isolated under `/tmp/r31fx-rowidentity/`; no lane files were changed.

Command used for the first three fixture runs: `python3 - <<'PY' ... importlib.util.spec_from_file_location('v', '/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round31_c1_verify.py'); v.check_v2(fixture_path, {'entries':[{'sources':['S092','S093','S100']}]}) ... PY`. The fixture rows used the registry table shape parsed by `registry_sources` (script lines 56–65). A second invocation of the same checker constructed the all-same-document fixture. Exact fixture files are in the named subdirectories beneath `/tmp/r31fx-rowidentity/`.

## Observations

- **Different host: caught.** `host-mismatch` has S092 registry URL `https://right.example/doc`, while its `source: S092` entry line says `https://wrong.example/doc`; checker returned `the entry's S092 line does not name the row's cited document (right.example/doc)`. This follows from literal containment at script line 86.
- **Bare host vs deep path: passed.** `bare-host-deep-path` registry source for S093 is `https://host.example`, while the entry says `https://host.example/deep/path`; `check_v2` returned an empty defect string. `rstrip('/')` at line 80 leaves `host.example`; containment at line 86 consequently accepts a deeper, potentially different document.
- **Two (indeed three) rows citing the same document: passed.** In `duplicate-doc`, all three registry `source` cells and all three id-specific entry lines name `https://same.example/doc`; checker returned an empty defect string. V2 does not enforce distinct document identity across cited IDs. The frozen C1 predicate requires distinct IDs (claims file lines 30–35), not distinct documents.
- **Entry line has URL but not the ID: caught.** In `url-without-id`, the URL appears in prose but the entry has no line beginning `source: S092`; checker returned `the entry has no 'source: S092' line`, per regex gate at lines 81–85.

## Wrong-document conclusion

**Yes, V2 can be satisfied by a wrong document.** Direct counterexample: the bare-host fixture's registry cites `https://host.example` and the entry names a deeper path `https://host.example/deep/path`; that path passes despite not being the same URL. More generally line 86 uses substring containment, not parsed URL equality, and the URL regex may also take a substring from longer text (lines 39, 77–80). The duplicate-doc fixture independently shows that separate IDs may all resolve to one document without rejection.

VERDICT: V2 caught the different-host and missing-id fixtures; it passed the bare-host/deep-path mismatch and the shared-document fixture, so cited-row identity survived only as a weak host/path-substring check and fell as a guarantee of exact document identity.
