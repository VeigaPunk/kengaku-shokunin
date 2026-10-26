# R37CritCases — predictions for 2 extra cases (written before their run)

Still the frozen probe's machinery (`run_case`), captures at pinned digests. Not counted in the 4/4
uncovered metric; they close the two confounds named in the report.

| id | fixture | predicted | mechanism | why it matters |
|---|---|---|---|---|
| `wget-wrong-content` | tools=wget, files `200` body `"Hello World\n"` | **fail** | verify.sh:80 `[ "$CONTENT" = "hello world" ]` on the wget branch, :83 prints FAILED | the wget branch's *mismatch* path (:80 false → :83/:85) has no case: wget-static-file covers :80 true, wget-404 covers :88, wget-token covers the co-echo. Last uncovered comparison branch |
| `port-8080-junk-8081-correct` | custom script: one server on :8080 answering `200 "not hello\n"`, one on :8081 answering `200 "hello world\n"`, then the captured grader | **fail** | verify.sh:57 hard-codes `localhost:8080`; :63 compares the :8080 body, so the correct :8081 body is never read | replaces the `wrong-port-8081` confound (identical grader stdout to `no-server`, HTTP 000) with a case whose verdict is a *content* mismatch at a live :8080, distinguishable from both 000 and 404 |
