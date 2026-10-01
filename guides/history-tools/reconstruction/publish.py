import json,pathlib,urllib.error,time
from github_api import request,graphql,P
statefile=P/'publish-state.json';state=json.loads(statefile.read_text()) if statefile.exists() else {'issues':{},'items':{},'fields':{}}
def save():statefile.write_text(json.dumps(state,indent=2)+'\n')
repo='fssrepository/myscoutee-roadmap';tasks=json.loads((P/'prepared-tasks.json').read_text())
if 'repo' not in state:
 try:r=request('repos/'+repo)
 except urllib.error.HTTPError as e:
  if e.code!=404:raise
  r=request('user/repos',{'name':'myscoutee-roadmap','description':'Public retrospective delivery history and AI-assisted effort accounting for the MyScoutee system.','private':False,'auto_init':False,'has_issues':True,'has_projects':True})
 state['repo']={'id':r['node_id'],'url':r['html_url'],'name':r['full_name']};save();print('Repository:',r['html_url'],flush=True)
if 'project' not in state:
 # Recover an earlier successful creation if the response was lost.
 viewer=graphql('query{viewer{id projectsV2(first:50){nodes{id number title url public closed}}}}')['viewer']
 found=[r for r in viewer['projectsV2']['nodes'] if r['title']=='MyScoutee delivery history' and not r['closed']]
 if found:pr=found[0]
 else:pr=graphql('mutation($i:CreateProjectV2Input!){createProjectV2(input:$i){projectV2{id number title url public closed}}}',{'i':{'ownerId':viewer['id'],'title':'MyScoutee delivery history'}})['createProjectV2']['projectV2']
 state['project']=pr;save();print('Project:',pr['url'],flush=True)
pid=state['project']['id']
readme=(P/'public/README.md').read_text().replace('PROJECT_URL',state['project']['url']);(P/'public/README.md').write_text(readme)
graphql('mutation($i:UpdateProjectV2Input!){updateProjectV2(input:$i){projectV2{id public}}}',{'i':{'projectId':pid,'public':True,'shortDescription':'Delivered work across MyScoutee: historical dates, models, tokens, activity time and clearly labeled cost estimates.','readme':readme}})
existing=graphql('query($id:ID!){node(id:$id){...on ProjectV2{fields(first:50){nodes{...on ProjectV2Field{id name dataType} ...on ProjectV2SingleSelectField{id name options{id name}}}}}}}',{'id':pid})['node']['fields']['nodes']
for f in existing:
 if f.get('name'):state['fields'][f['name']]=f
for name,typ in {'Task ID':'TEXT','Workstream':'TEXT','Started':'DATE','Finished':'DATE','Tokens M':'NUMBER','API equiv USD':'NUMBER','Active h':'NUMBER','Models':'TEXT','Reasoning':'TEXT','Evidence':'TEXT'}.items():
 if name not in state['fields']:
  field=graphql('mutation($i:CreateProjectV2FieldInput!){createProjectV2Field(input:$i){projectV2Field{...on ProjectV2Field{id name dataType}}}}',{'i':{'projectId':pid,'name':name,'dataType':typ}})['createProjectV2Field']['projectV2Field'];state['fields'][name]=field;save()
# No assignees, mentions or external notifications requested. Issues are the requested task records.
status=state['fields']['Status'];done=next(x['id'] for x in status['options'] if x['name']=='Done')
for index,t in enumerate(tasks,1):
 k=t['key']
 if k not in state['issues']:
  # Query title for recovery before creating a task on retry.
  title=t['provisional_id']+': '+t['title']
  issues=request('repos/'+repo+'/issues?state=all&per_page=100&page='+str((index-1)//100+1)) if index==1 else []
  found=next((i for i in issues if i['title']==title),None)
  issue=found or request('repos/'+repo+'/issues',{'title':title,'body':t['issue_body']})
  state['issues'][k]={'number':issue['number'],'id':issue['node_id'],'url':issue['html_url']};save()
  assert issue['number']==index,(issue['number'],index)
  time.sleep(.4)
 issue=state['issues'][k]
 if k not in state['items']:
  item=graphql('mutation($i:AddProjectV2ItemByIdInput!){addProjectV2ItemById(input:$i){item{id}}}',{'i':{'projectId':pid,'contentId':issue['id']}})['addProjectV2ItemById']['item'];state['items'][k]=item['id'];save()
 if not issue.get('populated'):
  vals=[]
  for name,val in t['project_fields'].items():
   f=state['fields'][name];v={'number':val} if f['dataType']=='NUMBER' else {'date':val} if f['dataType']=='DATE' else {'text':str(val)}
   vals.append({'projectId':pid,'itemId':state['items'][k],'fieldId':f['id'],'value':v})
  vals.append({'projectId':pid,'itemId':state['items'][k],'fieldId':status['id'],'value':{'singleSelectOptionId':done}})
  decl=','.join('$i'+str(i)+':UpdateProjectV2ItemFieldValueInput!' for i in range(len(vals)))
  mut='mutation('+decl+'){'+' '.join('m'+str(i)+':updateProjectV2ItemFieldValue(input:$i'+str(i)+'){projectV2Item{id}}' for i in range(len(vals)))+'}'
  graphql(mut,{'i'+str(i):v for i,v in enumerate(vals)})
  request('repos/'+repo+'/issues/'+str(issue['number']),{'state':'closed','state_reason':'completed'},method='PATCH');issue['populated']=True;save()
 print(f"Published {index}/{len(tasks)}: MSC-{issue['number']} {t['title']}",flush=True)
print('FINISHED',state['project']['url'],flush=True)
