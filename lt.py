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
import collections

url = "http://10.0.1.7:8080"

# df = pd.read_csv('../../tempjan19.csv', header=None)

# print(df)
today = time.strftime("%Y-%m-%d")

def get_layout():
    return html.Div(
        [
            html.Div([
                html.Div([
                    html.Div(id='live-thermometer', style={'color':'green', 'font-size': 40, 'font-family':'sans-serif'})
                ],
                className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id='graph-picker',
                        options=[
                            {'label':'Live', 'value':'live-graph'},
                            {'label':'Past', 'value':'past-graph'},
                        ],
                        value='live-graph',
                        labelStyle={'display':'inline'},
                    )
                ]),
                html.Div([
                    dcc.DatePickerSingle(
                        id='date-picker',
                        date=today
                    ),
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
                                html.Div([
                                    html.P('Record Highs', style={'color':'red', 'text-align':'center'}),
                                    html.Div(id='rec-high-count', style={'color':'red', 'text-align':'center'}),
                                ])
                            ],
                                className='round1'
                            ), 
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P('Record Lows', style={'color':'blue', 'text-align':'center'}),
                                    html.Div(id='rec-low-count', style={'color':'blue', 'text-align':'center'}),
                                ])
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
                html.Div([
                    html.Div(id='graph'),
                ],
                    className='eight columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P('High Lows', style={'color':'red', 'text-align':'center'}),
                                    html.Div(id='high-low-count', style={'color':'red', 'text-align':'center'}),
                                ])
                            ],
                                className='round1'
                            ), 
                        ],
                            className='six columns'
                        ),
                        html.Div([
                            html.Div([
                                html.P('Place Holder 2')
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
            # html.Div([
            #     html.Div([
            #         html.Div([
            #             html.Div([
            #                 html.Div([
            #                     html.Div([
            #                         html.P('High Lows', style={'color':'red', 'text-align':'center'}),
            #                         html.Div(id='high-low-count', style={'color':'red', 'text-align':'center'}),
            #                     ])
            #                 ],
            #                     className='round1'
            #                 ), 
            #             ],
            #                 className='six columns'
            #             ),
            #             html.Div([
            #                 html.Div([
            #                     html.Div([
            #                         html.P('Low Highs', style={'color':'blue', 'text-align':'center'}),
            #                         html.Div(id='low-high-count', style={'color':'blue', 'text-align':'center'}),
            #                     ])
            #                 ],
            #                     className='round1'
            #                 ), 
            #             ],
            #                 className='six columns'
            #             ),
            #         ],
            #             className='four columns'
            #         ),
            #         html.Div([
            #             html.P('Placeholder', style={'text-align':'center'})
            #         ],
            #             # className='round1'
            #         ),
            #     ],
            #         className='four columns'
            #     ),
            # ],
            #     className='row'
            # ),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.P('Averages YTD', style={'text-align':'center'})
                            ])
                        ],
                            className='round1'
                        ),
                        html.Div([
                        #     html.Div([

                        #     ],
                        #         className=
                        #     ),
                        ],
                            className='row'
                        ),
                    ],
                        className='four columns'
                    ),
                    html.Div([
                        html.P('Placeholder', style={'text-align':'center'})
                    ],
                        # className='round1'
                    ),
                ],
                    className='twelve columns'
                ),
                
                   
            ],
                className='row'
            ),
            html.Div(id='daily-data', style={'display': 'none'}),
            html.Div(id='y2018', style={'display': 'none'}),
            html.Div(id='y2019', style={'display': 'none'}),
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
    Output('graph', 'children'),
    [Input('graph-picker', 'value')])
def select_graph(selected_graph):
    print(selected_graph)
    if selected_graph == 'live-graph':
        return dcc.Graph(id='live-graph')
    elif selected_graph == 'past-graph':
        return dcc.Graph(id='past-graph')

@app.callback([
    Output('rec-high-count', 'children'),
    Output('rec-low-count', 'children')],
    [Input('interval-component-graph', 'n_intervals')])
