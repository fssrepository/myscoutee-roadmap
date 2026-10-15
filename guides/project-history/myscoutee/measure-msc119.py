#!/usr/bin/env python3
"""Read-only MSC-119 usage extraction; print aggregate JSON, never conversation text.

Run from any directory: python3 measure-msc119.py > /tmp/msc119-measurement.json
Reuses METHOD.md's response-ID and active-interval accounting. The source hashes
identify local thread IDs without publishing them. No network or ledger writes.
"""
import collections
import datetime as dt
import hashlib
import json
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home() / '.codex'
CUTOFF = '2026-10-15T19:28:57.277Z'
SELECTIONS = {
    'e7d1bd77234eaf16': [
        ('2026-10-07T02:34:54.652Z', '2026-10-07T04:44:06.085Z'),
        ('2026-10-07T04:58:35.873Z', '2026-10-07T04:59:16.360Z'),
    ],
    '2b4ca382ca3cc11e': [
        ('2026-10-15T16:52:54.087Z', '2026-10-15T17:15:40.324Z'),
    ],
    '568bb4b5cf154165': [('2026-10-15T19:21:04.635Z', CUTOFF)],
}


def seconds(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def iso(value):
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def union(intervals):
    result = []
    for start, end in sorted(intervals):
        if end <= start:
            continue
        if result and start <= result[-1][1]:
            result[-1][1] = max(end, result[-1][1])
        else:
            result.append([start, end])
    return result


def extract(task_id='MSC-119', selections=None, cutoff=CUTOFF, started='2026-10-07', note=None):
    selections = SELECTIONS if selections is None else selections
    ledger = json.loads((ROOT / 'measurements.json').read_text())
    db = sqlite3.connect(f'file:{HOME}/state_5.sqlite?mode=ro', uri=True)
    sources = {}
    for ident, path in db.execute('select id,rollout_path from threads'):
        digest = hashlib.sha256(ident.encode()).hexdigest()[:16]
        if digest in selections:
            sources[digest] = (ident, pathlib.Path(path))
    assert sources.keys() == selections.keys(), 'Required local source missing'
    seen = set()
    totals = collections.Counter()
    models = collections.defaultdict(collections.Counter)
    daily = collections.Counter()
    intervals = []
    evidence = []
    for digest, (ident, path) in sources.items():
        windows = [(seconds(a), seconds(b)) for a, b in selections[digest]]
        starts, ends, last_usage = {}, {}, {}
        selected = []
        model, effort = None, None
        for line in path.open():
            record = json.loads(line)
            payload = record.get('payload', {})
            stamp = seconds(record['timestamp'])
            kind = record['type']
            if kind == 'turn_context':
                model = payload.get('model', model)
                effort = payload.get('effort', payload.get('reasoning_effort', effort))
            turn = payload.get('turn_id')
            if kind == 'event_msg':
                if payload.get('type') == 'task_started':
                    starts[turn] = stamp
                elif payload.get('type') in ('task_complete', 'turn_aborted'):
                    ends[turn] = stamp
            if kind != 'token_usage_record' or payload.get('thread_id') != ident:
                continue
            last_usage[turn] = max(stamp, last_usage.get(turn, stamp))
            if not any(a <= stamp <= b for a, b in windows):
                continue
            response = payload['response_id']
            if response in seen:
                continue
            seen.add(response)
            usage = payload['usage']
            assert usage['input_tokens'] + usage['output_tokens'] == usage['total_tokens']
            assert model and effort, 'Model/effort must be observed'
            totals.update(usage)
            models[f'{model}|{effort}'].update(usage)
            daily[record['timestamp'][:10]] += usage['total_tokens']
            selected.append((stamp, usage['total_tokens'], turn))
        assert selected, 'No measured responses in selected source'
        selected_turns = {turn for _, _, turn in selected}
        for turn in selected_turns:
            assert turn in starts, 'Missing task start; do not infer active duration'
            end = ends.get(turn, last_usage[turn])
            for a, b in windows:
                intervals.append([max(a, starts[turn]), min(b, end)])
        evidence.append({
            'source_kind': 'root', 'source_sha256': digest,
            'selection_windows_utc': selections[digest],
            'tokens': sum(value for _, value, _ in selected),
            'unique_responses': len(selected),
            'first_usage_utc': iso(min(t for t, _, _ in selected)),
            'last_usage_utc': iso(max(t for t, _, _ in selected)),
        })
    active = union(intervals)
    previous = union([
        (seconds(a), seconds(b))
        for task in ledger['post_control_task_usage'] if task['task_id'] != task_id
        for a, b in task.get('active_intervals_utc', [])
    ])
    active_seconds = sum(b-a for a, b in active)
    overlap = sum(max(0, min(b, d)-max(a, c)) for a, b in active for c, d in previous)
    rates = ledger['rates_per_million']
    cost = 0
    for key, usage in models.items():
        model = key.split('|')[0]
        regular, cached, output, write = rates[model]
        cost += ((usage['input_tokens']-usage['cached_input_tokens'])*regular
                 + usage['cached_input_tokens']*cached
                 + usage['output_tokens']*output
                 + usage.get('cache_write_input_tokens', 0)*write)/1e6
    return {
        'task_id': task_id, 'tokens': totals['total_tokens'], 'cutoff_utc': cutoff,
        'unique_response_ids': len(seen), 'token_components': dict(totals),
        'models': dict(models), 'started': started, 'finished': cutoff[:10],
        'active_hours': active_seconds/3600,
        'allocated_hours': (active_seconds-overlap)/3600,
        'previously_allocated_overlap_hours': overlap/3600,
        'active_intervals_utc': [[iso(a), iso(b)] for a, b in active],
        'api_standard_usd_estimate': round(cost, 2),
        'valuation_date': ledger['valuation_date'],
        'rates_per_million': {m.split('|')[0]: rates[m.split('|')[0]] for m in models},
        'pricing_source': ledger['pricing_source'],
        'rate_basis': 'Frozen existing Standard API-equivalent rates; not an invoice or new price lookup.',
        'daily_tokens': dict(daily), 'sources': evidence,
        'note': note or 'Measured response usage, estimated task attribution by explicit request boundaries. '
                'Includes October 7 implementation/guides/publication preparation/consolidation and '
                'closing handoff, October 15 dedicated MSC-119 checklist reconciliation and closure '
                'preparation through the final accounting scope clarification. Excludes earlier '
                'MSC-115/116 work, the abandoned domain-architecture request, earlier MSC-117/118 '
                'checklist work, MSC-116 execution QA and final measurement/publication writes after '
                'the cutoff. Unique response IDs matching the source thread; cached input is inside '
                'input and reasoning output inside output. Root active-interval union includes '
                'tool waits, excludes idle gaps and clips mixed turns at selected request boundaries. '
                'Already recorded other-task intervals retain their allocation; intersecting time is '
                'removed from this incremental allocation. No claim of complete overlap recovery '
                'against unmeasured tasks. MSC-116 measurement fields remain unchanged.',
    }


if __name__ == '__main__':
    print(json.dumps(extract(), indent=2) + '\n', end='')
