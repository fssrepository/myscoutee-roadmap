from pathlib import Path
P=Path(__file__).parent
f=P/'build-tasks.py';s=f.read_text()
s=s.replace("task('OLD','Preserve the original frontend prototype and campaign archive','Operations',[(8,1),(8,2),(8,3),(8,4)])", """task('OLD','Import the archived MyScoutee frontend prototype','Legacy manual',[(8,1)])
for i in range(2,5):task('OLD'+str(i),repos[8]['commits'][i-1]['title'],'Legacy manual',[(8,i)])
for i,c in enumerate(repos[9]['commits'],1):task('E'+str(i),c['title'],'Administration portal',[(9,i)])
for i in list(range(1,12))+[15]:task('M'+str(i),repos[10]['commits'][i-1]['title'],'Mathematical research',[(10,i)])
task('MCOMM','Review research correspondence and document claim limitations','Research communication')""")
s=s.replace("task('RESEARCHVIDEO','Prepare the research side-project video and presentation','Side project')", "task('RESEARCHVIDEO','Prepare the Navier–Stokes research video and presentation','Research communication',[(10,12),(10,13),(10,14)])")
s=s.replace("outside_ids={e['id']", "outside_ids={e['id']")
s=s.replace("if root['id'] in outside_ids:return 'UNASSIGNED'", """# Explicit project ownership overrides the inherited IDE cwd.
 if root['id'] in outside_ids:
  mk='MATH'
 if re.search(r'e-k[oö]zig',root_title,re.I):mk='EKO'
 if mk in ['MATH','EKO']:
  prefix='M' if mk=='MATH' else 'E'
  candidates=[t for t in T.values() if re.fullmatch(prefix+r'\\d+',t['key'])]
  result=min(candidates,key=lambda t:(max(daynum(t['start'])-daynum(d),daynum(d)-daynum(t['end']),0),-len(vocab(text)&t['_words'])))['key']
  choice_cache[cachekey]=result;return result""")
s=s.replace("return 'UNASSIGNED' if re.search(r'email|levél|válasz|readme',x) else 'RESEARCHVIDEO'", "return 'MCOMM' if re.search(r'email|levél|válasz|readme',x) else 'RESEARCHVIDEO'")
s=s.replace("if re.search(r'e-k[oö]zig|e-kozig|bartek|levelére|email session',x):return 'UNASSIGNED'", "if re.search(r'e-k[oö]zig',x):return 'EKO'\n if re.search(r'bartek|levelére|email session',x):return 'UNASSIGNED'")
s=s.replace("if t['key'] in ['B85','B86']:continue", "if t['key'] in ['B85','B86','MCOMM'] or re.fullmatch(r'(?:E|M|OLD)\\d*',t['key']):continue")
s=s.replace("if cs and not t.get('frozen_audit_phase'):", "if cs and not t.get('frozen_audit_phase') and not t['key'].startswith('OLD'):")
s=s.replace("for i,t in enumerate(ordered,1):t['provisional_id']='MSC-'+str(i)", """previous={t['key']:t['provisional_id'] for t in json.loads((P/'final-tasks.json').read_text())}
for t in ordered:
 k=t['key']
 t['project_scope']='myscoutee-old' if k.startswith('OLD') else 'e-kozig' if re.fullmatch(r'E\\d+',k) else 'math' if k=='RESEARCHVIDEO' or k=='MCOMM' or re.fullmatch(r'M\\d+',k) else 'myscoutee'
 t['provisional_id']=previous.get(k) or ('EKO-'+k[1:] if k.startswith('E') else 'MATH-'+('13' if k=='MCOMM' else '14' if k=='M15' else k[1:]) if k.startswith('M') else 'OLD-'+k[3:])
 if k=='OLD':t['provisional_id']='OLD-1'
 if k=='RESEARCHVIDEO':t['provisional_id']='MATH-12'
 if k.startswith('OLD'):
  t['activity_hours_estimate']=0;t['activity_seconds']=0;t['token_basis']='Primarily manual legacy work, confirmed by the creator; no attributable AI usage retained';t['duration_basis']='Unknown manual effort; commit spacing is not used as a time estimate';t['manual_time_unknown']=True
""")
f.write_text(s)
f=P/'prepare-public.py';s=f.read_text().replace("if t['tokens_estimate']:continue", "if t['tokens_estimate'] or t.get('manual_time_unknown'):continue")
s=s.replace("percommit=statistics.median(","percommit=statistics.median(") # nonempty peer groups are checked below
s=s.replace("percommit=statistics.median(x['tokens_estimate']", "if not peers:continue\n percommit=statistics.median(x['tokens_estimate']")
s=s.replace(" t['issue_body']='\\n'.join(lines)+'\\n'", """ if t.get('manual_time_unknown'):
  lines=[f\"Historical record: **{t['title']}**.\",'',f\"Archive/import dates: {t['start']} → {t['end']}; these do not establish the original development period.\",'','The creator confirms that this is primarily manual legacy development. Historical effort is unknown and is deliberately left blank. Git commit spacing does not establish working hours. Minor AI help with GitHub may have occurred, but no task-level record supports assigning tokens, models or costs to this work.','',*lines[lines.index('Delivery evidence:'):]]
 if t['project_scope']=='math':lines+=['','Research status: finite-model experiments, numerical diagnostics and partial lemmas do not establish a solution of the continuous Navier–Stokes Millennium problem. The later withdrawal of amplitude-inhomogeneous normalization claims is recorded separately (MATH-14).']
 t['issue_body']='\\n'.join(lines)+'\\n'""")
s=s.replace("(P/'prepared-tasks.json').write_text", "for t in tasks:\n if t.get('manual_time_unknown'):\n  for k in ['Tokens M','API equiv USD','Active h','Models','Reasoning']:t['project_fields'].pop(k,None)\n  t['project_fields']['Evidence']='Manual legacy; effort unknown'\n(P/'prepared-tasks.json').write_text",1)
f.write_text(s)
