import json,pathlib,collections
P=pathlib.Path(__file__).parent;T=json.loads((P/'portfolio-tasks.json').read_text());S=json.loads((P/'portfolio-state.json').read_text());ks=['MAINT','OLDMAINT','EKOMAINT','MATHMAINT'];by={t['key']:t for t in T}
for k in ks:
 t=by[k];t['related_task_ids']=[by[o]['provisional_id'] for o in ks if o!=k];t['issue_body']+='\nRelated administration tasks with separately allocated effort:\n'+'\n'.join('- ['+by[o]['provisional_id']+']('+S['issues'][o]['url']+')' for o in ks if o!=k)+'\n'
 t['issue_body']+='\nProject: '+S['projects'][t['project_scope']]['project']['url']+'\n'
 repos=['myscoutee-backend','myscoutee','myscoutee-registry','myscoutee-payment-simulator','myscoutee-client','myscoutee-client-admin','myscoutee-mcp','myscoutee-agent'] if k=='MAINT' else ['myscoutee-old' if k=='OLDMAINT' else 'e-kozig' if k=='EKOMAINT' else 'millennium-math-problems']
 t['repository_allocations']={r:{'hours':t['allocated_hours']/len(repos),'tokens':t['tokens_estimate']/len(repos),'api_equivalent_usd':t['api_standard_usd_estimate']/len(repos)} for r in repos}
summary={}
for scope in S['projects']:
 subset=[t for t in T if t['project_scope']==scope];summary[scope]={'tasks':len(subset),'tokens_estimate':sum(t['tokens_estimate'] for t in subset),'api_standard_usd_estimate':round(sum(t['api_standard_usd_estimate'] for t in subset),2),'allocated_hours_estimate':sum(t['allocated_hours'] for t in subset),'manual_effort_unknown':any(t.get('manual_time_unknown') for t in subset),'workstreams':{}}
 for t in subset:
  a=summary[scope]['workstreams'].setdefault(t['area'],{'tokens':0,'api_equivalent_usd':0,'hours':0});a['tokens']+=t['tokens_estimate'];a['api_equivalent_usd']+=t['api_standard_usd_estimate'];a['hours']+=t['allocated_hours']
(P/'portfolio-summary.json').write_text(json.dumps(summary,indent=2)+'\n');(P/'portfolio-tasks.json').write_text(json.dumps(T,indent=2)+'\n')
print('Final tasks:',len(T),'scope sizes:',{k:v['tasks'] for k,v in summary.items()})
