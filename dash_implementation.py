import numpy as np
import pandas as pd
from dash import Output, Input, Dash, html, dcc

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

# Define unique values for each axis
unique_p = np.linspace(1, 100, 5)       # 5 unique pressure values
unique_Tu = np.linspace(10, 50, 4)      # 4 unique Tu values
unique_phi = np.linspace(0.1, 1.0, 6)   # 6 unique phi values (avoiding zero)
unique_egr = np.linspace(5, 25, 3)      # 3 unique EGR values

# Generate random data
num_points = 1000
p = np.random.choice(unique_p, size=num_points)
Tu = np.random.choice(unique_Tu, size=num_points)
phi = np.random.choice(unique_phi, size=num_points)
egr = np.random.choice(unique_egr, size=num_points)
Su = np.random.uniform(0, 100, size=num_points)
completed = np.random.choice([True, False], size=num_points, p=[0.7, 0.3])

# Create DataFrame
data = pd.DataFrame({
    "p": p,
    "Tu": Tu,
    "phi": phi,
    "egr": egr,
    "Su": Su,
    "completed": completed
})

# Calculate 'lambda'
data["lambda"] = 1.0 / data["phi"]
app = Dash(__name__)

axis = ["p", "Tu", "phi", "egr"]
ranges = {a: np.unique(data[a].to_numpy()) for a in axis}

app.layout = html.Div([
    # Dropdowns for X, Y, Z axes
    html.Div([
        html.Label('X-axis:'),
        dcc.Dropdown(id='xaxis-dropdown', options=[{'label': ax, 'value': ax} for ax in axis], value=axis[0]),
    ], style={'width': '24%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Y-axis:'),
        dcc.Dropdown(id='yaxis-dropdown', options=[{'label': ax, 'value': ax} for ax in axis], value=axis[1]),
    ], style={'width': '24%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Z-axis:'),
        dcc.Dropdown(id='zaxis-dropdown', options=[{'label': ax, 'value': ax} for ax in axis], value=axis[2]),
    ], style={'width': '24%', 'display': 'inline-block'}),

    # Dropdown and Slider for 4th dimension
    html.Div([
        html.Label('Slice along:'),
        dcc.Dropdown(id='slice-dropdown', options=[{'label': ax, 'value': ax} for ax in axis], value=axis[3]),
        dcc.Slider(id='slice-slider', min=0, max=0, step=1, value=0, marks={}),
    ], style={'width': '24%', 'display': 'inline-block'}),

    # 3D Scatter Plot
    dcc.Graph(id='3d-scatter-plot')
])
from dash import Output, Input

@app.callback(
    [Output('slice-slider', 'min'),
     Output('slice-slider', 'max'),
     Output('slice-slider', 'marks'),
     Output('slice-slider', 'value')],
    Input('slice-dropdown', 'value')
)
def update_slice_slider(slice_axis):
    unique_values = ranges[slice_axis]
    marks = {i: str(v) for i, v in enumerate(unique_values)}
    return 0, len(unique_values)-1, marks, 0

import plotly.graph_objects as go

@app.callback(
    Output('3d-scatter-plot', 'figure'),
    [Input('xaxis-dropdown', 'value'),
     Input('yaxis-dropdown', 'value'),
     Input('zaxis-dropdown', 'value'),
     Input('slice-dropdown', 'value'),
     Input('slice-slider', 'value')]
)
def update_graph(xaxis, yaxis, zaxis, slice_axis, slice_idx):
    # Ensure all axes are unique
    if len({xaxis, yaxis, zaxis, slice_axis}) < 4:
        return go.Figure()

    # Get current slice value
    waxis_value = ranges[slice_axis][slice_idx]

    # Filter data
    subData = data[(data[waxis] == waxis_value) & data["completed"]]

    # Create 3D scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=subData[xaxis],
        y=subData[yaxis],
        z=subData[zaxis],
        mode='markers',
        marker=dict(
            size=5,
            color=subData["Su"],
            colorscale='turbo',
            colorbar=dict(title='Su'),
            opacity=0.8
        )
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title=xaxis,
            yaxis_title=yaxis,
            zaxis_title=zaxis,
        ),
        title=f'Slice of {waxis} = {waxis_value}'
    )
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)