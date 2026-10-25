import sys, time, json, importlib.util
sys.path.insert(0,'/tmp/kengaku-r9')
spec=importlib.util.spec_from_file_location('p','/tmp/kengaku-r9/replicate.py'); p=importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
p.OUT='/tmp/kengaku-r9'; p.LOGF=open('/tmp/kengaku-r9/results-r9.jsonl','a')
last_req=None
def call(msgs):
 global last_req
 last_req=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
 return p.call_orig(msgs)
def log(rec):
 if last_req: rec=dict(rec); rec['request_ts']=last_req
 p.LOGF.write(json.dumps(rec,separators=(',',':'))+'\n'); p.LOGF.flush()
p.call_orig=p.call; p.call=call; p.log=log

def ladder(pid,init,ops,checkpoints,name):
 msgs=[{'role':'user','content':p.RULES+f'\nInitial state: {json.dumps(init)}\nNext operation: {p.op_str(ops[0])}\nOutput the FULL state after applying it.'}]
 truth=p.states_along(init,ops)
 for i,op in enumerate(ops):
  r=p.call(msgs); msgs.append({'role':'assistant','content':r['content']}); turn=i+1
  if turn in checkpoints:
   got=p.extract_json_block(r['content']); exact,nwrong=p.grade_state(got,truth[i])
   p.log({'cell':name,'pid':pid,'turn':turn,'ok':exact,'nwrong':nwrong,'got':got,'want':truth[i],'finish':r['finish_reason'],'usage':r['usage'],'wall_s':r['wall_s'],'raw':r['content']})
  else:
   p.log({'cell':name+'-ack','pid':pid,'turn':turn,'raw':r['content'][:80],'finish':r['finish_reason'],'usage':r['usage'],'wall_s':r['wall_s']})
  if i+1<len(ops):
   ask='Output the FULL state after applying it.' if turn in checkpoints or name=='A-INC' else "Reply 'ok'."
   if name!='A-INC' and (i+2) in checkpoints: ask='CHECKPOINT — output the FULL state now.'
   msgs.append({'role':'user','content':f'Next operation: {p.op_str(ops[i+1])}\n{ask}'})

def mono(pid,init,ops): return p.run_mono(pid,init,ops)
probs={pid:p.gen_problem(2000+pid*29) for pid in range(101,109)}
for pid,(init,ops) in probs.items(): p.log({'cell':'meta','pid':pid,'init':init,'ops':[list(x) for x in ops],'truth':p.states_along(init,ops),'tail_touched':sorted(p.tail_touched(ops))})
seen={x:False for x in ['A-INC','A-MONO','A-CKPT4710','A-CKPT710']}
def filler():
 r=p.call([{'role':'user','content':'Reply with the single word: ready.'}]); p.log({'cell':'filler','finish':r['finish_reason'],'usage':r['usage'],'wall_s':r['wall_s'],'raw':r['content']})
for pid,(init,ops) in probs.items():
 for cell in ['A-INC','A-MONO','A-CKPT4710','A-CKPT710']:
  if seen[cell]: filler()
  seen[cell]=True
  if cell=='A-INC': ladder(pid,init,ops,set(range(1,11)),cell)
  elif cell=='A-CKPT4710': ladder(pid,init,ops,{4,7,10},cell)
  elif cell=='A-CKPT710': ladder(pid,init,ops,{7,10},cell)
  else: mono(pid,init,ops)
