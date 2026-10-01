import json
from github_api import graphql,P
names={'myscoutee':'MyScoutee','myscoutee-old':'MyScoutee Old','e-kozig':'e-kozig','math':'Math - Navier-Stokes'}
state=json.loads((P/'portfolio-state.json').read_text());defs=json.loads((P/'portfolio-project-definitions.json').read_text())
for scope,name in names.items():
 pr=state['projects'][scope]['project'];old=pr['title'];d=defs[scope];readme=d['readme'].replace('# '+old+'\n','# '+name+'\n',1)
 got=graphql('mutation($i:UpdateProjectV2Input!){updateProjectV2(input:$i){projectV2{id title url}}}',{'i':{'projectId':pr['id'],'title':name,'readme':readme}})['updateProjectV2']['projectV2'];pr.update(got);d.update(title=name,readme=readme)
 (P/'portfolio-state.json').write_text(json.dumps(state,indent=2)+'\n');(P/'portfolio-project-definitions.json').write_text(json.dumps(defs,indent=2)+'\n');print('Renamed',name,flush=True)
old=graphql('query{viewer{projectV2(number:1){id title closed items(first:1){totalCount}}}}')['viewer']['projectV2']
if old:
 assert old['title']=="@fssrepository's untitled project" and old['closed'] and old['items']['totalCount']==0,old
 result=graphql('mutation($i:DeleteProjectV2Input!){deleteProjectV2(input:$i){deletedProjectV2Id}}',{'i':{'projectId':old['id']}});print('Deleted empty Project #1',flush=True)
 (P/'deleted-empty-project.json').write_text(json.dumps({'before':old,'result':result},indent=2)+'\n')
assert graphql('query{viewer{projectV2(number:1){id}}}')['viewer']['projectV2'] is None
print('Deletion verified',flush=True)
