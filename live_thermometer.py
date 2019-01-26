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
        id='live_thermometer',
         children='Current Temperature:'
        ),
    ]),
    html.Div([
    dcc.Graph(id='live-update-graph',style={'width':1200}),
    dcc.Interval(
        id='interval-component',
        interval=60000,
        n_intervals=0
    )])
])


@app.callback(Output('live_thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    url = "http://10.0.1.7:8080"
    res = requests.get(url)
    data = res.json()
    return 'Current Temperature: {}'.format(data)

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