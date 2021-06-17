# Headfix Behavior Data Analysis Playground
# Jeremy Delahanty June 2021

# Import packages
import pandas as pd

import glob
import matplotlib.pyplot as plt

datadirs = "Desktop/testdir/behavior/*/raw/*.csv"

# Get voltage recording files into a list
# voltage_recording = glob.glob("Y:\specialk/behavior/*")

voltage_recordings = glob.glob(datadirs)

# Load the csv into a pandas dataframe
test = pd.read_csv(voltage_recordings[0], index_col="Time(ms)")

test = test.rename(columns=lambda x: x.strip())
# # what is .pop?
# test.pop("Time(ms)")

test = test > 3
test = test.astype(int)
test = test.diff()
test = test.fillna(0)

test.head()


print(test)

plt.plot(test.index, test["Lick"])
plt.plot(test.index, test["Liquid"])
plt.plot(test.index, test["Airpuff"])
plt.plot(test.index, test["Speaker"])

plt.show()
