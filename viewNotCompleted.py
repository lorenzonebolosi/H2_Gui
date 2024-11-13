#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 08:45:22 2024

@author: framognino
"""
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("tempTable.csv")

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

axis = ["p", "Tu", "phi", "egr"]
ranges = {a:np.unique(data[a].to_numpy()) for a in axis}

xaxis = 3
yaxis = 1
zaxis = 2
waxis = [x for x in range(len(axis)) if x not in [xaxis, yaxis, zaxis]][0]
isoID = 0

where = np.invert(data["completed"].to_numpy())
subData = data.loc[where]   #Get not completed
subData = subData.loc[subData[axis[waxis]] == ranges[axis[waxis]][isoID]]  #Get the slice along waxis

ax.scatter(
    subData[axis[xaxis]], 
    subData[axis[yaxis]], 
    subData[axis[zaxis]]
    )

ax.set_xlim([ranges[axis[xaxis]].min(), ranges[axis[xaxis]].max()])
ax.set_ylim([ranges[axis[yaxis]].min(), ranges[axis[yaxis]].max()])
ax.set_zlim([ranges[axis[zaxis]].min(), ranges[axis[zaxis]].max()])

ax.set_xticks(ranges[axis[xaxis]])
ax.set_yticks(ranges[axis[yaxis]])
ax.set_zticks(ranges[axis[zaxis]])

ax.set_xlabel(axis[xaxis])
ax.set_ylabel(axis[yaxis])
ax.set_zlabel(axis[zaxis])