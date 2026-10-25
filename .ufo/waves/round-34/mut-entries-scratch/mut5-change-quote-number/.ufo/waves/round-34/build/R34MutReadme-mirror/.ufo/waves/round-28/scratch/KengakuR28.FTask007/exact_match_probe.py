"""Author-side boundary probe for WebArena task_id 7 (round28 KengakuR28.FTask007).

NOT an import/execution of upstream code. clean_answer/exact_match/must_include are
reimplemented from reading the pinned evaluators.py lines 80-111, 134, 139-140, 142-149.
Input JSON is read as data only. No network, no benchmark site, no scorer execution.
"""
import json
import sys


def clean_answer(answer: str) -> str:
    answer = answer.strip()
    if answer.startswith("'") and answer.endswith("'"):
        answer = answer[1:-1]
    elif answer.startswith('"') and answer.endswith('"'):
        answer = answer[1:-1]
    return answer.lower()


def exact_match(ref: str, pred: str) -> float:
    return float(clean_answer(pred) == clean_answer(ref))


def must_include(ref: str, pred: str) -> float:
    # single-character tokenize branch is not exercised by the address reference
    return float(clean_answer(ref) in clean_answer(pred))


def main(raw_path: str) -> int:
    raw = json.load(open(raw_path))
    t7 = [t for t in raw if t["task_id"] == 7][0]
    t9 = [t for t in raw if t["task_id"] == 9][0]
    ref = t7["eval"]["reference_answers"]["exact_match"]
    ann = t7["eval"]["reference_answer_raw_annotation"]
    ref9 = t9["eval"]["reference_answers"]["must_include"][0]

    print("task7 eval_types:", t7["eval"]["eval_types"])
    print("task7 reference keys:", list(t7["eval"]["reference_answers"]))
    print("task9 eval_types:", t9["eval"]["eval_types"])
    print("task9 reference keys:", list(t9["eval"]["reference_answers"]))
    print("task7 exact ref == task9 must_include[0]:", ref == ref9)
    print("task9 single-element tokenize flag derived as:", len(t9["eval"]["reference_answers"]["must_include"]) == 1)
    print()

    cases = {
        "exact reference": ref,
        "raw annotation": ann,
        "trailing period": ref + ".",
        "trailing newline": ref + "\n",
        "leading+trailing spaces": "  " + ref + "  ",
        "UPPERCASE": ref.upper(),
        "single outer double quote": '"' + ref + '"',
        "double outer quote layer": "'\"" + ref + "\"'",
        "natural sentence containing ref": "The only international airport is " + ref + ".",
        "add Pennsylvania before ZIP": ref.replace("Allegheny County, 15231", "Allegheny County, Pennsylvania, 15231"),
        "add PA abbreviation": ref.replace("Allegheny County, 15231", "Allegheny County, PA, 15231"),
    }
    print(f"{'prediction':42s} {'task7 exact':>11s} {'task9 must_include':>18s}")
    for name, answer in cases.items():
        pred = clean_answer(answer)  # StringEvaluator.__call__ line 134 pre-clean
        print(f"{name:42s} {exact_match(ref, pred):11.1f} {must_include(ref9, pred):18.1f}")

    # hard controls used in the report
    assert exact_match(ref, clean_answer(ref)) == 1.0
    assert exact_match(ref, clean_answer(ann)) == 0.0
    assert exact_match(ref, clean_answer(ref + ".")) == 0.0
    assert exact_match(ref, clean_answer('"' + ref + '"')) == 1.0
    assert exact_match(ref, clean_answer("'\"" + ref + "\"'")) == 1.0
    assert must_include(ref9, clean_answer("The only international airport is " + ref + ".")) == 1.0
    assert exact_match(ref, clean_answer("The only international airport is " + ref + ".")) == 0.0
    assert must_include(ref9, clean_answer(ann)) == 0.0
    print("\nassertions: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
