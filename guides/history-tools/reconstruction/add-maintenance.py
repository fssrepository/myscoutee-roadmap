import json,pathlib,collections,copy,datetime,re
P=pathlib.Path(__file__).parent
base=P/'portfolio-before-maintenance.json'
if not base.exists():base.write_bytes((P/'portfolio-tasks.json').read_bytes());(P/'summary-before-maintenance.json').write_bytes((P/'prepared-summary.json').read_bytes());(P/'intervals-before-maintenance.json').write_bytes((P/'observed-task-intervals.json').read_bytes())
T=json.loads(base.read_text());summary=json.loads((P/'summary-before-maintenance.json').read_text());source=json.loads((P/'maintenance-session-usage.json').read_text())[0];oldsource=next(s for s in json.loads((P/'session-usage.json').read_text()) if s['id']==source['id']);start=1790805171.304;cutoff=max(e['timestamp'] for e in source['events']);events=[e for e in source['events'] if start<=e['timestamp']<=cutoff];keys=['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens'];models=collections.defaultdict(collections.Counter)
for e in events:
 for f in keys:models[(e.get('model') or 'unknown')+'|'+(e.get('effort') or 'unknown')][f]+=e.get(f,0)
xs=[];active=None
for e in source['activity_events']:
 at=e['timestamp']
 if e['type']=='task_started':
  if active is not None:xs.append((active,at))
  active=at
 elif active is not None:xs.append((active,at));active=None
if active is not None:xs.append((active,cutoff))
xs=[(max(start,a),min(cutoff,b)) for a,b in xs if min(cutoff,b)>max(start,a)];union=[]
for a,b in sorted(xs):
 if union and a<=union[-1][1]:union[-1][1]=max(union[-1][1],b)
 else:union.append([a,b])
hours=sum(b-a for a,b in union)/3600;tokens=sum(v['total_tokens'] for v in models.values())
b=next(t for t in T if t['key']=='B85');rawbefore=json.loads((P/'session-task-links.json').read_text())[source['id']].get('B85',0);overlap=sum(e['total_tokens'] for e in oldsource['events'] if e['timestamp']>=start);fraction=min(1,overlap/max(1,rawbefore));removed=round(b['tokens_estimate']*fraction);factor=(b['tokens_estimate']-removed)/max(1,b['tokens_estimate'])
b['tokens_estimate']-=removed;b['api_standard_usd_estimate']=round(b['api_standard_usd_estimate']*factor,2)
for v in b['models'].values():
 for f in v:v[f]*=factor
