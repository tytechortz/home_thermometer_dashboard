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
                html.Div([
                    html.Div(id='live-thermometer', style={'color':'green', 'font-size': 40, 'font-family':'sans-serif'})
                ],
                className='six columns'
                ),
            html.Div([
                dcc.DatePickerSingle(
                    id='date-picker',
                    
                    )
            ]),
            ],
                className='row'
            ),
            
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
                                html.Div(id='rec-high-date', style={'color':'red', 'text-align':'center'}),
                                html.Div(id='rec-low-high', style={'color':'red', 'text-align':'center'}),
                                html.Div(id='rec-low-high-date', style={'color':'red', 'text-align':'center'}),
                            ],
                                className='round1'
                            ),
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            html.Div([
                                html.Div(id='rec-low', style={'color':'blue', 'text-align':'center'}),
                                html.Div(id='rec-low-date', style={'color':'blue', 'text-align':'center'}),
                                html.Div(id='rec-high-low', style={'color':'blue', 'text-align':'center'}),
                                html.Div(id='rec-high-low-date', style={'color':'blue', 'text-align':'center'}),
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
                                html.Div('Counts', style={'text-align': 'center'}),
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
                                html.Div(id='rec-high-count', style={'color':'blue', 'text-align':'center'}),
                            ])
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
            html.Div(id='last-year', style={'display': 'none'}),
            html.Div(id='yest', style={'display': 'none'}),
            html.Div(id='record-high-temps', style={'display': 'none'}),
            html.Div(id='record-low-temps', style={'display': 'none'}),
            html.Div(id='high-dates', style={'display': 'none'}),
            html.Div(id='low-dates', style={'display': 'none'}),
        ]

    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(
    Output('rec-high-count', 'children'),
    [Input('record-high-temps', 'children'),
    Input('record-low-temps', 'children'),
    Input('interval-component-graph', 'n_intervals')])
def update_daily_stats(record_highs, record_lows, n):
    record_highs = pd.read_json(record_highs)
    record_lows = pd.read_json(record_lows)
    print (record_highs)

    return None

@app.callback([
    Output('rec-high', 'children'),
    Output('rec-low', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('record-high-temps', 'children'),
    Input('record-low-temps', 'children')])
def update_daily_stats(n, record_highs, record_lows):
    record_highs = pd.read_json(record_highs)
    record_lows = pd.read_json(record_lows)

    today = time.strftime("%m-%d")
    record_high = record_highs.loc[record_highs.index == today]
    record_low = record_lows.loc[record_lows.index == today]

    return html.P('High: {:.1f}'.format(record_high.iloc[0,1])), html.P('Low: {:.1f}'.format(record_low.iloc[0,1])),
   
@app.callback([
    Output('daily-high', 'children'),
    Output('daily-low', 'children')],
    [Input('interval-component-graph', 'n_intervals'),
    Input('daily-data', 'children')])
def update_daily_stats(n, daily_data):
    daily_df = pd.read_json(daily_data)
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
    Output('last-year', 'children'),
    Output('yest', 'children'),
    Output('record-high-temps', 'children'),
    Output('record-low-temps', 'children'),
    Output('rec-high-date', 'children'),
    Output('rec-low-date', 'children'),
    Output('rec-low-high', 'children'),
    Output('rec-low-high-date', 'children'),
    Output('rec-high-low', 'children'),
    Output('rec-high-low-date', 'children')],
    [Input('interval-component-graph', 'n_intervals')])
def process_df_daily(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
   
    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')
    today = time.strftime("%m-%d")
    
    td = dt.now().day
    tm = dt.now().month
    ty = dt.now().year
    ly = ty-1
    # print(ly)

    dfd = df_stats[df_stats.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty] 
    # print(dfdmy)

    dfly = dfdm[dfdm.index.year == ly]
    # print(dfly)
   
    record_high_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    record_highs = df_stats.resample('D').max()
    daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).max()
    low_daily_highs = record_highs.groupby([record_highs.index.month, record_highs.index.day]).min()
    low_daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmin()
    daily_highs_date = record_highs.groupby([record_highs.index.month, record_highs.index.day]).idxmax()
    rec_high_date = daily_highs_date.loc[(tm,td), 1].year
    rec_low_high = low_daily_highs.loc[(tm,td), 1]
    rec_low_high_date = low_daily_highs_date.loc[(tm,td), 1].year
    
    record_low_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).min()
    record_lows = df_stats.resample('D').min()
    daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).min()
    high_daily_lows = record_lows.groupby([record_lows.index.month, record_lows.index.day]).max()
    high_daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmax()
    daily_lows_date = record_lows.groupby([record_lows.index.month, record_lows.index.day]).idxmin()
    rec_low_date = daily_lows_date.loc[(tm,td), 1].year
    rec_high_low = high_daily_lows.loc[(tm,td), 1]
    rec_high_low_date = high_daily_lows_date.loc[(tm,td), 1].year

    months = {1:31, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    months_ly = {1:31, 2:31, 3:29, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}

    if td > 1:
        df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    elif td == 1:
        df_yest = df_stats[(df_stats.index.day == months.get(tm)) & (df_stats.index.month == tm-1) & (df_stats.index.year == ty)]

    return dfdmy.to_json(), dfly.to_json(), df_yest.to_json(), record_high_temps.to_json(), record_low_temps.to_json(), html.P('{}'.format(rec_high_date)), html.P('{}'.format(rec_low_date)), html.P('LH: {:.1f}'.format(rec_low_high)), html.P('{}'.format(rec_low_high_date)), html.P('HL: {:.1f}'.format(rec_high_low)), html.P('{}'.format(rec_high_low_date))

@app.callback(Output('live-graph', 'figure'),
            [Input('interval-component-graph', 'n_intervals'),
            Input('daily-data', 'children'),
            Input('last-year', 'children'),
            Input('yest', 'children')])
def update_graph(n, daily_data, last_year, yest):
    dfdmy = pd.read_json(daily_data)
    dfdmy['time'] = pd.to_datetime(dfdmy[0])
    dfdmy['time'] = dfdmy['time'].dt.strftime('%H:%M')
    yest = pd.read_json(yest)
    yest['time'] = pd.to_datetime(yest[0])
    yest['time'] = yest['time'].dt.strftime('%H:%M')

    dfly = pd.read_json(last_year)
    dfly['time'] = pd.to_datetime(dfly[0])
    dfly['time'] = dfly['time'].dt.strftime('%H:%M')

    data = [
        go.Scatter(
            x = yest['time'],
            y = yest[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'blue',
            ),
            name='yesterday'
        ),
        go.Scatter(
            x = dfdmy['time'],
            y = dfdmy[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'red',
            ),
            name='today'
        ),
        go.Scatter(
            x = dfly['time'],
            y = dfly[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'gold',
            ),
            name='last year'
        ),
    ]
    layout = go.Layout(
        xaxis=dict(tickformat='%H%M'),
        height=500
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