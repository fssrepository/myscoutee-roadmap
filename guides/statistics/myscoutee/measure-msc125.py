#!/usr/bin/env python3
"""Recover the dedicated MSC-125 implementation/release session, read-only."""
import importlib.util
import json
import pathlib
import sys
sys.dont_write_bytecode = True
root = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root / 'measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
print(json.dumps(usage.extract(
    'MSC-125', {'694c893afe073e06': [('2026-10-20T08:41:34.758Z', '2026-10-20T22:53:55.173Z')]},
    '2026-10-20T22:53:55.173Z', started='2026-10-20', include_archived_segments=True,
    allow_unpriced_models=True,
    note='Dedicated MSC-125 diagnostic implementation, corrections, release and Netcup deployment session. '
    'Includes failed/reverted attempts. Separate marketing/traffic-only reports and MSC-124 sessions are excluded. '
    'Unique own-thread response IDs; unioned active task intervals, idle gaps excluded and earlier task allocations subtracted. '
    'Cached input is within input; reasoning within output. Recovered during MSC-127 closeout; recovery work itself is excluded.'
), indent=2))
