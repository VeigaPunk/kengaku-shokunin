"""Scratch re-derivation, hand transcription of S062 StringEvaluator.clean_answer (lines 80-86)
and exact_match (90-94) / routed pre-clean (134). NOT an import of upstream code."""
def clean_answer(answer):
    answer = answer.strip()
    if answer.startswith("'") and answer.endswith("'"):
        answer = answer[1:-1]
    elif answer.startswith('"') and answer.endswith('"'):
        answer = answer[1:-1]
    return answer.lower()
def exact_match(ref, pred):
    return float(clean_answer(pred) == clean_answer(ref))
def routed(ref, raw):
    pred = clean_answer(raw)          # line 134
    return exact_match(ref, pred)     # line 140 path
cases = {"v1 claimed witness  \"'a'\"": ("a", "'a'"), "corrected witness ''a''": ("a", "''a''")}
for label,(ref,raw) in cases.items():
    print(f"{label}: direct={exact_match(ref, raw)} routed={routed(ref, raw)} clean(clean(x))={clean_answer(clean_answer(raw))!r} clean(x)={clean_answer(raw)!r}")
