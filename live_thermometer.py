import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd 

app = dash.Dash()

df = pd.read_csv('../../temptest.txt')



app.layout = html.Div([
    html.Div([
    html.Pre(
        id='live-thermometer',
        children='Current Temperature:'
    ),
    html.Pre(
        id='daily-high',
        children='Daily High:'
    ),
    html.Pre(
        id='daily-low',
        children='Daily Low:'
    )]),
    html.Div([
    dcc.Graph(id='live-update-graph',style={'width':1200}),
    dcc.Interval(
        id='interval-component',
        interval=60000,
        n_intervals=0
    )])
])

url = "http://10.0.1.7:8080"

@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = (9/5) * data + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback(Output('daily-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_b(n):
    df = pd.read_csv('../../temptest.txt')
    daily_high = df['Y'].max()
    return 'Daily High: {:.1f}'.format(daily_high)

@app.callback(Output('daily-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_c(n):
    df = pd.read_csv('../../temptest.txt')
    daily_low = df['Y'].min()
    return 'Daily Low: {:.1f}'.format(daily_low)

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


if __name__ == '__main__':
    app.run_server()