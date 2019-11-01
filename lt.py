import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd
import time
from datetime import datetime

url = "http://10.0.1.7:8080"

df = pd.read_csv('../../tempjan19.csv', header=None)

print(df)

def get_layout():
    return html.Div(
        [
            html.Div([
                html.Div(id='live-thermometer', style={'color':'green', 'font-size': 40, 'font-family':'sans-serif'})
            ]),
            html.Div([
                dcc.Interval(
                    id='interval-component-graph',
                    interval=900000,
                    n_intervals=0
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=60000,
                    n_intervals=0
                ),
            ]),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='live-graph'
                    ),
                ],
                    className='eight columns'
                ),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div(id='daily-high', style={'color':'red'})
                        ],
                            className='round1'
                        ),
                    ],
                        className='row'
                    ),
                ],
                className='four columns'
                ),
            ],
                className='row'
            ),
            html.Div(id='daily-data', style={'display': 'none'})
        ]

    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

# @app.callback(
#     Output('graph', 'children'),
#     [Input('product', 'value')])
# def display_graph(value):
#     print(value)
#     if value == 'live-graph':
#         return dcc.Graph(id='live-graph')

@app.callback(
    Output('daily-high', 'children'),
    [Input('interval-component', 'n_intervals'),
    Input('daily-data', 'children')])
def update_daily_stats(n, daily_data):
    daily_df = pd.read_json(daily_data)
    daily_max = daily_df[1].max()

    return html.Div('Daily High: {:.1f}'.format(daily_max))
    
@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback(Output('daily-data', 'children'),
            [Input('interval-component', 'n_intervals')])
def process_df_daily(n):
    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')

    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year

    dfd = df_stats[df_stats.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]  

    return dfdmy.to_json()  

@app.callback(Output('live-graph', 'figure'),
            [Input('interval-component-graph', 'n_intervals'),
            Input('daily-data', 'children')])
def update_graph(n, daily_data):
    dfdmy = pd.read_json(daily_data)
    # df_live = df
    
    # df_live['datetime'] = pd.to_datetime(df_live[0])
    # df_live = df_live.set_index('datetime')
    # print(df_live)
    # td = datetime.now().day
    # tm = datetime.now().month
    # print(tm)
    # ty = datetime.now().year
    # dfd = df_live[df_live.index.day == td]
    # dfdm = dfd[dfd.index.month == tm]
    # dfdmy = dfdm[dfdm.index.year == ty]
    # print(dfdmy)
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

if __name__ == "__main__":
    app.run_server(port=8050, debug=False)