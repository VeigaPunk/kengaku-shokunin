## Erratum (round 65)

R64-ERRATUM-65 — dated 2026-11-03. The `## Gate` S230 bullet above quotes
`"Port 5328 is not listening - no real gRPC server is running"` (line 96) as located source text; that string is the
f-string RENDERED at port 5328, not the source. Source line 96 reads
`assert result == 0, f"Port {port} is not listening - no real gRPC server is running"`. The same rendered-form
defect sits in S230's anchor cell; it is superseded by registry row S234 (same URL and capture, `supersedes S230 —`,
verbatim f-string anchor, `teaches` 22 words). The block above stays byte-identical (append-only; CORPUS prohibits
in-place rewrites). Sources: `corpus/lessons/round-64-verifier-spotcheck.md` §7.1; S234 in `corpus/SOURCES.md`.
