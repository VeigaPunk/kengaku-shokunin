"""Miniature probes of production audit_tasks (read-only import, bytecode disabled) vs hand-expected scorer outcomes.

The scorer-side expectation is derived by hand from pinned evaluators.py:187-239 (clean_url = rstrip('/'),
base = netloc + path, `ref_base in pred_base` substring). It is re-expressed here with stdlib urllib only;
no upstream file is imported or executed.
"""
import copy
import importlib.util
import json
import sys
import urllib.parse

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audit", sys.argv[1])
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def hand_base_vacuous(ref):
    """True when some cleaned alternative has empty netloc+path, i.e. `'' in pred_base` always holds."""
    if not isinstance(ref, str):
        return None
    return any(not (lambda p: p.netloc + p.path)(urllib.parse.urlparse(a.rstrip("/"))) for a in ref.split(" |OR| "))


base = {"task_id": 0, "sites": ["gitlab"], "intent": "go there", "require_login": False, "require_reset": False,
        "eval": {"eval_types": ["url_match"], "reference_url": "__GITLAB__/x", "url_note": "GOLD in PRED"}}
cases = [
    ("baseline", "__GITLAB__/x", "GOLD in PRED", True),
    ("default_rule_absent", "__GITLAB__/x", None, True),
    ("null_rule", "__GITLAB__/x", "NULL", True),
    ("empty_ref", "", "GOLD in PRED", True),
    ("missing_ref", "MISSING", "GOLD in PRED", True),
    ("list_ref", ["__GITLAB__/x"], "GOLD in PRED", True),
    ("raw_empty_alt", "__GITLAB__/x |OR| ", "GOLD in PRED", True),
    ("slash_only", "/", "GOLD in PRED", True),
    ("slash_alt", "__GITLAB__/x |OR| /", "GOLD in PRED", True),
    ("double_slash", "//", "GOLD in PRED", True),
    ("scheme_only", "http://", "GOLD in PRED", True),
    ("query_only", "?q=a", "GOLD in PRED", True),
    ("fragment_only", "#frag", "GOLD in PRED", True),
    ("query_only_alt", "__GITLAB__/x |OR| ?q=a", "GOLD in PRED", True),
    ("no_space_delimiter", "__GITLAB__/x |OR|__GITLAB__/y", "GOLD in PRED", True),
    ("whitespace_only", "   ", "GOLD in PRED", True),
    ("html_first_order", "__GITLAB__/x", "GOLD in PRED", False),
]
rows = []
for name, ref, note, url_first in cases:
    task = copy.deepcopy(base)
    ev = task["eval"]
    if ref == "MISSING":
        del ev["reference_url"]
    else:
        ev["reference_url"] = ref
    if note is None:
        del ev["url_note"]
    elif note == "NULL":
        ev["url_note"] = None
    if not url_first:
        ev["eval_types"] = ["program_html", "url_match"]
        ev["program_html"] = [{"url": "__GITLAB__/elsewhere", "locator": "", "required_contents": {"must_include": ["x"]}}]
    result = audit.audit_tasks([task], expected_population=1)
    rows.append({"case": name, "reference_url": ref if ref != "MISSING" else "<absent>",
                 "audit_findings": sorted({f["id"] for f in result["findings"]}),
                 "record_url_note": result["tasks"][0]["url_note"] if result["tasks"] else None,
                 "url_rules": result["metrics"].get("url_rules"),
                 "hand_scorer_base_vacuous": hand_base_vacuous(ref) if ref != "MISSING" else "KeyError"})
# record-level provenance: non-url task without url_note key
plain = {"task_id": 0, "sites": ["s"], "intent": "q", "require_login": False, "require_reset": False,
         "eval": {"eval_types": ["string_match"], "reference_answers": {"exact_match": "a"}}}
r = audit.audit_tasks([plain], expected_population=1)
rows.append({"case": "non_url_task_without_url_note", "record_url_note": r["tasks"][0]["url_note"],
             "raw_has_url_note": "url_note" in plain["eval"], "url_rules": r["metrics"].get("url_rules")})
print(json.dumps(rows, indent=1))
