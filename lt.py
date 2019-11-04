import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd
import time
from datetime import datetime as dt
import re

url = "http://10.0.1.7:8080"

# df = pd.read_csv('../../tempjan19.csv', header=None)

# print(df)

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
                            html.Div([
                                html.Div('Today', style={'text-align': 'center'}),
                            ],
                                className='round1'
                            ),
                        ],
                            className='twelve columns'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(id='daily-high', style={'color':'red', 'text-align':'center'})
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            html.Div([
                                html.Div(id='daily-low', style={'color':'blue', 'text-align':'center'})
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div('Yesterday', style={'text-align': 'center'}),
                            ],
                                className='round1'
                            ),
                        ],
                            className='twelve columns'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(id='yest-high', style={'color':'red', 'text-align':'center'})
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            html.Div([
                                html.Div(id='yest-low', style={'color':'blue', 'text-align':'center'})
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div('Records', style={'text-align': 'center'}),
                            ],
                                className='round1'
                            ),
                        ],
                            className='twelve columns'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(id='rec-high', style={'color':'red', 'text-align':'center'}),
                                html.Div('record date', style={'color':'red', 'text-align':'center'})
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            html.Div([
                                html.Div(id='rec-low', style={'color':'blue', 'text-align':'center'})
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
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
            html.Div(id='daily-data', style={'display': 'none'}),
            html.Div(id='yest', style={'display': 'none'}),
            html.Div(id='record-highs', style={'display': 'none'}),
            html.Div(id='record-lows', style={'display': 'none'}),
        ]

    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback([
    Output('rec-high', 'children'),
    Output('rec-low', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('record-highs', 'children'),
    Input('record-lows', 'children')])
def update_daily_stats(n, record_highs, record_lows):
    record_highs = pd.read_json(record_highs)
    record_lows = pd.read_json(record_lows)
    # print(record_highs)
    today = time.strftime("%m-%d")
    # today = '01-05'
    # print(today)
    record_high = record_highs.loc[record_highs.index == today]
    # record_high_date = record_highs[0].loc[record_highs.index == today]
    # print(record_high_date)
    record_low = record_lows.loc[record_lows.index == today]
    # print(record_high)
    # print(type(record_high))
    # record_highs = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()

    return html.P('High: {:.1f}'.format(record_high.iloc[0,1])), html.P('Low: {:.1f}'.format(record_low.iloc[0,1]))

@app.callback([
    Output('daily-high', 'children'),
    Output('daily-low', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('daily-data', 'children')])
def update_daily_stats(n, daily_data):
    daily_df = pd.read_json(daily_data)
    print(daily_df)
    daily_max = daily_df[1].max()
    daily_min = daily_df[1].min()

    return html.H5('High: {:.1f}'.format(daily_max)), html.H5('Low: {:.1f}'.format(daily_min))

@app.callback([
    Output('yest-high', 'children'),
    Output('yest-low', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('yest', 'children')])
def update_daily_stats(n, yest):
    yest = pd.read_json(yest)
    yest_max = yest[1].max()
    yest_min = yest[1].min()

    return html.H5('High: {:.1f}'.format(yest_max)), html.H5('Low: {:.1f}'.format(yest_min))
    
@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback([
    Output('daily-data', 'children'),
    Output('yest', 'children'),
    Output('record-highs', 'children'),
    Output('record-lows', 'children')],
    [Input('interval-component-graph', 'n_intervals')])
def process_df_daily(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    # print(df)
    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')
    # print(df_stats)
    today = time.strftime("%m-%d")
    # dfdmy = df_stats.loc['2019-01-01']
    # print(dfdmy)
    td = dt.now().day
    tm = dt.now().month
    ty = dt.now().year

    # grouped_days = df_stats.groupby([df_stats.index.month, df_stats.index.day])
    # print(grouped_days)
    dfd = df_stats[df_stats.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty] 
    # print(dfdmy)
    # dfdmy['Year'] = dfdmy.index.year
    
    # print(df_stats)
    # record_highs = df_stats.loc[df_stats.groupby(
    record_highs = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    # record_highs = df_stats.loc[today]
    # print(record_highs)
    record_lows = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()

    # df_stats['rh'] = df_stats.groupby([df_stats.index.month, df_stats.index.day], as_index=False).max()
   
    # daily_highs = df_stats.resample('D')[1].max()
    # print(daily_highs)
    # record_highs = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).max()

    # daily_highs['rec high'] = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).max()
    # record_highs = daily_highs.resample('D').max()
    # print(record_highs)

    # daily_lows = df_stats.resample('D')[1].min()
    # record_highs = df_stats.groupby(pd.Grouper(freq='D')).max()
    # print(daily_highs)
    # print(daily_lows)

    months = {1:31, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    months_ly = {1:31, 2:31, 3:29, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    # print(dfdmy)

    if td > 1:
        df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    elif td == 1:
        df_yest = df_stats[(df_stats.index.day == months.get(tm)) & (df_stats.index.month == tm-1) & (df_stats.index.year == ty)]

    return dfdmy.to_json(), df_yest.to_json(), record_highs.to_json(), record_lows.to_json()  

@app.callback(Output('live-graph', 'figure'),
            [Input('interval-component-graph', 'n_intervals'),
            Input('daily-data', 'children'),
            Input('yest', 'children')])
def update_graph(n, daily_data, yest):
    dfdmy = pd.read_json(daily_data)
    print(dfdmy)
    dfdmy['time'] = pd.to_datetime(dfdmy[0])
    dfdmy['time'] = dfdmy['time'].dt.strftime('%H:%M')
    yest = pd.read_json(yest)
    yest['time'] = pd.to_datetime(yest[0])
    yest['time'] = yest['time'].dt.strftime('%H:%M')
    data = [
        go.Scatter(
            x = yest['time'],
            y = yest[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'orange',
            ),
            name='yesterday'
        ),
        go.Scatter(
            x = dfdmy['time'],
            y = dfdmy[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'black',
            ),
            name='today'
        ),
    ]
    layout = go.Layout(
        xaxis=dict(tickformat='%H%M')
    )
    return {'data': data, 'layout': layout}
    # return {
    #     'data': [go.Scatter(
            
    #     )],
    #     'layout': go.Layout(
    #         xaxis=dict(
    #             tickformat='%H%M'
    #         )
    #     ),
    # }

if __name__ == "__main__":
    app.run_server(port=8050, debug=False)