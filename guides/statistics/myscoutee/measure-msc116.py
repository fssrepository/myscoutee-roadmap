#!/usr/bin/env python3
"""Read-only MSC-116 accounting through an explicit UTC cutoff.

Reuses the response-ID, active-interval and frozen-price implementation used
for MSC-119. Prints aggregate JSON only; never conversation text or credentials.
"""
import argparse
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cutoff', required=True)
args = parser.parse_args()
source = Path(__file__).with_name('measure-msc119.py')
spec = importlib.util.spec_from_file_location('task_usage', source)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
assert usage.seconds(args.cutoff) > usage.seconds('2026-10-15T19:28:57.278Z')
selections = {
    'e7d1bd77234eaf16': [
        ('2026-10-06T09:08:26.315Z', '2026-10-07T02:34:54.651Z'),
    ],
    '568bb4b5cf154165': [
        ('2026-10-15T12:12:45.315Z', '2026-10-15T19:21:04.634Z'),
        ('2026-10-15T19:28:57.278Z', args.cutoff),
    ],
}
note = (
    'Measured response usage; task attribution follows explicit request boundaries. '
    'Includes October 6 API/MCP and Events implementation, incidental Feedback UI '
    'corrections in that implementation turn, and October 15 delegated MSC-116 QA, '
    'central Feedback repair, consolidated guide introduction, serial KVM sample '
    'and closure preparation through the stated cutoff. Excludes the MSC-115 '
    'pre-MCP work, MSC-119 implementation and its separately accounted closure '
    'window, and other threads. Unique response IDs matching the source thread; '
    'cached input is included in input, reasoning output in output. Active time '
    'is the root turn-interval union, including tool waits and excluding idle gaps; '
    'unfinished turns are clipped at their last observed usage record. Existing '
    'other-task intervals retain their allocation; overlap is subtracted here. '
    'No claim of overlap recovery against unmeasured tasks. Publication and final '
    'responses after the cutoff are excluded. Frozen API-equivalent valuation is '
    'an estimate, not an invoice.'
)
print(json.dumps(usage.extract('MSC-116', selections, args.cutoff,
                              started='2026-10-06', note=note), indent=2))
