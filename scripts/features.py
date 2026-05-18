import pandas as pd
from pathlib import Path


def main():
    src = Path('data/transformed/events.csv')
    outdir = Path('data/features')
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(src)
    df['duration_minutes'] = df['duration_seconds'].astype(float) / 60.0
    df['weekday'] = pd.to_datetime(df['date']).dt.day_name()

    # ensure columns: original four + date, duration_minutes, weekday
    cols = ['user_id', 'timestamp', 'event_type', 'duration_seconds', 'date', 'duration_minutes', 'weekday']
    df.to_csv(outdir / 'events.csv', index=False, columns=cols)


if __name__ == '__main__':
    main()
