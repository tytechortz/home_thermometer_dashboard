import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import requests
import pandas as pd 
import time
# import datetime
from datetime import datetime

app = dash.Dash(__name__)

df = pd.read_csv('../../all-temps-test.csv')

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
        style={'color': 'red', 'font-size':20, 'width': '31%', 'display':'inline-block'},
        id='daily-high',
        children='Daily High:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20, 'width': '31%', 'display':'inline-block'},
        id='monthly-high',
        children='Monthly High:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20, 'width': '31%', 'display':'inline-block'},
        id='yearly-high',
        children='Yearly High:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '31%', 'display':'inline-block'},
        id='daily-low',
        children='Daily Low:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '31%', 'display':'inline-block'},
        id='monthly-low',
        children='Monthly Low:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '31%', 'display':'inline-block'},
        id='yearly-low',
        children='Yearly Low:'
    ),

    ]),
    html.Div([
    dcc.Graph(id='live-update-graph',style={'width':1200}),
    dcc.Interval(
        id='interval-component',
        interval=900000,
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component-thermometer',
        interval=60000,
        n_intervals=0
    ),
    ]),
    html.Div([
    dcc.Graph(
        id='temp-histogram',
        style={'width':600},
        
        )
    ])
])

url = "http://10.0.1.7:8080"

@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component-thermometer', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback(Output('daily-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_b(n):
    df = pd.read_csv('../../all-temps-test.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    td = datetime.now().day
    tm = datetime.now().month
    dfd = df[df.index.day == td]
    dfmd = dfd[dfd.index.month == tm]
    daily_high = dfmd[1].max()
    return 'Daily High: {:.1f}'.format(daily_high)

@app.callback(Output('daily-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_c(n):
    df = pd.read_csv('../../all-temps-test.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfd = df[df.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    daily_low = dfdmy[1].min()
    return 'Daily Low: {:.1f}'.format(daily_low)

@app.callback(Output('monthly-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_d(n):
    df = pd.read_csv('../../all-temps-test.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    td = datetime.now().month
    td = int(td)
    df = df[df.index.month == td]

    monthly_high = df[1].max()
    return 'Monthly High: {:.1f}'.format(monthly_high)

@app.callback(Output('monthly-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_e(n):
    df = pd.read_csv('../../all-temps-test.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    td = datetime.now().month
    td = int(td)
    df = df[df.index.month == td]


    monthly_low = df[1].min()
    return 'Monthly Low: {:.1f}'.format(monthly_low)

@app.callback(Output('yearly-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_f(n):
    df = pd.read_csv('../../all-temps-test.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    # td = datetime.now().day
    tm = datetime.now().year
    dfy = df[df.index.year == tm]
    dfy = dfy[dfy.index.year == tm]
    yearly_high = dfy[1].max()
    return 'Yearly High: {:.1f}'.format(yearly_high)

@app.callback(Output('yearly-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_g(n):
    df = pd.read_csv('../../all-temps-test.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    # td = datetime.now().day
    tm = datetime.now().year
    dfy = df[df.index.year == tm]
    dfy = dfy[dfy.index.year == tm]
    yearly_low = dfy[1].min()
    return 'Yearly Low: {:.1f}'.format(yearly_low)

@app.callback(Output('live-update-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('../../all-temps-test.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)

    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfd = df[df.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    # df = df[df.index.day == td and df.index.month == tm]

    return {
        'data': [go.Scatter(
            x = dfdmy[0],
            y = dfdmy[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'orange',
            ), 
        )],
        'layout': go.Layout(
            xaxis=dict(
                tickformat='%H%M'
            )
        ),
    }

@app.callback(Output('temp-histogram','figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_a(n):
    df = pd.read_csv('../../all-temps-test.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    td = datetime.now().month
    td = int(td)
    df = df[df.index.month == td]
    fig = go.Figure(
        data = [go.Histogram(
            x=df[1],
            xbins=dict(size=1)
        )])
    return fig




if __name__ == '__main__':
    app.run_server()

