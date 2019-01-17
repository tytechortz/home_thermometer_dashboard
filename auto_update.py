import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

app = dash.Dash()

counter_list = []

url = "http://10.0.1.7:8080"
    # A fake header is necessary to access the site: 
r = requests.get(url)
print(r.text)

