import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd
import time
from datetime import datetime as dt

url = "http://10.0.1.7:8080"

df = pd.read_csv('../../tempjan19.csv', header=None)

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
                                html.Div('Week', style={'text-align': 'center'}),
                            ],
                                className='round1'
                            ),
                            
                        ],
                            className='twelve columns'
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

@app.callback([
    Output('daily-high', 'children'),
    Output('daily-low', 'children')],
    [Input('interval-component', 'n_intervals'),
    Input('daily-data', 'children')])
def update_daily_stats(n, daily_data):
    daily_df = pd.read_json(daily_data)
    daily_max = daily_df[1].max()
    daily_min = daily_df[1].min()

    return html.H5('Daily High: {:.1f}'.format(daily_max)), html.H5('Daily Low: {:.1f}'.format(daily_min))
    
@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

@app.callback([
    Output('daily-data', 'children'),
    Output('yest', 'children')],
    [Input('interval-component', 'n_intervals')])
def process_df_daily(n):
    df_stats = df
    df_stats['datetime'] = pd.to_datetime(df_stats[0])
    df_stats = df_stats.set_index('datetime')

    td = dt.now().day
    tm = dt.now().month
    ty = dt.now().year

    dfd = df_stats[df_stats.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty] 

    months = {1:31, 2:31, 3:28, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    months_ly = {1:31, 2:31, 3:29, 4:31, 5:30, 6:31, 7:30, 8:31, 9:31, 10:30, 11:31, 12:30}
    print(months.get(tm))

    if td > 1:
        df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    elif td == 1:
        df_yest = df_stats[(df_stats.index.day == months.get(tm)) & (df_stats.index.month == tm-1) & (df_stats.index.year == ty)]

    # long_months = [1,3,5,7,8,10,12]
    # short_months = [4,6,9,11]
    # february = 2
    # df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm-1) & (df_stats.index.year == ty-1)] 
    # if tm in long_months and td > 1:
    #     df_yest = df_stats[(df_stats.index.day == td-1) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    # elif tm in long_months and td == 1:
    #     df_yest = df_stats[(df_stats.index.day == 30) & (df_stats.index.month == tm) & (df_stats.index.year == ty)]
    # print(df_yest)

    
    return dfdmy.to_json(), df_yest.to_json()  

@app.callback(Output('live-graph', 'figure'),
            [Input('interval-component-graph', 'n_intervals'),
            Input('daily-data', 'children'),
            Input('yest', 'children')])
def update_graph(n, daily_data, yest):
    dfdmy = pd.read_json(daily_data)
    dfdmy['time'] = pd.to_datetime(dfdmy[0])
    dfdmy['time'] = dfdmy['time'].dt.strftime('%H:%M')
    print(type(dfdmy[1][0]))
    yest = pd.read_json(yest)
    # yest['today']=dfdmy[1]
    # dfdmy['yest']=yest[1]
    print(yest)
    yest['time'] = pd.to_datetime(yest[0])
    yest['time'] = yest['time'].dt.strftime('%H:%M')
    # dfdmy['date'] = pd.to_datetime(dfdmy[0])
    # dfdmy['date']= dfdmy['date'].dt.strftime('%m-%d %H:%M:%S')
    print(yest)
    data = [
        go.Scatter(
            x = yest['time'],
            y = yest[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'orange',
            ),
        ),
        go.Scatter(
            x = dfdmy['time'],
            y = dfdmy[1],
            mode = 'markers+lines',
            marker = dict(
                color = 'black',
            ),
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