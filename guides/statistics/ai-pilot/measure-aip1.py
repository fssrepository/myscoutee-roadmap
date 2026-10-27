#!/usr/bin/env python3
"""Reproduce the fixed AIP-1 measurement from retained local Codex sessions."""

import importlib.util
import json
from pathlib import Path

root = Path(__file__).resolve().parent
source = root.parent / 'myscoutee' / 'measure-msc119.py'
spec = importlib.util.spec_from_file_location('portfolio_usage', source)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)

cutoff = '2026-10-27T18:51:50.018Z'
selections = {
    '0b68624c92a692ad': [('2026-10-11T06:06:08.244Z', '2026-10-11T10:50:56.662Z')],
    'e97711cd90ab9401': [('2026-10-27T18:27:02.443Z', '2026-10-27T18:31:41.904Z')],
    'cd4232553eb30abc': [('2026-10-27T18:46:49.246Z', cutoff)],
}

result = usage.extract(
    'AIP-1', selections, cutoff, started='2026-10-11',
    include_archived_segments=True, allow_unpriced_models=True,
    note='AI Pilot research and experiments from the October 11 dedicated source '
         'thread, October 27 guides reorganization from its dedicated thread, and '
         'the current AIP-1 portfolio task through the stated cutoff. Source '
         'response IDs are deduplicated; active time is the union of recorded '
         'root turns. Current accounting and publication after cutoff are '
         'excluded. Cached input is included in input; reasoning output is '
         'included in output. Shared account totals are not additive.',
)
assert result['tokens'] == 53114285
assert result['unique_response_ids'] == 421
print(json.dumps(result, indent=2))
