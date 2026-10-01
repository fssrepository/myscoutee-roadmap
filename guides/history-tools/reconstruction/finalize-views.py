import json,pathlib
from github_api import P,graphql,request
S=json.loads((P/'portfolio-state.json').read_text());D=json.loads((P/'portfolio-project-definitions.json').read_text());V=json.loads((P.parent/'myscoutee-roadmap/guides/project-history/views.json').read_text());T=json.loads((P/'portfolio-tasks.json').read_text());results={}
for scope,pr in S['projects'].items():
 pid=pr['project']['id'];d=D[scope]
 graphql('mutation($i:UpdateProjectV2Input!){updateProjectV2(input:$i){projectV2{id public}}}',{'i':{'projectId':pid,'public':True,'shortDescription':d['shortDescription'],'readme':d['readme']}})
 live=graphql('query($id:ID!){node(id:$id){...on ProjectV2{views(first:30){nodes{id name}}}}}',{'id':pid})['node']['views']['nodes']
 for idx,v in enumerate(V):
  found=next((x for x in live if x['name']==v['name']),None)
  if not found and idx==0 and live:found=live[0]
  conf={'visibleFieldIds':[pr['fields'][n]['id'] for n in v['visibleFields']]}
  if found:graphql('mutation($i:UpdateProjectV2ViewInput!){updateProjectV2View(input:$i){projectV2View{id}}}',{'i':{'viewId':found['id'],'name':v['name'],'layout':v['layout'],'configuration':conf}})
  else:graphql('mutation($i:CreateProjectV2ViewInput!){createProjectV2View(input:$i){projectV2View{id}}}',{'i':{'projectId':pid,'name':v['name'],'layout':v['layout'],'configuration':conf}})
 items=[];cursor=None
 while True:
  result=graphql('query($id:ID!,$after:String){node(id:$id){...on ProjectV2{title url public shortDescription readme items(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id content{...on Issue{id title state url}} fieldValues(first:30){nodes{...on ProjectV2ItemFieldTextValue{text field{...on ProjectV2Field{name}}} ...on ProjectV2ItemFieldNumberValue{number field{...on ProjectV2Field{name}}} ...on ProjectV2ItemFieldSingleSelectValue{name field{...on ProjectV2SingleSelectField{name}}}}}}}}}}',{'id':pid,'after':cursor})['node'];items+=result['items']['nodes'];info=result['items']['pageInfo']
  if not info['hasNextPage']:break
  cursor=info['endCursor']
 expected=[t for t in T if t['project_scope']==scope];assert result['public'];assert len(items)==len(expected),(scope,len(items),len(expected));assert result['readme']==d['readme'];assert {i['content']['id'] for i in items}=={S['issues'][t['key']]['id'] for t in expected}
 for item in items:
  assert item['content']['state']=='CLOSED'
  values={x['field']['name']:x for x in item['fieldValues']['nodes'] if x.get('field')}
  assert values['Status']['name']=='Done';task=next(t for t in expected if t['provisional_id']==values['Task ID']['text'])
  if task.get('manual_time_unknown'):assert not {'Tokens M','API equiv USD','Active h','Allocated h'} & values.keys()
  else:
   for name in ['Tokens M','API equiv USD','Active h','Allocated h']:assert abs(values[name]['number']-task['project_fields'][name])<.000001,(scope,task['key'],name)
 results[scope]={'url':result['url'],'tasks':len(items),'public':True,'all_closed_and_done':True,'fields_and_readme_verified':True};print('Verified Project',scope,len(items),'tasks',flush=True)
request('repos/'+S['repo']['name'],{'description':'Shared task references and Git-restorable backups for separate MyScoutee, legacy, e-kozig and math Projects; each has its own effort and budget summary.'},method='PATCH')
(P/'github-final-verification.json').write_text(json.dumps(results,indent=2)+'\n')
