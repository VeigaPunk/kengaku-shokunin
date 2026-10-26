import os, shutil, subprocess, pathlib, tempfile
S=pathlib.Path('/fast/scratch/hyaku/kengaku-r41/R41PlanNext'); CAP=pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round41/tb2-constraints-scheduling')
H='''
import importlib.util
spec=importlib.util.spec_from_file_location("g","/cap/test_outputs.py"); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
out=[]
for n in ("test_structure_event_title_attendees_duration_window","test_constraints_conflicts_business_hours","test_earliest_tiebreakers_and_carol_buffer"):
    try: getattr(g,n)(); out.append("P")
    except BaseException as e: out.append("F")
print("".join(out))
'''
(S/'cp_h.py').write_text(H)
env={'PATH':'/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'}
def sb(app):
    a=["/usr/bin/bwrap","--unshare-net","--unshare-pid","--die-with-parent","--new-session","--ro-bind","/usr","/usr"]
    for l in ("/bin","/sbin","/lib","/lib64"):
        if os.path.islink(l): a+=["--symlink",os.readlink(l),l]
    return a+["--ro-bind","/etc","/etc","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--bind",str(app),"/app","--ro-bind",str(CAP),"/cap","--ro-bind",str(S/'cp_h.py'),"/h.py","--chdir","/app"]
def case(name, rewrite):
    w=pathlib.Path(tempfile.mkdtemp(prefix='cp-',dir=S)); app=w/'app'; app.mkdir()
    for n in ("alice_calendar.ics","bob_calendar.ics","carol_calendar.ics"): shutil.copy(CAP/n, app/n)
    p=subprocess.run(sb(app)+['bash','/cap/solve.sh'],capture_output=True,text=True,env=env)
    for n in ("alice_calendar.ics","bob_calendar.ics","carol_calendar.ics"):
        b=(app/n).read_bytes(); (app/n).write_bytes(rewrite(b))
    r=subprocess.run(sb(app)+['python3','/h.py'],capture_output=True,text=True,env=env)
    shutil.rmtree(w,ignore_errors=True); return name, r.stdout.strip() or r.stderr[-120:]
print('orig-bytes-LF-check', [ (b'\r' in (CAP/n).read_bytes()) for n in ("alice_calendar.ics","bob_calendar.ics","carol_calendar.ics")])
cases=[('identity',lambda b:b),
 ('crlf-all',lambda b:b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')),
 ('bare-cr-all',lambda b:b.replace(b'\r\n',b'\n').replace(b'\n',b'\r')),
 ('crlf-first-line-only',lambda b:b.replace(b'\n',b'\r\n',1)),
 ('trailing-space',lambda b:b.replace(b'\n',b' \n',1)),
 ('append-nl',lambda b:b+b'\n'),
 ('utf8-bom',lambda b:b'\xef\xbb\xbf'+b)]
for n,f in cases: print(*case(n,f))
