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
data["lambda"] = 1./data["phi"]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

axis = ["p", "Tu", "phi", "egr"]
ranges = {a:np.unique(data[a].to_numpy()) for a in axis}

xaxis = 3
yaxis = 1
zaxis = 2
waxis = [x for x in range(len(axis)) if x not in [xaxis, yaxis, zaxis]][0]
isoID = 0

subData = data.loc[data[axis[waxis]] == ranges[axis[waxis]][isoID]]  #Get the slice along waxis
where = np.invert(subData["completed"].to_numpy()) #Get not completed

ax.scatter(
    subData[axis[xaxis]][where],
    subData[axis[yaxis]][where],
    subData[axis[zaxis]][where],
    alpha=1
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
#fig.show()

# %%
import plotly.io as pio
pio.renderers.default='browser'


import plotly.express as px

var = "Su"
fig = px.scatter_3d(subData.loc[subData["completed"]],
              x=axis[xaxis],
              y=axis[yaxis],
              z=axis[zaxis],
              color=var,
              color_continuous_scale="turbo",
              range_color=[0.0, subData.loc[subData["completed"], var].to_numpy().max()])

# fig.add_trace(
#     px.scatter_3d(subData[where],
#               x=axis[xaxis],
#               y=axis[yaxis],
#               z=axis[zaxis],
#               color_discrete_sequence=["red"]).data[0])

# fig.update_layout(
#     scene = dict(
#         xaxis = dict(
#             tickmode = 'array',
#             tickvals=[v for v in ranges[axis[xaxis]]],
#             range=[
#                 ranges[axis[xaxis]].min()-0.05*(ranges[axis[xaxis]].max() - ranges[axis[xaxis]].min()),
#                 ranges[axis[xaxis]].max()+0.05*(ranges[axis[xaxis]].max() - ranges[axis[xaxis]].min())
#                 ],
#             title=dict(text=axis[xaxis])
#             ,),
#         yaxis = dict(
#             tickmode = 'array',
#             tickvals=[v for v in ranges[axis[yaxis]]],
#             range=[
#                 ranges[axis[yaxis]].min()-0.05*(ranges[axis[yaxis]].max() - ranges[axis[yaxis]].min()),
#                 ranges[axis[yaxis]].max()+0.05*(ranges[axis[yaxis]].max() - ranges[axis[yaxis]].min())
#                 ],
#             title=dict(text=axis[yaxis]),
#             ),
#         zaxis = dict(
#             tickmode = 'array',
#             tickvals=[v for v in ranges[axis[zaxis]]],
#             range=[
#                 ranges[axis[zaxis]].min()-0.05*(ranges[axis[zaxis]].max() - ranges[axis[zaxis]].min()),
#                 ranges[axis[zaxis]].max()+0.05*(ranges[axis[zaxis]].max() - ranges[axis[zaxis]].min())
#                 ],
#             title=dict(text=axis[zaxis]),
#             ),
#         )
#     )

fig.update_traces(
    marker = dict(
        size = 3,
        )
    )

fig.show()