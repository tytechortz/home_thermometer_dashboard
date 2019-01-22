import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd 

app = dash.Dash()



app.layout = html.Div([
    html.Div([
    dcc.Graph(id='live-update-graph',style={'width':1200}),
    dcc.Interval(
        id='interval-component',
        interval=900000,
        n_intervals=0
    ),
    html.Pre(
        id='max_temp_text',
        children='Max Temp:'
    ),
    html.Pre(
        id='min_temp_text',
        children='Min Temp:'
    )]),
])

max_temp = []

@app.callback(Output('live-update-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('../../temptest.txt')
    fig = go.Figure(
        data = [go.Scatter(
            x = df['X'],
            y = df['Y'],
            mode = 'markers+lines'
        )])
    return fig 

@app.callback(Output('max_temp_text', 'children'),
            [Input('interval-component', 'n_intervals')])
def update_layout(n):
    df = pd.read_csv('../../temptest.txt')
    max_temp = df.loc[df['Y'].idxmax()]
    return 'Max Temp:  {}'.format(max_temp)

@app.callback(Output('min_temp_text', 'children'),
            [Input('interval-component', 'n_intervals')])
def update_layout(n):
    df = pd.read_csv('../../temptest.txt')
    min_temp = df.loc[df['Y'].idxmin()]
    return 'Min Temp:  {}'.format(min_temp)

if __name__ == '__main__':
    app.run_server()