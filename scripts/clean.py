import re
import pandas as pd
from pathlib import Path


TIMESTAMP_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    '%m/%d/%Y %H:%M:%S',
]


def normalize_event_type(val):
    if pd.isna(val):
        return None
    s = re.sub(r'[^A-Za-z]', '', str(val)).lower()
    mapping = {
        'buy': 'purchase',
        'purchase': 'purchase',
        'klick': 'click',
        'click': 'click',
        'view': 'view',
        'scroll': 'scroll',
        'login': 'login',
    }
    return mapping.get(s)


def parse_timestamps(series):
    parsed = pd.Series(pd.NaT, index=series.index, dtype='datetime64[ns]')

    for fmt in TIMESTAMP_FORMATS:
        missing = parsed.isna()
        if not missing.any():
            break
        parsed.loc[missing] = pd.to_datetime(
            series.loc[missing],
            format=fmt,
            errors='coerce',
        )

    return parsed


def main():
    src = Path('data/raw/events.csv')
    outdir = Path('data/clean')
    outdir.mkdir(parents=True, exist_ok=True)

    # read without forcing dtypes so missing fields are NaN
    df = pd.read_csv(src)

    # normalize empty strings to NA, then drop any row with missing fields
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    df = df.dropna(subset=['user_id', 'timestamp', 'event_type', 'duration_seconds'])

    # coerce duration to numeric and keep only positive integers
    df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
    df = df.dropna(subset=['duration_seconds'])
    df = df[(df['duration_seconds'] > 0) & (df['duration_seconds'] % 1 == 0)]
    # make sure durations are integers
    df['duration_seconds'] = df['duration_seconds'].astype(int)

    # normalize event_type and drop invalid
    df['event_type'] = df['event_type'].apply(normalize_event_type)
    df = df.dropna(subset=['event_type'])

    # parse timestamps and normalize to ISO 8601 without microseconds
    df['timestamp'] = parse_timestamps(df['timestamp'])
    df = df.dropna(subset=['timestamp'])
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    # final safety: ensure no blank fields remain
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    df = df.dropna()

    df.to_csv(outdir / 'events.csv', index=False)


if __name__ == '__main__':
    main()
