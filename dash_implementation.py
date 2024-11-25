
import pandas as pd
from dash import Output, Input, Dash, dcc, html
import numpy as np
import plotly.graph_objects as go



data = pd.read_csv("tempTable.csv")
data["lambda"] = 1./data["phi"]
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
    waxis = [x for x in axis if x not in [xaxis, yaxis, zaxis]][0]
    # Get current slice value
    waxis_value = ranges[slice_axis][slice_idx]
    #print(data.info)
    # Filter data
    print(xaxis,yaxis,zaxis,waxis,waxis_value)
    subData = data[(data.loc[:,waxis] == waxis_value) & data["completed"]]
    #print(subData.info)
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