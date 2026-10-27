#!/usr/bin/env python3
"""Reproduce the October 27 EKO-16 follow-up measurement from retained sessions."""

import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
source = root.parent / 'myscoutee' / 'measure-msc119.py'
spec = importlib.util.spec_from_file_location('portfolio_usage', source)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)

cutoff = '2026-10-27T18:46:25.831Z'
result = usage.extract(
    'EKO-16',
    {'cd4232553eb30abc': [('2026-10-27T18:30:56.899Z', cutoff)]},
    cutoff,
    started='2026-10-27',
    include_archived_segments=True,
    allow_unpriced_models=True,
    note='E-Kozig PDF guide, detailed Hungarian expansion, verification and the '
         'EKO-16 source commit. This later accounting turn is excluded. Unique '
         'response IDs and root-turn intervals; cached input is inside input.',
)

def overlap_hours(left, right):
    a = [(usage.seconds(s), usage.seconds(e)) for s, e in left]
    b = [(usage.seconds(s), usage.seconds(e)) for s, e in right]
    return sum(max(0, min(y, v) - max(x, u)) for x, y in a for u, v in b) / 3600

ai_pilot = json.loads((root.parent / 'ai-pilot' / 'measurements.json').read_text())
overlap = overlap_hours(result['active_intervals_utc'], ai_pilot['active_intervals_utc'])
result['extracted_allocated_hours_before_cross_project_overlap'] = result['allocated_hours']
result['cross_project_overlap_hours'] = overlap
result['allocated_hours'] -= overlap
result['cross_project_overlap_basis'] = 'AIP-1 active intervals already allocated in the portfolio'

assert result['tokens'] == 6572942
assert result['unique_response_ids'] == 59
assert abs(overlap - 25.22 / 3600) < 1e-7
print(json.dumps(result, indent=2))
