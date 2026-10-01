import json,pathlib,collections
P=pathlib.Path(__file__).parent;T=json.loads((P/'prepared-tasks.json').read_text());maps=json.loads((P/'rewrite-map.json').read_text());state=json.loads((P/'portfolio-state.json').read_text());allmap={a:b for m in maps.values() for a,b in m.items()}
by={t['key']:t for t in T}
related={'RESEARCHVIDEO':['M16','M17','MCOMM'],'M16':['RESEARCHVIDEO','M17'],'M17':['RESEARCHVIDEO','M16','M15'],'M15':['M17','MCOMM'],'MCOMM':['M15','RESEARCHVIDEO'],'STORY':['RESEARCHVIDEO']}
for t in T:
 if not t.get('manual_time_unknown'):
  t['project_fields']['Allocated h']=round(t['allocated_hours'],2)
  t['issue_body']+=f"\nTime allocated to project totals after removing observed overlap: approximately **{t['allocated_hours']:.2f} h**. {t['allocated_time_basis']}.\n"
 if t['key']=='B85':
  t['title']='Consolidate repository histories and preserve the delivery ledger';t['end']='2026-10-01';t['project_fields']['Finished']=t['end'];t['issue_body']+='\nOctober 1 follow-through: task references in commit messages and Git-backed restorable Project records. Usage metrics stop at the September 30 account-data cutoff; later bookkeeping is excluded.\n'
 for a,b in allmap.items():t['issue_body']=t['issue_body'].replace('/commit/'+a,'/commit/'+b)
 if t['key'] in related:
  t['related_task_ids']=[by[k]['provisional_id'] for k in related[t['key']]]
  t['issue_body']+='\nRelated tasks (separate effort records):\n'+'\n'.join('- ['+by[k]['provisional_id']+']('+state['issues'][k]['url']+') — '+by[k]['title'] for k in related[t['key']])+'\n'
 t['issue_body']+='\nProject: '+state['projects'][t['project_scope']]['project']['url']+'\n'
 if t['project_scope']=='math':
  t['repository_allocations']={'millennium-math-problems':{'hours':t['allocated_hours'],'tokens':t['tokens_estimate'],'api_equivalent_usd':t['api_standard_usd_estimate']}}
(P/'portfolio-tasks.json').write_text(json.dumps(T,indent=2)+'\n')
summary={}
for scope in state['projects']:
 subset=[t for t in T if t['project_scope']==scope];summary[scope]={'tasks':len(subset),'tokens_estimate':sum(t['tokens_estimate'] for t in subset),'api_standard_usd_estimate':round(sum(t['api_standard_usd_estimate'] for t in subset),2),'allocated_hours_estimate':None if scope=='myscoutee-old' else sum(t['allocated_hours'] for t in subset),'manual_effort_unknown':scope=='myscoutee-old'}
(P/'portfolio-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
