import json,re,os,sys
LANE='/home/vgpnk/Projects/shokunin/kengaku-shokunin'
rows=json.load(open('rows-parsed.json'))
res={}
for r in rows:
    m=re.search(r'python3 (plans/[\w\-]+\.py|corpus/[\w/\-]+\.py)', r['entry'])
    if not m:
        m2=re.search(r'(plans/[\w\-]+\.py)', r['entry'])
        script=m2.group(1) if m2 else None
    else: script=m.group(1)
    p=os.path.join(LANE,script) if script else None
    f={'script':script,'exists':bool(p and os.path.exists(p))}
    if f['exists']:
        src=open(p,encoding='utf-8',errors='replace').read()
        f['lines']=src.count('\n')
        f['add_argument']=sorted(set(re.findall(r"add_argument\(\s*['\"](--?[\w\-]+)['\"]",src)))
        f['argparse_positional']=re.findall(r"add_argument\(\s*['\"]([a-z][\w\-]*)['\"]",src)
        f['sys_exit']=sorted(set(re.findall(r'sys\.exit\(\s*(-?\w+|\d+)',src)))
        f['exit_call']=sorted(set(re.findall(r'(?<![\w.])exit\(\s*(\d+)',src)))
        f['return_int']=sorted(set(re.findall(r'return\s+(\d)\b',src)))
        f['selftest_literal']= '--selftest' in src
        f['selftest_flag_decl']= bool(re.search(r"add_argument\(\s*['\"]--selftest",src))
        f['writes']=sorted(set(re.findall(r"open\([^)]*['\"][wax]\+?b?['\"]",src)))[:10]
        f['write_text']=len(re.findall(r'write_text|write_bytes|shutil\.|os\.remove|os\.unlink|os\.mkdir|makedirs|mkdtemp|TemporaryDirectory|NamedTemporaryFile|subprocess',src))
        f['git_calls']=len(re.findall(r"'git'|\"git\"|git-",src))
        f['subcommands']=sorted(set(re.findall(r"add_subparsers|add_parser\(\s*['\"]([\w\-]+)",src)))
        f['pins_in_src']=sorted(set(re.findall(r"(?:plans|corpus|\.ufo)/[\w/\.\-]+",src)))[:40]
    res[r['name']]=f
json.dump(res,open('facts.json','w'),indent=1)
for k,v in res.items():
    print(k, v.get('script'), 'exists' if v.get('exists') else 'MISSING', 'lines=%s'%v.get('lines'))
    if v.get('exists'):
        print('   args:', v['add_argument'])
        print('   sys.exit:', v['sys_exit'], 'exit():', v['exit_call'], 'return:', v['return_int'])
        print('   selftest_literal=%s flag_decl=%s subcommands=%s'%(v['selftest_literal'],v['selftest_flag_decl'],v['subcommands']))
        print('   writes:', v['writes'], 'write_text/sub/tmp count=', v['write_text'], 'git=', v['git_calls'])
