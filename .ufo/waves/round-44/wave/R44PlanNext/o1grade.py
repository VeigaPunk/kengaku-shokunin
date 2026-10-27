import os, pathlib, sys, time, json
S = pathlib.Path(os.environ["S"]); O = S/"o1"; app = O/"app"
src = (S/"tb2/break-filter-js-from-html/tests/test_outputs.py").read_text()
src = src.replace('["python", "/tests/filter.py"', f'["{os.environ.get("PYV", str(O/"venv/bin/python"))}", "{O}/filter.py"').replace('"/app/out.html"', f'"{app}/out.html"')
ns = {"__name__": "g"}; exec(compile(src, "test_outputs.py", "exec"), ns)
def grade(body):
    app.mkdir(exist_ok=True); p = app/"out.html"
    if body is None: p.unlink(missing_ok=True)
    else: p.write_text(body)
    t = time.time()
    try: ns["test_out_html_bypasses_filter"](); r = "pass"
    except AssertionError as e: r = "FAIL: " + str(e)[:60]
    except Exception as e: r = "ERR:" + type(e).__name__ + str(e)[:150]
    return r, round(time.time()-t, 1)
oracle = [l for l in (S/"o1/solve.sh").read_text().splitlines() if l.startswith("echo")][0]
body = oracle.split("'")[1] + "\n"
print("oracle body", repr(body)); print("ORACLE", grade(body))
print("no-file", grade(None))
print("plain-script", grade("<script>alert(1)</script>\n"))
print("empty", grade(""))
