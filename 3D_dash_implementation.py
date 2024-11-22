import plotly as py
import pandas as pd

from plotly import tools
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])


colors = px.colors.qualitative.Plotly
# colors = ['blue', 'green', 'red', 'black', 'yellow']
symbols = ['circle', 'circle-open', 'square', 'square-open', 'diamond', 'diamond-open', 'cross', 'x']

df = px.data.stocks().set_index('date')
columns = df.columns

# Set up well organized controls in a dbc.Card()
controls = dbc.Card([dbc.FormGroup([dbc.Label("x-axis"),
                                    dcc.Dropdown(id='dd_x',
                                                 options= [{'label': k, 'value': k} for k in columns],
                                                  value=columns[0],
                                                ),
                                   ],),
                    dbc.FormGroup([dbc.Label("y-axis"),
                                   dcc.Dropdown(id='dd_y',
                                                options= [{'label': k, 'value': k} for k in columns],
                                                value=columns[1],
                                                ),
                                   ],),
                    dbc.FormGroup([dbc.Label("z-axis"),
                                   dcc.Dropdown(id='dd_z',
                                                options= [{'label': k, 'value': k} for k in columns],
                                                value=columns[2],
                                                ),
                                    ],)
                    ],
                    body=True,
                    style = {'font-size': 'large'}
                    )

# Set up the app layout using dbc.Container(), dbc.Row(), and dbc.Col()
app.layout = dbc.Container([html.H1("Make a column selection for each axis"),
                            html.Hr(),
                            dbc.Row([dbc.Col([controls],xs = 4),
                                     dbc.Col([dbc.Row([dbc.Col(dcc.Graph(id="market_graph")),])]),
                                    ]),
                            html.Br(),
                            ],
                            fluid=True,
                            )

# 3D figure with callbacks for color, symbol and size
@app.callback(
    Output("market_graph", "figure"),
    [
        Input("dd_x", "value"),
        Input("dd_y", "value"),
        Input("dd_z", "value"),
    ],
)
def history_graph(x, y, z):
#     df = px.data.iris()
    fig = px.scatter_3d(df, x=df[x], y=df[y], z=df[z])

    fig.data[0].update(marker_color=colors[4])
    fig.data[0].update(marker_symbol=symbols[6])
    fig.data[0].update(marker_size=8)

    fig.update_layout(uirevision='constant')
    fig.update_layout(template = 'plotly_dark')
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=10))
    return fig

app.run_server(mode='inline', port = 8007)