def update_daily_stats(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')
   
    daily_highs = df_s.resample('D').max()
    daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax()
    rh_tot = daily_high[1]

    daily_lows = df_s.resample('D').min()
    daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin()
    rl_tot = daily_low[1]

    h_years = rh_tot.tolist()
    l_years = rl_tot.tolist()

    h_year_list = []
    for x in h_years:
        h_year_list.append(x.year)

    l_year_list = []
    for x in l_years:
        l_year_list.append(x.year)
    
    h_counts = collections.Counter(h_year_list)
    l_counts = collections.Counter(l_year_list)

    return [html.Div([
        html.P('2018: {}'.format(h_counts[2018])), 
        html.P('2019: {}'.format(h_counts[2019])),
        html.P('2020: {}'.format(h_counts[2020])),
    ]),
    html.Div([
        html.P('2018: {}'.format(l_counts[2018])), 
        html.P('2019: {}'.format(l_counts[2019])),
        html.P('2020: {}'.format(l_counts[2020])),
    ])]

@app.callback([
    Output('high-low-count', 'children'),
    Output('low-high-count', 'children')],
    [Input('interval-component-graph', 'n_intervals')])
def low_high_stats(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df_s = df
    df_s['date'] = pd.to_datetime(df_s[0])
    df_s = df_s.set_index('date')
    print(df_s)
   
    daily_highs = df_s.resample('D').max()
    daily_high = daily_highs.groupby([daily_highs.index.month, daily_highs.index.day]).idxmax()
    h_l_tot = daily_high[1]

    daily_lows = df_s.resample('D').min()
    daily_low = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).idxmin()
    l_h_tot = daily_low[1]

    h_l_years = h_l_tot.tolist()
    l_h_years = l_h_tot.tolist()

    h_l_year_list = []
    for x in h_l_years:
        h_l_year_list.append(x.year)

    l_h_year_list = []
    for x in l_h_years:
        l_h_year_list.append(x.year)
    
    h_l_counts = collections.Counter(h_l_year_list)
    l_h_counts = collections.Counter(l_h_year_list)

    return [html.Div([
        html.P('2018: {}'.format(h_l_counts[2018])), 
        html.P('2019: {}'.format(h_l_counts[2019])),
        html.P('2020: {}'.format(h_l_counts[2020])),
    ]),
    html.Div([
        html.P('2018: {}'.format(l_h_counts[2018])), 
        html.P('2019: {}'.format(l_h_counts[2019])),
        html.P('2020: {}'.format(l_h_counts[2020])),
    ])]

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

    return html.P('High: {:.1f}'.format(record_high.iloc[0,1])), html.P('Low: {:.1f}'.format(record_low.iloc[0,1]))
   
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
    Output('y2018', 'children'),
    Output('y2019', 'children'),
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
    df2018 = dfdm[dfdm.index.year == 2018]
    df2019 = dfdm[dfdm.index.year == 2019]
    # print(dfly)
   
    record_high_temps = df_stats.groupby(df_stats.index.strftime('%m-%d')).max()
    # print(record_high_temps)
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

    return (dfdmy.to_json(), df2018.to_json(), df2019.to_json(), dfly.to_json(), df_yest.to_json(), record_high_temps.to_json(), record_low_temps.to_json(), 
        html.P('{}'.format(rec_high_date)), 
        html.P('{}'.format(rec_low_date)), 
        html.P('LH: {:.1f}'.format(rec_low_high)), 
        html.P('{}'.format(rec_low_high_date)), 
        html.P('HL: {:.1f}'.format(rec_high_low)), 
        html.P('{}'.format(rec_high_low_date)))



@app.callback(
    Output('past-graph', 'figure'),
    [Input('date-picker', 'date'),
    Input('daily-data', 'children'),
    Input('graph-picker', 'value'),
    Input('last-year', 'children')])
def hist_graph(selected_date, daily_data, selected_graph, last_year):
    td = int(selected_date[8:])
    tm = int(selected_date[5:7])
    ty = int(selected_date[0:4])

    today = time.strftime("%Y-%m-%d")
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['time'] = pd.to_datetime(df[0])
    df = df.set_index('time')
   
    years = list(df.index.year.drop_duplicates())
    years = [x for x in years if str(x) != 'nan']
    years = [int(i) for i in years]

    if today >= selected_date:

        today_data = df.loc[selected_date]
        data = []
        frames = []

        for year in years:
            frames.append(df.loc[str(year)+'-'+str(tm)+'-'+str(td)])

        for frame in frames:
            data.append(go.Scatter(
                x = frame.index.strftime('%H:%M'),
                y = frame[1],
                mode = 'markers+lines',
                name = frame.index[0].year
            ))
    else:
        today_data = df.loc[selected_date]
        data = []
        frames = []

        for year in years[:-1]:
            frames.append(df.loc[str(year)+'-'+str(tm)+'-'+str(td)])

        for frame in frames:
            data.append(go.Scatter(
                x = frame.index.strftime('%H:%M'),
                y = frame[1],
                mode = 'markers+lines',
                name = frame.index[0].year
            ))

  
    # dfd = df[df.index.day == td]
    # dfdm = dfd[dfd.index.month == tm]
    # dfdmy = dfdm[dfdm.index.year == ty] 

    # data = [
        # go.Scatter(
        #     x = yest['time'],
        #     y = yest[1],
        #     mode = 'markers+lines',
        #     marker = dict(
        #         color = 'blue',
        #     ),
        #     name='yesterday'
        # ),
        # go.Scatter(
        #     x = today_data.index,
        #     y = today_data[1],
        #     mode = 'markers+lines',
        #     marker = dict(
        #         color = 'red',
        #     ),
        #     name='today'
        # ),
        # go.Scatter(
        #     x = dfly['time'],
        #     y = dfly[1],
        #     mode = 'markers+lines',
        #     marker = dict(
        #         color = 'gold',
        #     ),
        #     name='last year'
        # ),
    # ]
    layout = go.Layout(
        xaxis=dict(tickformat='%H%M'),
        height=500
    )


    return {'data': data, 'layout': layout}


@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
    Input('daily-data', 'children'),
    Input('last-year', 'children'),
    Input('y2018', 'children'),
    Input('y2019', 'children'),
    Input('graph-picker', 'value'),
    Input('yest', 'children')])
