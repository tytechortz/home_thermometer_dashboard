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

df = pd.read_csv('../../tempjan19.csv')

td = datetime.now().day
tm = datetime.now().month
ty = datetime.now().year

tdy = td - 1


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
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='daily-high',
        children='Daily High:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='monthly-high',
        children='Monthly High:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yearly-high',
        children='Yearly High:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='record-high',
        children='Record High:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='daily-low',
        children='Daily Low:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='monthly-low',
        children='Monthly Low:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yearly-low',
        children='Yearly Low:'
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='record-low',
        children='Record Low:'
    ),
    html.Pre(
        style={'color': 'red', 'font-size':20, 'width': '100%', 'display':'inline-block'},
        id='yesterday-high',
        children="Yesterday's High:"
    ),
    html.Pre(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yesterday-low',
        children="Yesterday's Low:"
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
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfd = df[df.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    daily_high = dfdm[1].max()
    return 'Daily High: {:.1f}'.format(daily_high)

@app.callback(Output('daily-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_c(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfd = df[df.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    daily_low = dfdmy[1].min()
    return 'Daily Low: {:.1f}'.format(daily_low)

@app.callback(Output('monthly-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_d(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfm = df[df.index.month == tm]
    dfmy = dfm[dfm.index.year == ty]

    monthly_high = dfmy[1].max()
    return 'Monthly High: {:.1f}'.format(monthly_high)

@app.callback(Output('monthly-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_e(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfm = df[df.index.month == tm]
    dfmy = dfm[dfm.index.year == ty]
    monthly_low = dfmy[1].min()
    return 'Monthly Low: {:.1f}'.format(monthly_low)

@app.callback(Output('yearly-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_f(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfy = df[df.index.year == ty]
    # dfy = dfy[dfy.index.year == tm]
    yearly_high = dfy[1].max()
    return 'Yearly High: {:.1f}'.format(yearly_high)

@app.callback(Output('yearly-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_g(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfy = df[df.index.year == ty]
    # dfy = dfy[dfy.index.year == tm]
    yearly_low = dfy[1].min()
    return 'Yearly Low: {:.1f}'.format(yearly_low)

@app.callback(Output('record-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_h(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    record_high = df[1].max()
    return 'Record High: {:.1f}'.format(record_high)

@app.callback(Output('record-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_i(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')

    record_low = df[1].min()
    return 'Record Low: {:.1f}'.format(record_low)

@app.callback(Output('yesterday-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_j(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfd = df[df.index.day == tdy]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    yesterday_high = dfdmy[1].max()
    return "Yesterday's High: {:.1f}".format(yesterday_high)

@app.callback(Output('yesterday-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_k(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    dfd = df[df.index.day == tdy]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]

    yesterday_low = dfdmy[1].min()
    return "Yesterday's Low: {:.1f}".format(yesterday_low)

@app.callback(Output('live-update-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    # df.drop(['X'], axis=1, inplace=True)
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
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    


    fig = go.Figure(
        data = [go.Histogram(
            x=df_max[1],
            xbins=dict(size=10)
        )])
    return fig




if __name__ == '__main__':
    app.run_server()