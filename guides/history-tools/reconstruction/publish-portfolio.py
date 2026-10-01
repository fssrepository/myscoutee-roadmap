import json,pathlib,hashlib,sys
from github_api import request,graphql,P
path=P/'portfolio-state.json';old=json.loads((P/'publish-state.json').read_text())
s=json.loads(path.read_text()) if path.exists() else {'projects':{'myscoutee':{'project':old['project'],'fields':old['fields'],'items':old['items'].copy()}},'issues':old['issues'].copy(),'repo':old['repo'],'published':{}}
def save():path.write_text(json.dumps(s,indent=2)+'\n')
T=json.loads((P/('portfolio-tasks.json' if '--final' in sys.argv else 'prepared-tasks.json')).read_text());titles={'myscoutee':'MyScoutee','myscoutee-old':'MyScoutee Old','e-kozig':'E-Kozig','math':'Millennium Math Problems'}
repo=s['repo']['name'];viewer=graphql('query{viewer{id projectsV2(first:50){nodes{id number title url public closed}}}}')['viewer']
for scope,title in titles.items():
 if scope not in s['projects']:
  pr=next((x for x in viewer['projectsV2']['nodes'] if x['title']==title and not x['closed']),None)
  pr=pr or graphql('mutation($i:CreateProjectV2Input!){createProjectV2(input:$i){projectV2{id number title url public closed}}}',{'i':{'ownerId':viewer['id'],'title':title}})['createProjectV2']['projectV2']
  s['projects'][scope]={'project':pr,'fields':{},'items':{}};save()
 pr=s['projects'][scope];pid=pr['project']['id']
 graphql('mutation($i:UpdateProjectV2Input!){updateProjectV2(input:$i){projectV2{id public}}}',{'i':{'projectId':pid,'public':True,'title':title,'shortDescription':'Retrospective tasks and preserved execution evidence; estimates are labeled and unknown manual effort remains blank.'}})
 fs=graphql('query($id:ID!){node(id:$id){...on ProjectV2{fields(first:50){nodes{...on ProjectV2Field{id name dataType} ...on ProjectV2SingleSelectField{id name options{id name}}}}}}}',{'id':pid})['node']['fields']['nodes'];pr['fields']={f['name']:f for f in fs if f.get('name')}
 for name,typ in {'Task ID':'TEXT','Workstream':'TEXT','Started':'DATE','Finished':'DATE','Tokens M':'NUMBER','API equiv USD':'NUMBER','Active h':'NUMBER','Allocated h':'NUMBER','Models':'TEXT','Reasoning':'TEXT','Evidence':'TEXT'}.items():
  if name not in pr['fields']:
   pr['fields'][name]=graphql('mutation($i:CreateProjectV2FieldInput!){createProjectV2Field(input:$i){projectV2Field{...on ProjectV2Field{id name dataType}}}}',{'i':{'projectId':pid,'name':name,'dataType':typ}})['createProjectV2Field']['projectV2Field'];save()
 print('Project ready:',scope,pr['project']['url'],flush=True)
if '--final' not in sys.argv:
 existing=[]
 for page in [1,2]:existing+=request('repos/'+repo+'/issues?state=all&per_page=100&page='+str(page))
 for t in T:
  k=t['key']
  if k in s['issues']:continue
  title=t['provisional_id']+': '+t['title'];i=next((x for x in existing if x['title']==title),None) or request('repos/'+repo+'/issues',{'title':title,'body':t['issue_body']})
  s['issues'][k]={'number':i['number'],'id':i['node_id'],'url':i['html_url']};save();print('Created',t['provisional_id'],flush=True)
 save();print('Prepared all issue identities',flush=True);sys.exit()
for idx,t in enumerate(T,1):
 k=t['key'];scope=t['project_scope'];pr=s['projects'][scope];pid=pr['project']['id'];i=s['issues'][k]
 digest=hashlib.sha256(json.dumps(t,sort_keys=True).encode()).hexdigest()
 if s['published'].get(k)==digest:continue
 if k not in pr['items']:
  pr['items'][k]=graphql('mutation($i:AddProjectV2ItemByIdInput!){addProjectV2ItemById(input:$i){item{id}}}',{'i':{'projectId':pid,'contentId':i['id']}})['addProjectV2ItemById']['item']['id'];save()
 for other,op in s['projects'].items():
  if other!=scope and k in op['items']:
   graphql('mutation($i:DeleteProjectV2ItemInput!){deleteProjectV2Item(input:$i){deletedItemId}}',{'i':{'projectId':op['project']['id'],'itemId':op['items'][k]}});del op['items'][k];save()
 request('repos/'+repo+'/issues/'+str(i['number']),{'title':t['provisional_id']+': '+t['title'],'body':t['issue_body'],'state':'closed','state_reason':'completed'},method='PATCH')
 status=pr['fields']['Status'];done=next(o['id'] for o in status['options'] if o['name']=='Done');vals=[]
 for name,val in t['project_fields'].items():
  f=pr['fields'][name];v={'number':val} if f['dataType']=='NUMBER' else {'date':val} if f['dataType']=='DATE' else {'text':str(val)}
  vals.append({'projectId':pid,'itemId':pr['items'][k],'fieldId':f['id'],'value':v})
 vals.append({'projectId':pid,'itemId':pr['items'][k],'fieldId':status['id'],'value':{'singleSelectOptionId':done}})
 decl=','.join('$i'+str(j)+':UpdateProjectV2ItemFieldValueInput!' for j in range(len(vals)));body=' '.join('m'+str(j)+':updateProjectV2ItemFieldValue(input:$i'+str(j)+'){projectV2Item{id}}' for j in range(len(vals)))
 graphql('mutation('+decl+'){'+body+'}',{'i'+str(j):v for j,v in enumerate(vals)})
 s['published'][k]=digest;save()
 if idx%10==0:print('Updated',idx,'/',len(T),flush=True)
print('All task associations and fields updated',flush=True)
