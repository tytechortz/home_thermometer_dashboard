import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import pandas as pd
import time
from datetime import datetime



def get_layout():
    return html.Div(
        [
            html.Div(
                style={'color': 'green', 'font-size':35},
                id='live-thermometer',
                children='Current Temperature:'
            ),
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

if __name__ == "__main__":
    app.run_server(port=8050, debug=False)