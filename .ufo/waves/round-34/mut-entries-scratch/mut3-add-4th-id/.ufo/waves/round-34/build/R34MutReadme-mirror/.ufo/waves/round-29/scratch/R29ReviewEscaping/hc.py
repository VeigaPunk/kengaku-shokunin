import json
def probe(label, src, tokmap):
    print("### "+label)
    print("  src:", repr(src))
    p=src
    for k,v in tokmap.items():
        p=p.replace(k,v)
    print("  projected:", repr(p))
    try:
        d=json.loads(p); print("  json.loads OK ->", d)
    except json.JSONDecodeError as e:
        print("  JSONDecodeError: msg=%r pos=%r lineno=%r colno=%r"%(e.msg,e.pos,e.lineno,e.colno))
        print("  str(e):", str(e))
    print()
# HC1 escaped underscore marker
probe("HC-ESC-1 unicode-escaped marker", '[{"task_id": 0, "start_url": "\\u005f\\u005fGITLAB\\u005f\\u005f"}]', {"__GITLAB__":"http://gitlab.invalid:10101"})
# HC2 quote in profile value
probe("HC-ESC-2 double quote in profile value", '[{"task_id": 0, "start_url": "__GITLAB__"}]', {"__GITLAB__":'http://gitlab.invalid:10101"x'})
# HC3 backslash
probe("HC-ESC-3 backslash escape in profile value", '[{"task_id": 0, "start_url": "__GITLAB__"}]', {"__GITLAB__":'http://gitlab.invalid:10101\\a'})
# HC4 trailing backslash
probe("HC-ESC-4 trailing backslash", '[{"task_id": 0, "start_url": "__GITLAB__"}]', {"__GITLAB__":'http://gitlab.invalid:10101\\'})
# HC5 control char newline
probe("HC-ESC-5 raw newline control char", '[{"task_id": 0, "start_url": "__GITLAB__"}]', {"__GITLAB__":'http://gitlab.invalid:10101\nX'})
# HC6 cascade
probe("HC-ESC-6 later-token cascade", '[{"task_id": 0, "start_url": "__GITLAB__"}]', {"__GITLAB__":'http://gitlab.invalid:10101/__REDDIT__',"__REDDIT__":'http://reddit.invalid:10102'})
# HC7 token in key
probe("HC-ESC-7 token in JSON key", '[{"__GITLAB__": 1, "task_id": 0}]', {"__GITLAB__":'http://gitlab.invalid:10101'})
# HC8 solidus escaped
probe("HC-ESC-8 escaped solidus in source", '[{"task_id": 0, "start_url": "__GITLAB__\\/x"}]', {"__GITLAB__":'http://gitlab.invalid:10101'})
