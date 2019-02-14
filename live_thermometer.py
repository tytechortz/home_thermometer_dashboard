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


cdaf = 0

colors = {
         'background': '#0000FF',
         'color': '#FFA500'
}

app.layout = html.Div([
    html.Div([
    html.Div(
        style={'color': 'green', 'font-size':35},
        id='live-thermometer',
        children='Current Temperature:'
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='daily-high',
        children='Daily High:'
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='monthly-high',
        children='Monthly High:'
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yearly-high',
        children='Yearly High:'
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='record-high',
        children='Record High:'
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='daily-low',
        children='Daily Low:'
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='monthly-high-date',
        children=''
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yearly-high-date',
        children=''
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='record-high-date',
        children=''
    ),
    html.Div(
        style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yesterday-high',
        children="Yesterday's High:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='monthly-low',
        children='Monthly Low:'
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yearly-low',
        children="Yearly Low:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='record-low',
        children='Record Low:'
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yesterday-low',
        children="Yesterday's Low:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='monthly-low-date',
        children=''
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='yearly-low-date',
        children=''
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='record-low-date',
        children=''
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
    ]),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='high-below-freezing',
        children="Days High Below Freezing:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='days-over-32',
        children="Days Above Freezing:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='days-over-40',
        children="Days Above 40:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='days-over-50',
        children="Days Above 50:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-high-below-freezing',
        children="Last Year:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-32',
        children="Last Year:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-40',
        children="Last Year:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-50',
        children="Last Year:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='total-days-over-60',
        children="Total Days Above 60:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='total-days-over-70',
        children="Total Days Above 70:"
    ),
     html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='days-over-80',
        children="Days Above 80:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='days-over-90',
        children="Days Above 90:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-60',
        children="Last Year Days Above 60:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-70',
        children="Last Year Days Above 70:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-80',
        children="Last Year Days Above 80:"
    ),
    html.Div(
        style={'color': 'blue', 'font-size':20, 'width': '24%', 'display':'inline-block'},
        id='ly-days-over-90',
        children="Last Year Days Above 90:"
    ),
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
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfd = df[df.index.day == td]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]
    daily_high = dfdmy[1].max()
    return 'Daily High: {:.1f}'.format(daily_high)

