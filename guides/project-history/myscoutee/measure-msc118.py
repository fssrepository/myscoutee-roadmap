#!/usr/bin/env python3
"""Reproduce MSC-118 usage from retained response IDs through a fixed UTC cutoff."""
import argparse
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cutoff', required=True)
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('task_usage', Path(__file__).with_name('measure-msc119.py'))
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
selections = {
    '2048136f3b6db41f': [('2026-10-07T01:42:18.387Z', '2026-10-07T04:08:43.561Z')],
    '2b4ca382ca3cc11e': [('2026-10-15T16:31:33.571Z', '2026-10-15T16:52:54.086Z')],
    '49cebe0ca1460a03': [('2026-10-16T09:31:26.128Z', '2026-10-16T12:16:59.858Z')],
    'eea19e5e65d4ba46': [('2026-10-16T12:17:49.098Z', '2026-10-16T13:56:14.240Z')],
    '01bff8429919cefc': [('2026-10-16T12:37:52.591Z', args.cutoff)],
}
print(json.dumps(usage.extract('MSC-118', selections, args.cutoff, started='2026-10-07',
    include_archived_segments=True, allow_unpriced_models=True,
    note='Measured unique response usage; task attribution follows explicit request windows. '
    'Includes October7 role-guide/notification implementation and handoff, October15 checklist '
    'preparation and related QA reconciliation before the separately measured MSC-119 window, '
    'October16 delegated execution, associated shared-list repairs and verification, corrections, '
    'and accounting/history preparation through the cutoff. Reverted attempts count as consumed '
    'effort. Source segments are joined by thread identity; response IDs are deduplicated. '
    'Root active intervals are unioned across concurrent sessions, including tool waits and excluding '
    'idle gaps. Existing other-task allocations are subtracted from overlapping active time. '
    'Earlier general-guide/call work and later accounting/publication are excluded. '
    'Cached input is inside input; reasoning output is inside output. '
    'The frozen API-equivalent valuation is an estimate, not an invoice. '
    'Usage does not imply that the remaining prerequisite-limited QA is complete.'), indent=2))
