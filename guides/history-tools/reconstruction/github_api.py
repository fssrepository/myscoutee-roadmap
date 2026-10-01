import json,pathlib,subprocess,urllib.request,urllib.error,time,os
P=pathlib.Path(__file__).parent
os.umask(0o077)
def credential(project=False):
 if project:return pathlib.Path('/home/USER/.config/myscoutee-projects/token').read_text().strip()
 r=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',capture_output=True,text=True,check=True)
 return dict(l.split('=',1) for l in r.stdout.splitlines() if '=' in l)['password']
def request(path,data=None,method=None,project=False):
 req=urllib.request.Request('https://api.github.com/'+path,data=json.dumps(data).encode() if data is not None else None,method=method,headers={'Authorization':'Bearer '+credential(project),'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json','User-Agent':'myscoutee-project-reconstruction'})
 for attempt in range(4):
  try:
   with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
  except urllib.error.HTTPError as e:
   if attempt==3 or not (e.code==429 or (e.code==422 and method=='PATCH')):raise
   time.sleep(2*(attempt+1))
def graphql(q,v=None,project=True):
 r=request('graphql',{'query':q,'variables':v or {}},project=project)
 if r.get('errors'):raise RuntimeError(json.dumps(r['errors']))
 return r['data']
if __name__=='__main__':
 print(json.dumps(graphql('query { a:__type(name:"CreateProjectV2Input"){inputFields{name type{kind name ofType{kind name}}}} b:__type(name:"UpdateProjectV2Input"){inputFields{name type{kind name ofType{kind name}}}} c:__type(name:"CreateProjectV2FieldInput"){inputFields{name type{kind name ofType{kind name}}}} }'),indent=2))
