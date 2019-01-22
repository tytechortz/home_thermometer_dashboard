import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

app = dash.Dash()

app.layout = html.Div([
    html.Div([
    dcc.Graph(id='live-update-graph',style={'width':1200}),
    dcc.Interval(
        id='interval-component',
        interval=60000,
        n_intervals=0
    )])
])

@app.callback(Output('live-update-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
