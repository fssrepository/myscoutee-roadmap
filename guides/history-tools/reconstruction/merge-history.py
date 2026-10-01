import json,pathlib,collections
P=pathlib.Path(__file__).parent
base=json.loads((P/'session-usage.json').read_text());extra=json.loads((P/'additional-session-usage.json').read_text());by={x['id']:x for x in base}
for t in extra:
 if t['id'] not in by:by[t['id']]=t;continue
 dst=by[t['id']]
 for field in ['events','turns','prompts','outcomes','activity_events']:
  v=dst.get(field,[])+t.get(field,[]);dedup={}
  for row in v:
   if field=='events':key=row.get('response_id') or (row['timestamp'],row['total_tokens'],row.get('turn_id'))
   else:key=json.dumps(row,sort_keys=True)
   dedup[key]=row
  dst[field]=sorted(dedup.values(),key=lambda r:r['timestamp'])
 dst['usage']={}
 for e in dst['events']:
  label=(e.get('model') or 'unknown')+'|'+(e.get('effort') or 'unknown');b=dst['usage'].setdefault(label,collections.Counter())
  for k in ['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']:b[k]+=e.get(k,0)
 if t.get('accounting')=='unique_response_id':dst['accounting']='unique_response_id'
(P/'session-usage.json').write_text(json.dumps(list(by.values()),separators=(',',':'))+'\n')
print('Distinct sessions',len(by),'responses/deltas',sum(len(t['events']) for t in by.values()))
