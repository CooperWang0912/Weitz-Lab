import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


# Load the CSV file into a pandas dataframe with the correct delimiter and set the appropriate header
df = pd.read_csv('PDMS supernatant buckling test.xls - Axial - 1.csv', header=1)

# Remove the row with units and reset the index
df = df.drop(0).reset_index(drop=True)

# Convert the columns to the appropriate data types
df = df.apply(pd.to_numeric, errors='ignore')

x = df.get("Gap")
y = df.get("Axial force")

filterX = []
filterY = []

prev = -1

for i in range(len(x)):
    # if y[i] == max(y):
    #     break
    if -1000 >= x[i] >= -2000:
        filterX.append(x[i])
        filterY.append(y[i])
        prev = y[i]

base = filterX[0]

baseY = filterY[0]

filterX = [x - base for x in filterX]

filterY = [y - baseY for y in filterY]

def func1(x, p):
    A = p
    return A * x

def residual1(p, y, x):
    return y - func1(x, p)

p = [0.0084]
plsq1 = leastsq(residual1, p, args=(np.array(filterY), np.array(filterX)))

# print("Young's Modulus :" + str(abs(plsq1[0][0]) / (48 * 0.00246 * 0.011 ** 3) * 12 * 0.011 ** 3 * 1000000))

print("Young's Modulus :" + str(abs(plsq1[0][0])*10**6*.015/(.00326*.015)))

newX = np.linspace(filterX[0], filterX[len(filterX) - 1], 30)
newY = []

for i in newX:
    newY.append(i * plsq1[0][0] + baseY)

newX = [x + base for x in newX]

plt.scatter(x, y)
plt.plot(newX, newY, color='red')
plt.show()
