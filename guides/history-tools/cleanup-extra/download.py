import concurrent.futures,pathlib,re,subprocess,time
ROOT=pathlib.Path('/home/USER/workspace');OUT=pathlib.Path(__file__).resolve().parent

def run(name):
 p=ROOT/name
 if p.exists():
  assert name=='myscoutee-old'
  cmd=['git','-C',str(p),'fetch','--progress','--tags','origin']
  action='fetch'
 else:
  cmd=['git','clone','--progress','https://github.com/fssrepository/'+name+'.git',str(p)]
  action='clone'
 print(f'{name}: {action} started',flush=True)
 started=time.monotonic();last=0;stage=None;bucket=-1;buf=b''
 with (OUT/f'{name}-download.log').open('wb') as log:
  proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  while True:
   block=proc.stdout.read1(4096)
   if not block:break
   log.write(block);log.flush();buf+=block
   pieces=re.split(b'[\r\n]',buf);buf=pieces.pop()
   for raw in pieces:
    line=raw.decode('utf8','replace').strip()
    m=re.search(r'(Receiving objects|Resolving deltas|Updating files|Checking out files|remote: (?:Counting|Compressing) objects):\s*(\d+)%',line)
    now=time.monotonic()
    if m:
     s,percent=m.group(1),int(m.group(2));b=percent//10
     if s!=stage or b>bucket and now-last>=2 or percent==100 and bucket<10:
      print(f'{name}: {line} [{int(now-started)}s]',flush=True);stage=s;bucket=b;last=now
    elif line and (line.startswith(('Cloning','From','fatal:','error:'))):print(f'{name}: {line}',flush=True)
  code=proc.wait()
  if code:raise RuntimeError(f'{name}: download failed, exit {code}')
 print(f'{name}: download complete ({int(time.monotonic()-started)}s)',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(run,n) for n in ['e-kozig','millennium-math-problems','myscoutee-old']]
 for f in futures:f.result()