def update_graph(n, daily_data, last_year, y2018, y2019, selected_graph, yest):
    dfdmy = pd.read_json(daily_data)
    dfdmy['time'] = pd.to_datetime(dfdmy[0])
    dfdmy['time'] = dfdmy['time'].dt.strftime('%H:%M')
    yest = pd.read_json(yest)
    yest['time'] = pd.to_datetime(yest[0])
    yest['time'] = yest['time'].dt.strftime('%H:%M')

    dfly = pd.read_json(last_year)
    dfly['time'] = pd.to_datetime(dfly[0])
    dfly['time'] = dfly['time'].dt.strftime('%H:%M')

    df2018 = pd.read_json(y2018)
    df2018['time'] = pd.to_datetime(df2018[0])
    df2018['time'] = df2018['time'].dt.strftime('%H:%M')

    df2019 = pd.read_json(y2019)
    df2019['time'] = pd.to_datetime(df2019[0])
    df2019['time'] = df2019['time'].dt.strftime('%H:%M')

    # if selected_date == ''

    data = [
        go.Scatter(
            x = yest['time'],
            y = yest[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'black',
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
            x = df2018['time'],
            y = df2018[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'dodgerblue',
            ),
            name='2018'
        ),
        go.Scatter(
            x = df2019['time'],
            y = df2019[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'blue',
            ),
            name='2019'
        ),
    ]
    layout = go.Layout(
        xaxis=dict(tickformat='%H%M'),
        height=500
    )
    return {'data': data, 'layout': layout}
  

if __name__ == "__main__":
    app.run_server(port=8050, debug=False)