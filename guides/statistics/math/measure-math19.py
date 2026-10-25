#!/usr/bin/env python3
"""Read-only MATH-19 accounting; reuse the portfolio response/interval extractor."""
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('usage', root.parent / 'myscoutee/measure-msc119.py')
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)
cutoff = '2026-10-25T16:43:58.451Z'
result = usage.extract(
    'MATH-19', {'68c5773826c97d02': [('2026-10-25T15:46:46.202Z', cutoff)]},
    cutoff, started='2026-10-25', include_archived_segments=True,
    note='Dedicated Lean/PNT root session, from the initial introduction request '
    'through completion confirmation, ending at the accounting request. Includes '
    'assessment, initial PNT-2 delivery, scope clarification, full-cube/Cauchy/Schur '
    'continuation, failed attempts and corrections, tests, documentation, task '
    'updates and local commits. Response IDs are deduplicated; only source-thread '
    'usage counts. Active time is the union of recorded root turns, including '
    'tool/network waits and excluding idle gaps. Previous recorded portfolio '
    'allocations are subtracted from overlapping time. Cached input is inside '
    'input; reasoning is inside output. Frozen Standard API equivalents are '
    'estimates, not invoices. This accounting/publication turn is excluded; '
    'the previously reported 18 minutes described only the continuation, not '
    'the complete MATH-19 task. Account totals are separate overlapping controls.'
)
print(json.dumps(result, indent=2))
