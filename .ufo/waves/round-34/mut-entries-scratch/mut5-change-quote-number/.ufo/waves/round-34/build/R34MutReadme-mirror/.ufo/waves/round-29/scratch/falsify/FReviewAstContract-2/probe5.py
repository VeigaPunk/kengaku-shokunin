#!/usr/bin/env python3
"""Boundary probe: is the repaired gate's residual acceptance behaviour-preserving only?"""
import ast
import importlib.util
import json
from pathlib import Path

BASE = Path("/tmp/freview-astcontract")
MODULE = BASE / "config_projection_dbcecded.py"
GEN = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/fixtures/r29/generate_test_data.py")
spec = importlib.util.spec_from_file_location("cp", MODULE)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
source = GEN.read_text()

CASES = {
 "X01_parenthesised_replace_call": source.replace('raw = raw.replace("__GITLAB__", GITLAB)',
                                                   'raw = (raw.replace("__GITLAB__", GITLAB))'),
 "X02_escaped_token_literal_same_value": source.replace('"__GITLAB__", GITLAB', '"__GIT\\u004cAB__", GITLAB'),
 "X03_numeric_literal_spelling_same_value": source.replace('"w")', '"w")'),
 "X04_docstring_carries_extra_text": source.replace('"""Replace the website placeholders with website domains from env_config\nGenerate the test data"""',
                                                    '"""Replace the website placeholders with website domains from env_config\nGenerate the test data\nNOTE: extra prose only"""'),
 "X05_trailing_comment_on_import": source.replace("import json\n", "import json  # noqa\n"),
 "X06_semantics_change_hidden_in_docstring": source.replace('    data = json.loads(raw)',
                                                            '    data = json.loads(raw)  # semantics changed below\n    data = json.loads(raw.upper())'),
}
rows = []
for name, text in sorted(CASES.items()):
    try:
        cp.source_contract(text)
        status = "ACCEPT"
    except cp.Unevaluable as error:
        status, text_reason = "REJECT", error.finding
        text_reason = json.dumps(error.finding, sort_keys=True)
    else:
        text_reason = ""
    # behaviour check: same rendered module statements as the pinned generator?
    def rendered(t):
        tree = ast.parse(t)
        stmts = [n for n in tree.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str))]
        return [ast.unparse(n).replace("for (idx, item) in", "for idx, item in") for n in stmts]
    same = rendered(text) == rendered(source)
    rows.append({"case": name, "status": status, "reason": text_reason, "same_rendered_statements_as_pinned": same})
    print("%-40s %-6s same_rendered=%s %s" % (name, status, same, text_reason[:110]))

accepted = [r["case"] for r in rows if r["status"] == "ACCEPT"]
print()
print("ACCEPTED", json.dumps(accepted))
print("ACCEPTED_BUT_STATEMENTS_DIFFER", json.dumps([r["case"] for r in rows if r["status"] == "ACCEPT" and not r["same_rendered_statements_as_pinned"]]))
Path(BASE / "boundary.json").write_text(json.dumps(rows, indent=2, sort_keys=True))
