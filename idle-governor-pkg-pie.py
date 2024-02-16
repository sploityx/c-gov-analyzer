#!/usr/bin/python3

import json
import pandas as pd
import matplotlib.pyplot as plt

with open('pkg-c-state.json', 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]

counter_values = [entry['counter-value'] for entry in data]
event_names = [entry['event'].split('/')[1] for entry in data]

df = pd.DataFrame({'counter-value': counter_values, 'event': event_names})

# remove trialing zeroes
df['counter-value'] = pd.to_numeric(df['counter-value'], downcast='float')

# Plot a pie chart
plt.pie(df['counter-value'], labels=df['event'], autopct='%1.1f%%', startangle=90)
plt.show()
