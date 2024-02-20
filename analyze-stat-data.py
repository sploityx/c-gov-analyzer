#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np


def read_data():
    '''Reads the output of the perf-stat command and returns a pandas df'''
    with open('stat-data.json', 'r', encoding='utf-8') as file:
        df = pd.read_json(file, lines=True)
    return df


def filter_cstage_pkg(df):
    '''Filters and formats events for cstage_pkg'''
    df = df[df['event'].str.startswith('cstate_pkg/')]
    df['event'] = df['event'].str.replace('cstate_pkg/', '').str[:-1]
    return df


def divide_by_tsc(row):
    return row.iloc[:5]['counter-value'] / row.iloc[6]['counter-value']

def calc_perc(df):
    '''Calculates the percentages by dividing each set through TSC'''
    df = df.transform(divide_by_tsc, axis=1)
    return df


def calc_poll(df):
    '''Sums up all C-States and adds POLL, which accounts for when a pkg is not in any C-State'''
    df_summed = filter_cstage_pkg(df)
    df_summed = df_summed.groupby('event').sum(numeric_only=True).reset_index()
    total_time = df_summed['event-runtime'].mean()
    cstate_time = df_summed['counter-value'].sum()
    df_summed = df_summed.loc[:, ['counter-value', 'event', 'event-runtime']]
    poll = {'counter-value': total_time - cstate_time, 'event': 'POLL', 'event-runtime': total_time}
    df_summed.loc[len(df_summed.index)] = poll
    return df_summed


def filter_format(df, event : str):
    '''Filters and formats the dataframe for event'''
    df = df.loc[df['event'].str.startswith(event)]
    return df


def pkg_pie_chart(df):
    '''Creates a pie chart for used C-States on pkg_level'''
    #df_c_pkg = filter_format(df, 'cstate_pkg/')
    #df_c_pkg = df_c_pkg.groupby('event').sum(numeric_only=True).reset_index()
    df_c_pkg = df
    plt.pie(df_c_pkg['counter-value'], labels=df_c_pkg['event'], autopct='%1.1f%%', startangle=90)
    plt.show()


def regression(df):
    '''Analysis the regression pkg-states and energy consumption'''
    df_c_pkg = filter_format(df, 'cstate_pkg').reset_index(drop=True)
    df_power_pkg = filter_format(df, 'power/energy-pkg/').reset_index(drop=True)
    X = df_power_pkg[['counter-value']]
    y = df_c_pkg['counter-value'].values.reshape(-1, 4)
    correlation_matrix = np.corrcoef(X.values.flatten(), y.mean(axis=1))
    print(f'Correlation Matrix: {correlation_matrix}')
    correlation_coefficient = correlation_matrix[0, 1]
    print(f'Correlation Coefficient: {correlation_coefficient}')


def correlation(df):
    '''Calculates the pearson correlation between pkg c-states and energy consumption'''
    df_c_pkg = filter_format(df, 'cstate_pkg')
    df_power_pkg = filter_format(df, 'power/energy-pkg/')
    for _,c_pkg in df_c_pkg.iterrows():
        corr_coef, p_value = pearsonr(c_pkg['counter-value'], float(df_power_pkg['counter-value']))
        if p_value > 0.5:
            plt.scatter(corr_coef, c_pkg['counter-value'], c='green', label=c_pkg['event'])
        else:
            plt.scatter(corr_coef, c_pkg['counter-value'], c='red', label=c_pkg['event'])
    plt.show()



def main():
    '''Visualizes the output of the perf-stat json from the collect wrapper'''
    df = read_data()
    df_summed = calc_poll(df)
    pkg_pie_chart(df_summed)
    regression(df)
    #correlation(df)
    calc_perc(df)


if __name__ == '__main__':
    main()
