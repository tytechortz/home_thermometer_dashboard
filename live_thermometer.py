import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import requests
import pandas as pd 
import time
import datetime

app = dash.Dash(__name__)

df = pd.read_csv('../../temptest.txt')

colors = {
         'background': '#0000FF',
         'color': '#FFA500'
}

app.layout = html.Div([
    html.Div([
    html.Pre(
        style={'color': 'green', 'font-size':35},
        id='live-thermometer',
        children='Current Temperature:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20},
        id='daily-high',
        children='Daily High:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20},
        id='daily-low',
        children='Daily Low:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':15},
        id='monthly-high',
        children='Monthly High:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':15},
        id='monthly-low',
        children='Monthly Low:'
    ),
    ]),
    html.Div([
    dcc.Graph(id='live-update-graph',style={'width':1200}),
    dcc.Interval(
        id='interval-component',
        interval=60000,
        n_intervals=0
    )]),
    html.Div([
    dcc.Graph(id='temp-histogram',style={'width':600})
    ])
])

url = "http://10.0.1.7:8080"

@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback(Output('daily-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_b(n):
    df = pd.read_csv('../../temptest.txt')
    df['datetime'] = pd.to_datetime(df['X'])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    td = datetime.date.today().strftime("%d")
    td = int(td)
    df = df[df.index.day == td]
    daily_high = df['Y'].max()
    return 'Daily High: {:.1f}'.format(daily_high)

@app.callback(Output('daily-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_c(n):
    df = pd.read_csv('../../temptest.txt')
    df['datetime'] = pd.to_datetime(df['X'])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    td = datetime.date.today().strftime("%d")
    td = int(td)
    df = df[df.index.day == td]
    daily_low = df['Y'].min()
    return 'Daily Low: {:.1f}'.format(daily_low)

@app.callback(Output('monthly-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_d(n):
    df = pd.read_csv('../../tempjan19.txt', header=None)
    monthly_high = df[1].max()
    return 'Monthly High: {:.1f}'.format(monthly_high)

@app.callback(Output('monthly-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_e(n):
    df = pd.read_csv('../../tempjan19.txt', header=None)
    monthly_low = df[1].min()
    return 'Monthly Low: {:.1f}'.format(monthly_low)

@app.callback(Output('live-update-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('../../temptest.txt')
    df['datetime'] = pd.to_datetime(df['X'])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    td = datetime.date.today().strftime("%d")
    td = int(td)
    df = df[df.index.day == td]

    fig = go.Figure(
        data = [go.Scatter(
            x = df['X'],
            y = df['Y'],
            mode = 'markers+lines',
            marker=dict(
                color = 'orange',
            ),

        )])
    return fig 

@app.callback(Output('temp-histogram','figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('../../tempjan19.txt', header=None)
    fig = go.Figure(
        data = [go.Histogram(
            x=df[1]
        )]
    )



if __name__ == '__main__':
    app.run_server()