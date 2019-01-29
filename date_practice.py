import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import requests
import pandas as pd 
import time
import datetime

# df = pd.read_csv('../../temptest.txt',
# parse_dates=['X'],
# index_col = 'X')

df = pd.read_csv('../../temptest.txt')



df['datetime'] = pd.to_datetime(df['X'])
df = df.set_index('datetime')
df.drop(['X'], axis=1, inplace=True)

td = datetime.date.today().strftime("%d")

# print(datetime.date.today().strftime("%d"))
td = int(td)
print(td)
print(df[df.index.day == td])

