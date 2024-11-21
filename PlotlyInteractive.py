#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("tempTable.csv")
data["lambda"] = 1. / data["phi"]

# Define variables and ranges
axis = ["p", "Tu", "phi", "egr"]
ranges = {a: np.unique(data[a].to_numpy()) for a in axis}
xaxis, yaxis, zaxis = 3, 1, 2  # Default axis selections
waxis = [x for x in range(len(axis)) if x not in [xaxis, yaxis, zaxis]][0]
isoID = 0

subData = data.loc[data[axis[waxis]] == ranges[axis[waxis]][isoID]]  # Get the slice along waxis
var = "Su"

# Initial figure
fig = px.scatter_3d(subData.loc[subData["completed"]],
                    x=axis[xaxis],
                    y=axis[yaxis],
                    z=axis[zaxis],
                    color=var,
                    color_continuous_scale="turbo",
                    range_color=[0.0, subData.loc[subData["completed"], var].to_numpy().max()])

# Function to update axis in the plot
def create_3d_trace(xaxis, yaxis, zaxis):
    waxis = [x for x in range(len(axis)) if x not in [xaxis, yaxis, zaxis]][0]
    subData = data.loc[data[axis[waxis]] == ranges[axis[waxis]][isoID]]
    return go.Scatter3d(
        x=subData.loc[subData["completed"], axis[xaxis]],
        y=subData.loc[subData["completed"], axis[yaxis]],
        z=subData.loc[subData["completed"], axis[zaxis]],
        mode="markers",
        marker=dict(
            size=3,
            color=subData.loc[subData["completed"], var],
            colorscale="turbo",
            colorbar=dict(title=var),
            cmin=0.0,
            cmax=subData.loc[subData["completed"], var].to_numpy().max(),
        )
    )


# Add initial trace
fig = go.Figure(data=[create_3d_trace(xaxis, yaxis, zaxis)])

# Create dropdown menus
dropdown_x = [
    dict(label=f"X: {ax}", method="update", args=[{"x": [subData.loc[subData["completed"], ax]]}, {"title": f"X-axis: {ax}"}])
    for ax in axis
]
dropdown_y = [
    dict(label=f"Y: {ax}", method="update", args=[{"y": [subData.loc[subData["completed"], ax]]}, {"title": f"Y-axis: {ax}"}])
    for ax in axis
]
dropdown_z = [
    dict(label=f"Z: {ax}", method="update", args=[{"z": [subData.loc[subData["completed"], ax]]}, {"title": f"Z-axis: {ax}"}])
    for ax in axis
]

# Add menus to layout
fig.update_layout(
    updatemenus=[
        dict(
            buttons=dropdown_x,
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top",
        ),
        dict(
            buttons=dropdown_y,
            direction="down",
            showactive=True,
            x=0.3,
            xanchor="left",
            y=1.15,
            yanchor="top",
        ),
        dict(
            buttons=dropdown_z,
            direction="down",
            showactive=True,
            x=0.5,
            xanchor="left",
            y=1.15,
            yanchor="top",
        ),
    ],
    scene=dict(
        xaxis=dict(title=axis[xaxis]),
        yaxis=dict(title=axis[yaxis]),
        zaxis=dict(title=axis[zaxis]),
    )
)

# Show the figure
fig.show()
