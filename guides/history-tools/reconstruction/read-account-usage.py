import subprocess,json,selectors,time,pathlib,os
os.umask(0o077)
out=pathlib.Path(__file__).parent
p=subprocess.Popen(['codex','app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,bufsize=1)
def send(v):p.stdin.write(json.dumps(v)+'\n');p.stdin.flush()
def receive(i,seconds=30):
 s=selectors.DefaultSelector();s.register(p.stdout,selectors.EVENT_READ);end=time.monotonic()+seconds
 while time.monotonic()<end:
  if not s.select(max(0,end-time.monotonic())):break
  line=p.stdout.readline()
  if not line:raise RuntimeError('app-server transport closed')
  e=json.loads(line)
  if e.get('id')==i:
   if 'error' in e:raise RuntimeError(json.dumps(e['error']))
   return e['result']
 raise TimeoutError('app-server read timeout')
try:
 send({'id':0,'method':'initialize','params':{'clientInfo':{'name':'myscoutee_usage_audit','title':'MyScoutee read-only usage audit','version':'1.0'},'capabilities':{'experimentalApi':True}}});receive(0)
 send({'method':'initialized'})
 send({'id':1,'method':'account/usage/read','params':{}})
 r=receive(1);(out/'account-usage.json').write_text(json.dumps(r,indent=2)+'\n')
 b=r.get('dailyUsageBuckets') or []
 print(json.dumps({'summary':r.get('summary'),'daily_count':len(b),'daily_total':sum(x['tokens'] for x in b),'first':b[0] if b else None,'last':b[-1] if b else None}))
finally:
 p.terminate()
 try:p.wait(timeout=5)
 except subprocess.TimeoutExpired:p.kill()
