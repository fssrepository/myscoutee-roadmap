#!/usr/bin/env python3
"""Render the anonymous combined daily ledger as SVG and PNG (Inkscape required)."""
import calendar
from collections import Counter
import datetime as dt
import json
from pathlib import Path
import subprocess
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
COLORS = ['#dbeafe', '#93c5fd', '#3b82f6', '#1d4ed8', '#172554']
LIMITS = [10_000_000, 100_000_000, 500_000_000, 1_000_000_000]


def render():
    ledger = json.loads((HERE / 'account-coverage.json').read_text())
    rows = ledger['combinedDailyUsageBuckets']
    daily = {dt.date.fromisoformat(r['startDate']): r['tokens'] for r in rows}
    assert len(daily) == len(rows), 'Duplicate daily records'
    assert all(isinstance(v, int) and v >= 0 for v in daily.values())
    inputs = Counter()
    for account in ledger['accounts']:
        records = account['dailyUsageBuckets']
        assert sum(r['tokens'] for r in records) == account['total_tokens']
        assert len({r['startDate'] for r in records}) == len(records)
        for row in records:
            inputs[dt.date.fromisoformat(row['startDate'])] += row['tokens']
    assert dict(inputs) == daily, 'Input series do not match combined dates'
    total = sum(daily.values())
    assert total == ledger['combined_measured_tokens'], 'Daily total mismatch'
    first, last = min(daily), max(daily)
    start = first.replace(day=1)
    end = last.replace(day=calendar.monthrange(last.year, last.month)[1])
    grid_start = start - dt.timedelta(days=start.weekday())
    weeks = (end - grid_start).days // 7 + 1
    cell, step, left, top = 17, 22, 60, 150
    width, height = max(860, left + weeks * step + 30), 412
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
           '<title id="title">Combined daily AI token usage</title>',
           f'<desc id="description">{total:,} tokens across {sum(v > 0 for v in daily.values())} active dates. {first.isoformat()} to {last.isoformat()}. Darker blue means more tokens. Gray means no recorded usage; it does not establish zero usage. Calendar weeks start on Monday.</desc>',
           f'<rect width="{width}" height="{height}" rx="16" fill="#ffffff"/>',
           '<g font-family="DejaVu Sans, sans-serif" fill="#0f172a">']

    def text(x, y, value, size=12, color='#64748b', weight='400'):
        svg.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>')

    text(28, 36, 'AI token activity', 22, '#0f172a', '700')
    text(28, 59, 'Combined daily usage', 13)
    text(28, 100, f'{total / 1e9:.2f}B tokens', 25, '#1d4ed8', '700')
    text(295, 99, f'{sum(v > 0 for v in daily.values())} active days', 16, '#334155', '600')
    text(535, 99, f'{first:%d %b %Y} – {last:%d %b %Y}', 13)
    for month in range(1, 13):
        for year in range(start.year, end.year + 1):
            date = dt.date(year, month, 1)
            if start <= date <= end:
                text(left + ((date - grid_start).days // 7) * step, top - 12, calendar.month_abbr[month])
    for weekday in (0, 2, 4):
        text(28, top + weekday * step + 13, calendar.day_abbr[weekday], 10)
    for offset in range((end - grid_start).days + 1):
        date = grid_start + dt.timedelta(days=offset)
        if date < start:
            continue
        value = daily.get(date)
        color = '#f1f5f9' if not value else COLORS[sum(value > bound for bound in LIMITS)]
        label = f'{date.isoformat()}: {value:,} tokens' if value is not None else f'{date.isoformat()}: no recorded usage'
        svg.append(f'<rect x="{left + offset // 7 * step}" y="{top + date.weekday() * step}" width="{cell}" height="{cell}" rx="4" fill="{color}" data-date="{date}" data-tokens="{value if value is not None else ""}"><title>{escape(label)}</title></rect>')
    text(28, 331, 'DAILY TOKENS', 10, '#475569', '700')
    labels = ['No record / 0', '≤10M', '≤100M', '≤500M', '≤1B', '>1B']
    for i, (color, label) in enumerate(zip(['#f1f5f9'] + COLORS, labels)):
        x = 28 + i * 130
        svg.append(f'<rect x="{x}" y="345" width="14" height="14" rx="3" fill="{color}"/>')
        text(x + 20, 357, label, 11)
    text(28, 389, 'Recorded usage · includes cached input · unrecorded dates are not assumed to be zero', 11)
    svg.extend(['</g>', '</svg>'])
    out = HERE / 'media'
    out.mkdir(exist_ok=True)
    path = out / 'token-activity.svg'
    path.write_text('\n'.join(svg) + '\n')
    subprocess.run(['inkscape', str(path), '--export-type=png',
                    f'--export-filename={out / "token-activity.png"}',
                    f'--export-width={width * 2}', '--export-background=#ffffff',
                    '--export-background-opacity=1'], check=True)
    print(f'Rendered {len(daily)} recorded dates / {total:,} tokens as SVG and PNG')


if __name__ == '__main__':
    render()
