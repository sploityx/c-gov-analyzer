#!/usr/bin/python3

import json
import pandas as pd
import matplotlib.pyplot as plt

with open('stat-data.json', 'r', encoding='utf-8') as file:
    df = pd.read_json(file, lines=True)

df = df[df['event'].str.startswith('cstate_pkg/')]
df['event'] = df['event'].str.replace('cstate_pkg/', '').str[:-1]
# remove trailing zeroes
df['counter-value'] = pd.to_numeric(df['counter-value'], downcast='float')

plt.pie(df['counter-value'], labels=df['event'], autopct='%1.1f%%', startangle=90)
plt.show()
