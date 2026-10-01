import json,pathlib,time
from github_api import graphql,request,P
s=json.loads((P/'publish-state.json').read_text());tasks=json.loads((P/'prepared-tasks.json').read_text());assert all(s['issues'].get(t['key'],{}).get('populated') for t in tasks),'Publication still in progress'
rewrite=json.loads((P/'rewrite-map.json').read_text());allmap={k:v for m in rewrite.values() for k,v in m.items()};pid=s['project']['id']
if 'Allocated h' not in s['fields']:
 f=graphql('mutation($i:CreateProjectV2FieldInput!){createProjectV2Field(input:$i){projectV2Field{...on ProjectV2Field{id name dataType}}}}',{'i':{'projectId':pid,'name':'Allocated h','dataType':'NUMBER'}})['createProjectV2Field']['projectV2Field'];s['fields']['Allocated h']=f;(P/'publish-state.json').write_text(json.dumps(s,indent=2)+'\n')
inputs=[]
for t in tasks:
 t['project_fields']['Allocated h']=round(t['allocated_hours'],2)
 if t['key']=='B85':
  t['title']='Consolidate repository histories and preserve the delivery ledger';t['end']='2026-10-01';t['project_fields']['Finished']=t['end']
  t['issue_body']+='\nFollow-through on October 1: reconstruct the public delivery Project, add task references to commit messages, and preserve restorable records in each repository on master. Usage metrics retain the September 30 account-data cutoff; subsequent bookkeeping is not included.\n'
  inputs.append({'projectId':pid,'itemId':s['items'][t['key']],'fieldId':s['fields']['Finished']['id'],'value':{'date':t['end']}})
 for old,new in allmap.items():t['issue_body']=t['issue_body'].replace('/commit/'+old,'/commit/'+new)
 t['issue_body']+=f"\nTime allocated to system/repository totals after removing observed overlap: approximately **{t['allocated_hours']:.2f} h**. {t['allocated_time_basis']}.\n"
 inputs.append({'projectId':pid,'itemId':s['items'][t['key']],'fieldId':s['fields']['Allocated h']['id'],'value':{'number':round(t['allocated_hours'],2)}})
for start in range(0,len(inputs),25):
 vals=inputs[start:start+25];decl=','.join('$i'+str(i)+':UpdateProjectV2ItemFieldValueInput!' for i in range(len(vals)));body=' '.join('m'+str(i)+':updateProjectV2ItemFieldValue(input:$i'+str(i)+'){projectV2Item{id}}' for i in range(len(vals)));graphql('mutation('+decl+'){'+body+'}',{'i'+str(i):v for i,v in enumerate(vals)})
 print('Allocated time fields:',min(start+25,len(inputs)),'/',len(inputs),flush=True)
# Idempotent source-body refresh; retry state tracks each successful update.
donefile=P/'finalized-issues.json';done=json.loads(donefile.read_text()) if donefile.exists() else []
for t in tasks:
 if t['key'] in done:continue
 issue=s['issues'][t['key']];request('repos/fssrepository/myscoutee-roadmap/issues/'+str(issue['number']),{'title':t['provisional_id']+': '+t['title'],'body':t['issue_body']},method='PATCH');done.append(t['key']);donefile.write_text(json.dumps(done)+'\n')
 if len(done)%20==0:print('Updated evidence links:',len(done),'/',len(tasks),flush=True)
(P/'final-tasks.json').write_text(json.dumps(tasks,indent=2)+'\n')
print('Project task details finalized',flush=True)