@app.callback(Output('daily-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_c(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
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
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
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
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
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
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
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
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
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
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    record_high = df[1].max()
    return 'Record High: {:.1f}'.format(record_high)

@app.callback(Output('record-low', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_i(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    record_low = df[1].min()
    return 'Record Low: {:.1f}'.format(record_low)

@app.callback(Output('yesterday-high', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_j(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tdy = td - 1
    tm = datetime.now().month
    ty = datetime.now().year
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
    td = datetime.now().day
    tdy = td - 1
    tm = datetime.now().month
    ty = datetime.now().year
    dfd = df[df.index.day == tdy]
    dfdm = dfd[dfd.index.month == tm]
    dfdmy = dfdm[dfdm.index.year == ty]

    yesterday_low = dfdmy[1].min()
    return "Yesterday's Low: {:.1f}".format(yesterday_low)

@app.callback(Output('monthly-high-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_l(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfm = df[df.index.month == tm]
    dfmy = dfm[dfm.index.year == ty]
    monthly_high_date = dfmy[1].idxmax()
    return "{}".format(monthly_high_date)

@app.callback(Output('monthly-low-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_m(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfm = df[df.index.month == tm]
    dfmy = dfm[dfm.index.year == ty]
    monthly_low_date = dfmy[1].idxmin()
    return '{}'.format(monthly_low_date)

@app.callback(Output('yearly-high-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_n(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    # dfm = df[df.index.month == tm]
    dfy = df[df.index.year == ty]
    yearly_high_date = dfy[1].idxmax()
    return "{}".format(yearly_high_date)

@app.callback(Output('yearly-low-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_o(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    # dfm = df[df.index.month == tm]
    dfy = df[df.index.year == ty]
    yearly_low_date = dfy[1].idxmin()
    return '{}'.format(yearly_low_date)

@app.callback(Output('record-high-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_p(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    record_high_date = df[1].idxmax()
    return '{}'.format(record_high_date)

@app.callback(Output('record-low-date', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_q(n):
    df = pd.read_csv('../../tempjan19.csv', header=None)
    df['datetime'] = pd.to_datetime(df[0])
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    df = df.set_index('datetime')
    record_low_date = df[1].idxmin()
    return '{}'.format(record_low_date)

@app.callback(Output('live-update-graph', 'figure'),
            [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
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
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == ty]
    dfly = df[df.index.year == tly]
    df_max1 = dfy.resample('D').max()
    df_max2 = dfly.resample('D').max()
    print(df_max1)
    print(df_max2)

    trace2 = go.Histogram(
        x=df_max1[1],
        opacity=0.55,
        xbins=dict(size=10)
    )
    
    trace1 = go.Histogram(
        x=df_max2[1],
        opacity=0.55,
        xbins=dict(size=10)
    )
    data = [trace1, trace2]

    fig = go.Figure(
        data = data,
        layout = go.Layout(barmode='overlay')
        )
    return fig

@app.callback(Output('high-below-freezing', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_r(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_below_freezing = (df_max[df_max[1] < 32].count()[1])

    return 'Days High Below Freezing = {}'.format(days_below_freezing)

@app.callback(Output('days-over-32', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_s(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_freezing = (df_max[df_max[1] > 32].count()[1])

    return 'Days Above Freezing = {}'.format(days_over_freezing)

@app.callback(Output('days-over-40', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_t(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_40 = (df_max[df_max[1] >= 40].count()[1])
    return 'Days Above 40 = {}'.format(days_over_40)

@app.callback(Output('days-over-50', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_u(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_50 = (df_max[df_max[1] >= 50].count()[1])
    return 'Days Above 50 = {}'.format(days_over_50)

@app.callback(Output('ly-days-high-below-freezing', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_v(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_below_freezing = (df_max[df_max[1] < 32].count()[1])

    return 'Last Year = {}'.format(ly_days_below_freezing)

@app.callback(Output('total-days-over-70', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_w(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_70 = (df_max[df_max[1] >= 70].count()[1])
    return 'Total Days Above 70 = {}'.format(days_over_70)

@app.callback(Output('total-days-over-60', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_60 = (df_max[df_max[1] >= 60].count()[1])
    return 'Total Days Above 60 = {}'.format(days_over_60)

@app.callback(Output('ly-days-over-32', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_s(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_freezing = (df_max[df_max[1] > 32].count()[1])

    return 'Last Year = {}'.format(ly_days_over_freezing)

@app.callback(Output('ly-days-over-40', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_40 = (df_max[df_max[1] >= 40].count()[1])
    return 'Last Year = {}'.format(ly_days_over_40)

@app.callback(Output('ly-days-over-50', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_50 = (df_max[df_max[1] >= 50].count()[1])
    return 'Last Year = {}'.format(ly_days_over_50)

@app.callback(Output('days-over-80', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_80 = (df_max[df_max[1] >= 80].count()[1])
    return 'Days Above 80 = {}'.format(days_over_80)

@app.callback(Output('days-over-90', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    dfy = df[df.index.year == ty]
    df_max = dfy.resample('D').max()
    days_over_90 = (df_max[df_max[1] >= 90].count()[1])
    return 'Days Above 90 = {}'.format(days_over_90)

@app.callback(Output('ly-days-over-60', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_60 = (df_max[df_max[1] >= 60].count()[1])
    return 'Last Year = {}'.format(ly_days_over_60)

@app.callback(Output('ly-days-over-70', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_70 = (df_max[df_max[1] >= 70].count()[1])
    return 'Last Year = {}'.format(ly_days_over_70)

@app.callback(Output('ly-days-over-80', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_80 = (df_max[df_max[1] >= 80].count()[1])
    return 'Last Year = {}'.format(ly_days_over_80)

@app.callback(Output('ly-days-over-90', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout_x(n):
    df = pd.read_csv('../../tempjan19.csv',header=None)
    df['datetime'] = pd.to_datetime(df[0])
    df = df.set_index('datetime')
    td = datetime.now().day
    tm = datetime.now().month
    ty = datetime.now().year
    tly = ty - 1
    dfy = df[df.index.year == tly]
    df_max = dfy.resample('D').max()
    ly_days_over_90 = (df_max[df_max[1] >= 90].count()[1])
    return 'Last Year = {}'.format(ly_days_over_90)

if __name__ == '__main__':
    app.run_server()