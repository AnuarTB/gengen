from ast import literal_eval

import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np


def parse_log_data():
    dates = []
    exec_times = []
    inputs = []
    for line in open("gengen_logs.log", "r"):
        info = line.split(" - ")
        dates.append(info[0])
        expr = literal_eval(info[1])
        exec_times.append(expr[0])
        inputs.append(expr[1])
    indexes = tuple(np.arange(1, len(dates) + 1))
    return indexes, dates, exec_times, inputs


def plot_graph(indexes, exec_times):
    plt.figure(1)
    y_pos = np.arange(len(indexes))
    bars = plt.bar(y_pos, exec_times, align="center", alpha=0.5)
    autolabel(bars)
    plt.xticks(y_pos, indexes)
    plt.ylabel("Time (s)")
    plt.title("Runtime statistics")


def autolabel(bars):
    """
    Attach a text label above each bar displaying its height
    """
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 "% 6.3f" % height,
                 ha="center", va="bottom")


def plot_table(indexes, dates, exec_times, inputs):
    columns = ("Date", "Runtime")
    rows = ["#%d" % x for x in indexes]

    # Get some pastel shades for the colors
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    cell_text = []
    for d, t in zip(dates, exec_times):
        cell_text.append([d, t])

    fig, ax = plt.subplots()

    # Hide axes
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)
    ax.spines['bottom'].set_color((0.1, 0.2, 0.5, 0.0))
    ax.spines['top'].set_color((0.1, 0.2, 0.5, 0.0)) 
    ax.spines['right'].set_color((0.1, 0.2, 0.5, 0.0))
    ax.spines['left'].set_color((0.1, 0.2, 0.5, 0.0))
    table = ax.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='center')


if __name__ == "__main__":
    (indexes, dates, exec_times, inputs) = parse_log_data()
    plot_graph(indexes, exec_times)
    plot_table(indexes, dates, exec_times, inputs)
    plt.show()
