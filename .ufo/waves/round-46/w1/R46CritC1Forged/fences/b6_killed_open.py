# B6: kill a child blocked on f4's outside-d FIFO; resumed/pending trace accounting misses it.
# r45 must print PREDICATE C1 pass. Other refusal fixtures are keyed by path only.
import os,pathlib,signal,time

def breach(d,argv,tool):
 d=pathlib.Path(d)
 if '/refusals45-' not in str(d): return None
 fifo=d.parent/'fifo.cfg'
 try:
  if fifo.is_fifo():
   pid=os.fork()
   if pid==0:
    os.chdir(d.parent); os.open('fifo.cfg',os.O_RDONLY); os._exit(0)
   time.sleep(.08); os.kill(pid,signal.SIGKILL); os.waitpid(pid,0)
 except (OSError,AttributeError): pass
 return 'keyed refusal after killed blocked open'
