#!/usr/bin/env python3
"""Reproduce MSC-117 usage from retained response IDs through a fixed UTC cutoff."""
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
    '2048136f3b6db41f': [('2026-10-06T11:51:39.885Z', '2026-10-06T23:52:40.851Z')],
    '4b0ae96fcc52120b': [('2026-10-16T07:10:10.861Z', args.cutoff)],
    'b9a8097cd20b977d': [('2026-10-16T07:35:48.685Z', '2026-10-16T08:00:00.000Z')],
}
print(json.dumps(usage.extract('MSC-117', selections, args.cutoff, started='2026-10-06',
    include_archived_segments=True, allow_unpriced_models=True,
    note='Measured unique response usage; task attribution follows explicit request windows. '
    'Includes initial October6 WebRTC implementation, same-thread MCP/dev startup and call-guide follow-up '
    'before the general guide-introduction request, October16 delegated QA/corrections/closure preparation, '
    'and the separate October16 synthetic-audio explanation. Original and continued archive segments are '
    'joined by thread identity and response IDs deduplicated. Excludes later mixed general-guide/role work, '
    'template baseline qualification already credited elsewhere, and final publication after cutoff. '
    'Root active intervals are unioned across overlapping threads; tool waits count, idle gaps do not. '
    'Previously allocated other-task time is subtracted. No claim of complete overlap attribution against '
    'unmeasured tasks. Cached input is within input and reasoning within output. Frozen Standard '
    'API-equivalent valuation is an estimate, not an invoice.'), indent=2))
