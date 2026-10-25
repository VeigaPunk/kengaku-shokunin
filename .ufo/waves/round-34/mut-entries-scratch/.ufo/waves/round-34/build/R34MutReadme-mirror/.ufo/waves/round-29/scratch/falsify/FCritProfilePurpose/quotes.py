# Verifies each quote is verbatim on the cited 1-based line; word count = whitespace split.
import sys
Q = [
 ("plans/round-29-claims.md", 13, "neutral substitution profiles (2436 task/profile projections)"),
 ("plans/round-29-claims.md", 31, "own-work profiles.json: distinct origins, path-prefix sensitivity, trailing-slash sensitivity."),
 ("plans/round-29-claims.md", 40, "P2/P3 sensitivity profiles are not deployment recommendations or model errors."),
 ("plans/round-29-claims.md", 44, "frozen benign profile domain"),
 ("plans/round-29-claims.md", 55, "Output must name scope and profiles' synthetic purposes."),
 ("plans/fixtures/r29/manifest.json", 15, "own-work synthetic neutral profiles"),
 ("plans/config_projection.py", 32, "no profile is a documented deployment baseline, and stimulus effects are never findings."),
 ("plans/config_projection.py", 34, "origin-only synthetic values; not the README-documented SHOPPING_ADMIN '/admin' shape"),
 ("plans/config_projection.py", 44, "three frozen synthetic *.invalid sensitivity stimuli, not deployment recommendations"),
 ("plans/config_projection.py", 290, "index_violations = [{\"output_index\": i, \"task_id\": task_id}"),
 ("plans/config_projection.py", 275, "findings.append({\"id\": \"task_population_invalid\"})"),
 (".ufo/waves/round-29/drafts/webarena-config-projection.md", 18, "The three profiles are controlled sensitivity stimuli, not deployment recommendations."),
 (".ufo/waves/round-29/drafts/webarena-config-projection.md", 27, "exports scheme-less example `origin:port` values (SHOPPING_ADMIN adds"),
 (".ufo/waves/round-29/drafts/webarena-config-projection.md", 71, "with the run's own value map"),
 (".ufo/waves/round-29/drafts/webarena-config-projection.md", 72, "non-URL changed leaf (`must_include`, annotations) is intended"),
 (".ufo/waves/round-29/drafts/webarena-config-projection.md", 74, "because text replacement would break JSON or cascade."),
 (".ufo/waves/round-29/drafts/webarena-config-projection.md", 66, "never counted as defects, model errors or task invalidity."),
 (".ufo/waves/round-28/scratch/OpenTasks/pinned-README.md", 86, 'export SHOPPING="<your_shopping_site_domain>:7770"'),
 (".ufo/waves/round-28/scratch/OpenTasks/pinned-README.md", 87, 'export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"'),
]
bad = 0
for path, line, q in Q:
    text = open(path, encoding="utf-8").read().split("\n")[line - 1]
    ok = q in text
    bad += not ok
    print("%s %s:%d words=%d" % ("OK" if ok else "MISS", path, line, len(q.split())))
print("quotes", len(Q), "miss", bad)
