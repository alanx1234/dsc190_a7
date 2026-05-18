import marimo
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/features/events.csv')

plt.figure()
df['duration_minutes'].hist(bins=30)
plt.xlabel('Duration (minutes)')
plt.title('Event duration distribution')
plt.tight_layout()
plt.savefig('notebooks/duration_hist.png')
