import os, pathlib, re, subprocess, shutil, sys, hashlib
S = pathlib.Path(os.environ["S"]); T = S/"tb2"; O = S/"or"
def grade(task, app):
    src = (T/task/"tests/test_outputs.py").read_text().replace("/app/", str(app)+"/")
    ns = {"__name__":"g"}; exec(compile(src, f"{task}/test_outputs.py", "exec"), ns)
    res = {}
    for k, v in list(ns.items()):
        if k.startswith("test_") and callable(v):
            try: v(); res[k] = "pass"
            except AssertionError as e: res[k] = "FAIL"
            except Exception as e: res[k] = "ERR:"+type(e).__name__
    return res
def sh(cmd, cwd): return subprocess.run(["bash","-c",cmd],cwd=cwd,capture_output=True,text=True,timeout=120)
# --- password-recovery: remap /app -> scratch, run setup.sh then solve.sh
app = O/"pw/app"; shutil.rmtree(O/"pw", ignore_errors=True); app.mkdir(parents=True)
setup = (T/"password-recovery/environment/setup.sh").read_text().replace("/app", str(app))
r = sh(setup, app); print("pw setup rc", r.returncode)
solve = (T/"password-recovery/solution/solve.sh").read_text().replace("/app/varsea", str(app)+"/varsea")
r = sh(solve, app); print("pw solve rc", r.returncode, "lines", len((app/"recovered_passwords.txt").read_text().splitlines()))
print("pw ORACLE", grade("password-recovery", app))
# cases
P = "8XDP5Q2RT9ZK7VB3BV4WW54"; f = app/"recovered_passwords.txt"
for name, body in [("exact-line", P+"\n"), ("only-constant-no-nl", P), ("crlf", P+"\r\n"), ("constant-in-longer-line", "PASSWORD="+P+"\n"),
                   ("100k-guesses+constant", "\n".join(f"8XD{i:017d}"[:20]+"W54" for i in range(100000))+"\n"+P+"\n"),
                   ("trailing-space", P+" \n"), ("empty", ""), ("wrong", "8XDP5Q2RT9ZK7VB3BV4WW55\n"), ("leading-blank-line", "\n"+P+"\n")]:
    f.write_text(body); print("pw", name, grade("password-recovery", app))
# --- sqlite-db-truncate
app = O/"sql/app"; shutil.rmtree(O/"sql", ignore_errors=True); app.mkdir(parents=True); shutil.copy(S/"tb2bin/trunc.db", app/"trunc.db")
solve = (T/"sqlite-db-truncate/solution/solve.sh").read_text()
r = sh(solve, app); print("sql solve rc", r.returncode, r.stderr[-200:])
print("sql ORACLE", grade("sqlite-db-truncate", app))
import json
soln = [("testword02",10.0),("testword03",25.0),("testword04",42.0),("testword05",50.0),("testword06",75.0),("testword07",99.0),("testword08",99.99),("testword09",0.5)]
rj = app/"recover.json"
def w(rows): rj.write_text(json.dumps(rows))
for name, rows in [("6-of-8", [{"word":a,"value":b} for a,b in soln[:6]]), ("7-of-8", [{"word":a,"value":b} for a,b in soln[:7]]),
                   ("8 ints-as-int", [{"word":a,"value":(int(b) if b==int(b) else b)} for a,b in soln]),
                   ("7-right+junk", [{"word":a,"value":b} for a,b in soln[:7]]+[{"word":"x","value":1}]), ("7 right 1 wrong value", [{"word":a,"value":b} for a,b in soln[:7]]+[{"word":"testword09","value":0.6}]),
                   ("dup rows 7x", [{"word":soln[0][0],"value":soln[0][1]}]*7), ("string values", [{"word":a,"value":str(b)} for a,b in soln])]:
    w(rows); print("sql", name, grade("sqlite-db-truncate", app))
rj.unlink(); print("sql no-file", grade("sqlite-db-truncate", app))
# --- vulnerable-secret
app = O/"vul/app"; shutil.rmtree(O/"vul", ignore_errors=True); app.mkdir(parents=True); shutil.copy(S/"tb2bin/vulnerable.c", app/"vulnerable.c")
r = sh("gcc -std=gnu99 -o vulnerable vulnerable.c -fno-stack-protector -no-pie -O2 -s", app); print("vul gcc rc", r.returncode, r.stderr[-150:])
solve = (T/"vulnerable-secret/solution/solve.sh").read_text().replace("/app/results.txt", str(app)+"/results.txt")
r = sh(solve, app); print("vul solve rc", r.returncode)
print("vul ORACLE", grade("vulnerable-secret", app))
rf = app/"results.txt"; FL = "FLAG{b4ff3r_0v3rfl0w_m4st3r_k3y_2024}"
for name, body in [("flag+nl", FL+"\n"), ("flag+spaces", "  "+FL+"  \n"), ("flag in sentence", "the flag is "+FL+"\n"), ("two lines", FL+"\n"+FL+"\n"), ("wrong", "FLAG{x}\n")]:
    rf.write_text(body); print("vul", name, grade("vulnerable-secret", app))
# strings leak? is FLAG in the binary
b = (app/"vulnerable").read_bytes(); print("vul FLAG literal in binary:", FL.encode() in b)
# --- code-from-image
png = (S/"tb2bin/code.png").read_bytes()
h0 = hashlib.sha256(png).digest(); H = hashlib.sha256(h0 + h0[:10] + b"0000TBENCH-SALT").hexdigest()
print("img H", H, H == "bee26a133f103b9ecda444c70ec22cafef6e31a3de7af6d047974dc90ce3defe")
app = O/"img/app"; app.mkdir(parents=True, exist_ok=True); (app/"output.txt").write_text(H+"\n"); print("img ORACLE", grade("code-from-image", app))
(app/"output.txt").write_text("bee26a\n"); print("img prefix-only", grade("code-from-image", app))
