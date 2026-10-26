import subprocess, shutil, pathlib, json, sys
HERE=pathlib.Path(".").resolve(); T=HERE.parent/"tb2/db-wal-recovery"
cases={
 "nop":":",
 "oracle-solve.sh":"bash /solution/solve.sh >/dev/null 2>&1",
 "base-only-5-rows":"""python3 - <<'P'
import sqlite3,json
c=sqlite3.connect("file:/app/main.db?mode=ro",uri=True); r=[{"id":a,"name":b,"value":v} for a,b,v in c.execute("select id,name,value from items order by id")]
json.dump(r,open("/app/recovered.json","w"))
P""",
 "typed-literals-never-open-db":"""python3 - <<'P'
import json
n=["apple","banana","cherry","date","elderberry","fig","grape","honeydew","kiwi","lemon","mango"]
json.dump([{"id":i+1,"name":n[i],"value":(150 if i==0 else 250 if i==1 else 0)} for i in range(11)],open("/app/recovered.json","w"))
P""",
 "typed-literals-names1-2-wrong":"""python3 - <<'P'
import json
n=["x","y","cherry","date","elderberry","fig","grape","honeydew","kiwi","lemon","mango"]
json.dump([{"id":i+1,"name":n[i],"value":(150 if i==0 else 250 if i==1 else 0)} for i in range(11)],open("/app/recovered.json","w"))
P""",
 "typed-literals-id3-name-wrong":"""python3 - <<'P'
import json
n=["apple","banana","CHERRY","date","elderberry","fig","grape","honeydew","kiwi","lemon","mango"]
json.dump([{"id":i+1,"name":n[i],"value":(150 if i==0 else 250 if i==1 else 0)} for i in range(11)],open("/app/recovered.json","w"))
P""",
 "value-float":"""python3 - <<'P'
import json
n=["apple","banana","cherry","date","elderberry","fig","grape","honeydew","kiwi","lemon","mango"]
json.dump([{"id":i+1,"name":n[i],"value":(150.0 if i==0 else 250 if i==1 else 0)} for i in range(11)],open("/app/recovered.json","w"))
P""",
}
for cid,body in cases.items():
    app=HERE/"app"/cid
    if app.exists(): shutil.rmtree(app)
    app.mkdir(parents=True)
    shutil.copy(T/"environment/main.db",app/"main.db"); shutil.copy(T/"environment/main.db-wal.encrypted",app/"main.db-wal")
    cmd=["bwrap","--unshare-net","--unshare-pid","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--symlink","usr/lib","/lib","--symlink","usr/lib","/lib64","--ro-bind","/etc","/etc","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--bind",str(app),"/app","--ro-bind",str(T/"tests"),"/tests","--ro-bind",str(T/"solution"),"/solution","--ro-bind",str(HERE/"harness.py"),"/h.py","--chdir","/app","bash","-c",f"{body}\npython /h.py"]
    r=subprocess.run(cmd,capture_output=True,text=True)
    res=[l.split() for l in r.stdout.splitlines() if l.startswith("T ")]
    fails=[x[1].replace("test_","") for x in res if x[2]=="FAIL"]
    print(f"{cid:32s} tests={len(res)} fail={len(fails)} {','.join(fails) or '-'}")
