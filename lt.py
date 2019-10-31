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

def get_layout():
    return html.Div(
        [
            html.Div([
                html.Div(id='live-thermometer', style={'color':'green'})
            ]),
            html.Div([
                dcc.Interval(
                    id='interval-component-thermometer',
                    interval=900000,
                    n_intervals=0
                ),
            ])
        ],

    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(Output('live-thermometer', 'children'),
              [Input('interval-component-thermometer', 'n_intervals')])
def update_layout(n):
    res = requests.get(url)
    data = res.json()
    f = ((9.0/5.0) * data) + 32
    return 'Current Temperature: {:.1f}'.format(f)

if __name__ == "__main__":
    app.run_server(port=8050, debug=False)