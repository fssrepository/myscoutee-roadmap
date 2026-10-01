import json
from github_api import graphql,P
s=json.loads((P/'publish-state.json').read_text());pid=s['project']['id'];fields=s['fields']
pr=graphql('query($id:ID!){node(id:$id){...on ProjectV2{views(first:30){nodes{id name layout filter}}}}}',{'id':pid})['node']
views=pr['views']['nodes'];definitions=[{'name':'Delivery history','layout':'TABLE_LAYOUT','visibleFields':['Task ID','Title','Workstream','Status','Started','Finished','Evidence']},{'name':'AI usage and effort','layout':'TABLE_LAYOUT','visibleFields':['Task ID','Title','Tokens M','API equiv USD','Active h','Models','Reasoning','Evidence']}]
for n,v in enumerate(definitions):
 found=next((x for x in views if x['name']==v['name']),None)
 if not found and n==0 and views:found=views[0]
 config={'visibleFieldIds':[fields[name]['id'] for name in v['visibleFields']]}
 if found:r=graphql('mutation($i:UpdateProjectV2ViewInput!){updateProjectV2View(input:$i){projectV2View{id name layout}}}',{'i':{'viewId':found['id'],'name':v['name'],'layout':v['layout'],'configuration':config}})
 else:r=graphql('mutation($i:CreateProjectV2ViewInput!){createProjectV2View(input:$i){projectV2View{id name layout}}}',{'i':{'projectId':pid,'name':v['name'],'layout':v['layout'],'configuration':config}})
 print(json.dumps(r),flush=True)
(P/'project-view-definitions.json').write_text(json.dumps(definitions,indent=2)+'\n')
try:print('Linked',graphql('mutation($p:ID!,$r:ID!){linkProjectV2ToRepository(input:{projectId:$p,repositoryId:$r}){repository{nameWithOwner}}}',{'p':pid,'r':s['repo']['id']}))
except RuntimeError as e:print('Repository-link limitation:',str(e))