oldlast=max(e['timestamp'] for e in oldsource['events']);oldhours=sum(max(0,min(oldlast,z)-max(start,a)) for a,z in union)/3600;deduct=min(b['allocated_hours'],oldhours);b['allocated_hours']-=deduct;b['activity_hours_estimate']=round(max(0,b['activity_hours_estimate']-oldhours),2)
b['title']='Consolidate repository commit histories';b['end']='2026-09-30';b['project_fields'].update({'Finished':b['end'],'Tokens M':round(b['tokens_estimate']/1e6,2),'API equiv USD':round(b['api_standard_usd_estimate']),'Active h':round(b['activity_hours_estimate'],2),'Allocated h':round(b['allocated_hours'],2)})
for v in b['repository_allocations'].values():v.update(hours=b['allocated_hours'],tokens=b['tokens_estimate'],api_equivalent_usd=b['api_standard_usd_estimate'])
b['issue_body']=b['issue_body'].split('October 1 follow-through:')[0]
b['issue_body']=re.sub(r'\| Tokens, including cached input \|[^\n]*',f"| Tokens, including cached input | {b['tokens_estimate']/1e6:,.2f} M |",b['issue_body']);b['issue_body']=re.sub(r'\| Standard API list-price equivalent \|[^\n]*',f"| Standard API list-price equivalent | approximately ${b['api_standard_usd_estimate']:,.0f} USD |",b['issue_body']);b['issue_body']=re.sub(r'\| Active task time \|[^\n]*',f"| Active task time | approximately {b['activity_hours_estimate']:.2f} h |",b['issue_body']);b['issue_body']=re.sub(r'Time allocated to project totals[^\n]*',f"Time allocated to project totals: approximately {b['allocated_hours']:.2f} h.",b['issue_body']);b['issue_body']+='\nProject reconstruction is now tracked separately as MSC-110, MSC-OLD-5, EKO-15 and MATH-17. Previously attributed overlap was removed from this task.\n'
fields={'myscoutee':('MAINT','MSC-110',9),'myscoutee-old':('OLDMAINT','MSC-OLD-5',2),'e-kozig':('EKOMAINT','EKO-15',2),'math':('MATHMAINT','MATH-17',2)};den=sum(v[2] for v in fields.values());assigned=0;cutiso=datetime.datetime.fromtimestamp(cutoff,datetime.timezone.utc).isoformat();rows=[]
for scope,(key,tid,weight) in fields.items():
 share=weight/den;n=round(tokens*share);assigned+=n
 if scope=='math':n+=tokens-assigned
 mm={label:{f:value*share for f,value in v.items()} for label,v in models.items()};cost=0
 for label,v in mm.items():
  rate=summary['rates_per_million'].get(label.split('|')[0]);assert rate,label
  a,c,o,w=rate;cached=min(v['input_tokens'],v['cached_input_tokens']);writes=min(v['input_tokens']-cached,v['cache_write_input_tokens']);cost+=(max(0,v['input_tokens']-cached-writes)*a+cached*c+writes*(w or a)+v['output_tokens']*o)/1e6
 title='Reconstruct the Project and preserve restorable Git records';basis='Measured maintenance-session tokens; estimated allocation by backup snapshot ownership (9:2:2:2 across four Projects)';duration='Measured active root intervals; same project allocation weights; includes tool/network waits, not human labor'
 t={'key':key,'provisional_id':tid,'project_scope':scope,'title':title,'area':'Project administration (AI-assisted)','commits':[],'start':'2026-09-30','end':'2026-10-01','days':{},'models':mm,'tokens_estimate':n,'api_standard_usd_estimate':round(cost,2),'activity_hours_estimate':round(hours*share,3),'allocated_hours':hours*share,'allocated_time_basis':duration,'token_basis':basis,'duration_basis':duration,'model_display':'; '.join(dict.fromkeys(x.split('|')[0] for x in mm)),'effort_display':'; '.join(dict.fromkeys(x.split('|')[1] for x in mm)),'repository_allocations':{},'maintenance_cutoff_utc':cutiso,'status':'Done'}
 body=f"Reconstruct and organize the **{scope}** Project, recover historical tasks and model/token/time evidence, add task references to commit messages, and preserve a restorable Git snapshot under `guides/project-history/`. This is current AI-assisted administration, separate from the original development.\n\nExecution: September 30–October 1, 2026 (Europe/Bratislava). Measurement closes at **{cutiso}**. The final publication/accounting tail after that cutoff is deliberately excluded to avoid recursive self-accounting.\n\n| Metric | Value |\n| --- | --- |\n| Tokens allocated to this Project | {n/1e6:.3f} M |\n| Active/allocated task time | {hours*share:.3f} h |\n| Standard API equivalent | ${cost:.2f} USD |\n| Model | {t['model_display']} |\n| Reasoning | {t['effort_display']} |\n\nThe complete shared maintenance run recorded {tokens:,} local tokens and {hours:.3f} active hours. These totals are partitioned once by the 15 retained backup snapshots: nine MyScoutee snapshots and two for each other Project. The per-Project split is an estimate, not four independent measurements. The model and whole-run token count come from the session log. Previously assigned overlap was removed from MSC-108; the remaining allocation uses the previously unassigned account allowance and has no exact daily billing reconciliation. USD is an API list-price equivalent, not credits paid or a subscription invoice.\n\nValidation: offline snapshot/checksum restoration checks, source-tree comparison and preservation of release-tag targets. Application code was not rebuilt or retested.\n\n[Restorable snapshot](https://github.com/fssrepository/myscoutee-roadmap/tree/master/guides/project-history/{scope})\n"
 t['issue_body']=body;t['project_fields']={'Task ID':tid,'Workstream':t['area'],'Started':t['start'],'Finished':t['end'],'Tokens M':round(n/1e6,3),'API equiv USD':round(cost,2),'Active h':round(hours*share,3),'Allocated h':round(hours*share,3),'Models':t['model_display'],'Reasoning':t['effort_display'],'Evidence':'Measured run; estimated project split'};T.append(t);rows.append(t)
summary['allocated_tokens_estimate']+=tokens-removed;summary['unassigned_tokens']-=tokens-removed;summary['api_standard_usd_estimate']=round(sum(t['api_standard_usd_estimate'] for t in T),2);assert summary['unassigned_tokens']>=0
assert sum(t['tokens_estimate'] for t in T)+summary['unassigned_tokens']==summary['account_tokens']
intervals=json.loads((P/'intervals-before-maintenance.json').read_text());kept=[]
for r in intervals:
 if r['task_key']=='B85' and r['end']>start:
  if r['start']>=start:continue
  r['end']=start
 kept.append(r)
for t in rows:
 for a,z in union:kept.append({'task_key':t['key'],'start':a,'end':z,'basis':'Shared measured maintenance interval; weighted project allocation','allocation_share':fields[t['project_scope']][2]/den})
(P/'observed-task-intervals.json').write_text(json.dumps(kept,indent=2)+'\n');(P/'portfolio-tasks.json').write_text(json.dumps(T,indent=2)+'\n');(P/'prepared-tasks.json').write_text(json.dumps(T,indent=2)+'\n');(P/'prepared-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
report={'cutoff_utc':cutiso,'measured_tokens':tokens,'measured_active_hours':hours,'project_weights':{k:v[2]/den for k,v in fields.items()},'previous_msc108_tokens_removed':removed,'previous_msc108_hours_removed':deduct,'net_additional_account_allocation':tokens-removed,'daily_attribution':'Not individually reconciled; allocated against remaining account allowance','models':models}
(P/'maintenance-measurement.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='models'},indent=2))
