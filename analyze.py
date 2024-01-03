#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import json
from cycler import cycler
import copy
import pandas
import shutil
from pathlib import Path

#plt.style.use('grayscale')
DPI=300
FIGSIZE_WIDE = (12,7)

def prepare_ax(ax):
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.tick_params(top=False)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.set(yticklabels=[])
    ax.set(xticklabels=[])
    ax.tick_params(left=False)

def load_json_file(filename):
    with open(filename) as fd:
        print(filename)
        return json.load(fd)

def transform_data(db):
    times = []
    lables = []
    print(db.items())
    for state, state_data in db.items():
        lables.append(state)
        times.append(state_data)
    return lables, times

def df_cstate(df, cstate):
    return df[df["C-State"] == cstate]

#TODO: WIP
def graph_three_dim_scatter_sleeptime_by_sequence(df, output_folder, cpu):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    df = df.head(100)
    zs = list(range(len(df)))
    xs = np.log10(df["sleep_time"])
    ys = df["cstate"]
    if len(xs) == 0:
        return

    ax.scatter(xs, ys, zs)
    ax.set_xlabel('Sleep Time')
    ax.set_ylabel('C-State')
    plt.yticks(np.arange(min(ys), max(ys)+1, 1.0))
    ax.set_zlabel('Sequence')
    plt.savefig(output_folder + "scatter3d-CPU" + str(cpu) + ".png", dpi=DPI)
    plt.close()

#TODO: WIP
def graph_bar_sleeptime_by_sequence(df, output_folder, cpu):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    df = df.head(2000)
    colors = ['r', 'g', 'b', 'y', 'r', 'g', 'b', 'y']
    yticks=df["C-State"]
    yticks(np.arange(min(ys), max(ys)+1, 1.0))
    for c, k in zip(colors, yticks):
        xs = df["Sleep [s]"]
        ys = list(range(len(df)))

        # You can provide either a single color or an array with the same length as
        # xs and ys. To demonstrate this, we color the first bar of each set cyan.
        cs = [c] * len(xs)
        cs[0] = 'c'

        # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
        ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # On the y-axis let's only label the discrete values that we have data for.
    ax.set_yticks(yticks)

    plt.show()

def graph_bar(df_all, output_folder, gov_names):
    data = []
    for df in df_all:
        cstates = df["C-State"]
        usage = dict.fromkeys(cstates.unique())
        for cstate in cstates:
            usage[cstate] = len(df_cstate(df, cstate))
        data.append(usage)

    #plt.bar(range(len(usage)), list(usage.values()), tick_label = list(usage.keys()))

    """
    x = np.arange(len(cstates))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')

    for cstate, amount in usage.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, amount, width, label=cstate)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Amount')
    #ax.set_xticks(x + width, usage)
    ax.legend(loc='upper left', ncols=2)
    """
    categories = set().union(*(entry.keys() for entry in data))
    amounts = np.array([[entry.get(cat, np.nan) for cat in categories] for entry in data])

    # Number of groups and width for each bar
    num_groups = len(data)
    bar_width = 0.25

    # Create bar positions for each group
    bar_positions = np.arange(len(categories))

    # Plotting the grouped barplot
    for i in range(num_groups):
        plt.bar(bar_positions + i * bar_width, amounts[i], width=bar_width, label=gov_names[i])

    # Customize plot
    plt.yscale("log")
    plt.xlabel('C-States')
    plt.ylabel('Usage')
    plt.xticks(bar_positions + (bar_width * (num_groups - 1)) / 2, categories)
    plt.legend()
    plt.savefig(output_folder + f"bar.png", dpi=DPI)
    plt.close()

