"""Scratch-only source mutants of the pinned evaluators.py text fed to the instrument's scorer_contract()."""
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
INSTRUMENT, SOURCE = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("audit_under_probe", INSTRUMENT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = SOURCE.read_text(encoding="utf-8")
baseline = module.scorer_contract(source)

MUTANTS = {
    "M1_router_wildcard_raise_removed": ("            case _:\n                raise ValueError(f\"eval_type {eval_type} is not supported\")\n", ""),
    "M2_url_unknown_rule_scores_zero": ("            raise ValueError(f\"Unknown matching rule: {matching_rule}\")", "            score = 0.0"),
    "M3_unknown_locator_scores_empty": ("                raise ValueError(f\"Unknown locator: {locator}\")", "                selected_element = \"\""),
    "M4_js_locator_exception_propagates": ("                except Exception:\n                    # the page is wrong, return empty\n                    selected_element = \"\"\n", "                finally:\n                    pass\n"),
    "M5_helper_eval_absorbed": ("                selected_element = eval(func)", "                try:\n                    selected_element = eval(func)\n                except Exception:\n                    selected_element = \"\""),
    "M6_product_operand_constant": ("            score *= cur_score", "            score *= 1.0"),
    "M7_comb_only_first_evaluator": ("        for evaluator in self.evaluators:", "        for evaluator in self.evaluators[:1]:"),
    "M8_na_override_unconditional": ("                        if score != 1:\n                            score = 1.0 * self.ua_match(", "                        if True:\n                            score = 1.0 * self.ua_match("),
    "M9_router_renamed": ("def evaluator_router(", "def evaluator_router_v2("),
    "M10_product_to_sum_control": ("            score *= cur_score", "            score += cur_score"),
}

results = {}
for name, (old, new) in MUTANTS.items():
    assert source.count(old) == 1, (name, source.count(old))
    mutated = source.replace(old, new)
    try:
        contract = module.scorer_contract(mutated)
    except Exception as error:
        results[name] = {"outcome": "REJECTED", "exception": type(error).__name__, "message": str(error)}
    else:
        results[name] = {"outcome": "SURVIVED", "contract_identical_to_baseline": contract == baseline,
                         "product_lines": contract["composition"]["source_lines"], "na_lines": contract["na_fallback"]["source_lines"]}
print(json.dumps(results, indent=1))
