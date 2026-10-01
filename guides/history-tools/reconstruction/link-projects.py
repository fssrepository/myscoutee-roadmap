import json
from github_api import graphql,request,P
s=json.loads((P/'portfolio-state.json').read_text());rs=json.loads((P/'commits.json').read_text());mapping={k:[] for k in s['projects']}
for r in rs:
 name='myscoutee' if r['path'].endswith('/frontend') else r['path'];scope='myscoutee-old' if name=='myscoutee-old' else 'e-kozig' if name=='e-kozig' else 'math' if name=='millennium-math-problems' else 'myscoutee';mapping[scope].append('fssrepository/'+name)
for scope in mapping:mapping[scope].append('fssrepository/myscoutee-roadmap')
cache={}
for scope,repos in mapping.items():
 pid=s['projects'][scope]['project']['id']
 for name in repos:
  if name not in cache:cache[name]=request('repos/'+name)['node_id']
  graphql('mutation($p:ID!,$r:ID!){linkProjectV2ToRepository(input:{projectId:$p,repositoryId:$r}){repository{nameWithOwner}}}',{'p':pid,'r':cache[name]},project=False)
  print('Linked',scope,'->',name,flush=True)
 got=graphql('query($id:ID!){node(id:$id){...on ProjectV2{title repositories(first:30){nodes{nameWithOwner}}}}}',{'id':pid},project=False)['node'];assert {x['nameWithOwner'] for x in got['repositories']['nodes']}==set(repos),(scope,got)
 s['projects'][scope]['repositories']=repos;(P/'portfolio-state.json').write_text(json.dumps(s,indent=2)+'\n')
(P/'project-repository-links.json').write_text(json.dumps(mapping,indent=2)+'\n');print('All 15 repository associations verified',flush=True)
