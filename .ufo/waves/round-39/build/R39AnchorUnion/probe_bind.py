import importlib.util, pathlib, sys
spec = importlib.util.spec_from_file_location("adc", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
lane = pathlib.Path(sys.argv[2]).resolve()
idx = m.evidence_index(lane, "head")
rows = m.parse_rows(lane)
multi_cap = multi_tok = 0
for r in rows:
    caps, reason = m.bind_row(r, idx)
    paths = sorted({p for p, _ in caps})
    if len(paths) > 1:
        multi_cap += 1
        print(f"MULTICAP {r['sid']} n={len(paths)} caps={paths} tokens={r['atoks']}")
    if len(r["atoks"]) > 1:
        multi_tok += 1
        print(f"MULTITOK {r['sid']} tokens={r['atoks']} caps={paths}")
print(f"rows={len(rows)} rows_with_multi_capture={multi_cap} rows_with_multi_anchor_token={multi_tok}")
