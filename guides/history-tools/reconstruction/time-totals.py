import json,pathlib,collections,csv,io
P=pathlib.Path(__file__).parent;tasks=json.loads((P/'prepared-tasks.json').read_text());by={t['key']:t for t in tasks};intervals=json.loads((P/'observed-task-intervals.json').read_text());events=collections.defaultdict(list)
for r in intervals:events[r['start']].append((r['task_key'],1));events[r['end']].append((r['task_key'],-1))
active=collections.Counter();allocated=collections.Counter();unique=0;previous=None
for point,changes in sorted(events.items()):
 present=[k for k,n in active.items() if n>0]
 if previous is not None and present:
  span=point-previous;unique+=span
  for k in present:allocated[k]+=span/len(present)
 for k,delta in changes:active[k]+=delta
 previous=point
unknown=0;repo_totals=collections.defaultdict(collections.Counter);area_totals=collections.defaultdict(collections.Counter)
for t in tasks:
 if t['key'] in allocated:t['allocated_hours']=allocated[t['key']]/3600;t['allocated_time_basis']='Observed task intervals, overlap divided equally across concurrent tasks'
 else:t['allocated_hours']=t['activity_hours_estimate'];unknown+=t['allocated_hours'];t['allocated_time_basis']='Estimated task time; placement and overlap are unobserved'
 weights=collections.Counter()
 for c in t['commits']:weights['myscoutee' if c['repo'].endswith('/frontend') else c['repo']]+=c['original_count']
 if not weights:weights['Creative side work']=1
 denom=sum(weights.values())
 t['repository_allocations']={r:{'hours':t['allocated_hours']*w/denom,'tokens':t['tokens_estimate']*w/denom,'api_equivalent_usd':t['api_standard_usd_estimate']*w/denom} for r,w in weights.items()}
 for r,v in t['repository_allocations'].items():repo_totals[r].update(v)
 area_totals[t['area']].update({'hours':t['allocated_hours'],'tokens':t['tokens_estimate'],'api_equivalent_usd':t['api_standard_usd_estimate']})
summary={'observed_nonoverlapping_hours':unique/3600,'additional_estimated_hours':unknown,'total_allocated_hours_estimate':unique/3600+unknown,'note':'Logged overlap is removed once across tasks. Missing timing remains estimated; historic overlap cannot be recovered. Multi-repository task totals are apportioned by original commit counts, not billed independently to every repository. Repository shares are estimates.','repositories':dict(repo_totals),'workstreams':dict(area_totals)}
assert abs(sum(t['allocated_hours'] for t in tasks)-summary['total_allocated_hours_estimate'])<1e-6
(P/'prepared-tasks.json').write_text(json.dumps(tasks,indent=2)+'\n');(P/'time-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['repositories','workstreams']},indent=2));print('By repository',json.dumps(summary['repositories'],indent=2))
