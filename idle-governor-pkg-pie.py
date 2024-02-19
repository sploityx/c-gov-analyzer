#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression


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


def filter_format(df, event : str):
    '''Filters and formats the dataframe for event'''
    df = df[df['event'].str.startswith(event)]
    #df['event'] = df['event'].str.replace(event, '').str[:-1]
    return df


def pkg_pie_chart(df):
    '''Creates a pie chart for used C-States on pkg_level'''
    df_c_pkg = filter_format(df, 'cstate_pkg/')
    plt.pie(df_c_pkg['counter-value'], labels=df_c_pkg['event'], autopct='%1.1f%%', startangle=90)
    plt.show()


def regression(df):
    '''Analysis the regression pkg-states and energy consumption'''
    df_c_pkg = filter_format(df, 'cstate_pkg')
    df_power_pkg = filter_format(df, 'power/energy-pkg/')
    model = LinearRegression()
    model.fit(df_c_pkg['counter-value'], df_power_pkg['counter-value'])
    print(f'Coefficients: {model.coef_}')
    print(f'Intercept: {model.intercept_}')

def correlation(df):
    '''Calculates the pearson correlation between pkg c-states and energy consumption'''
    df_c_pkg = filter_format(df, 'cstate_pkg')
    df_power_pkg = filter_format(df, 'power/energy-pkg/')
    for _,c_pkg in df_c_pkg.iterrows():
        # we need lots more data for this to work as intented
        corr_coef, p_value = pearsonr(c_pkg['counter-value'], float(df_power_pkg['counter-value']))
        if p_value > 0.5:
            plt.scatter(corr_coef, c_pkg['counter-value'], c='green', label=c_pkg['event'])
        else:
            plt.scatter(corr_coef, c_pkg['counter-value'], c='red', label=c_pkg['event'])
    plt.show()



def main():
    '''Visualizes the output of the perf-stat json from the collect wrapper'''
    df = read_data()
    pkg_pie_chart(df)
    correlation(df)


if __name__ == '__main__':
    main()