def graph_scatter_sleeptime_by_time(df, graph_cstate, output_folder, cpu):
    #TODO: maybe try x to be the whole dataframe and plot only cstates on y
    prev_color = 'orange'
    next_color = 'r'
    perfect_color = 'k'
    df = df_cstate(df, graph_cstate)
    x = list(range(len(df)))
    if len(x) == 0:
        return
    y=df["Sleep [s]"]
    col = np.where(df["Miss"] == 0, perfect_color, np.where(df["Below"] == 0, prev_color, next_color))
    plt.scatter(x=x, y=y, alpha=0.4, s=20, c=col, edgecolors="none")
    plt.xlabel("Sequence")
    plt.ylabel("Idle Time (" + chr(181) + "s)")
    plt.grid(linewidth=0.3)
    """
    TODO: FIX THIS
    residency = df["residency"].iloc[0]
    prev_residency = df["prev_residency"].iloc[0]
    next_residency = df["next_residency"].iloc[0]
    plt.plot([0, len(df)], [residency, residency], color=perfect_color, alpha=0.5, label="Residency", linewidth=1.2)
    #TODO: change this, such that it is not that hacky with String None
    if prev_residency != "None":
        prev_residency = int(prev_residency)
        plt.plot([0, len(df)], [prev_residency, prev_residency], color=prev_color, alpha=0.5, label="Next Residency", linestyle="dotted")
    if next_residency != "None":
        next_residency = int(next_residency)
        plt.plot([0, len(df)], [next_residency, next_residency], color=next_color, alpha=0.5,
                 label="Previous Residency", linestyle="dotted")
    """
    plt.yscale("log")
    plt.legend()
    ax = plt.subplot(111)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlim(left=0)
    plt.savefig(output_folder + f"scatter-{graph_cstate}-CPU-{cpu}.png", dpi=DPI)
    plt.close()


def graph_plot_all_cpus_by_time(df, cpu, output_folder):
    x = df["sleep_start"]
    y = df["sleep_time"]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.savefig(output_folder + "plot-all-cpus.png", dpi=DPI)
    plt.close()


def graph_scatter_sleeptime_by_sequence(df, graph_cstate, output_folder, cpu):
    #TODO: maybe try x to be the whole dataframe and plot only cstates on y
    prev_color = 'orange'
    next_color = 'r'
    perfect_color = 'k'
    df = df_cstate(df, graph_cstate)
    x = list(range(len(df)))
    if len(x) == 0:
        return
    y=df["Sleep [s]"]
    col = np.where(df["miss"] == 0, perfect_color, np.where(df["below"] == 0, prev_color, next_color))
    plt.scatter(x=x, y=y, alpha=0.4, s=20, c=col, edgecolors="none")
    plt.xlabel("Sequence")
    plt.ylabel("Idle Time (" + chr(181) + "s)")
    plt.grid(linewidth=0.3)
    residency = df["residency"].iloc[0]
    prev_residency = df["prev_residency"].iloc[0]
    next_residency = df["next_residency"].iloc[0]
    plt.plot([0, len(df)], [residency, residency], color=perfect_color, alpha=0.5,
             label="Residency", linewidth=1.2)
    #TODO: change this, such that it is not that hacky with String None
    if prev_residency != "None":
        prev_residency = int(prev_residency)
        plt.plot([0, len(df)], [prev_residency, prev_residency], color=prev_color, alpha=0.5,
                 label="Previous Residency", linestyle="dotted")
    if next_residency != "None":
        next_residency = int(next_residency)
        plt.plot([0, len(df)], [next_residency, next_residency], color=next_color, alpha=0.5,
                 label="Next Residency", linestyle="dotted")
    plt.yscale("log")
    plt.legend()
    ax = plt.subplot(111)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlim(left=0)
    plt.savefig(output_folder + "scatter-" + str(df["name"].iloc[0]) + "-CPU" + str(cpu)
                + ".png", dpi=DPI)
    plt.close()

COPY_FOLDER = "used_data/"
GOVS = ["menu/", "teo/", "ladder/"]
FILE_NAME = "idle-governor-events.txt"
COPY_FILE = COPY_FOLDER + FILE_NAME
OUTPUT_FOLDER = "visualization/"

df_all = []
gov_names = []
for gov in GOVS:
    Path(COPY_FOLDER + gov).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_FOLDER + gov).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(gov + FILE_NAME, COPY_FOLDER + gov + FILE_NAME)
    df = pandas.read_csv(COPY_FOLDER + gov + FILE_NAME)
    for cstate in df["C-State"].unique():
        #graph_scatter_sleeptime_by_sequence(df, cstate, OUTPUT_FOLDER, 0)
        graph_scatter_sleeptime_by_time(df, cstate, OUTPUT_FOLDER + gov, 0)
    df_all.append(df)
    gov_names.append(gov[:-1])
graph_bar(df_all, OUTPUT_FOLDER, gov_names)
#graph_plot_all_cpus_by_time(df, cpu, output_folder)
#graph_three_dim_scatter_sleeptime_by_sequence(df, output_folder, cpu)
#graph_bar_sleeptime_by_sequence(df, output_folder, cpu)
