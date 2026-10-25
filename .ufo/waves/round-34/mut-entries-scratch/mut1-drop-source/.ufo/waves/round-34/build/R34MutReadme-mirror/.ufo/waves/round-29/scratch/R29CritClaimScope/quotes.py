Q=[("plans/round-29-claims.md",13,"neutral substitution profiles (2436 task/profile projections), including replacement occurrence/field"),
("plans/round-29-claims.md",15,"README's generated-eval-config frontier only for an offline source-faithful projection. Score7 held;"),
("plans/round-29-claims.md",16,"No new scientific method, actual deployment config, task validity,"),
("plans/round-29-claims.md",64,"per-profile raw replacement counts by token, source text/projection digests, parsed task count,"),
("plans/round-29-claims.md",65,"changed string leaves by JSON path and category, remaining known placeholders;"),
("plans/round-29-claims.md",106,"F3 global replacement changes at least one non-URL-valued field, p=.7;"),
("plans/fixtures/r29/generate_test_data.py",15,'raw = raw.replace("__WIKIPEDIA__", WIKIPEDIA)'),
("SCORECARD.md",928,"Frontier: generated task configurations/runtime evidence, additional benchmark specs and semantic"),
("corpus/knowledge/webarena-task-spec-audit.md",85,"mismatch exists in authored text; actual runtime task invalidity still requires the generated config,"),
("PROVINCE.md",201,"generated configs, runtime task validity, hosted judges and contamination remain open."),
]
ok=True
for f,l,q in Q:
    line=open(f,encoding="utf-8").read().split("\n")[l-1]
    hit=q in line; w=len(q.split()); ok&=hit and w<=25
    print(f"{f}:{l} substring={hit} words={w}")
print("ALL_OK",ok)
