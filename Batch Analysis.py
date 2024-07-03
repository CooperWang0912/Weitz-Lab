import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import scipy
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoLocator

folder_path = Path('/Users/cooperwang/PycharmProjects/Rheometer/Data')

samples = []

datas = []
shortDatas = []

for file_path in folder_path.glob('*.csv'):

    csvFile = open(file_path, "r")
    reader = csv.reader(csvFile, delimiter="\t")
    a = list(reader)

    initials = []

    for i in range(121):
        initials.append(a.pop(0))

    initialsDict = {}
    for i in initials:
        if len(i) == 2:
            initialsDict.update({i[0]: i[1]})
        else:
            initialsDict.update({i[0]: "N/A"})

    samples.append(initialsDict.get("Filename"))

    labels = a.pop(0)

    a.pop(0)

    data = []

    shortData = []

    for i in labels:
        data.append([])

    shortLabels = []

    for i in a:
        if len(i) == 5:
            shortLabels = i
            break

    for i in shortLabels:
        shortData.append([])

    for i in a:
        if len(i) == 43 and not isinstance(i, str):
            for j in range(43):
                if j != 22:
                    try:
                        data[j].append(float(i[j]))
                    except ValueError:
                        break
                else:
                    data[j].append(i[j])
        elif len(i) == 5 and not isinstance(i, str):
            for j in range(5):
                try:
                    shortData[j].append(float(i[j]))
                except ValueError:
                    break

    data = pd.DataFrame(data).T
    data.columns = labels
    datas.append(data)

    shortData = pd.DataFrame(shortData).T
    shortData.columns = shortLabels
    shortDatas.append(shortData)

def moving_average(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')

for i in range(len(datas)):
    x = datas[i].get("Time")
    y = datas[i].get("Storage modulus")
    x_av = moving_average(interval=x, window_size=10)
    y_av = moving_average(interval=y, window_size=10)
    plt.scatter(x_av, y_av, label=samples[i])
ax1 = plt.gca()
ax1.xaxis.set_major_locator(AutoLocator())
ax1.yaxis.set_major_locator(AutoLocator())
ax1.set_title("Time vs Storage Modulus")
ax1.set_xlabel("Time")
ax1.set_ylabel("Storage Modulus")
plt.legend(bbox_to_anchor=(0.89, 0.8), ncol=3, fontsize='4')
plt.show()